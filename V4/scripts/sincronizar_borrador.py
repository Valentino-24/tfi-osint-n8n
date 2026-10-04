"""Sincroniza las conexiones del borrador (workflow_entity) con el artefacto.

Contexto: en n8n 2.x `import:workflow` NO sobreescribe `connections` de un
workflow existente (lo verifica: dice 'Successfully imported' y deja la
columna igual). El borrador quedo corrupto cuando se publico desde la UI
con el cable del puerto loop movido al puerto done. Como la version
publicada (activeVersionId) si estaba bien, la ingesta siguio funcionando,
pero cualquier Publish desde la UI promoveria el borrador roto.

Este script deja borrador y publicado alineados con el artefacto, que es la
fuente de verdad. Se ejecuta con n8n detenido.
"""
import json
import os
import shutil
import sqlite3
import sys

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'B_workflow.json')
DB = os.path.join(os.environ['TEMP'], 'opencode', 'fix.sqlite')
WF_ID = 'KkotjSD5uO4CXI4D'

art = json.load(open(ART, encoding='utf-8'))
conns = art['connections']

print('artefacto -> Loop Over Items:')
lob = conns['Loop Over Items']['main']
print('   loop ->', ', '.join(x['node'] for x in lob[0]) if lob[0] else '(vacio)')
print('   done ->', ', '.join(x['node'] for x in lob[1]) if len(lob) > 1 and lob[1] else '(vacio)')

con = sqlite3.connect(DB)
cur = con.cursor()

before = cur.execute('SELECT connections FROM workflow_entity WHERE id=?', (WF_ID,)).fetchone()
if before is None:
    print('ERROR: no existe el workflow', WF_ID)
    sys.exit(1)

old = json.loads(before[0]).get('Loop Over Items', {}).get('main', [])
print()
print('borrador ANTES: loop ->', ', '.join(x['node'] for x in old[0]) if old[0] else '(vacio)')

merged = json.loads(before[0])
merged['Loop Over Items'] = conns['Loop Over Items']
cur.execute('UPDATE workflow_entity SET connections=? WHERE id=?',
            (json.dumps(merged, ensure_ascii=False), WF_ID))
con.commit()

after = json.loads(cur.execute(
    'SELECT connections FROM workflow_entity WHERE id=?', (WF_ID,)).fetchone()[0])
new = after.get('Loop Over Items', {}).get('main', [])
print('borrador DESPUES: loop ->', ', '.join(x['node'] for x in new[0]) if new[0] else '(vacio)')
print('                  done ->',
      ', '.join(x['node'] for x in new[1]) if len(new) > 1 and new[1] else '(vacio)')
print()
print('integridad_check:', cur.execute('PRAGMA integrity_check').fetchone()[0])
print('borrador sincronizado con el artefacto.')
