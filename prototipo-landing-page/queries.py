"""Consultas del prototipo.

Cada funcion devuelve filas crudas y trae el SQL a la vista. Es deliberado:
la tesis exige que toda cifra presentada tenga su consulta, su fecha y su
ventana. Si estas consultas cambian, el README tiene que cambiar con ellas.
"""

from db import consultar, ZONA

# La zona horaria se fija en el SQL y no en Python, para que el dato no
# dependa de la maquina desde la que se mira el panel.
TZ = f"AT TIME ZONE '{ZONA}'"


def resumen() -> list[dict]:
    """KPIs de la cabecera.

    Ojo con la diferencia entre dos fechas que se parecen y no son lo mismo:
    `dias_recoleccion` cuenta dias en que el SISTEMA ingirio, mientras que
    `publicado_desde/hasta` abarca cuando se publico cada post. El feed
    `new/.rss` devuelve tambien publicaciones viejas, asi que hoy puede
    haber 1 dia de recoleccion y 83 dias distintos de publicacion.
    """
    return consultar(f"""
        SELECT
          COUNT(*)                                                   AS total_posts,
          COUNT(*) FILTER (WHERE nlp_category IS NOT NULL
                             AND nlp_category <> 'No relevante')    AS con_senal,
          COUNT(*) FILTER (WHERE nlp_category = 'No relevante')     AS sin_senal,
          COUNT(DISTINCT subreddit_id)                               AS comunidades,
          COUNT(DISTINCT (ingested_at {TZ})::date)                  AS dias_recoleccion,
          MIN(ingested_at {TZ})::date                               AS desde,
          MAX(ingested_at {TZ})::date                               AS hasta,
          MAX(ingested_at {TZ})::date                                AS ultima_carga,
          MIN((created_utc {TZ})::date)                             AS publicado_desde,
          MAX((created_utc {TZ})::date)                             AS publicado_hasta
        FROM posts
    """)


def por_comunidad() -> list[dict]:
    """Volumen por subreddit y proporcion con senal clasificada."""
    return consultar(f"""
        SELECT s.display_name,
               COUNT(*)                                                AS total,
               COUNT(*) FILTER (WHERE p.nlp_category IS NOT NULL
                                  AND p.nlp_category <> 'No relevante') AS con_senal,
               ROUND(100.0 * COUNT(*) FILTER (WHERE p.nlp_category IS NOT NULL
                                                 AND p.nlp_category <> 'No relevante')
                     / NULLIF(COUNT(*), 0), 1)                         AS pct_senal
        FROM posts p
        JOIN subreddits s ON s.id = p.subreddit_id
        GROUP BY s.display_name
        ORDER BY total DESC
    """)


def comunidades_con_estado() -> list[dict]:
    """Volumen por subreddit con su estado de monitoreo (para la v2).

    LEFT JOIN para incluir subreddits sin posts (p. ej. r/derechogenial,
    desactivada por alcance tematico IN-07 con 0 posts). El frente decide
    que mostrar: el alcance activo es `active_monitoring = true`.
    """
    return consultar(f"""
        SELECT s.display_name,
               s.active_monitoring,
               COUNT(p.id)                                            AS total,
               COUNT(p.id) FILTER (WHERE p.nlp_category IS NOT NULL
                                     AND p.nlp_category <> 'No relevante') AS con_senal,
               ROUND(100.0 * COUNT(p.id) FILTER (WHERE p.nlp_category IS NOT NULL
                                                   AND p.nlp_category <> 'No relevante')
                     / NULLIF(COUNT(p.id), 0), 1)                     AS pct_senal
        FROM subreddits s
        LEFT JOIN posts p ON p.subreddit_id = s.id
        GROUP BY s.display_name, s.active_monitoring
        ORDER BY s.active_monitoring DESC, total DESC
    """)


def por_categoria() -> list[dict]:
    """Distribucion por las 9 categorias del diccionario mas 'No relevante'."""
    return consultar("""
        SELECT COALESCE(nlp_category, '(sin clasificar)')            AS categoria,
               COUNT(*)                                             AS total,
               ROUND(AVG(nlp_score)::numeric, 3)                    AS score_promedio
        FROM posts
        GROUP BY 1
        ORDER BY total DESC
    """)


