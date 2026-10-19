## Context

La V2 (6,0/10) es la base textual obligatoria: el tribunal de V3 (5,5/10, NO APROBADO) ordenó reconstruir la V4 sobre ella porque la V3 condensó el documento de 39 a 24 páginas y resolvió correcciones **por declaración o supresión**, no por evidencia (N-03). Los autores descartan el borrador V4 de 125 páginas y fijan el orden de magnitud de la V2 (~40 páginas).

El sistema real difiere de lo que describen V2 y V3 en puntos estructurales: la fuente es **RSS/Atom público** (no la API con OAuth2), el clasificador vigente tiene **9 categorías y 201 términos** (no 5), el corpus real es la ventana B5 cerrada con **724 posts y 15 días** (no 8.240 posts en 181 días) y la muestra de control real es **n = 50** (no 500). El informe V4 debe describir el sistema que existe, no el que las versiones anteriores declaraban.

## Goals / Non-Goals

**Goals**

- Producir `V4/devoluciones/tesis_v4.md`: el informe completo, autocontenido, en Markdown, con la estructura de capítulos que el proyecto viene usando.
- Fijar un presupuesto de extensión por capítulo (42–48 páginas equivalentes) para que la V4 no repita ni la condensación de 24 páginas de V3 ni las 125 páginas del borrador descartado.
- Restituir el contenido que la V3 eliminó y que el tribunal valoró (protocolo 3.3, entorno de pruebas, tabla 4.2, modismos, priorización del Cap. 8, citas 2.1.3, Anexo B).
- Sostener cada cifra con su consulta, su fecha y su `n`; retirar toda cifra heredada.
- Cerrar, en el texto, los 8 ítems bloqueantes de la Sección 9 en lo que depende de la redacción y de la evidencia disponible.

**Non-Goals**

- No producir PDF ni `.docx`: el entregable es Markdown; la conversión la hace el usuario.
- No modificar la base, el DDL, el artefacto del workflow, `generar_workflow.py`, nodos ni credenciales.
- No publicar ni activar el workflow (regla dura: lo hace el operador desde la UI).
- No cerrar formalmente C-08 a C-11 ni declarar E4/E5/E6/E7/E8 como evidencias consolidadas: este change toma lecturas de redacción y las archiva con trazabilidad.
- No inventar métricas, ni «proyectar» resultados, ni completar tablas con datos de V2/V3.
- No reescribir la KB ni `CHANGES.md` en este change.

## Decisions

### D-1 — Base V2, una sola pieza, sin plan embebido

El texto se reconstruye desde `V4/devoluciones/tesis_v2.txt` (cuerpo real, líneas 2614–3442), no desde `tesis_v3.md`. La V3 aporta únicamente correcciones puntuales que el tribunal validó. El entregable es **un solo archivo** `V4/devoluciones/tesis_v4.md`; el plan capítulo por capítulo vive en este `design.md`, no dentro del informe.

- **Alternativa**: un archivo por capítulo en `V4/capitulos/` (lo que preveía C-16). **Descartada**: el usuario necesita una pieza única para pasarla a otra herramienta y generar el PDF.
- **Consecuencia**: C-16 no produce los archivos por capítulo; cuando se archive, deberá referenciar este change. La normalización de la V2 sigue siendo un paso interno (tarea 1.1).

### D-2 — Presupuesto de extensión cerrado

El informe se escribe contra un presupuesto, no contra «lo que salga». Total objetivo: **42–48 páginas equivalentes** (16.000–19.000 palabras, sin contar tablas ni figuras). Si un capítulo se pasa, se recorta antes de agregar en otro. El Cap. 4 es el más extenso (núcleo del artefacto), seguido del Cap. 5.

| Bloque | Páginas objetivo |
|---|---|
| Resumen + Abstract | 2 |
| Cap. 1 Introducción | 5 |
| Cap. 2 Marco teórico y estado del arte | 4,5 |
| Cap. 3 Marco metodológico | 5,5 |
| Cap. 4 Desarrollo del sistema | 8,5 |
| Cap. 5 Resultados | 6,5 |
| Cap. 6 Discusión | 3 |
| Cap. 7 Conclusiones | 3 |
| Cap. 8 Recomendaciones | 2 |
| Referencias | 2,5 |
| Anexos A–D | 4 |
| **Total** | **~46** |

