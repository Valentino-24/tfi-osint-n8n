# Latencia 5.3 — descomposición por estado del motor

**Fecha de corte:** 2026-10-17 (ventana B5 cerrada el 19/10)
**Generado:** 2026-10-22
**Uso:** respaldo de la sección 5.3 de la V5 y de la respuesta al hallazgo N-09.

## Por qué se rehace

La V4 informaba una latencia de 126,9 min de mediana y atribuía la causa al ciclo de 15 minutos,
afirmando que el «piso teórico del diseño» era de 15 a 17 minutos. Ambas cosas son incorrectas:
15 minutos es el período del ciclo (cota superior de la espera), y la mediana agregada está dominada
por el tiempo en que el motor no estaba ejecutándose.

## Universo

Publicaciones creadas dentro de la ventana y persistidas antes del corte:

```sql
-- 437 filas
SELECT count(*)
FROM posts
WHERE created_utc >= '2026-10-01 00:00-03'
  AND ingested_at  <  '2026-10-19 00:00-03';
```

## 1. Distribución agregada (reproduce la V4)

```sql
WITH x AS (
  SELECT EXTRACT(EPOCH FROM (ingested_at - created_utc))/60.0 AS lat
  FROM posts
  WHERE created_utc >= '2026-10-01 00:00-03'
    AND ingested_at  <  '2026-10-19 00:00-03'
)
SELECT count(*), min(lat),
       percentile_cont(0.5)  WITHIN GROUP (ORDER BY lat),
       percentile_cont(0.95) WITHIN GROUP (ORDER BY lat),
       max(lat)
FROM x;
```

| n | mín | mediana | P95 | máx | > 5 min |
|---:|---:|---:|---:|---:|---:|
| 437 | 0,3 | 126,9 | 1.376,2 | 7.020,2 | 398 (91,1 %) |

## 2. Registro de ejecuciones del motor

Fuente: `execution_entity` de la base SQLite de n8n (`/home/node/.n8n/database.sqlite`),
workflow `KkotjSD5uO4CXI4D`.

| Métrica | Valor |
|---|---|
| Ejecuciones conservadas (total) | 382 |
| Ejecuciones en la ventana | 361 |
| Cobertura temporal del registro | 05/10 a 18/10 |
| Estado | 100 % `success` |
| Modo | 336 `trigger`, 25 `manual` |
| Intervalo entre corridas | mediana 15,0 min; P95 19,3 min; máx 1.838,2 min |
| Intervalos en el rango esperado (< 20 min) | 342 de 360 |

Las ejecuciones anteriores al 05/10 no quedaron retenidas en la base del motor; por eso la
cobertura se verifica además con una fuente independiente (ver punto 3).

## 3. Verificación independiente con `ingested_at`

```sql
SELECT to_char(ingested_at AT TIME ZONE 'America/Argentina/Buenos_Aires','MM-DD') AS dia,
       min(to_char(ingested_at AT TIME ZONE 'America/Argentina/Buenos_Aires','HH24:MI')) AS primera,
       max(to_char(ingested_at AT TIME ZONE 'America/Argentina/Buenos_Aires','HH24:MI')) AS ultima
FROM posts
WHERE ingested_at >= '2026-10-01 00:00-03'
GROUP BY 1 ORDER BY 1;
```

En los 17 días con ingesta, la primera escritura ocurre entre las 11:54 y las 18:14, y la última
entre las 13:16 y las 23:47. **Ningún día registra actividad entre las 19:00 y las 12:00.**

Unión de intervalos entre corridas consecutivas (huecos menores a 20 min fusionados):

| Métrica | Valor |
|---|---|
| Intervalos de ejecución | 18 |
| Minutos en ejecución | 4.929 |
| Minutos del período | 25.920 |
| **Cobertura** | **19,0 %** |

## 4. Latencia según estado del motor

```python
# off = minutos del intervalo [created_utc, ingested_at] fuera de los intervalos de ejecución
# grupo "en ejecución": off <= 0,5 min
```

| Grupo | n | mín | mediana | P95 | máx | > 5 min | > 60 min |
|---|---:|---:|---:|---:|---:|---:|---:|
| En ejecución | 126 | 0,3 | 9,0 | 15,7 | 16,9 | 97 (77,0 %) | 0 |
| Detenido | 311 | 0,7 | 371,1 | 1.557,3 | 7.020,2 | 301 (96,8 %) | 254 |
| Total | 437 | 0,3 | 126,9 | 1.376,2 | 7.020,2 | 398 | 254 |

El grupo «en ejecución» no tiene **ninguna** observación por encima de 60 minutos y su máximo
es 16,9 min, consistente con un período de 15 min más la espera fija entre comunidades.

## 5. Por comunidad (solo creadas con el motor en ejecución)

| Comunidad | n | mediana | P95 | máx |
|---|---:|---:|---:|---:|
| r/devsarg | 105 | 9,3 | 15,7 | 16,9 |
| r/Malware | 8 | 9,4 | 15,2 | 15,8 |
| r/netsec | 13 | 7,1 | 13,6 | 13,8 |

## 6. Conclusiones registradas en la V5

1. El umbral de 5 minutos **no se cumple** y no se mueve.
2. El piso real es cercano a cero (mínimo observado 0,3 min); 15 min es el período y, por lo tanto,
   una cota superior de la espera de una publicación que aparece justo después de una consulta.
3. La espera esperada con período de 15 min y arribos uniformes es 7,5 min, coherente con la mediana
   de 9,0 min del grupo en ejecución.
4. El 71,2 % de las publicaciones se creó con el motor detenido; la operación cubrió el 19,0 % del
   período, en jornadas diurnas.
5. Ninguna de las 254 observaciones con más de una hora de espera pertenece al grupo en ejecución.

## Reproducibilidad

- `docker start tfi-postgres` (solo lectura sobre la base)
- `docker cp tfi-n8n:/home/node/.n8n/database.sqlite` (copia de la base del motor; el contenedor
  permanece detenido para no disparar ciclos nuevos)
- Scripts usados: `analiza_ejecuciones.py`, `latencia_apagado.py` (temporales, no versionados)
