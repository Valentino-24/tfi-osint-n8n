# -*- coding: utf-8 -*-
"""Verifica que un pulido editorial no haya roto la evidencia del informe.

Uso:
    python V4/scripts/verificar_pulido.py ORIGINAL.md PULIDO.md

PULIDO.md puede ser el informe completo o un solo capitulo devuelto por Claude:
se comparan las secciones (titulos de nivel 1) que existan en ambos archivos.
Comprueba, seccion por seccion: numeros, rotulos de tabla y figura, encabezados,
filas de tabla, referencias, citas en linea, enlaces de figuras y extension.
Sale con codigo 1 si algun control falla.
"""
import collections
import difflib
import io
import re
import sys

TOLERANCIA = 0.10          # el pulido puede mover la extension como maximo un 10 %
PATRON_NUM = re.compile(r"\d+(?:[.,]\d+)*")
PATRON_ROTULO = re.compile(r"\b(Tabla|Figura)\s+([A-Za-z0-9]+(?:\.[0-9]+)?)\.")
PATRON_ENCAB = re.compile(r"(?m)^(#{1,6})\s+(.*)$")
PATRON_CITA = re.compile(r"\(([^()]{3,70}?,\s*(?:19|20)\d\d[a-z]?)\)")
PATRON_FIGURA = re.compile(r"!\[[^\]]*\]\([^)]*\)")
PATRON_TRUNCADO = re.compile(
    r"\.\.\.\s*$|^\s*\.\.\.|el resto (?:queda|permanece|se mantiene) (?:igual|sin cambios)|"
    r"\[(?:resto|omitido|continua|continúa)|<<<|SIGUE IGUAL", re.I | re.M)


def leer(ruta: str) -> str:
    return io.open(ruta, encoding="utf-8").read().replace("\r\n", "\n")


def secciones(texto: str) -> "collections.OrderedDict[str, str]":
    """Devuelve {titulo de nivel 1: cuerpo} conservando el orden."""
    partes = collections.OrderedDict()
    actual = "(preliminares)"
    partes[actual] = []
    for linea in texto.split("\n"):
        m = re.match(r"^#\s+(.*)$", linea)
        if m:
            actual = m.group(1).strip()
            partes[actual] = []
        else:
            partes[actual].append(linea)
    return collections.OrderedDict((k, "\n".join(v)) for k, v in partes.items())


def filas_por_tabla(texto: str) -> list[int]:
    """Cantidad de filas de cada tabla (bloques consecutivos de lineas con |)."""
    filas, dentro = [], False
    for linea in texto.split("\n"):
        es_fila = linea.lstrip().startswith("|")
        if es_fila and not dentro:
            filas.append(0)
            dentro = True
        if es_fila:
            filas[-1] += 1
        elif dentro:
            dentro = False
    return filas


def encabezados(texto: str) -> list[tuple[int, str]]:
    return [(len(m.group(1)), m.group(2).strip()) for m in PATRON_ENCAB.finditer(texto)]