> **Desviación registrada al cerrar el apply (2026-10-19).** El cuerpo del entregable quedó en **20.364 palabras de prosa** (21.042 con portada, índices y siglas), ≈ **51 páginas** a 400 palabras/página, o sea **≈ 7 % sobre el techo**. El exceso no es relleno: proviene de correcciones exigidas por las dos evaluaciones y agregadas después del control de presupuesto (entorno de ejecución de H-06, ejemplos de modismos de H-09, condiciones de configuración de n8n de H-01c, nota de cambio de umbrales de N-05, priorización esfuerzo/impacto de N-03 en el Cap. 8, aclaración del residual en el Cap. 5). Se decidió **no recortar**: el tribunal reprobó la versión anterior por resolver las correcciones borrando contenido. Si se requiere volver a 48 páginas, los recortes candidatos son el Cap. 5 (cifras repetidas ya tabuladas) y el Cap. 2 (listado de herramientas), nunca el Cap. 4. Detalle en `V4/evidencias/informe_v4_2026-10-19/CHECKLIST_CORRECCIONES.md` §5.3.

### D-3 — Solo datos reales, con trazabilidad obligatoria

Toda cifra del informe cumple una de estas tres condiciones:

1. Proviene de una consulta `SELECT` archivada en `V4/evidencias/informe_v4_2026-10-19/` con su SQL, fecha y `n`.
2. Proviene de un archivo de evidencia existente, citado por nombre y fecha.
3. Es una especificación de diseño (versión de motor, scheduler, tamaño de diccionario, fórmula), verificable contra el código o el DDL.

Ninguna otra cifra entra. La tabla de cifras prohibidas (§ más abajo) es de cumplimiento obligatorio en la verificación final.

### D-4 — Huecos: producir, declarar o retirar

Cuando falta un dato:

- Si es una **consulta de solo lectura** o un archivo que ya existe → se produce en este change (tarea 2.x) y se archiva.
- Si requiere un trabajo que no existe (evaluador externo, benchmark nuevo, captura-recaptura) → **se declara la limitación en el capítulo correspondiente y se retira la afirmación** que dependía de ella.
- **Prohibido** dejar `[COMPLETAR]` sin dueño, sin evidencia asociada y sin fecha. Si un hueco no se puede cerrar, el texto debe poder leerse sin él.

### D-5 — Decisiones métricas que el informe adopta y declara

| Métrica | Decisión | Por qué |
|---|---|---|
| **Cobertura** | **Se retira** de §1.6, Resumen, Abstract, Cap. 5 y Cap. 7 | E8 (captura–recaptura) no es ejecutable con una sola fuente y una sola captura; el tribunal admite retirarla antes que dejarla «parcial» sin justificar (H-05, C-11) |
| **Latencia** | Se mide `ingested_at − created_utc` con `n`, media, DS, P50 y P95; el criterio «P95 ≤ 5 min» de §1.6 se conserva y **se declara NO CUMPLIDO si la medición lo confirma**, explicando que el scheduler es de 15 min y que la antigüedad del post al ingerirse depende de la profundidad del feed | N-01: no se mueve el umbral después de medir; nunca criterio y diseño a la vez |
| **Throughput** | Se reporta el **valor medido en operación** (724 posts en 17 días ≈ 1,8 posts/h de promedio; máximo diario observado: 307) y se contrasta con el **techo teórico de la cadencia real** (4 ticks/h × 100 ítems por comunidad). El umbral ≥ 1.000/h se declara **NO CUMPLIDO en operación**; no se reutiliza el 1.450 (era NLP aislado) | H-06: separar banco de pruebas de operación; la cadencia real es de un tick cada 15 min |
| **Precisión / recall / F1** | Se publican con `n = 50`, fecha 2026-09-30, IC exactos (Clopper-Pearson) y las dos desviaciones del muestreo declaradas. **No se presenta recall poblacional**: el IC exacto del estrato `No relevante` es [1,1 %; 29,2 %] (el `[5,2 %; 40,2 %]` de la evidencia archivada era un intervalo Wald sobre la versión previa del clasificador) | H-04, H-12, H-13, C-24/C-10 |
| **Tasa de FP** | Fórmula explícita `FP / (TP + FP)` sobre la muestra de control → 2/29 = **6,9 %**, con `n` | H-04: la fórmula faltaba desde V2 |
| **OE6 (alertas)** | **PARCIAL**: implementado y deshabilitado por defecto; sin evidencia de envío real. Se ajustan Resumen, Abstract y §7.2 | H-02, IN-04 |
| **Casos 5.3** | Se reemplazan por **casos reales del corpus B5** (post, fecha, categoría, score, enlace), sin entidades identificables. Los tres casos de V2/V3 (14/03, 05/05, 22/06 de 2026) **no existen en la ventana** y se retiran | H-17, N-02 |
| **Anomalías** | Se reporta el número real de evaluaciones y disparos desde `anomalias`; se justifica el umbral `max(cuantil 95 de Poisson, 3)` y se declara la limitación de que solo se evalúan las categorías con posts en la ventana móvil (IN-10) | H-03, N-04 |
| **F1 como criterio** | Se incorpora a §1.6 con umbral explícito o se retira del texto; no se deja implícito | N-05 |

