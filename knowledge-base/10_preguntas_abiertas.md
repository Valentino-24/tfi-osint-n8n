# Preguntas Abiertas

## Inconsistencias detectadas

### ~~IN-01 — La guía declara 15 nodos y la verificación final 14~~ — RESUELTA 2026-09-30

**Estado**: resuelta. El workflow tiene **16 nodos** (`B_workflow.json`, 16 nodos;
`generar_workflow.py` declara 16). Las dos ramas, ingesta y anomalías, fueron
ejecutadas en runtime y verificadas. La guía decía 15 y la verificación previa 14;
ambas cifras quedaron desactualizadas al crecer el workflow. La guía ya dice 16.
**Documento A dice**: `GUIA_EJECUCION.md` describe el workflow como 15 nodos.
**Documento B dice**: la sesión de verificación reportó 14 nodos.
**Impacto**: afecta la Figura 3, el Anexo B y la trazabilidad del artefacto.
**Resolución propuesta**: regenerar el export desde `generar_workflow.py`, contar los nodos en la versión final y actualizar la guía y la figura con ese número.

### IN-02 — El estado de B4 en la guía quedó desactualizado
**Documento A dice**: la tabla de estado inicial muestra B4 como pendiente.
**Documento B dice**: la corrida real verificó 201 posts y un post de phishing.
**Impacto**: un lector puede pensar que la ingesta nunca fue ejecutada.
**Resolución propuesta**: actualizar la tabla de estado con la fecha, la corrida y la limitación de `r/derechogenial`.

### IN-03 — Semántica de `ingested_at` en el upsert
**Documento A dice**: `ingested_at` no debe tocarse para preservar la latencia.
**Documento B dice**: el DDL solo define el default y no expresa la regla del `ON CONFLICT`.
**Impacto**: puede cambiar la latencia calculada si un post se reprocesa.
**Resolución propuesta**: fijar la sentencia final de upsert y verificarla con una segunda corrida controlada.

### IN-04 — Paleta de evidencia de la alerta externa
**Documento A dice**: el sistema tiene nodo Telegram.
**Documento B dice**: Telegram está deshabilitado y no hay captura real.
**Impacto**: no se puede afirmar que OE6 esté cumplido con una alerta enviada.
**Resolución propuesta**: mantener Telegram como opcional y reclasificar OE6 si no se obtiene evidencia real.

### IN-05 — Idioma y correcciones de redacción en la KB
**Documento A dice**: la KB se genera en español técnico.
**Documento B dice**: algunos borradores iniciales pueden contener términos en inglés o errores de tipeo.
**Impacto**: reduce calidad editorial y puede filtrar términos no deseados a la tesis.
**Resolución propuesta**: revisar la KB antes de usarla como fuente del documento final.

### IN-06 — El extractor de entidades matchea por subcadena, sin límites de palabra
**Detectado**: 2026-10-01, durante la jornada 1 de la ventana B5, al revisar el campo `entities`
de los posts ingeridos.
**Documento A dice**: `Extract Entities` extrae CVE, emails, IPs, dominios y productos, y es la
fuente del campo `entities` que la tesis usa como evidencia de OE4.
**Documento B dice**: el nodo busca el término con `includes()` sobre el texto normalizado, sin
exigir límites de palabra. Un término que aparece **dentro** de otra palabra se cuenta como
mención.
**Caso verificado**: el post *"WordPress malware in official WooCommerce theme (**Kiosko**):
hidden admin users and corrupt..."* quedó con `entities->'products' = ["ios"]`, extraído de
"K**ios**ko". El término del diccionario es `ios` (iOS de Apple) y no aparece en el texto.
**Impacto acotado**: la **clasificación no se ve afectada** — ese post fue clasificado
`Malware` por otros términos del diccionario. Lo que se degrada es la **calidad del campo
`entities`**, que queda con falsos positivos y por lo tanto no es confiable como evidencia
cuantitativa de menciones sin un ajuste posterior.
**Por qué no se corrige ahora**: la ventana B5 está en curso. Cambiar el extractor a mitad de
ventana haría incomparables los `entities` de los días anteriores y posteriores. El cambio de
comportamiento debe ocurrir **fuera de la ventana** y declararse como cambio de versión.
**Resolución propuesta**: agregar límites de palabra al extractor (regex con `\b`, o
comparación por token) en `V4/scripts/generar_workflow.py`, regenerar el artefacto, y tratar el
campo `entities` ya recolectado como afectado por la limitación conocida. Requiere change
propio en el roadmap y decisión de los autores sobre si se recalcula `entities` sobre el
corpus ya ingerido o se declara la limitación tal cual.

