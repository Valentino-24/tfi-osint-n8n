#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recalculo del regimen de operacion de la instancia de n8n (hallazgo N-17).

Fuentes:
  1. Registro de ejecuciones: tabla `execution_entity` de la base SQLite de n8n
     (/home/node/.n8n/database.sqlite), workflow KkotjSD5uO4CXI4D. Se copia con
     `docker cp` desde el contenedor detenido tfi-n8n (no se inicia).
  2. Publicaciones: tabla `posts` de PostgreSQL (contenedor tfi-postgres), solo
     lectura. Se inicia el contenedor y se ejecutan consultas SELECT / COPY.

Salida: cobertura de operacion con numerador y denominador sobre el mismo
intervalo, regimen por dia, descomposicion de la latencia por estado de la
instancia y huecos entre jornadas.

Uso:  python regimen_operacion.py
"""

import csv
import datetime as dt
import io
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TZ = dt.timedelta(hours=-3)  # America/Argentina/Buenos_Aires (UTC-3, sin DST)
WORKFLOW = "KkotjSD5uO4CXI4D"
CUT_LOCAL = dt.datetime(2026, 10, 18, 0, 0, 0)      # corte del corpus B5
WIN_LOCAL = dt.datetime(2026, 10, 1, 0, 0, 0)       # inicio de la ventana
MERGE_GAP_MIN = 20                                   # fusion de corridas


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


def get_sqlite(tmp):
    dest = os.path.join(tmp, "n8n_database.sqlite")
    run(["docker", "cp", "tfi-n8n:/home/node/.n8n/database.sqlite", dest])
    return dest


def ensure_postgres():
    out = run(["docker", "inspect", "-f", "{{.State.Running}}", "tfi-postgres"]).stdout.decode().strip()
    if out != "true":
        run(["docker", "start", "tfi-postgres"])
        import time
        for _ in range(30):
            time.sleep(1)
            try:
                run(["docker", "exec", "tfi-postgres", "psql", "-U", "postgres", "-d", "tesi_osint", "-tAc", "select 1"])
                return
            except subprocess.CalledProcessError:
                continue
        raise RuntimeError("tfi-postgres no respondio")


def psql(sql):
    p = subprocess.run(
        ["docker", "exec", "-i", "tfi-postgres", "psql", "-U", "postgres", "-d", "tesi_osint", "-t", "-A", "-F", "|"],
        input=sql.encode("utf-8"), capture_output=True, check=True)
    return p.stdout.decode("utf-8", "replace")


def parse(s):
    s = s.strip()
    if s.endswith("+00"):
        return dt.datetime.fromisoformat(s[:-3])
    if len(s) > 6 and s[-6] in "+-":
        off = dt.timedelta(hours=int(s[-5:-3]), minutes=int(s[-3:])) * (1 if s[-6] == "+" else -1)
        return dt.datetime.fromisoformat(s[:-6]) - off
    return dt.datetime.fromisoformat(s)


def q(v, p):
    v = sorted(v)
    k = (len(v) - 1) * p
    f = int(k)
    c = min(f + 1, len(v) - 1)
    return v[f] + (v[c] - v[f]) * (k - f)


def main():
    tmp = tempfile.mkdtemp(prefix="n17_")
    try:
        print("=" * 78)
        print("REGIMEN DE OPERACION - recalculo N-17")
        print("Ventana: 2026-10-01 00:00 -> 2026-10-18 00:00 (hora local, UTC-3)")
        print("=" * 78)

        # --- 1. registro de ejecuciones -------------------------------------
        db = get_sqlite(tmp)
        con = sqlite3.connect(db)
        raw = con.execute(
            "select id, mode, startedAt, stoppedAt, status from execution_entity "
            "where workflowId=? order by startedAt", (WORKFLOW,)).fetchall()

        def p2(s):
            return dt.datetime.strptime(s.split(".")[0].replace("T", " "), "%Y-%m-%d %H:%M:%S")

        ex = [{"id": r[0], "mode": r[1], "start": p2(r[2]), "stop": p2(r[3]), "status": r[4]} for r in raw]

        print("\n[1] REGISTRO DE EJECUCIONES (execution_entity, workflow %s)" % WORKFLOW)
        print("    corridas conservadas: %d" % len(ex))
        print("    rango UTC: %s -> %s" % (raw[0][2], raw[-1][2]))
        print("    estados: %s" % {s: sum(1 for e in ex if e["status"] == s) for s in set(e["status"] for e in ex)})

        cut_utc = CUT_LOCAL - TZ
        inwin = [e for e in ex if e["start"] < cut_utc]
        out = [e for e in ex if e["start"] >= cut_utc]
        print("    dentro de la ventana: %d (automaticas=%d, manuales=%d)" % (
            len(inwin),
            sum(1 for e in inwin if e["mode"] == "trigger"),
            sum(1 for e in inwin if e["mode"] == "manual")))
        print("    posteriores al corte: %d (automaticas=%d, manuales=%d)" % (
            len(out),
            sum(1 for e in out if e["mode"] == "trigger"),
            sum(1 for e in out if e["mode"] == "manual")))

        # intervalos entre corridas consecutivas de la ventana
        ints = [(b["start"] - a["start"]).total_seconds() / 60.0 for a, b in zip(inwin, inwin[1:])]
        print("    intervalos consecutivos: %d | mediana=%.1f min | P95=%.1f min | max=%.1f min | <20 min=%d" % (
            len(ints), q(ints, .5), q(ints, .95), max(ints), sum(1 for x in ints if x < 20)))

        # --- 2. union de intervalos ----------------------------------------
        blocks = []
        for e in inwin:
            if blocks and (e["start"] - blocks[-1][1]).total_seconds() / 60.0 < MERGE_GAP_MIN:
                blocks[-1][1] = max(blocks[-1][1], e["stop"])
            else:
                blocks.append([e["start"], e["stop"]])
        total_min = sum((b - a).total_seconds() / 60.0 for a, b in blocks)
        first, last = blocks[0][0], blocks[-1][1]

        print("\n[2] UNION DE INTERVALOS (huecos < %d min fusionados)" % MERGE_GAP_MIN)
        print("    tramos: %d | minutos en ejecucion: %.1f" % (len(blocks), total_min))
        print("    primer tramo: %s | ultimo tramo: %s (hora local)" % (
            (first + TZ).strftime("%d/%m %H:%M:%S"), (last + TZ).strftime("%d/%m %H:%M:%S")))

        span_first_cut = (CUT_LOCAL - TZ - first).total_seconds() / 60.0
        win_min = (CUT_LOCAL - TZ - (WIN_LOCAL - TZ)).total_seconds() / 60.0
        print("\n[3] COBERTURA")
        print("    (a) mismo intervalo [primera corrida, corte]: %.0f min -> %.1f %%" % (
            span_first_cut, 100 * total_min / span_first_cut))
        print("    (b) ventana completa 17 dias: %.0f min -> %.1f %% (cota inferior: el registro no cubre el 01/10-05/10)" % (
            win_min, 100 * total_min / win_min))
        print("    (c) referencia V5: 4.929 / 25.920 min (18 dias) = 19,0 % -> denominador inconsistente")

        # --- 3. regimen por dia --------------------------------------------
        print("\n[4] REGIMEN POR DIA (hora local)")
        print("    fecha       auto manual  primera   ultima    minutos")
        byday = {}
        for e in inwin:
            byday.setdefault((e["start"] + TZ).date(), []).append(e)
        for d in sorted(byday):
            v = byday[d]
            print("    %s  %4d %6d  %s   %s   %6.0f" % (
                d, sum(1 for e in v if e["mode"] == "trigger"), sum(1 for e in v if e["mode"] == "manual"),
                min(x["start"] + TZ for x in v).strftime("%H:%M"),
                max(x["stop"] + TZ for x in v).strftime("%H:%M"),
                sum((x["stop"] - x["start"]).total_seconds() / 60.0 for x in v)))

        # --- 4. publicaciones ----------------------------------------------
        ensure_postgres()
        out_csv = psql("COPY (SELECT id, created_utc, ingested_at FROM posts "
                       "WHERE ingested_at >= '2026-10-01 00:00:00-03' "
                       "AND ingested_at <  '2026-10-19 00:00:00-03' ORDER BY created_utc) "
                       "TO STDOUT WITH (FORMAT csv, HEADER true);\n")
        print("\n[5] PUBLICACIONES (posts, solo lectura)")
        print("    persistidas entre el 01/10 y el 18/10: %d" % (len(out_csv.strip().splitlines()) - 1))
        print("    ingesta por dia (posts con created_utc en la ventana):")

        daily = psql(
            "SELECT to_char(ingested_at AT TIME ZONE 'America/Argentina/Buenos_Aires','YYYY-MM-DD'), count(*), "
            "to_char(min(ingested_at) AT TIME ZONE 'America/Argentina/Buenos_Aires','HH24:MI'), "
            "to_char(max(ingested_at) AT TIME ZONE 'America/Argentina/Buenos_Aires','HH24:MI') "
            "FROM posts WHERE ingested_at >= '2026-10-01 00:00:00-03' AND ingested_at < '2026-10-19 00:00:00-03' "
            "GROUP BY 1 ORDER BY 1;")
        for line in daily.splitlines():
            if "|" in line:
                f = [x.strip() for x in line.split("|")]
                print("      %s  n=%3s  %s-%s" % (f[0], f[1], f[2], f[3]))

        win = []
        for r in csv.DictReader(io.StringIO(out_csv)):
            c = parse(r["created_utc"])
            i = parse(r["ingested_at"])
            if WIN_LOCAL - TZ <= c < CUT_LOCAL - TZ:
                win.append((c, i))
        print("    creadas dentro de la ventana: %d" % len(win))

        def off_min(c, i):
            tot = (i - c).total_seconds() / 60.0
            on = sum(max(0.0, (min(b, i) - max(a, c)).total_seconds() / 60.0) for a, b in blocks)
            return tot - on

        groups = {"en ejecucion": [], "detenida": [], "sin registro": []}
        for c, i in win:
            t = (i - c).total_seconds() / 60.0
            if c < first:
                groups["sin registro"].append(t)
            elif off_min(c, i) <= 0.5:
                groups["en ejecucion"].append(t)
            else:
                groups["detenida"].append(t)

        print("\n[6] LATENCIA POR ESTADO DE LA INSTANCIA (minutos)")
        print("    grupo            n    P50      P95      max    >5min        >60min")
        for k in ("en ejecucion", "detenida", "sin registro"):
            v = groups[k]
            print("    %-14s %4d  %6.1f  %8.1f  %7.1f  %4d (%4.1f%%)  %4d" % (
                k, len(v), q(v, .5), q(v, .95), max(v),
                sum(1 for x in v if x > 5), 100 * sum(1 for x in v if x > 5) / len(v),
                sum(1 for x in v if x > 60)))
        print("    creadas antes de la primera corrida conservada: %d" % len(groups["sin registro"]))
        print("    clasificables: %d | detenida = %.1f %% de las clasificables" % (
            len(groups["en ejecucion"]) + len(groups["detenida"]),
            100 * len(groups["detenida"]) / (len(groups["en ejecucion"]) + len(groups["detenida"]))))

        # --- 5. huecos entre jornadas --------------------------------------
        print("\n[7] HUECOS ENTRE TRAMOS")
        gaps = [((blocks[i + 1][0] - blocks[i][1]).total_seconds() / 3600.0, blocks[i][1], blocks[i + 1][0])
                for i in range(len(blocks) - 1)]
        noct = [(g, a, b) for g, a, b in gaps if (b + TZ).date() > (a + TZ).date()]
        intra = [(g, a, b) for g, a, b in gaps if (b + TZ).date() == (a + TZ).date()]
        print("    huecos entre jornadas (cruzan la medianoche):")
        for g, a, b in noct:
            print("      %s -> %s  %.1f h" % ((a + TZ).strftime("%d/%m %H:%M"), (b + TZ).strftime("%d/%m %H:%M"), g))
        print("    minimo=%.1f h | maximo=%.1f h | n=%d" % (
            min(g for g, _, _ in noct), max(g for g, _, _ in noct), len(noct)))
        print("    reinicios dentro del mismo dia (no son huecos de jornada):")
        for g, a, b in intra:
            print("      %s -> %s  %.1f h" % ((a + TZ).strftime("%d/%m %H:%M"), (b + TZ).strftime("%d/%m %H:%M"), g))

        # --- 6. insercion de evaluaciones ----------------------------------
        print("\n[8] INSERCION DE LAS EVALUACIONES DEL MOTOR (anomalias.created_at)")
        ev = psql(
            "SELECT to_char(ventana_fin AT TIME ZONE 'America/Argentina/Buenos_Aires','DD/MM'), "
            "to_char(min(created_at) AT TIME ZONE 'America/Argentina/Buenos_Aires','DD/MM HH24:MI:SS'), count(*) "
            "FROM anomalias GROUP BY 1 ORDER BY 1;")
        for line in ev.splitlines():
            if "|" in line:
                print("    ventana_fin=%s  insertada=%s  filas=%s" % tuple(x.strip() for x in line.split("|")))
        print("\nfin.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
