# -*- coding: utf-8 -*-
"""Genera muestreo_sql.txt: dossier de evidencia del muestreo V5.

Ejecuta SOLO consultas de lectura y escribe un .txt con:
  - parametros (corte, semilla, fecha de generacion)
  - el SQL literal de cada consulta
  - los resultados reales
  - la formula de tamano de muestra aplicada
  - los sha256 de los archivos entregables

Uso: python generar_evidencia_muestreo.py
"""
import subprocess, hashlib, io, os, datetime

SEMILLA = "20261020"
CORTE = "2026-10-18 03:00:00+00"
TRACK = "2026-10-19 00:00:00+00"
N0 = 554
N0_MUESTRA = 182
OUT = os.path.dirname(os.path.abspath(__file__))
SEP = "@@SEP@@"
PSQL = ["docker", "exec", "tfi-postgres", "psql", "-U", "postgres", "-d", "tesi_osint", "-t", "-A", "-F", SEP]


def q(sql):
    r = subprocess.run(PSQL + ["-c", sql], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(r.stderr[:600])
    return [l.split(SEP) for l in r.stdout.splitlines() if l.strip()]


FILTRO = f"p.created_utc < '{CORTE}' AND p.ingested_at < '{TRACK}'"

Q_TOTAL = "SELECT count(*) FROM posts;"
Q_VENTANA = f"""SELECT
  count(*)                                                   AS total_ventana,
  count(*) FILTER (WHERE p.nlp_category <> 'No relevante')    AS positivos_clasificador,
  count(*) FILTER (WHERE p.nlp_category =  'No relevante')    AS negativos_clasificador,
  count(*) FILTER (WHERE p.nlp_category IS NULL)              AS sin_clasificar
FROM posts p
WHERE {FILTRO};"""
Q_COM = f"""SELECT s.display_name,
  count(*) FILTER (WHERE p.nlp_category <> 'No relevante') AS positivos,
  count(*) FILTER (WHERE p.nlp_category =  'No relevante') AS negativos,
  count(*)                                                 AS total
FROM posts p JOIN subreddits s ON s.id = p.subreddit_id
WHERE {FILTRO}
GROUP BY s.display_name ORDER BY 4 DESC;"""
Q_TRACK = """SELECT count(*) FROM posts
WHERE ingested_at >= '2026-10-19 00:00:00+00';"""
Q_HUECO = """SELECT min(created_utc), max(created_utc) FROM posts
WHERE nlp_category IS NOT NULL;"""


def n(valor, defecto=0):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return defecto


def wilson_proporcion(n_, N):
    """Solo para documentar la tabla de tamano (no se usa en el analisis)."""
    return n_, N


def tam(n_simple, N):
    """Correccion por poblacion finita."""
    return n_simple / (1 + (n_simple - 1) / N)


def sha(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()


def main():
    total = n(q(Q_TOTAL)[0][0])
    v = q(Q_VENTANA)[0]
    ventana, pos, neg, nulos = n(v[0]), n(v[1]), n(v[2]), n(v[3])
    com = q(Q_COM)
    track = n(q(Q_TRACK)[0][0])
    hueco = q(Q_HUECO)[0]

    # Tabla de tamano de muestra (z=1.96, e=0.05)
    z, e = 1.96, 0.05
    filas_tam = []
    for p in (0.091, 0.15, 0.227):
        n_simple = z * z * p * (1 - p) / (e * e)
        filas_tam.append((p, n_simple, tam(n_simple, N0)))

    lineas = []
    A = lineas.append
    A("DOSSIER DE EVIDENCIA — MUESTREO V5 (N-08)")
    A("=" * 62)
    A(f"Generado (UTC): {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S}")
    A("Base: tesi_osint (PostgreSQL 18, contenedor tfi-postgres)")
    A(f"Corte B5: created_utc < {CORTE}")
    A(f"Exclusion track C-25: ingested_at < {TRACK}")
    A(f"Semilla de sorteo: {SEMILLA}  |  orden: md5(id || '{SEMILLA}')")
    A("")
    A("1. POBLACION")
    A("-" * 62)
    A(f"Base completa hoy ................................ {total} posts")
    A(f"Ventana B5 al corte ............................. {ventana} posts")
    A(f"Track secundario C-25 (posterior al corte) ...... {track} posts")
    A(f"Sin clasificar (nlp_category NULL) en la ventana . {nulos} posts")
    A(f"Rango temporal de posts clasificados ............ {hueco[0]} .. {hueco[1]}")
    A("")
    A(f"Estrato 1 (positivos del clasificador) .......... {pos}")
    A(f"Estrato 2 (negativos del clasificador, N0) ...... {neg}")
    A(f"Suma ............................................ {pos + neg}")
    A("")
    A("2. DISTRIBUCION POR COMUNIDAD")
    A("-" * 62)
    A(f"{'comunidad':<14}{'positivos':>10}{'negativos':>11}{'total':>8}")
    for nombre, p_, n_, t_ in com:
        A(f"{nombre:<14}{n(p_):>10}{n(n_):>11}{n(t_):>8}")
    A("")
    A("3. CONSULTAS EJECUTADAS (SQL literal)")
    A("-" * 62)
    for titulo, sql in [
        ("3.1 Total de la base", Q_TOTAL),
        ("3.2 Ventana B5 y estratos", Q_VENTANA),
        ("3.3 Distribucion por comunidad", Q_COM),
        ("3.4 Track posterior al corte", Q_TRACK),
        ("3.5 Rango temporal", Q_HUECO),
    ]:
        A(f"-- {titulo}")
        A(sql.strip())
        A("")
    A("-- 3.6 Sorteo del estrato 2 (reproducible)")
    A(f"""SELECT p.id, p.title, coalesce(p.selftext,''), s.display_name
FROM posts p JOIN subreddits s ON s.id = p.subreddit_id
WHERE p.nlp_category = 'No relevante'
  AND {FILTRO}
ORDER BY md5(p.id || '{SEMILLA}')
LIMIT {N0_MUESTRA};""")
    A("")
    A("-- 3.7 Censo del estrato 1 (todos los positivos del clasificador)")
    A(f"""SELECT p.id, p.title, coalesce(p.selftext,''), s.display_name
FROM posts p JOIN subreddits s ON s.id = p.subreddit_id
WHERE p.nlp_category <> 'No relevante' AND p.nlp_category IS NOT NULL
  AND {FILTRO}
ORDER BY md5(p.id || '{SEMILLA}');""")
    A("")
    A("4. TAMANO DE MUESTRA")
    A("-" * 62)
    A("n = z^2 * p(1-p) / e^2   con z = 1,96 (95%) y e = 0,05")
    A("n_ajustado = n / (1 + (n-1)/N)   con N = N0 = 554")
    A("")
    A(f"{'omision p':<12}{'n simple':>10}{'n con FPC':>12}")
    for p, ns, na in filas_tam:
        A(f"{p*100:>8.1f} %{ns:>12.0f}{na:>12.0f}")
    A("")
    A(f"Adoptado: n0 = {N0_MUESTRA} (escenario conservador p = 22,7 %)")
    A(f"Factor de ponderacion: w = N0/n0 = {N0}/{N0_MUESTRA} = {N0/N0_MUESTRA:.4f}")
    A("")
    A("5. COMPOSICION DEL MATERIAL DE ANOTACION")
    A("-" * 62)
    A(f"Hoja ciega completa: {pos} (censo) + {N0_MUESTRA} (muestra) = {pos + N0_MUESTRA} casos")
    A("Submuestra comun: 25 del estrato 1 + 25 del estrato 2 = 50 casos")
    A("Orden de presentacion mezclado (random.seed(20261020)); codigo C-xxx no revela estrato")
    A("La hoja NO incluye: nlp_category, nlp_score, id de plataforma, estrato_origen")
    A("")
    A("6. HASHES SHA-256 DE LOS ENTREGABLES")
    A("-" * 62)
    for f in ["muestra_v5_etiquetado.csv", "muestra_v5_etiquetado.xlsx",
              "muestra_v5_anot1.csv", "muestra_v5_anot1.xlsx",
              "muestra_v5_anot2.csv", "muestra_v5_anot2.xlsx",
              "muestra_v5_correspondencia.csv", "adjudicacion_v5.xlsx",
              "guia_etiquetado_v5.md", "paquete_anotadores_v5.zip"]:
        p = os.path.join(OUT, f)
        if os.path.exists(p):
            A(f"{sha(p)}  {f}")
        else:
            A(f"{'(ausente)':<64}  {f}")
    A("")
    A("NOTA: muestra_v5_correspondencia.csv NO se publica (contiene id de plataforma,")
    A("estrato y prediccion). Se conserva para trazabilidad ante el tribunal.")

    destino = os.path.join(OUT, "muestreo_sql.txt")
    io.open(destino, "w", encoding="utf-8", newline="\n").write("\n".join(lineas) + "\n")
    print(f"Escrito: {destino}")
    print(f"Ventana={ventana} positivos={pos} negativos={neg} nulos={nulos} track={track}")
    print("sha256 dossier:", sha(destino))


if __name__ == "__main__":
    main()
