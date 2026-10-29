# -*- coding: utf-8 -*-
"""Compuertas de verificacion del PDF de la tesis.

Comprueba sobre el PDF final y el DOCX intermedio:

- cantidad de paginas y tamano A4 de todas las paginas;
- fuentes del cuerpo (Times New Roman presente, Aptos ausente);
- margenes 25/25/30/20 mm;
- ninguna pagina con menos de 40 caracteres;
- las tres listas de indice con numero de pagina en cada entrada (10/28/4);
- ausencia de `@@@` y de entradas de indice sin numero;
- todos los rotulos del Markdown presentes en el PDF (32 tablas, 4 figuras);
- portada en una sola pagina;
- similitud de tokens contra el PDF aprobado (>= 0,97).

Escribe `V4/devoluciones/build/verificacion_pdf.json` y un resumen de texto.
Termina con codigo distinto de cero si alguna compuerta falla.

Uso:
    python V4/scripts/verificar_pdf.py
    python V4/scripts/verificar_pdf.py --pdf ... --md ... --docx ... --aprobado ...
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import io
import json
import os
import re
import sys
import xml.sax.saxutils
import zipfile
from pathlib import Path

import pypdfium2 as pdfium

RAIZ = Path(__file__).resolve().parents[2]
MD_POR_DEFECTO = RAIZ / "V4" / "devoluciones" / "tesis_v5.md"
PDF_POR_DEFECTO = RAIZ / "V4" / "devoluciones" / "tesis_v5.pdf"
DOCX_POR_DEFECTO = Path(os.environ.get("TEMP", "/tmp")) / "tfi_tesis_build" / "tesis_v5.docx"
APROBADO_POR_DEFECTO = (RAIZ / "V4" / "devoluciones" / "recuperacion"
                        / "tesis_v5_aprobado_2026-10-28.pdf")
REGISTRO = RAIZ / "V4" / "devoluciones" / "build" / "verificacion_pdf.json"

A4 = (595.3, 841.9)
TOLERANCIA_PT = 2.0
MARGENES_TWIPS = {"top": 1417, "bottom": 1417, "left": 1701, "right": 1134}
TOLERANCIA_TWIPS = 30
INDICES = {"Índice general": 10, "Índice de tablas": 28, "Índice de figuras": 4}
CARACTERES_MINIMOS = 40
SIMILITUD_MINIMA = 0.97


def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 16), b""):
            h.update(bloque)
    return h.hexdigest()


def texto_pdf(ruta: Path) -> tuple[list[str], float, float]:
    doc = pdfium.PdfDocument(str(ruta))
    paginas = [doc[i].get_textpage().get_text_range() for i in range(len(doc))]
    ancho, alto = doc[0].get_size()
    doc.close()
    return paginas, ancho, alto


def tamano_paginas(ruta: Path) -> tuple[bool, str]:
    doc = pdfium.PdfDocument(str(ruta))
    malas = []
    for i in range(len(doc)):
        ancho, alto = doc[i].get_size()
        if abs(ancho - A4[0]) > TOLERANCIA_PT or abs(alto - A4[1]) > TOLERANCIA_PT:
            malas.append(f"{i + 1}:{ancho:.0f}x{alto:.0f}")
    n = len(doc)
    doc.close()
    return (not malas), f"{n} paginas; fuera de A4: {malas[:6] if malas else 'ninguna'}"


PATRON_TEXTO = re.compile(r"<w:tab\s*/>|<w:t(?:\s[^>]*)?>(.*?)</w:t>", re.S)
# Word traduce los ids de pandoc a los nombres locales del estilo (Ttulo1..3).
ES_TITULO = re.compile(r"^(?:Heading[123]|Ttulo[123]|Title)$")


def parrafos_docx(docx: Path) -> list[tuple[str, str]]:
    """(estilo, texto) de cada parrafo, en orden."""
    with zipfile.ZipFile(docx) as z:
        documento = z.read("word/document.xml").decode("utf-8")
    salida = []
    for p in re.findall(r"<w:p(?:\s[^>]*)?>.*?</w:p>", documento, re.S):
        estilo = re.search(r'<w:pStyle w:val="([^"]+)"', p)
        texto = ""
        for m in PATRON_TEXTO.finditer(p):
            if m.group(0).startswith("<w:tab"):
                texto += "\t"
            else:
                texto += xml.sax.saxutils.unescape(m.group(1))
        salida.append((estilo.group(1) if estilo else "", texto.strip()))
    return salida


ENCABEZADO_INDICE = {"ÍNDICE GENERAL", "ÍNDICE DE TABLAS", "ÍNDICE DE FIGURAS"}


def compuerta_indices_pdf(paginas: list[str]) -> tuple[bool, str]:
    """Cada entrada de los tres indices, leida del PDF, debe terminar en pagina."""
    actual, conteo = None, {}
    for linea in "\n".join(paginas).splitlines():
        s = linea.strip()
        if not s or s.isdigit():
            continue
        if s.upper() in ENCABEZADO_INDICE:
            actual = s.upper()
            conteo[actual] = {"entradas": 0, "numeradas": 0}
            continue
        if not actual:
            continue
        # Solo son entradas del indice las que llevan puntos guia o empiezan como
        # rotulo ("Tabla 5.9.b.") o capitulo ("3. Marco..."). Cualquier otra linea
        # cierra la seccion.
        if not ("..." in s or re.match(r"^(?:Tabla|Figura)\s|\d+\.\s", s)):
            actual = None
            continue
        conteo[actual]["entradas"] += 1
        if re.search(r"\d\s*$", s):
            conteo[actual]["numeradas"] += 1
    detalle = {k: f"{v['numeradas']}/{v['entradas']}" for k, v in conteo.items()}
    ok = (len(conteo) == 3 and all(v["entradas"] and v["numeradas"] == v["entradas"]
                                   for v in conteo.values()))
    return ok, f"entradas numeradas por indice: {detalle}"


def compuerta_indices(docx: Path) -> tuple[bool, str, dict]:
    parrafos = parrafos_docx(docx)
    nombres = {k.lower(): k for k in INDICES}
    activo, conteo, sin_numero = None, {}, []
    for estilo, texto in parrafos:
        if ES_TITULO.match(estilo):
            activo = nombres.get(texto.strip().lower())
            continue
        if not activo or not texto:
            continue
        conteo[activo] = conteo.get(activo, 0) + 1
        if not re.search(r"\t\d{1,3}$", texto):
            sin_numero.append(f"{activo}: {texto[:60]!r}")
    detalles = {k: conteo.get(k, 0) for k in INDICES}
    ok = (detalles == INDICES) and not sin_numero
    return ok, f"entradas {detalles} (esperado {INDICES}); sin numero: " \
               f"{sin_numero[:5] if sin_numero else 'ninguna'}", detalles


def compuerta_fuentes(docx: Path) -> tuple[bool, str]:
    with zipfile.ZipFile(docx) as z:
        documento = z.read("word/document.xml").decode("utf-8")
        estilos = z.read("word/styles.xml").decode("utf-8")
    times = documento.count('w:ascii="Times New Roman"') + estilos.count('w:ascii="Times New Roman"')
    aptos = re.findall(r'w:ascii="Aptos[^"]*"', documento + estilos)
    ok = times > 0 and not aptos
    return ok, f"Times New Roman en {times} definiciones; Aptos: {len(aptos)}"


def compuerta_margenes(docx: Path) -> tuple[bool, str]:
    with zipfile.ZipFile(docx) as z:
        documento = z.read("word/document.xml").decode("utf-8")
    margenes = re.search(r"<w:pgMar\b[^>]*>", documento)
    if not margenes:
        return False, "sin w:pgMar"
    valores = {k: int(v) for k, v in re.findall(r'w:(top|bottom|left|right)="(-?\d+)"',
                                               margenes.group(0))}
    malos = {k: valores.get(k) for k, esperado in MARGENES_TWIPS.items()
             if abs(valores.get(k, -99999) - esperado) > TOLERANCIA_TWIPS}
    return not malos, f"{valores}; fuera de rango: {malos if malos else 'ninguno'}"


def compuerta_rotulos(md: Path, docx: Path, todo_pdf: str) -> tuple[bool, str]:
    texto = io.open(md, encoding="utf-8").read()
    rotulos = re.findall(
        r"(?m)^(?:\*\*|!\[)(Tabla|Figura)\s+([A-Za-z0-9]+(?:\.[0-9]+)*(?:\.[a-z])?)\.",
        texto)
    etiquetas = {f"{t} {n}." for t, n in rotulos}
    faltantes = sorted(e for e in etiquetas if e not in todo_pdf)
    tablas = sum(1 for t, _ in rotulos if t == "Tabla")
    figuras = sum(1 for t, _ in rotulos if t == "Figura")
    with zipfile.ZipFile(docx) as z:
        cuerpo = z.read("word/document.xml").decode("utf-8")
    tablas_docx = cuerpo.count("<w:tbl>")
    ok = (not faltantes and tablas == 28 and figuras == 4 and tablas_docx == 32)
    return ok, f"{tablas} rotulos de tabla y {figuras} de figura; tablas en el DOCX: " \
               f"{tablas_docx} (esperado 32); ausentes: {faltantes[:6] if faltantes else 'ninguno'}"


def compuerta_portada(paginas: list[str]) -> tuple[bool, str]:
    if len(paginas) < 2:
        return False, "menos de 2 paginas"
    p1, p2 = paginas[0], paginas[1]
    ok = ("SISTEMA AUTOMATIZADO" in p1.upper() and "Mendoza, Argentina" in p1
          and "Mendoza, Argentina" not in p2
          and "Versión del documento" in p2)
    return ok, ("portada en la pagina 1 y nota de version en la 2"
                if ok else "la portada no cierra en una pagina")


def similitud(texto_final: str, texto_aprobado: str) -> float:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.path.insert(0, str(RAIZ / "V4" / "devoluciones" / "recuperacion"))
    import comparar_md_pdf as cmp  # noqa: PLC0415

    a = cmp.normalizar(texto_aprobado).split()
    b = cmp.normalizar(texto_final).split()
    return difflib_ratio(a, b)


def difflib_ratio(a: list[str], b: list[str]) -> float:
    import difflib

    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def ejecutar(pdf: Path, md: Path, docx: Path, aprobado: Path | None,
             escribir: bool = True) -> int:
    compuertas = []

    def anotar(nombre: str, ok: bool, detalle: str) -> None:
        compuertas.append({"compuerta": nombre, "ok": ok, "detalle": detalle})
        print(f"[{ 'OK ' if ok else 'FALLA' }] {nombre:22} {detalle}")

    if not pdf.exists():
        anotar("pdf_existe", False, f"no existe {pdf}")
        return 1
    paginas, ancho, alto = texto_pdf(pdf)
    crudo = "\n".join(paginas)
    # Word deja glifos sin mapear (U+FFFE) en la capa de texto del PDF; el
    # glifo se dibuja bien, pero ensucia la extraccion. Se cuentan y se quitan
    # antes de comparar. El mismo defecto aparece en tesis_v4.pdf y en el PDF
    # aprobado, asi que no es una compuerta.
    nonchars = crudo.count("\ufffe") + crudo.count("\ufffd")
    print(f"[info] glifos sin mapear en la capa de texto: {nonchars}")
    todo = crudo.replace("\ufffe", "").replace("\ufffd", "")

    ok, detalle = tamano_paginas(pdf)
    anotar("tamano_a4", ok, detalle)

    flojas = [(i + 1, len(t.strip())) for i, t in enumerate(paginas)
              if len(t.strip()) < CARACTERES_MINIMOS]
    anotar("paginas_con_texto", not flojas,
           f"{len(paginas)} paginas; con menos de {CARACTERES_MINIMOS} caracteres: "
           f"{flojas[:6] if flojas else 'ninguna'}")

    ok, detalle, conteo = compuerta_indices(docx)
    anotar("indices_numerados", ok, detalle)

    ok, detalle = compuerta_indices_pdf(paginas)
    anotar("indices_en_pdf", ok, detalle)

    ok = "@@@" not in todo
    anotar("sin_marcadores", ok, "sin '@@@'" if ok else "aparece '@@@'")

    ok, detalle = compuerta_fuentes(docx)
    anotar("fuentes", ok, detalle)

    ok, detalle = compuerta_margenes(docx)
    anotar("margenes", ok, detalle)

    ok, detalle = compuerta_rotulos(md, docx, todo)
    anotar("rotulos", ok, detalle)

    ok, detalle = compuerta_portada(paginas)
    anotar("portada_una_pagina", ok, detalle)

    if aprobado and aprobado.exists():
        paginas_ap, _, _ = texto_pdf(aprobado)
        ratio = similitud(todo, "\n".join(paginas_ap))
        ok = ratio >= SIMILITUD_MINIMA
        anotar("similitud_aprobado", ok,
               f"{ratio:.4f} (minimo {SIMILITUD_MINIMA})")
    else:
        anotar("similitud_aprobado", False, "no se encontro el PDF aprobado")

    fallos = [c for c in compuertas if not c["ok"]]
    registro = {
        "fecha": datetime.datetime.now().isoformat(timespec="seconds"),
        "pdf": str(pdf),
        "sha256": sha256(pdf),
        "paginas": len(paginas),
        "tamano_pagina_pt": [round(ancho, 1), round(alto, 1)],
        "entradas_indice": conteo,
        "compuertas": compuertas,
        "ok": not fallos,
    }
    if escribir:
        REGISTRO.parent.mkdir(parents=True, exist_ok=True)
        io.open(REGISTRO, "w", encoding="utf-8", newline="\n").write(
            json.dumps(registro, ensure_ascii=False, indent=2) + "\n")
        resumen = REGISTRO.with_suffix(".txt")
        lineas = [f"Verificacion del PDF — {registro['fecha']}",
                  f"PDF: {pdf} ({len(paginas)} paginas) sha256 {registro['sha256']}"]
        lineas += [f"{'OK ' if c['ok'] else 'FALLA'}  {c['compuerta']}: {c['detalle']}"
                   for c in compuertas]
        lineas.append("RESULTADO: " + ("OK" if registro["ok"] else f"{len(fallos)} fallas"))
        io.open(resumen, "w", encoding="utf-8", newline="\n").write("\n".join(lineas) + "\n")
        print("registro:", REGISTRO)
    return 0 if registro["ok"] else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Verifica el PDF de la tesis contra el PDF aprobado")
    ap.add_argument("--pdf", type=Path, default=PDF_POR_DEFECTO)
    ap.add_argument("--md", type=Path, default=MD_POR_DEFECTO)
    ap.add_argument("--docx", type=Path, default=DOCX_POR_DEFECTO)
    ap.add_argument("--aprobado", type=Path, default=APROBADO_POR_DEFECTO)
    ap.add_argument("--sin-registro", action="store_true")
    args = ap.parse_args(argv)
    return ejecutar(args.pdf, args.md, args.docx, args.aprobado,
                    escribir=not args.sin_registro)


if __name__ == "__main__":
    sys.exit(main())