### IN-07 — El denominador por subreddit de la ventana no coincide con el alcance real
**Detectado**: 2026-10-02, al regenerar la bitácora del 2026-10-01 con `V4/scripts/bitacora_b5.py`.
**Documento A dice**: `V4/evidencias/VENTANA_B5.md` §6 fija el denominador de **todo** desglose por
subreddit de la ventana en tres comunidades: `r/argentina`, `r/devsarg`, `r/derechogenial`. Es el
alcance del Plan B.
**Documento B dice**: el workflow en ejecución (`Prepare Subreddits`, fuente de verdad
`V4/scripts/generar_workflow.py`) monitorea **otro** conjunto: `r/netsec`, `r/Malware`, `r/devsarg`
(Plan C). Los posts ingeridos lo confirman: `SELECT subreddit_id, COUNT(*) FROM posts GROUP BY 1`
devuelve solo esas tres claves.
**Estado verificado de `subreddits`** (6 filas, con duplicados):

| `id` | `display_name` | `active_monitoring` | posts |
|---|---|---|---|
| `argentina` | `r/argentina` | false | 0 |
| `derechogenial` | `r/derechogenial` | **true** | 0 |
| `DerechoGenial` | `r/DerechoGenial` | false | 0 |
| `devsarg` | `r/devsarg` | true | 120 |
| `Malware` | `r/Malware` | true | 101 |
| `netsec` | `r/netsec` | true | 104 |

**Tres problemas encadenados**:
1. **§6 de `VENTANA_B5.md` está desactualizada**: nombra un conjunto de tres comunidades que el
   sistema ya no monitorea. Como §6 gobierna todo porcentaje por subreddit de la ventana,
   cualquier cifra calculada con ese denominador sería incorrecta.
2. **`r/derechogenial` figura con `active_monitoring = true` pero el workflow nunca la ingiere.**
   Es un resto del Plan B: la base declara activa una comunidad que el pipeline no consulta, y por
   eso el script de bitácora advierte `4 de 3 esperados`.
3. **Duplicados en `subreddits`**: `derechogenial`/`r/derechogenial` y `DerechoGenial`/`r/DerechoGenial`
   son la misma comunidad con distinta capitalización, en dos filas. Ninguna tiene posts.
**Por qué no se corrige unilateralmente**: definir cuál es el conjunto de comunidades del alcance y
qué hacer con las filas del Plan B es una decisión de los **autores con sus directores**, no una
corrección técnica. La regla dura del proyecto impide **eliminar** un subreddit; la vía prevista es
desactivarlo con `active_monitoring`, y en este caso además habría que decidir si las filas
duplicadas se consolidan o se conservan.
**Resolución propuesta**: (a) actualizar §6 de `VENTANA_B5.md` con el conjunto del Plan C una vez
confirmado por los autores; (b) poner `active_monitoring = false` en `r/derechogenial` para que la
base no declare activa una comunidad que el pipeline no consulta; (c) decidir el destino de
`r/argentina` y de las dos filas de derechogenial, conservando la evidencia histórica de B4.

### IN-08 — El 429 de Reddit aborta el ciclo de ingesta y la corrida figura como `success`
**Detectado**: 2026-10-02, al contrastar los conteos de items que el usuario veía en el editor de
n8n contra el detalle de las ejecuciones preservadas en la base de la instancia.
**Síntoma**: algunas corridas muestran `300 items` y `Loop Over Items` con 4 pasos; otras muestran
`101 items` y 2 pasos. **No es un error de lectura ni una diferencia de comentarios** — la tabla
`comments` no participa del pipeline y la ingesta no trae comentarios de ninguna fuente.
**Causa verificada**: `Fetch Posts RSS` recibe **HTTP 429** (*rate limit* de Reddit) al consultar
el **segundo** subreddit de la lista, que es `r/Malware` (orden en `Prepare Subreddits`:
`r/netsec`, `r/Malware`, `r/devsarg`). El nodo emite **1 ítem de error**, no un post:
`{"error": "Request failed with status code 429"}`. `Parse Reddit Posts` lo descarta y devuelve 0
posts válidos; al no haber ítems, el loop se cierra y **el tercer subreddit no se consulta en ese
ciclo**.
**Distinción entre las dos firmas numéricas**:

