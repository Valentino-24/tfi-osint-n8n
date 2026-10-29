# Pulido editorial del informe V4 con Claude (navegador, plan gratuito)

Guía operativa para pulir la **prosa** de `V4/devoluciones/tesis_v4.md` con Claude en el navegador,
sin dañar la evidencia. El agente del repositorio hace la verificación y la regeneración del PDF.

---

## 1. Qué se le puede pedir y qué no

| Se le puede pedir a Claude | NO se le puede pedir (lo hace el agente) |
|---|---|
| Reescritura de prosa: oraciones largas, párrafos densos, repeticiones, concordancia, registro | Regenerar el PDF, los índices o las figuras |
| Consistencia terminológica **dentro de la prosa** | Cambiar cifras, tablas, rótulos o encabezados |
| Cohesión entre párrafos (conectores, orden de la información) | Agregar o quitar secciones, tablas, figuras o referencias |
| Títulos de sección *solo* si se acuerda antes | Recortar el documento para acortarlo |

**Por qué:** el informe está trazado contra 45 hallazgos del tribunal
(`V4/evidencias/informe_v4_2026-10-19/CHECKLIST_CORRECCIONES.md`) y cada cifra sale de una consulta
fechada (`consultas_corpus_b5.txt`). Una reescritura libre rompe esa trazabilidad y,
si toca números, invalida la evidencia. El pulido debe ser **de forma, nunca de contenido**.

**Archivo a subir:** `V4/devoluciones/tesis_v4.md` (161 KB, 1.152 líneas, 24.588 palabras).
Ya está en Markdown: **no hay que convertir nada**. Las 4 figuras están como enlaces a
`../figuras/*.png` y Claude no las verá: debe dejarlas intactas.

---

## 2. Modelo y esfuerzo

| Tarea | Modelo | Esfuerzo / thinking | Motivo |
|---|---|---|---|
| Pulido de prosa capítulo por capítulo | **Sonnet 5.5** | **High** (o thinking activado) | Es el modelo de mejor redacción disponible en el plan gratuito; el pulido exige sostener criterio de estilo en textos largos |
| Pasada final de consistencia entre capítulos | **Sonnet 5.5** | **Medium** | Tarea de control: comparar, no crear |
| Correcciones mecánicas (comillas, guiones, espacios) | Sonnet 5.5 o **Haiku 5.5** | **Low**, sin thinking | Es trabajo de sustitución, no de criterio |

- En el **plan gratuito** el selector ofrece **Sonnet** y **Haiku** de la familia 5.5; **Opus está en los planes pagos**. No hay cupo fijo: la ventana es móvil (~5 h), así que conviene trabajar por capítulos y **exportar la respuesta a un archivo** después de cada uno, para no depender de la conversación.
- **No usar Haiku para redactar**: en prosa larga deriva el registro.
- Los nombres exactos de los niveles de esfuerzo pueden variar en la UI; lo que importa es la regla: **criterio de estilo → High; control y mecánica → Low/Medium**.

---

## 3. Metodología (5 pasos)

```text
0. Sonda      → 1 párrafo difícil: calibrar el estilo de salida antes de invertir cupo
1. Hoja de estilo y reglas → mensaje fijo que se repite en cada capítulo
2. Capítulo por capítulo   → N mensajes, uno por capítulo, respuesta con delimitadores
3. Changelog por capítulo  → junto con el texto, la lista de cambios aplicados
4. Verificación del agente → ./V4/scripts/verificar_pulido.py (invariantes) + reconstrucción del PDF
```

**Regla de oro:** una respuesta = **un capítulo**, devuelto entre marcas fijas. Nunca "reescribí todo el
informe": a esa escala el modelo resume, omite y cambia cifras sin avisar.

**Cupo:** cada capítulo ronda las 2.000–5.000 palabras (el Capítulo 5 tiene 4.956). Un capítulo por
mensaje, con `High`, es una unidad de trabajo razonable para la ventana móvil. Si el capítulo queda
cortado, pedir "continuá desde la oración X" en el mensaje siguiente.

**Criterio de parada:** si Claude devuelve cambios que tocan cifras, tablas o encabezados, se descarta
la respuesta y se repite el mensaje con el recordatorio de reglas.

---

## 4. Prompts (copiar y pegar)

### 4.0 Sonda de calibración

