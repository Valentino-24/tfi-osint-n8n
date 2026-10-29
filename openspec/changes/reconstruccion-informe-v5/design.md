# Diseño técnico — Reconstrucción del informe V5

Este documento es el **plan de ejecución** de los 16 ítems del plan de correcciones del tribunal, con el diseño concreto, la evidencia que lo respalda y la decisión de alcance de cada uno. La devolución auditó `tesis_v4.pdf` (75 páginas) y ordenó las correcciones por prioridad: ítems 1–5 bloqueantes de habilitación a defensa, 6–13 alta, 14–16 media.

## Contexto de partida

- **Documento base**: `V4/devoluciones/tesis_v4.md` (1.152 líneas, 13 H1, 46 H2, 22 tablas, 4 figuras). Se convierte a PDF con `V4/scripts/convertir_pdf.py` (pandoc → DOCX → Word COM → PDF).
- **Correcciones previas**: R-01…R-05 (commit `b77964c`) responden al prompt de autorevisión, no a esta devolución. Cubren parcialmente H-01 (ítem 4) y N-05 (ítem 12); **ninguna cierra un bloqueante**.
- **Datos reales**: corpus B5 con corte `2026-10-17`. La base `tesi_osint` hoy contiene 765 posts (incluye el track secundario C-25 y datos hasta el 19/10); el subconjunto del corte tiene 724 posts y 170 detecciones declaradas. Toda cifra nueva se recalcula con su consulta, fecha y `n`.
- **Verificaciones ya hechas contra el repo/base** (confirman al tribunal): erratas del diccionario (`caeron`, `sequestro`) presentes en `generar_workflow.py`; `1x4xuvc` con `nlp_score = 0.25` (el guion no matchea); IDs de r/devsarg (1x5acdz, 1x2vur9, 1wr7qwo) reales en la base; `B_workflow.json` con `active = False` (contradice la Figura 1); devsarg = 59,1 % del corpus con 7 detecciones (4,1 %); «irreversible» ×5; «alertas tempranas» ×2.

## Principios de ejecución

1. **Bloqueantes primero, en orden.** Los ítems 1–5 son condición de defensa; se cierran antes de tocar los de alta. El ítem 1 (declaración) es requisito previo indispensable.
2. **Sin cifras sin consulta.** Cada número nuevo lleva su `SELECT`, su fecha y su `n` archivados en `V4/evidencias/informe_v5_2026-10-20/`.
3. **Plan B explícito por ítem.** Cuando una exigencia depende de un recurso que el equipo puede no tener (2º anotador, fuente local), se define la alternativa declarativa (NO EVALUADO) y se documenta.
4. **Cambios conmutablemente reversibles.** El diccionario (N-12) toca código; cualquier cambio se valida con una corrida controlada y no altera la base de producción.
5. **Una sola pasada de consistencia al final.** N-14 se corrige en una tabla de 14 filas rastreada, y la verificación final recorre Resumen/Abstract/cuerpo/figuras/anexos.

---

## Bloqueante 1 — Declaración de trazabilidad entre versiones (N-07)

**Qué exige el tribunal**: un anexo firmado por los tres autores, con conocimiento de la dirección, con tres contenidos: (a) cada cifra cuantitativa de V2/V3 ausente en V4 y su origen; (b) el ciclo de vida de los datos con fechas (B4 24/09 descartado, corpus 25–30/09 con r/DerechoGenial y r/argentina, depuración no declarada, B5 con primer registro 01/10); (c) si alguna cifra de V4 deriva de material de V2/V3.