### D-6 — Restituir el protocolo 3.3 sin fingir su ejecución

El tribunal valoró el diseño metodológico de §3.3 de V2 (muestra estratificada, etiquetado independiente, Kappa, regla de desempate por mayoría). La realidad es: **un solo anotador, `n = 50`, sin Kappa calculable**. El informe:

- describe el **protocolo diseñado** (con la regla de desempate y el Kappa de Fleiss como criterio);
- describe la **ejecución real** (un anotador, `n = 50`, estratificación condicionada por la predicción y sorteo declarado);
- declara la **brecha** y su consecuencia (Kappa no calculable; recall no publicable);
- deja el evaluador externo como trabajo futuro (C-15), no como resultado.

No se escribe «tres evaluadores» ni «Kappa 0,78»: sería repetir el patrón que el tribunal penalizó.

### D-7 — Describir el sistema que existe, no el de V2/V3

Puntos donde el texto se aparta de la base V2 porque la realidad es otra:

- **Fuente**: RSS/Atom público (`new/.rss`) con rate limiting caracterizado (`CARACTERIZACION_RATE_LIMIT.md`), no API con OAuth2 ni `restrict_sr`. Se explica el motivo (bloqueo del endpoint `.json`, Responsible Builder Policy) y el efecto sobre el alcance.
- **OE1**: se reformula a «recolectar automáticamente desde la fuente pública de Reddit», no «API oficial».
- **Clasificador**: 9 categorías / 201 términos, match por token exacto **sin lematización**, score saturante `min(1, hits/4)`, `MIN_HITS = 1`; `entities` por subcadena con falso positivo conocido (IN-06) declarado.
- **Workflow**: 16 nodos en el artefacto verificable; el generador ya incorpora el fix del 429 (17 nodos), pendiente de regenerar/publicar (IN-08, C-06). Se describe el mecanismo real: centinela `_skip`, espera fija de 60 s, rotación determinista por ranura.
- **DDL**: tabla de atributos espejo **exacto** de `A_DDL.sql` (5 tablas, `RESTRICT`, índices). `pg_trgm` se elimina del texto o se justifica; no se afirma 3FN sin la salvedad de `nlp_category`.
- **Motor de anomalías**: ventana móvil de 11 días, umbral Poisson, corrida 12:05, Telegram deshabilitado.

### D-8 — Forma

APA 7 con correspondencia biunívoca citas↔referencias y URL/fecha de recuperación en fuentes institucionales; **coma decimal** en todo el documento; tablas y figuras numeradas con título y referencia en el cuerpo; índice de tablas y figuras; cuatro figuras (F1 arquitectura — ya existe; F2 DER; F3 captura n8n; F4 serie temporal por categoría); anexos A (DDL), B (workflow exportado importable), C (diccionario de 9 categorías y 201 términos), D (repositorio). Declaración de autoría con uso de herramientas de asistencia, precisa.

### D-9 — Trazabilidad por cifra

Cada tabla del Cap. 5 y cada cifra del Resumen lleva, en el texto o en una nota, su fuente (`V4/evidencias/...` o consulta archivada). La verificación final recorre el documento y falla si encuentra una cifra sin fuente.

## Plan capítulo por capítulo

> Las referencias `l.xxxx` son al cuerpo real de `V4/devoluciones/tesis_v2.txt`.

