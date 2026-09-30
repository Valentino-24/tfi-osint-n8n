## Context

El pipeline funciona de punta a punta sobre Docker: 16 nodos, seudonimización HMAC, idempotencia del upsert verificada, y tres comunidades ingiriendo sin duplicados. El componente que no funciona es el de clasificación.

`CLASSIFY_CODE` (`V4/scripts/generar_workflow.py:89-128`) implementa un clasificador por diccionario con cinco categorías. La evidencia del 2026-09-30 sobre los 301 posts ingeridos muestra que su cobertura léxica no corresponde al alcance de la tesis: 3 clasificaciones positivas en total, 1 de ellas falso positivo por coincidencia con términos genéricos, y 0 detecciones al sustituirlo por un diccionario bilingüe de nueve categorías sobre el mismo corpus.

La causa de ese 0 no es el diccionario nuevo sino el corpus. Medido con el diccionario nuevo sobre 100 posts por comunidad: `r/malware` 19%, `r/netsec` 6%, `r/cybersecurity` 3%, `r/reverseengineering` 3%, `r/devsarg` 0%. Los subreddits monitorizados son generalistas —política, programación, derechos del consumidor— y no contienen tráfico de amenazas.

Restricciones que gobiernan el diseño:

- **El DDL no se toca.** `posts.nlp_category` es `VARCHAR(100)` sin dominio, y `nlp_score` tiene `CHECK (nlp_score BETWEEN 0 AND 1)`. Ninguna categoría nueva requiere migración.
- **`B_workflow.json` nunca se edita a mano.** Es artefacto de `generar_workflow.py` (regla dura de `AGENTS.md`).
- **Sin muestra etiquetada no hay métrica de desempeño.** Cinco criterios de aceptación están RETIRADOS en la tesis por esta razón. Ninguna cifra de este change rehabilita uno.
- **Ninguna cifra se declara sin su consulta, fecha, ventana y `n`** (RN-GL-01).
- **RN-GL-03** exige registrar el cambio de diseño antes de modificar la implementación. Este documento es ese registro.

## Goals / Non-Goals

**Goals:**

- Alinear el diccionario con el alcance de la tesis: nueve categorías sobre un eje único de tipo de amenaza, en castellano e inglés.
- Hacer la fórmula de `nlp_score` estable ante cambios del diccionario e interpretable, para poder documentarla según RN-CL-02.
- Declarar explícitamente la limitación de no lematización en lugar de esconderla detrás de formas conjugadas escritas a mano.
- Constituir la muestra de control etiquetada que hoy impide medir cualquier desempeño del clasificador.
- Convertir la selección de comunidades en una decisión con evidencia medible, no en una intuición.
- Dejar el generador y el workflow en ejecución sincronizados, para que regenerar el artefacto no revierta correcciones ya validadas.

**Non-Goals:**

- No tocar `A_DDL.sql`, ni añadir columnas, índices o constraints.
- No activar el workflow, iniciar la ventana de recolección ni modificar la definición de ventana de C-05.
- No borrar ni desactivar la fila huérfana `derechogenial` de `subreddits`.
- No declarar precisión, recall, F1, Kappa ni matriz de confusión: son resultado de la muestra de control, no de este change.
- No tocar credenciales, tokens ni la clave HMAC.
- No seleccionar definitivamente las comunidades del corpus: este change produce la evidencia, la decisión de alcance es de los autores.

## Decisions

### D-1 — La taxonomía usa un único eje: tipo de amenaza

**Qué**: las nueve categorías son `Phishing`, `Robo de Credenciales`, `Malware`, `Ransomware`, `Vulnerabilidades`, `Filtración de Datos`, `Infraestructura y Ataques`, `Hacktivismo` e `Ingenieria Social`. Todas nombran un tipo de amenaza. Ninguna nombra un origen geográfico ni un contexto.

