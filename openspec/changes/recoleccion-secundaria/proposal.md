## Why

La ventana B5 se cerró el **2026-10-19** con corte `2026-10-17` (DD-08, tarea 6.1 de C-05): **724 posts**, **15 días completos evaluados**, límite superior fijo `2026-10-18 00:00:00 -03:00`. El autor decidió que la recolección **siga en paralelo** como respaldo ante una posible devolución del profesor sobre los datos o sobre la ventana.

Esa recolección posterior al corte es útil **solo si su límite está explícito**. Los posts que ingiera caen en la misma tabla `posts` y las evaluaciones del motor en la misma `anomalias`: una consulta que no acote por el límite fijo del corpus B5 los mezclaría silenciosamente con la evidencia de la ventana y volvería irreproducibles el **724** y los **15** días. El `2026-10-18` ya quedó registrado como día sin recolección (`VENTANA_B5.md` §18) y falta un lugar propio para el track que continúa después del corte.

C-05 no cubre esto: cierra la ventana. Este change delimita lo que sucede **después** de cerrarla.

## What Changes

- Delimitar el **track secundario**: la recolección posterior al corte `2026-10-17`, con sus propias reglas de registro, que **no** integra el corpus de B5 ni modifica sus métricas.
- Fijar la **frontera única** entre la ventana y el track: `posts.ingested_at ∈ [2026-09-25 00:00:00 -03:00, 2026-10-18 00:00:00 -03:00)` para B5; todo lo posterior es track secundario. Para `anomalias`, el mismo límite con `ventana_fin <= 2026-10-18 00:00:00 -03:00`.
- Declarar que **ninguna métrica del track** se presenta como evidencia de B5 (RN-GL-01): el acumulado de **724**, los **15** días, la serie diaria y las anomalías de la ventana quedan **congelados**.
- Registrar que una eventual **extensión del corte** es una enmienda documentada de DD-08 y de `VENTANA_B5.md` §3 (fecha, responsable, fecha de la decisión, motivo y efecto sobre las métricas ya publicadas), **no** una continuidad implícita del track secundario.
- Mantener la **bitácora diaria como registro único**: las entradas posteriores al corte siguen saliendo del mismo script con el rótulo de «día posterior al corte» que ya tienen, y el estado del track se anota en `VENTANA_B5.md` §18.
- **Sin publicar el workflow desde el agente**: la republicación la hace el operador manualmente desde la UI (regla dura). Este change delimita y documenta; no publica, no activa y no modifica nodos.

## Capabilities

### New Capabilities

- `recoleccion-secundaria`: reglas del track de recolección posterior al corte — frontera temporal única, aislamiento de la evidencia de B5, registro diario propio, métricas propias con su trazabilidad, y el procedimiento si se decide extender el corte.

### Modified Capabilities

Ninguna. `openspec/specs/` está vacío: no existen specs previos cuyos requisitos cambien.

## Impact

- **Artefactos nuevos**: este change (`proposal.md`, `design.md`, `tasks.md`, `specs/recoleccion-secundaria/spec.md`).
- **Documentación coherente ya actualizada**: `V4/evidencias/VENTANA_B5.md` §18.2 (puntero al track), `knowledge-base/09_decisiones_y_supuestos.md` DD-08 y SU-02, `knowledge-base/02_descripcion_general.md` §Estado de implementación, `knowledge-base/10_preguntas_abiertas.md` (constancia del cierre).
- **Sin impacto en**: `V4/anexos/A_DDL.sql`, `V4/anexos/B_workflow.json`, `V4/scripts/generar_workflow.py`, la lógica de nodos y las credenciales. Ninguna tabla, columna, índice ni sentencia cambia.
- **Sin impacto sobre las métricas de B5**: 724 posts, 15 días y la serie diaria no cambian, ni por este change ni por la recolección posterior.
- **Sin escrituras destructivas**: las tareas solo ejecutan consultas `SELECT` de conteo y agregación sobre `tesi_osint`.
- **Dependencias**: requiere C-05 **cerrado** (ya lo está: corte fijado el 2026-10-19). No bloquea C-08 → C-09 → C-20 → C-21 → C-23, que se apoyan en la ventana ya cerrada.
- **Riesgo que cierra**: mientras la recolección secundaria corra sin límite documentado, cualquier consulta mal acotada puede contaminar el corpus de B5 con posts posteriores al corte. Ese es exactamente el riesgo que este change deja declarado y verificable.
