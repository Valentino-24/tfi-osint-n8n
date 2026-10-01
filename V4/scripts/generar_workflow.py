# -*- coding: utf-8 -*-
"""
Genera el workflow n8n del TFI OSINT V4 (B3).
Salida: V4/anexos/B_workflow.json — importable en n8n 2.22.6 (verificado contra nodos instalados).
Regenerable: ante cualquier cambio en el pipeline, se edita acá y se re-ejecuta.

Pipeline (2 triggers en un solo workflow):
  INGESTA  : Schedule 15min -> 3 subreddits (feed Atom RSS publico, sin OAuth) -> (A) upsert subreddits |
                                                                               (B) new/.rss -> parse -> HMAC -> clasificador -> entidades -> upsert posts
  ANOMALÍAS: Schedule 00:05 -> counts diarios SQL -> motor Poisson (q95 + mínimo absoluto)
             -> registrar eval. en anomalias + alerta condicional -> Telegram (opcional)

Nota: ingesta via RSS (feed Atom publico) porque la cuenta Reddit del usuario está bloqueada
para crear apps (https://www.reddit.com/prefs/apps) y los endpoints .json dan 403
("blocked by network security") desde esta IP. El rate limit publico alcanza: 3 requests por
ciclo de 15 min (limite ~10/min). Limitaciones RSS: sin score, num_comments ni suscriptores
(columnas quedan en 0). Si en el futuro se consigue una app de Reddit, se regenera con OAuth:
endpoints oauth.reddit.com + nodo Get Reddit Token + about.json.
"""
import json
import uuid
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "anexos" / "B_workflow.json"

# ----------------------------------------------------------------------
# Código JS de los nodos Code (n8n v2). r-strings: los backslashes JS quedan literales.
# ----------------------------------------------------------------------
# Sin OAuth: feed Atom RSS publico con User-Agent (cuenta Reddit bloqueada para crear apps, .json bloqueados por IP).
# Corpus mixto (change rediseno-diccionario-evaluacion, decision D-9).
# Criterio de inclusion: tema declarado de seguridad de la informacion, mas
# r/devsarg como comunidad tecnica argentina de referencia.
# OJO - el subreddit_id DEBE llevar la misma forma de mayusculas que aparece en
# los permalinks del feed, porque se deriva del enlace y se compara de forma
# exacta contra la FK posts_subreddit_id. Verificado contra feed real:
#   r/Malware       -> permalinks traen "Malware", NO "malware"
#   r/DerechoGenial -> permalinks traen "DerechoGenial"
# Escribirlo en minuscula revierte el bug de clave foranea corregido antes.
PREPARE_SUBS = r"""const subs = [
  { subreddit_id: 'netsec', display_name: 'r/netsec', rss_url: 'https://www.reddit.com/r/netsec/new/.rss?limit=100' },
  { subreddit_id: 'Malware', display_name: 'r/Malware', rss_url: 'https://www.reddit.com/r/Malware/new/.rss?limit=100' },
  { subreddit_id: 'devsarg', display_name: 'r/devsarg', rss_url: 'https://www.reddit.com/r/devsarg/new/.rss?limit=100' }
];
return subs;"""

PARSE_POSTS = r"""// Parser para feed Atom RSS de Reddit (nodo RSS Read, rss-parser).
// id y subreddit_id se derivan del link del post:
//   https://www.reddit.com/r/{sub}/comments/{id}/{slug}/
// limitaciones RSS: score y num_comments no vienen -> 0 (documentado).
//
// Descarte explicito de items con error (RN-FU-03 / D-10): cuando "Fetch Posts RSS" agota
// sus 3 intentos y recibe 429, onError=continueRegularOutput deja pasar el item con la
// propiedad .error en vez de cortar el flujo. Ese item NO es un post: se descarta aqui de
// forma explicita para que el clasificador nunca vea un objeto de error. El subreddit que
// fallo queda con 0 posts en la corrida, que es el estado honesto (ver
// V4/evidencias/CARACTERIZACION_RATE_LIMIT.md seccion 4). El loop continua con el resto.
const out = [];
for (const item of $input.all()) {
  const d = item.json || {};
  if (d.error) continue;              // item de error tras 429/403 agotado
  const link = String(d.link || '');
  const m = link.match(/\/r\/([a-z0-9_]+)\/comments\/([a-z0-9]+)\//i);
  if (!m) continue;
  const authorRaw = (typeof d.author === 'string' ? d.author : (d.author && d.author.name) || '')
    .replace(/^\/u\//, '')
    .trim();
  const text = String(d.contentSnippet || '')
    .replace(/\s*submitted by\s+\S+\s*/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  const iso = d.isoDate || d.pubDate || null;
  out.push({
    json: {
      id: m[2],
      subreddit_id: m[1],
      title: String(d.title || ''),
      selftext: text || null,
      url: link,
      author: authorRaw || '[deleted]',
      score: 0,
      num_comments: 0,
      created_utc: iso ? Math.floor(new Date(iso).getTime() / 1000) : 0
    }
  });
}
return out;"""

