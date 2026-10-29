# Inventario de recuperación — V5

Fecha de extracción: 2026-10-28
Origen: objetos de Git del repositorio `tfi-osint-n8n` (índice y `HEAD`).
Método: `git show <blob> > archivo` con redirección binaria de `cmd`.

| Archivo | Blob de origen | SHA-256 | Bytes |
|---|---|---|---|
| `tesis_v5_aprobado_2026-10-28.pdf` | `:V4/devoluciones/tesis_v5.pdf` (`41f9d74b`) | `ad6094e65a4da9ca09693688442c06a0feb4ceb4e2f516bdc3dc78fea5b33280` | 1.496.015 |
| `tesis_v5_2026-10-28.docx` | `:V4/devoluciones/build/tesis_v5.docx` (`d1c8416a`) | `dff5276643d5f84294c99a33d447ab622206d998a4a37133146cad376de10ac9` | 1.018.163 |
| `tesis_v5_head.md` | `HEAD:V4/devoluciones/tesis_v5.md` (`bb28d503`) | `e092e42663e6e9115b1a8c820c0971de687acf2a4669dd0c872765fbf3a83bbe` | 253.534 |

## Estado de cada artefacto

- **PDF aprobado (118 páginas, Word 365, 2026-10-28 14:38)**: es la referencia visual y de contenido.
  Defectos conocidos: los tres índices sin número de página, página 36 vacía, portada derramada a la
  página 2.
- **DOCX (Word 365, 2026-10-28 16:55–17:38)**: única copia del contenido nuevo (Tabla 5.9.b, 5.15,
  Anexo E). Su texto coincide en un 98,75 % con el PDF aprobado; las diferencias son artefactos de
  extracción de tablas y encabezados repetidos por salto de página (`build/diff_contenido.md`). Se usa
  como fuente para reconstruir el Markdown, sujeto a la revisión de la tarea 2.6.
- **Markdown de `HEAD` (1.942 líneas)**: contenido anterior; no tiene 5.9.b, 5.15 ni Anexo E. Se
  conserva como referencia histórica, no como fuente.

## Derivación del Markdown

| Paso | Comando / script | Resultado |
|---|---|---|
| DOCX → GFM | `pandoc -f docx -t gfm --wrap=none --extract-media=recuperacion/media` | `tesis_v5_desde_docx.md` (277.858 B, sha256 `b4359d38…`) |
| Normalización | `python recuperacion/normalizar_md.py` | `../tesis_v5.md` (274.765 B, sha256 `b1225349…`) |
| Cifras clave | `python recuperacion/verificar_cifras_md.py` | 12/12 presentes, código 0 (`verificacion_cifras.txt`) |
| Comparación con el PDF | `python recuperacion/comparar_md_pdf.py` | similitud 0,9875, 0 bloques con contenido ausente (`../build/diff_contenido.md`) |

La normalización no altera el contenido: los tokens del GFM y del Markdown final son idénticos
(40.580 cada uno, diferencia de multiconjuntos 0). Los cuatro PNG extraídos del DOCX son idénticos
por SHA-256 a `V4/figuras/Figura_1_arquitectura.png`, `Figura_2_der.png`, `Figura_3_workflow.png` y
`Figura_4_serie_temporal.png`, que son los que referencia el Markdown.

## Advertencia operativa

Este directorio es la única copia del PDF aprobado y del DOCX con el contenido nuevo. No ejecutar
`git restore`, `git checkout` ni `git rm --cached` sobre `V4/devoluciones/` hasta que estos archivos
estén copiados fuera del repositorio o commiteados. `recuperacion/` no se versiona.
