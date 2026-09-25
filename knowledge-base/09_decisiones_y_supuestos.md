# Decisiones y Supuestos

## Decisiones documentadas

### DD-01 — Usar RSS como fuente operativa
**Decisión**: migrar la ingesta de Reddit a feeds RSS/Atom públicos.
**Contexto**: la API `.json` pública devolvió 403 "blocked by network security" desde la IP del proyecto y la creación de apps quedó sujeta a la Responsible Builder Policy.
**Alternativas consideradas**: OAuth con developer account de Reddit; esperar un desbloqueo de la API; RSS como fuente degradada.
**Justificación**: permite seguir recolectando evidencia real sin depender de una cuenta de desarrollador.
**Trade-offs aceptados**: no llegan `score`, `num_comments` ni suscriptores; el feed puede devolver 0 items o 429.

### DD-02 — Mantener el modelo de DDL completo
**Decisión**: conservar las tablas `subreddits`, `posts`, `comments`, `anomalias` y `alertas` aunque la operación actual use RSS.
**Contexto**: el modelo documenta el sistema previsto y permite comparar estados y exportar evidencia.
**Alternativas consideradas**: reducir el esquema a las tablas realmente pobladas.
**Justificación**: comentarios y alertas son parte del diseño; vacíos no significan que deban eliminarse.
**Trade-offs aceptados**: `comments` permanece vacía y `alertas` depende de que el motor dispare y Telegram sea configurado.

### DD-03 — Seudonimizar con HMAC-SHA-256
**Decisión**: usar HMAC-SHA-256 con clave secreta por despliegue para `author_hash`.
**Contexto**: la V2 describía incorrectamente "SHA-256 con salt" y la tesis requiere seudonimización reproducible dentro de un despliegue.
**Alternativas consideradas**: hash simple; salt fijo; HMAC rotativo.
**Justificación**: HMAC aporta la clave de despliegue y separa el hash de otros despliegues.
**Trade-offs aceptados**: el valor original no se puede recuperar desde el hash y la gestión de claves debe documentarse.

### DD-04 — Persistencia idempotente
**Decisión**: usar `ON CONFLICT (id) DO UPDATE` en los upserts.
**Contexto**: los reintentos y corridas manuales repiten consultas sobre posts ya vistos.
**Alternativas consideradas**: borrar y volver a insertar; mantener solo inserts y aceptar duplicados.
**Justificación**: el upsert permite reanudar el flujo sin duplicar y hace comparables las corridas.
**Trade-offs aceptados**: hay que definir y documentar con precisión qué campos se actualizan y cómo se preserva la latencia.

### DD-05 — Motor de anomalías con Poisson y mínimo absoluto
**Decisión**: umbral `max(cuantil 95 de Poisson, 3)` frente a la media de los diez días previos.
**Contexto**: el auditor pidió justificar el umbral; `μ + 2σ` no explica bien conteos pequeños y variables.
**Alternativas consideradas**: μ+2σ; cuantil simple; EWMA.
**Justificación**: el cuantil de Poisson representa la dispersión esperada de conteos y el mínimo evita alertas por volúmenes triviales.
**Trade-offs aceptados**: el motor necesita varios días de historia; con una base corta las evaluaciones no son concluyentes.

### DD-06 — Usar RESTRICT en la relación posts-subreddits
**Decisión**: `posts.subreddit_id` usa `ON DELETE RESTRICT`.
**Contexto**: borrar un subreddit destruiría evidencia ya recolectada.
**Alternativas consideradas**: CASCADE o borrado lógico sin integridad referencial.
**Justificación**: `active_monitoring` permite desactivar el monitoreo sin perder trazabilidad.
**Trade-offs aceptados**: la operación de borrado debe documentarse y ser explícita.

### DD-07 — Telegram queda opcional
**Decisión**: registrar las alertas en PostgreSQL pero dejar el nodo de Telegram deshabilitado por defecto.
**Contexto**: la evidencia de una alerta externa requiere un canal real y no debe bloquear la recolección.
**Alternativas consideradas**: exigir Telegram en la primera versión.
**Justificación**: la base de datos conserva el registro auditable aunque el canal externo no esté configurado.
**Trade-offs aceptados**: E12 no puede presentarse como alerta enviada hasta obtener una captura real.

## Supuestos inferidos

### SU-01 — La KB describe el sistema real y la tesis completa
**Supuesto**: conviene documentar tanto el prototipo ejecutado como el alcance académico y los pasos B5/B6.
**Origen**: decisión tomada por el autor al iniciar la fundación de OpenSpec.
**Riesgo si es falso**: mezcla documentación de producto con documentación metodológica.
**Cómo validar**: revisar `01_vision_y_objetivos.md` y `10_preguntas_abiertas.md` con el equipo.

### SU-02 — La ventana de recolección será real y declarará su duración
**Supuesto**: no se usará la ventana ficticia de seis meses de versiones anteriores.
**Origen**: `PLAN_V4.md`, sección de realidad y límites.
**Riesgo si es falso**: las métricas de la tesis serían incomparables o no trazables.
**Cómo validar**: fechar el inicio y fin de la ventana antes de producir las tablas finales.
**Estado (2026-09-25)**: la ventana real es la **B5**, con inicio **2026-09-25** y corte
**`no fijada`** — decisión abierta de los autores con sus directores. El corpus se define sobre
`posts.ingested_at`; la fecha de corte no tiene fecha tentativa y la cierra la tarea 6.1 del
change `ventana-recoleccion-b5` (C-05). Criterio de suficiencia: 10 días completos de
evaluaciones en `anomalias` (base comparativa de RN-AN-02). Definición completa y bitácora
diaria en `V4/evidencias/VENTANA_B5.md` y `V4/evidencias/bitacora_b5/`.

### SU-03 — La base seguirá siendo local durante la recolección
**Supuesto**: PostgreSQL en `localhost:5433` y n8n local son suficientes para la entrega.
**Origen**: guías de instalación y ejecución.
**Riesgo si es falso**: habría que documentar disponibilidad, backups, seguridad y Continuous del entorno.
**Cómo validar**: registrar la especificación del entorno E9.
