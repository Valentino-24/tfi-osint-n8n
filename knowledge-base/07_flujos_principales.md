# Flujos Principales

## Flujo 1: Ingesta programada de publicaciones

**Disparador**: Schedule cada 15 minutos.
**Actor**: n8n.

**Pasos**:

1. n8n carga la lista de subreddits activos.
2. Ejecuta `Prepare Subreddits` y resuelve el id de cada subreddit.
3.Hace un upsert de `subreddits` con `active_monitoring` y valores disponibles.
4. Consulta el feed `new/.rss` de cada subreddit.
5. Parsea cada item: título, cuerpo, enlace, autor, guid y fecha de publicación.
6. Deriva el id del post desde `/r/{sub}/comments/{id}/`.
7. Calcula `author_hash` con HMAC-SHA-256.
8. Clasifica con el diccionario y calcula `nlp_score`.
9. Extrae entidades tecnológicas en JSONB.
10. Hace upsert de `posts` con `ON CONFLICT (id) DO UPDATE`.
11. Deja `nlp_category`, `nlp_score`, `entities` e `ingested_at` disponibles para análisis.

**Diagrama de secuencia**:

```text
Schedule -> Prepare -> RSS Read -> Parse -> HMAC -> Clasificar
                                                 -> Entidades
   -> Upsert Subreddits -------------------------------> PostgreSQL
   -> Upsert Posts ------------------------------------> PostgreSQL
```

**Casos de error**:
- 429/403 en un feed: reintento hasta tres veces con 30 segundos; continuar con el resto.
- Respuesta vacía: no crear filas ficticias; conservar el estado de la corrida.
- Variable HMAC ausente: la ejecución debe detenerse con error explícito.
- Falta de credencial Postgres: reasignar la credencial en n8n; no inventar una conexión alternativa.

## Flujo 2: Evaluación diaria de anomalías

**Disparador**: Schedule diario a las 00:05.
**Actor**: n8n.

**Pasos**:

1. Calcula el intervalo de ayer (`ventana_inicio`, `ventana_fin`).
2. Cuenta posts por `nlp_category` en esa ventana.
3. Obtiene la media diaria de los diez días previos por categoría.
4. Calcula el umbral: máximo entre cuantil 95 de Poisson y 3.
5. Inserta una fila en `anomalias` por categoría, con `disparo` explícito.
6. Si hubo disparo, inserta la alerta en `alertas` con estado inicial.
7. Si el nodo Telegram está habilitado, envía la notificación.

**Caso de error**: con pocos días de datos, las evaluaciones pueden ser cero o carecer de base suficiente. Eso se reporta como limitación, no como ausencia de anomalías.

## Flujo 3: Consulta de evidencia

**Disparador**: consulta manual por parte del autor.
**Actor**: autor analista.

**Pasos**:

1. Conectar `psql` a `localhost:5433`, base `tesi_osint`, rol `tesi_app`.
2. Ejecutar consultas de recuentos, latencia, series horarias y anomalías.
3. Exportar la salida a `V4/evidencias/` con fecha y consulta usada.
4. Relacionar cada tabla, cifra o figura de la tesis con su evidencia.

**Restricciones**: no derivar una cifra que la consulta no haya contado; registrar `n` y la ventana temporal de cada métrica.