**Diseño**:
- **Documento nuevo**: `V4/evidencias/informe_v5_2026-10-20/Declaracion_trazabilidad_versiones.md` — borrador redactado por el agente, **firmado por Lorca, Zúñiga y Severino** y visado por los directores (Cortez, Enferrel). El agente no puede firmar; entrega el borrador listo para firma.
- **Tabla (a)**: columnas `Cifra retirada | Versión | Valor publicado | Origen | ¿Cómo se estableció?`. Filas mínimas exigidas: corpus 8.240/181 días; 42.150 comentarios; comunidades V3 (r/argentina, r/devsarg, r/derechogenial); Kappa de Fleiss 0,78 (3 evaluadores); latencia media 4,2 min / P95 4,9 min; throughput 1.450 posts/h del banco de pruebas; precisión 82 %; Tablas 1–5 de la V3; los 3 casos de la Sección 5.3 de la V3. Cada origen se clasifica en: *medición sobre corpus descartado* / *proyección* / *simulación* / *generación con herramienta de asistencia* / *otro (especificar)*.
- **Tabla (b)**: línea de tiempo con fechas — B4 (24/09, descartado) → corpus 25–30/09 (muestra del 30/09, con r/DerechoGenial y r/argentina) → depuración (fecha y criterio) → B5 (01/10 → 17/10, corte 19/10). Columna «destino de lo eliminado».
- **Punto (c)**: declaración booleana por cifra de V4 que reutiliza material anterior (p. ej. casos de 5.6 vs casos V2/V3).
- **Riesgo**: es la pieza más sensible (el tribunal habla de *integridad académica*). El borrador debe ser **exhaustivo y sin eufemismos**; toda omisión debilita la habilitación. El contenido lo valorará el tribunal según el reglamento.

**Entregable**: borrador del anexo + tarea de firma para los autores.

---

## Bloqueante 2 — Nueva validación sobre el corpus B5 (N-08/H-13/H-04)

Este es el ítem de mayor costo técnico y define el diseño metodológico de la V5. Hay **dos vías** y una decisión de equipo que las separa.

### Diagnóstico que el tribunal documentó (y que hay que corregir)

- **(a) Muestra ajena al corpus**: la muestra del 30/09 salió de un corpus anterior a B5 (incluía r/DerechoGenial, 10 de 50 casos). No puede estimar el desempeño sobre B5.
- **(b) Estratos mal ponderados**: el estrato censado fueron los 28 positivos del *clasificador anterior* (TP 24 + FP 4) y el sorteado, 22 de sus negativos (FN 5 + TN 17). Con el clasificador vigente, 3 de los 29 positivos vienen del estrato sorteado. El denominador de la precisión mezcla casos censados (peso 1) con sorteados (peso N₀/22), donde **N₀ no está informado**. La sensibilidad estimada (24+3w)/(24+5w) solo llega a 0,80 si w ≤ 4,8 (corpus ≤ 134 publicaciones); con 300 → ≈0,71; con 500 → ≈0,67. **Sin N₀ el CUMPLIDO no se sostiene.**
- **(c) Un anotador asistido**: 6.3 admite «asistencia de herramientas» sin identificarlas; contradice la Declaración de autoría.
- **(d) Sorteo no reproducible**: semilla declarada (20260930) pero ordenamiento por `md5()` era código muerto; solo se reproducen 8 de 50 filas.
- **(e) Ninguna amenaza en español**: las 29 amenazas humanas son de r/netsec (9) y r/Malware (20). El léxico rioplatense —que sostiene la brecha— no tiene validación cuantitativa.
- **(f) Cuentas inconsistentes**: Tabla 5.9 (TP 24→27, FP 4→2) vs «tres FP de más» (los FP bajan 2); 4.4.1 dice 25 de 29, Tabla 5.9 dice 24.

### Vía A — Validación nueva real (preferida)