HMAC_CODE = r"""const crypto = require('crypto');
const key = $env.OSINT_HMAC_KEY;
if (!key) {
  throw new Error('Falta la variable de entorno OSINT_HMAC_KEY. Seteala antes de arrancar n8n (ver GUIA_EJECUCION.md).');
}
const out = [];
for (const item of $input.all()) {
  out.push({
    json: {
      ...item.json,
      author_hash: crypto.createHmac('sha256', key).update(String(item.json.author)).digest('hex'),
      created_utc_iso: new Date((item.json.created_utc || 0) * 1000).toISOString()
    }
  });
  delete out[out.length - 1].json.author;
}
return out;"""

CLASSIFY_CODE = r"""// Clasificador por diccionario bilingue (ES+EN), 9 categorias. Texto normalizado sin acentos.
// Match: terminos de UNA palabra por token EXACTO (words.has); de VARIAS por substring (text.includes).
// Restricciones que el diccionario respeta (si se rompen, el termino nunca encontraria el texto):
//   - sin tildes: la normalizacion NFD las saca del texto, no del termino ('bufer' nunca encontraria el texto);
//   - sin guiones: el tokenizado parte en /[^a-z0-9]+/, o sea 'zero-day' se parte en 'zero'+'day'
//     y la cadena con guion nunca aparece como token -> escribi 'zero day';
//   - con las formas conjugadas reales: 'filtraron' no matchea con 'filtrar'.
// Se sacaron los cuasisinonimos demasiado genericos (mp, cuenta, enlace, correo, bug, falla,
// transferencia, banco, filtrar, cangrejo, pescar, actualizacion) por falsos positivos.
// 2026-09-30: se SACO 'dni' de 'Filtración de Datos' por el mismo motivo. Matcheaba con un post
// sobre "dar de baja apoderado de jubilacion anses", que es tramite administrativo y no una
// filtracion. Con MIN_HITS=2 el falso positivo no se notaba porque el post tenia un solo hit; al
// bajar el umbral a 1 se hizo visible. Un termino que matchea con paperwork es demasiado generico.
// Fórmula de puntuación (4.4), AHORA SATURANTE: score = min(1, hits(c) / SATURATION), hits >= MIN_HITS.
// Por qué el cambio: antes era score = hits(c) / |keywords(c)|, y el denominador depende del tamaño
// del diccionario. Al ampliarlo de 5 a 9 categorías (y de ~10 a ~22 términos cada una), el MISMO
// post con los mismos 2 hits pasaba de 0.22 a 0.07: la escala se comprime y nlp_score deja de ser
// comparable entre corridas y entre categorías. SATURATION fija la escala (2 hits=0.5, 3=0.75,
// 4+=1.0), independiente del tamaño del diccionario, y sigue dentro de [0,1] (CHECK en la DB).
//
// MIN_HITS BAJADO DE 2 A 1 (2026-09-30, evaluacion de la muestra de control de 50 posts):
// con MIN_HITS=2 el clasificador descartaba amenazas obvias. "Fake Interpol Investigation Emails
// Are Dropping Ransomware on Small Businesses" tiene la palabra 'ransomware' en el TITULO, el
// termino existe en el diccionario y matchea perfecto, y aun asi el post se fue a 'No relevante'
// por no alcanzar el segundo hit. Medido sobre los 50 posts etiquetados a mano:
//   MIN_HITS=2 -> detecta 25/29 amenazas (86,2 %)
//   MIN_HITS=1 -> detecta 27/29 amenazas (93,1 %)
// Costo medido del cambio: los falsos positivos pasan de 1/21 a 3/21 en el grupo de control.
// Los 2 nuevos son terminos demasiado genericos del diccionario, no un efecto del umbral:
// 'dni' matcheaba con un post sobre dar de baja un apoderado de jubilacion y se saco en el
// mismo commit (ver 'Filtración de Datos'). MIN_HITS=1 tambien absorbe el ruido de fondo que
// antes salia: 'suplantacion de identidad' matchea con consultas legales laborales, que quedan
// fuera del ambito del proyecto (amenazas a infraestructura).
// Quedan 2 falsos negativos por vocabulario ausente ('edr evasion', 'red team'). NO se
// agregaron esos terminos: definirlos sin conocimiento tecnico de ciberseguridad meteria el
// mismo error conceptual adentro del diccionario. Documentado como limitacion abierta en
// V4/evidencias/evaluacion_muestra_control_2026-09-30.md.
const DICT = {
  'Phishing': ['phishing', 'phisher', 'smishing', 'vishing', 'spear phishing', 'correo fraudulento', 'correo suplantado', 'remitente falso', 'enlace fraudulento', 'enlace sospechoso', 'pagina falsa', 'sitio falso', 'portal falso', 'ingreso falso', 'verificar identidad', 'verificacion de identidad', 'captura de datos', 'suplantacion de correo', 'business email compromise', 'fake login', 'credential harvest', 'harvesting'],
  'Robo de Credenciales': ['clonacion de tarjeta', 'tarjeta clonada', 'clonar', 'robo de contrasena', 'robaron mi contrasena', 'cambio de contrasena', 'cambiar mi contrasena', 'acceso no autorizado', 'acceso remoto', 'tomaron control de la cuenta', 'tomo control de mi cuenta', 'sesion robada', 'robo de token', 'segundo factor', 'factor de autenticacion', 'credential stuffing', 'account takeover', 'session hijacking', 'session hijack', 'token theft', 'password theft', 'password dumping', '2fa bypass', 'mfa fatigue', 'sim swap', 'sim swapping', 'otp bypass', 'push bombing', 'adversary in the middle'],
  'Malware': ['malware', 'virus troyano', 'troyano', 'gusano', 'keylogger', 'rootkit', 'infostealer', 'stealer', 'dropper', 'loader', 'criptominer', 'miner', 'carga util', 'ejecucion remota', 'command and control', 'c2 server', 'rat', 'packed', 'obfuscated', 'ofuscado', 'payload', 'reverse shell', 'bind shell', 'webshell'],
  'Ransomware': ['ransomware', 'nota de rescate', 'pedir rescate', 'piden rescate', 'bloquearon mis archivos', 'mis archivos estan cifrados', 'sequestro de datos', 'extorsion', 'wannacry', 'lockbit', 'revil', 'blackcat', 'locker', 'decryptor', 'desencriptador'],
  'Vulnerabilidades': ['cve', 'exploit', 'exploits', 'parche', 'parchear', 'patch tuesday', 'actualizacion de seguridad', 'backdoor', 'puerta trasera', 'zero day', 'prueba de concepto', 'proof of concept', 'inyeccion sql', 'sql injection', 'xss', 'rce', 'ejecucion remota de codigo', 'escalamiento de privilegios', 'buffer overflow', 'desbordamiento de buffer', 'bypass de autenticacion', 'authentication bypass', 'kerberoasting', 'movimiento lateral', 'lateral movement', 'privilege escalation', 'nvd', 'cisa', 'zero day vulnerability', 'poc'],
  'Filtración de Datos': ['filtracion', 'filtraron', 'filtrado', 'filtran', 'fuga de datos', 'fuga de informacion', 'base filtrada', 'base de datos expuesta', 'bases expuestas', 'base expuesta', 'datos personales', 'venta de datos', 'venden datos', 'vazamiento', 'exfiltracion', 'exfiltrated', 'leak', 'leaked', 'leaks', 'breach', 'breached', 'exposed database', 'exposed credentials', 'credentials dump', 'combo list', 'dark web', 'pastebin', 'data dump', 'breach notification'],
  'Infraestructura y Ataques': ['botnet', 'ddos', 'denegacion de servicio', 'denial of service', 'caida de servicio', 'sitio caido', 'tiraron el sitio', 'tiraron abajo el sitio', 'ataque de red', 'amplificacion', 'reflection attack', 'volumetric', 'ip flood', 'takedown', 'caeron los servidores', 'caida de servidores'],
  'Hacktivismo': ['hacktivismo', 'hacktivista', 'hackeo', 'hackearon', 'hackear', 'deface', 'defacement', 'defaced', 'dox', 'doxeado', 'doxing', 'anonymous', 'filtracion publicada', 'publicacion de datos filtrados', 'protesta hacker', 'hactivist'],
  'Ingenieria Social': ['ingenieria social', 'social engineering', 'mecanismo de engano', 'se hacen pasar', 'suplantar identidad', 'suplantacion de identidad', 'baiting', 'confianza ganada', 'falsa llamada', 'llamada del banco', 'falso empleado', 'falsa policia', 'falso soporte', 'pretexting', 'impersonation', 'pretexto', 'scam call', 'fake support', 'vishing script', 'ayuda de escritorio falsa']
};
const MIN_HITS = 1;
const SATURATION = 4; // hits a partir de los cuales el score vale 1.0 (escala fija, ver cabecera)
const norm = (s) => String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
const out = [];
for (const item of $input.all()) {
  const text = norm(item.json.title + ' ' + (item.json.selftext || ''));
  const words = new Set(text.split(/[^a-z0-9]+/));
  let best = null;
  let bestHits = 0;
  for (const cat of Object.keys(DICT)) {
    let hits = 0;
    for (const kw of DICT[cat]) {
      const k = kw.includes(' ') ? (text.includes(kw) ? 1 : 0) : (words.has(kw) ? 1 : 0);
      hits += k;
    }
    if (hits > bestHits) {
      bestHits = hits;
      best = cat;
    }
  }
  if (best && bestHits >= MIN_HITS) {
    item.json.nlp_category = best;
    item.json.nlp_score = Math.min(1, Math.round((bestHits / SATURATION) * 10000) / 10000); // normalizado [0,1]
  } else {
    item.json.nlp_category = 'No relevante';
    item.json.nlp_score = 0;
  }
  out.push({ json: item.json });
}
return out;"""

