# Proposal

## Why

La V5 del informe quedó sin una fuente reproducible: el mejor PDF (118 páginas, generado el
2026-10-28 a las 14:38) existe solo en el índice de Git, su Markdown de origen fue borrado del
árbol de trabajo y el conversor versionado en `HEAD` sigue apuntando a `tesis_v4.md`. Los tres
índices de ese PDF salieron sin número de página, hay una página en blanco (36) y la portada se
derrama a la página 2. Sin un generador único, determinista y verificado, cualquier corrección
vuelve a producir un artefacto distinto del aprobado.

## What Changes

- **Restituir las fuentes desde los objetos de Git**: `tesis_v5.md` (contenido) y el PDF aprobado
  del 28/10 14:38 como referencia visual, sin reescribir cifras ni prosa.
- **Reemplazar la cadena de parches por un conversor único y versionado** en
  `V4/scripts/convertir_pdf.py`, con `--md` para elegir la fuente y sin pasos manuales posteriores.
- **Fijar la tipografía y el layout de `tesis_v4.pdf`** (Times New Roman 12, A4, márgenes
  25/30/20 mm, portada e índices con el mismo criterio), según el pedido del 2026-10-28 17:40.
- **Numerar los tres índices** (general, tablas y figuras) con página real y puntos guía, sin
  marcadores `@@@` ni entradas sin número.
- **Agregar una verificación automática** que falle el build si queda un `@@@`, una entrada de
  índice sin página, una página en blanco o un PDF con menos páginas que el anterior.
- **Versionar el árbol de documentos** bajo `V4/documentos/` con una estructura explícita, sin
  secretos ni artefactos de build.
- **No cambia**: el corpus B5, las cifras del informe, el workflow de n8n, el esquema de la base
  ni la operatoria de recolección.

## Capabilities

### New Capabilities

- `generacion-pdf-informe`: define cómo se produce, numera y verifica el PDF del informe a partir
  de una fuente Markdown versionada, con paridad de estilo respecto de la versión anterior y
  compuertas de aceptación antes de publicar el artefacto.

### Modified Capabilities

<!-- Ninguna: no cambian requisitos de comportamiento del pipeline ni del modelo de datos. -->

## Impact

- **Documentos**: `V4/devoluciones/tesis_v5.md` (restituido), `V4/devoluciones/tesis_v5.pdf`
  (regenerado), `V4/devoluciones/build/` (intermedios), `V4/documentos/` (organización).
- **Código**: `V4/scripts/convertir_pdf.py` (reescritura), nuevos verificadores en
  `V4/scripts/` si hacen falta.
- **Dependencias**: Pandoc (`miniconda3/Library/bin/pandoc.exe`), Microsoft Word 365 vía
  `pywin32` (ya instalado), `pypdfium2` para la verificación del PDF.
- **Sin impacto** en n8n, PostgreSQL, credenciales, evidencias ni datos de producción.
