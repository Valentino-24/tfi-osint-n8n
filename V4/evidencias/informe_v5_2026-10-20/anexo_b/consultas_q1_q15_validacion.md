# Validación Q1–Q15 — reconstrucción SQL

**Fecha de validación:** 2026-10-22
**Base:** `tfi-postgres`, `tesi_osint` (PostgreSQL 18)
**Referencia congelada:** `V4/evidencias/informe_v4_2026-10-19/consultas_corpus_b5.txt`
**Script validado:** `V4/evidencias/informe_v5_2026-10-20/anexo_b/consultas_q1_q15.sql`

## Método

- Todas las consultas son de solo lectura (`SELECT`).
- La base creció de 755 a 765 filas después del corte. Para reproducir el estado
  congelado del 2026-10-19 se fijaron literales de fecha:
  - ventana: `created_utc < '2026-10-18 03:00:00+00' AND ingested_at < '2026-10-19 00:00:00+00'`.
  - track secundario congelado: `ingested_at >= '2026-10-19 00:00:00+00' AND ingested_at < '2026-10-19 18:00:00+00'`
    (las 31 filas persistidas hasta 2026-10-19 17:18:19.823468+00; las 10 filas
    posteriores, ingeridas desde 2026-10-19 18:31 en adelante, se excluyen).
- `anomalias` (112 filas) y `alertas` (6 filas) no cambiaron, por lo que Q7–Q11
  reproducen sin filtro adicional.

**Resultado global: 15/15 PASS.**

Ninguna consulta requiere un snapshot pre-19/10 para reproducirse: el estado se
reconstruye con literales sobre `ingested_at`. Sin esos literales, Q1, Q15 y todo
lo que cuenta la ventana fallarían porque la tabla creció (765 filas hoy).

## Normalización aplicada

Se compararon valores de columna (no orden ni formato). La salida esperada de Q12
trae títulos truncados por el ancho de columna de `psql`; la consulta devuelve el
valor completo y `psql` lo trunca igual al mostrarlo en formato alineado, por lo
que la comparación coincide. La diferencia de acentos visible en el `.txt`
(`Filtraci├│n`) es una mala decodificación del archivo original, no un valor
distinto en la base (`Filtración`).

---

## Q1 TOTALES — PASS

```sql
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
```

Actual:

```text
 total | ventana | previos | track | comentarios | sin_categoria
-------+---------+---------+-------+-------------+---------------
   755 |     724 |       0 |    31 |           0 |             0
(1 row)
```

Esperado: `755 | 724 | 0 | 31 | 0 | 0`. **PASS.**

Nota: `total` se fija con `ingested_at < '2026-10-19 18:00:00+00'`, que abarca
las 724 de ventana más las 31 del track y excluye las 10 filas posteriores.

---

## Q2 RANGO DE INGESTA VENTANA — PASS

```sql
SELECT
  min(ingested_at) AS min_ingesta,
  max(ingested_at) AS max_ingesta,
  min(created_utc) AS min_creado,
  max(created_utc) AS max_creado
FROM posts
WHERE created_utc < '2026-10-18 03:00:00+00'
  AND ingested_at < '2026-10-19 00:00:00+00';
```

Actual:

```text
          min_ingesta          |          max_ingesta          |       min_creado       |       max_creado
-------------------------------+-------------------------------+------------------------+------------------------
 2026-10-01 16:15:43.944968+00 | 2026-10-17 16:16:14.406781+00 | 2026-05-21 18:47:28+00 | 2026-10-17 16:06:14+00
(1 row)
```

Esperado: idéntico. **PASS.**

---

## Q3 POR SUBREDDIT — PASS

```sql
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
```

Actual:

```text
 subreddit_id |  n  |  pct  | no_relevante | pct_no_rel
--------------+-----+-------+--------------+------------
 devsarg      | 428 | 59.12 |          421 |      98.36
 netsec       | 150 | 20.72 |           84 |      56.00
 Malware      | 146 | 20.17 |           49 |      33.56
(3 rows)
```

Esperado: idéntico. **PASS.**

---

## Q4 POR DIA (hora local) — PASS

