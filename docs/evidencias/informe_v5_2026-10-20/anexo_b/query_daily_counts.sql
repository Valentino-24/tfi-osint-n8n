-- Ventana: ayer [00:00, 00:00) hora de Buenos Aires. Base: media diaria de los 10 días previos.
SELECT
  p.nlp_category AS categoria,
  COUNT(*) FILTER (WHERE p.ingested_at >= date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '1 day'
                   AND p.ingested_at <  date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires')) AS n_observado,
  COUNT(*) FILTER (WHERE p.ingested_at >= date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '11 day'
                   AND p.ingested_at <  date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '1 day') / 10.0 AS base_media,
  (date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '1 day') AT TIME ZONE 'America/Argentina/Buenos_Aires' AS ventana_inicio,
  date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') AT TIME ZONE 'America/Argentina/Buenos_Aires' AS ventana_fin
FROM posts p
WHERE p.nlp_category IS NOT NULL
  AND p.nlp_category <> 'No relevante'
  AND p.ingested_at >= date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '11 day'
GROUP BY p.nlp_category
ORDER BY p.nlp_category