EXTRACT_ENTITIES = r"""// Extracción de entidades (OE4, [N-06]): CVE, emails, IPs, dominios y productos.
const PRODUCTS = ['whatsapp', 'telegram', 'mercado pago', 'windows', 'linux', 'android', 'ios', 'chrome', 'firefox', 'bitcoin', 'usdt', 'afi p', 'banco nacion', 'galicia', 'santander', 'uala', 'cvu', 'mercado libre'];
const norm = (s) => String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
const uniq = (a) => Array.from(new Set(a));
const out = [];
for (const item of $input.all()) {
  const raw = item.json.title + ' ' + (item.json.selftext || '');
  const low = norm(raw);
  const entities = {
    cves: uniq((low.match(/\bcve-\d{4}-\d{4,7}\b/g) || []).map((x) => x.toUpperCase())).slice(0, 20),
    emails: uniq((raw.match(/\b[\w.+-]+@[\w-]+\.[\w.]+\b/g) || [])).slice(0, 20),
    ips: uniq((low.match(/\b(?:\d{1,3}\.){3}\d{1,3}\b/g) || [])).slice(0, 20),
    domains: uniq((low.match(/\b(?:[a-z0-9-]+\.)+(?:com|ar|org|net|io|gov|edu)\b/g) || []).filter((d) => !d.startsWith('reddit.com'))).slice(0, 20),
    products: uniq(PRODUCTS.filter((p) => low.includes(p))).slice(0, 20)
  };
  item.json.entities = entities;
  item.json.entities_json = JSON.stringify(entities);
  out.push({ json: item.json });
}
return out;"""

