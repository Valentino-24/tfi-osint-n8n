# Motor de anomalías — recálculo retrospectivo (N-11 / 6.2)

Fecha de generación: 2026-10-20. Base: `tesi_osint`, contenedor `tfi-postgres`. Solo consultas `SELECT`.
Ventana: publicaciones creadas del 01/10/2026 al 17/10/2026 (día local ART).

## 1. Consulta de conteos por `created_utc`

```sql
SELECT p.nlp_category AS categoria,
       to_char(p.created_utc AT TIME ZONE 'America/Argentina/Buenos_Aires','YYYY-MM-DD') AS dia,
       count(*) AS n
FROM posts p
WHERE p.created_utc >= '2026-10-01 00:00-03'
  AND p.created_utc <  '2026-10-18 00:00-03'
  AND p.nlp_category IS NOT NULL
  AND p.nlp_category <> 'No relevante'
GROUP BY 1,2 ORDER BY 2,1;
```

## 2. Criterios del recálculo

- **Base temporal:** `created_utc` (fecha de creación del contenido), no `ingested_at`.
- **Días excluidos de la línea base:** `2026-10-01` (carga inicial de 307 publicaciones) y `2026-10-03` (sin recolección).
- **Días de línea base:** 15 (2026-10-02 a 2026-10-17).
- **λ por categoría** = publicaciones de la categoría / días de línea base.
- **Umbral** `u = max(3, q95(λ) + 1)`, con `q95` el cuantil 0,95 de Poisson(λ).

## 3. Línea base y umbrales

| Categoría | Publicaciones 02–17/10 | λ | q95(λ) | u |
|---|---:|---:|---:|---:|
| Filtración de Datos | 2 | 0.133 | 1 | 3 |
| Hacktivismo | 1 | 0.067 | 1 | 3 |
| Malware | 21 | 1.400 | 4 | 5 |
| Phishing | 6 | 0.400 | 2 | 3 |
| Ransomware | 1 | 0.067 | 1 | 3 |
| Robo de Credenciales | 3 | 0.200 | 1 | 3 |
| Vulnerabilidades | 19 | 1.267 | 3 | 4 |

## 4. Conteos diarios por fecha de creación

| Día | Filtración d | Hacktivismo | Malware | Phishing | Ransomware | Robo de Cred | Vulnerabilid |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-10-01 *(carga inicial)* | 0 | 0 | 1 | 0 | 0 | 0 | 2 |
| 2026-10-02 | 0 | 0 | 0 | 1 | 0 | 0 | 2 |
| 2026-10-03 *(sin servicio)* | 0 | 0 | 4 | 0 | 0 | 0 | 1 |
| 2026-10-04 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| 2026-10-05 | 0 | 0 | 4 | 0 | 0 | 1 | 1 |
| 2026-10-06 | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| 2026-10-07 | 0 | 0 | 2 | 0 | 0 | 0 | 1 |
| 2026-10-08 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 2026-10-09 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 2026-10-10 | 2 | 0 | 0 | 0 | 0 | 0 | 1 |
| 2026-10-11 | 0 | 0 | 3 | 1 | 0 | 0 | 0 |
| 2026-10-12 | 0 | 1 | 1 | 1 | 0 | 0 | 3 |
| 2026-10-13 | 0 | 0 | 1 | 1 | 0 | 0 | 2 |
| 2026-10-14 | 0 | 0 | 2 | 1 | 0 | 0 | 2 |
| 2026-10-15 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 2026-10-16 | 0 | 0 | 2 | 0 | 0 | 0 | 3 |
| 2026-10-17 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |

## 5. Resultado

- Evaluaciones: **105** (15 días × 7 categorías).
- Disparos esperados bajo la hipótesis nula (Σ P(X ≥ u | λ)): **0.95**.
- Disparos observados con la serie corregida: **0**.
- Techo nominal de la regla: 5 % por evaluación → 5,25 disparos esperados en 105 evaluaciones.

## 6. Serie histórica del motor (por `ingested_at`), para contraste

