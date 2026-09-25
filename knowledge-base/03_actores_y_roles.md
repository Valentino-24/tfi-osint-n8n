# Actores y Roles

## Actores del sistema

| Actor | Descripción | Cómo interactúa |
|---|---|---|
| Autor operador | Persona que ejecuta y mantiene el prototipo | Arranca PostgreSQL/n8n, importa el workflow, configura credenciales y ejecuta consultas |
| Autor analista | Investiga la salida del pipeline | Consulta `posts`, `anomalias` y `alertas`; prepara evidencias |
| n8n | Orquestador de tareas | Ejecuta los triggers, transformaciones y operaciones SQL |
| Reddit | Fuente externa de datos | Expone feeds RSS/Atom públicos |
| PostgreSQL | Almacén de hechos observados | Persiste subreddits, posts, comentarios, anomalías y alertas |
| Evaluador externo | Revisor independiente | Etiqueta una submuestra de posts para evaluar la clasificación |
| Tribunal/auditor | Destinatario de la evidencia | Verifica trazabilidad, reproducibilidad y correspondencia con el texto |

## RBAC — Matriz de permisos

El prototipo no implementa autenticación ni RBAC de aplicación. Los permisos son operativos y se dividen por responsabilidad:

| Rol | n8n | PostgreSQL | Código/workflow | Evidencias |
|---|---|---|---|---|
| Autor operador | Configura y ejecuta | Conexión de aplicación | Importa y ejecuta | Prepara consultas y capturas |
| Autor analista | Consulta estado | Solo lectura para análisis | No modifica el DDL sin acuerdo | Produce y valida |
| Evaluador externo | Sin acceso al pipeline | Acceso mínimo a submuestra, si se acuerda | No modifica | Etiqueta muestra |
| Tribunal/auditor | Acceso al export/evidencia | Acceso según la autorización concedida | Revisión de artefactos | Verifica afirmaciones |

## Rutas públicas

- Feeds RSS públicos `https://www.reddit.com/r/{subreddit}/new/.rss`.
- Interfaz local de n8n: `http://localhost:5678` (protegida por la configuración del despliegue).
- Puerto PostgreSQL local: `5433`; no debe exponerse a Internet.
- No hay rutas públicas propias ni endpoints de consulta del proyecto.
