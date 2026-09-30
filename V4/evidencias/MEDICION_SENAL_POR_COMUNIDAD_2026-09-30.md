# Medición de señal por comunidad

**Tarea**: grupo 8 del change `rediseno-diccionario-evaluacion` (8.1 a 8.8).
**Fecha de la medición**: 2026-09-30 18:51 (America/Argentina/Buenos_Aires).
**Clasificador**: `MIN_HITS = 1`, score `min(1, hits / 4)`, 210 términos en 9 categorías.
**Naturaleza de los datos**: **corrida de control técnico, no corpus de resultados.**

> Los datos que siguen provienen de la corrida de control del 2026-09-29/30, con
> el workflow inactivo y declarada como tal en la bitácora. **No son evidencia
> publicable.** La medición se repetirá sobre la ventana B5 oficial una vez que
> termine la recolección. Este documento existe para dejar registrado el método y
> el encuadre, no para reportar un resultado.

---

## 1. Qué se midió y con qué método (8.1)

Se midió la **tasa de señal por comunidad**: qué proporción de los posts de cada
subreddit recibe una categoría de amenaza en lugar de `No relevante`.

**Muestra**: censo completo. No es una muestra: son todos los posts con
`nlp_category IS NOT NULL` presentes en la base el 2026-09-30.

- `n` total = **520** posts
- posts con señal = **113**
- comunidades medidas = **5** (más la fila huérfana `r/derechogenial`, con 0 posts)

**Consulta** (ejecutada el 2026-09-30, reproducible tal cual):

```sql
SELECT s.display_name,
       COUNT(*)                                                  AS n_posts,
       COUNT(*) FILTER (WHERE p.nlp_category <> 'No relevante')  AS n_amenaza,
       ROUND(100.0 * COUNT(*) FILTER (WHERE p.nlp_category <> 'No relevante')
             / NULLIF(COUNT(*), 0), 1)                            AS pct_amenaza,
       MIN(p.ingested_at AT TIME ZONE 'America/Argentina/Buenos_Aires'),
       MAX(p.ingested_at AT TIME ZONE 'America/Argentina/Buenos_Aires'),
       MIN(p.created_utc::date), MAX(p.created_utc::date)
FROM posts p
JOIN subreddits s ON s.id = p.subreddit_id
WHERE p.nlp_category IS NOT NULL
GROUP BY s.display_name
ORDER BY n_amenaza DESC, s.display_name;
```

## 2. Resultado

| subreddit | n | señal | % señal | ingerido | publicado |
|---|---|---|---|---|---|
| r/Malware | 101 | 67 | **66,3 %** | 2026-09-30 | 2026-05-21 → 2026-09-30 |
| r/netsec | 102 | 41 | **40,2 %** | 2026-09-30 | 2026-08-19 → 2026-09-30 |
| r/DerechoGenial | 100 | 3 | **3,0 %** | 2026-09-29 | 2026-09-23 → 2026-09-30 |
| r/devsarg | 116 | 2 | **1,7 %** | 2026-09-29 → 2026-09-30 | 2026-09-25 → 2026-09-30 |
| r/argentina | 101 | 0 | **0,0 %** | 2026-09-29 | 2026-09-26 → 2026-09-30 |
| **total** | **520** | **113** | **21,7 %** | | |

Distribución de categorías de amenaza:

| subreddit | Malware | Vulns. | Phishing | Ransomware | Infra. | Robo de Cred. | Filtración |
|---|---|---|---|---|---|---|---|
| r/Malware | 50 | 7 | 4 | 3 | 2 | 1 | 0 |
| r/netsec | 5 | 32 | 2 | 0 | 0 | 1 | 1 |
| r/DerechoGenial | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| r/devsarg | 0 | 0 | 0 | 0 | 1 | 0 | 1 |

