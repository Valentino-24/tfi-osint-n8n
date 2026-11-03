// Clasificador por diccionario bilingue (ES+EN), 9 categorias. Texto normalizado sin acentos.
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
  'Ransomware': ['ransomware', 'nota de rescate', 'pedir rescate', 'piden rescate', 'bloquearon mis archivos', 'mis archivos estan cifrados', 'secuestro de datos', 'extorsion', 'wannacry', 'lockbit', 'revil', 'blackcat', 'locker', 'decryptor', 'desencriptador'],
  'Vulnerabilidades': ['cve', 'exploit', 'exploits', 'parche', 'parchear', 'patch tuesday', 'actualizacion de seguridad', 'backdoor', 'puerta trasera', 'zero day', 'prueba de concepto', 'proof of concept', 'inyeccion sql', 'sql injection', 'xss', 'rce', 'ejecucion remota de codigo', 'escalamiento de privilegios', 'buffer overflow', 'desbordamiento de buffer', 'bypass de autenticacion', 'authentication bypass', 'kerberoasting', 'movimiento lateral', 'lateral movement', 'privilege escalation', 'nvd', 'cisa', 'zero day vulnerability', 'poc'],
  'Filtración de Datos': ['filtracion', 'filtraron', 'filtrado', 'filtran', 'fuga de datos', 'fuga de informacion', 'base filtrada', 'base de datos expuesta', 'bases expuestas', 'base expuesta', 'datos personales', 'venta de datos', 'venden datos', 'vazamiento', 'exfiltracion', 'exfiltrated', 'leak', 'leaked', 'leaks', 'breach', 'breached', 'exposed database', 'exposed credentials', 'credentials dump', 'combo list', 'dark web', 'pastebin', 'data dump', 'breach notification'],
  'Infraestructura y Ataques': ['botnet', 'ddos', 'denegacion de servicio', 'denial of service', 'caida de servicio', 'sitio caido', 'tiraron el sitio', 'tiraron abajo el sitio', 'ataque de red', 'amplificacion', 'reflection attack', 'volumetric', 'ip flood', 'takedown', 'cayeron los servidores', 'caida de servidores'],
  'Hacktivismo': ['hacktivismo', 'hacktivista', 'hackeo', 'hackearon', 'hackear', 'deface', 'defacement', 'defaced', 'dox', 'doxeado', 'doxing', 'anonymous', 'filtracion publicada', 'publicacion de datos filtrados', 'protesta hacker', 'hactivist'],
  'Ingenieria Social': ['ingenieria social', 'social engineering', 'mecanismo de engano', 'se hacen pasar', 'suplantar identidad', 'suplantacion de identidad', 'baiting', 'confianza ganada', 'falsa llamada', 'llamada del banco', 'falso empleado', 'falsa policia', 'falso soporte', 'pretexting', 'impersonation', 'pretexto', 'scam call', 'fake support', 'vishing script', 'ayuda de escritorio falsa']
};
const MIN_HITS = 1;
const SATURATION = 4; // hits a partir de los cuales el score vale 1.0 (escala fija, ver cabecera)
const norm = (s) => String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
const out = [];
for (const item of $input.all()) {
  if (item.json._skip) { out.push(item); continue; }   // centinela de 429: no se clasifica
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
return out;
