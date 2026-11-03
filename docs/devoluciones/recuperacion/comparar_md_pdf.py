# -*- coding: utf-8 -*-
"""Compara el Markdown reconstruido con el texto del PDF aprobado.

Normalizacion: minusculas y todo caracter no ASCII a espacio. Con eso los
acentos del PDF (que salen como U+FFFD por la codificacion de las fuentes
incrustadas) y los del Markdown caen en la misma posicion y no generan ruido.

El PDF extrae las tablas por columnas y corta palabras por justificacion
("cread as" por "creadas"). Para separar ese ruido de una diferencia real:

- un token del PDF se considera presente si aparece en una ventana de +/-2500
  caracteres alrededor del punto de insercion en el Markdown, o si (con 3 o mas
  letras) es subcadena del texto de la ventana sin espacios (corte de palabra);
- un token del Markdown se considera presente si aparece en cualquier parte del
  texto del PDF, con la misma regla de subcadena.
"""

import bisect
import collections
import datetime
import difflib
import hashlib
import io
import re

import pypdfium2 as pdfium

MD = r"V4\devoluciones\tesis_v5.md"
PDF = r"V4\devoluciones\recuperacion\tesis_v5_aprobado_2026-10-28.pdf"
SALIDA = r"V4\devoluciones\build\diff_contenido.md"
VENTANA = 2500


def normalizar(texto: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", texto.lower())


def tokens_con_posiciones(norm: str):
    toks = norm.split()
    pos, i = [], 0
    for t in toks:
        j = norm.index(t, i)
        pos.append((j, j + len(t)))
        i = j + len(t)
    return toks, pos


def recortar(norm, pos, a, b, margen=140):
    ini = max(0, pos[a][0] - margen) if a < len(pos) else len(norm)
    fin = min(len(norm), pos[b - 1][1] + margen) if b > a else ini + margen
    return re.sub(r"\s+", " ", norm[ini:fin]).strip()


def sha(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 16), b""):
            h.update(bloque)
    return h.hexdigest()


