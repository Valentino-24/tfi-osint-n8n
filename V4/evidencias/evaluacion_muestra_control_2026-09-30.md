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

Métricas medidas **contra el artefacto generado** (`B_workflow.json`), no contra una
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

### Falsos negativos que quedan

1. **EDR evasion** — inyección de procesos sin `WriteProcessMemory` (r/netsec)
2. **Red team sobre ServiceNow** — anatomía de un equipo rojo (r/netsec)

Ambos son falta de vocabulario real. **No se agregaron los términos**: definirlos sin
conocimiento técnico de ciberseguridad introduciría el mismo error conceptual
dentro del diccionario. Quedan como limitación abierta.

### Los 2 falsos positivos que quedan

| Canal | Modelo dijo | Título | Por qué no se corrige acá |
|---|---|---|---|
| r/Malware | Malware | Catálogo open-source de 2.800+ familias | Material de defensa; se tagged por la palabra "malware" repetida |
| r/DerechoGenial | Ingeniería Social | Suplantación de identidad en redes sociales | Fuera del ámbito del proyecto (infraestructura, no conflictos legales) |

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
- **Reconciliar el post `1umy56h`** ("Silent Swap", extensión clipper de cripto): la base lo guarda como `No relevante` con score 0, pero la lógica actual encuentra 2 hits y lo clasifica `Malware`. Sugiere que la ejecución que lo clasificó se diferencie del artefacto actual. Resolver antes de atribuir métricas definitivas a la ventana.
- **Reetiquetar las 89 clasificaciones** solo cuando el workflow vuelva a correr, si se quiere que la base refleje el clasificador nuevo.