**Diseño del muestreo** (a ejecutar con consultas sobre `tesi_osint`):
1. **Estrato censado**: las **170 detecciones** clasificadas como amenaza en B5. Se etiquetan las 170 (censo, sin muestreo). Tamaño justificado por la propia V4.
2. **Estrato muestreado**: muestra aleatoria **reproducible** de las **554 «No relevante»**. Tamaño: la V4 calcula ~127 para ±5 puntos si la omisión ronda 9 %, y ~270 si ronda 23 %. **Decisión**: dimensionar la muestra con la omisión estimada en el censo y declarar la fórmula; usar `ORDER BY md5(id || '20261020')` con semilla fija y **archivar el hash del archivo de muestra** para reproducibilidad.
3. **Estimadores ponderados**: P = TP/(TP+FP) con denominador censado; S y F1 con pesos w = N₀/n₀ (N₀ = tamaño del estrato «No relevante», **ahora sí informado**). IC exactos (Wilson o Clopper-Pearson) sobre los estimadores ponderados.
4. **Resultados por comunidad/idioma**: precisión/FDR para r/devsarg vs r/netsec+r/Malware por separado.

**Diseño de los dos anotadores** (lo que preguntaste — ver la sección «Mecánica de anotación» más abajo).

**Conciliación Tabla 5.9 / 4.4.1**: tabla de transición caso por caso (28 positivos anteriores → qué pasó con cada uno con el clasificador vigente).

### Vía B — Declaración de NO EVALUADO (si no hay segundo anotador)

Si el equipo no consigue un segundo anotador, la V5:
- Reclasifica **sensibilidad y F1 como NO EVALUADOS sobre el corpus B5**.
- Mantiene la **precisión como valor indicativo** (la muestra del 30/09, correctamente rotulada y sin ponderar).
- **Reescribe §7.4** para no concluir que «la evidencia respalda el supuesto en la dimensión de clasificación».
- Publica igualmente la **matriz por categoría** y la conciliación 5.9/4.4.1.

**Decisión tomada**: hay **tres** anotadores disponibles → se adopta la **Vía A** con kappa de Fleiss. La Vía B queda solo como contingencia documentada.

---

## Bloqueante 3 — Evidencia accesible y código/SQL (H-07/H-15/m-29)

**Qué exige**: (a) URL o copia congelada (ZIP) con hash SHA-256 declarado en el documento; (b) Anexo B con el **código** de HMAC Anonymize, Classify Dictionary, Extract Entities y Anomaly Engine; (c) SQL de Upsert Posts, Query Daily Counts, Registrar Anomalias y Alertas, y de las consultas Q1–Q15; (d) la sentencia `ON CONFLICT … SET` con su lista explícita de columnas (m-29: la Figura 1 dice «13 columnas» pero 4.3 enumera 7 campos).

**Diseño**:
- **Paquete congelado**: `V4/evidencias/informe_v5_2026-10-20/evidencia_v5.zip` con las consultas (Q1–Q15), la muestra y sus hashes, las salidas crudas, el DDL, el `B_workflow.json` del corte y el diccionario. Se calcula y declara el **SHA-256 del ZIP** en el Anexo D.
- **Anexo B ampliado**: transcripción literal del código de los 4 nodos de código (desde `generar_workflow.py`, que es la fuente) y del SQL de los 3 nodos de PostgreSQL. Formato `Source Code` (Consolas 9,5) ya soportado por `convertir_pdf.py`.
- **m-29**: transcribir el `INSERT … ON CONFLICT (id) DO UPDATE SET <lista explícita>` y verificar contra 4.3 que los campos sobrescritos son 7 (no 13). Confirmar que `ingested_at` y `created_utc` **no** se sobrescriben (de lo contrario se alteran latencia y conteos diarios del motor).

**Riesgo**: el ZIP puede ser grande; si supera límites razonables, se declara la URL del repositorio institucional **o** se publica solo el subconjunto de código+consultas+hashes.

---

## Bloqueante 4 — Desexposición de identificadores (N-10/H-01)

**Qué exige**: reemplazar IDs y títulos literales de r/devsarg por códigos internos; citar la fuente original para r/netsec y r/Malware; ampliar el riesgo residual; decidir sobre las menciones `/u/`; eliminar «irreversible»; declarar el destino de la clave rotada.

