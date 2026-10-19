# -*- coding: utf-8 -*-
"""
Convierte V4/devoluciones/tesis_v4.md a PDF con calidad de imprenta.

Ruta: Pandoc (Markdown -> DOCX) + Microsoft Word (estilos, saltos de pagina,
numeracion, indices con pagina, exportacion a PDF). No modifica el Markdown
original: trabaja sobre una copia en V4/devoluciones/build/.

Uso:
    python V4/scripts/convertir_pdf.py
    python V4/scripts/convertir_pdf.py --sin-word               (solo el DOCX)
    python V4/scripts/convertir_pdf.py --sin-numerar-indices    (indices tal cual el MD)
    python V4/scripts/convertir_pdf.py --renderizar             (exporta paginas a PNG)
"""

from __future__ import annotations

import argparse
import io
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
MD_ORIGEN = RAIZ / "V4" / "devoluciones" / "tesis_v4.md"
CARPETA_BUILD = RAIZ / "V4" / "devoluciones" / "build"
MD_BUILD = CARPETA_BUILD / "tesis_v4.build.md"
DOCX_BUILD = CARPETA_BUILD / "tesis_v4.docx"
PDF_SALIDA = RAIZ / "V4" / "devoluciones" / "tesis_v4.pdf"

# --- Constantes de Word (literales para no depender de la generacion COM) ---
WD_ALIGN_LEFT = 0
WD_ALIGN_CENTER = 1
WD_ALIGN_JUSTIFY = 3
WD_LINE_SPACE_SINGLE = 0
WD_LINE_SPACE_1PT5 = 1
WD_EXPORT_FORMAT_PDF = 17
WD_EXPORT_ALL_DOCUMENT = 0
WD_EXPORT_DOCUMENT_CONTENT = 0
WD_EXPORT_CREATE_HEADING_BOOKMARKS = 1
WD_HEADER_FOOTER_PRIMARY = 1
WD_ALIGN_PAGE_NUMBER_CENTER = 1
WD_AUTOFIT_WINDOW = 2
WD_INFO_ACTIVE_END_PAGE = 3
IDIOMA_ES_AR = 11274

A4_ANCHO = 595.3
A4_ALTO = 841.9
MARGEN_SUP = 70.9   # 25 mm
MARGEN_INF = 70.9   # 25 mm
MARGEN_IZQ = 85.0   # 30 mm
MARGEN_DER = 56.7   # 20 mm

FUENTE_CUERPO = "Times New Roman"
FUENTE_CODIGO = "Consolas"

ESTILOS_TITULO = {"Título 1": 1, "Título 2": 2, "Título 3": 3,
                  "Heading 1": 1, "Heading 2": 2, "Heading 3": 3,
                  "Title": 1, "Subtitle": 2}
ESTILOS_CITA = {"Texto de bloque", "Block Text", "Quote", "Cita"}
ESTILO_FIGURA = {"Captioned Figure"}
ESTILO_EPIGRAFE = {"Image Caption"}
ESTILO_CODIGO = {"Source Code"}
INDICES = ("Índice general", "Índice de tablas", "Índice de figuras")
PREFIJO_INDICE = "índice"

ROTULO = re.compile(r"^(Tabla|Figura)\s+([A-Za-z0-9]+(?:\.[0-9]+)?)\.\s")
SALTO_OPENXML = ["```{=openxml}", '<w:p><w:r><w:br w:type="page"/></w:r></w:p>', "```"]
MARCA_SALTO = "\x0c"


