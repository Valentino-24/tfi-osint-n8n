"""Backfill de la seccion 6 en entradas generadas con el bug de commit c953616.

El bullet de la seccion 6 se emitia sin consultar la bandera `dia_cerrado`,
asi que siempre decia "el dia no estaba cerrado ... corte parcial", incluso
cuando la cabecera de la misma entrada declaraba `dia cerrado`. Es una
autocontradiccion dentro de un mismo documento de evidencia.

El bug esta corregido en el generador (bitacora_b5.py); esto solo reescribe
el bullet de las entradas ya archivadas para que coincidan con su propia
cabecera.

Que NO se toca:
  - la cabecera, que ya era correcta
  - `n`, el total de la seccion 1 ni el acumulado de la seccion 3
  - la marca de tiempo de generacion
  - entradas cuya cabecera declara `corte a mitad de dia`: ahi el bullet
    viejo era correcto y se deja igual

Se elimina ademas la referencia (dagger-1): esos tres archivos no definian
ese pie en ningun otro lado, asi que la cita quedaba huerta.

Uso: python corregir_seccion6.py [--aplicar]
"""
import re
import sys
from pathlib import Path

DIR = (Path(__file__).resolve().parent.parent / 'evidencias' / 'bitacora_b5')
APLICAR = '--aplicar' in sys.argv

if not DIR.is_dir():
    sys.exit('no existe %s' % DIR)

VIEJO = re.compile(
    r'- El día `(?P<f>\d{4}-\d{2}-\d{2})` acumula `n = (?P<n>\d+)` posts '
    r'al instante de esta generación\. El día no estaba cerrado cuando se '
    r'generó la entrada \(.{1,3}\d+\), así que el número es un '
    r'\*\*corte parcial\*\* y no el total del día\.')

NAT = re.compile(r'Naturaleza del `n` \| \*\*(.{3,45}?)\*\*')

NUEVO = ('- El día `{f}` acumula `n = {n}` posts ingeridos en el día. '
         'El día ya estaba **cerrado** al generarse esta entrada, así que '
         '`{n}` es el total del día y no un corte parcial.')

cambios = []
for p in sorted(DIR.glob('2026-*.md')):
    txt = p.read_text(encoding='utf-8')
    m = VIEJO.search(txt)
    if not m:
        continue
    nat = NAT.search(txt)
    nat = nat.group(1) if nat else '?'
    if nat != 'día cerrado':
        cambios.append((p.name, 'SKIPPED', 'cabecera=%s' % nat))
        continue
    nuevo = NUEVO.format(f=m.group('f'), n=m.group('n'))
    cambios.append((p.name, 'n=%s' % m.group('n'), nuevo[:60] + '...'))
    if APLICAR:
        p.write_text(VIEJO.sub(nuevo, txt, count=1), encoding='utf-8')

print('modo:', 'APLICAR' if APLICAR else 'SIMULACION (no se escribio nada)')
for c in cambios:
    print('  %-16s %-8s %s' % c)
if not cambios:
    print('  nada que corregir')
print('total:', len(cambios))