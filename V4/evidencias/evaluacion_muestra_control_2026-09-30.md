# Evaluación de la muestra de control — 2026-09-30

Muestra de `n=50` posts etiquetada a mano y contrastada contra la predicción del clasificador.

- **Etiquetas:** `muestra_control_50_2026-09-30_ETIQUETAS.csv`
- **Clave del modelo:** `muestra_control_50_2026-09-30_RESPUESTA_MODELO.csv` (entregada al anotador **después** de etiquetar)
- **Cálculo:** `V4/scripts/evaluar_muestra_control.py`, salida en `evaluacion_muestra_control_2026-09-30.json`
- **Anotador:** Enzo Severino · **Fecha:** 2026-09-30

## 1. Criterio de etiquetado (tarea 6.1, acordado)

> Cuenta como amenaza lo que **describe un ataque o campaña en curso, real y verificable**, aunque se publique como reporte. No cuenta el material puramente educativo, de prevención o catálogo.

Aplicado a los 50 posts, el criterio **no obligó a cambiar ninguna etiqueta**. Quedaron consistentes tanto los falsos negativos como el material preventivo que el sistema marcó como amenaza.

**Anotadores: 1. Cohen's Kappa no es calculable.** No hay acuerdo entre anotadores que reportar y esa cifra no puede presentarse como tal.

## 2. Matriz de confusión (detección de amenaza sí/no)

| | Modelo: amenaza | Modelo: no relevante |
|---|---|---|
| **Humano: amenaza** | **TP = 24** | **FN = 5** |
| **Humano: no relevante** | FP = 4 | TN = 17 |

- Precision: 24/28 = **0,857**
- Recall: 24/29 = **0,828**
- F1 = **0,842**
- Acierto exacto de categoría: 37/50 = **74,0 %**

## 3. Fiabilidad: por qué el recall no es publicable

La métrica que importa no es la de la tabla anterior. En el estrato que el modelo descartó como "No relevante", **5 de 22 posts eran amenazas reales**:

| | Valor |
|---|---|
| Amenazas ocultas | 5/22 = 22,7 % |
| **IC 95 %** | **[5,2 % , 40,2 %]** |
| Proyección a los 473 posts de ese estrato | **entre 25 y 190 amenazas no detectadas** |

El intervalo es tan ancho que **no permite afirmar una cifra de recall**. Con `n=50` el recall es un punto de partida, no una métrica de la ventana.

Para un intervalo de ±5 puntos en este estrato hacen falta aproximadamente **270 posts**. Con 50 no se cierra.

## 4. Concordancia por subreddit

| Canal | n | Amenazas (humano) | Amenazas (modelo) | Categoría exacta |
|---|---|---|---|---|
| r/netsec | 9 | 9 | 6 | 6 |
| r/Malware | 23 | 20 | 19 | 16 |
| r/devsarg | 8 | 0 | 0 | 8 |
| r/DerechoGenial | 10 | 0 | 3 | 7 |

### Los 5 falsos negativos

Amenazas reales que el sistema marcó `No relevante`:

1. **Ransomware** — correos falsos de "Interpol" sueltan ransomware sobre pymes (r/Malware)
2. **Malware** — extensión de navegador que secuestra transacciones cripto (r/Malware)
3. **Malware** — evasión de EDR por inyección de procesos sin `WriteProcessMemory` (r/netsec)
4. **Infraestructura y Ataques** — anatomía de un equipo rojo sobre ServiceNow (r/netsec)
5. **Vulnerabilidades** — escalada local de privilegios en CodeMeter (r/netsec)

### Los 4 falsos positivos

| Canal | Modelo dijo | Título |
|---|---|---|
| r/DerechoGenial | Phishing | Multinacional retiene mi sueldo |
| r/DerechoGenial | Phishing | Suplantación de identidad en redes sociales |
| r/DerechoGenial | Phishing | Me llegó una giftcard que no es mía |
| r/Malware | Malware | Catálogo open-source de 2.800+ familias |

Los tres de `r/DerechoGenial` quedan fuera por el **ámbito del proyecto**: se captan amenazas a infraestructura, no conflictos legales laborales entre personas. El de la giftcard se resolvió como posible error de configuración de la empresa, sin evidencia de ataque. El del catálogo es material de defensa: el sistema lo marcó solo por cantidad de apariciones de la palabra "malware".

## 5. Lectura de fondo

