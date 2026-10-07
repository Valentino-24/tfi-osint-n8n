"""Reetiqueta la seccion 4 de las bitacoras ya archivadas.

Lo que cambia (y lo unico):
  - el SELECT y el GROUP BY de la consulta pasan de ventana_fin a ventana_inicio
  - las filas del resultado se recorren 1 dia hacia atras
  - la prosa que dice "agrupadas por ventana_fin"

Lo que NO se toca en ningun caso:
  - el WHERE, que sigue en ventana_fin: ese es el corte con que se genero la
    entrada y moverlo meteria evaluaciones posteriores, cambiando numeros ya
    archivados
  - la marca de tiempo de generacion, el total de la seccion 1 ni el
    acumulado de la seccion 3

Es una biyeccion (ventana_fin = ventana_inicio + 1 dia), asi que todos los
CONTEOS quedan identicos: solo cambia el rotulo.

Uso: python migrar_seccion4.py [--aplicar]
"""
import datetime
import re
import sys
from pathlib import Path

DIR = (Path(__file__).resolve().parent.parent / 'evidencias' / 'bitacora_b5')
APLICAR = '--aplicar' in sys.argv

if not DIR.is_dir():
    sys.exit('no existe %s' % DIR)

SQL_RE = re.compile(r'\(ventana_fin AT TIME ZONE')
FILA_RE = re.compile(r'^    (\d{4}-\d{2}-\d{2}) \| (\d+)$', re.M)
PROSA_RE = re.compile(r'agrupadas por `ventana_fin`')
FIN = re.compile(r'^## 5\.', re.M)

cambios = []
for p in sorted(DIR.glob('2026-*.md')):
    txt = p.read_text(encoding='utf-8')
    m4 = re.search(r'^## 4\.', txt, re.M)
    m5 = FIN.search(txt)
    if not m4 or not m5:
        continue
    ini, fin = m4.start(), m5.start()
    # `sec` es SOLO la seccion 4. Antes se le asignaba txt[:ini] (el texto
    # anterior a la seccion), con lo que no matcheaba nada y, peor, al
    # escribir `sec + despues` se habria BORRADO la seccion 4 completa.
    antes, sec, despues = txt[:ini], txt[ini:fin], txt[fin:]
    original = sec

    n_sql = len(SQL_RE.findall(sec))
    sec = SQL_RE.sub('(ventana_inicio AT TIME ZONE', sec)

    def correr(m):
        d = datetime.date.fromisoformat(m.group(1)) - datetime.timedelta(days=1)
        return '    %s | %s' % (d.isoformat(), m.group(2))
    sec, n_filas = FILA_RE.subn(correr, sec)

    sec, n_prosa = PROSA_RE.subn(
        'agrupadas por `ventana_inicio`, con el día que cada fila evaluó', sec)

    if sec == original:
        continue
    cambios.append((p.name, n_sql, n_filas, n_prosa))
    if APLICAR:
        p.write_text(antes + sec + despues, encoding='utf-8')

print('modo:', 'APLICAR' if APLICAR else 'SIMULACION (no se escribio nada)')
print('%-20s %-6s %-6s %s' % ('archivo', 'sql', 'filas', 'prosa'))
for c in cambios:
    print('%-20s %-6s %-6s %s' % c)
if not cambios:
    print('  nada que migrar')
print('\ntotal archivos:', len(cambios))