# Proposal

## Why

El pipeline de generación del PDF (`docs/scripts/convertir_pdf.py`) no puede procesar el índice multinivel de la V6. El algoritmo `numerar_indices` asume una correspondencia 1:1 entre el número secuencial de la entrada del índice (1-61) y el número de capítulo (1-10), por lo que 51 entradas quedan "SIN PAGINA" y el build aborta. El tribunal pide explícitamente un índice multinivel (m-28, NO RESUELTO; H-14, PARCIAL), y el contenido del informe ya tiene 61 entradas en el índice general. Sin esta corrección, el PDF no puede generarse con índices numerados.

## What Changes

- Modificar `mapa_cuerpo` en `convertir_pdf.py` para construir un diccionario `texto_a_pagina` que mapee el texto normalizado de cada encabezado (H1, H2, H3) a su número de página, además del existente `capitulos` (int→página).
- Modificar `numerar_indices` para que, cuando una entrada del índice no se resuelva por número de capítulo, intente matching por texto normalizado (quitar acentos, mayúsculas, números iniciales) contra `texto_a_pagina`.
- Agregar manejo de colisiones: si dos entradas normalizan al mismo texto, usar la primera coincidencia.
- Ajustar `verificar_pdf.py` para que las compuertas `indices_numerados` y `rotulos` reflejen los conteos reales de V6 (61 entradas en Índice general, 29 tablas, 33 tablas en DOCX).

## Capabilities

### New Capabilities
- `pdf-index-numbering`: soporte para índices multinivel en el pipeline de generación del PDF, con matching por texto normalizado entre entradas del índice y encabezados del cuerpo.

### Modified Capabilities
(none)

## Impact

- `docs/scripts/convertir_pdf.py` — funciones `mapa_cuerpo` y `numerar_indices`
- `docs/scripts/verificar_pdf.py` — compuertas `indices_numerados` y `rotulos`
- No afecta el Markdown del informe ni el contenido del PDF
- No afecta el workflow de n8n ni la base de datos
