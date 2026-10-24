-- Evidencia de recalculo V5 - 2026-10-22
-- Corte B5: created_utc < '2026-10-18 03:00:00+00' AND ingested_at < '2026-10-19 00:00:00+00'

-- 1) Totales B5
SELECT COUNT(*) AS total_b5
FROM posts
WHERE created_utc < '2026-10-18 03:00:00+00'
  AND ingested_at < '2026-10-19 00:00:00+00';

-- 2) Por categoria
SELECT nlp_category, COUNT(*) AS cnt
FROM posts
WHERE created_utc < '2026-10-18 03:00:00+00'
  AND ingested_at < '2026-10-19 00:00:00+00'
GROUP BY nlp_category
ORDER BY cnt DESC;

-- 3) Por comunidad
SELECT s.display_name, COUNT(*) AS cnt
FROM posts p
JOIN subreddits s ON s.id = p.subreddit_id
WHERE p.created_utc < '2026-10-18 03:00:00+00'
  AND p.ingested_at < '2026-10-19 00:00:00+00'
GROUP BY s.display_name
ORDER BY cnt DESC;