ANOMALY_ENGINE = r"""// Motor de anomalías (4.5): ventana diaria, base = media diaria de los 10 días previos,
// umbral = max(cuantil 95 de Poisson + 1, mínimo absoluto 3). Disparo si n_observado >= umbral.
function poissonCdf(k, l) {
  let s = 0;
  for (let i = 0; i <= k; i++) {
    let logP = -l;
    for (let j = 2; j <= i; j++) {
      logP += Math.log(l / j);
    }
    s += Math.exp(logP);
  }
  return Math.min(1, s);
}
const MIN_ABS = 3;
const out = [];
for (const item of $input.all()) {
  const lambda = Math.max(0, Number(item.json.base_media) || 0);
  const n = Math.max(0, Math.round(Number(item.json.n_observado) || 0));
  let t = 0;
  if (lambda > 0) {
    while (t < 500 && (1 - poissonCdf(t, lambda)) > 0.05) {
      t += 1;
    }
  }
  const umbralPoisson = lambda > 0 ? t + 1 : 1;
  const umbral = Math.max(umbralPoisson, MIN_ABS);
  out.push({
    json: {
      ventana_inicio: item.json.ventana_inicio,
      ventana_fin: item.json.ventana_fin,
      categoria: item.json.categoria,
      n_observado: n,
      base_media: Math.round(lambda * 1000) / 1000,
      umbral: umbral,
      disparo: n >= umbral
    }
  });
}
return out;"""

# ----------------------------------------------------------------------
# SQL de los nodos Postgres (executeQuery + options.queryReplacement, nodo v2.6)
# ----------------------------------------------------------------------
# Nota: subscribers se deja en 0/NULL — el RSS no trae about.json y el endpoint publico esta bloqueado.
# Si en el futuro se vuelve a OAuth, este upsert puede volver a actualizar subscribers con about.json.
UPSERT_SUBREDDITS_SQL = (
    "INSERT INTO subreddits (id, display_name, active_monitoring)\n"
    "VALUES ($1, $2, TRUE)\n"
    "ON CONFLICT (id) DO UPDATE SET display_name = EXCLUDED.display_name"
)

