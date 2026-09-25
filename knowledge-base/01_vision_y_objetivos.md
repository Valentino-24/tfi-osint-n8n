# Visión y Objetivos

## Propósito del sistema

El TFI OSINT/n8n es un prototipo real de monitoreo OSINT para detectar señales tempranas de phishing y otras amenazas en conversaciones públicas de Reddit. El sistema ingiere publicaciones, las clasifica con un diccionario taxonómico, extrae entidades tecnológicas, seudonimiza autores y registra evaluaciones de un motor de anomalías.

La V4 del trabajo final se apoya en evidencia producida por el sistema: no se aceptan cifras fabricadas. Las métricas de resultados deben salir de consultas sobre la base real y de la corrida de recolección.

## Objetivos por actor

| Actor | Objetivo principal | Objetivos secundarios |
|---|---|---|
| Autores del TFI | Construir y defender un artefacto verificable | Documentar el método, la arquitectura y los límites reales del prototipo |
| Operador del sistema | Mantener la recolección funcionando | Configurar n8n, PostgreSQL y las variables de entorno; verificar corridas |
| Investigador/analista | Detectar señales relevantes | Consultar categorías, entidades, posts y anomalías persistidas |
| Evaluador externo | Evaluar la clasificación | Etiquetar una submuestra y contrastar con las salidas del sistema |
| Tribunal/auditor | Comprobar trazabilidad y honestidad_epistémica | Verificar que anexos, tablas, figuras y cifras provengan del sistema real |

## Alcance v4.0

- Ingesta de feeds RSS públicos de tres subreddits: `r/argentina`, `r/devsarg` y `r/derechogenial`.
- Persistencia idempotente de posts en PostgreSQL.
- Seudonimización del autor con HMAC-SHA-256 y clave secreta por despliegue.
- Clasificación por diccionario con categoría y score normalizado en `[0, 1]`.
- Extracción de entidades tecnológicas: CVE, emails, IPs, dominios y productos.
- Registro de anomalías por categoría y de alertas en base de datos.
- Generación de evidencias reproducibles: DDL, export del workflow, consultas SQL, capturas y figuras.
- Documentación de la ventana real de recolección y de sus límites.

## Fuera de alcance

- Autenticación, usuarios o multi-tenancy de la aplicación: n8n es local y el acceso queda controlado por el despliegue.
- Publicación activa en redes sociales o respuesta automática a amenazas.
- Alertas obligatorias por Telegram: el nodo está presente pero desactivado por defecto.
- Ingesta de comentarios en la operación actual: la tabla existe, pero el pipeline RSS no los trae.
- Recuperación de `score`, `num_comments` y suscriptores desde RSS.
- Reemplazar el clasificador por un modelo entrenado: la V4 documenta el clasificador por diccionario.
- Usar cifras de versiones anteriores que no fueron producidas por el sistema actual.

## Métricas de éxito

- El pipeline ejecuta consultas de ingesta sin duplicar posts.
- La base contiene posts con `nlp_category`, `nlp_score`, `entities` y `author_hash` válido.
- La latencia publicación→ingesta puede calcularse sobre datos reales.
- El motor de anomalías registra evaluaciones reproducibles.
- Cada afirmación cuantitativa de la tesis puede rastrearse a una consulta, export o evidencia identificada.
