# Diseño del muestreo para la validación V5 sobre el corpus B5

Sub-artefacto del bloqueante 2 (N-08) del change `reconstruccion-informe-v5`.

## Datos reales de B5 (del corte `2026-10-17`)

Fuente: `V4/evidencias/informe_v4_2026-10-19/consultas_corpus_b5.txt` (Q1–Q15). Ventana 724 posts, 31 del track secundario C-25 (fuera del corte). `comments` = 0.

| Estrato | Definición | N (población) |
|---|---|---|
| **Estrato 1 — positivos del clasificador** | Posts con `nlp_category <> 'No relevante'` | **170** |
| **Estrato 2 — negativos del clasificador** | Posts con `nlp_category = 'No relevante'` | **554** |
| **Total** | | **724** |

Distribución de los 170 positivos por categoría (Q5): Malware 79, Vulnerabilidades 61, Phishing 12, Robo de Credenciales 5, Filtración de Datos 4, Ransomware 4, Infraestructura y Ataques 3, Hacktivismo 2 = 170.

Por comunidad (Q3): devsarg 428 (59,12 %), netsec 150 (20,72 %), Malware 146 (20,17 %).

> **N₀ = 554.** Este es exactamente el dato que la V4 **no informaba** y que hacía inválida la estimación estratificada (N-08b). Publicarlo es parte de la corrección.

## El error que se corrige (N-08b, N-14 #9)

La V4 calculó la sensibilidad como si la muestra fuera aleatoria simple, mezclando el estrato censado (peso 1) con el sorteado (peso N₀/n₀). La fórmula correcta con pesos por estrato:

- **Precisión** = TP / (TP + FP) sobre el **censo de los 170** (denominador censado, sin ponderar).
- **Sensibilidad** = TP / (TP + w·k), con **k** = casos del estrato 2 sorteados que resultan amenaza real y **w = N₀/n₀ = 554/182**. No hay término aparte para los positivos del clasificador: los 170 están censados, sin incertidumbre de muestreo.
- **F1** derivado de ambas: F1 = 2·P·S/(P+S).

Con n₀ casos sorteados del estrato 2, cada caso negativo del clasificador que resulte amenaza real pesa w veces más que un caso del censo.

## Tamaño de muestra

Fórmula (proporción, 95 %): `n = z² · p(1−p) / e²`, con corrección por población finita `n_ajustado = n / (1 + (n−1)/N)` porque el estrato es acotado (N=554).

| Omisión esperada (p) | n simple (±5 pp) | n con FPC (N=554) |
|---|---|---|
| 9,1 % (la que informa la V4) | 127 | **104** |
| 15 % | 196 | **145** |
| 22,7 % (la que corresponde al «270») | 270 | **182** |

**Decisión de diseño**: dimensionar con la omisión **observada en el censo** (una vez etiquetados los 170, se conoce la tasa real de omisión del clasificador en el estrato positivo, que da una referencia). Mientras no se conozca, adoptar el escenario conservador **p = 22,7 % → n₀ = 182** (el más exigente de los tres). Si el tiempo aprieta, el mínimo defendible es n₀ = 104 con la omisión del 9,1 %, pero **debe declararse el supuesto**.

> Nota: la corrección por población finita es un refinamiento que la V4 no usó. Declararla mejora la solidez metodológica ante el tribunal.

## Procedimiento de sorteo reproducible

Objetivo: que cualquier tercero reproduzca exactamente la misma muestra (la V4 falló acá: `md5()` era código muerto, solo 8 de 50 filas reproducibles → N-08d).

```sql
-- Semilla declarada: 20261020 (fecha de la validación V5)
-- Orden estable por hash determinista del id + semilla.
SELECT id, title, selftext
FROM posts
WHERE nlp_category = 'No relevante'
  AND created_utc < '2026-10-18 03:00:00+00'      -- corte B5
  AND ingested_at   < (timestamptz '2026-10-19 00:00:00+00')  -- excluye track C-25
ORDER BY md5(id || '20261020')
LIMIT 182;
```

Reglas:
1. **Semilla fija y declarada** en el documento (`20261020`).
2. **`ORDER BY` determinista** (`md5`), no aleatorio del motor.
3. **Archivar la salida** de la consulta en un `.csv` con su `sha256`.
4. **Declarar el hash del archivo** de muestra en el informe (junto al del ZIP de evidencia).

