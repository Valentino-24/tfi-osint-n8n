# Conversión de `tesis_v4.md` a PDF — prompt para Claude y elección de modelo

Documento operativo para el autor. No forma parte del informe que se entrega al tribunal.

- Entrada: `V4/devoluciones/tesis_v4.md` (164.600 bytes, 1.151 líneas, UTF-8 sin BOM).
- Estructura que la conversión debe preservar: 13 encabezados de nivel 1 y 46 de nivel 2, **22 tablas** numeradas, **4 figuras** referenciadas como `../figuras/…png`, índices manuales (general, de tablas, de figuras), siglas, Resumen, Abstract, Referencias y Anexos A–D.
- Salida esperada: un PDF A4, 12 pt, interlineado 1,5, texto justificado, numeración de páginas, índice con números de página y sin alterar una sola palabra del contenido.

---

## 1. Preparación (una sola vez, antes de abrir Claude)

1. Abrí un chat **nuevo** y elegí el modelo y el esfuerzo según la sección 4.
2. Adjuntá el archivo `V4/devoluciones/tesis_v4.md`.
3. Pegá el prompt de la sección 2 **en el mismo mensaje** en el que adjuntás el archivo.
4. No pidas "arreglos" ni "mejoras" del texto. Cada turno extra consume la ventana de uso del plan gratuito y, además, el informe ya está cerrado y auditado.

---

## 2. Prompt principal (copiar tal cual, con el archivo adjunto)

```text
Actuá como ingeniero de publicación técnica. Te adjunto un informe de tesis completo en
Markdown (UTF-8, español de Argentina, unas 20.000 palabras). NO lo reescribas, no lo
resumas, no corrijas su redacción y no cambies ninguna cifra: ese documento ya fue
auditado y aprobado por los autores. Tu única tarea es darme la receta para convertirlo
en un PDF de calidad de imprenta, sin pérdida de contenido.

CONTEXTO DEL DOCUMENTO
- Portada con título, universidad, carrera, autores y directores; nota de versión como
  cita en bloque; declaración de autoría.
- Índices escritos a mano: "Índice general", "Índice de tablas" (22 entradas), "Índice de
  figuras" (4 entradas), y una tabla de siglas.
- Cuerpo: encabezados `#` de capítulo (numerados a mano: "1. Introducción", "2. ...", ...,
  "9. Referencias bibliográficas", "10. Anexos A–D") y encabezados `##` de sección
  (numerados a mano: "5.3 ..."). La numeración viene escrita en el texto, no debe
  regenerarse ni duplicarse.
- Tablas en sintaxis de barras de Markdown (pipe tables), con ancho variable: hay tablas
  de 2 y de 6 columnas y algunas con celdas largas.
- Figuras con rutas relativas: `![Figura N. Epígrafe](../figuras/Figura_N_xxx.png)`. El
  script debe resolver esa ruta contra la ubicación del Markdown y verificar que cada
  archivo exista; el epígrafe va debajo de la imagen, numerado como ya está escrito.
- Énfasis, código en línea, y referencias bibliográficas en APA 7 dentro del texto
  (por ejemplo "(Russell y Klassen, 2019)"). No hay notas al pie ni fórmulas.

REQUISITOS DEL PDF
1. A4, márgenes 25 mm arriba/abajo e izquierda 30 mm / derecha 20 mm, cuerpo de 12 pt con
   interlineado 1,5, texto justificado, sans o serif legible, títulos jerarquizados.
2. Numeración de páginas en el pie, con la portada sin número.
3. El "Índice general", el "Índice de tablas" y el "Índice de figuras" deben quedar con
   sus números de página reales. Si la herramienta elegida no puede calcularlos
   automáticamente, decime explícitamente cómo obtenerlos y cómo reinyectarlos.
4. Las 22 tablas y las 4 figuras deben quedar rotuladas ("Tabla 5.1. ..." y "Figura 1. ...")
   y en lo posible no cortarse entre páginas.
5. Saltos de página antes de cada capítulo de nivel 1.
6. Ninguna celda truncada, ningún texto invisible, ninguna imagen faltante, ningún
   encabezado huérfano al final de página.