UPSERT_POSTS_SQL = (
    "INSERT INTO posts (id, subreddit_id, title, selftext, url, author_hash, score, num_comments, created_utc, nlp_category, nlp_score, entities, nlp_processed)\n"
    "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9::timestamptz, $10, $11, $12::jsonb, TRUE)\n"
    "ON CONFLICT (id) DO UPDATE SET\n"
    "  title = EXCLUDED.title,\n"
    "  selftext = EXCLUDED.selftext,\n"
    "  url = EXCLUDED.url,\n"
    "  score = EXCLUDED.score,\n"
    "  num_comments = EXCLUDED.num_comments,\n"
    "  nlp_category = EXCLUDED.nlp_category,\n"
    "  nlp_score = EXCLUDED.nlp_score,\n"
    "  entities = EXCLUDED.entities,\n"
    "  nlp_processed = TRUE"
)

QUERY_COUNTS_SQL = (
    "-- Ventana: ayer [00:00, 00:00) hora de Buenos Aires. Base: media diaria de los 10 días previos.\n"
    "SELECT\n"
    "  p.nlp_category AS categoria,\n"
    "  COUNT(*) FILTER (WHERE p.ingested_at >= date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '1 day'\n"
    "                   AND p.ingested_at <  date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires')) AS n_observado,\n"
    "  COUNT(*) FILTER (WHERE p.ingested_at >= date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '11 day'\n"
    "                   AND p.ingested_at <  date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '1 day') / 10.0 AS base_media,\n"
    "  (date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '1 day') AT TIME ZONE 'America/Argentina/Buenos_Aires' AS ventana_inicio,\n"
    "  date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') AT TIME ZONE 'America/Argentina/Buenos_Aires' AS ventana_fin\n"
    "FROM posts p\n"
    "WHERE p.nlp_category IS NOT NULL\n"
    "  AND p.nlp_category <> 'No relevante'\n"
    "  AND p.ingested_at >= date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '11 day'\n"
    "GROUP BY p.nlp_category\n"
    "ORDER BY p.nlp_category"
)

RECORD_ANOMALIAS_SQL = (
    "-- Inserta TODA la evaluación en anomalias; genera alerta solo si hubo disparo.\n"
    "-- OJO 1: la función que acepta jsonb se llama jsonb_to_recordset. json_to_recordset\n"
    "-- solo tiene la firma (json); invocarla con un jsonb da\n"
    "-- 'no existe la función json_to_recordset(jsonb)' y la evaluación no se registra.\n"
    "-- OJO 2: *to_recordset exige un ARRAY json en el nivel superior. El nodo manda\n"
    "-- JSON.stringify($json), que es un objeto suelto, y eso da\n"
    "-- 'no se puede invocar jsonb_to_recordset en un no-array'. Por eso el\n"
    "-- jsonb_build_array: envuelve el objeto en un array de un elemento.\n"
    "-- El nodo corre la query una vez por item de entrada, asi que aqui llega\n"
    "-- una sola categoria por vez y se inserta una fila por evaluacion.\n"
    "-- OJO 3: la insercion es IDEMPOTENTE sobre (ventana_inicio, ventana_fin,\n"
    "-- categoria). Sin este WHERE NOT EXISTS, ejecutar el workflow dos veces el\n"
    "-- mismo dia inserta la misma evaluacion dos veces y el conteo de\n"
    "-- suficiencia (que cuenta filas por dia) queda inflado. Con el guardia,\n"
    "-- relanzar el nodo a mano para recuperar un dia perdido no duplica nada,\n"
    "-- y tampoco se generan alertas repetidas porque el INSERT de alertas sale\n"
    "-- de 'ins', que queda vacio si la evaluacion ya existia.\n"
    "WITH reg AS (\n"
    "  SELECT * FROM jsonb_to_recordset(jsonb_build_array($1::jsonb))\n"
    "    AS x(ventana_inicio timestamptz, ventana_fin timestamptz, categoria varchar, n_observado int, base_media real, umbral real, disparo boolean)\n"
    "),\n"
    "ins AS (\n"
    "  INSERT INTO anomalias (ventana_inicio, ventana_fin, categoria, n_observado, base_media, umbral, disparo)\n"
    "  SELECT * FROM reg\n"
    "  WHERE NOT EXISTS (\n"
    "    SELECT 1 FROM anomalias a\n"
    "    WHERE a.ventana_inicio = reg.ventana_inicio\n"
    "      AND a.ventana_fin    = reg.ventana_fin\n"
    "      AND a.categoria      = reg.categoria\n"
    "  )\n"
    "  RETURNING id, categoria, n_observado, base_media, umbral, disparo, ventana_inicio\n"
    ")\n"
    "INSERT INTO alertas (anomalia_id, canal, destinatario, payload, estado)\n"
    "SELECT id, 'telegram', 'canal_tfi',\n"
    "       jsonb_build_object('categoria', categoria, 'n_observado', n_observado, 'base_media', base_media, 'umbral', umbral, 'ventana_inicio', ventana_inicio),\n"
    "       'PENDIENTE'\n"
    "FROM ins\n"
    "WHERE disparo\n"
    "RETURNING id, anomalia_id, canal, payload, estado"
)

