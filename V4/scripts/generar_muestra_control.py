"""
Genera la muestra de control de 50 posts (tarea 6.2) para el change
`rediseno-diccionario-evaluacion`.

SOLO LECTURA: no escribe nada en tesi_osint (requisito de la spec).

Dos archivos, deliberadamente separados:
  1. ..._POSTS.csv          -> lo lee y etiqueta el anotador. SIN la respuesta
                              del modelo, para que no quede anclado.
  2. ..._RESPUESTA_MODELO.csv -> la prediccion del clasificador, que queda
                              fuera de la vista del anotador.

Sustrato: mezcla estratificada. El 94,4 % de los posts cae en `No relevante`,
asi que un sorteo puro de 50 daria ~3 positivos y la recall no seria
calculable. Se incluyen los 28 posts con alguna categoria de amenaza y se
completan con 22 sorteados de `No relevante`. La columna `peso_muestreo`
permite luego ponderar y estimar metricas sobre la poblacion real.
"""
import csv
import html
import os
import random
import re
import unicodedata
from datetime import datetime, timezone, timedelta

import psycopg

TZ = timezone(timedelta(hours=-3))
FECHA = "2026-09-30"
SEED = 20260930          # fijo y declarado => la muestra es reproducible
N_TOTAL = 50
N_CANDIDATOS = 28        # se incluyen todos (censo del estrato)
N_NO_RELEVANTE = N_TOTAL - N_CANDIDATOS

DIR = r"C:\Users\sever\OneDrive\Desktop\tfi-osint-n8n\V4\evidencias"
BASE = "muestra_control_50_2026-09-30"

SQL_MUESTRA = """
WITH candidatos AS (
    SELECT p.id, s.display_name, p.title, p.selftext, p.url,
           p.created_utc, p.score, p.num_comments,
           p.nlp_category, p.nlp_score,
           CASE WHEN p.nlp_category = 'No relevante'
                THEN 'no_relevante' ELSE 'amenaza' END AS estrato
    FROM posts p
    JOIN subreddits s ON s.id = p.subreddit_id
    WHERE p.nlp_category IS NOT NULL
),
sorteados AS (
    SELECT * FROM candidatos
    ORDER BY md5(id || :semilla)
)
SELECT * FROM sorteados
WHERE estrato = 'amenaza'
   OR estrato = 'no_relevante'
LIMIT :n
"""


def limpiar(txt, limite):
    """Deja el texto legible para un humano: sin HTML ni entities."""
    if not txt:
        return ""
    t = html.unescape(txt)
    t = re.sub(r"<[^>]+>", " ", t)
    t = unicodedata.normalize("NFC", t)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > limite:
        t = t[:limite].rsplit(" ", 1)[0] + " […]"
    return t


def main():
    with psycopg.connect(host=os.environ["PGHOST"], port=os.environ["PGPORT"],
                         dbname=os.environ["PGDATABASE"], user=os.environ["PGUSER"],
                         password=os.environ["PGPASSWORD"]) as c:
        with c.cursor() as cur:
            cur.execute("""
                SELECT p.id, s.display_name, p.title, p.selftext, p.url, p.created_utc,
                       p.score, p.num_comments, p.nlp_category, p.nlp_score,
                       CASE WHEN p.nlp_category = 'No relevante'
                            THEN 'no_relevante' ELSE 'amenaza' END
                FROM posts p JOIN subreddits s ON s.id = p.subreddit_id
                WHERE p.nlp_category IS NOT NULL
            """)
            filas = cur.fetchall()
            cur.execute("""
                SELECT count(*) FROM posts p JOIN subreddits s ON s.id=p.subreddit_id
                WHERE p.nlp_category = 'No relevante'
            """)
            n_no_rel = cur.fetchone()[0]
            cur.execute("""
                SELECT count(*) FROM posts p JOIN subreddits s ON s.id=p.subreddit_id
                WHERE p.nlp_category IS NOT NULL AND p.nlp_category <> 'No relevante'
            """)
            n_amenaza = cur.fetchone()[0]

    rnd = random.Random(SEED)
    amenaza = [f for f in filas if f[10] == "amenaza"]
    no_rel = [f for f in filas if f[10] == "no_relevante"]
    rnd.shuffle(amenaza)
    rnd.shuffle(no_rel)

    elegidas = amenaza[:N_CANDIDATOS] + no_rel[:N_NO_RELEVANTE]
    rnd.shuffle(elegidas)

    peso_ame = 1.0
    peso_nor = round(n_no_rel / N_NO_RELEVANTE, 2) if N_NO_RELEVANTE else 0

    # --- archivo 1: para el anotador, sin respuesta del modelo ---
    cols_et = ["post_id", "subreddit", "titulo", "cuerpo", "url",
               "creado_utc", "puntaje", "n_comentarios", "estrato",
               "categoria_humana", "anotador", "etiquetado_el",
               "criterio_aplicado", "notas"]
    ruta_et = os.path.join(DIR, f"{BASE}_POSTS.csv")
    with open(ruta_et, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(cols_et)
        for r in elegidas:
            creado = r[5].astimezone(TZ).strftime("%Y-%m-%dT%H:%M:%S%z") if r[5] else ""
            w.writerow([r[0], r[1], limpiar(r[2], 200), limpiar(r[3], 700),
                        r[4], creado, r[6], r[7], r[10],
                        "", "", "", "", ""])

    # --- archivo 2: la clave del modelo, fuera de la vista del anotador ---
    ruta_mod = os.path.join(DIR, f"{BASE}_RESPUESTA_MODELO.csv")
    with open(ruta_mod, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["post_id", "subreddit", "categoria_modelo", "score_modelo",
                    "estrato", "peso_muestreo"])
        for r in elegidas:
            peso = peso_ame if r[10] == "amenaza" else peso_nor
            w.writerow([r[0], r[1], r[8], r[9], r[10], peso])

    print(f"poblacion total clasificada : {len(filas)}")
    print(f"  estrato amenaza           : {n_amenaza}  (censo: {min(N_CANDIDATOS, n_amenaza)})")
    print(f"  estrato no_relevante      : {n_no_rel}  (muestreados: {N_NO_RELEVANTE}, peso {peso_nor})")
    print(f"muestra                     : {len(elegidas)}")
    print(f"semilla                     : {SEED}")
    print(f"\n{ruta_et}")
    print(ruta_mod)


if __name__ == "__main__":
    main()