**Diseño**:
- **Códigos internos**: en §5.4 y Tabla 5.11, reemplazar `1x5acdz`→`C-01`, `1x2vur9`→`C-02`, `1wr7qwo`→`C-03`, etc., con descripción genérica («publicación de un usuario que relata un ofrecimiento de reclutamiento con pedido de credenciales»). Tabla de correspondencia `C-0x ↔ id` en archivo **fuera** del documento, a disposición del tribunal.
- **r/netsec y r/Malware**: en lugar de citar la publicación de Reddit, citar **CVE o aviso del fabricante** (p. ej. en §5.4, «CVE-2026-XXXX»). Verificar los CVE reales del caso del 12/10 antes de citarlos.
- **Riesgo residual ampliado** (§3.4): vector del **identificador de plataforma** (`posts.id`, `posts.url` permiten recuperar al autor sin la clave) + las **menciones `/u/`** que se conservan en claro tras descartar el prefijo. Decidir: eliminar o seudonimizar las menciones (m-19/N-10).
- **«Irreversible»**: eliminar las 5 ocurrencias (Resumen, Abstract «irreversible pseudonymization», 2.2 y 3.4) y reemplazar por «seudonimización por HMAC-SHA-256 con clave de despliegue (reversible por comparación para el custodio de la clave)».
- **Clave rotada**: declarar si la clave anterior al 26/09 fue destruida (H-01c).

---

## Bloqueante 5 — Las 14 contradicciones de N-14

**Diseño**: tabla de rastreo de 14 filas, cada una con ubicación, corrección y verificación. Ya localizadas y confirmadas contra el repo:

| # | Tema | Ubicación | Corrección concreta | Verificado |
|---|---|---|---|---|
| 1 | FP r/devsarg (6/7, 3/7, 2 correctas) | 5.1, 6.1, 7.3 | Publicar clasificación de las 7 detecciones; unificar | ✓ base: 7 detecciones reales |
| 2 | Estado del workflow (`active=1` vs `false`) | 4.1, Fig. 1, Fig. 3 | Unificar a `active=false` (real: `B_workflow.json`) | ✓ `active = False` |
| 3 | Días de operación (16/15/17) | portada, 2.2, Fig. 1, 6.1, 7.2, 7.3 | Unificar; no llamar «continua» a operación interrumpida | — |
| 4 | Fecha de corte (17/10 vs 18/10 vs 19/10) | portada, 3.2, Cap. 5, Anexo D | Una sola definición | — |
| 5 | Corrección del motor (05/10) | 4.5, Tabla 5.5 | Corregir 4.5 | — |
| 6 | Diferencia 167/170 | 5.4, Tabla 5.2 | Las 3 son del 02/10 (03/10 sin ingesta) | — |
| 7 | FP r/DerechoGenial (3 vs 1) | 1.4, Tabla 5.10 | Indicar versión del clasificador | — |
| 8 | Tabla 5.9 vs 4.4.1 (24 vs 25) | — | Ver N-08(f) | — |
| 9 | Tamaño de muestra (270 vs 127) | 6.4, 8.2 | Recalcular con omisión vigente | — |
| 10 | Throughput (no se verifica vs NO CUMPLIDO) | Resumen, 1.1, 5.12, 7.1 | Ver H-06 | — |
| 11 | Códigos IN-06/IN-08 sin definir | Fig. 1, Tabla 7.2 | Definir o retirar | — |
| 12 | Fecha «10/03» (es 03/10) | 5.1 | Corregir | — |
| 13 | Criterios a priori modificados | 1.6 | Ver N-05 | — |
| 14 | Semilla (declarada vs no reproducible) | 3.3.2, 6.3 | Ver N-08(d) | — |

---

## Ítems de prioridad alta (6–13)

