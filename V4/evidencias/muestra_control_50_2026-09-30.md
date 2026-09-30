# Muestra de control — 50 posts (tarea 6.2)

Generada el `2026-09-30` con `generar_muestra.py` (procedimiento en la sección 5). Solo lectura: **no se escribió nada en `tesi_osint`**.

## 1. Archivos

| Archivo | Quién lo usa | Contenido |
|---|---|---|
| `muestra_control_50_2026-09-30_POSTS.csv` | el anotador | Los 50 posts con texto legible. **Sin la predicción del clasificador**, para que la etiqueta no quede anclada a la respuesta del modelo. |
| `muestra_control_50_2026-09-30_RESPUESTA_MODELO.csv` | el cálculo de métricas | La categoría y el score que produjo el clasificador. **No se entrega al anotador hasta que termine.** |

Los dos están separados a propósito. Si el anotador ve la respuesta del modelo antes de decidir, la etiqueta deja de ser independiente y la métrica mide la concordancia con el modelo en vez del desempeño del modelo.

## 2. Procedimiento y su justificación

La población es de 501 posts clasificados. La distribución es muy desigual:

| Estrato | Población | En la muestra | Peso |
|---|---|---|---|
| Alguna categoría de amenaza | 28 | **28** (censo) | 1,00 |
| `No relevante` | 473 | **22** (sorteo) | 21,50 |
| **Total** | **501** | **50** | — |

**No se sortearon 50 al azar.** Un sorteo puro de la población habría dado cerca de **3 posts de amenaza**, porque el 94,4 % de la base cae en `No relevante`. Con 3 positivos la recall no es calculable: bastaría que uno estuviera mal para moverla un 33 %.

Por eso la muestra es **estratificada**: se tomaron los 28 posts con categoría de amenaza (censo del estrato, no sorteo) y se completaron con 22 sorteados de `No relevante`.

La columna `peso_muestreo` de la clave del modelo permite después estimar métricas **sobre la población real** y no solo sobre la muestra. Sin ponderar, las cifras de la estratificada no son representativas y no deben reportarse.

**Semilla declarada `20260930`**: la muestra es reproducible. Repetir el procedimiento da exactamente los mismos 50 posts.

## 3. Independencia respecto del corpus de resultados

La spec exige que la muestra **no** sea el mismo conjunto sobre el que se reportan métricas de la ventana.

Los 501 posts son anteriores al inicio formal de la ventana B5: la corrida del `2026-09-30` quedó registrada en la bitácora como **corrida de control técnico**, con el workflow inactivo y sin scheduler. El corpus de resultados de B5 se_armará con las corridas posteriores a esta muestra.

**Verificación:** la no superposición entre el conjunto de muestra y el corpus de resultados de la ventana solo podrá comprobarse cuando la ventana termine de recolectar. Está pendiente y anotada como tal.

## 4. Desviación declarada

La spec pide que **la muestra se sortee antes de ejecutar el clasificador sobre esos posts**, para que el sorteo no quede sesgado por el resultado.

No se pudo cumplir literalmente: el clasificador ya había corrido sobre los 501 posts antes de que existiera esta tarea. La garantía sustantiva **sí se conserva**: el sorteo es aleatorio y no está condicionado a la categoría del modelo. Se incluyen los 28posts de amenaza por estrato, no porque el modelo los haya marcado.

Lo que no puede garantizarse es la condición temporal. Queda declarado como desviación de la spec `muestra-control-etiquetada`.

## 5. Consulta y procedimiento

Población y estratos:

```sql
SELECT p.id, s.display_name, p.title, p.selftext, p.url, p.created_utc,
       p.score, p.num_comments, p.nlp_category, p.nlp_score,
       CASE WHEN p.nlp_category = 'No relevante'
            THEN 'no_relevante' ELSE 'amenaza' END AS estrato
FROM posts p
JOIN subreddits s ON s.id = p.subreddit_id
WHERE p.nlp_category IS NOT NULL;
```

Sorteo determinístico por subreddit, con la semilla declarada:

```sql
ORDER BY md5(p.id || '20260930')
```

## 6. Cómo etiquetar

1. Abrir `..._POSTS.csv` en Excel o un editor de texto. Está en `UTF-8 con BOM`, así que los acentos se ven bien en Excel.
2. Leer `titulo` y `cuerpo` de cada fila.
3. Elegir la categoría del diccionario de 9 que corresponde y anotarla en `categoria_humana`.
4. Poner tu nombre en `anotador` y la fecha en `etiquetado_el`.
5. Si tuviste dudas sobre un post, anotarlo en `notas`. **Un post dudoso no se descarta**: se etiqueta igual y se deja la duda registrada.

Las categorías permitidas están en `knowledge-base/04_modelo_de_datos.md`.

## 7. Lo que falta antes de cerrar

- **Tarea 6.1** sigue abierta: el criterio de qué cuenta como amenaza y qué cuenta como `No relevante` no está acordado con los autores y sus directores. Etiquetar sin ese acuerdo produce etiquetas que dependen de quién mire.
- **Coordenada por anotador.** La spec exige reportar el acuerdo entre anotadores (Cohen's Kappa). Con un solo anotador **no hay acuerdo que reportar** y esa cifra no puede presentarse como tal.
- **Tarea 6.4**: las etiquetas se persisten en un archivo versionable, con autor y fecha.