# ----------------------------------------------------------------------
# Nodos
# ----------------------------------------------------------------------
# IDs de nodo ESTABLES (2026-09-30): antes se generaba un uuid4() nuevo en cada
# ejecucion, asi que regenerar el artefacto cambiaba los ids de los 16 nodos y el
# diff quedaba tapado por 16 lineas de GUID, escondiendo el cambio real. Ahora el
# id se deriva del nombre del nodo, de modo que el mismo nodo conserva su id entre
# ejecuciones y el diff muestra solo lo que cambio de verdad.
def nid(nombre):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "tfi-osint-n8n/nodo/" + nombre))

nodes = [
    # --- INGESTA ---
    {
        "parameters": {"rule": {"interval": [{"field": "minutes", "minutesInterval": 15}]}},
        "id": nid("Schedule Ingesta"), "name": "Schedule Ingesta",
        "type": "n8n-nodes-base.scheduleTrigger", "typeVersion": 1.2,
        "position": [-1900, -240],
    },
    {
        "parameters": {"jsCode": PREPARE_SUBS},
        "id": nid("Prepare Subreddits"), "name": "Prepare Subreddits",
        "type": "n8n-nodes-base.code", "typeVersion": 2,
        "position": [-1580, -240],
    },
    # Rama A: registro de subreddits monitoreados (suscriptores no disponibles via RSS)
    {
        "parameters": {
            "operation": "executeQuery",
            "query": UPSERT_SUBREDDITS_SQL,
            "options": {
                "queryReplacement": "={{ [ $json.subreddit_id, $json.display_name ] }}"
            },
        },
        "id": nid("Upsert Subreddits"), "name": "Upsert Subreddits",
        "type": "n8n-nodes-base.postgres", "typeVersion": 2.6,
        "position": [-620, -560],
    },
    # Rama B: throttling. splitInBatches (batchSize 1) + Wait 30s entre requests:
    # el rate limit publico de Reddit es ~1 req/min por IP. Sin esto el ciclo de 15 min dispara
    # los 3 requests seguidos y el subreddit responde 429 (que continueOnFail deja pasar).
    # El ciclo lo cierra "Upsert Posts" -> "Loop Over Items" (main[0] = salida "loop").
    # OJO: el ciclo exige executionOrder v1 en los settings del workflow (ya esta).
    {
        "parameters": {"batchSize": 1, "options": {}},
        "id": nid("Loop Over Items"), "name": "Loop Over Items",
        "type": "n8n-nodes-base.splitInBatches", "typeVersion": 3,
        "position": [-1420, 80],
    },
    {
        "parameters": {"amount": 30, "unit": "seconds"},
        "id": nid("Espera Rate Limit"), "name": "Espera Rate Limit",
        "type": "n8n-nodes-base.wait", "typeVersion": 1.1,
        "position": [-1180, 80],
    },
    # Rama B: posts (feed Atom RSS publico)
    {
        "parameters": {
            "url": "={{ $json.rss_url }}",
            "options": {
                "customFields": "author, contentSnippet, guid"
            },
        },
        "id": nid("Fetch Posts RSS"), "name": "Fetch Posts RSS",
        "type": "n8n-nodes-base.rssFeedRead", "typeVersion": 1.2,
        "position": [-940, 80],
        # Mitigacion RN-FU-03 ante 429/403 de Reddit. Decision D-10 (2026-09-30).
        #
        # Los settings van en la RAIZ del nodo, no bajo una clave "settings". En n8n 2.40.6
        # el motor los lee desde node.<campo>:
        #   workflow-execute.js:933  -> node.retryOnFail
        #   workflow-execute.js:937  -> node.maxTries
        #   workflow-execute.js:938  -> node.waitBetweenTries
        #   workflow-execute.js:563  -> node.continueOnFail
        #   workflow-execute.js:564  -> node.onError
        # Bajo "settings" el motor los ignora por completo: no reintenta y no continua.
        # Ese fue el motivo real del HTTP 429 que aborto la corrida del 2026-09-30.
        #
        # waitBetweenTries = 5000 es el MAXIMO que admite el motor:
        #   Math.min(5000, Math.max(0, node.waitBetweenTries || 1000))   (:938)
        # RN-FU-03 pedia 30 s, cifra imposible por configuracion. Decision D-10 (aprobada
        # 2026-09-30): la regla se relaja a "3 intentos con hasta 5 s" y el tope se declara
        # como-imposed por el motor, no como una eleccion del proyecto. El espaciado de 30 s
        # ENTRE subreddits lo aporta el nodo "Espera Rate Limit", que si es ours.
        #
        # onError=continueRegularOutput: si un subreddit da 429 tras los 3 intentos, el item
        # llega con .error y "Parse Reddit Posts" lo descarta; el loop sigue con el resto.
        # continueOnFail se conserva porque el motor lo acepta como equivalente (:563).
        "retryOnFail": True,
        "maxTries": 3,
        "waitBetweenTries": 5000,
        "continueOnFail": True,
        "onError": "continueRegularOutput",
    },
    {
        "parameters": {"jsCode": PARSE_POSTS},
        "id": nid("Parse Reddit Posts"), "name": "Parse Reddit Posts",
        "type": "n8n-nodes-base.code", "typeVersion": 2,
        "position": [-620, 80],
    },
    {
        "parameters": {"jsCode": HMAC_CODE},
        "id": nid("HMAC Anonymize"), "name": "HMAC Anonymize",
        "type": "n8n-nodes-base.code", "typeVersion": 2,
        "position": [-300, 80],
    },
    {
        "parameters": {"jsCode": CLASSIFY_CODE},
        "id": nid("Classify Dictionary"), "name": "Classify Dictionary",
        "type": "n8n-nodes-base.code", "typeVersion": 2,
        "position": [20, 80],
    },
    {
        "parameters": {"jsCode": EXTRACT_ENTITIES},
        "id": nid("Extract Entities"), "name": "Extract Entities",
        "type": "n8n-nodes-base.code", "typeVersion": 2,
        "position": [340, 80],
    },
    {
        "parameters": {
            "operation": "executeQuery",
            "query": UPSERT_POSTS_SQL,
            "options": {
                "queryReplacement": "={{ [ $json.id, $json.subreddit_id, $json.title, $json.selftext, $json.url, $json.author_hash, $json.score, $json.num_comments, $json.created_utc_iso, $json.nlp_category, $json.nlp_score, $json.entities_json ] }}"
            },
        },
        "id": nid("Upsert Posts"), "name": "Upsert Posts",
        "type": "n8n-nodes-base.postgres", "typeVersion": 2.6,
        "position": [660, 80],
    },
    # --- ANOMALÍAS ---
    {
        # 2026-10-01: la hora paso de 00:05 a 12:05. La ventana que evalua este
        # trigger NO depende de la hora de ejecucion: QUERY_COUNTS_SQL calcula
        # 'ayer' con date_trunc('day', now()...), o sea el dia calendario
        # [00:00, 00:00) de Buenos Aires. A las 12:05 ese dia ya esta cerrado y
        # el resultado es identico al que daria a las 00:05.
        # El motivo del cambio es operativo: la maquina que corre la instancia no
        # esta encendida de noche, asi que un trigger a las 00:05 se perdia todos
        # los dias y la tabla anomalias nunca llenaba. Corriendolo al mediodia se
        # evalua dentro de la franja en que la maquina si esta prendida.
        # El cambio NO toca la rama de ingesta, que sigue cada 15 minutos.
        "parameters": {"rule": {"interval": [{"field": "days", "triggerAtHour": 12, "triggerAtMinute": 5}]}},
        "id": nid("Schedule Anomalias"), "name": "Schedule Anomalias",
        "type": "n8n-nodes-base.scheduleTrigger", "typeVersion": 1.2,
        "position": [-1900, 560],
    },
    {
        "parameters": {"operation": "executeQuery", "query": QUERY_COUNTS_SQL, "options": {}},
        "id": nid("Query Daily Counts"), "name": "Query Daily Counts",
        "type": "n8n-nodes-base.postgres", "typeVersion": 2.6,
        "position": [-1580, 560],
    },
    {
        "parameters": {"jsCode": ANOMALY_ENGINE},
        "id": nid("Anomaly Engine"), "name": "Anomaly Engine",
        "type": "n8n-nodes-base.code", "typeVersion": 2,
        "position": [-1260, 560],
    },
    {
        "parameters": {
            "operation": "executeQuery",
            "query": RECORD_ANOMALIAS_SQL,
            "options": {"queryReplacement": "={{ [ JSON.stringify($json) ] }}"},
        },
        "id": nid("Registrar Anomalias y Alertas"), "name": "Registrar Anomalias y Alertas",
        "type": "n8n-nodes-base.postgres", "typeVersion": 2.6,
        "position": [-940, 560],
    },
    {
        "parameters": {
            "url": "={{ 'https://api.telegram.org/bot' + $env.TELEGRAM_BOT_TOKEN + '/sendMessage' }}",
            "authentication": "none",
            "method": "POST",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ JSON.stringify({ chat_id: $env.TELEGRAM_CHAT_ID, text: 'ALERTA TFI OSINT: ' + $json.payload.categoria + ' — posts: ' + $json.payload.n_observado + ' (umbral ' + $json.payload.umbral + '), ventana ' + $json.payload.ventana_inicio }) }}",
            "options": {},
        },
        "disabled": True,  # habilitar solo cuando exista el bot de Telegram (ver guía)
        "id": nid("Send Telegram Alert"), "name": "Send Telegram Alert",
        "type": "n8n-nodes-base.httpRequest", "typeVersion": 4.2,
        "position": [-620, 560],
    },
]