**Por qué**: la propuesta de agregar "Ciberdelito en Argentina" junto a "Ingeniería Social" mezcla dos ejes ortogonales —técnica y procedencia— en la misma columna. Un post de ransomware publicado en Argentina y otro de phishing publicado en España caerían en la misma categoría según el eje técnico y en distintas según el geográfico, y la taxonomía no puede sostener los dos a la vez. El contexto argentino no se pierde: se captura en `posts.entities` mediante `PRODUCTS` (`mercado pago`, `dni`, `cvu`, `banco nacion`, `galicia`, `uala`), que ya existe y no se toca. Además, los nombres en inglés de las categorías facilitan la reconciliación con MITRE ATT&CK, que es el estándar que un evaluador técnico reconoce.

**Alternativas consideradas**: (a) dos ejes, técnicas y contexto, rejected porque duplica el modelo de datos y obliga a una tabla de relación nueva, es decir DDL; (b) conservar "Estafas Virtuales" como categoría propia, rejected porque solapa con las otras tres categorías sin aportar señal distinguible; (c) nombres de categoría en castellano, rejected porque `nlp_category` es el valor persistido y un evaluador familiarizado con MITRE no puede mapearlos sin tabla de equivalencia.

### D-2 — `MIN_HITS` se mantiene en 2 y la precisión se mejora por el lado del diccionario

**Qué**: `MIN_HITS` sigue en 2. Los términos genéricos se eliminan en lugar de bajar el umbral a 1.

**Por qué**: el umbral de 2 existe para compensar un diccionario con términos triviales. Bajar a 1 sin limpiar el diccionario convierte cualquier mención de "cuenta" o "banco" en una detección. Con el diccionario limpio, un único acierto sobre un término específico como `ransomware` sí es señal, pero ese es un ajuste que se decide **contra la muestra de control**, no contra los datos de producción. Medido con el diccionario nuevo sobre los 301 posts, `MIN_HITS = 1` produce 8 detecciones de las cuales al menos 5 son falsos positivos evidentes —"Sobre el sentido de aprender vs la IA" clasificado `Infraestructura y Ataques`, "Intento de ingreso a BNA+" clasificado `Filtración de Datos`. Ese resultado justifica mantener 2 hasta que exista muestra etiquetada.

**Alternativas consideradas**: (a) `MIN_HITS = 1` desde el inicio, rejected por la evidencia anterior y por convertir el umbral en un ajuste sobre datos no etiquetados; (b) subir `MIN_HITS` a 3, rejected porque sobre corpus con señal real elrecall cae por debajo de lo aceptable sin que la precisión mejore de forma medible.

### D-3 — `nlp_score` pasa a normalización saturante

**Qué**: `nlp_score = min(1, round(hits / 4, 4))`. Dos aciertos valen `0.5`, cuatro o más valen `1.0`. La constante se declara como `SATURATION = 4` en el código.

**Por qué**: la fórmula vigente `hits / |keywords(categoría)|` acopla la escala al tamaño del diccionario. Al pasar de 5 a 9 categorías y de 51 a 202 términos, un post con 2 aciertos en `Vulnerabilidades` pasa de `0.22` a `0.07` sin que la clasificación haya cambiado. Un score cuyo valor depende de cuántas palabras tiene el diccionario no es una confianza, y RN-CL-02 exige que sea una confianza normalizada e interpretable. La escala saturada es independiente del diccionario, se explica en una frase y se puede verificar a mano contra `posts.nlp_score`.

**Alternativas consideradas**: (a) normalizar contra un máximo fijo de 10, rejected porque el techo arbitrario no se sostiene cuando una categoría legitimately concentra 8 o 9 coincidencias; (b) dejar la fórmula y recalcular los scores históricos, rejected porque no se puede: los posts ya clasificados guardan el score viejo y no se re-derivan sin reprocesar el corpus, que es una operación destructiva fuera de alcance; (c) no cambiar la fórmula, rejected porque contradice RN-CL-02 en el momento en que la tesis más la necesita.

