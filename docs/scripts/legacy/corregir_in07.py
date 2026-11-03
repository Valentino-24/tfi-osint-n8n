"""Correccion de las entradas de bitacora B5 por la resolucion IN-07 (2026-10-07).

El alcance de la ventana quedo fijado en el Plan C (r/netsec, r/Malware,
r/devsarg). Las entradas del 2026-09-30 en adelante se generaron con dos
defectos encadenados:

  1. el denominador de cobertura contaba las 6 filas de `subreddits` (incluidas
     las fuera de alcance) en vez de los 3 subreddits del alcance;
  2. la base declaraba activa a r/derechogenial (resto del Plan B), por eso la
     linea de activos decia "(4 de 3 esperados)", un contador imposible.

La resolucion IN-07 (2026-10-07) desactivo r/derechogenial. Este script
reescribe SOLO la seccion 2 de las entradas ya archivadas para que queden
consistentes con el alcance declarado y con el estado actual de la base.

Que NO se toca:
  - el `n` del dia, el acumulado de la ventana ni el estado de suficiencia
  - la marca de tiempo de generacion
  - la seccion 1, 3, 4, 5 ni 6
  - la entrada 2026-09-25: se genero bajo el alcance Plan B (r/argentina,
    r/derechogenial, r/devsarg) y es el registro historico del ultimo dia con
    ese alcance; solo recibe una anotacion y la prosa corregida

Uso: python corregir_in07.py [--aplicar]
"""
import re
import sys
from pathlib import Path

DIR = (Path(__file__).resolve().parent.parent / 'evidencias' / 'bitacora_b5')
APLICAR = '--aplicar' in sys.argv
SOLO_CHECK = '--check' in sys.argv

if not DIR.is_dir():
    sys.exit('no existe %s' % DIR)

PLAN_C = ('| r/devsarg |', '| r/Malware |', '| r/netsec |')
FUERA_DE_ALCANCE = ('| r/argentina |', '| r/derechogenial |', '| r/DerechoGenial |')

# Fila de TABLA fuera de alcance (linea que empieza con el pipe). El bloque de
# "consulta de control" lista las 6 filas de `subreddits` y NO debe contar aca:
# ahi la presencia de r/argentina es intencional y legittima.
FILA_FUERA = re.compile(r'^\| r/(argentina|derechogenial|DerechoGenial) \|')

# ------------------------------------------------------------------- cabecera
CAB_6 = re.compile(
    r'\| Denominador de cobertura \| \*\*6\*\* subreddit\(s\) monitorizado\(s\) '
    r'\(se incluyen los que aportan 0\) \|')
CAB_NUEVO = ('| Denominador de cobertura | **3** subreddit(s) monitorizado(s) del '
             'alcance Plan C (IN-07); se incluyen los que aportan 0 |')

# ---------------------------------------------------------------------- prosa
PROSA_VIEJA = re.compile(
    r'Los \d+ subreddit\(s\) monitorizado\(s\) de `subreddits` se listan todos, '
    r'incluido el que aporta 0\. El denominador de todo porcentaje de esta ventana son los '
    r'\*\*\d+ subreddit\(s\) monitorizado\(s\)\*\*, no solo los que aportaron posts '
    r'\(RN-GL-02\); el `n` observado del día es \*\*(?P<n>\d+)\*\* y la suma de los `n` de '
    r'la tabla coincide con él\. Un subreddit sin fila propia se reportaría con `n = 0` y su '
    r'causa declarada\.')

def prosa_nueva(n):
    return (f'La tabla es el alcance: **3** subreddit(s) con `active_monitoring = true`, '
            f'listados todos aunque aporten 0 (RN-GL-02). Dos denominadores distintos y '
            f'separados: la columna `% sobre el día` divide sobre el `n` observado del día, '
            f'**{n}**, y la suma de los `n` de la tabla coincide con él; el **denominador de '
            f'cobertura** — cuántos subreddit componen el alcance declarado — es **3**. Un '
            f'subreddit monitoreado sin posts se reporta con `n = 0` y su causa declarada; uno '
            f'fuera del alcance (IN-07) no aparece en la tabla.')