# ----------------------------------------------------------------------
# Conexiones
# ----------------------------------------------------------------------
connections = {
    "Schedule Ingesta": {"main": [[{"node": "Prepare Subreddits", "type": "main", "index": 0}]]},
    "Prepare Subreddits": {"main": [[
        {"node": "Upsert Subreddits", "type": "main", "index": 0},
        {"node": "Loop Over Items", "type": "main", "index": 0},
    ]]},
    # splitInBatches: main[0] = "loop" (un item por iteracion), main[1] = "done" (sin conectar).
    "Loop Over Items": {"main": [
        [{"node": "Espera Rate Limit", "type": "main", "index": 0}],
        [],
    ]},
    "Espera Rate Limit": {"main": [[{"node": "Fetch Posts RSS", "type": "main", "index": 0}]]},
    "Fetch Posts RSS": {"main": [[{"node": "Parse Reddit Posts", "type": "main", "index": 0}]]},
    "Parse Reddit Posts": {"main": [[{"node": "HMAC Anonymize", "type": "main", "index": 0}]]},
    "HMAC Anonymize": {"main": [[{"node": "Classify Dictionary", "type": "main", "index": 0}]]},
    "Classify Dictionary": {"main": [[{"node": "Extract Entities", "type": "main", "index": 0}]]},
    "Extract Entities": {"main": [[{"node": "Upsert Posts", "type": "main", "index": 0}]]},
    # Cierra el ciclo: cada item procesado vuelve al loop para el rate limit del siguiente subreddit.
    "Upsert Posts": {"main": [[{"node": "Loop Over Items", "type": "main", "index": 0}]]},
    "Schedule Anomalias": {"main": [[{"node": "Query Daily Counts", "type": "main", "index": 0}]]},
    "Query Daily Counts": {"main": [[{"node": "Anomaly Engine", "type": "main", "index": 0}]]},
    "Anomaly Engine": {"main": [[{"node": "Registrar Anomalias y Alertas", "type": "main", "index": 0}]]},
    "Registrar Anomalias y Alertas": {"main": [[{"node": "Send Telegram Alert", "type": "main", "index": 0}]]},
}

