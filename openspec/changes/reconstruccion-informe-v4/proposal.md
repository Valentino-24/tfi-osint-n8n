## Why

La devolución V3 del 22/09/2026 bajó el trabajo a **5,5/10** y declaró **NO APROBADO con reentrega obligatoria (V4)**, con 8 ítems bloqueantes en su Sección 9. El tribunal ordena reconstruir el informe **sobre la base textual de la V2** (6,0/10), incorporando las correcciones válidas de ambas instancias, y recuperar lo que la V3 eliminó al condensar el documento de 39 a 24 páginas: protocolo de validación 3.3 con regla de desempate, entorno de benchmarking, tabla de atributos 4.2, ejemplos de modismos, priorización del Cap. 8, citas del marco conceptual y Anexo B completo.

El borrador de V4 existente (fuera del repo, 125 páginas) queda **descartado por los autores** por su extensión: la V2 ronda las 40 páginas y ese es el orden de magnitud del informe. No hay vuelta atrás en los datos: el corpus real es el de la ventana B5 (**724 posts, 15 días**, corte `2026-10-17`) y las métricas que se pueden sostener son las que la evidencia existente respalda.

Este change produce **una sola pieza**: `V4/devoluciones/tesis_v4.md`, el informe completo en Markdown, listo para que el usuario lo convierta a PDF con otra herramienta. El plan capítulo por capítulo que lo dirige vive en `design.md` de este change; el archivo `tesis_v4.md` es el documento en sí, no un plan.

## What Changes

- **Archivo nuevo**: `V4/devoluciones/tesis_v4.md` — informe completo, estructura de capítulos de V2/V3 (Resumen, Abstract, Cap. 1–8, Referencias, Anexos A–D), **42–48 páginas equivalentes** con presupuesto por capítulo, escrito en castellano con coma decimal y APA 7.
- **Plan de reconstrucción capítulo por capítulo**: en `design.md`, con la base textual de V2 a restituir, las correcciones H/M/N/m aplicables por capítulo, la evidencia real que entra y el límite de alcance de cada uno.
- **Solo datos reales**: ninguna cifra heredada de V2/V3 sobrevive sin recalcularse. Se fija una tabla explícita de cifras prohibidas (8.240 / 42.150 / 181 días / Tabla 3 redonda / muestra de 500 / matriz 6×6 / cobertura 84 % / precisión 82 % / F1 0,815 / latencia 4,2 min / throughput 1.450 / los tres casos de enero–junio) y un procedimiento de huecos: **se produce ahora si es una consulta `SELECT` o un archivo que ya existe, o se declara la limitación y se retira la afirmación** — sin marcadores `[COMPLETAR]` sin dueño ni evidencia.
- **Decisiones métricas que el documento adopta** (y declara como tales): se **retira** la métrica de cobertura de §1.6 y de todo el informe (E8 no es ejecutable con la fuente RSS); se publica la latencia medida desde la base con n/media/DS/P50/P95 y se declara el criterio de §1.6 como no cumplido si corresponde, **sin mover el umbral**; throughput **operativo** (4 ticks/h × 100 ítems = 400/h) separado del banco de pruebas; precisión/recall/F1 con `n = 50`, su fecha y sus intervalos; OE6 queda **PARCIAL** (implementado, deshabilitado, sin envío real); los tres casos de 5.3 se reemplazan por **casos reales del corpus B5**, porque los de V2 (marzo, mayo y junio de 2026) no existen en la ventana.
- **Reescritura de lo que la realidad del sistema contradice**: la fuente es **RSS/Atom público** con cuota caracterizada, no la API con OAuth2 que describen V2/V3; OE1 se reformula; el clasificador es de **9 categorías y 201 términos** con score saturante, no de 5; el workflow tiene 16 nodos en el artefacto verificable.
- **Evidencias de solo lectura**: las tablas cuantitativas del Cap. 5 salen de consultas `SELECT` ejecutadas sobre `tesi_osint` durante este change, archivadas con su consulta, su fecha y su `n` en `V4/evidencias/informe_v4_2026-10-19/`. No escriben en la base.

## Capabilities

### New Capabilities

- `informe-tesis-v4`: el informe V4 como documento — estructura y presupuesto de capítulos, política de datos reales y de huecos, decisiones métricas declaradas, trazabilidad de cada cifra a su evidencia.

### Modified Capabilities

Ninguna. `openspec/specs/` está vacío: no existen specs previos cuyos requisitos cambien.

## Impact

- **Artefactos nuevos**: este change (`proposal.md`, `design.md`, `tasks.md`) y `V4/devoluciones/tesis_v4.md`.
- **Lecturas de solo lectura**: consultas `SELECT` sobre `tesi_osint` y archivos existentes en `V4/evidencias/`, `V4/anexos/` y `V4/devoluciones/`.
- **Sin impacto en el sistema**: no se modifica `A_DDL.sql`, `B_workflow.json`, `generar_workflow.py`, nodos ni credenciales; no se publica ni activa ningún workflow (regla dura); no se escribe en la base.
- **Relación con el roadmap**: adelanta el contenido de **C-16, C-18, C-19, C-20 y C-21** en un solo entregable (un solo archivo, no uno por capítulo). **No cierra** C-08 a C-11: sus evidencias consolidadas (E4, E5, E6, E7, E8) siguen siendo suyas; lo que este change produce son lecturas de redacción con su trazabilidad. No se registra en `CHANGES.md` hasta que los autores confirmen cómo convivir con esa secuencia.
- **Dependencias abiertas**: la decisión 6.3 de C-05 (posts previos) y la habilitación de Telegram (IN-04) no bloquean la redacción; se declaran como límites.
- **Riesgo que cierra**: un informe reescrito con cifras heredadas repetiría el hallazgo crítico H-07/N-02 — «la distancia entre lo que se declara logrado y lo que el documento demuestra» — que es exactamente lo que bajó la nota de V2 a V3.