# --------------------------------------------------------------------------
# 1. Markdown de trabajo
# --------------------------------------------------------------------------
def preparar_markdown() -> int:
    texto = io.open(MD_ORIGEN, encoding="utf-8").read().replace("\r\n", "\n")

    reemplazos = 0
    for ruta in sorted((RAIZ / "V4" / "figuras").glob("*.png")):
        relativa = "../figuras/" + ruta.name
        if relativa in texto:
            texto = texto.replace(relativa, ruta.as_posix())
            reemplazos += 1

    lineas = texto.split("\n")

    # Reglas horizontales decorativas: pandoc las convierte en un objeto VML que
    # Word inserta como parrafo propio; cuando una cae al inicio de una pagina
    # empuja el titulo siguiente y deja la pagina en blanco. Se descartan.
    sin_reglas = [l for l in lineas if l.strip() not in ("---", "***", "___")]
    reglas = len(lineas) - len(sin_reglas)
    lineas = sin_reglas

    # Portada: cada linea del bloque inicial en su propio renglon (en Markdown los
    # saltos simples se fusionan en un mismo parrafo).
    fin_portada = next((i for i, l in enumerate(lineas) if l.startswith("> ")), 0)
    for i in range(fin_portada - 1):
        if lineas[i].strip() and lineas[i + 1].strip() and not lineas[i].startswith("#"):
            if not lineas[i].endswith("  "):
                lineas[i] = lineas[i] + "  "

    # Salto de pagina antes de cada titulo de nivel 1 (excepto el primero) y antes
    # del primer indice, para que la portada quede sola en su pagina.
    salida: list[str] = []
    for linea in lineas:
        corta = linea.startswith("# ") or linea.strip() in ("## Índice general",)
        if corta and any(l.strip() for l in salida):
            salida += [""] + SALTO_OPENXML + [""]
        salida.append(linea)

    CARPETA_BUILD.mkdir(parents=True, exist_ok=True)
    io.open(MD_BUILD, "w", encoding="utf-8", newline="\n").write("\n".join(salida))
    print(f"[prep] reglas horizontales descartadas: {reglas}")
    return reemplazos


def correr_pandoc() -> None:
    pandoc = shutil.which("pandoc") or r"C:\Users\sever\miniconda3\Library\bin\pandoc.exe"
    cmd = [pandoc, str(MD_BUILD),
           "--from=markdown+pipe_tables+raw_attribute+implicit_figures",
           "--to=docx", "--output=" + str(DOCX_BUILD), "--standalone"]
    print("[pandoc] " + " ".join(cmd[1:]))
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit("pandoc fallo:\n" + (r.stderr or ""))
    if r.stderr.strip():
        print("[pandoc stderr] " + r.stderr.strip())


# Word no expone ParagraphFormat.AutoHyphenation por late binding (solo el
# ajuste de documento), asi que el guionado se desactiva parrafo por parrafo
# insertando <w:suppressAutoHyphens/> en el XML. El elemento debe quedar en el
# orden que fija el esquema (despues de w:tabs y antes de w:spacing), por eso se
# inserta antes de la primera etiqueta posterior valida.
ORDEN_PPR = ("<w:kinsoku", "<w:wordWrap", "<w:overflowPunct", "<w:topLinePunct",
             "<w:autoSpaceDE", "<w:autoSpaceDN", "<w:bidi", "<w:adjustRightInd",
             "<w:snapToGrid", "<w:spacing", "<w:ind", "<w:contextualSpacing",
             "<w:mirrorIndents", "<w:suppressOverlap", "<w:jc", "<w:textAlignment",
             "<w:textboxTightWrap", "<w:outlineLvl", "<w:divId", "<w:cnfStyle",
             "<w:rPr", "<w:sectPr", "<w:pPrChange", "</w:pPr>")