def main():
    pdf = pdfium.PdfDocument(PDF)
    texto_pdf = "\n".join(pdf[i].get_textpage().get_text_range() for i in range(len(pdf)))
    npaginas = len(pdf)
    pdf.close()

    texto_md = io.open(MD, encoding="utf-8").read()
    # Las rutas y anchos de las imagenes no son texto del PDF: se conserva solo
    # el epigrafe (texto alternativo), que si aparece bajo cada figura.
    texto_md = re.sub(r"!\[([^\]]*)\]\([^)]*\)(?:\{[^}]*\})?", r"\1", texto_md)

    lineas = texto_md.split("\n")
    partes = [normalizar(l) for l in lineas]
    inicios, cursor = [], 0
    for parte in partes:
        inicios.append(cursor)
        cursor += len(parte) + 1
    norm_md = " ".join(partes)

    norm_pdf = normalizar(texto_pdf)
    tok_pdf, pos_pdf = tokens_con_posiciones(norm_pdf)
    tok_md, pos_md = tokens_con_posiciones(norm_md)
    cnt_pdf_total = collections.Counter(norm_pdf.split())
    plano_pdf = norm_pdf.replace(" ", "")

    sm = difflib.SequenceMatcher(None, tok_pdf, tok_md, autojunk=False)
    ratio = sm.ratio()
    bloques = [op for op in sm.get_opcodes() if op[0] != "equal"]

    def ancla(j):
        return min(max(j, 0), len(pos_md) - 1) if pos_md else -1

    def ventana(j):
        if not pos_md:
            return collections.Counter(), ""
        j = ancla(j)
        ini = max(0, pos_md[j][0] - VENTANA)
        fin = min(len(norm_md), pos_md[j][1] + VENTANA)
        trozo = norm_md[ini:fin]
        return collections.Counter(trozo.split()), trozo.replace(" ", "")

    def lineas_de(j1, j2):
        if not pos_md:
            return set()
        if j1 >= j2:
            j1, j2 = ancla(j1), ancla(j1) + 1
        a = bisect.bisect_right(inicios, pos_md[j1][0]) - 1
        b = bisect.bisect_right(inicios, pos_md[min(j2, len(pos_md)) - 1][1]) - 1
        return set(range(a, b + 1))

    def en_tabla(j1, j2):
        idx = lineas_de(j1, j2)
        ampliado = set()
        for i in idx:
            ampliado.update(range(max(0, i - 1), min(len(lineas), i + 2)))
        return any(lineas[i].startswith("|") for i in ampliado)

    def encabezado_previo(j1):
        """Tokens del encabezado de la ultima tabla antes del punto de anclaje."""
        idx = lineas_de(j1, j1 + 1)
        if not idx:
            return set()
        i = max(idx)
        while i >= 0 and not lineas[i].startswith("|"):
            i -= 1
        if i < 0:
            return set()
        while i > 0 and lineas[i - 1].startswith("|"):
            i -= 1
        return set(normalizar(lineas[i]).split())


    filas = []
    perdidos_total = collections.Counter()
    agregados_total = collections.Counter()
    for tag, i1, i2, j1, j2 in bloques:
        cnt, plano = ventana(j1)
        perdidos = []
        for t, n in collections.Counter(tok_pdf[i1:i2]).items():
            if len(t) < 3:
                continue          # fragmento de corte por justificacion
            if cnt[t] >= n:
                continue
            if t in plano:
                continue
            perdidos.append(t)
        agregados = []
        for t, n in collections.Counter(tok_md[j1:j2]).items():
            if len(t) < 3:
                continue
            if cnt_pdf_total[t] >= n:
                continue
            if t in plano_pdf:
                continue
            agregados.append(t)
        perdidos_total.update(perdidos)
        agregados_total.update(agregados)
        filas.append({
            "tag": tag, "i1": i1, "i2": i2, "j1": j1, "j2": j2,
            "tabla": en_tabla(j1, j2), "perdidos": perdidos, "agregados": agregados,
            "peso": max(i2 - i1, j2 - j1),
            "encabezado": bool(perdidos) and set(perdidos) <= encabezado_previo(j1),
        })

    reales = [f for f in filas if f["perdidos"] or f["agregados"]]
    pendientes = [f for f in reales if not f["encabezado"]]
    total_pdf = sum(i2 - i1 for _, i1, i2, _, _ in bloques)
    total_md = sum(j2 - j1 for _, _, _, j1, j2 in bloques)

    out = []
    out.append("# Diferencia de contenido entre el Markdown reconstruido y el PDF aprobado\n")
    out.append(f"Fecha: {datetime.datetime.now():%Y-%m-%d %H:%M}\n")
    out.append(f"- Markdown: `{MD}` (sha256 `{sha(MD)[:16]}…`)")
    out.append(f"- PDF aprobado: `{PDF}` ({npaginas} páginas, sha256 `{sha(PDF)[:16]}…`)")
    out.append(f"- Tokens normalizados: PDF {len(tok_pdf)}, Markdown {len(tok_md)}")
    out.append(f"- Similitud de secuencia: **{ratio:.4f}** (umbral 0,97)")
    out.append(f"- Bloques distintos: {len(bloques)} "
               f"({sum(1 for f in filas if f['tabla'])} en tablas, "
               f"{sum(1 for f in filas if not f['tabla'])} en texto)")
    out.append(f"- Tokens afectados: {total_pdf} en el PDF, {total_md} en el Markdown")
    out.append(f"- Bloques con contenido ausente del otro lado: **{len(pendientes)}**"
               f" (más {len(reales) - len(pendientes)} con solo el encabezado repetido de una tabla)\n")
    out.append("Normalización: minúsculas; todo carácter no ASCII se reemplaza por espacio. "
               "Los acentos del PDF salen como U+FFFD por la codificación de las fuentes "
               "incrustadas y quedan en la misma posición que los del Markdown. Un token cuenta "
               "como presente si aparece en la ventana local (±2500 caracteres) o, con 3 o más "
               "letras, como subcadena del texto sin espacios (corte de palabra por "
               "justificación: `cread as`). Los tokens de 1 y 2 letras se ignoran: el PDF los "
               "produce al partir palabras (`r ne tsec`).\n")

    out.append("## Bloques con contenido ausente\n")
    if not pendientes:
        out.append("Ninguno: todas las diferencias son de orden o segmentación; no hay "
                   "palabras del PDF que falten en el Markdown ni palabras del Markdown que "
                   "falten en el PDF.\n")
    for n, f in enumerate(reales, 1):
        out.append(f"### R{n}. {f['tag']} — PDF {f['i2'] - f['i1']} / Markdown {f['j2'] - f['j1']} tokens"
                   f"{' (tabla)' if f['tabla'] else ''}\n")
        if f["encabezado"]:
            out.append("Tocados todos por el **encabezado repetido** de una tabla: Word repite la "
                       "fila de títulos en cada página y el PDF la contiene varias veces, mientras "
                       "que el Markdown la tiene una sola vez. No es contenido ausente.\n")
        if f["perdidos"]:
            out.append("Tokens del PDF ausentes en el Markdown: "
                       + ", ".join(f"`{t}`" for t in f["perdidos"][:40]) + "\n")
        if f["agregados"]:
            out.append("Tokens del Markdown ausentes en el PDF: "
                       + ", ".join(f"`{t}`" for t in f["agregados"][:40]) + "\n")
        out.append("PDF aprobado:\n")
        out.append("> " + (recortar(norm_pdf, pos_pdf, f["i1"], f["i2"]) or "(vacío)") + "\n")
        out.append("Markdown:\n")
        out.append("> " + (recortar(norm_md, pos_md, f["j1"], f["j2"]) or "(vacío)") + "\n")

    out.append("## Bloques de 8 tokens o más\n")
    out.append("| # | tipo | dónde | tokens PDF | tokens MD | contexto en el PDF |")
    out.append("|---|------|-------|-----------:|----------:|--------------------|")
    for n, f in enumerate([f for f in filas if f["peso"] >= 8], 1):
        ctx = recortar(norm_pdf, pos_pdf, f["i1"], f["i2"], margen=60).replace("|", "\\|")
        out.append(f"| {n} | {f['tag']} | {'tabla' if f['tabla'] else 'texto'} | "
                   f"{f['i2'] - f['i1']} | {f['j2'] - f['j1']} | {ctx[:170]} |")

    out.append("\n## Bloques menores\n")
    out.append("| # | tipo | dónde | tokens PDF | tokens MD | contexto en el Markdown |")
    out.append("|---|------|-------|-----------:|----------:|-------------------------|")
    for n, f in enumerate([f for f in filas if f["peso"] < 8], 1):
        ctx = recortar(norm_md, pos_md, f["j1"], f["j2"], margen=60).replace("|", "\\|")
        out.append(f"| {n} | {f['tag']} | {'tabla' if f['tabla'] else 'texto'} | "
                   f"{f['i2'] - f['i1']} | {f['j2'] - f['j1']} | {ctx[:160]} |")

    io.open(SALIDA, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print(f"similitud {ratio:.4f} | bloques {len(bloques)} | reales {len(reales)} "
          f"| perdidos {sum(perdidos_total.values())} | agregados {sum(agregados_total.values())}")
    if reales:
        print("reales:", [(f["tag"], f["perdidos"][:6], f["agregados"][:6]) for f in reales[:10]])
    print("escrito", SALIDA)


if __name__ == "__main__":
    main()
