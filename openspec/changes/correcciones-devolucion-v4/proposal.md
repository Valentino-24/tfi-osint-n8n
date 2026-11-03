# Proposal

## Why

La devolución del tribunal sobre la tesis V4 (calificación 6,9/10, APROBADO CON CORRECCIONES OBLIGATORIAS, reentrega V5) identifica dos ítems bloqueantes que impiden habilitar la defensa: **N-07** (sustitución integral del corpus sin trazabilidad entre versiones) y **N-08** (validación del clasificador ajena al corpus y estimación estratificada mal calculada). Además hay numerosos ítems mayores y menores que conviene cerrar antes de entregar al tribunal a través del Excel de correcciones, siguiendo el flujo incremental que la cátedra propone.

## What Changes

- **Trazabilidad entre versiones (N-07)**: Completar y dejar verificable la *Declaración de trazabilidad entre versiones* con fechas, ciclo de vida de los datos (B4, muestra preliminar 25-30/09, `TRUNCATE` 01/10, ventana B5), origen de las cifras de V2/V3, qué se retiró y qué cifras del informe vigente **no** derivan de esas versiones. El tribunal exige firma de los tres autores y conocimiento de la dirección; se prioriza que esté lista aunque las firmas físicas se agreguen después.
- **Validación del clasificador sobre B5 (N-08)**: Verificar y ajustar la validación existente (`docs/evidencias/informe_v5_2026-10-20/`) para que cumpla con lo exigido (muestra reproducible, consenso entre anotadores, acuerdo entre ellos —con registro claro—, estimadores ponderados por estrato, intervalos exactos, desglose por `r/devsarg`, conciliación tabla de transición). Se aprovecha que ya hay muestreo, consenso y análisis guardados.
- **Correcciones mayores (N-09 a N-14)**: Asegurar consistencia en latencia, exposición de identificadores (ya parcialmente corregida), motor de anomalías (ya recalculado), diccionario, alcance "Argentina" y pasar una revisión de inconsistencias internas.
- **Correcciones V3 (H-01, H-02, H-06, H-07, H-15)**: Atender las observaciones pendientes con mayor impacto: seudonimización (decir "reversible por custodio de la clave" evitando "irreversible"), alertas (clarificar alcance diario vs "temprana"), throughput (mantener NO EVALUADO con justificación), reproducibilidad (SQL/anexo con código/nodos clave) y Anexo B.
- **Formales/menores (m-21 a m-30)**: Pasada de consistencia, figuras, herramientas, índice, etc. Siguiendo el Excel del tribunal de forma incremental.

## Capabilities

### New Capabilities
- `trazabilidad-versiones`: Asegurar trazabilidad entre versiones V2/V3/docs/V5 con declaración verificable.
- `validacion-clasificador-b5`: Validación del clasificador sobre corpus B5 con muestreo reproducible, consenso, acuerdo entre anotadores, ponderación por estrato e intervalos.
- `correcciones-devolucion-v4`: Correcciones puntuales al informe V5 para atender la devolución V4.

### Modified Capabilities
<!-- None -->

## Impact
- `docs/devoluciones/tesis_v5.md` (capítulos/4, 5, 7, 8, anexos)
- `docs/evidencias/informe_v5_2026-10-20/` (declaración/validación)
- `docs/devoluciones/build/` (regenerar PDF/verificación tras cambios sustanciales)
- `openspec/changes/correcciones-devolucion-v4/`