**6. Latencia (N-09)**. Corregir «piso 15–17 min» (es **cota superior** de espera por sondeo, no piso; espera media ≈7,5 min). El scheduler explica ~1 % del P95; el exceso lo explica la operación (corridas incompletas 53,6 %, interrupción 44 h, posible visibilidad de plataforma). Descomponer latencia por comunidad, excluir la interrupción, informar el registro de ejecuciones de n8n (ciclos programados/ejecutados/completos/con 429-403/con contenido) y revisar una muestra de latencias >60 min. Reescribir 5.3, 6.3, 7.3, 8.2. **Requiere datos de n8n**: verificar disponibilidad de ejecuciones en el SQLite de n8n.

**7. Motor de anomalías (N-11)**. Recalcular retrospectivamente **sin tocar la tabla de producción**: conteos por `created_utc`, exclusión de la carga inicial (01/10) y de los días sin operación de la línea base (dividir por días efectivamente operados, no por 10). Informar **falsas alarmas esperadas** = Σ P(X ≥ u | λ) sobre las evaluaciones vs disparos observados. Definir referencia externa (CVE/avisos de la fecha). Reclasificar OE5 como «implementado; eficacia no demostrada». Corregir 4.5 y 3.2.

**8. Diccionario (N-12)**. Corregir erratas (`caeron`→`cayeron`, `sequestro`→`secuestro`); revisar términos genéricos (`filtrado`, `datos personales`, `leak`, `clonar`, `payload`, `loader`, `packed`, `miner`) con el criterio ya aplicado a `dni`; eliminar solapamientos (`zero day` ⊂ `zero day vulnerability`, etc.) o contar solo la coincidencia más larga; **verificar el tratamiento de guiones** (confirmado: `1x4xuvc`=0,25 → `zero-day` no matchea `zero day`; normalizar guion→espacio); publicar la traza de coincidencias de los casos de Tabla 5.11 y del disparo del 12/10. **Toca `generar_workflow.py`** → validar con corrida controlada, no publicar workflow.

**9. Alcance Argentina (N-13)**. Optar: (a) incorporar otra fuente argentina/hispanohablante e informar métricas por idioma, **o** (b) reformular título, objetivo general, PI-2, brecha (2.2) y conclusiones al alcance real (comunidades técnicas de Reddit, léxico bilingüe evaluado principalmente en inglés, componente local exploratorio), declarando el cambio de fuentes como iteración en la Tabla 3.1. Reemplazar «se verificó empíricamente» por «se ilustra con dos casos».

**10. Throughput (H-06)**. O medir capacidad por **reproducción controlada** (reprocesar los 724 textos por los nodos de transformación/clasificación/persistencia, informando n, posts/h, dispersión y equipo), o clasificarlo **NO EVALUADO en todo el documento** y excluirlo de §7.2. Resumen/Tablas 1.1/5.12/7.1 deben coincidir.

**11. Alertas tempranas (H-02)**. Ajustar objetivo general y evaluar el título a «avisos diarios» o justificar «temprana» con la latencia de alerta (el motor corre 12:05 sobre el día anterior → hasta ~36 h). Incluir un **payload de alerta enmascarado**. Aclarar el manejo de la credencial (contradicción Anexo B vs 4.6).

**12. FDR como complemento (N-05)**. Presentar la tasa de falsos descubrimientos como **complemento informativo, no como criterio** (la nota de 1.6 ya admite que es el complemento de la precisión); las Tablas 5.12/7.1 y §7.2 cuentan «cuatro» cuando son tres criterios. Precisar cuándo se fijó cada umbral.

**13. Extracción de entidades (N-06)**. Informar resultados de la extracción (cuántas publicaciones tienen entidades, cuántos CVE, ejemplos, errores) y **publicar la matriz por categoría** (nueve categorías + «No relevante»). Explicar cómo una expresión regular reconoce «nombres de productos o tecnologías».

## Ítems de prioridad media (14–16)