### D-4 — La ausencia de lematización se compensa con formas flexionada y se declara como limitación

**Qué**: el diccionario incluye formas conjugadas frecuentes (`filtraron`, `filtran`, `filtrado`, `hackearon`, `hackear`, `suplantan`, `clonar`, `pidieron`). El conjunto resultante tiene 202 términos sin acentos, sin guiones y sin duplicados.

**Por qué**: el clasificador hace `text.split(/[^a-z0-9]+/)` y compara por token exacto. No hay lematización, y añadirla es un cambio de alcance mayor que este change. Sin las formas conjugadas, el término `filtrar` nunca encuentra el texto "filtraron", y el caso más común del corpus en castellano queda indetectable. La alternativa —un stemmer— se difiere y se registra como deuda.

Dos restricciones del mismo mecanismo condicionan qué términos pueden escribirse: los términos con guion **nunca** matchean, porque el tokenizador los parte y el comparador de substring no aplica al no contener espacio (`zero-day` es inaplicable; debe escribirse `zero day`). Y los términos deben escribirse sin tildes, porque la normalización NFD del texto las elimina y un término acentuado nunca coincidiría.

**Alternativas consideradas**: (a) implementar lematización por sufijos en el Code node, rejected como cambio de alcance mayor, con su propia validación; (b) no incluir formas conjugadas, rejected porque deja fuera el caso dominante del corpus en castellano; (c) usar sinónimos en lugar de conjugaciones, rejected porque no cubre la flexión.

### D-5 — El diccionario se construye desde una definición, no se ajusta contra los datos de producción

**Qué**: la selección de términos sigue el esquema: definición del alcance → construcción del diccionario desde esa definición → etiquetado manual → evaluación → reporte. Ningún término se agrega porque haya hecho subir la tasa de detección en producción.

**Por qué**: si el diccionario se ajusta mirando los resultados y luego se evalúa sobre los mismos posts, la cifra resultante mide el sobreajuste y no el desempeño. Es el error que la V3 ya cometió al presentar tasas sin respaldo. Este change produce el diccionario; la evaluación se hace contra la muestra de control, que es independiente por construcción.

**Alternativas consideradas**: (a) agregar los términos quedetectan los 3 posts positivos históricos, rejected porque son 3 observaciones, dos de ellas mal clasificadas, y ajustar con 3 observaciones es sobreajuste; (b) usar el vocabulario del feed como diccionario, rejected porque el feed es el conjunto de prueba.

### D-6 — La selección de corpus se decide con medición, y la medición se archiva

**Qué**: la señal por comunidad se mide antes de decidir qué comunidades integran el corpus, y el resultado se archiva en `V4/evidencias/` con su consulta, fecha y `n`. Este change produce esa evidencia; la decisión de alcance corresponde a los autores con sus directores.

**Estado**: medición archivada el 2026-09-30 en `V4/evidencias/MEDICION_SENAL_POR_COMUNIDAD_2026-09-30.md` (censo de 520 posts, 5 comunidades, 113 con señal). Las cifras citadas abajo como 19 % y 0 % son las del momento de la decisión y **no son reproducibles hoy**: el umbral bajó de `MIN_HITS=2` a `MIN_HITS=1`. Las vigentes son 66,3 % para `r/Malware` y 1,7 % para `r/devsarg`.

**Por qué**: la medición sobre 100 posts por comunidad con el diccionario nuevo separa dos cosas que se confundían: la capacidad del clasificador y la temática de la comunidad. `r/malware` con 19% y `r/devsarg` con 0% miden lo mismo —el mismo diccionario— y la diferencia de 19 puntos no puede atribuirse al algoritmo.

**Alternativas consideradas**: (a) fijar las comunidades por afinidad temática aparente y medir después, rejected porque es el orden que produjo el desacople actual; (b) elegir la comunidad que maximiza la tasa, rejected explícitamente: elegir el corpus por su rendimiento es sobreajuste del diseño experimental y anula la validez de cualquier cifra resultante; (c) conservar el corpus actual sin medir, rejected porque la medición es lo que sostiene la decisión.

