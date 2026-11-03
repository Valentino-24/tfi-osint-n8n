-- Consultas Q1..Q15 del capítulo de resultados (ventana B5, corte 2026-10-17).
-- Todas son de solo lectura. Los literales de fecha fijan el estado congelado
-- del 2026-10-19, de modo que la base pueda haber crecido sin alterar la salida.
-- Track secundario congelado: 31 filas persistidas hasta 2026-10-19 18:00 UTC.

-- === Q1 TOTALES ===
SELECT
  count(*) FILTER (WHERE ingested_at < '2026-10-19 18:00:00+00') AS total,
  count(*) FILTER (WHERE created_utc < '2026-10-18 03:00:00+00'
                     AND ingested_at < '2026-10-19 00:00:00+00') AS ventana,
  count(*) FILTER (WHERE created_utc < '2026-10-01 03:00:00+00'
                     AND ingested_at < '2026-10-01 03:00:00+00') AS previos,
  count(*) FILTER (WHERE ingested_at >= '2026-10-19 00:00:00+00'
                     AND ingested_at <  '2026-10-19 18:00:00+00') AS track,
  (SELECT count(*) FROM comments) AS comentarios,
  count(*) FILTER (WHERE ingested_at < '2026-10-19 00:00:00+00'
                     AND nlp_category IS NULL) AS sin_categoria
FROM posts;

-- === Q2 RANGO DE INGESTA VENTANA ===
SELECT
  min(ingested_at) AS min_ingesta,
  max(ingested_at) AS max_ingesta,
  min(created_utc) AS min_creado,
  max(created_utc) AS max_creado
FROM posts
WHERE created_utc < '2026-10-18 03:00:00+00'
  AND ingested_at < '2026-10-19 00:00:00+00';

-- === Q3 POR SUBREDDIT ===
SELECT
  subreddit_id,
  count(*) AS n,
  round(100.0 * count(*) / sum(count(*)) OVER (), 2) AS pct,
  count(*) FILTER (WHERE nlp_category = 'No relevante') AS no_relevante,
  round(100.0 * count(*) FILTER (WHERE nlp_category = 'No relevante')
        / count(*), 2) AS pct_no_rel
FROM posts
WHERE created_utc < '2026-10-18 03:00:00+00'
  AND ingested_at < '2026-10-19 00:00:00+00'
GROUP BY subreddit_id
ORDER BY n DESC;

-- === Q4 POR DIA (hora local) ===
SELECT
  (ingested_at AT TIME ZONE 'America/Argentina/Buenos_Aires')::date AS dia,
  count(*) AS n
FROM posts
WHERE created_utc < '2026-10-18 03:00:00+00'
  AND ingested_at < '2026-10-19 00:00:00+00'
GROUP BY 1
ORDER BY 1;

-- === Q5 TABLA 3 CATEGORIAS ===
SELECT
  nlp_category AS categoria,
  count(*) AS n,
  round(100.0 * count(*) / sum(count(*)) OVER (), 2) AS pct,
  round(avg(nlp_score)::numeric, 3) AS score_medio
FROM posts
WHERE created_utc < '2026-10-18 03:00:00+00'
  AND ingested_at < '2026-10-19 00:00:00+00'
GROUP BY nlp_category
ORDER BY n DESC;

-- === Q6 LATENCIA ===
SELECT
  count(*) AS n,
  round(avg(extract(epoch FROM ingested_at - created_utc) / 60.0)::numeric, 2) AS media,
  round(stddev_samp(extract(epoch FROM ingested_at - created_utc) / 60.0)::numeric, 2) AS ds,
  round(percentile_cont(0.5) WITHIN GROUP (
          ORDER BY extract(epoch FROM ingested_at - created_utc) / 60.0)::numeric, 2) AS p50,
  round(percentile_cont(0.95) WITHIN GROUP (
          ORDER BY extract(epoch FROM ingested_at - created_utc) / 60.0)::numeric, 2) AS p95,
  round(min(extract(epoch FROM ingested_at - created_utc) / 60.0)::numeric, 2) AS minimo,
  round(max(extract(epoch FROM ingested_at - created_utc) / 60.0)::numeric, 2) AS maximo,
  count(*) FILTER (WHERE extract(epoch FROM ingested_at - created_utc) / 60.0 > 5) AS gt5,
  count(*) FILTER (WHERE extract(epoch FROM ingested_at - created_utc) / 60.0 > 15) AS gt15,
  count(*) FILTER (WHERE extract(epoch FROM ingested_at - created_utc) / 60.0 > 60) AS gt60,
  count(*) FILTER (WHERE extract(epoch FROM ingested_at - created_utc) / 60.0 > 1440) AS gt24h,
  count(*) FILTER (WHERE extract(epoch FROM ingested_at - created_utc) < 0) AS negativos