```sql
SELECT
  (ingested_at AT TIME ZONE 'America/Argentina/Buenos_Aires')::date AS dia,
  count(*) AS n
FROM posts
WHERE created_utc < '2026-10-18 03:00:00+00'
  AND ingested_at < '2026-10-19 00:00:00+00'
GROUP BY 1
ORDER BY 1;
```

Actual:

```text
    dia     |  n
------------+-----
 2026-10-01 | 307
 2026-10-02 |  32
 2026-10-04 |  37
 2026-10-05 |  25
 2026-10-06 |  39
 2026-10-07 |  16
 2026-10-08 |  35
 2026-10-09 |  31
 2026-10-10 |  26
 2026-10-11 |  17
 2026-10-12 |  31
 2026-10-13 |  28
 2026-10-14 |  28
 2026-10-15 |  31
 2026-10-16 |  33
 2026-10-17 |   8
(16 rows)
```

Esperado: idéntico. **PASS.** (El día es el de `ingested_at`, no el de creación;
agrupar por `created_utc` produciría fechas de mayo a septiembre.)

---

## Q5 TABLA 3 CATEGORIAS — PASS

```sql
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
```

Actual:

```text
         categoria         |  n  |  pct  | score_medio
---------------------------+-----+-------+-------------
 No relevante              | 554 | 76.52 |       0.000
 Malware                   |  79 | 10.91 |       0.389
 Vulnerabilidades          |  61 |  8.43 |       0.320
 Phishing                  |  12 |  1.66 |       0.250
 Robo de Credenciales      |   5 |  0.69 |       0.250
 Filtración de Datos       |   4 |  0.55 |       0.250
 Ransomware                |   4 |  0.55 |       0.250
 Infraestructura y Ataques |   3 |  0.41 |       0.250
 Hacktivismo               |   2 |  0.28 |       0.250
(9 rows)
```

Esperado: idéntico (salvo la decodificación `Filtraci├│n` del `.txt`). **PASS.**

---

## Q6 LATENCIA — PASS

```sql
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
```

Actual:

```text
  n  |  media   |    ds    |  p50   |    p95    | minimo |  maximo   | gt5 | gt15 | gt60 | gt24h | negativos
-----+----------+----------+--------+-----------+--------+-----------+-----+------+------+-------+-----------
 724 | 16483.78 | 38407.90 | 889.85 | 117613.06 |   0.28 | 191368.81 | 685 |  580 |  541 |   295 |         0
(1 row)
```

Esperado: idéntico. **PASS.**

Nota: la latencia está expresada en **minutos** (`epoch/60`). En segundos la
media sería 989.026,84 y no coincidiría.

---

## Q7 ANOMALIAS RESUMEN — PASS

```sql
SELECT
  count(*) AS filas,
  count(DISTINCT ventana_inicio) AS dias,
  count(*) FILTER (WHERE disparo) AS disparos,
  min(ventana_fin) AS desde,
  max(ventana_fin) AS hasta
FROM anomalias;
```

Actual:

```text
 filas | dias | disparos |         desde          |         hasta
-------+------+----------+------------------------+------------------------
   112 |   15 |        6 | 2026-10-02 03:00:00+00 | 2026-10-18 03:00:00+00
(1 row)
```

Esperado: idéntico. **PASS.**

---

## Q8 ANOMALIAS POR CATEGORIA — PASS

```sql
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
```

Actual:

```text
         categoria         | evals | observados | disparos | base_media_prom | umbral_prom
---------------------------+-------+------------+----------+-----------------+-------------
 Filtración de Datos       |    15 |          4 |        0 |            0.19 |        3.00
 Malware                   |    15 |         79 |        1 |            4.00 |        8.33
 Phishing                  |    15 |         11 |        1 |            0.57 |        3.00
 Robo de Credenciales      |    15 |          5 |        0 |            0.25 |        3.00
 Vulnerabilidades          |    15 |         59 |        2 |            2.95 |        6.87
 Hacktivismo               |    14 |          2 |        0 |            0.11 |        3.00
 Ransomware                |    14 |          4 |        1 |            0.24 |        3.00
 Infraestructura y Ataques |     9 |          3 |        1 |            0.27 |        3.00
(8 rows)
```