### Resumen + Abstract (2 pp) — l. 2615–2660

- **Restituir**: estructura y tono de V2 (problema, solución, corpus, resultados, marco legal).
- **Cambiar**: métricas reales (724 posts, 15 días, 9 categorías, n = 50, latencia medida, throughput operativo); eliminar «superó todos los umbrales» y toda cifra heredada; declarar OE6 parcial y cobertura retirada.
- **Espejo exacto** entre Resumen y Abstract (M-01).
- **No entra**: comentarios (la tabla está vacía), ventana de seis meses, 8.240/42.150.

### Cap. 1 — Introducción (5 pp) — l. 2661–2812

- **Restituir**: 1.1 contextualización, 1.2 planteamiento, 1.3 justificación, 1.4 delimitación, 1.5 objetivos (OE1–OE8), 1.6 supuesto y criterios, 1.7 PI-1–PI-4.
- **Corregir**: delimitación temporal con la ventana real (nominal 25/09/2026, operativa 01/10/2026, corte 17/10/2026); OE1 reformulado a fuente pública; OE6 «diseñar» y no «cumplir»; criterios de éxito sin cobertura, con F1 explícito y sin redundancia precisión⇔FP (N-05); supuesto medible (M-10).
- **Evidencia**: `VENTANA_B5.md` §1–§3; `knowledge-base/01_vision_y_objetivos.md`.
- **No entra**: promesas de API oficial, «sistema en tiempo real» sin matiz.

### Cap. 2 — Marco teórico y estado del arte (4,5 pp) — l. 2813–2896

- **Restituir**: 2.1.1 OSINT (ciclo de 5 fases, Russell y Klassen; Pastor-Galindo), 2.1.2 Reddit como fuente, 2.1.3 NLP, 2.1.4 ETL/n8n, 2.2 estado del arte (SpiderFoot, Maltego CE, theHarvester, Recon-ng; Liao et al. correctamente usado; Zong).
- **Corregir**: 2.1.2 describe la **fuente pública** y sus restricciones reales, no OAuth2/100 rpm como si fuera el mecanismo del sistema; H-08 fuentes con URL y fecha; H-09 conservar los ejemplos de modismos («caer», «pescar», «cangrejo») **sin** el «>30 %» contrafáctico; H-10 completar las 8 referencias huérfanas y **contrastar explícitamente con Rivas y Dengra (2026)** — el texto del antecedente está disponible en `V4/devoluciones/Tesis_Rivas_Dengra.md`; m-14 APA 7 sin «et al.» en la lista de referencias.
- **No entra**: CABASE/Fortinet como cifras duras sin URL verificable; si no se verifica la fuente, se reformula cualitativamente.

### Cap. 3 — Marco metodológico (5,5 pp) — l. 2897–2979

- **Restituir**: 3.1 DSR y sus 6 fases mapeadas; 3.2 protocolo de recolección; **3.3 completo** (diseño muestral, estratificación, etiquetado, Kappa, regla de desempate) — el aporte que V3 borró; 3.4 aspectos legales.
- **Corregir**: 3.3 separa **diseño** de **ejecución real** (D-6); H-04 fórmula de FP; H-13 sesgo endógeno declarado; 3.4 terminología exacta **«HMAC-SHA-256 con clave secreta por despliegue»**, gestión de clave (generación, custodia, rotación) y riesgo residual (el seudonimizado sigue siendo dato personal, Ley 25.326); política de enmascaramiento de atributos indirectos.
- **Evidencia**: `evaluacion_muestra_control_2026-09-30.md`, `GUIA_ETIQUETADO_MUESTRA.md`, `ROTACION_HMAC_2026-09-26.md`, `muestra_control_50_*`.
- **No entra**: «tres evaluadores», «Kappa 0,78», «salt dinámico».

### Cap. 4 — Desarrollo del sistema (8,5 pp) — l. 2980–3070 + §4.5 nueva