```
 to_char |         categoria         | n_observado | base_media | umbral | disparo 
---------+---------------------------+-------------+------------+--------+---------
 10-02   | Filtración de Datos       |           2 |          0 |      3 | f
 10-02   | Infraestructura y Ataques |           3 |          0 |      3 | t
 10-02   | Malware                   |          55 |          0 |      3 | t
 10-02   | Phishing                  |           6 |          0 |      3 | t
 10-02   | Ransomware                |           3 |          0 |      3 | t
 10-02   | Robo de Credenciales      |           2 |          0 |      3 | f
 10-02   | Vulnerabilidades          |          41 |          0 |      3 | t
 10-05   | Filtración de Datos       |           0 |        0.2 |      3 | f
 10-05   | Hacktivismo               |           0 |          0 |      3 | f
 10-05   | Infraestructura y Ataques |           0 |        0.3 |      3 | f
 10-05   | Malware                   |           5 |        5.5 |     11 | f
 10-05   | Phishing                  |           1 |        0.7 |      3 | f
 10-05   | Ransomware                |           0 |        0.3 |      3 | f
 10-05   | Robo de Credenciales      |           0 |        0.2 |      3 | f
 10-05   | Vulnerabilidades          |           1 |        4.3 |      9 | f
 10-06   | Filtración de Datos       |           0 |        0.2 |      3 | f
 10-06   | Hacktivismo               |           1 |          0 |      3 | f
 10-06   | Infraestructura y Ataques |           0 |        0.3 |      3 | f
 10-06   | Malware                   |           2 |          6 |     11 | f
 10-06   | Phishing                  |           0 |        0.8 |      3 | f
 10-06   | Ransomware                |           0 |        0.3 |      3 | f
 10-06   | Robo de Credenciales      |           1 |        0.2 |      3 | f
 10-06   | Vulnerabilidades          |           1 |        4.4 |      9 | f
 10-07   | Filtración de Datos       |           0 |        0.2 |      3 | f
 10-07   | Hacktivismo               |           0 |        0.1 |      3 | f
 10-07   | Infraestructura y Ataques |           0 |        0.3 |      3 | f
 10-07   | Malware                   |           2 |        6.2 |     12 | f
 10-07   | Phishing                  |           0 |        0.8 |      3 | f
 10-07   | Ransomware                |           1 |        0.3 |      3 | f
 10-07   | Robo de Credenciales      |           1 |        0.3 |      3 | f
 10-07   | Vulnerabilidades          |           1 |        4.5 |      9 | f
 10-08   | Filtración de Datos       |           0 |        0.2 |      3 | f
 10-08   | Hacktivismo               |           0 |        0.1 |      3 | f
 10-08   | Infraestructura y Ataques |           0 |        0.3 |      3 | f
 10-08   | Malware                   |           2 |        6.4 |     12 | f
 10-08   | Phishing                  |           0 |        0.8 |      3 | f
 10-08   | Ransomware                |           0 |        0.4 |      3 | f
 10-08   | Robo de Credenciales      |           0 |        0.4 |      3 | f
 10-08   | Vulnerabilidades          |           1 |        4.6 |      9 | f
 10-09   | Filtración de Datos       |           0 |        0.2 |      3 | f
 10-09   | Hacktivismo               |           0 |        0.1 |      3 | f
 10-09   | Infraestructura y Ataques |           0 |        0.3 |      3 | f
 10-09   | Malware                   |           1 |        6.6 |     12 | f
 10-09   | Phishing                  |           0 |        0.8 |      3 | f
 10-09   | Ransomware                |           0 |        0.4 |      3 | f
 10-09   | Robo de Credenciales      |           0 |        0.4 |      3 | f
 10-09   | Vulnerabilidades          |           1 |        4.7 |     10 | f
 10-10   | Filtración de Datos       |           0 |        0.2 |      3 | f
 10-10   | Hacktivismo               |           0 |        0.1 |      3 | f
 10-10   | Infraestructura y Ataques |           0 |        0.3 |      3 | f
 10-10   | Malware                   |           1 |        6.7 |     12 | f
 10-10   | Phishing                  |           0 |        0.8 |      3 | f
 10-10   | Ransomware                |           0 |        0.4 |      3 | f
 10-10   | Robo de Credenciales      |           0 |        0.4 |      3 | f
 10-10   | Vulnerabilidades          |           1 |        4.8 |     10 | f
 10-11   | Filtración de Datos       |           1 |        0.2 |      3 | f
 10-11   | Hacktivismo               |           0 |        0.1 |      3 | f
 10-11   | Infraestructura y Ataques |           0 |        0.3 |      3 | f
 10-11   | Malware                   |           0 |        6.8 |     12 | f
 10-11   | Phishing                  |           0 |        0.8 |      3 | f
 10-11   | Ransomware                |           0 |        0.4 |      3 | f
 10-11   | Robo de Credenciales      |           0 |        0.4 |      3 | f
 10-11   | Vulnerabilidades          |           0 |        4.9 |     10 | f
 10-12   | Filtración de Datos       |           1 |        0.3 |      3 | f
 10-12   | Hacktivismo               |           0 |        0.1 |      3 | f
 10-12   | Infraestructura y Ataques |           0 |        0.3 |      3 | f
 10-12   | Malware                   |           2 |        6.8 |     12 | f
 10-12   | Phishing                  |           1 |        0.8 |      3 | f
 10-12   | Ransomware                |           0 |        0.4 |      3 | f
 10-12   | Robo de Credenciales      |           0 |        0.4 |      3 | f
 10-12   | Vulnerabilidades          |           0 |        4.9 |     10 | f
 10-13   | Filtración de Datos       |           0 |        0.2 |      3 | f
 10-13   | Hacktivismo               |           1 |        0.1 |      3 | f
 10-13   | Malware                   |           2 |        1.5 |      5 | f
 10-13   | Phishing                  |           1 |        0.3 |      3 | f
 10-13   | Ransomware                |           0 |        0.1 |      3 | f
 10-13   | Robo de Credenciales      |           0 |        0.2 |      3 | f
 10-13   | Vulnerabilidades          |           4 |        0.8 |      3 | t
 10-14   | Filtración de Datos       |           0 |        0.2 |      3 | f
 10-14   | Hacktivismo               |           0 |        0.2 |      3 | f
 10-14   | Malware                   |           1 |        1.7 |      5 | f
 10-14   | Phishing                  |           1 |        0.3 |      3 | f
 10-14   | Ransomware                |           0 |        0.1 |      3 | f
 10-14   | Robo de Credenciales      |           0 |        0.2 |      3 | f
 10-14   | Vulnerabilidades          |           2 |          1 |      4 | f
 10-15   | Filtración de Datos       |           0 |        0.2 |      3 | f
 10-15   | Hacktivismo               |           0 |        0.2 |      3 | f
 10-15   | Malware                   |           1 |        1.8 |      5 | f
 10-15   | Phishing                  |           1 |        0.4 |      3 | f
 10-15   | Ransomware                |           0 |        0.1 |      3 | f
 10-15   | Robo de Credenciales      |           0 |        0.2 |      3 | f
 10-15   | Vulnerabilidades          |           2 |        1.2 |      4 | f
 10-16   | Filtración de Datos       |           0 |        0.2 |      3 | f
 10-16   | Hacktivismo               |           0 |        0.2 |      3 | f
 10-16   | Malware                   |           1 |        1.4 |      5 | f
 10-16   | Phishing                  |           0 |        0.4 |      3 | f
 10-16   | Ransomware                |           0 |        0.1 |      3 | f
 10-16   | Robo de Credenciales      |           1 |        0.2 |      3 | f
 10-16   | Vulnerabilidades          |           1 |        1.3 |      4 | f
 10-17   | Filtración de Datos       |           0 |        0.2 |      3 | f
 10-17   | Hacktivismo               |           0 |        0.1 |      3 | f
 10-17   | Malware                   |           2 |        1.3 |      4 | f
 10-17   | Phishing                  |           0 |        0.4 |      3 | f
 10-17   | Ransomware                |           0 |        0.1 |      3 | f
 10-17   | Robo de Credenciales      |           0 |        0.2 |      3 | f
 10-17   | Vulnerabilidades          |           3 |        1.3 |      4 | f
 10-18   | Filtración de Datos       |           0 |        0.2 |      3 | f
 10-18   | Hacktivismo               |           0 |        0.1 |      3 | f
 10-18   | Malware                   |           2 |        1.3 |      4 | f
 10-18   | Phishing                  |           0 |        0.4 |      3 | f
 10-18   | Robo de Credenciales      |           0 |        0.1 |      3 | f
 10-18   | Vulnerabilidades          |           0 |        1.5 |      5 | f
(112 rows)

```

## 7. Interpretación

- Los **5 disparos del 02/10** corresponden a la carga inicial del 01/10 (55 publicaciones de Malware, 41 de Vulnerabilidades) evaluada con `base_media = 0`: son un artefacto de la puesta en marcha, no detecciones.
- El **disparo del 13/10** corresponde a la jornada del 12/10 y se produce porque la ventana móvil de diez días perdió el 01/10: la línea base cayó de 4,9 a 0,8 y el umbral de 10 a 3. La serie histórica muestra esa discontinuidad entre `10-12` (`base_media` 4,9) y `10-13` (`base_media` 0,8).
- Con `created_utc`, la jornada del 12/10 registra **3** publicaciones de Vulnerabilidades frente a un umbral de **4**: no dispara.
- **Referencia externa:** las tres publicaciones del 12/10 remiten a la cadena de RCE preautenticación en LG webOS, CVE-2026-91768 y un RCE premiado por Google. Son hechos verificables, pero `r/netsec` es 78,8 % Vulnerabilidades (52/66), de modo que tres en un día no constituye una jornada inusual.
- **Clasificación de OE5:** implementado; eficacia no demostrada.