# ----------------------------------------------------------------------
# Validación estructural antes de escribir
# ----------------------------------------------------------------------
names = {n["name"] for n in nodes}
errors = []
for src, conns in connections.items():
    if src not in names:
        errors.append(f"Origen inexistente: {src}")
    for targets in conns["main"]:
        for t in targets:
            if t["node"] not in names:
                errors.append(f"Destino inexistente: {t['node']} (desde {src})")
if errors:
    raise SystemExit("Errores de validación:\n" + "\n".join(errors))

workflow = {
    "id": "TFIOsintV4Monitor01",
    "name": "TFI OSINT V4 - Monitor de Amenazas",
    "nodes": nodes,
    "pinData": {},
    "connections": connections,
    "active": False,
    "settings": {"executionOrder": "v1", "timezone": "America/Argentina/Buenos_Aires"},
    # versionId fijo (2026-09-30): era un uuid4() aleatorio, asi que regenerar el
    # artefacto cambiaba una linea mas del diff sin motivo. n8n lo reemplaza al
    # importar; mantenerlo estable hace que el artefacto sea reproducible byte a
    # byte entre ejecuciones y el diff muestre solo cambios reales.
    "versionId": str(uuid.uuid5(uuid.NAMESPACE_URL, "tfi-osint-n8n/workflow")),
    "meta": {"templateCredsSetupCompleted": False},
    "tags": [],
}

OUT.write_text(json.dumps(workflow, ensure_ascii=False, indent=2), encoding="utf-8")
# round-trip de validación
json.loads(OUT.read_text(encoding="utf-8"))
print(f"OK -> {OUT}  ({len(nodes)} nodos)")