Esperado: idéntico. **PASS.** (El orden es `evals DESC, categoria ASC`.)

---

## Q9 DISPAROS DETALLE — PASS

```sql
SELECT
  ventana_fin::date AS dia,
  categoria,
  n_observado,
  base_media,
  umbral
FROM anomalias
WHERE disparo
ORDER BY dia, categoria;
```

Actual:

```text
    dia     |         categoria         | n_observado | base_media | umbral
------------+---------------------------+-------------+------------+--------
 2026-10-02 | Infraestructura y Ataques |           3 |          0 |      3
 2026-10-02 | Malware                   |          55 |          0 |      3
 2026-10-02 | Phishing                  |           6 |          0 |      3
 2026-10-02 | Ransomware                |           3 |          0 |      3
 2026-10-02 | Vulnerabilidades          |          41 |          0 |      3
 2026-10-13 | Vulnerabilidades          |           4 |        0.8 |      3
(6 rows)
```

Esperado: idéntico. **PASS.**

---

## Q10 CATEGORIAS EVALUADAS POR DIA — PASS

```sql
SELECT
  ventana_fin::date AS dia,
  count(*) AS filas,
  string_agg(DISTINCT categoria, ' | ' ORDER BY categoria) AS cats
FROM anomalias
GROUP BY 1
ORDER BY 1;
```

Actual:

```text
    dia     | filas |                                                                   cats
------------+-------+-------------------------------------------------------------------------------------------------------------------------------------------
 2026-10-02 |     7 | Filtración de Datos | Infraestructura y Ataques | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-05 |     8 | Filtración de Datos | Hacktivismo | Infraestructura y Ataques | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-06 |     8 | Filtración de Datos | Hacktivismo | Infraestructura y Ataques | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-07 |     8 | Filtración de Datos | Hacktivismo | Infraestructura y Ataques | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-08 |     8 | Filtración de Datos | Hacktivismo | Infraestructura y Ataques | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-09 |     8 | Filtración de Datos | Hacktivismo | Infraestructura y Ataques | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-10 |     8 | Filtración de Datos | Hacktivismo | Infraestructura y Ataques | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-11 |     8 | Filtración de Datos | Hacktivismo | Infraestructura y Ataques | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-12 |     8 | Filtración de Datos | Hacktivismo | Infraestructura y Ataques | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-13 |     7 | Filtración de Datos | Hacktivismo | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-14 |     7 | Filtración de Datos | Hacktivismo | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-15 |     7 | Filtración de Datos | Hacktivismo | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-16 |     7 | Filtración de Datos | Hacktivismo | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-17 |     7 | Filtración de Datos | Hacktivismo | Malware | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades
 2026-10-18 |     6 | Filtración de Datos | Hacktivismo | Malware | Phishing | Robo de Credenciales | Vulnerabilidades
(15 rows)
```

Esperado: idéntico. **PASS.**

---

## Q11 ALERTAS — PASS

```sql
SELECT
  canal,
  estado,
  count(*) AS n
FROM alertas
GROUP BY canal, estado
ORDER BY canal, estado;
```

Actual:

```text
  canal   |  estado   | n
----------+-----------+---
 telegram | PENDIENTE | 6
(1 row)
```

Esperado: idéntico. **PASS.**

---

## Q12 TOP POSTS POR CATEGORIA — PASS

```sql
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
```

Actual:

```text
       nlp_category        |   id    |                                                    titulo                                                    | score |   fecha    |                                                 url
---------------------------+---------+--------------------------------------------------------------------------------------------------------------+-------+------------+------------------------------------------------------------------------------------------------------
 Filtración de Datos       | 1x2vur9 | Guardar datos personales                                                                                     | 0.250 | 2026-10-11 | https://www.reddit.com/r/devsarg/comments/1x2vur9/guardar_datos_personales/
 Filtración de Datos       | 1x2kl6z | Consulta sobre monetizar APP Android y datos personales (Argentina)                                          | 0.250 | 2026-10-10 | https://www.reddit.com/r/devsarg/comments/1x2kl6z/consulta_sobre_monetizar_app_android_y_datos/
 Hacktivismo               | 1x42omu | hackearon el sitio oficial de la fundacion altos estudios en ciencias comerciales                            | 0.250 | 2026-10-12 | https://www.reddit.com/r/devsarg/comments/1x42omu/hackearon_el_sitio_oficial_de_la_fundacion_altos/
 Hacktivismo               | 1wsgqxi | Design behind OIDA, a nxc like CLI for OT/ICS assessments                                                    | 0.250 | 2026-09-28 | https://www.reddit.com/r/netsec/comments/1wsgqxi/design_behind_oida_a_nxc_like_cli_for_otics/
 Infraestructura y Ataques | 1wr7qwo | Sobre el sentido de aprender vs la IA                                                                        | 0.250 | 2026-09-27 | https://www.reddit.com/r/devsarg/comments/1wr7qwo/sobre_el_sentido_de_aprender_vs_la_ia/
 Infraestructura y Ataques | 1w8w0ou | Tengu, a Mirai-style Linux and IoT botnet                                                                    | 0.250 | 2026-09-06 | https://www.reddit.com/r/Malware/comments/1w8w0ou/tengu_a_miraistyle_linux_and_iot_botnet/
 Malware                   | 1x5iauj | ⚠️ URGENT WARNING: Fake "VRChat-DLSS5-Cam" GitHub repository is a dangerous Infostealer Malware (SmartLoader) | 1.000 | 2026-10-14 | https://www.reddit.com/r/Malware/comments/1x5iauj/urgent_warning_fake_vrchatdlss5cam_github/
 Malware                   | 1wwmtnr | Pre-installed C2 loader on cheap Android projectors - deploys proxy/ad-fraud botnets, can run arbitrary code | 1.000 | 2026-10-03 | https://www.reddit.com/r/Malware/comments/1wwmtnr/preinstalled_c2_loader_on_cheap_android/
 Phishing                  | 1x5pk5e | One Android Loader, Four Malicious APKs: Linking Challan and Gas Phishing to BTMOB                           | 0.250 | 2026-10-14 | https://www.reddit.com/r/Malware/comments/1x5pk5e/one_android_loader_four_malicious_apks_linking/
 Phishing                  | 1x5acdz | Recruiter de Brasil me pide e-mail y contraseña de LinkedIn para "optimizarme el perfil                      | 0.250 | 2026-10-13 | https://www.reddit.com/r/devsarg/comments/1x5acdz/recruiter_de_brasil_me_pide_email_y_contraseña_de/
 Ransomware                | 1wz2lr8 | IronChain Ransomware Threatens Businesses with Permanent Data Loss and Costly Downtime                       | 0.250 | 2026-10-06 | https://www.reddit.com/r/Malware/comments/1wz2lr8/ironchain_ransomware_threatens_businesses_with/
 Ransomware                | 1wcqfzm | SonicWall SMA1000 campaign: standalone Linux Impacket secretsdump deployed onto appliances (SHA-256 inside)  | 0.250 | 2026-09-10 | https://www.reddit.com/r/Malware/comments/1wcqfzm/sonicwall_sma1000_campaign_standalone_linux/
 Robo de Credenciales      | 1x6o056 | Usar ingeniera inversa para portear juegos de pc a Android es el futuro del gaming en celular? Yo lo hare.   | 0.250 | 2026-10-15 | https://www.reddit.com/r/devsarg/comments/1x6o056/usar_ingeniera_inversa_para_portear_juegos_de_pc/
 Robo de Credenciales      | 1wzchsp | Rockstar Games has now been compromised several different ways since 2018, and none of them were a zero-day  | 0.250 | 2026-10-06 | https://www.reddit.com/r/netsec/comments/1wzchsp/rockstar_games_has_now_been_compromised_several/
 Vulnerabilidades          | 1wtcs22 | Community Threat Notice: Citrix NetScaler ADC and NetScaler Gateway Vulnerabilities                          | 0.750 | 2026-09-29 | https://www.reddit.com/r/Malware/comments/1wtcs22/community_threat_notice_citrix_netscaler_adc_and/
 Vulnerabilidades          | 1wdo45j | CISA: WatchGuard RCE flaw now exploited in ransomware attacks                                                | 0.750 | 2026-09-11 | https://www.reddit.com/r/Malware/comments/1wdo45j/cisa_watchguard_rce_flaw_now_exploited_in/
(16 rows)
```

