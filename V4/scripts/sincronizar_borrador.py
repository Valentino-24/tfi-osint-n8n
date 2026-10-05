"""Sincroniza borrador, version borrador y version activa con el artefacto.

Los tres tienen que coincidir. n8n dispara el trigger de planificacion sobre el
borrador (versionId), no sobre activeVersionId: con el borrador roto la corrida
sale en 0 s sin iterar, aunque la version publicada este perfecta. Por eso el
2026-10-05 se perdio la corrida #90 de las 13:00.

Causa de que el borrador vuelva a romperse: la pestana del editor de n8n abierta
en el navegador tiene el borrador viejo en memoria y lo autoguarda. Mientras
esté abierta, cada despliegue lo revierte.

Requiere n8n detenido.
"""
import json
import os
import shutil
import sqlite3
import subprocess
import sys

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'anexos', 'B_workflow.json')
WF = 'KkotjSD5uO4CXI4D'
WORK = os.path.join(os.environ['TEMP'], 'opencode', 'sync_wal')
CT = 'tfi-n8n'

art = json.load(open(ART, encoding='utf-8'))
conns = art['connections']
nodes = art['nodes']
target = conns['Loop Over Items']
tl = target['main']
print('artefacto: loop -> %s | done -> %s' % (
    ', '.join(x['node'] for x in tl[0]) if tl[0] else '(vacio)',
    ', '.join(x['node'] for x in tl[1]) if len(tl) > 1 and tl[1] else '(vacio)'))

subprocess.run(['docker', 'stop', CT], capture_output=True)
shutil.rmtree(WORK, ignore_errors=True)
os.makedirs(WORK, exist_ok=True)
for ext in ('', '-wal', '-shm'):
    subprocess.run(['docker', 'cp', f'{CT}:/home/node/.n8n/database.sqlite{ext}',
                    os.path.join(WORK, f'database.sqlite{ext}')], capture_output=True)
shutil.copy(os.path.join(WORK, 'database.sqlite'),
            os.path.join(WORK, 'backup_pre_sync.sqlite'))

db = os.path.join(WORK, 'database.sqlite')
con = sqlite3.connect(db)
cur = con.cursor()
active_vid, draft_vid = cur.execute(
    'SELECT activeVersionId, versionId FROM workflow_entity WHERE id=?', (WF,)).fetchone()


def report(tag, blob):
    l = json.loads(blob).get('Loop Over Items', {}).get('main', [])
    lp = ', '.join(x['node'] for x in l[0]) if len(l) > 0 and l[0] else '(vacio)'
    dn = ', '.join(x['node'] for x in l[1]) if len(l) > 1 and l[1] else '(vacio)'
    print('  %-32s loop -> %-22s done -> %s' % (tag, lp, dn))


# connections: las tres copias
row = cur.execute('SELECT connections FROM workflow_entity WHERE id=?', (WF,)).fetchone()
m = json.loads(row[0])
m['Loop Over Items'] = target
cur.execute('UPDATE workflow_entity SET connections=? WHERE id=?',
            (json.dumps(m, ensure_ascii=False), WF))
report('borrador (workflow_entity)', json.dumps(m))

for tag, vid in (('activa', active_vid), ('borrador', draft_vid)):
    r = cur.execute('SELECT connections FROM workflow_history WHERE versionId=?', (vid,)).fetchone()
    if r:
        hm = json.loads(r[0])
        hm['Loop Over Items'] = target
        cur.execute('UPDATE workflow_history SET connections=? WHERE versionId=?',
                    (json.dumps(hm, ensure_ascii=False), vid))
        report('%s (history %s)' % (tag, vid[:8]), json.dumps(hm))

# jsCode del motor de anomalias en las dos versiones, sin tocar credenciales
def patch_engine(blob, tag):
    ns = json.loads(blob)
    for n in ns:
        if n['name'] == 'Anomaly Engine':
            antes = n['parameters'].get('jsCode', '')
            n['parameters']['jsCode'] = [x for x in nodes
                                         if x['name'] == 'Anomaly Engine'][0]['parameters']['jsCode']
            # Detectar por la recurrence y no por la linea rota: el comentario que
            # documenta el bug cita esa linea, asi que buscarla da falso positivo.
            estado = 'ok' if 'term = term * l / i' in antes else 'ROTO'
            print('  %-32s Poisson antes=%s despues=nuevo' % (tag, estado))
    return json.dumps(ns, ensure_ascii=False)


row = cur.execute('SELECT nodes FROM workflow_entity WHERE id=?', (WF,)).fetchone()
cur.execute('UPDATE workflow_entity SET nodes=? WHERE id=?',
            (patch_engine(row[0], 'borrador (workflow_entity)'), WF))

for tag, vid in (('activa', active_vid), ('borrador', draft_vid)):
    r = cur.execute('SELECT nodes FROM workflow_history WHERE versionId=?', (vid,)).fetchone()
    if r:
        cur.execute('UPDATE workflow_history SET nodes=? WHERE versionId=?',
                    (patch_engine(r[0], '%s (history %s)' % (tag, vid[:8])), vid))

con.commit()
print('integridad_check:', cur.execute('PRAGMA integrity_check').fetchone()[0])
ns = json.loads(cur.execute('SELECT nodes FROM workflow_entity WHERE id=?', (WF,)).fetchone()[0])
pg = [n for n in ns if n['type'] == 'n8n-nodes-base.postgres']
sin = [n['name'] for n in pg if not (n.get('credentials') or {}).get('postgres', {}).get('id')]
print('nodos Postgres:', len(pg), '| sin credencial:', sin if sin else 'ninguno (OK)')

con.close()
subprocess.run(['docker', 'cp', db, f'{CT}:/home/node/.n8n/database.sqlite'], capture_output=True)
subprocess.run(['docker', 'run', '--rm', '--user', '0:0', '--entrypoint', '/bin/sh',
                '-v', 'tfi_n8n:/data', 'n8nio/n8n:2.40.6', '-c',
                'rm -f /data/database.sqlite-wal /data/database.sqlite-shm; '
                'chown 1000:1000 /data/database.sqlite; chmod 600 /data/database.sqlite'],
               capture_output=True)
subprocess.run(['docker', 'start', CT], capture_output=True)
print('n8n detenido, sincronizado y reiniciado.')