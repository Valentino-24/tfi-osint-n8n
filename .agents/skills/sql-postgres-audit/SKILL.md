---
name: sql-postgres-audit
description: Postgres audit queries for TFI OSINT/n8n evidence. Use for window counts (ingested_at), distribution by subreddit (include zeros), anomalias days count, latency checks, upsert/idempotency verification. Read-only, reproducible, timezone-aware (America/Argentina/Buenos_Aires).
---

# SQL Postgres Audit (TFI OSINT/n8n)

## Context
DB: `tesi_osint` (Postgres 18, localhost:5433), role `tesi_app`. Tables: `subreddits`, `posts`, `comments`, `anomalias`, `alertas`. HMAC-SHA-256 `author_hash`. `ingested_at` = ingestion time.

## Principles
- **Read-only first**: Prefer `SELECT`. Never `INSERT/UPDATE/DELETE/TRUNCATE/DROP/ALTER`
- **Reproducible**: Save literal SQL + output to `V4/evidencias/` with date/window/n
- **Timezone aware**: Convert with `AT TIME ZONE 'America/Argentina/Buenos_Aires'` when grouping by "day"
- **Window by ingestion**: For B5 use `posts.ingested_at` range
- **Include zeros**: Join to `subreddits` and show all monitored in scope
- **Don't guess**: If uncertain, count distinct days/rows explicitly

## Common queries

### Posts in window (B5)
```sql
SELECT COUNT(*) AS n_posts_ventana
FROM posts
WHERE ingested_at >= TIMESTAMPTZ '2026-10-01T13:15:12-03:00'
  AND ingested_at <  TIMESTAMPTZ '2026-10-18T00:00:00-03:00';
```

### Distribution by subreddit (include zeros)
```sql
SELECT s.display_name,
       COUNT(p.id) AS n_posts
FROM subreddits s
LEFT JOIN posts p ON p.subreddit_id = s.id
  AND p.ingested_at >= TIMESTAMPTZ '2026-10-01T13:15:12-03:00'
  AND p.ingested_at <  TIMESTAMPTZ '2026-10-18T00:00:00-03:00'
WHERE s.active_monitoring = true
GROUP BY s.display_name
ORDER BY s.display_name;
```

### Days with anomalies evaluated
```sql
SELECT (ventana_inicio AT TIME ZONE 'America/Argentina/Buenos_Aires')::date AS dia_evaluado,
       COUNT(*) AS n_evaluaciones
FROM anomalias
WHERE ventana_fin >= TIMESTAMPTZ '2026-09-25T00:00:00-03:00'
  AND ventana_fin <= TIMESTAMPTZ '2026-10-18T00:00:00-03:00'
GROUP BY (ventana_inicio AT TIME ZONE 'America/Argentina/Buenos_Aires')::date
ORDER BY dia_evaluado;
```
> Note: Group by `ventana_inicio` (day evaluated), filter by `ventana_fin` with inclusive `<=` when cut is fixed.

### Check upsert/idempotency (ingested_at must not change)
```sql
SELECT id, ingested_at, nlp_category
FROM posts
WHERE id IN ('<id1>','<id2>')
ORDER BY id;
```
> For C-07: verify `ingested_at` identical across runs. Don't overwrite on conflict.

### Latency sample
```sql
SELECT id,
       created_utc,
       ingested_at,
       (ingested_at - created_utc) AS latencia
FROM posts
WHERE ingested_at >= TIMESTAMPTZ '2026-10-01T00:00:00-03:00'
ORDER BY ingested_at DESC
LIMIT 20;
```

## Gotchas for this project
- **TRUNCATE/reset**: After resets, `id` sequences can behave differently. Check counts.
- **B4 posts**: `ingested_at` 2026-09-24 - exclude from B5 unless decided
- **Scope change IN-07**: moved to `r/netsec,r/Malware,r/devsarg`. Don't count `r/argentina`/`r/derechogenial` unless explicitly asked
- **Motor horario**: Changed to 12:05 (machine off at night). `anomalias` rows depend on that
- **Poisson bug fixed**: Don't trust old umbrales
- **active_monitoring**: Never DELETE subreddit with posts - set `active_monitoring = false` if needed

## Checklist
- [ ] Read-only
- [ ] Timezone explicit
- [ ] Window explicit
- [ ] Denom includes zeros
- [ ] Output saved to `V4/evidencias/` with query+date+window+n
- [ ] No credentials in file