### D-7 — El rate limiting se mitiga con espaciado, no con reintentos acelerados

**Qué**: el workflow incorpora `Loop Over Items` con `batchSize: 1` y un nodo `Espera Rate Limit` de 30 segundos, de modo que las tres consultas al feed se espacian 30 s. El nodo `Fetch Posts RSS` conserva reintentos con `waitBetweenTries: 3000` y `onError: continue` como red de seguridad, no como mecanismo principal.

**Por qué**: lo medido el 2026-09-30 desde la IP del proyecto fue: 3 consultas con ~2,5 s de separación producen `200, 429, 429`; con 10 s producen `200, 200`; con 30 s producen `200, 200, 200`. Y el reintento acelerado es contraproducente: con 3 s entre intentos, `r/devsarg` recién respondió en el noveno intento y `r/derechogenial` agotó los diez. Cada intento rápido dentro de la ventana deslizable renueva el bloqueo. El espaciado satisface la restricción de la fuente; el reintento acelerado la combate y pierde.

**Alternativas consideradas**: (a) reducir `?limit=100` a `?limit=25` para reducir la carga por consulta, rejected porque el factor limitante es la frecuencia, no el tamaño: la medición falla a 2,5 s y a 5 s y funciona a 10 s, independientemente de `limit`; (b) desactivar las comunidades que devuelven 429, rejected por la regla dura de no desactivar un subreddit con datos y porque el 429 es transitorio, no una señal de que la fuente se retiró; (c) esperar el límite completo de 60 s, rejected porque 30 s es suficiente y 90 s por ciclo deja poco margen frente al scheduler de 15 minutos.

**Nota operativa**: el ciclo pasa a durar aproximadamente 2 minutos —30 s de espera por cada una de las tres iteraciones— contra los 15 minutos del scheduler. Si un ciclo excede los 15 minutos, las ejecuciones se superponen y hay que revisar `maxTries` o `waitBetweenTries`. El estado de superposición se reporta en la bitácora de C-05 si llegara a ocurrir.

### D-8 — El `subreddit_id` se deriva del identificador canónico, no del texto del enlace

**Qué**: `Prepare Subreddits` declara `DerechoGenial` con mayúscula inicial, que es la forma canónica que Reddit usa en sus URLs y la que `Parse Reddit Posts` extrae con la expresión regular `\/r\/([a-z0-9_]+)\/comments\/([a-z0-9]+)\/`.

**Por qué**: la clave foránea `posts_subreddit_id → subreddits.id` es una comparación de texto sensible a mayúsculas en PostgreSQL. Con `derechogenial` en la tabla y `DerechoGenial` en el enlace, la inserción falla. El síntoma observado fue `violates foreign key constraint "posts_subreddit_id_fkey"` en la tercera iteración del loop, con `r/argentina` y `r/devsarg` ingiriendo correctamente porque sus URLs están íntegramente en minúscula.

**Alternativas consideradas**: (a) derivar `subreddit_id` del ítem de `Prepare Subreddits` en lugar de la URL, rejected como cambio de alcance del nodo Parse; (b) normalizar a minúsculas con `lower()` en el upsert, rejected porque agrega una función a la ruta crítica de escritura y oculta la discrepancia en lugar de corregirla en su origen; (c) desactivar el subreddit problemático, rejected por la regla dura de no eliminar ni desactivar un subreddit con datos.

### D-9 — Corpus mixto: dos comunidades de seguridad y una técnica en castellano

**Qué**: el corpus de la ventana queda compuesto por `r/netsec`, `r/Malware` y `r/devsarg`. Se desactivan con `active_monitoring = false` `r/argentina` y `r/DerechoGenial`, y se conservan sus 201 posts.