El mismo procedimiento se aplica a la **submuestra común de 50** para el kappa: **25 casos del estrato 1 + 25 del estrato 2**, sorteados con semilla derivada (`20261020 + 1`), para que el kappa cubra ambas poblaciones y no solo los positivos del clasificador. Cada anotador recibe el mismo conjunto en **orden distinto** (semillas `+11` y `+12`).

## Diseño de la anotación (3 anotadores humanos)

### Submuestra común para el kappa — casos repetidos, a ciegas

- **50 casos** tomados de las 182 (o del total censado+muestreado), etiquetados **por los tres**, cada uno por separado.
- **Nadie ve `nlp_category` ni `nlp_score`** en la hoja. Sin la predicción del clasificador, la referencia es independiente.
- **Nadie se comunica entre sí** hasta cerrar su propia planilla.
- Se calcula **kappa de Fleiss** (3 anotadores) — más fuerte que el Cohen que pide el tribunal como mínimo.
- Objetivo: **κ ≥ 0,61** (acuerdo sustancial). Si κ < 0,61 → revisar la guía, re-etiquetar y documentar la iteración.

### Censo de los 170 + resto de la muestra

- El **censo de los 170** y los **182 de la muestra** los etiqueta el **autor 3** en una sola planilla (hoja completa de 352 casos), que incluye los 50 comunes.
- Los compañeros 1 y 2 etiquetan **solo los 50 comunes** en sus propias planillas.
- Los **desacuerdos** de la submuestra común se resuelven **por consenso de los tres**, registrado en `adjudicacion_v5.xlsx`; **nunca por un modelo de lenguaje**.

### Registro del consenso

`adjudicacion_v5.xlsx` (hoja «Adjudicacion») concentra **solo los casos con desacuerdo** entre los tres, con columnas `codigo_interno`, `titulo`, `etiqueta_anot1/2/3`, `etiqueta_final` y `motivo`. Lo genera el agente tras recibir las tres planillas; los autores completan `etiqueta_final` y `motivo` en la discusión. Si no hay consenso, se adopta la opción más conservadora (**No relevante**).

> **El agente (IA) no etiqueta ni arbitra.** El tribunal considera la asistencia de un LLM en el etiquetado un sesgo de circularidad (N-08c). El agente prepara la hoja, la guía, calcula kappa/IC y redacta.

## Formato de la hoja de etiquetado (a ciegas)

Archivo `muestra_v5_etiquetado` (`.csv` para trazabilidad y `.xlsx` para etiquetar), una fila por caso:

| Columna | Contenido |
|---|---|
| `codigo_interno` | C-001, C-002… (identificador ciego, sin relación con el id de plataforma) |
| `titulo` | Título del post |
| `texto` | Cuerpo (selftext), hasta 3000 caracteres |
| `comunidad` | r/devsarg / r/netsec / r/Malware (contexto público, no predicción) |
| `categoria_asignada` | **en blanco** — la llena el anotador (lista desplegable con las 10 categorías) |
| `comentario` | opcional (dudas, caso límite) |

**No incluye** `nlp_category`, `nlp_score`, el `id` de Reddit **ni el estrato de origen**. Excluir el estrato es deliberado: «estrato 1» equivale a «el clasificador dijo amenaza» y revelaría parcialmente la predicción. Además, el orden de presentación está **mezclado de forma determinista** para que la posición no revele el estrato. La correspondencia `codigo_interno ↔ id/estrato/nlp` vive en `muestra_v5_correspondencia.csv`, que solo usa el agente para el cálculo y que **no se publica** (resuelve a la vez N-10).

Versión para el kappa: **dos** copias de la submuestra de 50 (una por compañero: `..._anot1`, `..._anot2`), **en orden distinto**. El tercer anotador (autor 3) etiqueta la hoja completa, que contiene esos 50: sus etiquetas se extraen por `codigo_interno` y no requieren una planilla aparte.

Formato XLSX: encabezado fijo, filtros, texto con ajuste de línea, anchos por columna y validación de datos en `categoria_asignada`. El CSV se codifica en UTF-8 con BOM para que Excel no rompa los acentos.

