# Tasks

## 1. Modificar mapa_cuerpo en convertir_pdf.py
- [x] 1.1 Agregar función de normalización de texto (lowercase, sin acentos, strip de números iniciales)
- [x] 1.2 En `mapa_cuerpo`, construir `texto_a_pagina` dict (H1/H2/H3 normalizado → página) además de `capitulos`
- [x] 1.3 Retornar `texto_a_pagina` como tercer elemento de la tupla

## 2. Modificar numerar_indices en convertir_pdf.py
- [x] 2.1 Para entradas que no se resuelven por `capitulos.get(clave)`, normalizar el texto de la entrada y buscar en `texto_a_pagina`
- [x] 2.2 Si no hay coincidencia exacta, intentar matching por subcadena
- [x] 2.3 Manejar colisiones: usar la primera coincidencia
- [x] 2.4 Mantener warning (no abortar) para entradas sin página

## 3. Ajustar verificar_pdf.py
- [x] 3.1 Actualizar INDICES a 61 entradas en Índice general
- [x] 3.2 Verificar que rotulos (29) y tablas_docx (33) sigan correctos

## 4. Build y verificación
- [x] 4.1 Ejecutar `convertir_pdf.py` y verificar que no haya SIN PAGINA
- [x] 4.2 Ejecutar `verificar_pdf.py` y confirmar 10/10 compuertas
- [x] 4.3 Restaurar `raise SystemExit` si todo pasa (o dejar como warning)

## 5. Validación final
- [x] 5.1 Revisar el PDF manualmente (índice, tablas, figuras)
- [x] 5.2 Confirmar que el índice tiene 61 entradas numeradas
