-- =====================================================================
--  Anexo A (V5) — DDL REAL del sistema
--  Motor: PostgreSQL (cluster propio del proyecto, puerto 5433)
--  Base: tesi_osint  |  Rol: tesi_app
--
--  CORRECCIONES APLICADAS vs. Anexo A de la V2 (auditor):
--   [N-06]  + columna nlp_score (puntuación normalizada [0,1])
--   [N-06]  + columna entities (entidades tecnológicas extraídas, JSONB)
--   [N-06]  + tablas anomalias y alertas (el modelo no las tenía)
--   [m-20]  posts.subreddit_id pasa de ON DELETE CASCADE a RESTRICT
--           (desactivar monitoreo con active_monitoring, no borrando)
--   [H-16]  se ELIMINA pg_trgm y el índice GIN sobre to_tsvector:
--           la clasificación ocurre en n8n (diccionario), no en la DB
--           vía búsqueda de texto completo (no justificado)
--   [H-01]  author_hash CHAR(64) con HMAC-SHA-256 (la V2 decía
--           "SHA-256 + Salt" — se corrige terminología y mecanismo en la V4)
--   [m-21]  alertas.estado DEFAULT 'PENDIENTE' (era 'ENVIADA': una inserción
--           sin estado explícito quedaba registrada como enviada aunque el
--           envío estuviera deshabilitado). Renombrados los comentarios.
--          + anomalias: UNIQUE (categoria, ventana_inicio) para extender la
--           idempotencia del nodo de análisis a la base (reejecutar el motor
--           no duplica evaluaciones).
--
--  La latencia publicación→ingesta se obtiene de:
--      ingested_at - created_utc  (no hace falta columna adicional)
-- =====================================================================

BEGIN;

-- 1. Subreddits monitoreados
CREATE TABLE IF NOT EXISTS subreddits (
    id                VARCHAR(50)  PRIMARY KEY,
    display_name      VARCHAR(100) UNIQUE NOT NULL,
    subscribers       INTEGER      DEFAULT 0,
    active_monitoring BOOLEAN      DEFAULT TRUE,
    created_at        TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP
);

-- 2. Publicaciones principales
CREATE TABLE IF NOT EXISTS posts (
    id            VARCHAR(50)  PRIMARY KEY,
    subreddit_id  VARCHAR(50)  NOT NULL REFERENCES subreddits(id) ON DELETE RESTRICT,
    title         TEXT         NOT NULL,
    selftext      TEXT,
    url           TEXT,
    author_hash   CHAR(64)     NOT NULL,          -- usuario seudonimizado (HMAC-SHA-256)
    score         INTEGER      DEFAULT 0,
    num_comments  INTEGER      DEFAULT 0,
    created_utc   TIMESTAMPTZ  NOT NULL,          -- fecha real de publicación en Reddit
    nlp_category  VARCHAR(100),                   -- salida del clasificador por diccionario
    nlp_score     REAL         CHECK (nlp_score BETWEEN 0 AND 1),  -- [N-06] puntuación [0,1]
    entities      JSONB,                          -- [N-06] entidades extraídas (OE4)
    nlp_processed BOOLEAN      DEFAULT FALSE,
    ingested_at   TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP  -- cuándo lo ingirió el sistema (latencia)
);

-- 3. Comentarios asociados
CREATE TABLE IF NOT EXISTS comments (
    id            VARCHAR(50)  PRIMARY KEY,
    post_id       VARCHAR(50)  NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    body          TEXT         NOT NULL,
    author_hash   CHAR(64)     NOT NULL,
    score         INTEGER      DEFAULT 0,
    created_utc   TIMESTAMPTZ  NOT NULL,
    nlp_category  VARCHAR(100),
    nlp_score     REAL         CHECK (nlp_score BETWEEN 0 AND 1),
    nlp_processed BOOLEAN      DEFAULT FALSE,
    ingested_at   TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP
);

-- 4. Registro de disparos del motor de anomalías  [N-06]
CREATE TABLE IF NOT EXISTS anomalias (
    id            BIGSERIAL   PRIMARY KEY,
    ventana_inicio TIMESTAMPTZ NOT NULL,          -- inicio de la ventana analizada
    ventana_fin    TIMESTAMPTZ NOT NULL,          -- fin de la ventana analizada
    categoria      VARCHAR(100) NOT NULL,
    n_observado    INTEGER     NOT NULL,          -- posts contados en la ventana
    base_media     REAL        NOT NULL,          -- promedio histórico de la categoría
    umbral         REAL        NOT NULL,          -- umbral disparado (justificado en 4.5)
    disparo        BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at     TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    -- [m-21] una evaluación por (categoría, ventana): reejecutar el motor no duplica
    CONSTRAINT anomalias_categoria_ventana_uniq UNIQUE (categoria, ventana_inicio)
);

-- 5. Alertas registradas  [N-06]  [m-21]
CREATE TABLE IF NOT EXISTS alertas (
    id           BIGSERIAL    PRIMARY KEY,
    anomalia_id  BIGINT       REFERENCES anomalias(id) ON DELETE CASCADE,
    canal        VARCHAR(50)  NOT NULL,           -- ej.: 'telegram'
    destinatario VARCHAR(200),
    payload      JSONB,                           -- carga útil del aviso (sin datos personales)
    estado       VARCHAR(20)  DEFAULT 'PENDIENTE', -- [m-21] 'PENDIENTE' hasta confirmar el envío
    created_at   TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP
);

-- 6. Índices para análisis
CREATE INDEX IF NOT EXISTS idx_posts_created_utc    ON posts (created_utc DESC);
CREATE INDEX IF NOT EXISTS idx_posts_nlp_category   ON posts (nlp_category);
CREATE INDEX IF NOT EXISTS idx_posts_ingested_at    ON posts (ingested_at);
CREATE INDEX IF NOT EXISTS idx_comments_post_id     ON comments (post_id);
CREATE INDEX IF NOT EXISTS idx_anomalias_created_at ON anomalias (created_at);

COMMIT;