# ---------------------------------------------------- linea de subreddits activos
LINEA_VIEJA = re.compile(r'Subreddits con `active_monitoring = true` en la base: [^\n]+')

LINEA_PLAN_C = ('Subreddits con `active_monitoring = true` en la base: r/devsarg, r/Malware, '
                'r/netsec (3 de 3 esperados del alcance). Las desactivaciones que existen son '
                'decisiones de alcance temático de los autores (IN-07), nunca un ajuste de '
                'cobertura.')

LINEA_PLAN_B = ('Subreddits con `active_monitoring = true` en la base al momento de generar '
                'esta entrada: r/argentina, r/derechogenial, r/devsarg (3 de 3 esperados del '
                'alcance Plan B vigente ese día).')

# -------------------------------------------------- anotacion de la seccion 2
TITULO_2 = '## 2. Desglose por subreddit (denominador completo)\n'
ANOTACION_PLAN_C = (
    '> **Corregida el 2026-10-07 (resolución IN-07).** El alcance de la ventana es el '
    '**Plan C** (`r/netsec`, `r/Malware`, `r/devsarg`). La tabla es la del alcance: las filas '
    'fuera de alcance de `subreddits` (`r/argentina`, `r/derechogenial`, `r/DerechoGenial` — '
    'todas con `n = 0` en esta entrada) se omiten. Al generarse esta entrada el script tomaba '
    'las 6 filas como denominador y la base declaraba 4 subreddits activos; la resolución '
    'completa está en `knowledge-base/10_preguntas_abiertas.md` (IN-07) y en §6 de '
    '`VENTANA_B5.md`.\n\n')

ANOTACION_PLAN_B = (
    '> **Anotada el 2026-10-07 (resolución IN-07).** Esta entrada se generó bajo el alcance '
    '**Plan B** (`r/argentina`, `r/derechogenial`, `r/devsarg`) y queda como registro '
    'histórico: fue el último día con ese alcance y `r/argentina` aportó los **36** posts. '
    'A partir del 2026-09-30 el alcance es el **Plan C** (`r/netsec`, `r/Malware`, '
    '`r/devsarg`); ver `knowledge-base/10_preguntas_abiertas.md` (IN-07) y §6 de '
    '`VENTANA_B5.md`.\n\n')

# ------------------------------------------- bloque de consulta de control (Plan C)
CONTROL_LABEL_VIEJO = 'Consulta de control de los monitorizados:'
CONTROL_LABEL_NUEVO = ('Consulta de control de los monitorizados (resultado de la base a '
                       '2026-10-07, IN-07):')

CONTROL_VIEJO = (
    '    argentina | r/argentina | False\n'
    '    derechogenial | r/derechogenial | True\n'
    '    DerechoGenial | r/DerechoGenial | False\n'
    '    devsarg | r/devsarg | True\n'
    '    Malware | r/Malware | True\n'
    '    netsec | r/netsec | True\n')

CONTROL_NUEVO = (
    '    argentina | r/argentina | False\n'
    '    derechogenial | r/derechogenial | False\n'
    '    DerechoGenial | r/DerechoGenial | False\n'
    '    devsarg | r/devsarg | True\n'
    '    Malware | r/Malware | True\n'
    '    netsec | r/netsec | True\n')