def serie_diaria(categoria: str | None = None) -> list[dict]:
    """Posts ingeridos por dia, para ver el ritmo de recoleccion.

    Filtro opcional por categoria (nlp_category).
    """
    where = "WHERE nlp_category = %s" if categoria else ""
    params = (categoria,) if categoria else ()
    return consultar(f"""
        SELECT (ingested_at {TZ})::date AS dia,
               COUNT(*)               AS total,
               COUNT(*) FILTER (WHERE nlp_category IS NOT NULL
                                  AND nlp_category <> 'No relevante') AS con_senal
        FROM posts
        {where}
        GROUP BY 1
        ORDER BY 1
    """, params)


def anomalias() -> list[dict]:
    """Anomalias registradas por el motor de n8n.

    La tabla arranca vacia y se llena sola cuando corre el nodo de anomalias.
    Si devuelve [], no es un error del panel: todavia no se ejecuto esa rama.
    """
    return consultar(f"""
        SELECT a.id,
               (a.ventana_inicio {TZ})::date      AS dia,
               a.categoria,
               a.n_observado,
               ROUND(a.base_media::numeric, 2)    AS base_media,
               ROUND(a.umbral::numeric, 2)        AS umbral,
               a.disparo,
               EXISTS (SELECT 1 FROM alertas al WHERE al.anomalia_id = a.id) AS genero_alerta
        FROM anomalias a
        ORDER BY a.ventana_inicio DESC, a.categoria
        LIMIT 200
    """)


def entidades(tipo: str = "products", limite: int = 12) -> list[dict]:
    """Menciones mas frecuentes de un tipo de entidad.

    `entities` es jsonb con las claves ips, cves, emails, domains, products.
    El tipo se valida contra esa lista para no interpolarlo en el SQL.
    """
    permitidos = ("ips", "cves", "emails", "domains", "products")
    if tipo not in permitidos:
        raise ValueError(f"tipo de entidad no valido: {tipo}")
    return consultar(
        f"""
        SELECT e.value AS entidad, COUNT(*) AS menciones
        FROM posts p, LATERAL jsonb_array_elements_text(
             COALESCE(p.entities -> '{tipo}', '[]'::jsonb)
        ) AS e(value)
        GROUP BY e.value
        ORDER BY menciones DESC, entidad
        LIMIT %s
        """,
        (limite,),
    )


def distribucion_score() -> list[dict]:
    """Score de significancia en tramos. El 0.0 es la bolsa 'No relevante'."""
    return consultar("""
        SELECT CASE
                 WHEN nlp_score IS NULL THEN 'sin clasificar'
                 WHEN nlp_score = 0     THEN '0.00'
                 WHEN nlp_score < 0.5   THEN '0.01-0.49'
                 WHEN nlp_score < 0.75  THEN '0.50-0.74'
                 WHEN nlp_score < 1     THEN '0.75-0.99'
                 ELSE '1.00'
               END                            AS tramo,
               ROUND(MIN(nlp_score)::numeric, 2) AS desde,
               ROUND(MAX(nlp_score)::numeric, 2) AS hasta,
               COUNT(*)                      AS total
        FROM posts
        GROUP BY 1
        ORDER BY desde NULLS FIRST
    """)


def ultimos_posts(limite: int = 15, categoria: str | None = None,
                 desde: str | None = None, hasta: str | None = None) -> list[dict]:
    """Ultimos posts ingeridos, con su categoria.

    Filtros opcionales: categoria (nlp_category), desde/hasta (fecha de ingesta).
    """
    condiciones = []
    params = [ZONA, ZONA]
    if categoria:
        condiciones.append("p.nlp_category = %s")
        params.append(categoria)
    if desde:
        condiciones.append("(p.ingested_at AT TIME ZONE %s)::date >= %s")
        params.extend([ZONA, desde])
    if hasta:
        condiciones.append("(p.ingested_at AT TIME ZONE %s)::date <= %s")
        params.extend([ZONA, hasta])
    where = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""
    params.append(limite)
    sql = f"""
        SELECT p.id, s.display_name, p.title, p.nlp_category,
               ROUND(p.nlp_score::numeric, 2) AS nlp_score,
               (p.created_utc AT TIME ZONE %s)::date AS publicado,
               (p.ingested_at AT TIME ZONE %s)::time(0) AS ingests,
               p.url
        FROM posts p
        JOIN subreddits s ON s.id = p.subreddit_id
        {where}
        ORDER BY p.ingested_at DESC
        LIMIT %s
    """
    return consultar(sql, tuple(params))


# Criterio de suficiencia de la ventana B5, decidido el 2026-10-09:
# piso de 10 dias completos de evaluaciones de anomalias (base comparativa de
# RN-AN-02), objetivo declarado de 15 (dos ciclos semanales). El objetivo NO
# cierra la ventana: eso lo decide la tarea 6.1.
DIAS_MINIMO = 10
DIAS_OBJETIVO = 15