Esperado: mismos 16 registros, mismos `id`, `score`, `fecha`, `url`; los títulos
del `.txt` aparecen truncados por ancho de columna y coinciden con el truncamiento
de `psql`. **PASS.** (`fecha` es `created_utc::date` en UTC; con hora local la
primera fila cambiaría a 2026-10-10 y fallaría.)

---

## Q13 DISTRIBUCION DE SCORE — PASS

```sql
SELECT
  round(nlp_score::numeric, 2) AS score,
  count(*) AS n
FROM posts
WHERE created_utc < '2026-10-18 03:00:00+00'
  AND ingested_at < '2026-10-19 00:00:00+00'
GROUP BY 1
ORDER BY 1;
```

Actual:

```text
 score |  n
-------+-----
  0.00 | 554
  0.25 | 130
  0.50 |  26
  0.75 |   7
  1.00 |   7
(5 rows)
```

Esperado: idéntico. **PASS.**

---

## Q14 CATEGORIAS DISTINTAS EN VENTANA — PASS

```sql
SELECT
  nlp_category AS categoria,
  count(*) AS n
FROM posts
WHERE created_utc < '2026-10-18 03:00:00+00'
  AND ingested_at < '2026-10-19 00:00:00+00'
GROUP BY nlp_category
ORDER BY n DESC;
```

Actual:

```text
         categoria         |  n
---------------------------+-----
 No relevante              | 554
 Malware                   |  79
 Vulnerabilidades          |  61
 Phishing                  |  12
 Robo de Credenciales      |   5
 Filtración de Datos       |   4
 Ransomware                |   4
 Infraestructura y Ataques |   3
 Hacktivismo               |   2
(9 rows)
```

Esperado: idéntico. **PASS.**

---

## Q15 TRACK SECUNDARIO — PASS

```sql
SELECT
  count(*) AS n,
  min(ingested_at) AS desde,
  max(ingested_at) AS hasta
FROM posts
WHERE ingested_at >= '2026-10-19 00:00:00+00'
  AND ingested_at <  '2026-10-19 18:00:00+00';
```

Actual:

```text
 n  |             desde             |             hasta
----+-------------------------------+-------------------------------
 31 | 2026-10-19 16:53:41.054809+00 | 2026-10-19 17:18:19.823468+00
(1 row)
```

Esperado: idéntico. **PASS.**

Nota: sin el límite superior `< '2026-10-19 18:00:00+00'` la consulta devuelve
41 filas hoy, porque después del corte se persistieron 10 publicaciones más el
mismo 2026-10-19 (desde 18:31:14+00 hasta 22:02:18+00).

---

## Resumen

| Query | Estado |
|-------|--------|
| Q1 TOTALES | PASS |
| Q2 RANGO DE INGESTA VENTANA | PASS |
| Q3 POR SUBREDDIT | PASS |
| Q4 POR DIA (hora local) | PASS |
| Q5 TABLA 3 CATEGORIAS | PASS |
| Q6 LATENCIA | PASS |
| Q7 ANOMALIAS RESUMEN | PASS |
| Q8 ANOMALIAS POR CATEGORIA | PASS |
| Q9 DISPAROS DETALLE | PASS |
| Q10 CATEGORIAS EVALUADAS POR DIA | PASS |
| Q11 ALERTAS | PASS |
| Q12 TOP POSTS POR CATEGORIA | PASS |
| Q13 DISTRIBUCION DE SCORE | PASS |
| Q14 CATEGORIAS DISTINTAS EN VENTANA | PASS |
| Q15 TRACK SECUNDARIO | PASS |

**15/15 PASS. 0 FAIL.**