- **Restituir**: 4.1 arquitectura completa + Figura 1 (V3 la redujo a una oración); 4.2 **tabla de atributos espejo del DDL**; 4.3 orquestación con la sentencia de persistencia que garantiza idempotencia; 4.4 NLP con fórmula del score y extracción de entidades.
- **Agregar**: **4.5 Motor de detección de anomalías** (variable, ventana, base, umbral, regla de disparo, justificación Poisson), que V2 no tenía y el tribunal exigió (H-03).
- **Corregir**: H-16 tabla vs. DDL y `pg_trgm`; H-15 nodos reales del workflow y Anexo B importable; N-06 extracción de entidades con 3–5 ejemplos reales; m-18 sentencia `ON CONFLICT`; IN-10 (categorías evaluadas 7–8 de 9) declarado; `comments` como tabla no poblada (DD-02).
- **Evidencia**: `A_DDL.sql`, `B_workflow.json`, `generar_workflow.py` (DICT), `VERIFICACION_MOTOR_ANOMALIAS.md`, `CARACTERIZACION_RATE_LIMIT.md`.
- **No entra**: descripción de API/OAuth, `restrict_sr`, 5 categorías, workflow de 14 nodos.

### Cap. 5 — Resultados (6,5 pp) — l. 3071–3169

- **Restituir**: estructura de 5.1 (corpus, distribución temporal y por comunidad, clasificación temática), 5.2 rendimiento, 5.3 casos.
- **Corregir**: N-02 Tabla 3 desde SQL con **residual contado** (`No relevante (salida del clasificador)`) y explicación de por qué difiere de V2/V3; N-01 latencia con percentiles y criterio evaluado; H-12 `n`, DS y P; H-06 throughput operativo vs. banco de pruebas; H-07 cada tabla con su archivo fuente.
- **Casos**: seleccionar 2–3 casos **reales del corpus B5** por categoría y score, con fecha, ID y enlace, sin entidades identificables; los casos de V2/V3 se retiran (D-5).
- **Evidencia**: consultas archivadas (corpus, Tabla 3, latencia, anomalías) + `evaluacion_muestra_control_2026-09-30.*` + bitácora.
- **No entra**: 8.240, Tabla 1 mensual, Tabla 2 con r/argentina, 84 %, 82 %, 0,815, 4,2 min, 1.450, 42 posts/3,8 min/94 %.

### Cap. 6 — Discusión (3 pp) — l. 3170–3212

- **Restituir**: 6.1 contraste con literatura, 6.2 representatividad de Reddit, 6.3 limitaciones.
- **Corregir**: N-02 no estimar amenazas reales desde salidas crudas del clasificador — hacerlo corregido por precisión o en términos cualitativos; H-08 precisar qué dato de Fortinet se contrasta o retirarlo; 6.2 con fuentes primarias y fecha o reformulación cualitativa; 6.3 incorporar las limitaciones reales: un solo anotador, diccionario sin lematización, `entities` por subcadena, una sola fuente, techo del feed, categorías no evaluadas, Telegram deshabilitado.
- **No entra**: penetración 93/86,7/47,2/44,1 % sin fuente; «>30 %».

### Cap. 7 — Conclusiones (3 pp) — l. 3213–3295

- **Restituir**: 7.1 trazabilidad OE1–OE8, 7.2 PI-1–PI-4, 7.3 aporte.
- **Corregir**: H-02/H-03 estados honestos (OE5 con resultados reales del motor; OE6 parcial); M-01; PI-1 conserva la honestidad epistémica de V2 (benchmark no ejecutado); 7.3 solo afirma lo que existe en `V4/anexos/`.
- **No entra**: «todos los objetivos cumplidos», «anexos disponibles» si C o D no existen (en este change C y D se escriben).

### Cap. 8 — Recomendaciones (2 pp) — l. 3296–3331

- **Restituir**: las 5 recomendaciones de V2 **con su priorización por prioridad y esfuerzo** (N-03).
- **Corregir**: actualizar la que menciona el corpus de 8.240; ninguna recomendación puede implicar que el sistema ya hace lo que no hace.
- **No entra**: recomendaciones nuevas sin relación con los hallazgos.

### Referencias (2,5 pp) — l. 3332–3381

- APA 7, 17+ entradas, todas citadas; Rivas y Dengra (2026) con contraste en 2.2; CABASE y Fortinet con URL y fecha de consulta (o retiradas); n8n en su versión real (2.40.6) y PostgreSQL 18; Liao et al. en el lugar correcto.
- **No entra**: referencias que no se citan (H-10).

### Anexos (4 pp) — l. 3382–3442

