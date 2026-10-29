# Tasks

## 1. Recuperación de las fuentes (no destructiva)

- [x] 1.1 Crear `V4/devoluciones/recuperacion/` y extraer allí `:V4/devoluciones/tesis_v5.pdf`,
      `:V4/devoluciones/build/tesis_v5.docx` y `HEAD:V4/devoluciones/tesis_v5.md`.
      Verificación: los tres archivos existen y sus tamaños coinciden con `git cat-file -s`
      (1.496.015 / 1.018.163 / ~250 KB). **No ejecutar `git restore`, `git checkout` ni `git rm
      --cached` antes de este paso: el índice es la única copia del PDF aprobado.**
- [x] 1.2 Registrar en `recuperacion/INVENTARIO.md` la fecha, el blob de origen, el SHA-256 y el
      tamaño de cada archivo recuperado. Verificación: el inventario lista los tres hashes y
      `Get-FileHash` coincide con lo escrito.
- [x] 1.3 Comprobar que los archivos recuperados son legibles: el PDF abre con `pypdfium2` y tiene
      118 páginas; el DOCX abre con `zipfile` y contiene 32 tablas y 1.947 párrafos.
      Verificación: script de comprobación imprime `PDF=118, tablas=32, parrafos=1947`.

## 2. Reconstrucción del Markdown

- [x] 2.1 Convertir el DOCX recuperado a Markdown con
      `pandoc -f docx -t gfm --wrap=none -o recuperacion/tesis_v5_desde_docx.md`.
      Verificación: el archivo supera los 200 KB y contiene los 10 encabezados de capítulo.
- [x] 2.2 Normalizar el Markdown: encabezados `#`/`##`/`###`, rótulos `**Tabla X.Y.**` y
      `**Figura N.**`, notas al pie, bloques de código y referencias a imágenes.
      Verificación: no quedan `@@@` ni escapes de puntuación fuera de código; el conteo de
      tablas es 32 y las figuras son 4 (imágenes de `V4/figuras/`, idénticas por SHA-256).
- [x] 2.3 Restituir la portada, la nota de versión y las tres secciones de índice (general, tablas y
      figuras) con sus 10 + 28 + 4 entradas. Verificación: conteo exacto 10/28/4 y los títulos
      coinciden con los del PDF aprobado.
- [x] 2.4 Validar las cifras clave del informe con un script sobre el Markdown: 724, 352, 0,509,
      0,847, 0,612, 0,711, 235, 32,5, 1.376, 19,0, 4.929, 17 nodos. Verificación: las 12 aparecen
      al menos una vez y el script termina con código 0.
- [x] 2.5 Comparar token a token el Markdown reconstruido con el texto del PDF aprobado y escribir
      `build/diff_contenido.md` con los bloques distintos. Verificación: similitud ≥ 0,97 y el
      informe lista cada bloque con su contexto.
- [ ] 2.6 Revisar el diff con el usuario y dejar constancia de la aprobación (pendiente explícita
      en el change). Verificación: el usuario confirma que no hay cambios de cifras ni de prosa, o
      indica cuáles aceptar.
- [x] 2.7 Instalar el Markdown definitivo en `V4/devoluciones/tesis_v5.md`.
      Verificación: `git diff --stat` muestra solo ese archivo y las rutas de imágenes resuelven.

## 3. Conversor único y versionado

- [x] 3.1 Restituir `V4/scripts/convertir_pdf.py` desde `HEAD` (`7b55d71`) como base.
      Verificación: `python -c "import ast; ast.parse(open(...).read())"` no falla y el archivo
      conserva las funciones de estilo y numeración.
- [x] 3.2 Agregar los argumentos `--md`, `--out`, `--fuente` y `--verificar`, con valores por
      defecto para la V5. Verificación: `--help` lista los cuatro y una corrida sin argumentos usa
      `V4/devoluciones/tesis_v5.md`.
- [x] 3.3 Portar el mapeo estructural de índices (capítulos por estilo, tablas por el párrafo
      anterior, figuras por epígrafe) y la numeración en hasta 3 pasadas.
      Verificación: una corrida de prueba informa `10 capítulos, 32 entradas de tablas/figuras`
      (28 tablas + 4 figuras) y escribe `\t<página>` en cada entrada.
- [x] 3.4 Aplicar el estilo V4 completo: A4, márgenes 25/30/20 mm, Times New Roman 12 en el cuerpo,
      títulos, tablas, epígrafes, notas y código. Verificación: el DOCX generado declara esos
      márgenes y la fuente en el XML (`w:sectPr`, `w:rFonts`).
- [x] 3.5 Componer la portada en una sola página, con salto de página antes del índice, y numerar
      el pie con primera página distinta. Verificación: la sección 1 tiene
      `DifferentFirstPageHeaderFooter` y la portada no se derrama.
- [x] 3.6 Implementar `--sin-word`: genera solo el DOCX y falla con un mensaje claro si Word no está
      disponible. Verificación: la corrida sin Word devuelve código distinto de cero y explica el
      motivo.
- [x] 3.7 Agregar una compuerta interna que aborte si alguna entrada de índice queda sin página.
      Verificación: una prueba con una entrada sin destino hace fallar el build con el nombre de la
      entrada.

## 4. Verificación automática del PDF