def sin_guionado(ruta) -> None:
    """Evita que se corten con guion los titulos y todo el bloque de portada."""
    with zipfile.ZipFile(ruta) as z:
        partes = [(i, z.read(i.filename)) for i in z.infolist()]
    xml = next(d for i, d in partes if i.filename == "word/document.xml").decode("utf-8")

    trozos = re.split(r"(<w:p(?:\s[^>]*)?>.*?</w:p>)", xml, flags=re.S)
    portada, titulos, otros = True, 0, 0
    for k, trozo in enumerate(trozos):
        if not trozo.startswith("<w:p"):
            continue
        titulo = bool(re.search(r'<w:pStyle w:val="Heading[123]"', trozo))
        if "Índice general" in re.sub(r"<[^>]+>", "", trozo):
            portada = False
        if not (titulo or portada) or "<w:suppressAutoHyphens" in trozo:
            continue
        marca = "<w:suppressAutoHyphens/>"
        if "<w:pPr>" in trozo:
            cortes = [trozo.find(t) for t in ORDEN_PPR if trozo.find(t) >= 0]
            corte = min([c for c in cortes if c >= 0], default=trozo.index("<w:pPr>") + 7)
            trozo = trozo[:corte] + marca + trozo[corte:]
        else:
            fin = trozo.index(">") + 1
            trozo = trozo[:fin] + "<w:pPr>" + marca + "</w:pPr>" + trozo[fin:]
        trozos[k] = trozo
        if titulo:
            titulos += 1
        else:
            otros += 1

    nuevo = "".join(trozos).encode("utf-8")
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
        for info, datos in partes:
            z.writestr(info, nuevo if info.filename == "word/document.xml" else datos)
    print(f"[pandoc] guionado desactivado: {titulos} titulos, {otros} parrafos de portada")


# --------------------------------------------------------------------------
# 2. Word
# --------------------------------------------------------------------------
def pagina_actual(rango) -> int:
    return rango.Information(WD_INFO_ACTIVE_END_PAGE)


def preparar_pagina(doc) -> None:
    for seccion in doc.Sections:
        ps = seccion.PageSetup
        ps.PageWidth = A4_ANCHO
        ps.PageHeight = A4_ALTO
        ps.TopMargin = MARGEN_SUP
        ps.BottomMargin = MARGEN_INF
        ps.LeftMargin = MARGEN_IZQ
        ps.RightMargin = MARGEN_DER
        ps.HeaderDistance = 35.0
        ps.FooterDistance = 35.0
    doc.Content.LanguageID = IDIOMA_ES_AR
    doc.AutoHyphenation = True
    doc.HyphenationZone = 18
    doc.ConsecutiveHyphensLimit = 2


def arreglar_saltos(doc) -> None:
    """Convierte los parrafos que solo contienen un salto manual en 'salto antes'
    del parrafo siguiente, para no dejar paginas en blanco ni renglones vacios."""
    parrafos = doc.Paragraphs
    portadores = [i for i in range(1, parrafos.Count + 1)
                  if parrafos(i).Range.Text.strip() == ""
                  and MARCA_SALTO in parrafos(i).Range.Text]
    for i in reversed(portadores):
        try:
            parrafos(i + 1).Format.PageBreakBefore = True
            parrafos(i).Range.Delete()
        except Exception as e:  # noqa: BLE001
            print(f"[word] salto {i} sin convertir: {e}")
    print(f"[word] saltos de pagina convertidos: {len(portadores)}")


def estilo_cuerpo(doc) -> None:
    for p in doc.Paragraphs:
        try:
            nombre = p.Style.NameLocal
        except Exception:  # noqa: BLE001
            continue
        if nombre in ESTILOS_TITULO or nombre in ESTILO_FIGURA or \
                nombre in ESTILO_EPIGRAFE or nombre in ESTILO_CODIGO:
            continue
        f = p.Format
        p.Range.Font.Name = FUENTE_CUERPO
        p.Range.Font.Size = 12
        f.LineSpacingRule = WD_LINE_SPACE_1PT5
        f.SpaceBefore = 0
        f.SpaceAfter = 6
        f.FirstLineIndent = 0
        f.Alignment = WD_ALIGN_JUSTIFY
        if ROTULO.match(p.Range.Text.strip()):
            p.Range.Font.Bold = True
            f.Alignment = WD_ALIGN_LEFT
            f.KeepWithNext = True
            f.SpaceBefore = 10
        elif nombre in ESTILOS_CITA:
            f.LeftIndent = 28
            f.RightIndent = 14
            p.Range.Font.Size = 10.5


