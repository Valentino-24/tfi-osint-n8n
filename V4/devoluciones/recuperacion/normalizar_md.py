# -*- coding: utf-8 -*-
"""Normaliza la salida de Pandoc (DOCX -> GFM) a la fuente Markdown de la V5.

Decisiones:
- Las figuras llegan como HTML crudo (<figure><img ...>); el escritor de docx
  descarta HTML, asi que se convierten a la sintaxis de figura de Pandoc y se
  apuntan a las imagenes ya versionadas en V4/figuras/ (verificadas identicas
  por SHA-256 a las extraidas del DOCX).
- Se desescapa solo la puntuacion escapable de CommonMark, y nunca dentro de
  code spans ni bloques de codigo: ahi un backslash es contenido (regex, SQL).
- Los rotulos "Tabla ..." / "Figura ..." se dejan como parrafos: el conversor
  los detecta con ROTULO y los pone en negrita.
"""

import io
import re

ORIGEN = r"V4\devoluciones\recuperacion\tesis_v5_desde_docx.md"
DESTINO = r"V4\devoluciones\tesis_v5.md"

FIGURAS = {
    "image1.png": "Figura_1_arquitectura.png",
    "image2.png": "Figura_2_der.png",
    "image3.png": "Figura_3_workflow.png",
    "image4.png": "Figura_4_serie_temporal.png",
}

PUNTUACION = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
RE_ESCAPE = re.compile(r"\\([" + re.escape(PUNTUACION) + r"])")


def convertir_figura(bloque: str) -> str:
    img = re.search(r"image(\d)\.png", bloque)
    alt = re.search(r'alt="([^"]*)"', bloque)
    ancho = re.search(r"width:([0-9.]+in)", bloque)
    if not (img and alt and ancho):
        raise SystemExit("figura sin imageN/alt/width:\n" + bloque)
    ruta = FIGURAS["image%s.png" % img.group(1)]
    return "![%s](../figuras/%s){width=%s}" % (alt.group(1), ruta, ancho.group(1))


def desescapar(linea: str) -> str:
    """Desescapa puntuacion CommonMark fuera de los code spans."""
    partes = linea.split("`")
    for i in range(0, len(partes), 2):      # indices pares = fuera de code
        partes[i] = RE_ESCAPE.sub(r"\1", partes[i])
    return "`".join(partes)


def normalizar_heading(linea: str) -> str | None:
    m = re.match(r"^(#{1,6})\s*(.*?)\s*$", linea)
    if not m:
        return linea
    titulo = m.group(2).strip()
    if not titulo:
        return None                          # heading vacio: se descarta
    return "%s %s" % (m.group(1), titulo)


def main() -> None:
    texto = io.open(ORIGEN, encoding="utf-8").read().replace("\r\n", "\n")

    # 1) Figuras HTML -> sintaxis Markdown (antes de tocar lineas).
    texto, nfig = re.subn(r"<figure>.*?</figure>", lambda m: convertir_figura(m.group(0)),
                          texto, flags=re.S)
    print("[figuras] convertidas:", nfig)

    lineas = texto.split("\n")
    salida: list[str] = []
    en_codigo = False
    previa_blanca = True
    for linea in lineas:
        es_sangria = linea.startswith("    ") or linea.startswith("\t")
        if en_codigo:
            if es_sangria or not linea.strip():
                salida.append(linea.rstrip("\r"))
                previa_blanca = not linea.strip()
                continue
            en_codigo = False
        if es_sangria and previa_blanca:
            en_codigo = True
            salida.append(linea.rstrip("\r"))
            previa_blanca = False
            continue

        l = linea.replace("\xa0", " ")       # NBSP -> espacio comun
        l = desescapar(l)
        l = normalizar_heading(l)
        if l is None:
            previa_blanca = True
            continue
        l = l.rstrip()
        if not l:
            if previa_blanca and (not salida or salida[-1] == ""):
                continue                      # no acumular lineas en blanco
            previa_blanca = True
        else:
            previa_blanca = False
        salida.append(l)

    # 2) Una sola linea en blanco entre titulos y el resto.
    limpio: list[str] = []
    for i, l in enumerate(salida):
        if l.startswith("#") and limpio and limpio[-1] != "":
            limpio.append("")
        limpio.append(l)
        if l.startswith("#") and i + 1 < len(salida) and salida[i + 1].strip():
            limpio.append("")

    while limpio and limpio[-1] == "":
        limpio.pop()
    resultado = "\n".join(limpio) + "\n"
    io.open(DESTINO, "w", encoding="utf-8", newline="\n").write(resultado)
    print("[ok] escrito", DESTINO, len(resultado), "bytes,", len(limpio), "lineas")


if __name__ == "__main__":
    main()