def corregir_plan_c(p: Path) -> list:
    """Reescritura de la seccion 2 para las entradas de alcance Plan C."""
    txt = p.read_text(encoding='utf-8')
    cambios = []

    if CAB_6.search(txt):
        txt = CAB_6.sub(CAB_NUEVO, txt, count=1)
        cambios.append('denominador 6 -> 3')

    m = PROSA_VIEJA.search(txt)
    if m:
        txt = PROSA_VIEJA.sub(lambda mm: prosa_nueva(mm.group('n')), txt, count=1)
        cambios.append('prosa corregida (n=%s)' % m.group('n'))
    else:
        cambios.append('AVISO: prosa vieja no encontrada')

    m = LINEA_VIEJA.search(txt)
    if m:
        txt = LINEA_VIEJA.sub(LINEA_PLAN_C, txt, count=1)
        cambios.append('linea de activos reescrita')

    # quitar filas fuera de alcance de la tabla (todas con n = 0 en estas entradas)
    lineas = txt.splitlines(keepends=True)
    conservadas = [ln for ln in lineas if not ln.startswith(FUERA_DE_ALCANCE)]
    quitadas = sum(1 for ln in lineas if ln.startswith(FUERA_DE_ALCANCE))
    if quitadas:
        txt = ''.join(conservadas)
        cambios.append('filas fuera de alcance quitadas: %d' % quitadas)

    if TITULO_2 in txt and 'resolución IN-07' not in txt:
        txt = txt.replace(TITULO_2, TITULO_2 + ANOTACION_PLAN_C, 1)
        cambios.append('anotacion IN-07 insertada')

    if CONTROL_VIEJO in txt:
        txt = txt.replace(CONTROL_LABEL_VIEJO, CONTROL_LABEL_NUEVO, 1)
        txt = txt.replace(CONTROL_VIEJO, CONTROL_NUEVO, 1)
        cambios.append('control de monitorizados actualizado')

    return txt, cambios


def corregir_plan_b(p: Path) -> list:
    """Anotacion y prosa para la entrada 2026-09-25 (ultimo dia con alcance Plan B)."""
    txt = p.read_text(encoding='utf-8')
    cambios = []

    m = PROSA_VIEJA.search(txt)
    if m:
        txt = PROSA_VIEJA.sub(lambda mm: prosa_nueva(mm.group('n')), txt, count=1)
        cambios.append('prosa corregida (n=%s)' % m.group('n'))

    m = LINEA_VIEJA.search(txt)
    if m:
        txt = LINEA_VIEJA.sub(LINEA_PLAN_B, txt, count=1)
        cambios.append('linea de activos reescrita (Plan B historico)')

    if TITULO_2 in txt and 'resolución IN-07' not in txt:
        txt = txt.replace(TITULO_2, TITULO_2 + ANOTACION_PLAN_B, 1)
        cambios.append('anotacion IN-07 insertada')

    return txt, cambios


resultados = []
for p in sorted(DIR.glob('2026-*.md')):
    if p.name == '2026-09-25.md':
        txt, cambios = corregir_plan_b(p)
    else:
        txt, cambios = corregir_plan_c(p)
    if not cambios:
        continue
    resultados.append((p.name, cambios))
    if APLICAR:
        p.write_text(txt, encoding='utf-8')

print('modo:', 'APLICAR' if APLICAR else 'SIMULACION (no se escribio nada)')
for nombre, cambios in resultados:
    print('  %-15s %s' % (nombre, '; '.join(cambios)))
if not resultados:
    print('  nada que corregir')
print('archivos:', len(resultados))

# ----------------------------------------------------------------- postcondiciones
def verificar_postcondiciones() -> bool:
    errores = []
    for p in DIR.glob('2026-*.md'):
        txt = p.read_text(encoding='utf-8')
        if '(4 de 3 esperados)' in txt:
            errores.append('%s: sigue diciendo "(4 de 3 esperados)"' % p.name)
        if p.name != '2026-09-25.md':
            if FILA_FUERA.search(txt):
                errores.append('%s: fila fuera de alcance en la tabla' % p.name)
            if CAB_6.search(txt):
                errores.append('%s: cabecera sigue con denominador 6' % p.name)
    return errores


if SOLO_CHECK:
    errores = verificar_postcondiciones()
    print('check de postcondiciones:', 'FAIL' if errores else 'OK')
    for e in errores:
        print('  - %s' % e)
    sys.exit(1 if errores else 0)

if APLICAR:
    errores = verificar_postcondiciones()
    if errores:
        print('POSTCONDICIONES FALLIDAS:')
        for e in errores:
            print('  - %s' % e)
        sys.exit(1)
    print('postcondiciones OK')