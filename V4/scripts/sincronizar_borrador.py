"""Sincronizacion final con ASSERTIONS.

Por que esta reescrita: la version anterior fallacy en silencio. docker cp
deja el archivo como root:root y el helper que hacia chown + rm del WAL
fallaba sin que nadie lo viera, porque capture_output=True descarta el
stderr. El -wal viejo (4152 bytes) se replayeaba encima del main recien
copiado y resucitaba el estado anterior: por eso el borrador volvia a
romperse solo y por eso las corridas salian de 0 s.

Ningun paso puede fallar sin abortar. Y el workflow queda INACTIVO: la
publicacion la hace el usuario desde la UI.
"""
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'anexos', 'B_workflow.json')
WF = 'KkotjSD5uO4CXI4D'
WORK = os.path.join(os.environ['TEMP'], 'opencode', 'sync_final')
CT = 'tfi-n8n'


def run(args, **kw):
    r = subprocess.run(args, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.exit('FALLO %s\n  stdout: %s\n  stderr: %s' % (args, r.stdout.strip(), r.stderr.strip()))
    return r


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sha_volumen():
    r = run(['docker', 'run', '--rm', '--user', '0:0', '--entrypoint', 'sha256sum',
             '-v', 'tfi_n8n:/data', 'n8nio/n8n:2.40.6', '/data/database.sqlite'])
    return r.stdout.split()[0]


art = json.load(open(ART, encoding='utf-8'))
conns, nodes = art['connections'], art['nodes']
target = conns['Loop Over Items']
engine = [n for n in nodes if n['name'] == 'Anomaly Engine'][0]['parameters']['jsCode']

print('[1/7] detiendo n8n')
run(['docker', 'stop', CT])

print('[2/7] copiando sqlite + wal + shm')
shutil.rmtree(WORK, ignore_errors=True)
os.makedirs(WORK)
for ext in ('', '-wal', '-shm'):
    run(['docker', 'cp', f'{CT}:/home/node/.n8n/database.sqlite{ext}',
         os.path.join(WORK, f'database.sqlite{ext}')])
db = os.path.join(WORK, 'database.sqlite')
shutil.copy(db, os.path.join(WORK, 'backup_pre_sync.sqlite'))

print('[3/7] alineando las tres copias en la base')
con = sqlite3.connect(db)
cur = con.cursor()
active_vid, draft_vid = cur.execute(
    'SELECT activeVersionId, versionId FROM workflow_entity WHERE id=?', (WF,)).fetchone()

m = json.loads(cur.execute('SELECT connections FROM workflow_entity WHERE id=?', (WF,)).fetchone()[0])
m['Loop Over Items'] = target
cur.execute('UPDATE workflow_entity SET connections=? WHERE id=?',
            (json.dumps(m, ensure_ascii=False), WF))

ns = json.loads(cur.execute('SELECT nodes FROM workflow_entity WHERE id=?', (WF,)).fetchone()[0])
for n in ns:
    if n['name'] == 'Anomaly Engine':
        n['parameters']['jsCode'] = engine
cur.execute('UPDATE workflow_entity SET nodes=? WHERE id=?',
            (json.dumps(ns, ensure_ascii=False), WF))

for vid in {v for v in (active_vid, draft_vid) if v}:
    r = cur.execute('SELECT connections, nodes FROM workflow_history WHERE versionId=?', (vid,)).fetchone()
    if not r:
        print('     (version %s no esta en history, se omite)' % vid[:8])
        continue
    hm = json.loads(r[0])
    hm['Loop Over Items'] = target
    cur.execute('UPDATE workflow_history SET connections=? WHERE versionId=?',
                (json.dumps(hm, ensure_ascii=False), vid))
    hns = json.loads(r[1])
    for n in hns:
        if n['name'] == 'Anomaly Engine':
            n['parameters']['jsCode'] = engine
    cur.execute('UPDATE workflow_history SET nodes=? WHERE versionId=?',
                (json.dumps(hns, ensure_ascii=False), vid))

# La publicacion la hace el usuario desde la UI: este script NO toca
# active ni activeVersionId. Antes los dejaba en '0'/NULL, lo que
# despublicaba un workflow recien publicado por el usuario. Ahora se
# preservan tal cual: si esta activo, sigue activo; si no, sigue inactivo.
estado = cur.execute('SELECT active, activeVersionId FROM workflow_entity WHERE id=?',
                      (WF,)).fetchone()
print('     estado de publicacion preservado: active=%s activeVersionId=%s' % estado)
con.commit()

print('[4/7] verificando integridad y credenciales')
assert cur.execute('PRAGMA integrity_check').fetchone()[0] == 'ok', 'integridad fallida'
ns = json.loads(cur.execute('SELECT nodes FROM workflow_entity WHERE id=?', (WF,)).fetchone()[0])
pg = [n for n in ns if n['type'] == 'n8n-nodes-base.postgres']
sin = [n['name'] for n in pg if not (n.get('credentials') or {}).get('postgres', {}).get('id')]
assert not sin, 'nodos Postgres sin credencial: %s' % sin
loop = json.loads(cur.execute('SELECT connections FROM workflow_entity WHERE id=?',
                              (WF,)).fetchone()[0])['Loop Over Items']['main']
assert [x['node'] for x in loop[0]] == ['Espera Rate Limit'], 'cableado incorrecto: %s' % loop
con.close()
print('     integridad ok | %d nodos Postgres con credencial | loop -> Espera Rate Limit' % len(pg))

print('[5/7] copiando de vuelta y verificando por hash')
esperado = sha(db)
run(['docker', 'cp', db, f'{CT}:/home/node/.n8n/database.sqlite'])
real = sha_volumen()
assert real == esperado, 'el hash del volumen no coincide: %s != %s' % (real, esperado)
print('     hash confirmado', real[:16])

print('[6/7] borrando el WAL y arreglando permisos (verificado)')
run(['docker', 'run', '--rm', '--user', '0:0', '--entrypoint', '/bin/sh',
     '-v', 'tfi_n8n:/data', 'n8nio/n8n:2.40.6', '-c',
     'rm -f /data/database.sqlite-wal /data/database.sqlite-shm && '
     'chown 1000:1000 /data/database.sqlite && chmod 600 /data/database.sqlite && '
     'ls -l /data/database.sqlite*'])
izq = run(['docker', 'run', '--rm', '--user', '0:0', '--entrypoint', '/bin/sh',
           '-v', 'tfi_n8n:/data', 'n8nio/n8n:2.40.6', '-c',
           'ls /data/database.sqlite-wal /data/database.sqlite-shm 2>/dev/null | wc -l']).stdout.strip()
assert izq == '0', 'el WAL sigue presente (%s ficheros); se aborta para no perder datos' % izq
print('     WAL y shm eliminados, owner node:node, modo 600')

print('[7/7] arrancando n8n')
run(['docker', 'start', CT])
print('\nOK. Borrador y version activa alineados. Estado de publicacion: '
      'active=%s (lo decides vos desde la UI).' % estado[0])