**14. Figuras/epígrafes (m-22/H-11)**: Figura 3 (subtítulo superpuesto, nodos solapados, arista ambigua); Figura 4(a) eje categórico que omite el 03/10 → eje continuo con barra en cero; Figura 4(b) nota superpuesta; un solo título por figura (imagen o epígrafe, no ambos).
**15. DDL (m-21)**: `alertas.estado` DEFAULT **'PENDIENTE'** (hoy 'ENVIADA'); UNIQUE `(categoria, ventana_inicio)` en `anomalias`.
**16. Forma (m-23..m-28, m-30, M-08, m-17)**: DS de subconjuntos en Tabla 5.4; causas de la interrupción (m-24); Ley 25.326 a Referencias y corregir autoría del Decreto 1558/2001 (m-25); Abstract «false discovery rate» (m-26); identificar herramientas generativas (m-27); índice de dos niveles + Resumen/Abstract/Declaración/Siglas (m-28); «Trabajo Final de Inserción» vs «de Carrera» (m-30); suscriptores con fecha (M-08).

---

## Mecánica de anotación — qué hacen los tres (respuesta a tu pregunta)

El tribunal exige **dos anotadores independientes** sobre una submuestra común, con **kappa de Cohen**. Ustedes son tres: eso cubre el requisito e incluso permite un diseño más fuerte. El punto crítico es que la anotación **no puede ver la etiqueta automática** del clasificador (sería circular).

### Reparto de roles

### Reparto de roles (diseño adoptado: kappa de Fleiss, 3 anotadores)

**Los tres autores** etiquetan la **submuestra común de 50 casos**, cada uno a ciegas y por separado:
1. Reciben su archivo (`.xlsx` para etiquetar, `.csv` como respaldo) con columnas: `codigo_interno`, `titulo`, `texto`, `comunidad`, `categoria_asignada` (EN BLANCO), `comentario` (opcional).
2. **No ven** `nlp_category`, `nlp_score`, el `id` de Reddit **ni el estrato de origen**. Excluir el estrato es deliberado: «estrato 1» equivale a «el clasificador dijo amenaza» y sesgaría la etiqueta. El orden de presentación está mezclado de forma determinista.
3. Etiquetan cada fila con **una** de las 10 categorías (9 + «No relevante»), usando la **guía de etiquetado** (`guia_etiquetado_v5.md`).
4. **No se comunican entre sí** durante el etiquetado de los 50. La independencia es lo que el kappa mide.
5. Entregan por separado, sin discutir casos.

**Reparto de volumen**:
- **Autor 3**: etiqueta la **hoja completa de 352 casos** (170 del censo + 182 de la muestra). Incluye los 50 comunes, cuyas etiquetas se extraen por `codigo_interno` — no requiere planilla aparte.
- **Compañeros 1 y 2**: etiquetan **solo los 50 comunes** (`muestra_v5_anot1/2.xlsx`).

**Desacuerdos**: se resuelven por **consenso de los tres**, registrado en `adjudicacion_v5.xlsx` (columnas `etiqueta_final` y `motivo`). No hay árbitro único ni decisión por IA. Si no hay consenso, se adopta la opción más conservadora (**No relevante**).

**Rol del agente (yo)**: preparar la hoja de etiquetado (sampleo reproducible + export sin la etiqueta automática), redactar la guía de etiquetado, calcular kappa e IC, construir los estimadores ponderados y redactar las secciones del informe. **El agente no puede ser anotador** (no puede ver el texto y decidir categoría con independencia humana; y violaría la exigencia de anotadores humanos independientes).

### Guía de etiquetado (borrador a escribir)

Debe fijar, antes de etiquetar:
- **Definición operativa de «amenaza de ciberseguridad»** para el trabajo (lo que haría que un post cuente como positivo de la categoría).
- **Las 10 categorías** con definición y ejemplos límite (tomadas del Anexo C).
- **Reglas de desempate**: qué hacer con un post que toca dos categorías; qué hacer si es ambiguo → «No relevante» o categoría «discusión administrativa».
- **Casos de la muestra del 30/09** como ejemplos calibrados (excepto los que entren en la nueva submuestra común).
- Sin mirar el clasificador.

