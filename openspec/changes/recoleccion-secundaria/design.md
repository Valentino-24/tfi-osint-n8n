## Context

C-05 cerró la ventana B5 con corte `2026-10-17` (DD-08) y congeló sus métricas: **724 posts**, **15 días completos evaluados**, límite superior fijo `2026-10-18 00:00:00 -03:00` sobre `posts.ingested_at`. El autor quiere que la recolección continúe en paralelo como respaldo ante una posible devolución. La base `tesi_osint` no tiene esquema separado: los posts posteriores al corte entrarían a las mismas tablas que la evidencia de B5, y las evaluaciones del motor a la misma `anomalias`.

## Goals / Non-Goals

**Goals**

- Delimitar en el tiempo el track secundario y documentar sus reglas de registro.
- Garantizar que ninguna consulta ni presentación mezcle datos posteriores al corte con el corpus de B5.
- Dejar trazado qué sucede si se pide extender la ventana.
- Mantener el registro diario continuo, también los días sin recolección.

**Non-Goals**

- No tocar el DDL (`V4/anexos/A_DDL.sql`), el artefacto del workflow (`V4/anexos/B_workflow.json`), `V4/scripts/generar_workflow.py` ni la lógica de nodos.
- No publicar ni activar el workflow: lo hace el operador desde la UI (regla dura del proyecto).
- No extender la ventana ni recalcular el 724, los 15 días ni la serie diaria de B5.
- No corregir IN-06, IN-08 ni IN-10: son cambios propios posteriores a la ventana.
- No producir métricas de resultados del track secundario para el capítulo 5.

## Decisions

### D-1 - La frontera es temporal, no de esquema

El track secundario se distingue de B5 por **un único límite temporal**, no por otra tabla ni otro esquema: corpus B5 = `posts.ingested_at ∈ [2026-09-25 00:00:00 -03:00, 2026-10-18 00:00:00 -03:00)`; todo lo posterior es track secundario. En `anomalias`, el mismo límite con `ventana_fin <= 2026-10-18 00:00:00 -03:00` (inclusivo, §3.2 de `VENTANA_B5.md`).

- **Alternativa**: crear una tabla o esquema `secundaria`. **Descartada**: exige DDL, duplica el upsert y obligaría a mover datos ya ingeridos.
- **Consecuencia**: toda consulta de B5 **debe** acotar por ese límite. Por eso el requisito va en el spec, no solo en el diseño.

### D-2 - La bitácora sigue siendo un solo directorio y un solo script

Las entradas posteriores al corte se siguen generando con `V4/scripts/bitacora_b5.py` en `V4/evidencias/bitacora_b5/`: el script ya las rotula como «día posterior al corte oficial» y ya declara congelados el acumulado y los días evaluados. La entrada del `2026-10-18` existe con ese formato y sirve de plantilla.

- **Alternativa**: script y directorio propios (`bitacora_secundaria/`). **Descartada por ahora**: fragmentaría el registro diario y exigiría una rama nueva en el script; si el volumen de días secundarios crece, se reconsidera con su propio change.
- **Trade-off aceptado**: conviven en `bitacora_b5/` entradas que no son de B5. Se compensa con el rótulo del título y con `VENTANA_B5.md` §18.2.

### D-3 - El workflow se republica solo manualmente

Este change no ejecuta `n8n publish:workflow` ni ninguna flag `--publicar`: la publicación es del operador desde la UI (regla dura). El change documenta que el track está **inactivo** mientras el workflow no esté publicado — como el `2026-10-18`, jornada completa sin ninguna ejecución de trigger— y que esa ausencia se registra como día sin recolección, no como falla.

### D-4 - Extender el corte es una enmienda documentada, no una continuación

Si el profesor o los directores piden más días, la vía es modificar DD-08 y `VENTANA_B5.md` §3 con la nueva fecha, su responsable, su fecha de decisión, su motivo y su efecto sobre las métricas ya publicadas, y **recién entonces** recalcular el acumulado y los días. El track secundario **no** se convierte en evidencia de B5 por el solo hecho de existir.

### D-5 - Sin métricas de resultados del track

Ningún conteo del track secundario se publica como métrica de la ventana o del capítulo 5 (RN-GL-01). Si se cuentan para su propio registro, llevan su consulta, su fecha, su ventana y su número de observaciones.

## Risks / Trade-offs

| Riesgo | Efecto | Mitigación |
|---|---|---|
| Contaminación silenciosa | Una consulta sin acotar por el límite mezcla datos post-corte en 724/15 | Requisito explícito en el spec + verificación con `SELECT` en las tareas |
| Una sola serie temporal | Obliga a recordar el límite en cada consulta | El límite está fijo en `VENTANA_B5.md` §2 y en `VENTANA_CORTE_FECHA` del script |
| Doble vida de la bitácora | Entradas de `bitacora_b5/` que no son de B5 | Rótulo de título en cada entrada + puntero de §18.2 |
| El track queda inactivo | Si nadie republica el workflow, no hay datos de respaldo | Se documenta el estado (activo/inactivo) en cada entrada, como el `2026-10-18` |

## Migration Plan

Sin migración de datos: no hay DDL, no hay reescritura ni reclasificación de posts existentes. Solo documentación y verificaciones de solo lectura.

## Open Questions

- ¿El profesor pide extender la ventana? Si sí → D-4.
- ¿Hasta cuánto tiempo corre el track: hasta la entrega, hasta una fecha fija, o indefinido? Se decide al republicar el workflow.