> **Corrección (2026-09-30, commit `b45e996`).** La versión original de esta sección
> atribuyó los 5 falsos negativos a "falta de cobertura de vocabulario". Al verificar
> el caso a mano **esa conclusión era incorrecta** y quedó reemplazada por la de abajo.
> Se conserva el texto original por trazabilidad del razonamiento.

**Texto original (incorrecto):** el detector fallaba por cobertura de vocabulario,
con términos técnicos en inglés (*stealer*, *clipper*, *privilege escalation*,
*red team*) y con campañas descritas en segunda persona.

**Diagnóstico corregido:** 4 de los 5 falsos negativos **no eran vocabulario ausente**,
sino el umbral `MIN_HITS=2` descartando señales obvias de una sola palabra. El caso
"correos falsos de Interpol sueltan ransomware" tiene `ransomware` en el **título**,
el término existe en el diccionario y matchea sin ambigüedad, y el post se iba a
`No relevante` por no alcanzar el segundo hit. Solo 2 de los 5 (EDR evasion, red
team) son realmente cobertura de vocabulario.

Moraleja metodológica: **antes de concluir que falta un término, hay que comprobar si
ya matchea y el umbral lo descarta.** Es un error de razonamiento fácil de cometer
porque la conclusión (el sistema falla) era correcta, pero la causa (el diccionario)
orientaba mal la corrección.

**Los falsos negativos están en `r/Malware` y `r/netsec`, los canales que sí tienen
amenazas.** Ninguno está en `r/devsarg` ni en `r/DerechoGenial`. Consecuencia directa:
**retirar esos dos canales de la recolección no modifica el recall**. Son 0 de 8 y
0 de 10 amenazas, y su valor actual es el de control negativo — el sistema descarta
correctamente ruido real.

## 5.b Corrección aplicada — `MIN_HITS=1` y salida de `dni` (commit `b45e996`)

Con el umbral en 2, el sistema perdía señales válidas por exigir una segunda
coincidencia. Se cambió `MIN_HITS` a 1 y se eliminó `'dni'` de `Filtración de Datos`,
que matcheaba con un post sobre baja de apoderado de jubilación (trámite
administrativo, no amenaza).

> ⚠️ **Tabla superada, conservada solo como registro del método.** Mide el artefacto
> generado pero aplica el diccionario al `selftext` completo de la base, que no es lo
> que el pipeline real clasifica. **No citar estas cifras.** Las que valen están en
> *Corrección posterior: cifras medidas contra el workflow real*.

Métricas calculadas **contra el artefacto generado** (`B_workflow.json`), no contra una
copia del diccionario en memoria, para que lo validado sea lo que se importa:

| | `MIN_HITS=2` (base) | `MIN_HITS=1` sin `dni` | Cambio |
|---|---|---|---|
| TP | 24 | **27** | +3 |
| FP | 4 | **2** | −2 |
| FN | 5 | **2** | −3 |
| TN | 17 | **19** | +2 |
| Precision | 0,857 | **0,931** | +0,074 |
| Recall | 0,828 | **0,931** | +0,103 |
| F1 | 0,842 | **0,931** | +0,089 |

La precisión mejora además porque salen 2 de los 4 falsos positivos: los tres de
`r/DerechoGenial` estaban casi todos en `Phishing`, que tiene un solo hit.

### Efecto sobre la base ya ingerida

Aplicado a los **501 posts** almacenados, el cambio reclasifica **89**: 86 pasan de
`No relevante` a amenaza y 3 salen de una categoría de amenaza. **No son posts mal
ingeridos**, son posts que el sistema ya había guardado mal y que ahora se corrigen:
el total de `No relevante` estaba inflado por el umbral, no por el contenido.

Estos cambios **no están aplicados en la base**: el surte efecto cuando el workflow
vuelva a ejecutarse. Las clasificaciones ya ingeridas no se tocan.

### Corrección posterior: cifras medidas contra el workflow real

> **Corrección (2026-09-30, commit posterior a `b45e996`).** La tabla de arriba salió de
> una **simulación** que aplicaba el diccionario al `selftext` completo almacenado.
> El pipeline real no clasifica ese texto: `Parse Reddit Posts` arma el texto con
> `d.title` + `d.contentSnippet`, y el `contentSnippet` del feed Atom es más corto y
> está recortado. Medir contra lo que el sistema **realmente guardó** da cifras distintas,
> y son estas las que valen:

| | `MIN_HITS=2` (base real) | `MIN_HITS=1` (medición real) | Cambio |
|---|---|---|---|
| TP | 24 | **27** | +3 |
| FP | 4 | **4** | 0 |
| FN | 5 | **2** | −3 |
| TN | 17 | **17** | 0 |
| Precision | 0,857 | **0,871** | +0,014 |
| Recall | 0,828 | **0,931** | +0,103 |
| F1 | 0,842 | **0,900** | +0,058 |
| Acierto exacto de categoría | 74,0 % | **80,0 %** | +6,0 pp |

**La simulación era optimista en la precisión (0,931 contra 0,871 real).** La razón es
que el recorte del `contentSnippet` cambia cuántos términos matchean, y con `MIN_HITS=1`
cada match de más convierte un `No relevante` en amenaza. El recall no cambia: 27/29 en
ambos casos, porque los 2 falsos negativos restantes son los mismos y no dependen de
longitud del texto.

La corrección neta de `MIN_HITS=1` es **recall +0,103 a cambio de +0,014 de precisión**.
El error que se corrige es sistemático y conocido (descarta señales de una palabra), y
el costo es acotado y conocido (tres posts de `r/DerechoGenial` fuera del ámbito del
proyecto).

### Clasificación heredada en el corpus archivado

`r/argentina` y `r/DerechoGenial` están desactivados (`active_monitoring = false`), así
que **el loop no los recorre y sus 201 posts nunca se reclasifican**. Auditoría sobre la
grilla de la fórmula vigente (`hits/4` → 0, 0.25, 0.5, 0.75, 1.0):

- **517 de 520 posts** tienen score en la grilla vigente.
- **3 posts de `r/DerechoGenial`** conservan `nlp_score = 0.2`, que no existe en la
  fórmula vigente: es el residuo de la fórmula anterior (`hits / |keywords|` = 2/10).

Su **categoría** sigue siendo correcta (Phishing, que es lo que el clasificador actual
también devuelve), pero el **score quedó desactualizado**. Cualquier statistic que use
`nlp_score` sobre el corpus completo debe excluir estos 3 posts o declararlos.

### Falsos negativos que quedan (medición real)

1. **EDR evasion** — inyección de procesos sin `WriteProcessMemory` (r/netsec), score 0.0
2. **Red team sobre ServiceNow** — anatomía de un equipo rojo (r/netsec), score 0.0

Ambos son falta de vocabulario real. **No se agregaron los términos**: definirlos sin
conocimiento técnico de ciberseguridad introduciría el mismo error conceptual
dentro del diccionario. Quedan como limitación abierta.

### Los 4 falsos positivos (medición real)

| Canal | Modelo dijo | Score | Título | Por qué no se corrige acá |
|---|---|---|---|---|
| r/DerechoGenial | Phishing | 0.2 | Multinacional retiene mi sueldo | Fuera del ámbito del proyecto |
| r/DerechoGenial | Phishing | 0.2 | Suplantación de identidad en redes sociales | Fuera del ámbito del proyecto |
| r/DerechoGenial | Phishing | 0.2 | Me llegó una giftcard que no es mía | Fuera del ámbito del proyecto |
| r/Malware | Malware | 0.5 | Catálogo open-source de 2.800+ familias | Material de defensa; matchea por la palabra "malware" repetida |

**Son los mismos 4 de la línea base.** La simulación previa predecía que quedarían 2;
se equivocó porque el recorte del `contentSnippet` deja a los tres de `r/DerechoGenial`
con un solo hit, suficiente bajo `MIN_HITS=1`. El error de fondo es conocido y está
declarado: son conflictos legales laborales, no amenazas a infraestructura.

Los tres de `r/DerechoGenial` **no fueron reclasificados por esta corrida**: el subreddit
está desactivado y el loop no lo recorre. Su `nlp_score = 0.2` es residuo de la fórmula
anterior (ver *Clasificación heredada en el corpus archivado*).

### Aciertos de detección con categoría distinta (no son FP ni FN)

Cuatro posts de `r/Malware` que el sistema detecta como amenaza —acierto de detección—
pero con otra categoría que la humana. No afectan la matriz binaria, sí la métrica de
acierto exacto de categoría (80,0 %):