| Lectura en n8n | Significado |
|---|---|
| `300 items`, loop 4 pasos | corrida completa: 3 subreddits × 100 posts, más el paso de cierre |
| `101 items`, loop 2 pasos | 100 del primer subreddit + 1 ítem de error 429; el tercero se omite |

**Frecuencia observada**: se detectaron inicialmente **3 de 8** corridas automáticas del
2026-10-02 (#44, #45, #48). **Corrección al cierre de la jornada 2**: con el día completo son
**15 de 28** corridas incompletas (#44, #45, #48, #49, #51, #53, #54, #57, #58, #60, #61, #63,
#64, #66, #68), es decir un **53,6 %**, no el 37 % estimado a media jornada. Las 13 restantes
leyeron los 3. Ver `V4/evidencias/VENTANA_B5.md` §13 y §14.
**Corrección del denominador (2026-10-02, mismo día)**: el cierre anterior contaba **17 de 30**.
Son dos errores de conteo y ninguno de los dos favorece al proyecto. El rango `#39`–`#68` son 30
ejecuciones, pero **#40 y #41 son ejecuciones manuales** de la rama de anomalías, no de ingesta:
sumarlas al numerador y al denominador a la vez inflaba la tasa. Las automáticas de ingesta son
**28** (`#39` + `#42`–`#68`), de las cuales **13** fueron completas y **15** quedaron en 2/3.
**Por qué no lo detecta n8n ni el estado de la corrida**: `status` es `success` en las tres. El
fallo viaja *dentro* de un ítem, no como error de ejecución, así que ni el editor ni el log de
ejecuciones lo standout. Solo se ve al desarmar el detalle de `runData` de cada corrida.
**Alcance real del daño — "no se perdió nada" no equivale a "no se puede perder nada"**: Reddit
sirve las últimas ~100 entradas de `new/.rss`. Un post que no se leyó vuelve al tick siguiente
**si sigue dentro de esa ventana**, y el upsert sobre `post_id` es idempotente, de modo que no se
duplica. Pero si un subreddit publica **más de 100 posts entre dos ticks** y ese tick recibe un
429, los que quedaron fuera de la ventana **se pierden sin que nada lo registre**. Para `r/Malware`
—no pasó: prácticamente no publicó en la ventana (101 posts en total, 100 de ellos el 2026-10-01
13:16 y 1 el 2026-10-02 12:16), así que no había nada que recuperar—. Para `r/devsarg`, que es el
subreddit activo, el riesgo es real: 122 posts, 14 insertados en un mismo tick.
**Por qué no se corrige ahora**: la ventana B5 está en curso y el día 2026-10-01 ya se contabilizó
con 307 posts. Cambiar el comportamiento del pipeline a mitad de ventana volvería incomparables las
jornadas anteriores y posteriores.
**Causa raíz de fondo (verificada contra la wiki oficial de Reddit, actualizada 2026-05-11)**: el
acceso anónimo no es "un límite de 10 QPM" sino tráfico no autenticado que Reddit declara que
debe bloquearse: *"Traffic not using OAuth or login credentials will be blocked, and the default
rate limit will not apply"* y *"We can and will freely throttle or block unidentified Data API
users"*. Por eso el 429 es irregular y por eso afecta de forma posicional al que llega segundo.
Desde noviembre de 2025 (Responsible Builder Policy) el botón `create app` de `prefs/apps` ya no
crea una app: la ruta real es un *Data Access Request* revisado a mano, con 2 a 4 semanas de
demora y denegación posible sin apelación. El programa **Reddit for Researchers (RFR)** —gratuito,
para investigación académica no comercial— exigiría aprobación institucional del profesor, que se
dio por **no viable**. **En consecuencia, el arreglo del 429 no puede depender de OAuth** y debe
resolverse íntegramente del lado del workflow.
**Resolución aplicada (2026-10-02, commit `4a2f7c1`)**: implementada en
`V4/scripts/generar_workflow.py` (16 → 17 nodos). No publicada: B5 sigue abierta y publicar el
cambio a mitad de ventana volvería incomparables las jornadas.

| | Mecanismo | Estado |
|---|---|---|
| (a) | **Aislar el 429**: el item de error se convierte en un centinela `_skip` que recorre la cadena para que el loop siempre cierre sus 3 iteraciones; se descarta antes de escribir | **Aplicado y verificado en producción** |
| (b) | **Backoff**: espera fija de 60 s entre subreddits (antes 30 s) | **Aplicado a medias — ver abajo** |
| (c) | **Rotación** del orden, determinista por ranura de 15 min | **Aplicado** |
| (d) | Leer `Retry-After` / `X-Ratelimit-*` | **No aplicable — ver abajo** |

**(a) en detalle.** El bug de raíz era que el cierre del loop venía de `Upsert Posts`. Con un 429 el
centinela se filtraba antes de escribir, el nodo Postgres quedaba con 0 ítems de entrada, no se
ejecutaba y devolvía 0 ítems: el loop se quedaba sin nada que procesar y cerraba antes de la tercera
iteración. El cierre se movió a `Extract Entities`, que siempre entrega al menos el centinela, y se
agregó `Prepare Upsert` para filtrarlo justo antes de la base. La guarda vive en SQL
(`WHERE COALESCE($13, FALSE) = FALSE`) y no en un IF previo, porque el nodo corre una query por ítem
y el IF no alcanza cuando el centinela llega mezclado con posts reales.

**(d) no se puede hacer con este nodo.** El nodo RSS Read no expone las cabeceras de respuesta, y
para leerlas habría que reemplazarlo por HTTP Request + parseo de Atom, es decir rehacer el camino
de parsing que hoy funciona. Además el motor topa `waitBetweenTries` en **5000 ms**
(`update-workflow.tool.js:69` → `.max(5000)`), de modo que ni siquiera el backoff podría delegarse
al reintento nativo del nodo: la espera larga tiene que vivir en un nodo `Wait`, que es lo que hace
el punto (b). Queda declarado como limitación, no como pendiente resuelto.

**Efecto esperado, con honestidad sobre lo que no se sabe**: (a) garantiza que los 3 subreddits se
consulten siempre, así que una corrida pasa de 1/3 a 2/3 subreddits cuando hay un 429. (b) y (c)
apuntan a reducir la tasa de 429, pero eso **no está verificado**: depende de un umbral de Reddit que
no está documentado para tráfico anónimo y que la propia Reddit dice que puede cambiar libremente.
La verificación real es empírica y va en la bitácora de las jornadas siguientes.

**(b) quedó a medias, y el motivo es técnico.** Se implementó una espera adaptativa de 60 s / 90 s
según si el subreddit anterior había dado 429, leída de static data. **No funciona**: el nodo Wait
declara `amount` como `{type:'number', validateType:'number'}` y n8n **no castea a número** el
resultado de una expresión en un campo de ese tipo, así que el nodo aborta con *"Invalid wait amount.
Please enter a number that is 0 or greater"* y la ingesta entera muere ahí. Verificado contra el nodo
instalado (`Wait.node.js`), no es una suposición. Se revirtió a una espera **fija de 60 s**, que ya
es el doble de los 30 s originales y deja la corrida en 1 req/min. El flag `ultimo_429` se sigue
escribiendo en `Parse Reddit Posts` porque sirve de evidencia en `runData`, pero ya no controla la
espera. Una espera adaptativa real tendría que pasar por un Code node que emita el número, no por una
expresión en el campo del Wait.

**Verificación en producción (2026-10-04)**: primera corrida con la versión nueva, 32 posts y **3 de 3
subreddits** en la ventana del día (antes 2 de 3 cuando había 429), run de 14:54:08 a 14:56:13.
Confirma (a). No confirma (b) ni (c): eso recién se ve en las jornadas siguientes.

Mientras tanto, la incompletitud de cualquier tick debe leerse del detalle de `runData` y **nunca**
del `status` de la corrida.

## Preguntas abiertas priorizadas

| Prioridad | Pregunta | Bloquea | Decisor |
|---|---|---|---|
| Alta | ¿Cuál es la fecha de inicio de la ventana real y cuándo se cierra? | B5, métricas del Cap. 5 | Autores con sus directores |
| Alta | ¿Se puede conseguir una submuestra de 100 posts para el evaluador externo? | E14, Kappa y matriz de confusión | Autores / facultad |
| Alta | ¿Se habilita Telegram para obtener E12 o se retira/reclasifica OE6? | E12, alcance de alertas | Autores |
| Media | ¿Se conserva la ventana actual o se reinicia la recolección con métricas corregidas? | Comparabilidad de resultados | Autores con tribunal |
| Media | ¿Se obtiene una developer account de Reddit para recuperar score/comentarios? | Alcance de la fuente y OE2 | Autores |
| Media | ¿La tabla `comments` queda como parte del modelo no implementada? | Descripción del artefacto y alcance | Autores |
| Media | ¿Cuál es la fórmula exacta y documentada del score? | Sección 4.4 y evaluación | Autores / técnica |
| Media | ¿Se corrigen los límites de palabra del extractor de entidades fuera de la ventana B5, y se recalcula `entities` sobre el corpus ya ingerido? (IN-06) | Calidad del campo `entities`, evidencia de OE4 | Autores / técnica |
| **Alta** | ¿Cuál es el conjunto de comunidades del alcance: Plan B (`r/argentina`, `r/devsarg`, `r/derechogenial`) o Plan C (`r/netsec`, `r/Malware`, `r/devsarg`)? (IN-07) | **Todo porcentaje por subreddit** de la ventana, §6 de VENTANA_B5.md | **Autores con sus directores** |
| Media | ¿Se agrega manejo explícito del 429 (reintento con backoff y/o rotación de subreddit) fuera de la ventana B5? (IN-08) | Integridad de la cobertura de la ventana; hoy 3 de 8 ticks leen 2 de 3 subreddits sin registrarlo | Autores / técnica |
| Baja | ¿Se puede obtener E15 (copia del antecedente de Rivas y Dengra)? | Marco teórico H-10 | Autores / biblioteca |
| Baja | ¿Se versionan las evidencias binarias grandes o solo exports reproducibles? | Tamaño y higiene del repositorio | Autor operador |

## Estado de seguimiento de las preguntas priorizadas

Actualizado el **2026-09-25** por el change `ventana-recoleccion-b5` (C-05). Ninguna pregunta de
la tabla cambia de identidad ni se cierra: se registra su estado de avance.

| Pregunta | Estado | Constancia |
|---|---|---|
| ¿Cuál es la fecha de inicio de la ventana real y cuándo se cierra? (prioridad **Alta**) | **Parcialmente resuelta — sigue abierta.** Inicio **fijado el 2026-09-25** (inmutable); **fecha de corte `no fijada`**, pendiente de la decisión de los autores con sus directores (tarea **6.1** del change C-05) | `V4/evidencias/VENTANA_B5.md` §1 y §3 |
| ¿Se conserva la ventana actual o se reinicia la recolección con métricas corregidas? (prioridad **Media**) | **Abierta.** Sin decisión de los autores (tarea 6.2). Su acumulación es de 0/10 días completos evaluados al 2026-09-25, así que tampoco hay base para decidir | `V4/evidencias/VERIFICACION_INSTANCIA_2026-09-25.md` §7 |

**Limitación conocida de la evidencia de falla:** el log de ejecuciones de la instancia n8n no
está disponible ni preservado, por lo que el éxito de la ingesta **día por día no puede probarse
desde el log**; la bitácora lo declara como `sin observación` y su transcripción es manual
cuando el log exista (tarea 3.5 del change C-05, decisión D-3). Ver
`V4/evidencias/VERIFICACION_INSTANCIA_2026-09-25.md` §6.

## Decisiones pendientes para el próximo change

1. Definir la ventana de B5 y sus parámetros de corte.
2. Congelar el export del workflow y corregir la diferencia de conteo de nodos.
3. Ejecutar las consultas E4 y E6 sobre la base real.
4. Decidir si se completa o se retira la submuestra externa.