ENTORNO REAL DE EJECUCIÓN (importante: no propongas algo que no se pueda instalar)
- Windows 11, PowerShell 5.1, sin permisos de administrador garantizados.
- Instalado y verificado: pandoc 3.8, Python 3.11 (con matplotlib y Jinja2), Node.js,
  Microsoft Edge.
- NO está instalado: ninguna distribución de LaTeX (ni pdflatex, ni xelatex, ni lualatex),
  ni LibreOffice, ni wkhtmltopdf, ni los paquetes de Python `python-docx`, `weasyprint`,
  `markdown`, `markdown-pdf` ni `pypandoc`.
- No sé si hay Microsoft Word instalado. Si tu propuesta más confiable depende de Word,
  decilo y dame en paralelo una alternativa que funcione sin Office.

QUÉ QUIERO QUE ME DEVUELVAS, en este orden y sin rodeos
1. La ruta recomendada, en una frase, y por qué esa y no las otras dos (descartá
   explícitamente las alternativas que fallen por dependencias en Windows).
2. Los comandos exactos de instalación de todo lo que falte y el tamaño aproximado de la
   descarga (si algo pesa más de 200 MB, decilo y ofrecé la variante liviana).
3. Un único script en Python, `convertir_pdf.py`, completo y ejecutable, que:
   a. reciba la ruta del Markdown como argumento (por defecto `V4/devoluciones/tesis_v4.md`);
   b. resuelva las rutas de las figuras y aborte con un mensaje claro si falta alguna;
   c. genere los archivos intermedios en una subcarpeta `V4/devoluciones/build/` sin
      tocar el Markdown original;
   d. produzca el PDF final en `V4/devoluciones/tesis_v4.pdf`;
   e. imprima al terminar un resumen con la cantidad de tablas, figuras y encabezados
      procesados, para poder comparar contra 22, 4 y 13 + 46.
   e2. use solo la biblioteca estándar más lo instalado en el punto 2;
   f. si hace falta una hoja de estilos o plantilla, que la escriba el propio script.
4. El bloque completo de CSS (si la ruta es HTML/WeasyPrint) o de LaTeX (si es LaTeX) o las
   instrucciones de estilo de Word, con los valores exactos de márgenes, tipografía,
   interlineado y saltos de página.
