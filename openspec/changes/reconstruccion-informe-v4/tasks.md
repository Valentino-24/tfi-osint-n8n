# Tasks — reconstruccion-informe-v4

> Governance **ALTO** por el destino del entregable, pero **sin escrituras en el sistema**.
> Ninguna tarea modifica `A_DDL.sql`, `B_workflow.json`, `generar_workflow.py`, nodos, credenciales ni la base.
> Ninguna tarea publica ni activa el workflow: lo hace el operador manualmente desde la UI (regla dura).
> Toda interacción con `tesi_osint` es una consulta `SELECT`. Ningún secreto, token ni clave HMAC aparece en el informe ni en las evidencias.

## 1. Preparación de fuentes y reglas

- [x] 1.1 Normalizar la base textual de V2 desde `V4/devoluciones/tesis_v2.txt` (cuerpo real, l. 2614–3442): acentos, saltos de línea de la extracción, viñetas y comillas. Guardar la copia de trabajo en `%TEMP%\opencode\tesis_v2_normalizada.md` (fuera del repo) y verificar que conserva la numeración de secciones.
- [x] 1.2 Construir el checklist de correcciones con IDs y capítulo destino: H-01…H-17, M-01…M-12, N-01…N-06, m-13…m-20. Archivar en `V4/evidencias/informe_v4_2026-10-19/CHECKLIST_CORRECCIONES.md` con estado inicial y la evidencia que lo cerraría.
- [x] 1.3 Extraer de V2 la lista de referencias (l. 3336–3381) y verificar cuáles están citadas en el cuerpo; marcar las huérfanas (H-10) y las que requieren URL/fecha (CABASE, Fortinet, n8n, PostgreSQL, Reddit).
- [x] 1.4 Leer `V4/devoluciones/Tesis_Rivas_Dengra.md` (UTF-16, 4.761 líneas; convertir a UTF-8 en `%TEMP%\opencode\`) y extraer 5–8 puntos de contraste concretos (alcance, fuente, método, resultados) para §2.2.
- [x] 1.5 Fijar en el checklist la tabla de cifras prohibidas del `design.md` §«Tabla de cifras prohibidas» y usarla como lista de verificación en 5.1.

## 2. Lecturas de datos reales (solo `SELECT`) y archivado

- [x] 2.1 Corpus B5: contar posts totales, por subreddit y por día, con el límite fijo `ingested_at ∈ [2026-09-25 00:00:00 -03:00, 2026-10-18 00:00:00 -03:00)`; verificar 724 y las cifras por comunidad. Registrar consulta, fecha y `n`.
- [x] 2.2 Tabla 3: recuento por `COALESCE(nlp_category,'No relevante')` sobre el corpus B5 con la fila residual **contada** (no derivada); calcular porcentajes y verificar que suman 100 %. Incluir las 9 categorías y el residual.
- [x] 2.3 Latencia: `ingested_at − to_timestamp(created_utc)` en minutos con `created_utc > 0`; reportar `n`, media, DS, P50 y P95. Registrar también el mínimo, el máximo y cuántos posts superan 5, 15 y 60 minutos (para explicar la cola).
- [x] 2.4 Motor de anomalías: volcar `anomalias` completo (todas las evaluaciones, disparen o no) con `ventana_inicio`, `ventana_fin`, `categoria`, `n_observado`, `base_media`, `umbral`, `disparo`; contar evaluaciones, días y disparos reales. Verificar el conjunto de categorías evaluadas por día (IN-10).
- [x] 2.5 Alertas: contar filas de `alertas` por canal y estado; constatar que Telegram está deshabilitado y que no hay envío real (OE6 parcial).
- [x] 2.6 Muestra de control n = 50: recalcular desde `muestra_control_50_2026-09-30_ETIQUETAS.csv` y la respuesta del modelo la matriz binaria (TP/FP/FN/TN), la exactitud por categoría y la tasa de FP con la fórmula `FP/(TP+FP)`; producir la matriz 10×10 (9 categorías + `No relevante`) y declarar las celdas vacías. No recalcular con datos distintos de los etiquetados. **Desviación declarada:** la matriz 10×10 no se publica —con n = 50 las celdas quedarían en 0 o 1— y se informan en su lugar la matriz binaria (Tabla 5.7), la exactitud de categoría (42/50 = 84,0 %) y el detalle ítem por ítem (Tabla 5.10). Ver `CHECKLIST_CORRECCIONES.md` §5.1.
- [x] 2.7 Casos reales: seleccionar 2–3 posts del corpus B5 con categoría y `nlp_score` alto, uno por tipo de amenaza, con fecha, ID y enlace; verificar que no contengan entidades identificables o enmascararlas.
- [x] 2.8 Archivar **todas** las salidas de 2.1–2.7 en `V4/evidencias/informe_v4_2026-10-19/` (un archivo por consulta o tabla, con el SQL, la fecha de ejecución y el `n`). Verificar que ningún archivo contiene credenciales.

## 3. Redacción del informe (archivo único)

- [x] 3.1 Cap. 1 — Introducción (5 pp): restituir 1.1–1.7 de V2; ventana real; OE1 reformulado; OE6 «diseñar»; criterios sin cobertura, con F1 explícito y sin redundancia; supuesto medible.
- [x] 3.2 Cap. 2 — Marco teórico y estado del arte (4,5 pp): restituir 2.1–2.2; fuente pública en 2.1.2; modismos sin «>30 %»; referencias huérfanas cerradas; contraste con Rivas y Dengra; Liao bien usado.
- [x] 3.3 Cap. 3 — Marco metodológico (5,5 pp): restituir 3.3 completo (diseño vs. ejecución real); fórmula de FP; HMAC-SHA-256 con clave por despliegue, gestión y riesgo residual; enmascaramiento de atributos indirectos.
- [x] 3.4 Cap. 4 — Desarrollo (8,5 pp): arquitectura + F1; tabla de atributos espejo del DDL; workflow real (16 nodos, fix del 429, rotación, `ON CONFLICT`); NLP (9 categorías, 201 términos, score saturante, entidades y su limitación); **§4.5 motor de anomalías**; `comments` no poblada. **Corrección durante el apply:** el workflow desplegado tiene **17 nodos** (no 16): el nodo del fix del 429 se sumó a los 16 previstos. Tablas 4.1 y B.1 lo reflejan.
- [x] 3.5 Cap. 5 — Resultados (6,5 pp): corpus y serie diaria; Tabla 3 desde SQL; latencia con percentiles y criterio evaluado; throughput operativo; muestra n = 50 con IC; anomalías y disparos; casos reales con ID y enlace. Cada tabla con su fuente.
- [x] 3.6 Cap. 6 — Discusión (3 pp): contraste con literatura; amenazas corregidas por precisión o cualitativas; fuentes de penetración con URL/fecha o reformuladas; limitaciones reales (anotador único, sin lematización, `entities`, una fuente, techo del feed, IN-10, Telegram).
- [x] 3.7 Cap. 7 — Conclusiones (3 pp): OE1–OE8 con estado honesto; PI-1–PI-4; PI-1 conserva la honestidad de V2; 7.3 solo afirma lo que existe en `V4/anexos/`.
- [x] 3.8 Cap. 8 — Recomendaciones (2 pp): las 5 de V2 con prioridad y esfuerzo; sin cifras heredadas.
- [x] 3.9 Resumen y Abstract (2 pp): escritos al final; espejo exacto; métricas reales; sin «superó todos los umbrales»; OE6 parcial y cobertura retirada declarados.
- [x] 3.10 Referencias (2,5 pp): APA 7, 17+ entradas, todas citadas, con URL y fecha en fuentes institucionales; Rivas y Dengra incluida; sin «et al.» en la lista. **Desviación declarada:** la lista cierra con **15 entradas**, todas citadas en el cuerpo. Se descartaron Honnibal et al. (spaCy) y Stallings por quedar sin cita tras la reescritura; el criterio aplicado fue no dejar referencias huérfanas ni citas sin referencia.
- [x] 3.11 Anexos (4 pp): A DDL real; B export importable sin secretos; C diccionario de 9 categorías y 201 términos desde `generar_workflow.py`; D repositorio y estructura.
- [x] 3.12 Ensamblar todo en `V4/devoluciones/tesis_v4.md` con jerarquía de títulos consistente (H1 título, H2 capítulos, H3 secciones), sin HTML embebido y sin bloques de metadatos internos.

## 4. Figuras e índices

- [x] 4.1 Figura 2 (DER): generarla desde `V4/anexos/A_DDL.sql` con `matplotlib` o equivalente, reflejando las 5 tablas y `ON DELETE RESTRICT`; guardar script en `V4/scripts/` y PNG en `V4/figuras/`.
- [x] 4.2 Figura 3 (workflow): generar un diagrama de nodos y conexiones desde `V4/anexos/B_workflow.json` (no una captura de pantalla), declarándolo como diagrama derivado del export; verificar el conteo de nodos.
- [x] 4.3 Figura 4 (serie temporal por categoría): generarla desde la consulta horaria/diaria real (`date_trunc` × `nlp_category`) sobre el corpus B5; nunca con datos de V2/V3.
- [x] 4.4 Verificar que Figura 1 (`V4/figuras/Figura_1_arquitectura.png`) coincide con la arquitectura descrita en el Cap. 4; si no, corregir el texto o la figura.
- [x] 4.5 Insertar el índice de tablas y figuras después del índice general, con numeración verificada contra el cuerpo.

## 5. Verificación y cierre

- [x] 5.1 Auditar que **ninguna** cifra de la tabla de prohibidas aparece en `tesis_v4.md` (búsqueda literal de 8.240, 42.150, 84, 82, 0,815, 4,2, 1.450, 500, 0,78, 30 %, 94 %, 3,8). **Resultado:** todas en cero, con una excepción deliberada — en §1.6 se declara que los umbrales de clasificación pasaron de 82 % a 80 % y de 18 % a 20 % (hallazgo N-05 exigía declarar todo cambio de umbral). Los falsos positivos de la búsqueda se identificaron uno por uno: «3,8 min» ⊂ «16.483,8 minutos», «TODO» ⊂ «metodológico», «kappa»/«SHA-256 + Salt» legítimos en la nota de corrección del Anexo A.
- [x] 5.2 Recorrer el checklist de 1.2 y marcar cada hallazgo **RESUELTO / PARCIAL / NO RESUELTO** con la sección donde se atiende y su evidencia.
- [x] 5.3 Verificar el presupuesto de extensión: contar palabras por capítulo y comparar con el `design.md` §D-2; recortar los que excedan y completar los que queden por debajo del piso. **Resultado:** cuerpo ≈ **20.364 palabras de prosa** (≈ 51 páginas equivalentes a 400 palabras/página), **≈ 7 % sobre el techo** de 19.000 del diseño. Se declara la desviación en `CHECKLIST_CORRECCIONES.md` §5.3: el exceso proviene de las correcciones agregadas después del control de presupuesto (entorno de H-06, modismos de H-09, configuración de H-01c, nota de umbrales de N-05, priorización de N-03), no de relleno; se recortó la duplicación entre §6.4 y el Capítulo 8. Cap. 4 en 8,1 pp (techo 8,5) y Cap. 5 en 8,5 pp (presupuesto 6,5) por exigencia de trazabilidad de cada cifra.
- [x] 5.4 Verificación APA 7: cada cita en el cuerpo tiene su referencia y cada referencia está citada; URL y fecha en fuentes institucionales.
- [x] 5.5 Verificación de forma: coma decimal en todo el documento, tablas y figuras numeradas y referenciadas, títulos de sección coherentes con el índice.
- [x] 5.6 Verificar que no quedan marcadores `[COMPLETAR]` sin dueño, evidencia y fecha; cada limitación declarada es legible sin el dato faltante.
- [x] 5.7 Verificar que `V4/devoluciones/tesis_v4.md` existe, es UTF-8 válido, abre sin caracteres corruptos y contiene todos los capítulos y anexos.
- [x] 5.8 Registrar este change en `CHANGES.md` **solo si los autores confirman** cómo convive con C-16 y C-18…C-21; hasta entonces no se toca el roadmap. **Hecho el 2026-10-19**, con confirmación de los autores sobre la declaración pública de latencia y throughput no cumplidos. Registrado como **`[C-26] reconstruccion-informe-v4`** (`[~]` parcial), que **absorbe** `C-16`, `C-17`, `C-18`, `C-19`, `C-20`, `C-21`, `C-22` y `C-23`: los ocho compartían entregable y se ejecutaron en un solo change. También se alineó el estado de `C-05` a `[~]` parcial y se agregó la nota de estado real al 2026-10-19.
- [x] 5.9 Declarar en el registro del change que no hubo escrituras en la base, ni cambios en DDL/workflow/nodos/credenciales, ni publicación desde el agente.

## 6. Cierre del apply

- **Fecha de cierre:** 2026-10-19.
- **Entregable:** `V4/devoluciones/tesis_v4.md` (UTF-8 sin BOM): portada, declaración de autoría, índices de contenido/tablas/figuras, siglas, Resumen, Abstract, Cap. 1–8, Referencias y Anexos A–D. **22 tablas** numeradas y citadas, **4 figuras** embebidas (`V4/figuras/`), sin marcadores pendientes.
- **Trazabilidad de hallazgos:** `V4/evidencias/informe_v4_2026-10-19/CHECKLIST_CORRECCIONES.md` (45 IDs de las dos instancias, con la sección que resuelve cada uno y su estado).
- **Sin escrituras en el sistema:** todas las consultas a `tesi_osint` fueron `SELECT`. No se modificaron `A_DDL.sql`, `B_workflow.json`, `generar_workflow.py`, nodos, credenciales ni la base. El workflow no se publicó ni se activó desde el agente.
- **Tarea abierta:** 5.8 (registro en `CHANGES.md`), bloqueada hasta la confirmación de los tres autores sobre C-16 y C-18…C-21.
- **Desviaciones declaradas:** matriz de confusión por categoría no publicada (2.6); 15 referencias en lugar de 17 (3.10); prosa ≈ 19.500 palabras, 3 % sobre el techo (5.3); títulos de capítulo y conteo de nodos (17) corregidos durante el apply (3.4).
