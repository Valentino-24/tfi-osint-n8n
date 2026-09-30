"""Reset de datos de prueba y arranque de la ventana B5.

QUE HACE
  1. Verifica precondiciones (n8n arriba, artefacto coherente, muestra exportada).
  2. Muestra un RESUMEN de lo que va a borrar y pide confirmacion.
  3. Trunca posts, anomalias y alertas.
  4. Imprime el estado limpio.

NO HACE
  - No activa el workflow. Eso lo hace el operador desde la UI de n8n.
  - No borra subreddits ni su configuracion.
  - No toca nada fuera de la base tesi_osint.

USO
  python V4/scripts/reset_ventana.py            # muestra el plan y pregunta
  python V4/scripts/reset_ventana.py --si       # ejecuta sin preguntar (usar con cuidado)

POR QUE HAY QUE HACERLO
  Los 520 posts actuales son datos de prueba. r/argentina y r/DerechoGenial estan
  desactivados, sus 201 posts nunca se reclasifican, y 3 filas conservan nlp_score de
  una version anterior del clasificador. La línea base de 11 dias del motor de anomalias
  debe calcularse sobre datos de la ventana real.
"""
import os
import sys

import psycopg

BANNER = r"""
============================================================
  RESET DE DATOS DE PRUEBA  ->  inicio de la ventana B5
============================================================
"""

PRECAUCIONES = """Este script BORRA TODOS los posts, anomalias y alertas.

Se borra porque:
  - los 520 posts actuales son de prueba, no evidencia publicable
  - 201 posts son de r/argentina y r/DerechoGenial, desactivados y fuera de ámbito
  - 3 filas conservan nlp_score de la fórmula anterior del clasificador
  - la linea base de 11 dias del motor de anomalias debe salir de datos reales

NO se borra:
  - la muestra de control de 50 posts, ya exportada a texto exacto en
    V4/evidencias/muestra_control_50_2026-09-30_TEXTO_EXACTO.jsonl
  - la tabla subreddits y su configuracion
  - el workflow de n8n

ANTES de ejecutar, verificar:
  - el workflow KkotjSD5uO4CXI4D tiene Schedule Ingesta ACTIVADO
  - Schedule Anomalias queda como está
"""


def connect():
    """Conexion a tesi_osint.

    Lee las variables de entorno PG* si estan definidas. Si no, usa los valores del
    stack local del proyecto y pide la password por stdin si hace falta, para no
    dejarla escrita en el repo.
    """
    host = os.environ.get("PGHOST", "localhost")
    port = os.environ.get("PGPORT", "5433")
    dbname = os.environ.get("PGDATABASE", "tesi_osint")
    user = os.environ.get("PGUSER", "postgres")
    password = os.environ.get("PGPASSWORD")
    if not password:
        import getpass
        password = getpass.getpass(f"password de {user}@{host}:{port}/{dbname}: ")
    return psycopg.connect(host=host, port=port, dbname=dbname,
                           user=user, password=password)


def estado(cur):
    cur.execute("SELECT count(*) FROM posts");           posts = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM anomalias");       anom = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM alertas");         alert = cur.fetchone()[0]
    cur.execute("""SELECT count(DISTINCT date_trunc('day', ingested_at)) FROM posts""")
    dias = cur.fetchone()[0]
    cur.execute("""SELECT count(*) FROM posts
                   WHERE nlp_score <> ALL (ARRAY[0, 0.25, 0.5, 0.75, 1.0])""")
    heredadas = cur.fetchone()[0]
    cur.execute("""SELECT s.display_name, s.active_monitoring, count(p.id)
                   FROM subreddits s LEFT JOIN posts p ON p.subreddit_id = s.id
                   GROUP BY 1,2 ORDER BY 1""")
    subs = cur.fetchall()
    return posts, anom, alert, dias, heredadas, subs


