# Modelo de Datos

## Dominios

- **Monitoreo:** subreddits activos y posts recolectados desde fuentes públicas.
- **Clasificación:** categoría, score, entidades y procesamiento NLP.
- **Detección:** evaluaciones de anomalías y alertas registradas.
- **Evidencia:** consultas, exportaciones y capturas derivadas de la base real.

## ERD

```text
subreddits (1) ────────< (N) posts (1) ────────< (N) comments
                              |
                              +── (N) anomalias (por categoría/ventana)
                                     |
                                     └── (N) alertas
```

`posts` referencia `subreddits` con `ON DELETE RESTRICT`; la baja de un subreddit se realiza desactivando `active_monitoring`, no borrando filas que ya tienen posts.

## Entidades

### subreddits

- `id VARCHAR(50) PRIMARY KEY`
- `display_name VARCHAR(100) UNIQUE NOT NULL`
- `subscribers INTEGER DEFAULT 0` — no disponible actualmente vía RSS.
- `active_monitoring BOOLEAN DEFAULT TRUE`
- `created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP`

### posts

- `id VARCHAR(50) PRIMARY KEY` — id derivado del enlace `/r/{sub}/comments/{id}/`.
- `subreddit_id VARCHAR(50) NOT NULL` — FK a `subreddits.id`.
- `title TEXT NOT NULL`
- `selftext TEXT`
- `url TEXT`
- `author_hash CHAR(64) NOT NULL` — HMAC-SHA-256 hexadecimal.
- `score INTEGER DEFAULT 0` y `num_comments INTEGER DEFAULT 0` — no disponibles vía RSS.
- `created_utc TIMESTAMPTZ NOT NULL` — fecha de publicación de Reddit.
- `nlp_category VARCHAR(100)` — salida del clasificador por diccionario; admite las nueve
  categorías de la taxonomía (ver «Taxonomía de `nlp_category`»). El DDL no impone `CHECK`,
  `ENUM` ni tipo dominio sobre esta columna, de modo que **la integridad del campo la
  garantiza el clasificador, no el esquema**: nada impide escribir a mano un valor fuera de
  la taxonomía.
- `nlp_score REAL CHECK (nlp_score BETWEEN 0 AND 1)` — la única restricción de dominio que
  sí aplica al clasificador.
- `entities JSONB` — entidades extraídas.
- `nlp_processed BOOLEAN DEFAULT FALSE`.
- `ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP` — base de la latencia.

Índices: `created_utc`, `nlp_category` e `ingested_at`.

### comments

- `id VARCHAR(50) PRIMARY KEY`
- `post_id VARCHAR(50) NOT NULL` — FK a `posts.id`.
- `body TEXT NOT NULL`
- `author_hash CHAR(64) NOT NULL`
- `score INTEGER DEFAULT 0`
- `created_utc TIMESTAMPTZ NOT NULL`
- `nlp_category VARCHAR(100)`, `nlp_score REAL`, `nlp_processed BOOLEAN`, `ingested_at TIMESTAMPTZ`
  — mismas columnas NLP que `posts`, con la misma taxonomía y la misma ausencia de `CHECK` sobre
  `nlp_category`.

La tabla existe para el modelo y las consultas, pero el pipeline RSS actual no la puebla.

### anomalias

- `id BIGSERIAL PRIMARY KEY`
- `ventana_inicio TIMESTAMPTZ NOT NULL`
- `ventana_fin TIMESTAMPTZ NOT NULL`
- `categoria VARCHAR(100) NOT NULL`
- `n_observado INTEGER NOT NULL`
- `base_media REAL NOT NULL`
- `umbral REAL NOT NULL`
- `disparo BOOLEAN NOT NULL DEFAULT FALSE`
- `created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP`

### alertas

- `id BIGSERIAL PRIMARY KEY`
- `anomalia_id BIGINT` — FK a `anomalias.id`.
- `canal VARCHAR(50) NOT NULL`
- `destinatario VARCHAR(200)`
- `payload JSONB`
- `estado VARCHAR(20) DEFAULT 'ENVIADA'` — **pero el workflow inserta siempre `'PENDIENTE'`**
  de forma explícita, así que el default del DDL nunca se usa en la práctica. Una fila
  queda `ENVIADA` solo si algún proceso posterior la actualiza, y hoy no hay ninguno.
  Discrepancia conocida entre esquema y comportamiento: ver `10_preguntas_abiertas.md`.
- `created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP`

## Taxonomía de `nlp_category`

El clasificador por diccionario del Code node `Classify Dictionary` emite nueve categorías, todas
sobre un único eje: **tipo de amenaza**. Los nombres son literales exactos tal como aparecen
en el código y se persisten sin transformación en `nlp_category`.

- `Phishing` — 22 términos
- `Robo de Credenciales` — 29 términos
- `Malware` — 24 términos
- `Ransomware` — 15 términos
- `Vulnerabilidades` — 30 términos
- `Filtración de Datos` — 29 términos
- `Infraestructura y Ataques` — 16 términos
- `Hacktivismo` — 16 términos
- `Ingenieria Social` — 20 términos

Total: **201 términos**. `MIN_HITS = 1`: basta un acierto para que una categoría entre en
consideración. El score es **saturante**, `score = min(1, hits / SATURATION)` con
`SATURATION = 4`; un post con cuatro o más aciertos de la categoría alcanza `1.0`. La escala
es fija e independiente del tamaño del diccionario, y queda dentro del
`CHECK (nlp_score BETWEEN 0 AND 1)` del DDL. El score antes era lineal
(`hits / |keywords(categoría)|`), de modo que los posts ya ingeridos con la fórmula
anterior se distinguen de los reclasificados: su `nlp_score` no es comparable con el de las
corridas nuevas.

Observaciones que se registran como hechos del código y no como errores:

- **Inconsistencia de tildes:** `Filtración de Datos` la lleva y `Ingenieria Social` no, pese
  a ser las dos categorías en castellano con diacrítico. Se conserva tal cual para no romper
  la comparación con la evidencia ya persistida.
- `Estafas Virtuales` ya no es una categoría propia: sus términos se redistribuyeron entre
  `Phishing`, `Robo de Credenciales` e `Ingenieria Social`.
- El listado completo de los 201 términos vive en la constante `DICT` de
  `V4/scripts/generar_workflow.py`; el Anexo C está pendiente (change C-13) y hasta que
  exista esa es la fuente consultable.

## Seed data inicial

Se insertan o actualizan los tres subreddits monitoreados: `argentina`, `devsarg` y `derechogenial`. El DDL completo y las correcciones aplicadas están en `V4/anexos/A_DDL.sql`.
