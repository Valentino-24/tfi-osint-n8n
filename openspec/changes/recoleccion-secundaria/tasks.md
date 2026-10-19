# Tasks - recoleccion-secundaria

> Governance MEDIO. Ninguna tarea modifica el DDL, el artefacto del workflow, la lógica de nodos ni las credenciales.
> Ninguna tarea ejecuta escrituras sobre `tesi_osint`: solo consultas `SELECT` de conteo y agregación.
> Ninguna tarea publica ni activa el workflow en n8n: eso lo hace el operador manualmente desde la UI.

## 1. Frontera del track y verificación numérica

- [x] 1.1 Verificar con `SELECT` de solo lectura que el corpus de B5 con el límite fijo `[2026-09-25 00:00:00 -03:00, 2026-10-18 00:00:00 -03:00)` devuelve **724** posts, y registrar la consulta y su fecha junto con el resultado — **confirmado 2026-10-19 00:17 (-03)**: `COUNT(*) = 724` con esos dos límites; la serie diaria da los mismos 16 días que en el cierre (01/10 = 307 … 17/10 = 8). Consulta en `%TEMP%/opencode/q_track.py` (solo `SELECT`)
- [x] 1.2 Verificar con `SELECT` que el conteo de días completos de `anomalias` con `ventana_fin <= 2026-10-18 00:00:00 -03:00` devuelve **15**, y que las filas posteriores al corte (si las hay) quedan fuera de ese conteo — **confirmado 2026-10-19**: `COUNT(DISTINCT día) = 15` y **0** filas con `ventana_fin > 2026-10-18 00:00:00 -03:00`
- [x] 1.3 Verificar con `SELECT` que los posts con `ingested_at >= 2026-10-18 00:00:00 -03:00` (el track) están contados por separado y que su suma con el acumulado de B5 explica el total de la base, dejando las tres cifras identificadas (previos a la ventana / ventana / track) — **confirmado 2026-10-19**: **previos 0 / ventana 724 / track 0 / total 724** (los previos dan 0 por IN-09: la base no contiene posts anteriores al 2026-10-01)
- [x] 1.4 Confirmar en la base el estado real de la recolección secundaria al momento de cerrar el change (`max(ingested_at)` y `workflow_entity.active`) y declararlo en el registro del change — **confirmado 2026-10-19 00:17 (-03)**: `max(ingested_at) = 2026-10-17 16:16:14 UTC` (13:16:14 local); workflow `KkotjSD5uO4CXI4D` con **`active = 0`**; **395** ejecuciones y `max(createdAt) = 2026-10-19 02:08:25 UTC` = la `#463` del 18/10 23:08:25 local, o sea **ninguna ejecución posterior**. El track está **vacío e inactivo**

## 2. Registro diario del track

- [ ] 2.1 Declarar en este registro que las entradas posteriores al corte se generan con `V4/scripts/bitacora_b5.py` en `V4/evidencias/bitacora_b5/`, con el rótulo de «día posterior al corte oficial» que el script ya aplica (D-2)
- [ ] 2.2 Mientras dure el track: por cada día con recolección, generar la entrada con el comando estándar (`--fecha`, `--n8n-estado`, `--n8n-detalle`) sin `--permitir-reescritura`, de modo que las entradas archivadas de B5 no se reescriban
- [ ] 2.3 Si un día posterior al corte transcurre sin ninguna ejecución de trigger, generar igualmente la entrada como constancia de día sin recolección, con `n = 0` y el estado del workflow como evidencia (mismo criterio que el `2026-10-18`)
- [ ] 2.4 Anotar en `V4/evidencias/VENTANA_B5.md` §18 el estado del track (días cubiertos, workflow activo o inactivo), sin tocar §1–§4 ni el acumulado ya cerrado

## 3. Aislamiento de la evidencia de B5

- [ ] 3.1 Registrar en este change que ninguna métrica del track se presenta como evidencia de B5, y que toda métrica propia lleva consulta, fecha, ventana y número de observaciones (RN-GL-01)
- [ ] 3.2 Revisar que las cifras de la ventana usadas fuera de este change (724 posts, 15 días, serie diaria) siguen referenciando el corte `2026-10-17` y no un total de tabla que ya incluya el track

## 4. Documentación y coherencia

- [x] 4.1 `V4/evidencias/VENTANA_B5.md` §18.2 deja puntero a este change y declara que el track no es evidencia de B5
- [x] 4.2 `knowledge-base/09_decisiones_y_supuestos.md`: DD-08 declara el track secundario y SU-02 registra el cierre del `2026-10-19`
- [x] 4.3 `knowledge-base/02_descripcion_general.md` §Estado de implementación: B5 figurada como **CERRADA** con su corte y su puntero al track
- [x] 4.4 `knowledge-base/10_preguntas_abiertas.md`: constancia del cierre y de la resolución de las preguntas de fecha, suficiencia y conservar/reiniciar
- [ ] 4.5 Si este change produce artifacts en `V4/evidencias/`, nombrarlos y enlazarlos desde §18.2

## 5. Procedimiento de extensión y cierre

- [x] 5.1 El spec declara que extender el corte es una enmienda documentada de DD-08 y de `VENTANA_B5.md` §3, con su trazabilidad, antes de recalcular
- [ ] 5.2 Si el profesor o los directores piden extender la ventana: registrar la enmienda en DD-08 y en `VENTANA_B5.md` §3, actualizar `VENTANA_CORTE_FECHA` en `V4/scripts/bitacora_b5.py` y solo entonces recalcular acumulado y días
- [ ] 5.3 Verificación final: ninguna tarea tocó DDL, artefacto del workflow, nodos, credenciales ni HMAC; todas las interacciones con `tesi_osint` fueron `SELECT`
- [ ] 5.4 Archivar este change (`/opsx:archive`) cuando el track se cierre o cuando se le fije fecha fin; hasta entonces queda abierto como registro vivo