| Título | Humano | Modelo |
|---|---|---|
| Redis cryptomining toolkit recovered from an open directory | Infraestructura y Ataques | Malware |
| Open directory held custom exploit tooling and an EtherHiding loader | Infraestructura y Ataques | Vulnerabilidades |
| Operation Endgame disrupted hundreds of systems (StealC backend) | Infraestructura y Ataques | Malware |
| They got the guy behind the Steam Malware attacks | Infraestructura y Ataques | Malware |

El patrón es consistente y **no es ruido**: el anotador tendió `Infraestructura y Ataques` para ataques cuyo toolchain el diccionario lleva a `Malware` o `Vulnerabilidades`. Es una diferencia de criterio entre la etiqueta humana y el diccionario sobre dónde corta la frontera entre "herramienta de ataque" y "infraestructura", no un defecto de cobertura. Queda declarada como ambigüedad de la taxonomía y no se corrige sin revisar el diccionario.


## 6. Limitaciones del método

Estas restricciones acotan lo que las cifras de arriba permiten afirmar. No las
corrige un mejor clasificador: son propiedades de cómo se construyó la muestra.

**6.1 Un solo anotador, asistido por herramientas y sin formación específica.**
El etiquetado lo hizo una sola persona (Enzo Severino), con recomendaciones de un
asistente de IA y **sin conocimiento formal de ciberseguridad**. En las categorías
donde el criterio depende de jerga técnica —distinguir un exploit real de una
descripción genérica de ataque — esa limitación puede haber producido etiquetas inconsistentes.
Es la principal fuente de error de esta evaluación, y no se puede cuantificar sin
un segundo anotador independiente.

**6.2 La muestra está condicionada por la predicción del modelo.**
Se estratificó usando la categoría que el clasificador ya había asignado: los 28 posts
predichos como amenaza (el estrato entero, no una submuestra) y 22 de los 473
predichos como `No relevante`. Por lo tanto **esta muestra no estima el rendimiento
sobre la población de forma directa**, sino dentro de estratos definidos por el
propio modelo evaluado. No debe describirse como un muestreo "no condicionado a la
categoría".

**6.3 El sorteo no es reproducible como está documentado.**
La documentación de la muestra afirma que el orden se obtiene con
`ORDER BY md5(...)` en SQL, pero `generar_muestra_control.py` mezcla en Python con
`random.Random(20260930)` sobre el orden de retorno de la consulta. Con la misma base
y la misma semilla el resultado se reproduce; ante un cambio en el plan de ejecución
de la consulta puede cambiar. Corregir antes de usar la muestra como referencia
reproducible.

**6.4 Sin evaluator externo ni revisão por pares.**
No hubo validación por un tercero. Para una tesis de facultad el control es empírico
y con fuentes, pero conviene declararlo en vez de presentarlo como validación formal.

**6.5 Sin análisis de concordancia.**
Cohen's Kappa no es calculable con un único anotador. Cualquier cifra de acuerdo
entre anotadores sería inventada.

## 7. Qué sigue

- **Tarea 6.5 (abierta)** — Verificar la no superposición con el corpus de resultados de B5, posible recién cuando la ventana termine de recolectar.
- **Agregar vocabulario para los 2 FN restantes** (`edr evasion`, `red team`) — requiere validación con criterio técnico, no con el criterio de alcance ya usado.
- **Ampliar la muestra del estrato `No relevante`** si se quiere publicar un recall con intervalo acotado.
- **Decidir sobre `r/devsarg` y `r/DerechoGenial`** — bajar su frecuencia en vez de eliminarlos conserva el control negativo sin gastar llamadas a Reddit.
- **Corregir la discrepancia de reproducibilidad** entre la documentación y `generar_muestra_control.py` (ver 6.3).
- ~~**Reconciliar el post `1umy56h`**~~ — **Resuelto el 2026-09-30.** La base ya lo guarda como `Malware` con score 0.25. La discrepancia previa tenía dos causas: la fila provenía de una ejecución con el artefacto anterior, y la lógica histórica comparaba contra `selftext` completo mientras el pipeline real usa `d.title + d.contentSnippet`, cuyo recorte deja un solo hit. Con la grilla vigente (`hits/4`) un hit da 0.25.
- **Excluir o reetiquetar los 3 posts de `r/DerechoGenial`** que conservan `nlp_score = 0.2`, residuo de la fórmula anterior (ver *Clasificación heredada en el corpus archivado*).
- **Backfill de los 201 posts de `r/argentina` y `r/DerechoGenial`** si se los quiere usar en estadísticas de `nlp_score`: al estar desactivados, el loop nunca los reclasificó.
