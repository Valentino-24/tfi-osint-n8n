## Why

El sistema ya recolectó con el workflow RSS/Plan C (B4 verificada el 2026-09-24), pero la ventana de datos que sostiene todas las métricas del Capítulo 5 no existe todavía. La tesis arrastra la ventana ficticia de seis meses de V2/V3, y el supuesto SU-02 exige fecharla antes de producir cualquier tabla. C-05 es el reloj del proyecto: define qué métricas son calculables y bloquea el tramo crítico `C-08 → C-09 → C-20 → C-21 → C-23`.

Además, dos limitaciones de la corrida B4 quedaron sin caracterizar formalmente: el rate limiting que dejó a `r/derechogenial` con 0 posts, y la histone insuficiente para que la base de diez días del motor de anomalías sea interpretable.

## What Changes

- Fijar por escrito la **fecha de inicio de la ventana real de recolección: 2026-09-25**. Es una decisión ya tomada por los autores.
- Dejar la **fecha de corte explícitamente abierta**: se representa como decisión pendiente, no se inventa ni se propone un plazo por defecto.
- Sustituir en la documentación toda mención a la ventana ficticia de seis meses de V2/V3 por la ventana real, con su duración declarada (SU-02).
- Crear una **bitácora diaria de evidencia** en `V4/evidencias/` con una entrada por día: fecha, posts ingeridos, posts por subreddit, ejecuciones fallidas y su causa.
- **Caracterizar la ventana real de rate limiting de Reddit** observada en las corridas, cerrando el criterio pendiente de US-002.
- **Documentar el efecto de `r/derechogenial` en el corpus** (m-16): el subreddit está habilitado en `active_monitoring` pero no aporta posts, lo que sesga cualquier percentage por subreddit.
- Definir el **criterio de suficiencia** para dar por cerrada la ventana (RN-AN-02: la base comparativa es la media diaria de los diez días previos) y registrar el estado de acumulación día a día.
- Registrar la **decisión de los autores** sobre la fecha de cierre y sobre si se conserva la recolección actual o se reinicia con métricas corregidas (pregunta abierta de prioridad Media).
- **Ninguna métrica de resultados** se declara en este change (RN-GL-01). No se toca el DDL ni la lógica del pipeline.

## Capabilities

### New Capabilities

- `ventana-recoleccion-b5`: definición por escrito de la ventana real de recolección — fecha de inicio 2026-09-25, fecha de corte como decisión abierta, reemplazo de la ventana ficticia de seis meses (SU-02) y criterio de suficiencia para cerrarla.
- `bitacora-evidencia-diaria`: registro diario de la recolección en `V4/evidencias/` con fecha, posts ingeridos, distribución por subreddit, ejecuciones fallidas y causa, y trazabilidad a consultas SQL reproducibles.
- `caracterizacion-rate-limit`: caracterización de la ventana real de rate limiting de Reddit observada en las corridas, con su efecto sobre la cobertura por subreddit y el caso de `r/derechogenial` (US-002, m-16).
- `decision-cierre-ventana`: registro trazable de la decisión de los autores sobre la fecha de cierre de la ventana y sobre conservar o reiniciar la recolección (RN-GL-03).

### Modified Capabilities

Ninguna. `openspec/specs/` está vacío: no existen specs previos cuyas REQUISITOS cambien.

## Impact

- **Artefactos nuevos**: `V4/evidencias/bitacora_b5/` con una entrada diaria versionable, y el registro de caracterización de rate limiting.
- **Documentación a actualizar**: `V4/GUIA_EJECUCION.md` (tabla de estado de B5), `knowledge-base/02_descripcion_general.md` §Estado de implementación y `knowledge-base/09_decisiones_y_supuestos.md` §SU-02.
- **Sin impacto en**: `V4/anexos/A_DDL.sql` (Anexo A), `V4/anexos/B_workflow.json` (Anexo B), `V4/scripts/generar_workflow.py` y la lógica de nodos. Ninguna tabla, columna, índice o sentencia del pipeline cambia.
- **Sin impacto destructivo**: este change no ejecuta operaciones sobre `tesi_osint` más allá de consultas `SELECT` de conteo. No borra, no altera `active_monitoring`, no reinicia la recolección.
- **Dependencias**: requiere solo C-04 (verificada). No bloquea ni desbloquea DDL.
- **Habilita**: C-08 y C-11 (dependen directamente de la ventana) y, en cascada, C-09, C-20, C-21, C-23.
- **Restricción de paralelismo**: C-07 `semantica-ingested-at` debe cerrar antes de C-08, porque E6 se calcula sobre `ingested_at`. C-05 corre en paralelo con C-06 y C-07.
- **Riesgo asumido**: la corrida B4 del 2026-09-24 (201 posts verificados) es **anterior** a la fecha de inicio de la ventana. Sus posts no forman parte del corpus de B5 salvo decisión explícita de los autores. Esta consecuencia se documenta en `design.md` como decisión de diseño y se eleva a los autores en `decision-cierre-ventana`.