def estilo_titulos(doc) -> None:
    for p in doc.Paragraphs:
        try:
            nivel = ESTILOS_TITULO.get(p.Style.NameLocal)
        except Exception:  # noqa: BLE001
            continue
        if not nivel:
            continue
        f = p.Format
        p.Range.Font.Name = FUENTE_CUERPO
        p.Range.Font.Bold = True
        p.Range.Font.Color = 0
        f.Alignment = WD_ALIGN_LEFT
        f.FirstLineIndent = 0
        f.KeepWithNext = True
        f.LineSpacingRule = WD_LINE_SPACE_SINGLE
        if nivel == 1:
            p.Range.Font.Size = 14
            f.SpaceBefore = 18
            f.SpaceAfter = 12
        elif nivel == 2:
            p.Range.Font.Size = 12.5
            f.SpaceBefore = 12
            f.SpaceAfter = 6
        else:
            p.Range.Font.Size = 12
            f.SpaceBefore = 10
            f.SpaceAfter = 4


def estilo_portada(doc) -> None:
    """Centra la portada (todo lo anterior al primer indice) y agranda el titulo."""
    primero = True
    for p in doc.Paragraphs:
        try:
            nombre = p.Style.NameLocal
        except Exception:  # noqa: BLE001
            continue
        texto = p.Range.Text.strip()
        if nombre in ESTILOS_TITULO and texto.lower().startswith(PREFIJO_INDICE):
            break
        if nombre in ESTILOS_CITA:
            continue
        p.Format.Alignment = WD_ALIGN_CENTER
        p.Format.FirstLineIndent = 0
        if nombre in ESTILOS_TITULO and primero:
            p.Range.Font.Size = 16
            p.Format.SpaceAfter = 24
            primero = False


def estilo_tablas(doc) -> None:
    for t in doc.Tables:
        t.AutoFitBehavior(WD_AUTOFIT_WINDOW)
        t.Rows.AllowBreakAcrossPages = False
        t.Borders.Enable = True
        try:
            t.Rows(1).HeadingFormat = True
        except Exception:  # noqa: BLE001
            pass
        for parrafo in t.Range.Paragraphs:
            f = parrafo.Format
            parrafo.Range.Font.Name = FUENTE_CUERPO
            parrafo.Range.Font.Size = 9.5
            f.LineSpacingRule = WD_LINE_SPACE_SINGLE
            f.SpaceBefore = 1
            f.SpaceAfter = 1
            f.FirstLineIndent = 0
            f.Alignment = WD_ALIGN_LEFT
    print(f"[word] tablas formateadas: {doc.Tables.Count}")


def estilo_figuras(doc) -> None:
    figuras = epigrafes = 0
    for p in doc.Paragraphs:
        try:
            nombre = p.Style.NameLocal
        except Exception:  # noqa: BLE001
            continue
        if nombre in ESTILO_FIGURA:
            p.Format.Alignment = WD_ALIGN_CENTER
            p.Format.SpaceBefore = 12
            p.Format.SpaceAfter = 4
            p.Format.KeepWithNext = True
            figuras += 1
        elif nombre in ESTILO_EPIGRAFE:
            p.Format.Alignment = WD_ALIGN_CENTER
            p.Range.Font.Name = FUENTE_CUERPO
            p.Range.Font.Size = 10
            p.Range.Font.Italic = True
            p.Format.SpaceAfter = 12
            p.Format.LineSpacingRule = WD_LINE_SPACE_SINGLE
            epigrafes += 1
        elif nombre in ESTILO_CODIGO:
            p.Range.Font.Name = FUENTE_CODIGO
            p.Range.Font.Size = 9.5
            p.Format.Alignment = WD_ALIGN_LEFT
            p.Format.LineSpacingRule = WD_LINE_SPACE_SINGLE
    print(f"[word] figuras: {figuras}, epigrafes: {epigrafes}")


def numerar_paginas(doc) -> None:
    for seccion in doc.Sections:
        seccion.PageSetup.DifferentFirstPageHeaderFooter = True
        pie = seccion.Footers(WD_HEADER_FOOTER_PRIMARY)
        pie.Range.Font.Name = FUENTE_CUERPO
        pie.Range.Font.Size = 10
        pie.PageNumbers.Add(WD_ALIGN_PAGE_NUMBER_CENTER, False)