def suficiencia() -> list[dict]:
    """Dias completos evaluados por el motor de anomalias y estado de la ventana.

    Un dia cuenta una sola vez por cada `ventana_inicio` distinta en
    `anomalias`: esa fecha es el dia cuyos datos evaluo la corrida, no el dia
    en que corrio. `disparos` son las filas que superaron su umbral, no las
    alertas enviadas (la alerta es otro registro).
    """
    filas = consultar(f"""
        SELECT COUNT(DISTINCT (ventana_inicio {TZ})::date)  AS dias_completos,
               MIN((ventana_inicio {TZ})::date)             AS primer_dia,
               MAX((ventana_inicio {TZ})::date)             AS ultimo_dia,
               COUNT(*) FILTER (WHERE disparo)              AS disparos
        FROM anomalias
    """)
    fila = dict(filas[0])
    fila["minimo"] = DIAS_MINIMO
    fila["objetivo"] = DIAS_OBJETIVO
    dias = fila["dias_completos"] or 0
    if dias >= DIAS_OBJETIVO:
        fila["estado"] = "objetivo_alcanzado"
    elif dias >= DIAS_MINIMO:
        fila["estado"] = "minimo_alcanzado"
    else:
        fila["estado"] = "abierta"
    return [fila]


def alertas(limite: int = 50) -> list[dict]:
    """Alertas generadas por el motor de anomalias.

    La tabla arranca vacia y se llena cuando el motor detecta un disparo.
    Si devuelve [], no es un error: todavia no se ejecuto esa rama o no hubo disparos.
    """
    return consultar("""
        SELECT a.id,
               (a.created_at AT TIME ZONE %s)::date AS fecha,
               an.categoria,
               an.n_observado,
               ROUND(an.umbral::numeric, 2) AS umbral,
               a.estado,
               a.canal
        FROM alertas a
        JOIN anomalias an ON an.id = a.anomalia_id
        ORDER BY a.created_at DESC
        LIMIT %s
    """, (ZONA, limite))


def regimen_operacion() -> list[dict]:
    """Regimen de operacion de la instancia por dia.

    Reconstruye las jornadas desde ingested_at.
    """
    return consultar("""
        SELECT (ingested_at AT TIME ZONE %s)::date AS fecha,
               COUNT(*) AS publicaciones,
               MIN(ingested_at AT TIME ZONE %s)::time(0) AS primera_ingesta,
               MAX(ingested_at AT TIME ZONE %s)::time(0) AS ultima_ingesta
        FROM posts
        GROUP BY 1
        ORDER BY 1
    """, (ZONA, ZONA, ZONA))


def latencia_por_estado() -> list[dict]:
    """Latencia descompuesta por grupo de publicaciones."""
    return consultar("""
        SELECT
          CASE
            WHEN created_utc >= '2026-10-01 00:00:00+00' THEN 'en_ventana'
            ELSE 'arrastre_inicial'
          END AS grupo,
          COUNT(*) AS n,
          ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (ingested_at - created_utc)) / 60)::numeric, 1) AS p50_min,
          ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (ingested_at - created_utc)) / 60)::numeric, 1) AS p95_min,
          ROUND(MAX(EXTRACT(EPOCH FROM (ingested_at - created_utc)) / 60)::numeric, 1) AS max_min
        FROM posts
        GROUP BY 1
        ORDER BY 1
    """)

def alertas(limite: int = 50) -> list[dict]:
    return consultar("""
        SELECT a.id,
               (a.created_at AT TIME ZONE %s)::date AS fecha,
               an.categoria,
               an.n_observado,
               ROUND(an.umbral::numeric, 2) AS umbral,
               a.estado,
               a.canal
        FROM alertas a
        JOIN anomalias an ON an.id = a.anomalia_id
        ORDER BY a.created_at DESC
        LIMIT %s
    """, (ZONA, limite))


def regimen_operacion() -> list[dict]:
    return consultar("""
        SELECT (ingested_at AT TIME ZONE %s)::date AS fecha,
               COUNT(*) AS publicaciones,
               MIN(ingested_at AT TIME ZONE %s)::time(0) AS primera_ingesta,
               MAX(ingested_at AT TIME ZONE %s)::time(0) AS ultima_ingesta
        FROM posts
        GROUP BY 1
        ORDER BY 1
    """, (ZONA, ZONA, ZONA))