```text
Sos editor técnico de un informe académico en español rioplatense, registro formal e impersonal.
Te paso un párrafo de un informe de ingeniería. Reescribilo para que sea más claro y fluido, sin
cambiar ni una cifra, ni un nombre propio, ni el sentido de ninguna afirmación, y sin agregar
información que no esté.

Pedido: devolveme (1) el párrafo reescrito y (2) una lista con los cambios que aplicaste y por qué.

PÁRRAFO:
<pegar acá el párrafo de la línea 883 de tesis_v4.md>
```

Sirve para medir cuánto "inventa" el modelo antes de darle el informe completo.

### 4.1 Reglas del juego (mensaje fijo, se repite en cada capítulo)

```text
Vas a editar un capítulo de un informe académico ya evaluado. Es una corrección de forma.

REGLAS INVIOLABLES
1. No cambies ninguna cifra, unidad, fecha, porcentaje ni intervalo de confianza.
2. No cambies rótulos de tablas ni de figuras ("Tabla 5.9.", "Figura 2."), ni los epígrafes.
3. No cambies los encabezados (líneas que empiezan con #, ## o ###), ni su orden.
4. No toques las filas de las tablas (líneas que empiezan con |) ni los enlaces de las figuras.
5. No agregues ni quites secciones, tablas, figuras, referencias ni citas en línea.
6. No agregues información, ejemplos, comparaciones ni matices que no estén en el texto original.
7. No recortes contenido para acortar: el documento puede crecer o reducirse como máximo un 10 %.
8. Conservá el español rioplatense, el registro formal y la voz impersonal (sin "yo", sin "nosotros"
   en primera persona de autor).
9. Conservá las comillas angulares «», la coma decimal (0,931) y el espacio antes del signo
   porcentual (80 %). No los "normalices".
10. No cambies los términos técnicos establecidos: workflow, n8n, subreddit, clasificador,
    etiquetado, HMAC-SHA-256. No los traduzcas ni los alternes con sinónimos.

QUÉ SÍ QUIERO
- Oraciones de más de 45 palabras: partirlas en dos o tres, sin perder matices ni relaciones
  lógicas (causa, contraste, condición).
- Párrafos de más de 150 palabras: dividirlos en unidades con una idea cada uno.
- Repeticiones léxicas cercanas, concordancia y régimen preposicional.
- Cohesión: que el lector sepa al empezar cada párrafo de qué se está hablando.
- Precisión: reemplazar vaguedades ("diversos", "variados", "muy") por lo que el texto ya dice.

FORMATO DE RESPUESTA
Devolveme, en este orden y sin comentarios extra:
(a) el changelog: lista numerada de cambios, cada uno con la ubicación aproximada y el motivo;
(b) el capítulo completo reescrito, entre las marcas exactas:
<<<CAPITULO
...texto...
CAPITULO>>>
Conservá el texto íntegro: nada de "el resto queda igual".
```

### 4.2 Un mensaje por capítulo

```text
Capítulo N. Objetivos de este pasaje, medidos sobre el original:
- X oraciones de 45 o más palabras (las peores: las de las líneas ...);
- Y párrafos de 150 o más palabras;
- además: <lo que hayas notado al leer>.
Aplicá las reglas del mensaje anterior y devolvé el capítulo completo reescrito.
Rango: desde la línea "# CAPÍTULO N: ..." hasta la línea anterior al capítulo siguiente.
```

### 4.3 Control final de invariantes (después del último capítulo)

```text
Tarea de control, sin reescribir nada. Te paso el capítulo original y tu versión pulida.
Comparálos y decime, en forma de tabla, si tu versión:
1. conserva todos los números del original (listá cualquier diferencia);
2. conserva todos los rótulos de tabla y figura;
3. conserva los encabezados y su orden;
4. conserva la cantidad de filas de cada tabla;
5. conserva los enlaces de las figuras.
Si encontrás una diferencia, marcá si fue deliberada o un error.
```

---

## 5. Hoja de estilo del informe (decisiones ya tomadas, no las cambies)

