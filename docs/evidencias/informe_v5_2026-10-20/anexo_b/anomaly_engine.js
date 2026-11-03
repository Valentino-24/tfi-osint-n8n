// Motor de anomalías (4.5): ventana diaria, base = media diaria de los 10 días previos,
// umbral = max(cuantil 95 de Poisson + 1, mínimo absoluto 3). Disparo si n_observado >= umbral.
// Poisson real por recurrencia: P(i) = P(i-1) * l / i, arrancando en P(0) = e^-l.
//
// 2026-10-05: la version anterior aritmetizaba las masas con
//   for (let j = 2; j <= i; j++) logP += Math.log(l / j)
// lo que produce l^(i-1)/i! * e^-l en vez de l^i/i! * e^-l: le falta un factor l
// a TODAS las masas menos la de i = 0. Comprobado con l = 5,5:
//   P(1) exacta 0,022477 | la que computaba el nodo 0,004087  (factor 0,18)
// La CDF rota satura en 1/l, asi que para l > 1,05 nunca alcanza 0,95, el while
// de busqueda del umbral corre hasta el tope de 500 y devuelve umbral = 501.
// Con umbral 501 ninguna categoria con base > 1,05 puede disparar nunca: se
// comprobo en produccion con Malware (base 5,5) y Vulnerabilidades (base 4,3),
// ambos con umbral 501. La unica categoria que sobrevivia era Phishing
// (base 0,7), por accidente, no por diseno.
function poissonCdf(k, l) {
  if (!(l > 0)) return 1;
  let term = Math.exp(-l);
  let s = term;
  for (let i = 1; i <= k; i++) {
    term = term * l / i;
    s += term;
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
return out;