**Por qué**: el proyecto tiene dos preguntas que un corpus monolítico no responde. La primera es si el clasificador detecta amenazas; para eso hace falta una comunidad donde el tráfico de amenazas exista. La segunda es si el método es viable sobre una comunidad técnica local; para eso hace falta una comunidad argentina. Un corpus mixto responde ambas, y la comparación entre sus brazos es la que produce el hallazgo sobre la barrera.

El criterio de inclusión es **temático y previo**, no empírico: una comunidad entra si su tema declarado es seguridad de la información, y `r/devsarg` entra por ser la comunidad técnica argentina de referencia. Ninguna comunidad entra ni sale por su tasa de detección.

**Alternativas consideradas**: (a) solo seguridad, rejected porque elimina el brazo local y con él la pregunta sobre aplicabilidad local; (b) solo castellano, rejected porque la medición muestra que la señal es cero y el sistema no sería evaluable; (c) las cuatro comunidades de seguridad más `r/devsarg`, rejected por costo de tasa de llamadas: el ciclo crecería de 3 a 5 iteraciones y, a 30 s de espaciado, de 2 a 3 minutos, con el riesgo de solapamiento contra el scheduler de 15 minutos que D-7 ya registra.

**Consecuencia metodológica asumida**: la medición de señal se hizo sobre estas mismas comunidades antes de fijar el corpus, y `r/netsec` y `r/Malware` son las dos de mayor tasa. La consecuencia es que **la tasa de señal observada en el corpus final no puede usarse como estimación de desempeño**, porque la comunidad se seleccionó por esa misma tasa. Esta restricción se escribe en la evidencia y en el spec, no se resuelve re-midiendo sobre el mismo conjunto. La única estimación válida de desempeño es la que salga de la muestra de control, que es independiente por construcción (D-5).

**Consecuencia operativa**: `r/Malware` aparece con mayúscula inicial en las URLs de sus permalinks, igual que `r/DerechoGenial`. `subreddit_id` se deriva del link y se compara exacto contra la PK, así que `PREPARE_SUBS` MUST declarar `Malware` y no `malware`. Es el mismo modo de falla que D-8 y la misma clase de bug.

### D-10 — Los settings por nodo van en la raíz, y el backoff de reintento está topado a 5 s

**Qué**: dos correcciones en el nodo `Fetch Posts RSS`. (a) Los settings de mitigación ante 429/403 se mueven de la clave `node.settings` a la raíz del objeto nodo. (b) `waitBetweenTries` sube de 3000 ms a 5000 ms. En paralelo, RN-FU-03 se reescribe de "3 reintentos con 30 s" a "3 reintentos con hasta 5 s", y `Parse Reddit Posts` descarta de forma explícita los items que llegan con `.error`.

**Por qué**: la corrida de control del 2026-09-30 (ejecución 9, 04:30:13 → 04:31:47) terminó en `error` con HTTP 429 en `r/devsarg`, abortando el ciclo. La causa no fue el rate limit ni el espaciado de 30 s, que funcionaron: el motor de n8n 2.40.6 lee los settings por nodo desde la **raíz**, no desde una clave `settings`.

| Referencia en n8n-core 2.40.6 | Campo que lee |
|---|---|
| `dist/execution-engine/workflow-execute.js:933` | `node.retryOnFail` |
| `:937` | `node.maxTries` |
| `:938` | `node.waitBetweenTries` |
| `:563` | `node.continueOnFail` |
| `:564` | `node.onError` |

Bajo `node.settings` los cinco campos quedan ignorados. Dos firmas lo confirman en la ejecución 9: el intento fallido duró **400 ms** cuando `maxTries: 3` con `waitBetweenTries: 3000` exigirían ≥6 s, y la ejecución terminó en error global pese a `onError: continueRegularOutput`. La mitigación existía en el código y nunca se aplicó.

La misma línea `:938` establece el techo del backoff nativo: `Math.min(5000, Math.max(0, node.waitBetweenTries || 1000))`. Los 30 s por reintento de la redacción original de RN-FU-03 eran **imposibles por configuración**, no una omisión del proyecto.