def compara_multiconjunto(etiqueta: str, a: str, b: str, patron, clave=None) -> list[str]:
    clave = clave or (lambda m: m)
    ca = collections.Counter(clave(m) for m in patron.findall(a))
    cb = collections.Counter(clave(m) for m in patron.findall(b))
    faltan = ca - cb
    sobran = cb - ca
    if not faltan and not sobran:
        print(f"  OK    {etiqueta}: {sum(ca.values())} elementos, sin diferencias")
        return []
    avisos = []
    if faltan:
        avisos.append(f"{etiqueta}: FALTAN en el pulido -> {dict(faltan)}")
    if sobran:
        avisos.append(f"{etiqueta}: APARECEN de mas en el pulido -> {dict(sobran)}")
    print(f"  FALLA {etiqueta}: faltan {len(faltan)} / sobran {len(sobran)}")
    return avisos


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    original, pulido = leer(sys.argv[1]), leer(sys.argv[2])
    sec_orig = secciones(original)
    sec_pul = secciones(pulido)
    avisos: list[str] = []

    print(f"original: {sys.argv[1]}  ({len(original.split())} palabras)")
    print(f"pulido  : {sys.argv[2]}  ({len(pulido.split())} palabras)")

    comunes = [t for t in sec_pul if t in sec_orig]
    if not comunes:
        print("FALLA  no hay ninguna seccion con el mismo titulo en los dos archivos")
        return 1
    faltantes_de_estructura = [t for t in sec_orig if t not in sec_pul]
    print(f"\nsecciones comparadas: {len(comunes)}"
          + (f" | no incluidas en el pulido: {len(faltantes_de_estructura)}" if faltantes_de_estructura else ""))

    truncado = [i + 1 for i, l in enumerate(pulido.split("\n")) if PATRON_TRUNCADO.search(l)]
    if truncado:
        avisos.append(f"respuesta truncada o resumida en las lineas {truncado[:8]}")
        print(f"\nFALLA  marcas de texto resumido/truncado: lineas {truncado[:8]}")
    else:
        print("\nOK    sin marcas de texto resumido")

    for titulo in comunes:
        a, b = sec_orig[titulo], sec_pul[titulo]
        print(f"\n=== {titulo[:70]} ===")
        avisos += compara_multiconjunto("numeros", a, b, PATRON_NUM)
        avisos += compara_multiconjunto("rotulos tabla/figura", a, b, PATRON_ROTULO,
                                       clave=lambda m: f"{m[0]} {m[1]}.")

        ea, eb = encabezados(a), encabezados(b)
        if ea == eb:
            print(f"  OK    encabezados: {len(ea)} y en el mismo orden")
        else:
            solo_a = [f"{'#' * n} {t}" for n, t in ea if (n, t) not in eb]
            solo_b = [f"{'#' * n} {t}" for n, t in eb if (n, t) not in ea]
            avisos.append(f"encabezados distintos en '{titulo}': faltan {solo_a[:3]} / aparecen {solo_b[:3]}")
            print(f"  FALLA encabezados: faltan {solo_a[:3]} / aparecen {solo_b[:3]}")

        fa, fb = filas_por_tabla(a), filas_por_tabla(b)
        if fa == fb:
            print(f"  OK    filas por tabla: {fa}")
        else:
            avisos.append(f"tablas distintas en '{titulo}': original {fa} / pulido {fb}")
            print(f"  FALLA filas por tabla: original {fa} / pulido {fb}")

        fig_a, fig_b = PATRON_FIGURA.findall(a), PATRON_FIGURA.findall(b)
        if fig_a == fig_b:
            print(f"  OK    enlaces de figuras: {len(fig_a)} intactos")
        else:
            avisos.append(f"enlaces de figuras distintos en '{titulo}'")
            print("  FALLA enlaces de figuras")

        avisos += compara_multiconjunto("citas en linea", a, b, PATRON_CITA)

        pa, pb = len(a.split()), len(b.split())
        delta = (pb - pa) / pa if pa else 0
        estado = "OK   " if abs(delta) <= TOLERANCIA else "FALLA"
        print(f"  {estado} extension: {pa} -> {pb} palabras ({delta:+.1%})")
        if abs(delta) > TOLERANCIA:
            avisos.append(f"extension fuera de tolerancia en '{titulo}': {delta:+.1%}")

    # Referencias: la lista completa debe conservarse aunque se pulan capitulos sueltos
    if "REFERENCIAS" in "".join(sec_pul).upper():
        ref_a = [l for l in secciones(original).get("REFERENCIAS", "").split("\n") if l.strip()]
        ref_b = [l for l in sec_pul.get("REFERENCIAS", "").split("\n") if l.strip()]
        if len(ref_a) != len(ref_b):
            avisos.append(f"referencias: {len(ref_a)} entradas en el original, {len(ref_b)} en el pulido")
            print(f"\nFALLA  referencias: {len(ref_a)} -> {len(ref_b)} entradas")
        else:
            print(f"\nOK    referencias: {len(ref_a)} entradas")

    print("\n=== RESULTADO ===")
    if avisos:
        for a in avisos:
            print(f"  - {a}")
        print(f"FALLA: {len(avisos)} control(es). No apliques el pulido sin resolverlos.")
        return 1
    print("Todo verificado: el pulido no altero cifras, rotulos, encabezados, tablas, citas ni figuras.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
