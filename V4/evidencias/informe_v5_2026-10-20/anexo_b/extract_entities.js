// Extracción de entidades (OE4, [N-06]): CVE, emails, IPs, dominios y productos.
const PRODUCTS = ['whatsapp', 'telegram', 'mercado pago', 'windows', 'linux', 'android', 'ios', 'chrome', 'firefox', 'bitcoin', 'usdt', 'afi p', 'banco nacion', 'galicia', 'santander', 'uala', 'cvu', 'mercado libre'];
const norm = (s) => String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
const uniq = (a) => Array.from(new Set(a));
const out = [];
for (const item of $input.all()) {
  if (item.json._skip) { out.push(item); continue; }   // centinela de 429: sin entidades
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
return out;