# --------------------------------------------------------------------------
# 3. Indices con numero de pagina (dos pasadas: la numeracion puede mover el texto)
# --------------------------------------------------------------------------
def mapa_cuerpo(doc, desde: int) -> tuple[dict[str, int], dict[int, int]]:
    """Pagina real de cada rotulo y de cada capitulo.

    Los rotulos se localizan por su posicion estructural (el parrafo que precede a
    cada tabla y el epigrafe que acompana a cada figura), no por la primera
    coincidencia textual: una cita en prosa del tipo 'se cuantifica en la Tabla 5.9'
    apuntaria a la pagina equivocada.
    """
    etiquetas: dict[str, int] = {}
    capitulos: dict[int, int] = {}

    def fecha(nombre: str, rango) -> None:
        m = ROTULO.match(rango.Text.strip())
        if not m:
            return
        try:
            pagina = pagina_actual(rango)
        except Exception:  # noqa: BLE001
            return
        if pagina >= desde:
            etiquetas.setdefault(f"{m.group(1)} {m.group(2)}.", pagina)

    for tabla in doc.Tables:
        posicion = tabla.Range.Start - 1
        # En algunos casos entre el rotulo y la tabla hay un parrafo de prosa que
        # cita la tabla; se busca hacia atras hasta cuatro parrafos.
        for retroceso in range(4):
            try:
                parrafo = doc.Range(posicion - retroceso, posicion - retroceso).Paragraphs(1)
            except Exception:  # noqa: BLE001
                break
            if ROTULO.match(parrafo.Range.Text.strip()):
                fecha("rotulo", parrafo.Range)
                break

    for p in doc.Paragraphs:
        try:
            nombre = p.Style.NameLocal
            texto = p.Range.Text.strip()
            if nombre in ESTILO_EPIGRAFE:
                fecha("epigrafe", p.Range)
            elif nombre in ESTILOS_TITULO and ESTILOS_TITULO[nombre] == 1:
                m = re.match(r"^CAP[IÍ]TULO\s+(\d+)\s*:", texto, re.IGNORECASE)
                if m:
                    pagina = pagina_actual(p.Range)
                    if pagina >= desde:
                        capitulos.setdefault(int(m.group(1)), pagina)
                elif texto.upper().startswith("REFERENCIAS") and pagina_actual(p.Range) >= desde:
                    capitulos.setdefault(9, pagina_actual(p.Range))
                elif texto.upper().startswith("ANEXOS") and pagina_actual(p.Range) >= desde:
                    capitulos.setdefault(10, pagina_actual(p.Range))
            elif len(texto) < 200 and ROTULO.match(texto):
                # Respaldo: rotulos cuyo parrafo no quedo pegado a la tabla o figura.
                m = ROTULO.match(texto)
                pagina = pagina_actual(p.Range)
                if pagina >= desde:
                    etiquetas.setdefault(f"{m.group(1)} {m.group(2)}.", pagina)
        except Exception:  # noqa: BLE001
            continue
    return etiquetas, capitulos


def recolectar_entradas(doc):
    """(indice de parrafo, texto base, clave de rotulo o numero de capitulo)."""
    parrafos = doc.Paragraphs
    entradas: list[tuple[int, str, str | int]] = []
    seccion = None
    for i in range(1, parrafos.Count + 1):
        p = parrafos(i)
        try:
            texto = p.Range.Text.strip()
            nombre = p.Style.NameLocal
        except Exception:  # noqa: BLE001
            continue
        if nombre in ESTILOS_TITULO:
            seccion = texto if (ESTILOS_TITULO[nombre] == 2 and texto in INDICES) else None
            continue
        if not seccion or not texto:
            continue
        m = ROTULO.match(texto)
        if m:
            entradas.append((i, texto, f"{m.group(1)} {m.group(2)}."))
            continue
        numero = None
        m = re.match(r"^(\d+)\.\s+\S", texto)
        if m:
            numero = int(m.group(1))
        else:
            try:
                m = re.match(r"^(\d+)", p.Range.ListFormat.ListString.strip())
                if m:
                    numero = int(m.group(1))
            except Exception:  # noqa: BLE001
                numero = None
        if numero:
            entradas.append((i, texto, numero))
    return entradas