FROM posts
WHERE created_utc < '2026-10-18 03:00:00+00'
  AND ingested_at < '2026-10-19 00:00:00+00';

-- === Q7 ANOMALIAS RESUMEN ===
SELECT
  count(*) AS filas,
  count(DISTINCT ventana_inicio) AS dias,
  count(*) FILTER (WHERE disparo) AS disparos,
  min(ventana_fin) AS desde,
  max(ventana_fin) AS hasta
FROM anomalias;

-- === Q8 ANOMALIAS POR CATEGORIA ===
SELECT
  categoria,
  count(*) AS evals,
  sum(n_observado) AS observados,
  count(*) FILTER (WHERE disparo) AS disparos,
  round(avg(base_media)::numeric, 2) AS base_media_prom,
  round(avg(umbral)::numeric, 2) AS umbral_prom
FROM anomalias
GROUP BY categoria
ORDER BY evals DESC, categoria;

-- === Q9 DISPAROS DETALLE ===
SELECT
  ventana_fin::date AS dia,
  categoria,
  n_observado,
  base_media,
  umbral
FROM anomalias
WHERE disparo
ORDER BY dia, categoria;

-- === Q10 CATEGORIAS EVALUADAS POR DIA ===
SELECT
  ventana_fin::date AS dia,
  count(*) AS filas,
  string_agg(DISTINCT categoria, ' | ' ORDER BY categoria) AS cats
FROM anomalias
GROUP BY 1
ORDER BY 1;

-- === Q11 ALERTAS ===
SELECT
  canal,
  estado,
  count(*) AS n
FROM alertas
GROUP BY canal, estado
ORDER BY canal, estado;

-- === Q12 TOP POSTS POR CATEGORIA ===
WITH ranked AS (
  SELECT
    nlp_category,
    id,
    title AS titulo,
    nlp_score AS score,
    created_utc,
    url,
    row_number() OVER (
      PARTITION BY nlp_category
      ORDER BY nlp_score DESC, created_utc DESC
    ) AS rn
  FROM posts
  WHERE created_utc < '2026-10-18 03:00:00+00'
    AND ingested_at < '2026-10-19 00:00:00+00'
    AND nlp_category IS NOT NULL
    AND nlp_category <> 'No relevante'
)
SELECT
  nlp_category,
  id,
  titulo,
  round(score::numeric, 3) AS score,
  created_utc::date AS fecha,
  url
FROM ranked
WHERE rn <= 2
ORDER BY nlp_category, rn;

-- === Q13 DISTRIBUCION DE SCORE ===
SELECT
  round(nlp_score::numeric, 2) AS score,
  count(*) AS n
FROM posts
WHERE created_utc < '2026-10-18 03:00:00+00'
  AND ingested_at < '2026-10-19 00:00:00+00'
GROUP BY 1
ORDER BY 1;

-- === Q14 CATEGORIAS DISTINTAS EN VENTANA ===
SELECT
  nlp_category AS categoria,
  count(*) AS n
FROM posts
WHERE created_utc < '2026-10-18 03:00:00+00'
  AND ingested_at < '2026-10-19 00:00:00+00'
GROUP BY nlp_category
ORDER BY n DESC;

-- === Q15 TRACK SECUNDARIO ===
SELECT
  count(*) AS n,
  min(ingested_at) AS desde,
  max(ingested_at) AS hasta
FROM posts
WHERE ingested_at >= '2026-10-19 00:00:00+00'
  AND ingested_at <  '2026-10-19 18:00:00+00';