**Advertencia de comparabilidad**: los posts de `r/Malware` y `r/argentina` se
ingerieron el 2026-09-30 y los de `r/DerechoGenial` y `r/devsarg` el 2026-09-29.
Son corridas distintas, con day-stamping de Reddit distinto, y la ventana de
publicación cubierta no es la misma (`r/Malware` abarca cuatro meses,
`r/netsec` uno y medio, `r/DerechoGenial` cinco días). Las tasas **no son
estrictamente comparables entre sí**.

## 3. Qué mide esta tabla y qué no (8.2, 8.6)

Esta tabla **no mide el desempeño del clasificador**. Mide dos cosas
sumultáneamente y el diseño no permite separarlas:

1. **La capacidad del clasificador** para detectar amenazas.
2. **La temática de la comunidad**, que predetermina qué hay que detectar.

`r/Malware` es una comunidad dedicada al malware. Que dé 66,3 % dice más sobre el
contenido del subreddit que sobre el diccionario. `r/netsec` da 40,2 % y
`r/argentina` 0,0 % con **el mismo diccionario y el mismo algoritmo**: la
diferencia de 40 puntos entre ellas no se le puede atribuir al clasificador.

Por eso **la tasa de señal del corpus final no es una estimación de desempeño**
(8.6). El corpus se fijó **después** de medir estas comunidades, y dos de las
tres que lo integran —`r/Malware` y `r/netsec`— son precisamente las de tasa
alta. Reportar «el clasificador acierta el 66 %» sobre ese corpus sería circular:
se seleccionaron las comunidades donde más acierta.

El desempeño del clasificador se mide en otro lugar y con otro método: la
muestra de control etiquetada a mano, con `n = 50`, en
[`evaluacion_muestra_control_2026-09-30.md`](evaluacion_muestra_control_2026-09-30.md)
(F1 = 0,931). Son dos mediciones distintas y no deben mezclarse.

## 4. Por qué el corpus no se elige por tasa (8.3, D-6)

**Queda declarado y descartado**: seleccionar el corpus por su tasa de señal es
**sobreajuste**. El argumento es circular —se elige lo que el sistema ya
detecta bien, y luego se reporta que el sistema funciona— y además invalida
cualquier evaluación posterior, porque la evaluación se hace sobre el mismo
conjunto que se usó para elegir.

D-6 fija por eso el orden correcto: **se mide, se archiva la medición, y la
decisión de alcance se toma aparte, por criterio temático y no por rendimiento.**
Este documento es la medición archivada; la decisión de la sección 6 es de
alcance.

## 5. Opciones sometidas a los autores (8.4)

Se ponían a disposición de los autores y sus directores dos composiciones, con
la medición de la sección 2 a la vista:

| opción | composición | qué responde | qué no responde |
|---|---|---|---|
| **A — corpus monolítico de seguridad** | `r/Malware`, `r/netsec` | ¿el clasificador detecta amenazas? | ¿el método es viable en una comunidad técnica local, en castellano? |
| **B — corpus mixto** | `r/Malware`, `r/netsec`, `r/devsarg` | ambas preguntas | — |
| **C — comunidad general** | `r/argentina` u otra | volumen alto | nada útil: el tema no es seguridad |

La opción C quedó descartada por alcance antes de medir: el objeto del
proyecto es la seguridad de la información, no el monitoreo general.

## 6. Decisión registrada (8.5, D-9)

**Se adopta la opción B: corpus mixto.**

- **Qué**: `r/netsec`, `r/Malware`, `r/devsarg`.
- **Criterio**: dos comunidades cuyo tema declarado es la seguridad de la
  información (`r/netsec`, `r/Malware`) más una comunidad técnica argentina en
  castellano como referencia local (`r/devsarg`).
- **Fecha**: decisión de alcance el **2026-09-25**; implementada en la ingesta
  del **2026-09-29** (los tres subreddits pasaron a `active_monitoring = true`).
- **Responsables**: autores del proyecto (Valentino Lorca, Jerónimo Zúñiga,
  Enzo Severino), con sus directores.

**Estado verificado al 2026-09-30** (`SELECT id, display_name,
active_monitoring FROM subreddits ORDER BY display_name;`):

