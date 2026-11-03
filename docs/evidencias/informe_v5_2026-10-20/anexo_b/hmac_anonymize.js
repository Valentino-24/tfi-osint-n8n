const crypto = require('crypto');
const key = $env.OSINT_HMAC_KEY;
if (!key) {
  throw new Error('Falta la variable de entorno OSINT_HMAC_KEY. Seteala antes de arrancar n8n (ver GUIA_EJECUCION.md).');
}
const out = [];
for (const item of $input.all()) {
  if (item.json._skip) { out.push(item); continue; }   // centinela de 429: pasa intacto
  out.push({
    json: {
      ...item.json,
      author_hash: crypto.createHmac('sha256', key).update(String(item.json.author)).digest('hex'),
      created_utc_iso: new Date((item.json.created_utc || 0) * 1000).toISOString()
    }
  });
  delete out[out.length - 1].json.author;
}
return out;
