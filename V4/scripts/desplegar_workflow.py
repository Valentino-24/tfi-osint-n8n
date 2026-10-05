"""Despliegue del workflow V4 a la instancia n8n, con reasignacion explicita de credenciales.

Por que existe este script y no un import a pelo
-------------------------------------------------
`B_workflow.json` se genera SIN referencias a credenciales a proposito: el
artefacto versionado tiene que ser reproducible en cualquier maquina y no
cargar ids de un entorno concreto. Pero n8n guarda la credencial *dentro del
nodo*, no en el workflow. Importar el JSONgenerated "as is" deja los cuatro
nodos Postgres sin base de datos: el workflow se publica y falla en la
primera ejecucion, o peor, escribe con defaults.

Este script hace explicito lo que la regla dura exige:
  "NUNCA asumir que una importacion conserva credenciales -> reasignar la
   credencial Postgres despues de importar."

Pasos: leer el artefacto generado, inyectar la referencia de credencial que
declara el operador, verificar que NINGUN nodo Postgres quedo sin ella, y recien
ahi importar. Si la verificacion falla, no importa nada.

Uso:
    PG_CRED_ID=<id> PG_CRED_NAME=<nombre> python V4/scripts/desplegar_workflow.py [--publicar] [--container tfi-n8n] [--workflow-id ID]

Solo lectura sobre la base de datos: no escribe filas, no toca el esquema.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# La consola de Windows usa cp1252 y el texto de n8n trae caracteres que no
# entran. Sin esto, el print revienta DESPUES de que el comando corrio, y el
# script muere sin poder distinguir exito de fallo.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parents[2]
GENERADO = REPO / "V4" / "anexos" / "B_workflow.json"

NODOS_POSTGRES_ESPERADOS = {
    "Upsert Subreddits",
    "Upsert Posts",
    "Query Daily Counts",
    "Registrar Anomalias y Alertas",
}


def log(msg: str) -> None:
    print(msg, flush=True)


def docker(container: str, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["docker", "exec", container, *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=check,
    )


def cargar_artefacto() -> dict:
    if not GENERADO.exists():
        sys.exit(f"ERROR: no existe {GENERADO}. Corri primero generar_workflow.py.")
    # Se valida que sea JSON legible antes de tocar nada.
    with GENERADO.open(encoding="utf-8") as fh:
        wf = json.load(fh)
    log(f"artefacto: {GENERADO.name} | {len(wf['nodes'])} nodos | name={wf.get('name')}")
    return wf


def inyectar_credencial(wf: dict, cred_id: str, cred_name: str) -> dict:
    """Agrega la referencia de credencial a todo nodo Postgres. Devuelve el conteo."""
    aplicadas = 0
    for nodo in wf["nodes"]:
        if nodo.get("type") != "n8n-nodes-base.postgres":
            continue
        nodo["credentials"] = {"postgres": {"id": cred_id, "name": cred_name}}
        aplicadas += 1
    return aplicadas


def verificar(wf: dict) -> None:
    """Falla ruidosamente si algo quedo sin credencial. Esto es el punto del script."""
    problemas = []
    vistos = set()
    for nodo in wf["nodes"]:
        if nodo.get("type") != "n8n-nodes-base.postgres":
            continue
        vistos.add(nodo["name"])
        cr = nodo.get("credentials", {}).get("postgres", {})
        if not cr.get("id"):
            problemas.append(f"    - {nodo['name']}: SIN credencial")
        else:
            log(f"    ok {nodo['name']}: {cr['name']} ({cr['id']})")

    faltantes = NODOS_POSTGRES_ESPERADOS - vistos
    if faltantes:
        problemas.append(f"    - nodos Postgres ausentes del artefacto: {sorted(faltantes)}")

    # El centinela del 429 tiene que existir: sin el, el loop se cierra antes de tiempo.
    nombres = {n["name"] for n in wf["nodes"]}
    for requerido in ("Prepare Upsert", "Extract Entities", "Loop Over Items", "Upsert Posts"):
        if requerido not in nombres:
            problemas.append(f"    - falta el nodo '{requerido}'")

    if problemas:
        log("VERIFICACION FALLIDA:")
        print("\n".join(problemas))
        sys.exit("No se importa nada. Seaborta.")
    log("verificacion OK: los 4 nodos Postgres tienen credencial y el fix del 429 esta presente")


# Valores que n8n omite al guardar porque ya son el default del nodo. Si el
# artefacto los declara de forma explicita y la instancia no, NO es una
# diferencia semantica: comparar sin normalizar aborta todos los despliegues.
DEFAULTS_OMITIBLES = {
    ("unit", "seconds"),
    ("batchSize", 1),
    ("authentication", "none"),
}

# Campos cuyo cambio SI significa que el despliegue no aplico.
PARAMETROS_CRITICOS = ("jsCode", "query", "url", "jsonBody", "amount", "rule", "sql")


def normalizar(params: dict) -> dict:
    """Quita los defaults que n8n omite, para comparar contenido y no formato."""
    out = {}
    for k, v in (params or {}).items():
        # Los valores pueden ser dict o listas, que no son hashables: el chequeo
        # contra el set de defaults solo aplica a escalares.
        if isinstance(v, (str, int, float, bool)) and (k, v) in DEFAULTS_OMITIBLES:
            continue
        if k == "rule" and isinstance(v, dict):
            rule = {}
            for rk, rv in v.items():
                if rk == "interval" and isinstance(rv, list):
                    iv = []
                    for it in rv:
                        if not isinstance(it, dict):
                            iv.append(it)
                            continue
                        it = dict(it)
                        # n8n no guarda 'field' cuando ya hay triggerAtHour/minute
                        if "triggerAtHour" in it and it.get("field") == "days":
                            it.pop("field")
                        iv.append(it)
                    rule[rk] = iv
                else:
                    rule[rk] = rv
            out[k] = rule
        else:
            out[k] = v
    return out


def huella_nodos(nodes: list) -> dict:
    """nombre -> parametros normalizados. Ignora credenciales a proposito.

    Sirve para probar que la instancia tiene el MISMO codigo que el artefacto.
    Comparar solo la cantidad de nodos no alcanza: dos versiones distintas
    pueden tener la misma cantidad y el despliegue pasa por verde igual. Eso
    paso el 2026-10-05 con el fix del Poisson.
    """
    return {n.get("name", "?"): normalizar(n.get("parameters", {}) or {})
            for n in nodes}


def diferencias_entre(esperado: dict, obtenido: dict) -> tuple:
    """(criticas, cosmetics). Criticas = cambia el comportamiento del nodo."""
    criticas, cosmetics = [], []
    for nombre in sorted(set(esperado) | set(obtenido)):
        e, o = esperado.get(nombre), obtenido.get(nombre)
        if e == o:
            continue
        if e is None or o is None:
            criticas.append((nombre, "(nodo ausente)", "(nodo ausente)" if o is None else "presente"))
            continue
        for k in sorted(set(e) | set(o)):
            if e.get(k) == o.get(k):
                continue
            etiqueta = "CRITICA" if k in PARAMETROS_CRITICOS else "cosmetica"
            (criticas if etiqueta == "CRITICA" else cosmetics).append(
                (nombre, k, "artefacto=%r instancia=%r" % (e.get(k), o.get(k))))
    return criticas, cosmetics


def escribir_al_contenedor(container: str, wf: dict) -> str:
    remoto = "/tmp/B_workflow_deploy.json"
    local = Path(tempfile.gettempdir()) / "B_workflow_deploy.json"
    with local.open("w", encoding="utf-8") as fh:
        json.dump(wf, fh, ensure_ascii=False, indent=2)
    subprocess.run(["docker", "cp", str(local), f"{container}:{remoto}"], check=True,
                   capture_output=True, text=True)
    log(f"copiado al contenedor -> {remoto}")
    return remoto


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--container", default="tfi-n8n")
    ap.add_argument("--workflow-id", default=None,
                    help="id del workflow a actualizar (por defecto, el del artefacto)")
    ap.add_argument("--publicar", action="store_true",
                    help="activa el workflow al final (n8n publish:workflow)")
    args = ap.parse_args()

    cred_id = os.environ.get("PG_CRED_ID", "").strip()
    cred_name = os.environ.get("PG_CRED_NAME", "").strip()
    if not cred_id:
        sys.exit("ERROR: falta PG_CRED_ID. No se asume ninguna credencial (regla dura).")

    wf = cargar_artefacto()
    wf_id = args.workflow_id or wf.get("id")
    if not wf_id:
        sys.exit("ERROR: el artefacto no trae id y no se paso --workflow-id.")

    # El artefacto trae su propio id estable (TFIOsintV4Monitor01), pero el
    # workflow que vive en la instancia se creo desde la UI y tiene otro
    # (KkotjSD5uO4CXI4D). `import:workflow` NO sobrescribe por id distinto: crea
    # un workflow NUEVO y deja el viejo intacto, devolviendo igual "Successfully
    # imported". Por eso el id se fuerza al destino: sin esto, cada despliegue
    # deja una copia mas en la instancia.
    if wf.get("id") != wf_id:
        log(f"  el artefacto declara id={wf.get('id')}; se fuerza id={wf_id} "
            f"para sobrescribir en vez de duplicar")
        wf["id"] = wf_id

    log(f"\ninyectando credencial '{cred_name or '(sin nombre)'}' ({cred_id}):")
    n = inyectar_credencial(wf, cred_id, cred_name)
    log(f"  nodos Postgres actualizados: {n}")

    log("\nverificando antes de importar:")
    verificar(wf)

    remoto = escribir_al_contenedor(args.container, wf)

    log(f"\nimportando sobre el workflow {wf_id}:")
    # OJO: `update:workflow` esta deprecado en n8n 2.x y falla en silencio
    # (solo avisa "No update flag like --active=true has been set!" y no cambia
    # nada). Hay que usar `import:workflow`, que es el que si escribe.
    res = docker(args.container, "n8n", "import:workflow", f"--input={remoto}",
                 check=False)
    out = (res.stdout or "") + (res.stderr or "")
    log("  " + out.strip().replace("\n", "\n  "))
    if res.returncode != 0:
        sys.exit("ERROR: la importacion fallo. No se publica nada.")
    if "WARNING" in out and "deprecated" in out:
        sys.exit("ERROR: la importacion emitio un warning de deprecacion; se aborta "
                 "antes de publicar porque podria no haber aplicado nada.")

    log("\nverificando lo que quedo importado:")
    res = docker(args.container, "n8n", "export:workflow", f"--id={wf_id}",
                 "--output=/tmp/verif_import.json", check=False)
    if res.returncode != 0:
        sys.exit("ERROR: no se pudo reexportar para verificar. No se publica a ciegas.")
    subprocess.run(["docker", "cp", f"{args.container}:/tmp/verif_import.json",
                    os.path.join(tempfile.gettempdir(), "verif_import.json")],
                   check=False, capture_output=True)
    with open(os.path.join(tempfile.gettempdir(), "verif_import.json"), encoding="utf-8") as fh:
        d = json.load(fh)
    vivo = d[0] if isinstance(d, list) else d
    log(f"  nodos: {len(vivo['nodes'])} (el artefacto tiene {len(wf['nodes'])})")

    # Un import que no aplicó nada devuelve exit 0 y parece un exito. Por eso el
    # conteo de nodos se compara contra el artefacto: es la unica prueba de que
    # la escritura ocurrio.
    if len(vivo["nodes"]) != len(wf["nodes"]):
        sys.exit(f"ERROR: el workflow importado tiene {len(vivo['nodes'])} nodos y el "
                 f"artefacto {len(wf['nodes'])}: la importacion NO aplico. No se publica.")
    log("  conteo de nodos coincide con el artefacto")

    # El conteo SOLO no alcanza. El 2026-10-05 se desplego un fix del motor de
    # anomalias (Poisson) y la verificacion dio verde: el workflow viejo tambien
    # tiene 17 nodos, asi que 17 == 17 paso igual, pero 'import:workflow' NO
    # sobreescribe el codigo de un workflow existente y la correccion nunca
    # llego a ejecutarse. Por eso se compara el CONTENIDO de cada nodo, no la
    # cantidad: una huella de los parametros, sin credenciales.
    esperado = huella_nodos(wf["nodes"])
    obtenido = huella_nodos(vivo["nodes"])
    criticas, cosmetics = diferencias_entre(esperado, obtenido)
    if criticas:
        print()
        print("ERROR: la instancia NO tiene el codigo del artefacto (importacion "
              "incompleta). Detalle de las diferencias criticas:")
        for nombre, campo, detalle in criticas:
            print(f"    - {nombre}.{campo}: {detalle}")
        sys.exit("No se publica. Reexportar el workflow o aplicar el cambio "
                 "sobre la base, como se hizo el 2026-10-05.")
    if cosmetics:
        log("  diferencias cosmeticas (n8n omite defaults), no bloquean:")
        for nombre, campo, detalle in cosmetics:
            log(f"    - {nombre}.{campo}: {detalle[:110]}")
    log(f"  contenido de los {len(esperado)} nodos coincide con el artefacto "
        f"({len(cosmeticas)} diferencias cosmeticas toleradas)")

    sin_cred = [n2["name"] for n2 in vivo["nodes"]
                if n2.get("type") == "n8n-nodes-base.postgres"
                and not n2.get("credentials", {}).get("postgres", {}).get("id")]
    if sin_cred:
        sys.exit(f"ERROR tras importar: nodos Postgres sin credencial: {sin_cred}. NO se publica.")
    log("  los nodos Postgres conservan la credencial")

    # El workflow tiene que quedar inactivo todavia: importar no debe activar la
    # ingesta por sorpresa. La activacion es un paso explicito.
    if vivo.get("active"):
        sys.exit("ERROR: el workflow quedo ACTIVO al importar. No se publica nada; "
                 "revisar antes de continuar.")
    log("  el workflow quedo inactivo (la activacion es un paso aparte)")

    if args.publicar:
        log("\npublicando:")
        res = docker(args.container, "n8n", "publish:workflow", f"--id={wf_id}", check=False)
        log("  " + ((res.stdout or "") + (res.stderr or "")).strip().replace("\n", "\n  "))
        if res.returncode != 0:
            sys.exit("ERROR: la publicacion fallo.")

    log("\nlisto.")


if __name__ == "__main__":
    main()