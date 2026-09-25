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
- `nlp_category VARCHAR(100)` — salida del clasificador.
- `nlp_score REAL CHECK (nlp_score BETWEEN 0 AND 1)`.
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
- `nlp_category VARCHAR(100)`, `nlp_score REAL`, `nlp_processed BOOLEAN`, `ingested_at TIMESTAMPTZ`.

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
- `estado VARCHAR(20) DEFAULT 'ENVIADA'`
- `created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP`

## Seed data inicial

Se insertan o actualizan los tres subreddits monitoreados: `argentina`, `devsarg` y `derechogenial`. El DDL completo y las correcciones aplicadas están en `V4/anexos/A_DDL.sql`.