**Alternativas consideradas**: (a) mover los settings a la raíz y aceptar el techo de 5 s, **elegida** porque cierra la causa raíz con un cambio mecánico y declara el límite como impuesto por la plataforma; (b) cambiar `rssFeedRead` por HTTP Request con parseo manual de Atom y backoff exponencial, rejected porque no resuelve el techo de 5 s por sí sola —el retry nativo sigue topado— y agrega superficie de código sin cubrir el caso observado; (c) implementar los 30 s con un nodo `Wait` explícito entre reintentos, rejected por complejidad y porque rompe la trazabilidad de qué request falló. Con el espaciado de 30 s **entre** subreddits que ya aporta `Espera Rate Limit`, la cobertura del caso observado no cambia.

**Consecuencia asumida**: un 429 que agote los 3 intentos deja al subreddit con **0 posts** en esa corrida y el ciclo **continúa** con el resto. Ese 0 es *no intentado*, no *Reddit no sirvió posts*, y se registra aparte del incidente 1 de `CARACTERIZACION_RATE_LIMIT.md` para no contaminar la comparación de cobertura. El subreddit NO se desactiva: `active_monitoring` permanece en `true`.

## Risks / Trade-offs

- **[La tasa de señal del corpus final no es una estimación de desempeño]** → D-9 lo declara: el corpus se fijó tras medir esas mismas comunidades, y dos de ellas se eligieron por su tasa. La cifra se archiva como caracterización del corpus, nunca como desempeño. La estimación de desempeño viene exclusivamente de la muestra de control. Si esto no queda escrito, cualquier revisor lo leerá como sobreajuste; escrito, es una limitación conocida con su alcance delimitado.

- **[Desactivar dos comunidades reduce la cobertura local del resultado]** → `r/argentina` y `r/DerechoGenial` quedan con `active_monitoring = false` y sus 201 posts intactos. La ventana pierde contexto local generalista y gana contexto local técnico. Es un intercambio deliberado, no una mejora: se declara como tal para que el resultado no se lea como más representativo de lo que es.

- **[El ciclo crece si se añaden comunidades de seguridad]** → D-9 fija 3 comunidades y ~2 minutos por ciclo. Si el scheduler de 15 minutos presenta superposición, se ajusta `waitBetweenTries` y se reporta, no se añaden comunidades.

- **[La muestra de control puede seguir sin suficiente señal positiva]** → Con `MIN_HITS = 2` y las tasas observadas, una muestra de 50 posts del corpus mixto puede contener pocos positivos. Si hay muy pocos, precisión se puede calcular pero recall queda con intervalo muy amplio. Se declara y se agranda la muestra; no se reporta recall sobre 3 positivos como si fuera estable.

- **[La muestra de control etiquetada puede resultar demasiado pequeña para métricas estables]** → 50 posts es el mínimo asumido. Si la distribución de clases la vuelve inestable, se declara la inestabilidad y se agranda la muestra; no se reporta una métrica sin su `n` ni su intervalo. El coeficiente Cohen's Kappa sobre 50 observaciones con clases desbalanceadas tiene una confianza baja, y eso se declara junto al número.

- **[Un vocabulario bilingüe puede introducir falsos positivos por polisemia del inglés]** → Términos como `packed`, `loader`, `miner` y `poc` son ambiguos en inglés. Se conservan porque `MIN_HITS = 2` exige un segundo acierto, pero la muestra de control es donde se detecta el problema. Si aparecen falsos positivos sistemáticos, se retiran en un change posterior con la evidencia de la muestra.

- **[Regenerar el artefacto reimporta el workflow y pierde la credencial de PostgreSQL]** → Es el riesgo operativo conocido de la regla dura. La mitigación es reasignar la credencial inmediatamente después de importar, y verificar que los cuatro nodos PostgreSQL la tengan asignada antes de dar por buena la corrida. No se asume que la importación la conserve.

