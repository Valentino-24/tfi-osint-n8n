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
PREPARE_SUBS = r"""const subs = [
  { subreddit_id: 'argentina', display_name: 'r/argentina', rss_url: 'https://www.reddit.com/r/argentina/new/.rss?limit=100' },
  { subreddit_id: 'devsarg', display_name: 'r/devsarg', rss_url: 'https://www.reddit.com/r/devsarg/new/.rss?limit=100' },
  { subreddit_id: 'derechogenial', display_name: 'r/derechogenial', rss_url: 'https://www.reddit.com/r/derechogenial/new/.rss?limit=100' }
];
return subs;"""

PARSE_POSTS = r"""// Parser para feed Atom RSS de Reddit (nodo RSS Read, rss-parser).
// id y subreddit_id se derivan del link del post:
//   https://www.reddit.com/r/{sub}/comments/{id}/{slug}/
// limitaciones RSS: score y num_comments no vienen -> 0 (documentado).
const out = [];
for (const item of $input.all()) {
  const d = item.json || {};
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

CLASSIFY_CODE = r"""// Clasificador por diccionario (Anexo C base). Texto normalizado sin acentos.
// Fórmula de puntuación (4.4): score = hits(c) / |keywords(c)| con hits >= MIN_HITS.
const DICT = {
  'Estafas Virtuales': ['estafa', 'estafas', 'estafa virtual', 'transferencia', 'mercado pago', 'mp', 'clonacion', 'clonacion de tarjeta', 'clonar', 'banco', 'billetera', 'cangrejo', 'piramidal', 'defraudacion'],
  'Phishing': ['phishing', 'suplantacion', 'enlace', 'correo', 'whatsapp', 'cuenta', 'pescar', 'smishing', 'verificacion', 'ingreso falso'],
  'Filtración de Datos': ['filtracion', 'filtrar', 'leak', 'fuga', 'dni', 'base de datos', 'venta de datos', 'expuesta', 'datos personales', 'vazamiento'],
  'Vulnerabilidades': ['vulnerabilidad', 'vulnerabilidades', 'bug', 'cve', 'exploit', 'parche', 'actualizacion', 'falla', 'pwn'],
  'Ransomware': ['ransomware', 'secuestro de datos', 'secuestro', 'encriptado', 'cifrado', 'rescate', 'wannacry', 'criptoransomware']
};
const MIN_HITS = 2;
const norm = (s) => String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
const out = [];
for (const item of $input.all()) {
  const text = norm(item.json.title + ' ' + (item.json.selftext || ''));
  const words = new Set(text.split(/[^a-z0-9]+/));
  let best = null;
  let bestHits = 0;
  let bestK = 1;
  for (const cat of Object.keys(DICT)) {
    let hits = 0;
    for (const kw of DICT[cat]) {
      const k = kw.includes(' ') ? (text.includes(kw) ? 1 : 0) : (words.has(kw) ? 1 : 0);
      hits += k;
    }
    if (hits > bestHits) {
      bestHits = hits;
      best = cat;
      bestK = DICT[cat].length;
    }
  }
  if (best && bestHits >= MIN_HITS) {
    item.json.nlp_category = best;
    item.json.nlp_score = Math.round((bestHits / bestK) * 10000) / 10000; // normalizado [0,1]
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
    "WITH ins AS (\n"
    "  INSERT INTO anomalias (ventana_inicio, ventana_fin, categoria, n_observado, base_media, umbral, disparo)\n"
    "  SELECT * FROM jsonb_to_recordset(jsonb_build_array($1::jsonb))\n"
    "    AS x(ventana_inicio timestamptz, ventana_fin timestamptz, categoria varchar, n_observado int, base_media real, umbral real, disparo boolean)\n"
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
def nid():
    return str(uuid.uuid4())

nodes = [
    # --- INGESTA ---
    {
        "parameters": {"rule": {"interval": [{"field": "minutes", "minutesInterval": 15}]}},
        "id": nid(), "name": "Schedule Ingesta",
        "type": "n8n-nodes-base.scheduleTrigger", "typeVersion": 1.2,
        "position": [-1900, -240],
    },
    {
        "parameters": {"jsCode": PREPARE_SUBS},
        "id": nid(), "name": "Prepare Subreddits",
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
        "id": nid(), "name": "Upsert Subreddits",
        "type": "n8n-nodes-base.postgres", "typeVersion": 2.6,
        "position": [-620, -560],
    },
    # Rama B: posts (feed Atom RSS publico)
    {
        "parameters": {
            "url": "={{ $json.rss_url }}",
            "options": {
                "customFields": "author, contentSnippet, guid"
            },
        },
        "id": nid(), "name": "Fetch Posts RSS",
        "type": "n8n-nodes-base.rssFeedRead", "typeVersion": 1.2,
        "position": [-940, 80],
        "retryOnFail": True,
        "maxRetries": 3,
        "waitBetweenRetries": 30000,
        # continueOnFail: si un subreddit da 429 (rate limit publico ~1 req/min por IP),
        # el resto del ciclo sigue e ingresa igual; el item con error lo descarta el parser.
        "continueOnFail": True,
    },
    {
        "parameters": {"jsCode": PARSE_POSTS},
        "id": nid(), "name": "Parse Reddit Posts",
        "type": "n8n-nodes-base.code", "typeVersion": 2,
        "position": [-620, 80],
    },
    {
        "parameters": {"jsCode": HMAC_CODE},
        "id": nid(), "name": "HMAC Anonymize",
        "type": "n8n-nodes-base.code", "typeVersion": 2,
        "position": [-300, 80],
    },
    {
        "parameters": {"jsCode": CLASSIFY_CODE},
        "id": nid(), "name": "Classify Dictionary",
        "type": "n8n-nodes-base.code", "typeVersion": 2,
        "position": [20, 80],
    },
    {
        "parameters": {"jsCode": EXTRACT_ENTITIES},
        "id": nid(), "name": "Extract Entities",
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
        "id": nid(), "name": "Upsert Posts",
        "type": "n8n-nodes-base.postgres", "typeVersion": 2.6,
        "position": [660, 80],
    },
    # --- ANOMALÍAS ---
    {
        "parameters": {"rule": {"interval": [{"field": "days", "triggerAtHour": 0, "triggerAtMinute": 5}]}},
        "id": nid(), "name": "Schedule Anomalias",
        "type": "n8n-nodes-base.scheduleTrigger", "typeVersion": 1.2,
        "position": [-1900, 560],
    },
    {
        "parameters": {"operation": "executeQuery", "query": QUERY_COUNTS_SQL, "options": {}},
        "id": nid(), "name": "Query Daily Counts",
        "type": "n8n-nodes-base.postgres", "typeVersion": 2.6,
        "position": [-1580, 560],
    },
    {
        "parameters": {"jsCode": ANOMALY_ENGINE},
        "id": nid(), "name": "Anomaly Engine",
        "type": "n8n-nodes-base.code", "typeVersion": 2,
        "position": [-1260, 560],
    },
    {
        "parameters": {
            "operation": "executeQuery",
            "query": RECORD_ANOMALIAS_SQL,
            "options": {"queryReplacement": "={{ [ JSON.stringify($json) ] }}"},
        },
        "id": nid(), "name": "Registrar Anomalias y Alertas",
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
        "id": nid(), "name": "Send Telegram Alert",
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
        {"node": "Fetch Posts RSS", "type": "main", "index": 0},
    ]]},
    "Fetch Posts RSS": {"main": [[{"node": "Parse Reddit Posts", "type": "main", "index": 0}]]},
    "Parse Reddit Posts": {"main": [[{"node": "HMAC Anonymize", "type": "main", "index": 0}]]},
    "HMAC Anonymize": {"main": [[{"node": "Classify Dictionary", "type": "main", "index": 0}]]},
    "Classify Dictionary": {"main": [[{"node": "Extract Entities", "type": "main", "index": 0}]]},
    "Extract Entities": {"main": [[{"node": "Upsert Posts", "type": "main", "index": 0}]]},
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
    "versionId": str(uuid.uuid4()),
    "meta": {"templateCredsSetupCompleted": False},
    "tags": [],
}

OUT.write_text(json.dumps(workflow, ensure_ascii=False, indent=2), encoding="utf-8")
# round-trip de validación
json.loads(OUT.read_text(encoding="utf-8"))
print(f"OK -> {OUT}  ({len(nodes)} nodos)")