5. Una lista de verificación de diez puntos para comparar el PDF generado contra el
   Markdown, con la instrucción concreta de qué buscar en cada punto (por ejemplo: "contar
   las tablas rotuladas en el PDF y comparar con las 22 entradas del índice de tablas").
6. Los tres errores más probables de esta conversión en Windows y cómo detectarlos.

No me des el texto del informe ni fragmentos de él: solo la receta, el script y la
plantilla. Si algo de lo que pido es imposible con este entorno, decilo en la primera
línea en lugar de inventar una solución que no corra.
```

---

## 3. Prompt de verificación (segundo turno, opcional y barato)

Úsalo solo si el PDF ya está generado y querés una segunda opinión sobre la fidelidad. Adjuntá el PDF y el Markdown.

```text
Te adjunto dos versiones del mismo documento: el Markdown original y el PDF generado a
partir de él. Compará y respondeme con una tabla de una sola columna de estado por fila,
usando OK / DIFERENCIA / FALTANTE, para estos diez ítems: (1) cantidad de tablas rotuladas,
(2) cantidad de figuras y que ninguna esté en blanco, (3) los 13 títulos de nivel 1, (4) que
el índice general tenga números de página, (5) que los índices de tablas y figuras tengan
página, (6) que la numeración de secciones coincida con la del Markdown y no esté duplicada,
(7) que no haya texto cortado en celdas, (8) que las cifras del Resumen coincidan con las
del Markdown, (9) que las Referencias conserven las 15 entradas, (10) que los Anexos A–D
estén presentes. No comentes el contenido del trabajo ni su calidad académica: solo la
fidelidad de la conversión. Al final, listá únicamente las diferencias que requieran acción.
```

---

## 4. Qué modelo y qué esfuerzo elegir en el plan gratuito

Estado de la oferta al 19/10/2026, según la documentación de Anthropic y sus notas de versión:

- La familia vigente es la **5.5**: `Opus 5.5` (22/09/2026), `Sonnet 5.5` (28/09/2026) y `Haiku 5.5` (07/10/2026). Todos con 1 M de contexto, 128 K de salida máxima y *thinking* adaptativo.
- El **plan gratuito incluye la familia Sonnet y la familia Haiku**. `Opus`, `Fable`, `Claude Code` y `Research` requieren plan pago.
- El **control de esfuerzo** (`low`, `medium`, `high`; `xhigh`/“Extra” en algunos modelos) está en el selector de modelo. En las aplicaciones, `Sonnet 5.5` y `Opus 5.5` arrancan en **medium**; en la API el valor por defecto es `high`.
- `Haiku 4.5` sale del selector el **29/10/2026** y lo reemplaza `Haiku 5.5`.
- El plan gratuito no tiene cupo fijo de mensajes: se consume por **ventana móvil de 5 horas**, y los archivos adjuntos largos y las conversaciones largas lo consumen más rápido.

**Recomendación para esta tarea:**

| Situación | Modelo | Esfuerzo | Por qué |
|---|---|---|---|
| Primera opción | **Sonnet 5.5** | **High** | Es trabajo estructural y determinista —plantilla, script, manejo de rutas y tablas—, no requiere el razonamiento abierto de `xhigh`. `High` alcanza para que el script salga completo y verificado en un solo turno. |
| Si el selector de esfuerzo no aparece en tu cuenta | **Sonnet 5.5** | el que traiga por defecto (medium) | Alcanza igual: la dificultad está en el detalle de la plantilla, no en el razonamiento. Si el resultado queda incompleto, subí a `High` antes de pedir otra cosa. |
| Si se te agotó la ventana de 5 horas y no querés esperar | **Haiku 5.5** | **High** | Es la única Haiku con control de esfuerzo. Suficiente para completar una plantilla, no para diseñarla desde cero. |
| No usar | `Opus` / `Fable` | — | No están en el plan gratuito. |

**Metodología concreta (esto es lo que más te ahorra cuota):**

1. **Un solo mensaje.** El prompt de la sección 2 ya trae todo lo que Claude necesita decidir; adjuntá el Markdown y pegá el prompt en el mismo envío. Iterar de a una pregunta consume la ventana de 5 horas y no mejora el resultado.
2. **Adjuntá el Markdown, no lo pegues** en el cuerpo del mensaje: el archivo adjunto se procesa mejor y deja lugar para la respuesta.
3. **Pedí el script, no el documento.** Un informe de 20.000 palabras no se puede generar completo en una respuesta de chat sin truncarse; el script tampoco se trunca y además es reproducible y auditable.
4. **No pidas que Claude “mejore” el informe.** El documento está cerrado; pedir reescritura arriesga la fidelidad de las cifras, que es exactamente lo que el tribunal revisó.
5. **Verificá con la sección 3 solo si el PDF ya salió.** Es un turno extra, pero es el que detecta tablas cortadas e índices sin número de página.

---

## 5. Alternativa local, sin Claude

El entorno de este proyecto ya tiene lo necesario para convertir el Markdown sin depender del chat:

- `pandoc 3.8` (`C:\Users\sever\miniconda3\Library\bin\pandoc.exe`) — disponible.
- `Microsoft Edge` (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`) — disponible, sirve para imprimir HTML a PDF.
- `Python 3.11` con `matplotlib` y `Jinja2`.
- **No** hay LaTeX, `LibreOffice`, `wkhtmltopdf`, `python-docx`, `weasyprint` ni `markdown`.

Con eso, la ruta sin instalar nada nuevo es `pandoc` a DOCX (`pandoc tesis_v4.md -o tesis_v4.docx`, que no necesita LaTeX) y desde ahí exportar a PDF; la ruta con mejor tipografía para la tesis —índices con números de página automáticos, control de huérfanas y viudas— es instalar un motor LaTeX y usar `pandoc --pdf-engine`. Las dos se pueden ejecutar y verificar en este repositorio, con las figuras resueltas y sin tocar el Markdown original.