## Guía de etiquetado (borrador a escribir)

Debe fijar, **antes** de etiquetar:
1. **Definición operativa de amenaza de ciberseguridad** para el trabajo.
2. **Las 10 categorías** con definición y 2–3 ejemplos límite cada una (base: Anexo C).
3. **Reglas de desempate**: post que toca dos categorías → la dominante; post ambiguo → «No relevante»; discusión administrativa o consulta personal → «No relevante».
4. **Casos calibrados**: 3–5 ejemplos resueltos (que **no** estén en la submuestra común, para no sesgar).
5. **Prohibición explícita** de consultar el clasificador.

## Cálculo (lo hace el agente)

1. **Kappa de Fleiss** sobre la submuestra de 50 → κ y su interpretación.
2. **Etiqueta final**: consenso de los tres.
3. **Matriz de confusión por estrato**: TP, FP (estrato 1); FN, TN (estrato 2).
4. **Estimadores**:
   - Precisión = TP/(TP+FP) — censada.
   - Sensibilidad = (TP + FN₁) / (TP + FN₁ + FN₂·w) con w = 554/n₀.
   - F1 → derivado.
   - **IC exactos** (Clopper-Pearson o Wilson) sobre cada estimador.
5. **Por comunidad/idioma**: precisión y FDR para r/devsarg vs r/netsec+r/Malware por separado.
6. **Matriz por categoría** (9 + «No relevante»).
7. **Conciliación Tabla 5.9 vs 4.4.1**: tabla de transición caso por caso de los 28 positivos anteriores.

## Cronograma

| Día | Actividad | Responsable |
|---|---|---|
| 1 | Guía + sorteo (semilla 20261020) + export XLSX (hoja completa + 2 planillas de 50) | agente |
| 1–2 | Etiquetado: autor 3 los 352; compañeros 1 y 2 los 50 comunes, a ciegas y por separado | los 3 autores |
| 2 | Cálculo de kappa de Fleiss; generación de `adjudicacion_v5.xlsx` con los desacuerdos. Si κ<0,61 → revisar guía y re-etiquetar | agente |
| 2–3 | Consenso de los desacuerdos, completando `etiqueta_final` y `motivo` | los 3 autores |
| 3–4 | Estimadores ponderados, IC, resultados por idioma, matriz por categoría | agente |
| 4 | Redacción de §3.3, §5.5, §7.4 | agente |

**Esfuerzo**: los 50 comunes ≈ 1–2 h por compañero; los 352 completos ≈ 4–6 h para el autor 3.

## Entregables de este sub-artefacto (ya generados)

| Archivo | Contenido |
|---|---|
| `muestra_v5_etiquetado.xlsx` / `.csv` | Hoja ciega completa (170 + 182 = 352 casos) |
| `muestra_v5_anot1.xlsx` / `.csv` | Submuestra de 50 (compañero 1) |
| `muestra_v5_anot2.xlsx` / `.csv` | Submuestra de 50 (compañero 2) |
| `muestra_v5_correspondencia.csv` | `codigo_interno ↔ id/estrato/nlp` (NO se publica) |
| `adjudicacion_v5.xlsx` | Plantilla de consenso (se completa tras las 3 planillas) |
| `guia_etiquetado_v5.md` | Guía de etiquetado |
| `sorteo_v5.py` | Script del sorteo reproducible (semilla, hashes) |
| `evaluar_v5.py` | Cálculo de kappa de Fleiss y generación de desacuerdos |
| `paquete_anotadores_v5.zip` | Paquete listo para enviar a los autores |

## Riesgos

| Riesgo | Mitigación |
|---|---|
| κ < 0,61 | Revisar guía, re-etiquetar, documentar la iteración |
| Tiempo insuficiente para 182 | Bajar a n₀ = 104 declarando el supuesto p = 9,1 % |
| Contagio entre anotadores | Órdenes distintos + sin comunicación + a ciegas |
| Sesgo del N₀ desconocido | Se conoce: N₀ = 554 (publicado) |
| Sesgo por conocer el estrato | `estrato_origen` excluido de la hoja; orden mezclado |
| El agente aparece como anotador | Prohibido por diseño; queda declarado |