### Cálculo (lo hago yo)

- **Kappa de Fleiss** (3 anotadores) sobre los 50 comunes. Objetivo: **κ ≥ 0,61** (acuerdo sustancial, umbral que menciona el tribunal).
- **Etiqueta final**: la del consenso de los tres (`adjudicacion_v5.xlsx`); si persiste el desacuerdo, **No relevante**.
- **Precisión**: TP/(TP+FP) sobre el **censo de las 170** (sin ponderar, denominador censado).
- **Sensibilidad y F1**: con **pesos por estrato** w = N₀/n₀ y **IC exactos** sobre los ponderados.
- **Por comunidad/idioma**: separar r/devsarg de r/netsec+r/Malware.
- **Matriz por categoría**.

### Cronograma de anotación (sugerido)

1. Día 1: guía de etiquetado + sorteo reproducible + export XLSX (agente). ✔ hecho
2. Día 1–2: los tres etiquetan la submuestra común de 50, a ciegas y por separado. El autor 3 continúa con los 352.
3. Día 2: cálculo del **kappa de Fleiss** y generación de `adjudicacion_v5.xlsx` con los desacuerdos. **Si κ < 0,61**, se revisa la guía y se re-etiqueta (documentando la iteración).
4. Día 2–3: **consenso de los tres** sobre los desacuerdos, completando `etiqueta_final` y `motivo`.
5. Día 3–4: cálculo de estimadores, redacción de §3.3, §5.5 y §7.4.

**Esfuerzo**: 50 casos ≈ 1–2 h por compañero; 352 casos ≈ 4–6 h para el autor 3.

---

## Orden de ejecución del change

1. **Decisiones de equipo**: N-08 → **Vía A adoptada** (3 anotadores, Fleiss); N-13 y H-06 → **pendientes** (definen §3.3, §5 y §7).
2. **Bloqueante 1**: borrador de la Declaración de trazabilidad → firma de los autores.
3. **Bloqueante 3**: extraer código+SQL, armar el ZIP, calcular hash.
4. **Bloqueante 4**: desexposición de IDs, «irreversible», riesgo residual.
5. **Bloqueante 2**: si vía A, correr la validación nueva (depende de los anotadores); si vía B, reclasificar.
6. **Bloqueante 5**: corregir las 14 contradicciones.
7. **Alta 6–13**.
8. **Media 14–16**.
9. **Regenerar PDF + verificación final** de índices, cifras y consistencia.

## Verificación final (definition of done)

- Cero apariciones de «irreversible»; cero IDs/títulos literales de r/devsarg.
- Anexo B con el código de los 4 nodos y el SQL; ZIP con hash declarado.
- Declaración de trazabilidad presente y firmada.
- κ informado (o NO EVALUADO declarado con §7.4 reescrito); N₀ publicado; estimadores ponderados con IC.
- Las 14 contradicciones corregidas (tabla de rastreo 14/14).
- Índices correctos; PDF sin mojibake; cifras clave con consulta, fecha y n.
- `V4/evidencias/informe_v5_2026-10-20/CHECKLIST_V5.md` con el estado ítem por ítem.

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| No hay 2º anotador | Vía B: sensibilidad/F1 NO EVALUADOS + §7.4 reescrito |
| ZIP demasiado grande | Publicar solo código+consultas+hashes; o URL institucional |
| Diccionario toca producción | Cambios solo en `generar_workflow.py`; corrida controlada; no publicar |
| Cambiar el diccionario altera las 170 | Declarar el efecto: censo con clasificador vigente vs corregido, en dos columnas |
| Firma del anexo demora | Redactar el borrador ya; la firma es de los autores |
| Datos de n8n no disponibles | Declarar la descomposición de latencia como limitada; informar lo que sí existe |
