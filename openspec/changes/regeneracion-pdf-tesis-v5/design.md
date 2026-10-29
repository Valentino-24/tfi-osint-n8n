# Design

## Context

Ver `proposal.md` — Why. El estado actual, medido sobre el repositorio el 2026-10-28:

| Artefacto | Origen | Páginas | Estado |
|---|---|---|---|
| `tesis_v5.pdf` (índice de Git) | Word 365, 2026-10-28 14:38 | 118 | Índices sin página, página 36 vacía, portada en 2 páginas |
| `tesis_v5.docx` (índice de Git) | Word 365, 2026-10-28 16:55–17:38 | — | Mismo contenido que el PDF (98,3 % de tokens), sin números de índice |
| `tesis_v5.pdf` (`HEAD`) | Word 365, 2026-10-26 13:58 | 97 | Índice de tablas/figuras sin página |
| `tesis_v5.md` (`HEAD`) | Markdown | — | 1.942 líneas; **no** contiene Tabla 5.9.b, 5.15 ni Anexo E |
| `tesis_v4.pdf` | Word 365, 2026-10-20 | 75 | Referencia tipográfica |

El contenido más nuevo (Tabla 5.9 por comunidad, 5.9.b por idioma, 5.15, Anexo E con E.1/E.2) solo
existe en el PDF y el DOCX staged. El Markdown de `HEAD` es anterior. El conversor de `HEAD`
(`7b55d71`) apunta a `tesis_v4.md` y no tiene `--md`; la cadena que produjo el PDF del 28/10 quedó
repartida en scripts temporales no versionados (`fix_indices_directo.py`, `fix_pdf_styles.py`,
`adjust_cover_tables.py`, entre otros).

Restricciones: Windows 10/11, Word 365 obligatorio para la exportación, Pandoc en
`C:\Users\sever\miniconda3\Library\bin\pandoc.exe`, `pywin32` y `pypdfium2` disponibles,
`python-docx` **no** instalado. Nada de secretos ni de acceso a la base en este change.

## Goals / Non-Goals

**Goals:**
- Recuperar el contenido aprobado sin reescribirlo y sin depender de blobs inalcanzables.
- Dejar un generador único, versionado y determinista, con una sola invocación.
- Garantizar números de página en los tres índices y ausencia de páginas vacías.
- Producir un registro de verificación reproducible antes de publicar el PDF.

**Non-Goals:**
- Corregir cifras, prosa, tablas ni referencias del informe.
- Cambiar el workflow de n8n, el esquema de la base o las evidencias.
- Reorganizar masivamente `V4/documentos/` en este change.
- Publicar o activar nada en n8n.

## Decisions

### D1 — Base de contenido: DOCX del 28/10, verificado contra el PDF aprobado

Se reconstruye el Markdown desde el DOCX staged (`git show
:V4/devoluciones/build/tesis_v5.docx`) con Pandoc (`-f docx -t gfm --wrap=none`), y se compara
token a token contra el PDF del 14:38. El Markdown de `HEAD` se conserva como referencia histórica
pero **no** se usa como fuente: perdió las tablas nuevas y el Anexo E.

*Alternativas*: (a) `HEAD:tesis_v5.md` — rechazada por contenido incompleto; (b) extraer texto del
PDF — rechazada porque pierde la estructura de tablas y encabezados; (c) reescribir a mano — 
rechazada por riesgo de introducir cifras.

### D2 — Tipografía: paridad con `tesis_v4.pdf`

Cuerpo Times New Roman 12, A4, márgenes 25/30/20 mm, portada e índices con el criterio de la V4,
según el pedido del 2026-10-28 17:40. El PDF aprobado del 28/10 estaba en Aptos 11; la conversión
de fuente cambia la paginación, por lo que los números de índice se recalculan, nunca se copian.

*Alternativa*: conservar Aptos 11 — rechazada porque contradice el pedido explícito. El generador
expone `--fuente` para revertir sin tocar código.

### D3 — Numeración de índices: dos pasadas con anclaje estructural

1. Componer el DOCX con los índices como texto plano (sin `@@@`, sin campos TOC).
2. Exportar un PDF preliminar.
3. Localizar cada destino por estructura, no por primera coincidencia textual: capítulos por estilo
   de título; tablas por el párrafo inmediatamente anterior a la tabla; figuras por el epígrafe.
   Ignorar todo lo anterior al inicio del cuerpo (evita que una entrada del índice se apunte a sí
   misma).