def numerar_indices(doc, intentos: int = 3) -> None:
    parrafos = doc.Paragraphs
    pagina_resumen = 0
    for p in parrafos:
        try:
            if p.Style.NameLocal in ESTILOS_TITULO and \
                    p.Range.Text.strip().upper() == "RESUMEN":
                pagina_resumen = pagina_actual(p.Range)
                break
        except Exception:  # noqa: BLE001
            continue
    if not pagina_resumen:
        print("[indices] no se encontro el RESUMEN; se omite la numeracion")
        return

    entradas = recolectar_entradas(doc)
    print(f"[indices] entradas detectadas: {len(entradas)}")
    aplicados: dict[int, tuple[str, int]] = {}   # indice -> (sufijo escrito, pagina)

    for intento in range(1, intentos + 1):
        etiquetas, capitulos = mapa_cuerpo(doc, pagina_resumen)
        cambios = resueltas = 0
        for indice, texto_base, clave in entradas:
            pagina = etiquetas.get(clave) if isinstance(clave, str) else capitulos.get(clave)
            if not pagina:
                continue
            resueltas += 1
            sufijo = f"  —  {pagina}"
            previo = aplicados.get(indice)
            if previo and previo[0] == sufijo:
                continue
            p = parrafos(indice)
            try:
                if previo:
                    quitar = doc.Range(p.Range.End - 1 - len(previo[0]), p.Range.End - 1)
                    quitar.Delete()
                cuerpo = doc.Range(parrafos(indice).Range.Start, parrafos(indice).Range.End - 1)
                cuerpo.InsertAfter(sufijo)
                aplicados[indice] = (sufijo, pagina)
                cambios += 1
            except Exception as e:  # noqa: BLE001
                print(f"[indices] fallo en '{texto_base[:38]}': {e}")
        print(f"[indices] pasada {intento}: resueltas {resueltas}, escritas {cambios}, "
              f"rotulos {len(etiquetas)}, capitulos {len(capitulos)}")
        if cambios == 0:
            break

    print("[indices] paginas asignadas a los rotulos:")
    for etiqueta in sorted(etiquetas, key=lambda e: (e.split()[0], e.split()[1])):
        print(f"    {etiqueta:14} -> {etiquetas[etiqueta]:3}")


def exportar_pdf(doc, destino: Path) -> None:
    doc.Save()
    if destino.exists():
        destino.unlink()
    doc.ExportAsFixedFormat(
        OutputFileName=str(destino), ExportFormat=WD_EXPORT_FORMAT_PDF,
        OpenAfterExport=False, OptimizeFor=0, Range=WD_EXPORT_ALL_DOCUMENT,
        Item=WD_EXPORT_DOCUMENT_CONTENT, IncludeDocProps=True, KeepIRM=True,
        CreateBookmarks=WD_EXPORT_CREATE_HEADING_BOOKMARKS, DocStructureTags=True,
        BitmapMissingFonts=True, UseISO19005_1=False)


def procesar_con_word(numerar: bool) -> None:
    import win32com.client

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        word.AutomationSecurity = 3
    except Exception:  # noqa: BLE001
        pass
    doc = None
    try:
        doc = word.Documents.Open(str(DOCX_BUILD), ReadOnly=False, AddToRecentFiles=False)
        preparar_pagina(doc)
        arreglar_saltos(doc)
        estilo_cuerpo(doc)
        estilo_titulos(doc)
        estilo_portada(doc)
        estilo_tablas(doc)
        estilo_figuras(doc)
        numerar_paginas(doc)
        print(f"[word] paginas tras el formateo: {doc.ComputeStatistics(2)}")
        if numerar:
            numerar_indices(doc)
        exportar_pdf(doc, PDF_SALIDA)
        print("[word] DOCX intermedio: " + str(DOCX_BUILD))
        print("[word] PDF generado:    " + str(PDF_SALIDA))
    finally:
        if doc is not None:
            try:
                doc.Close(SaveChanges=False)
            except Exception:  # noqa: BLE001
                pass
        word.Quit()


