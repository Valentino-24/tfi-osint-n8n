# Arquitectura Propuesta

## Patrones aplicados

| Patrón | Dónde se usa | Por qué |
|---|---|---|
| Pipeline por lotes | Triggers de ingesta y anomalías | El sistema procesa snapshots periódicos y no requiere interacción por request |
| Upsert idempotente | `subreddits` y `posts` | Permite reintentar sin duplicar hechos |
| Fuente pública degradable | RSS/Atom | Evita bloquear la recolección por falta de una developer account de Reddit |
| HMAC pseudonimización | Nodo Code antes del upsert | Reduce exposición del autor y mantiene trazabilidad técnica |
| Registro de auditoría | `anomalias` y `alertas` | Permite evidenciar evaluaciones y no solo disparos |
| Configuración por variables de entorno | Clave HMAC y acceso a módulos | Evita guardar secretos en el JSON exportable |

## Estructura de directorios

```text
Tesis/
├── PLAN_V4.md
├── V4/
│   ├── anexos/
│   │   ├── A_DDL.sql
│   │   └── B_workflow.json
│   ├── capitulos/
│   ├── evidencias/
│   ├── figuras/
│   ├── scripts/
│   │   ├── generar_workflow.py
│   │   ├── generar_figura1.py
│   │   └── scripts de arranque/parada de PostgreSQL
│   ├── devoluciones/
│   ├── GUIA_CONCEPTOS.md
│   ├── GUIA_EJECUCION.md
│   └── GUIA_INSTALACION.md
├── knowledge-base/
└── openspec/
```

`generar_workflow.py` es la fuente de verdad del workflow; `B_workflow.json` es el artefacto importable. Después de una importación por CLI se debe reasignar la credencial Postgres en la interfaz de n8n.

## Seguridad

- **Autenticación**: no hay aplicación propia; n8n y PostgreSQL son servicios locales del entorno del proyecto.
- **Autorización**: acceso al host y a la base por control del despliegue; la tabla `alertas` y las consultas analíticas no son públicas.
- **Datos de terceros**: se guardan título, cuerpo y datos derivados de publicaciones públicas; se seudonimiza el autor.
- **Secretos**: `OSINT_HMAC_KEY`, credenciales Postgres y token Telegram nunca se versionan.
- **Configuración n8n**: se necesitan `NODE_FUNCTION_ALLOW_BUILTIN=crypto` y `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` para el nodo Code que usa HMAC.
- **Riesgo residual**: la seudonimización reduce exposición, pero no elimina la condición de dato personal; se debe limitar el acceso y documentar retención.

## Variables de entorno

| Variable | Descripción | Ejemplo | Sensible |
|---|---|---|---|
| `OSINT_HMAC_KEY` | Clave secreta por despliegue para HMAC | valor generado de 32 bytes en hex | Sí |
| `NODE_FUNCTION_ALLOW_BUILTIN` | Permite el módulo builtin `crypto` en Code | `crypto` | No, pero controla capacidad |
| `N8N_BLOCK_ENV_ACCESS_IN_NODE` | Permite leer variables desde nodos Code | `false` | Sí, afecta seguridad |
| `TELEGRAM_BOT_TOKEN` | Token del bot, solo si se habilita Telegram | token de BotFather | Sí |
| `TELEGRAM_CHAT_ID` | Destinatario de la alerta | id numérico del chat | Sí |
| `PGPASSWORD` | Password del rol PostgreSQL en consultas locales | `tesi_app_2026` en entorno de desarrollo | Sí |

La configuración completa por etapas está en `V4/GUIA_EJECUCION.md` y `V4/GUIA_INSTALACION.md`.
