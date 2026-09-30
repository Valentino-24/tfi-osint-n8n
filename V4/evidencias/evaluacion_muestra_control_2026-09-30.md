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

Los tres de `r/DerechoGenial` quedan fuera por el **ámbito del proyecto**:采集 amenazas a infraestructura, no conflictos legales laborales entre personas. El de la giftcard se resolvió como posible error de configuración de la empresa, sin evidencia de ataque. El del catálogo es material de defensa: el sistema lo marcó solo por cantidad de apariciones de la palabra "malware".

## 5. Lectura de fondo

**Los 5 falsos negativos están en `r/Malware` y `r/netsec`, los canales que sí tienen amenazas.** Ninguno está en `r/devsarg` ni en `r/DerechoGenial`.

Consecuencia directa: **retirar esos dos canales de la recolección no modifica el recall**. Son 0 de 8 y 0 de 10 amenazas, y su valor actual es el de control negativo — el sistema descarta correctamente ruido real, 8 de 8 y 7 de 10.

El problema real está en otro lado: **el detector falla por cobertura de vocabulario**. Falla con términos técnicos en inglés (*stealer*, *clipper*, *privilege escalation*, *red team*) y con campañas descritas en segunda persona. Es un problema del diccionario, no de la selección de canales.

## 6. Qué sigue

- **6.5** — Verificar la no superposición con el corpus de resultados de B5, posible recién cuando la ventana termine de recolectar.
- Ampliar la muestra del estrato `No relevante` si se quiere publicar un recall con intervalo acotado.
- Decidir sobre `r/devsarg` y `r/DerechoGenial`: **bajar su frecuencia en vez de eliminarlos** conserva el control negativo sin gastar llamadas a Reddit.