4. Escribir `\t<página>` con tabulación derecha y puntos guía; recalcular paginación; repetir hasta
   que no haya cambios (máximo 3 pasadas).
5. Exportar el PDF final y verificar que las tres listas tengan 100 % de entradas numeradas.

*Alternativas*: campos TOC/TOF nativos de Word — rechazados porque las tablas y figuras no son
campos `SEQ` y el índice es texto literal del Markdown; el reemplazo `@@@` por búsqueda simple —
rechazado porque fue la causa del fallo (coincidencias múltiples y exportación sin repaginar).

### D4 — Un solo script, sin cadena de parches

`V4/scripts/convertir_pdf.py` absorbe todo: preparación del Markdown, Pandoc, estilos, saltos,
índices, numeración, exportación y verificación. Argumentos: `--md`, `--out`, `--fuente`,
`--sin-word` (solo DOCX, no apto para entrega) y `--verificar`. No se permiten scripts posteriores
sobre el DOCX.

### D5 — Verificación como compuerta, no como informe opcional

Un verificador con `pypdfium2` comprueba, sobre el PDF final:

- cantidad de páginas y tamaño A4;
- fuentes del cuerpo (Times New Roman presente, sin Aptos en el cuerpo);
- ninguna página con menos de 40 caracteres (salvo la portada si corresponde);
- las tres listas de índice: cantidad de entradas y número de página en cada una;
- ausencia de `@@@` y de entradas terminadas en punto sin número;
- inventario de tablas y figuras contra el Markdown (32 tablas, 4 figuras);
- comparación de tokens contra el PDF aprobado (similitud ≥ 0,97), reportando los bloques distintos.

El resultado se escribe en `V4/devoluciones/build/verificacion_pdf.json` y en un resumen legible.
Si una compuerta falla, el proceso termina con código distinto de cero.

### D6 — Ubicación de archivos

La fuente activa y el PDF final quedan en `V4/devoluciones/` (rutas que citan los scripts y el
propio informe). `V4/documentos/` se conserva como archivo histórico y no se toca en este change.

## Risks / Trade-offs

- **Word COM se cuelga o abre diálogos** → `DisplayAlerts=0`, `Visible=False`, cierre garantizado
  en `finally`, tiempo máximo por paso y una sola reintentativa; el build nunca corre desatendido.
- **El round-trip DOCX→MD pierde tablas** → verificar 32 tablas y los 28 rótulos del índice antes de
  generar; si falta una, reparar esa tabla a mano y registrarlo.
- **El DOCX del 17:38 contiene ediciones de la sesión fallida** → la comparación de tokens y la
  revisión humana del diff son obligatorias antes de commitear.
- **Times New Roman cambia la paginación y desborda la portada** → la portada se compone con saltos
  explícitos y se verifica que ocupe una sola página.
- **OneDrive bloquea el archivo** → trabajar sobre copia local en `build/`, cerrar Word antes de
  exportar y reintentar una vez.
- **El PDF aprobado tiene defectos de layout** (página 36 vacía, portada en dos páginas) → se
  corrigen en la composición, no se replican.

## Migration Plan

1. Extraer los blobs a `V4/devoluciones/recuperacion/` sin sobrescribir nada.
2. Reconstruir `tesis_v5.md` y validar inventario (tablas, figuras, rótulos, cifras clave).
3. Reescribir `convertir_pdf.py` y ejecutar `--sin-word` para validar el DOCX.
4. Ejecutar el build completo y la verificación; revisar el diff contra el PDF aprobado.
5. Commit atómico: fuente + script + registro de verificación. El PDF va en un commit separado.
6. Rollback: `git checkout` de los blobs originales; el PDF aprobado se conserva como referencia.

## Open Questions

- ¿La cátedra exige Aptos 11 (formato del PDF aprobado) o acepta la paridad con la V4 en Times New
  Roman? Se implementa V4 por el pedido del 17:40 y se deja `--fuente` para cambiarlo en una línea.
- ¿`V4/documentos/` debe ser la ubicación canónica de los PDF históricos? Se difiere; no bloquea el
  build.