- **A**: DDL real (`A_DDL.sql`), sin secretos.
- **B**: workflow exportado **importable** (`B_workflow.json`, 16 nodos) con la salvedad del fix pendiente (17 en el generador); sin clave HMAC ni tokens.
- **C**: diccionario de 9 categorías y 201 términos, generado desde `generar_workflow.py`.
- **D**: repositorio y estructura.
- Índice de tablas y figuras al inicio.

## Tabla de cifras prohibidas

| Cifra heredada | Reemplazo real |
|---|---|
| 8.240 posts / 42.150 comentarios / 50.390 elementos | 724 posts; `comments` = 0 (no poblada) |
| Ventana 01/01–30/06/2026 (181 días) | 01/10–17/10/2026, 15 días completos |
| Tabla 1 mensual (ene–jun) | Serie diaria 01–17/10 (bitácora) |
| Tabla 2: r/argentina 4.860, r/devsarg 1.540, r/derechogenial 1.840 | Conteo real por subreddit (netsec/Malware/devsarg) |
| Tabla 3: 38 / 26 / 16 / 12 / 8 % | Recuento SQL por 9 categorías + residual contado |
| Muestra 500, estratos 295/94/111 | n = 50, estratificación declarada |
| Kappa 0,78 (Cohen o Fleiss) | No calculable con un anotador; se declara |
| Matriz 6×6 | Matriz 10×10 sobre n = 50 (celdas vacías declaradas) o binaria + exactitud 84 % |
| Cobertura 84 % | Retirada (sin protocolo E8) |
| Precisión 82 % / recall 81 % / F1 0,815 | P = R = F1 = 0,931 (n = 50) con IC y limitaciones |
| FP 15 % (V2) / 18 % (V3) | 2/29 = 6,9 % con fórmula `FP/(TP+FP)` |
| Latencia 4,2 min (DS 0,5; P95 4,9) | Medición real: n, media, DS, P50, P95 |
| Throughput 1.450 posts/h | 1,8 posts/h medidos en operación (techo teórico ≈ 4 ticks/h × 100 ítems) |
| Casos 14/03, 05/05, 22/06 (42 posts, 3,8 min, 94 %) | Casos reales del corpus B5 |
| «>30 % mal clasificados por un clasificador en inglés» | Retirado; se conservan los ejemplos de modismos |
| Penetración 93 / 86,7 / 47,2 / 44,1 % | Fuente con URL y fecha, o formulación cualitativa |
| «Más de 50.000 elementos procesados» | 724 posts |

## Risks / Trade-offs

| Riesgo | Efecto | Mitigación |
|---|---|---|
| Repetir cifras heredadas | El tribunal vuelve a detectar H-07/N-02 y baja la nota | Tabla de cifras prohibidas + verificación 5.1 |
| Copiar la V2 sin corregir | Se repiten hallazgos ya señalados | Checklist H/M/N/m por capítulo (task 1.2 y 5.2) |
| Condensar de nuevo por miedo a la extensión | Repetir N-03 (pérdida de contenido) | Presupuesto por capítulo con piso, no solo techo |
| Huecos disfrazados de texto | «Corrección por declaración» que el tribunal ya penalizó | D-4: producir, declarar o retirar; sin marcadores huérfanos |
| Casos 5.3 sin respaldo | Inventar escenarios es el peor resultado posible | Solo casos seleccionados del corpus, con ID y enlace |
| Latencia/criterios incómodos | Mover el umbral para «aprobar» | D-5: el criterio se conserva y se declara el resultado |
| Texto que no compila a PDF limpio | Pérdida de tiempo del usuario | Markdown estándar, tablas simples, sin HTML embebido |

## Open Questions

- ¿Los autores aceptan declarar públicamente que el criterio de latencia y el de throughput **no se cumplen** en operación? (D-5). Si no, la alternativa es redefinir los criterios **declarándolo como cambio metodológico**, nunca moverlos en silencio.
- ¿Se usa el antecedente Rivas y Dengra para un contraste explícito en 2.2 o se documenta solo la referencia? El archivo está en el repo; el contraste es la opción que cierra H-10.
- ¿La decisión 6.3 de C-05 (posts previos a la ventana) afecta el conteo de 724? Hoy la base no tiene posts anteriores al 01/10 (IN-09); si cambia, el informe debe rehacerse en ese punto.