- **[La fila huérfana `derechogenial` queda en `subreddits` sin posts]** → No se borra en este change. `active_monitoring` permanece en `true` en las cuatro filas. La limpieza requiere su propio change y no puede ejecutarse junto a una modificación de diseño.

- **[C-10 y C-13 quedan bloqueados por este change]** → Es intencional: la matriz de confusión y el Anexo C se construyen contra nueve categorías, no contra cinco. Construirlos antes obligaría a rehacerlos.

- **[El ciclo de 2 minutos por iteración se superpone con el scheduler si Reddit degrada]** → Se reporta la superposición en la bitácora en lugar de ocultarla. El ajuste de `maxTries` y `waitBetweenTries` es operativo y no modifica el diseño del espaciado.

## Migration Plan

No hay migración de esquema. Los posts ya clasificados conservan su `nlp_category` y `nlp_score` antiguos; **no se reprocesan**. Declarar que las filas anteriores a este change usan la fórmula vieja es parte del reporte, porque comparar scores de ambas Convenience sin decirlo sería una inconsistencia silenciosa.

Orden de aplicación:

1. `DICT` de nueve categorías, retirement de términos genéricos y formas conjugadas en `generar_workflow.py`.
2. Fórmula de score saturante con `SATURATION = 4`, y actualización de los comentarios de cabecera del Code node.
3. `PREPARE_SUBS` con `DerechoGenial`.
4. Nodos `Loop Over Items` y `Espera Rate Limit` con su cableado, y `settings` del nodo RSS.
5. Regeneración de `B_workflow.json` y verificación estructural: 16 nodos, 9 categorías, cables presentes, sin secretos.
6. Reimportación en n8n y reasignación explícita de la credencial de PostgreSQL.
7. Ejecución de control y verificación de la ingesta con las tres comunidades.
8. Recolección de la muestra de control etiquetada.
9. Cálculo de métricas sobre la muestra.
10. Actualización de KB, tesis, Tabla 6 y Anexo C.

Rollback: revertir `generar_workflow.py` y regenerar `B_workflow.json`. El estado en `tesi_osint` no se altera por ninguna tarea de este change, salvo la inserción normal de posts por el pipeline. La fila huérfana y las 301 filas existentes permanecen en cualquier caso.

## Open Questions

1. ~~**Composición final del corpus**~~ — **RESUELTA el 2026-09-30**: corpus mixto `r/netsec` + `r/Malware` + `r/devsarg`, con desactivación de `r/argentina` y `r/DerechoGenial`. Decisión registrada en D-9.

6. **Si el corpus mixto basta para que la muestra tenga señal positiva** — con `MIN_HITS = 2` y las tasas observadas, `r/netsec` aporta 6% y `r/Malware` 19%. Una muestra de 50 posts del corpus mixto podría tener pocos positivos, suficiente para calcular precisión pero con intervalo muy amplio para recall. La decisión es si se agranda la muestra, si se acepta el intervalo amplio declarándolo, o si se reconsidera `MIN_HITS` contra la muestra etiquetada. Bloquea el grupo 7 de tareas.

2. **Tamaño final de la muestra de control** — 50 es el mínimo asumido. Si la distribución de clases resulta desbalanceada o Kappa inestable, se decide si se agranda y a qué `n`, y se declara.

3. **Criterio de etiquetado de la muestra** — qué cuenta como "post de amenaza" para los autores. Es la definición de la variable dependiente y condiciona todas las métricas. Sin acuerdo explícito con los directores, las métricas no son defendibles aunque sean calculables.

4. **Reimplementar o mantener la clasificación de los posts previos** — los 301 posts existentes quedaron con la taxonomía de cinco categorías y la fórmula de score anterior. Si la tesis los incluye, su clasificación es heterogénea respecto de la ventana nueva. Decisión de alcance, no técnica.

5. **Cuándo se implementa lematización** — deuda registrada en D-4. Depende de si la muestra de control muestra pérdida de recall por flexión.