# --------------------------------------------------------------------------
# 4. Verificacion
# --------------------------------------------------------------------------
def rotulos_markdown(texto_md: str) -> list[tuple[str, str]]:
    patron = re.compile(r"(?m)^(?:\*\*|!\[)(Tabla|Figura)\s+([A-Za-z0-9]+(?:\.[0-9]+)?)\.")
    return patron.findall(texto_md)


def verificar(renderizar: bool = False) -> None:
    import pypdfium2 as pdfium

    texto_md = io.open(MD_ORIGEN, encoding="utf-8").read()
    rotulos = rotulos_markdown(texto_md)
    etiquetas_md = {f"{t} {n}." for t, n in rotulos}

    with zipfile.ZipFile(DOCX_BUILD) as z:
        imagenes = [n for n in z.namelist() if n.startswith("word/media/")]

    pdf = pdfium.PdfDocument(str(PDF_SALIDA))
    paginas = len(pdf)
    textos = [pdf[i].get_textpage().get_text_range() for i in range(paginas)]
    todo = "\n".join(textos)
    faltantes = sorted(e for e in etiquetas_md if e not in todo)

    print("\n=== VERIFICACION ===")
    print(f"paginas del PDF              : {paginas}")
    print(f"rotulos en el MD             : {sum(1 for r in rotulos if r[0] == 'Tabla')} tablas, "
          f"{sum(1 for r in rotulos if r[0] == 'Figura')} figuras")
    print(f"rotulos ausentes del PDF     : {len(faltantes)} {faltantes if faltantes else ''}")
    print(f"imagenes embebidas en el DOCX: {len(imagenes)}")
    for marca in ("RESUMEN", "ABSTRACT", "REFERENCIAS BIBLIOGR", "ANEXOS",
                  "KkotjSD5uO4CXI4D", "17/10/2026"):
        print(f"contiene {marca:22}: {'si' if marca in todo else 'NO'}")
    errores = [c for c in ("Error!", "image not found", "COMPLETAR", "TBD", "FIXME")
               if c in todo]
    print(f"marcadores de error          : {errores if errores else 'ninguno'}")
    escasas = [(i + 1, len(t.strip())) for i, t in enumerate(textos) if len(t.strip()) < 250]
    print(f"paginas casi vacias          : {escasas if escasas else 'ninguna'}")

    if renderizar:
        carpeta = CARPETA_BUILD / "paginas"
        carpeta.mkdir(parents=True, exist_ok=True)
        elegidas = {0}
        for i, t in enumerate(textos):
            for marca in ("Figura 1.", "Tabla 5.4.", "Tabla C.1.", "Índice de tablas"):
                if marca in t:
                    elegidas.add(i)
                    break
        for i in sorted(elegidas):
            pdf[i].render(scale=1.4).to_pil().save(carpeta / f"pagina_{i + 1:03}.png")
        print(f"paginas renderizadas: {[i + 1 for i in sorted(elegidas)]}")
    pdf.close()


def main() -> None:
    ap = argparse.ArgumentParser(description="Convierte tesis_v4.md a PDF")
    ap.add_argument("--sin-word", action="store_true")
    ap.add_argument("--sin-numerar-indices", action="store_true")
    ap.add_argument("--renderizar", action="store_true")
    args = ap.parse_args()

    if not MD_ORIGEN.exists():
        raise SystemExit("no existe " + str(MD_ORIGEN))
    print(f"[prep] rutas de figuras resueltas: {preparar_markdown()}")
    correr_pandoc()
    if args.sin_word:
        return
    sin_guionado(DOCX_BUILD)
    procesar_con_word(numerar=not args.sin_numerar_indices)
    verificar(renderizar=args.renderizar)


if __name__ == "__main__":
    main()