- [x] 4.1 Implementar `V4/scripts/verificar_pdf.py` con las compuertas del design (páginas, A4,
      fuentes, páginas vacías, tres índices, `@@@`, inventario de tablas/figuras, similitud).
      Verificación: ejecutarlo contra el PDF aprobado reporta los defectos conocidos (índices sin
      página, página 36 vacía) sin falsos negativos.
- [x] 4.2 Emitir `V4/devoluciones/build/verificacion_pdf.json` y un resumen legible con fecha,
      fuente, SHA-256 del PDF, cantidad de páginas y resultado por compuerta.
      Verificación: ambos archivos existen y contienen los siete campos.
- [x] 4.3 Devolver código distinto de cero cuando una compuerta falla.
      Verificación: forzar una falla (por ejemplo, un PDF con una página vacía) y comprobar el
      código de salida.
- [x] 4.4 Integrar la verificación en `convertir_pdf.py` (`--verificar` activo por defecto).
      Verificación: una corrida completa sin fallas termina en 0 y con fallas en 1.

## 5. Composición y revisión

- [x] 5.1 Ejecutar el build completo y generar `V4/devoluciones/tesis_v5.pdf`.
      Verificación: el PDF existe, `verificacion_pdf.json` marca todas las compuertas en verde.
- [x] 5.2 Comprobar los tres índices: 10 + 28 + 4 entradas, todas con número, sin `@@@`.
      Verificación: el verificador informa `entradas_sin_pagina=0`.
- [x] 5.3 Comprobar que no hay páginas vacías y que la portada ocupa una sola página.
      Verificación: ninguna página con menos de 40 caracteres salvo la portada y la página de firma.
- [x] 5.4 Comprobar A4, Times New Roman 12 y márgenes.
      Verificación: `MediaBox` 595×842 pt y fuente Times New Roman en las páginas de cuerpo.
- [x] 5.5 Comparar el texto con el PDF aprobado (similitud ≥ 0,97) y revisar el diff.
      Verificación: `diff_contenido.md` sin cambios de cifras ni párrafos, o cambios justificados
      por el usuario.
- [ ] 5.6 Renderizar a PNG la portada, los índices, una tabla, un bloque de código y la página de
      firma. Verificación: las imágenes existen y la revisión visual confirma que no hay desbordes
      ni tablas cortadas.
- [ ] 5.7 Obtener la aprobación explícita del usuario sobre el PDF final.
      Verificación: el usuario responde "OK" al PDF entregado.

## 6. Documentación y cierre

- [ ] 6.1 Documentar el comando único de generación en `AGENTS.md` y en la base de conocimiento
      correspondiente. Verificación: el comando documentado corre tal cual y produce el PDF.
- [ ] 6.2 Actualizar `CHANGES.md` con la relación entre este change, C-26 y la V5.
      Verificación: la entrada menciona el change y el estado del PDF.
- [ ] 6.3 Commit atómico 1: Markdown restituido, conversor y verificador.
      Verificación: `git show --stat` lista solo esos archivos y el mensaje no menciona IA.
- [ ] 6.4 Commit atómico 2: PDF final y registro de verificación.
      Verificación: el SHA-256 del PDF commiteado coincide con el del registro.
- [ ] 6.5 Revisar que no se versionen secretos ni artefactos temporales.
      Verificación: `git status` limpio y sin `.env`, claves, tokens ni `recuperacion/`.

## Notas de ejecución (2026-10-29)

- **PDF final**: `V4/devoluciones/tesis_v5.pdf`, 113 páginas, sha256
  `0ccf5ac3242bf8b691d28431c594357287d16a62465b857afaa5a9e378413e9b`; las 10 compuertas de
  `build/verificacion_pdf.json` en verde.
- **Índices**: 10/28/4 entradas, todas con página, verificado sobre el DOCX y sobre el texto del
  PDF (`indices_en_pdf`: 10/10, 28/28, 4/4).
- **Defecto corregido en el conversor**: `ROTULO` no admitía sufijos con letra y descartaba
  «Tabla 5.9.b.», que quedaba sin número de página (41/42 entradas). Ahora acepta `5.9.b`.
- **Intermedios fuera de OneDrive**: Word se colgaba en `Documents.Open` cuando el DOCX se abría
  inmediatamente después de reescribirse dentro de la carpeta sincronizada (bloqueo del filtro de
  OneDrive, sin diálogo ni error). El MD de trabajo y el DOCX van a `%TEMP%\tfi_tesis_build`; en
  `V4/devoluciones/build/` quedan solo los informes.
- **Artefacto de la capa de texto**: 806 glifos sin mapear (U+FFFE) en la extracción del PDF nuevo;
  el PDF aprobado tiene 15 y `tesis_v4.pdf` 508. El glifo se dibuja bien y el defecto es del
  exportador de Word: se informa, no se usa como compuerta.
- **Test negativo**: sobre el PDF aprobado el verificador detecta tamaño carta (612×792), la página
  36 vacía, la portada en dos páginas y los índices sin número; sale con código 1.
- **Pendiente humano**: aprobación del diff de contenido (2.6), revisión visual (5.6) y aprobación
  del PDF (5.7).

## Workflow follow-up

- Archivar el change una vez aprobado el PDF y sincronizar el spec `generacion-pdf-informe`.
- Verificar el resultado archivado con `openspec status --change regeneracion-pdf-tesis-v5`.
