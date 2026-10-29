# -*- coding: utf-8 -*-
"""Comprueba que las cifras clave del informe esten presentes en el Markdown.

No valida la semantica de cada cifra (eso lo hace la comparacion con el PDF
aprobado, tarea 2.5): comprueba que ninguna se haya perdido en la conversion.
"""

import io
import re
import sys

P = r"V4\devoluciones\tesis_v5.md"
s = io.open(P, encoding="utf-8").read()

CLAVES = [
    ("724", "posts del corpus B5"),
    ("352", "casos etiquetados de la validacion"),
    ("0,509", "kappa de Fleiss"),
    ("0,847", "precision"),
    ("0,612", "sensibilidad"),
    ("0,711", "F1"),
    ("235", "amenazas"),
    ("32,5", "porcentaje de amenazas"),
    ("1.376", "minutos de la ventana"),
    ("19,0", "cobertura del motor"),
    ("4.929", "minutos operados"),
    ("17 nodos", "nodos del workflow"),
]

fallos = 0
print("%-10s %-6s %s" % ("cifra", "veces", "descripcion"))
for cifra, desc in CLAVES:
    patron = r"(?<![\d,.])" + re.escape(cifra) + r"(?![\d])"
    n = len(re.findall(patron, s))
    estado = "OK" if n else "FALTA"
    if not n:
        fallos += 1
    print("%-10s %-6d %s  %s" % (cifra, n, desc, estado))

# Coherencia de etiquetas: cada metrica debe nombrarse junto a su cifra.
ETIQUETAS = {
    "kappa": r"kappa|κ",
    "precision": r"precisi[oó]n",
    "sensibilidad": r"sensibilidad",
    "F1": r"F1",
    "amenazas": r"amenazas",
}
print("\netiquetas:")
for nombre, patron in ETIQUETAS.items():
    n = len(re.findall(patron, s, re.I))
    print("  %-14s %d" % (nombre, n))
    if not n:
        fallos += 1

print("\nresultado:", "OK" if not fallos else "%d fallos" % fallos)
sys.exit(0 if not fallos else 1)