| subreddit | `active_monitoring` | posts históricos |
|---|---|---|
| r/argentina | false | 101 |
| r/derechogenial | **true** | **0** |
| r/DerechoGenial | false | 100 |
| r/devsarg | true | 116 |
| r/Malware | true | 101 |
| r/netsec | true | 102 |

**Dos anomalías registradas, sin ocultar:**

1. `r/derechogenial` figura con `active_monitoring = true` y **0 posts**. Es una
   fila huérfana: la ingesta no lee la tabla `subreddits`, el Code node
   `Prepare Subreddits` devuelve una lista fija de tres. El bitácora lo detecta
   como «4 de 3 esperados».
2. La distinción `r/derechogenial` / `r/DerechoGenial` en la tabla es **case-
   folding de `display_name` en el `ON CONFLICT`**, no dos comunidades. No
   son dos mediciones independientes.

## 7. Comunidades desactivadas: alcance, no tasa (8.7)

`r/argentina` y `r/DerechoGenial` se desactivan con `active_monitoring = false`
(D-9). **Se conservan sus 201 posts** (101 + 100), no se borra nada.

**El criterio aplicado fue temático, no de rendimiento**: ambos subreddits
tratan sobre política y derechos en Argentina, fuera del objeto declarado del
proyecto.

**Declaración explícita del riesgo de apariencia contradictoria**: esas dos
comunidades son también las de tasa más baja de la medición (3,0 % y 0,0 %).
Cualquier lector puede sospechar que se descartaron por eso. La razón por la que
se descarta esa lectura es de método: **la salida del propio clasificador no
puede usarse para justificar el corpus sobre el que se evalúa ese
clasificador.** Por eso el criterio declarado es el tema, y por eso la
medición se archiva separada de la decisión.

Hay además un contraejemplo dentro del propio corpus que apoya que el criterio
no fue la tasa: **`r/devsarg` entra con 1,7 %, la segunda tasa más baja de la
medición.** Si el criterio fuera el rendimiento, el corpus no la contendría.

## 8. Criterio de inclusión a priori (8.8)

Se declara el criterio, para que pueda auditarse contra el resultado:

1. **Tema declarado de seguridad de la información**, según la descripción
   pública del subreddit. No según su volumen, ni su tasa, ni su historial en la
   base.
2. **`r/devsarg` como comunidad técnica argentina de referencia**, incluida por
   ser técnica y local, no por su rendimiento.
3. **Criterio de exclusión**: la comunidad debe tratar el objeto del proyecto.
   Fuera de ese alcance, se desactiva sin calificar su señal.

La comunidad `r/devsarg` cumple el punto 2 y su tasa no participó en la decisión.
Es el caso que hace testeable el criterio: si el criterio fuera la tasa, el
corpus no la contendría.

## 9. Limitaciones declaradas

1. **Datos de prueba, no corpus de resultados.** Corrida de control del
   2026-09-29/30 con el workflow inactivo. La medición se repite sobre B5.
2. **Censo, no muestra aleatoria.** Los `n` por comunidad (101 a 116) son los
   posts disponibles en el feed, no una muestra con tamaño diseñado.
3. **Ventanas de publicación desiguales y solapadas.** Ver la advertencia de la
   sección 2.
4. **Clasificador distinto al de la decisión.** D-6 citaba `r/malware` 19 % y
   `r/devsarg` 0 %. Esas cifras **no son reproducibles hoy**: el umbral bajó de
   `MIN_HITS = 2` a `MIN_HITS = 1` (85 posts reclasificados) y el corpus creció.
   Las cifras de la sección 2 son las vigentes; las de D-6 quedan como registro
   histórico del momento de la decisión.
5. **Sesgo por rate limiting.** La cobertura por subreddit está sesgada y no se
   compensa (D-5). Ver
   [`CARACTERIZACION_RATE_LIMIT.md`](CARACTERIZACION_RATE_LIMIT.md).
6. **Sin Cohen's Kappa**: un solo anotador. La concordancia no es calculable y
   no se reporta.