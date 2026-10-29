## Why

La devolución V4 del tribunal (UTN FRM, 20/10/2026) calificó el trabajo en **6,9/10 — APROBADO CON CORRECCIONES OBLIGATORIAS. REENTREGA V5**, y condicionó la **habilitación a defensa** al cierre de los **5 ítems bloqueantes** de su Sección 9. La V5 no es una mejora incremental: es la versión que habilita (o no) la defensa del trabajo. La declaración del ítem 1 es *requisito previo indispensable*.

La V4 ya cerró siete de los ocho bloqueantes de la V3 (reconstruyó el texto sobre la V2, midió la latencia desde la base, retiró la cobertura, publicó fórmulas/matriz/IC, reformuló el motor de anomalías, completó el DDL, incorporó figuras reales). Lo que falta es de otra naturaleza: **integridad académica declarada** (N-07), **una validación que mida el desempeño sobre el corpus evaluado** (N-08), **acceso verificable a la evidencia y al código** (H-07/H-15), **desexposición de identificadores** (N-10/H-01) y **consistencia interna** (N-14). A eso se suman 8 correcciones de prioridad alta y 3 de prioridad media.

Las correcciones R-01…R-05 aplicadas antes (commit `b77964c`) fueron respuestas al *prompt de autorevisión* de Claude, no a esta devolución. Al contrastarlas contra la Sección 9 se verificó que **ninguna cierra un ítem bloqueante completo**: cubren parcialmente el ítem 4 (H-01) y el ítem 12 (N-05). El resto sigue abierto.

## What Changes

- **Declaración de trazabilidad entre versiones** (N-07, bloqueante 1): anexo firmado por los tres autores y conocido por la dirección, que enumera cada cifra cuantitativa de V2/V3 ausente en V4 y declara su origen (medición sobre corpus descartado, proyección, simulación, generación con asistencia u otro), documenta con fechas el ciclo de vida de los datos (B4 → corpus 25–30/09 → depuración → B5) y el destino de lo eliminado, y declara si alguna cifra de V4 deriva de material de V2/V3.
- **Nueva validación sobre el corpus B5** (N-08/H-13/H-04, bloqueante 2): censo de las 170 detecciones y muestra aleatoria reproducible de las 554 «No relevante»; guía de etiquetado escrita; **dos anotadores independientes** sobre una submuestra común con **kappa de Cohen**; estimadores **ponderados por estrato con IC**; resultados **por idioma/comunidad**; conciliación caso por caso de la Tabla 5.9 vs 4.4.1. **Plan B si no hay segundo anotador**: reclasificar sensibilidad y F1 como **NO EVALUADOS** sobre el corpus, mantener la precisión como valor indicativo y reescribir §7.4.
- **Anexo de evidencia accesible** (H-07/H-15/m-29, bloqueante 3): URL o copia congelada (ZIP) con **hash SHA-256** declarado; Anexo B con el **código de los cuatro nodos de código** (HMAC Anonymize, Classify Dictionary, Extract Entities, Anomaly Engine) y el **SQL** de Upsert Posts / Query Daily Counts / Registrar Anomalias y Alertas y de las consultas Q1–Q15; sentencia `ON CONFLICT … SET` con su lista explícita.
- **Desexposición de identificadores** (N-10/H-01, bloqueante 4): reemplazar en el informe los IDs y títulos literales de r/devsarg (1x5acdz, 1x2vur9, 1wr7qwo, etc.) por códigos internos (C-01…) con tabla de correspondencia **fuera** del documento; citar la fuente original (CVE, aviso del fabricante) para las divulgaciones de r/netsec y r/Malware; ampliar el riesgo residual al vector del identificador de plataforma y a las menciones `/u/`; **eliminar toda aparición de «irreversible»**; declarar el destino de la clave HMAC rotada.
- **Corrección de las 14 contradicciones internas** (N-14, bloqueante 5) y pasada final de consistencia Resumen↔Abstract↔cuerpo↔figuras↔anexos.
- **8 correcciones de prioridad alta**: latencia (N-09), motor de anomalías (N-11), diccionario (N-12), alcance Argentina (N-13), throughput (H-06), alertas tempranas (H-02), FDR como complemento (N-05), extracción de entidades (N-06).
- **3 correcciones de prioridad media**: figuras/epígrafes (m-22), DDL (m-21), forma restante (m-23..m-28, m-30, M-08, m-17).
- **Regeneración del PDF** de entrega con verificación de índices, cifras y ausencia de mojibake.

## Capabilities

### New Capabilities

- `informe-tesis-v5`: el informe V5 como documento — corrección de los 16 ítems del plan del tribunal, política de evidencia accesible, exposición de identificadores, consistencia interna verificable y trazabilidad entre versiones.

### Modified Capabilities

Ninguna. `openspec/specs/` está vacío: no existen specs previos cuyos requisitos cambien.

## Impact

- **Artefactos nuevos/modificados**: este change (`proposal.md`, `design.md`, `tasks.md`) y `V4/devoluciones/tesis_v4.md` → `tesis_v5.md` (o el mismo archivo renombrado), más su PDF y evidencias asociadas.
- **Nuevo anexo no derivable de consultas**: la Declaración de trazabilidad entre versiones (documento firmado; el agente redacta el borrador, la firma la aportan los autores).
- **Lecturas de solo lectura**: consultas `SELECT` sobre `tesi_osint` para el censo de las 170 detecciones, la muestra nueva y la recomputación del motor. No se escribe en la base.
- **Sin impacto en el sistema**: no se modifica `A_DDL.sql`, `B_workflow.json`, `generar_workflow.py`, nodos ni credenciales; **no se publica ni activa ningún workflow** (regla dura). El diccionario (N-12) puede requerir cambios en `generar_workflow.py` para corregir erratas y guiones, pero eso se decide en `design.md` y no toca datos de producción.
- **Relación con el roadmap**: absorbe y continúa C-26; el rediseño de diccionario (`rediseno-diccionario-evaluacion`) es el insumo directo de N-12; el track secundario (`recoleccion-secundaria`, C-25) alimenta la ampliación de corpus si se opta por la vía (a) de N-13.
- **Dependencias abiertas**: disponibilidad de un **segundo anotador** (decide la vía de N-08); decisión sobre incorporar una fuente local adicional (vía (a) vs (b) de N-13); habilitación de Telegram (IN-04) sigue deshabilitada → OE6 permanece PARCIAL.
- **Riesgo que cierra**: entregar una V5 que no cierre los 5 bloqueantes deja el trabajo sin habilitación a defensa. El cambio de corpus de la V4 es legítimo; lo que el tribunal exige es **declararlo** (N-07) y **medir sobre él** (N-08).