| Tema | Decisión vigente en la V4 |
|---|---|
| Comillas | Angulares « » (32 apariciones). Las rectas solo aparecen en una celda de tabla, dentro de un nombre de configuración |
| Porcentajes | Número, espacio, signo: `80 %` (124 casos) |
| Decimales y miles | Coma decimal (`0,931`), punto de miles (`1.376,2`) |
| Guion | Raya (—) para incisos; guion medio (–) solo en rangos (`Anexos A–D`) |
| `workflow`, `n8n`, `subreddit` | Se mantienen en el original, sin traducir; `Reddit` capitalizado como nombre propio |
| Referencias | APA 7, 15 entradas, todas citadas |
| Voz | Impersonal; los autores solo en la declaración de autoría |
| Tablas | 22, numeradas `Tabla X.Y.`; figuras 4, `Figura N.` |

---

## 6. Verificación obligatoria después de cada capítulo (la hace el agente)

```powershell
python V4\scripts\verificar_pulido.py V4\devoluciones\tesis_v4.md <copia_pulida>.md
```

Comprueba, contra el original: multiconjunto de **números**, **rótulos** de tabla y figura,
**encabezados**, **filas de tabla**, **referencias**, **citas** y **variación de extensión**.
Si algo falla, se descarta el capítulo y se repite el mensaje.

Al cerrar el pulido, el agente regenera el PDF (`V4/scripts/convertir_pdf.py`) y vuelve a verificar
los 36 números de los índices: **el pulido cambia la paginación**, y un informe entregado con índices
desfasados es peor que un informe con algunas oraciones largas.

---

## 7. Diagnóstico medido del original (2026-10-19)

| Sección | Palabras |
|---|---|
| Portada y front matter | 640 |
| Resumen / Abstract | 482 / 407 |
| Capítulo 1 | 2.389 |
| Capítulo 2 | 2.284 |
| Capítulo 3 | 2.304 |
| Capítulo 4 | 3.984 |
| Capítulo 5 | 4.956 |
| Capítulo 6 | 2.107 |
| Capítulo 7 | 1.888 |
| Capítulo 8 | 944 |
| Referencias y anexos | 2.203 |
| **Total** | **24.588** |

Estado mecánico: **limpio**. O tildes faltantes, 0 espacios antes de coma, 0 palabras duplicadas,
0 viñetas inconsistentes. Lo que queda por pulir es densidad: **55 oraciones de 45+ palabras** y
**14 párrafos de 150+ palabras** (los peores, de 270, 232 y 204 palabras).

---

## 8. Lista de trabajo por capítulo (usar en el mensaje 4.2)

Medición del 2026-10-19 sobre `V4/devoluciones/tesis_v4.md`. Las líneas son del original.

| Sección | Palabras | Oraciones 45+ | Párrafos 150+ | Peor oración | Peor párrafo |
|---|---:|---:|---:|---|---|
| Front matter (portada, índices, siglas) | 425 | 1 | 0 | L63 (87 pal.) | — |
| RESUMEN | 482 | 3 | 0 | L75 (75 pal.) | — |
| ABSTRACT | 407 | 2 | 0 | L87 (67 pal.) | — |
| Capítulo 1 | 1.835 | 10 | 1 | L125 (71 pal.) | L111 (151 pal.) |
| Capítulo 2 | 2.284 | 12 | 1 | L240 (68 pal.) | L240 (270 pal.) |
| Capítulo 3 | 2.154 | 11 | 1 | L282 (80 pal.) | L322 (161 pal.) |
| Capítulo 4 | 3.354 | 18 | 4 | L416 (77 pal.) | L481 (232 pal.) |
| Capítulo 5 | 3.320 | 11 | 3 | L599 (58 pal.) | L599 (166 pal.) |
| Capítulo 6 | 1.941 | 10 | 1 | L816 (71 pal.) | L756 (168 pal.) |
| Capítulo 7 | 1.512 | 9 | 2 | L871 (168 pal.) | L871 (204 pal.) |
| Capítulo 8 | 676 | 3 | 0 | L925 (91 pal.) | — |
| Referencias | 372 | 0 | 0 | — | — |
| Anexos | 1.070 | 0 | 0 | — | — |

Orden sugerido de trabajo (de mayor a menor rendimiento): **4 → 2 → 5 → 3 → 6 → 7 → 1 → 8**,
y dejar Resumen/Abstract para el final, cuando el estilo de los capítulos ya esté asentado.
Las tres peores oraciones del informe (168, 110 y 102 palabras) están todas en el Capítulo 7,
y el peor párrafo del Capítulo 2 (270 palabras) es una lista de herramientas que probablemente
convenga conservar como bloque: en ese caso, el objetivo es partirlo en tres párrafos, no resumirlo.

---