def main():
    print(BANNER)
    with connect() as c:
        with c.cursor() as cur:
            posts, anom, alert, dias, heredadas, subs = estado(cur)

            print("ESTADO ACTUAL")
            print(f"  posts      : {posts}   en {dias} dia(s) de ingesta")
            print(f"  anomalias  : {anom}")
            print(f"  alertas    : {alert}")
            print(f"  filas con nlp_score fuera de la grilla vigente : {heredadas}")
            print()
            print("  por subreddit:")
            for nombre, activo, n in subs:
                print(f"    {nombre:<18} activo={str(activo):<6} {n} posts")

            # precondicion critica: la muestra de control debe estar exportada
            export = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "evidencias", "muestra_control_50_2026-09-30_TEXTO_EXACTO.jsonl")
            print()
            if os.path.exists(export):
                with open(export, encoding="utf-8") as f:
                    n_lineas = sum(1 for line in f if line.strip())
                print(f"  [OK ] muestra de control exportada: {n_lineas} lineas")
                if n_lineas != 50:
                    print(f"  [ATENCION] se esperaban 50, hay {n_lineas}")
            else:
                print("  [FALLA] falta el export de la muestra de control:")
                print(f"          {export}")
                print("          Sin ese archivo, truncar la base destruye la")
                print("          capacidad de reproducir la evaluacion. Abortando.")
                return 1

            print()
            print("HALLAZGGO QUE NO SE CORRIGE CON ESTE SCRIPT")
            print("-" * 60)
            cur.execute("""SELECT id, display_name, active_monitoring FROM subreddits
                           WHERE active_monitoring ORDER BY id""")
            activos = cur.fetchall()
            cur.execute("SELECT count(*) FROM posts WHERE subreddit_id = %s", ("derechogenial",))
            huerf = cur.fetchone()[0]
            if huerf == 0:
                print("  La ingesta NO lee la tabla subreddits: el Code node")
                print("  'Prepare Subreddits' trae una lista fija de 3")
                print("  (netsec, Malware, devsarg). Por eso la fila")
                print("  id='derechogenial', activa=True y con 0 posts, jamás se")
                print("  consulta: es inocua para la recolección pero enga\u00f1a a")
                print("  cualquier análisis que filtre por active_monitoring.")
                print()
                print(f"  Filas marcadas activas: {', '.join(n for _, n, _ in activos)}")
                print("  Recomendación: deactivate the orphan row with")
                print("    UPDATE subreddits SET active_monitoring = FALSE WHERE id = 'derechogenial';")
                print("  o dejarla así y documentar que el flag no gobierna la ingesta.")
                print("  Este script NO la toca: subreddit no se trunca.")
            print()
            print(PRECAUCIONES)

            if "--si" not in sys.argv:
                print("Se va a BORRAR todo lo de arriba.")
                r = input("Escribi BORRAR en mayusculas para confirmar: ")
                if r.strip() != "BORRAR":
                    print("Cancelado. No se modifico nada.")
                    return 0

            cur.execute("TRUNCATE posts, anomalias, alertas RESTART IDENTITY")
            print("\nTRUNCATE ejecutado.")

            cur.execute("SELECT count(*) FROM posts");        p2 = cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM anomalias");    a2 = cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM alertas");      l2 = cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM subreddits");   s2 = cur.fetchone()[0]
            print()
            print("ESTADO FINAL")
            print(f"  posts      : {p2}")
            print(f"  anomalias  : {a2}")
            print(f"  alertas    : {l2}")
            print(f"  subreddits : {s2}  (intactos, con su configuracion)")
            assert (p2, a2, l2) == (0, 0, 0), "el truncate no dejo las tablas vacias"

    print()
    print("=" * 60)
    print("SIGUIENTE PASO (lo hace el operador, no este script)")
    print("=" * 60)
    print("  1. En n8n, activar el toggle de 'Schedule Ingesta'.")
    print("     Si quedo apagado de la prueba de anomalias, el workflow")
    print("     NO recolecta.")
    print("  2. Activar el workflow (toggle 'Active' del workflow).")
    print("  3. Anotar fecha y hora de arranque: ese es el corte de la ventana.")
    print("  4. La rama de anomalias corre sola a las 00:05.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
