# Auditoría del diccionario del clasificador (N-12 / 6.3)

Generado: 2026-10-20. Base `tesi_osint`, contenedor `tfi-postgres`. Solo lectura.

## 1. Método

- Reimplementación en Python del nodo `Classify` a partir del código de `V4/scripts/generar_workflow.py`.
- Normalización: minúsculas + NFD sin diacríticos. Tokenización por `/[^a-z0-9]+/`.
- Coincidencia: término de una palabra contra el conjunto de tokens; término de varias por subcadena.
- Validación: reproduce **724 de 724** clasificaciones almacenadas (**0 discrepancias**).
- Corpus analizado: 724 publicaciones (170 clasificadas, 554 «No relevante»).

## 2. Inventario

- Términos: **201** en 9 categorías.
- Términos con caracteres no ASCII: **0**. Con guion: **0**. Con espacios anómalos: **0**.

## 3. (a) Erratas

| Término | Coincidencias (forma errónea) | Coincidencias (forma correcta) |
|---|---:|---:|
| `caeron los servidores` → `cayeron los servidores` | 0 | 0 |
| Término | Coincidencias (forma errónea) | Coincidencias (forma correcta) |
| `sequestro de datos` → `secuestro de datos` | 0 | 0 |

**Efecto de la corrección: nulo.** Ambas formas coinciden con 0 publicaciones; el corpus se reclasifica idéntico.
Corregidas en `V4/scripts/generar_workflow.py` y regenerado `V4/anexos/B_workflow.json` (diff: una sola línea, los dos términos).

## 4. (b) Términos genéricos — contrafactual

Términos retirados en el contrafactual: `acceso remoto`, `cambio de contrasena`, `clonar`, `datos personales`, `filtrado`, `leak`, `leaked`, `leaks`, `loader`, `miner`, `packed`, `payload`, `segundo factor`

- Clasificadas: **170 → 159** (−11, 6.5 %).
- Por comunidad: {'r/netsec': 66, 'r/Malware': 97, 'r/devsarg': 7} → {'r/netsec': 64, 'r/Malware': 91, 'r/devsarg': 4}.

Publicaciones que caerían:

| id | categoría actual | términos que la sostenían | comunidad | título |
|---|---|---|---|---|
| `1wnwy4b` | Filtración de Datos | `leaked` | r/netsec | Leaked GitHub App private keys let researchers impersonate 4 |
| `1wi4zky` | Malware | `payload` | r/Malware | [iOS] Analyzing anomalous cpu_resource / diskwrites_resource |
| `1x2vur9` | Filtración de Datos | `datos personales` | r/devsarg | Guardar datos personales |
| `1w6ynzn` | Malware | `payload` | r/netsec | From fake interview to signed ClickOnce: inside a three-payl |
| `1u0f2ft` | Malware | `payload` | r/Malware | Fake Interview deploys stealthy cross platform (macOS/Window |
| `1vvapze` | Malware | `payload` | r/Malware | I've been telling people to check the wrong thing first, and |
| `1uiw6ut` | Malware | `payload` | r/Malware | First time seeing this for MacOS |
| `1wwn0fa` | Malware | `loader` | r/Malware | Pre-installed C2 loader on cheap Android projectors - deploy |
| `1x6o056` | Robo de Credenciales | `clonar` | r/devsarg | Usar ingeniera inversa para portear juegos de pc a Android e |
| `1vj4co9` | Malware | `loader` | r/Malware | Fake Cloudflare verification on deceased influencer’s site d |
| `1x2kl6z` | Filtración de Datos | `datos personales` | r/devsarg | Consulta sobre monetizar APP Android y datos personales (Arg |

Casos de la Tabla 5.11 afectados: **C-09, C-08**.

## 5. (c) Solapamientos

| Par | Publicaciones con ambos | Publicaciones con solo el término corto |
|---|---:|---:|
| `zero day` / `zero day vulnerability` | 0 | 0 |
| `ejecucion remota` / `ejecucion remota de codigo` | 0 | 0 |
| `filtracion` / `filtracion publicada` | 0 | 0 |
| `vishing` / `vishing script` | 0 | 0 |

**Efecto medido en este corpus: nulo.** Ninguna publicación contiene ambos miembros de un par, de modo que la doble cuenta no llegó a producirse.

## 6. (d) Guiones

`norm()` no reemplaza guiones: el texto normalizado conserva `zero-day`, y el término de dos palabras `zero day` no es subcadena de `zero-day`.

Publicaciones afectadas: **5 de 724**. Conjunto clasificado: **170 → 170**.

| id | antes | después | términos nuevos | título |
|---|---|---|---|---|
| `1umy56h` | Malware / 0.25 | Malware / 0.50 | `command and control` | Silent Swap: A Crypto Clipper Extension Campaign |
| `1x4xuvc` | Vulnerabilidades / 0.25 | Vulnerabilidades / 0.50 | `zero day` | We Let AI Fuzz Adobe Reader for a Week. It Found a Crit |
| `1wzchsp` | Robo de Credenciales / 0.25 | Vulnerabilidades / 0.50 | `zero day`, `rce` | Rockstar Games has now been compromised several differe |
| `1vf3niv` | Malware / 1.00 | Malware / 1.00 | `command and control` | Technical analysis of Parivahan App ( shared on ScamInd |
| `1ui3ou8` | Malware / 0.25 | Filtración de Datos / 0.50 | `breach`, `breach notification` | Police take down SocGholish, maker of major pop-up scam |

## 7. Traza de coincidencias: 13 casos de la Tabla 5.11

| Código | id | categoría | términos |
|---|---|---|---|
| C-01 | `1x5iauj` | Malware | `malware`, `infostealer`, `loader`, `payload` |
| C-02 | `1wwmtnr` | Malware | `malware`, `dropper`, `loader`, `c2 server`, `obfuscated`, `payload` |
| C-03 | `1u257x9` | Malware | `malware`, `infostealer`, `dropper`, `rat`, `obfuscated`, `payload` |
| C-04 | `1x1squu` | Vulnerabilidades | `cve`, `rce` |
| C-05 | `1x3wv86` | Vulnerabilidades | `exploit`, `rce` |
| C-06 | `1x42omu` | Hacktivismo | `hackearon` |
| C-07 | `1x5acdz` | Phishing | `phishing` |
| C-08 | `1x6o056` | Robo de Credenciales | `clonar` |
| C-09 | `1x2vur9` | Filtración de Datos | `datos personales` |
| C-10 | `1wr7qwo` | Infraestructura y Ataques | `botnet` |
| C-11 | `1x3v6od` | Vulnerabilidades | `rce` |
| C-12 | `1x3xa8g` | Vulnerabilidades | `cve` |
| C-13 | `1x2i19l` | Vulnerabilidades | `rce` |

## 8. Decisión

Se congelan (c), (d) y (b): corregir (c) no tiene efecto, y corregir (b) o (d) desplaza el marco muestral de la validación (554 no clasificadas / censo de 170 clasificadas). Se corrigen solo las erratas, de efecto nulo. El efecto de las restantes se informa cuantificado y se traslada a 6.3 y a las recomendaciones.
