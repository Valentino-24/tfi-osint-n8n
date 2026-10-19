# -*- coding: utf-8 -*-
"""
Genera las cuatro figuras del informe V4 (2026-10-19) a partir de datos reales.

Fuentes de los datos:
  - V4/evidencias/informe_v4_2026-10-19/consultas_corpus_b5.txt  (consultas Q1-Q15 del 2026-10-19)
  - V4/anexos/A_DDL.sql                                          (esquema fisico, 5 tablas)
  - V4/anexos/B_workflow.json                                    (workflow desplegado, 17 nodos, active=1)
  - V4/evidencias/evaluacion_muestra_control_2026-09-30.md/JSON  (muestra de control n=50)

Salidas (PNG, 200 dpi):
  - V4/figuras/Figura_1_arquitectura.png
  - V4/figuras/Figura_2_der.png
  - V4/figuras/Figura_3_workflow.png
  - V4/figuras/Figura_4_serie_temporal.png

No modifica la base, ni el DDL, ni el workflow, ni sus evidencias.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

RAIZ = r"C:\Users\sever\OneDrive\Desktop\tfi-osint-n8n"
FIG = os.path.join(RAIZ, "V4", "figuras")
DPI = 200

AZUL = "#1f4e79"
CELESTE = "#deebf7"
GRIS = "#595959"
NARANJA = "#b45309"
VERDE = "#1e6f4f"
ROJO = "#a11a1a"


def caja(ax, x, y, w, h, texto, color=CELESTE, borde=AZUL, size=8, bold=False, radio=0.02):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.004,rounding_size={radio}",
                                linewidth=1.1, edgecolor=borde, facecolor=color, zorder=2))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=size,
            color="#111111", zorder=3, fontweight="bold" if bold else "normal", wrap=True)


def flecha(ax, p1, p2, color=GRIS, estilo="-|>", ls="-", lw=1.2, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=estilo, mutation_scale=11,
                                 linewidth=lw, color=color, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}", zorder=1))


# ---------------------------------------------------------------- Figura 1
def figura_1():
    fig, ax = plt.subplots(figsize=(10.4, 6.4))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 62)
    ax.axis("off")

    ax.text(1, 59.6, "Figura 1. Arquitectura del sistema OSINT: capas, nodos y artefactos reales",
            fontsize=10.5, fontweight="bold", color="#111111")

    # Capa 1: fuentes
    caja(ax, 1.5, 44, 20, 11, "FUENTES PÚBLICAS\n\nReddit RSS/Atom\nnew/.rss?limit=100\n\nr/netsec · r/Malware\nr/devsarg", CELESTE, AZUL, 7.6, True)
    # Capa 2: ingesta
    caja(ax, 25, 44, 30, 11, "INGESTA (n8n, cada 15 min)\n\nSchedule Ingesta → Prepare/Upsert Subreddits\n→ Loop Over Items (3 feeds)\n→ Espera 60 s → Fetch Posts RSS\n→ Parse → HMAC → Clasificador → Entidades", "#eaf3e6", VERDE, 7.4, True)
    # Capa 3: persistencia
    caja(ax, 58.5, 44, 40, 11, "PERSISTENCIA (PostgreSQL 18 · tesi_osint)\n\nUpsert Posts (ON CONFLICT id DO UPDATE)\n\n5 tablas: subreddits · posts · comments\nanomalias · alertas", "#fdf3e3", NARANJA, 7.4, True)
    # Capa 4: motor
    caja(ax, 58.5, 26, 40, 12, "MOTOR DE ANOMALÍAS (n8n, diario 12:05)\n\nQuery Daily Counts (SELECT, ventana móvil 11 días)\n→ Anomaly Engine (umbral Poisson q95 + piso 3)\n→ Registrar Anomalías y Alertas", "#f3e8f7", "#6b3fa0", 7.4, True)
    # Capa 5: alertas
    caja(ax, 58.5, 12, 40, 9, "ALERTAS\n\nTabla alertas (canal = telegram)\nSend Telegram Alert — DESHABILITADO por defecto\n(OE6: implementado, sin envío real)", "#fbeaea", ROJO, 7.4, True)

    flecha(ax, (21.5, 49.5), (25, 49.5), AZUL, lw=1.6)
    flecha(ax, (55, 49.5), (58.5, 49.5), VERDE, lw=1.6)
    flecha(ax, (78.5, 44), (78.5, 38), NARANJA, lw=1.6)
    flecha(ax, (78.5, 26), (78.5, 21), "#6b3fa0", lw=1.6)
    flecha(ax, (58.5, 32), (55, 40), GRIS, ls="--", rad=-0.15)
    ax.text(44.5, 33.5, "counts diarios\n(SELECT)", fontsize=6.6, color=GRIS, ha="center")

    # bloque inferior: detalle tecnico
    caja(ax, 1.5, 12, 53, 26, "", "#ffffff", "#bfbfbf", 7.2)
    ax.text(3, 35.4, "Controles transversales", fontsize=9, fontweight="bold", color="#111111")
    detalle = [
        "Seudonimización: HMAC-SHA-256 con clave por despliegue",
        "(variable de entorno OSINT_HMAC_KEY); no se persiste el usuario.",
        "Idempotencia: PRIMARY KEY (id) + ON CONFLICT … DO UPDATE sobre 13 columnas.",
        "Rate limiting: espera fija de 60 s entre feeds y centinela `_skip`",
        "para cerrar el loop cuando un feed falla (HTTP 429).",
        "Clasificador: diccionario de 9 categorías y 201 términos; score",
        "saturante min(1, hits/4); MIN_HITS = 1; sin lematización.",
        "Entidades: CVE, correos, IP, dominios y productos por coincidencia",
        "de subcadena (limitación declarada, IN-06).",
        "Volumen real de la ventana B5: 724 posts en 15 días completos,",
        "3 subreddits, 171 ciclos de ingesta con contenido.",
    ]
    for i, linea in enumerate(detalle):
        ax.text(3, 33.2 - i * 2.02, "• " + linea, fontsize=6.8, color="#222222")

    ax.text(1, 7.2, "Fuentes: V4/anexos/B_workflow.json (17 nodos, active = 1) · V4/anexos/A_DDL.sql · "
                   "consultas archivadas en V4/evidencias/informe_v4_2026-10-19/consultas_corpus_b5.txt (2026-10-19).",
            fontsize=6.6, color=GRIS, style="italic")
    fig.savefig(os.path.join(FIG, "Figura_1_arquitectura.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- Figura 2
def figura_2():
    fig, ax = plt.subplots(figsize=(10.4, 6.0))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 62)
    ax.axis("off")
    ax.text(1, 59.8, "Figura 2. Modelo entidad-relación del esquema físico (V4/anexos/A_DDL.sql)",
            fontsize=10.5, fontweight="bold")

    def tabla(x, y, w, titulo, filas, borde=AZUL, alto=4.6):
        h = 6.4 + alto * len(filas)
        ax.add_patch(Rectangle((x, y), w, h, facecolor="white", edgecolor=borde, linewidth=1.4, zorder=2))
        ax.add_patch(Rectangle((x, y + h - 4.6), w, 4.6, facecolor=borde, edgecolor=borde, zorder=3))
        ax.text(x + w / 2, y + h - 2.3, titulo, color="white", fontsize=8, fontweight="bold",
                ha="center", va="center", zorder=4)
        for i, (f, t) in enumerate(filas):
            yy = y + h - 4.6 - alto * (i + 1) + alto / 2
            ax.text(x + 1.1, yy, f, fontsize=6.6, va="center", zorder=4)
            ax.text(x + w - 1.1, yy, t, fontsize=6.2, va="center", ha="right", color="#444444", zorder=4)
        return (x, y, w, h)

    sub = tabla(2, 40, 30, "subreddits", [
        ("id  VARCHAR(50)  PK", ""),
        ("display_name  VARCHAR(100)", "UNIQUE, NOT NULL"),
        ("subscribers  INTEGER", "DEFAULT 0"),
        ("active_monitoring  BOOLEAN", "DEFAULT TRUE"),
        ("created_at  TIMESTAMPTZ", "DEFAULT now()"),
    ])
    pos = tabla(38, 30, 38, "posts", [
        ("id  VARCHAR(50)  PK", ""),
        ("subreddit_id  VARCHAR(50)  FK → subreddits", "RESTRICT"),
        ("title / selftext / url", "NOT NULL / — / —"),
        ("author_hash  CHAR(64)", "NOT NULL (HMAC)"),
        ("score / num_comments  INTEGER", "DEFAULT 0"),
        ("created_utc  TIMESTAMPTZ", "NOT NULL"),
        ("nlp_category  VARCHAR(100)", "—"),
        ("nlp_score  REAL", "CHECK 0–1"),
        ("entities  JSONB", "—"),
        ("nlp_processed  BOOLEAN", "DEFAULT false"),
        ("ingested_at  TIMESTAMPTZ", "DEFAULT now()"),
    ])
    com = tabla(2, 12, 30, "comments", [
        ("id  VARCHAR(50)  PK", ""),
        ("post_id  VARCHAR(50)  FK → posts", "CASCADE"),
        ("body  TEXT", "NOT NULL"),
        ("author_hash  CHAR(64)", "NOT NULL"),
        ("score / created_utc", "—"),
        ("nlp_category / nlp_score", "—"),
        ("nlp_processed / ingested_at", "—"),
    ])
    ano = tabla(38, 12, 38, "anomalias", [
        ("id  BIGSERIAL  PK", ""),
        ("ventana_inicio / ventana_fin", "TIMESTAMPTZ, NOT NULL"),
        ("categoria  VARCHAR(100)", "NOT NULL"),
        ("n_observado / base_media / umbral", "INT / REAL / REAL"),
        ("disparo  BOOLEAN", "DEFAULT false"),
        ("created_at  TIMESTAMPTZ", "DEFAULT now()"),
    ])
    ale = tabla(80, 30, 18, "alertas", [
        ("id  BIGSERIAL  PK", ""),
        ("anomalia_id  FK → anomalias", "CASCADE"),
        ("canal  VARCHAR(50)", "NOT NULL"),
        ("destinatario / payload", "— / JSONB"),
        ("estado  VARCHAR(20)", "DEFAULT ENVIADA"),
        ("created_at", "DEFAULT now()"),
    ])

    flecha(ax, (32, 52), (38, 52), AZUL, lw=1.3)
    ax.text(35, 53.2, "1:N", fontsize=6.4, color=AZUL, ha="center")
    flecha(ax, (17, 40), (17, 30), AZUL, lw=1.3)
    ax.text(18, 35, "1:N", fontsize=6.4, color=AZUL)
    flecha(ax, (57, 12), (57, 8.4), "#6b3fa0", lw=1.3)
    flecha(ax, (76, 30), (89, 30), ROJO, lw=1.3)
    ax.text(82.5, 31.2, "1:N", fontsize=6.4, color=ROJO, ha="center")
    ax.text(50, 7.2, "ON DELETE RESTRICT en posts.subreddit_id · ON DELETE CASCADE en comments.post_id, "
                     "alertas.anomalia_id (y en anomalias no hay FK saliente).",
            fontsize=6.8, color=GRIS, ha="center")
    ax.text(1, 3.6, "Índices: idx_posts_created_utc (btree desc) · idx_posts_nlp_category · idx_posts_ingested_at · "
                    "idx_comments_post_id · idx_anomalias_created_at. La tabla comments existe pero no se pobló en la ventana B5 (0 filas).",
            fontsize=6.6, color=GRIS)
    fig.savefig(os.path.join(FIG, "Figura_2_der.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- Figura 3
def figura_3():
    ruta = os.path.join(RAIZ, "V4", "anexos", "B_workflow.json")
    with open(ruta, encoding="utf-8") as fh:
        wf = json.load(fh)
    nodos = {n["name"]: n for n in wf["nodes"]}
    conex = {}
    for origen, ramas in wf.get("connections", {}).items():
        destinos = []
        for rama in ramas.get("main", []):
            for d in rama:
                destinos.append((d["node"], d.get("index", 0)))
        conex[origen] = destinos

    pos = {
        "Schedule Ingesta": (2, 46), "Prepare Subreddits": (20, 46), "Upsert Subreddits": (20, 36),
        "Loop Over Items": (38, 46), "Espera Rate Limit": (38, 36), "Fetch Posts RSS": (38, 26),
        "Parse Reddit Posts": (56, 26), "HMAC Anonymize": (74, 26), "Classify Dictionary": (74, 15),
        "Extract Entities": (74, 4), "Prepare Upsert": (56, 4), "Upsert Posts": (36, 4),
        "Schedule Anomalias": (2, 36), "Query Daily Counts": (2, 26), "Anomaly Engine": (2, 15),
        "Registrar Anomalias y Alertas": (2, 4), "Send Telegram Alert": (20, 4),
    }
    ancho, alto = 16, 7
    fig, ax = plt.subplots(figsize=(11.0, 6.6))
    ax.set_xlim(0, 94)
    ax.set_ylim(0, 58)
    ax.axis("off")
    ax.text(0.5, 56.2, f"Figura 3. Grafo de nodos y conexiones del workflow desplegado ({wf['name']})",
            fontsize=10.5, fontweight="bold")
    ax.text(0.5, 52.6, f"{len(wf['nodes'])} nodos · active = {str(wf.get('active')).lower()} · "
                       "generado desde el propio export JSON (las conexiones se leen del archivo).",
            fontsize=7.4, color=GRIS)
    for nombre, (x, y) in pos.items():
        tipo = nodos[nombre]["type"].split(".")[-1]
        color = CELESTE
        borde = AZUL
        if tipo == "scheduleTrigger":
            color, borde = "#fdf3e3", NARANJA
        elif tipo == "postgres":
            color, borde = "#eaf3e6", VERDE
        elif tipo == "code":
            color, borde = "#f3e8f7", "#6b3fa0"
        elif tipo == "httpRequest":
            color, borde = "#fbeaea", ROJO
        elif tipo in ("wait", "splitInBatches"):
            color, borde = "#f2f2f2", GRIS
        caja(ax, x, y, ancho, alto, nombre + "\n" + tipo, color, borde, 6.0, True)
    for origen, destinos in conex.items():
        if origen not in pos:
            continue
        x1, y1 = pos[origen]
        for destino, idx in destinos:
            if destino not in pos:
                continue
            x2, y2 = pos[destino]
            p1 = (x1 + ancho / 2, y1 + (alto if y2 > y1 else 0))
            p2 = (x2 + ancho / 2, y2 + (0 if y2 > y1 else alto))
            estilo = "-|>" if idx == 0 else "-|>"
            flecha(ax, p1, p2, "#666666", estilo, lw=1.0, rad=0.12)
    ax.text(56, 0.4, "Rama principal (índice 0) en trazo continuo. El loop se cierra desde Extract Entities hacia Loop Over Items "
                     "con el centinela `_skip`.", fontsize=6.6, color=GRIS)
    fig.savefig(os.path.join(FIG, "Figura_3_workflow.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- Figura 4
def figura_4():
    # Serie de ingesta (consultas Q4 y Q3 archivadas el 2026-10-19)
    dias = ["10-01", "10-02", "10-04", "10-05", "10-06", "10-07", "10-08", "10-09", "10-10",
            "10-11", "10-12", "10-13", "10-14", "10-15", "10-16", "10-17"]
    posts = [307, 32, 37, 25, 39, 16, 35, 31, 26, 17, 31, 28, 28, 31, 33, 8]
    eventos = [8, 10, 7, 9, 17, 10, 15, 13, 7, 9, 12, 14, 11, 11, 16, 3]
    cats = ["Malware", "Vulnerabilidades", "Phishing", "Robo de Credenciales", "Filtración de Datos",
            "Ransomware", "Infraestructura y Ataques", "Hacktivismo"]
    n_cat = [79, 61, 12, 5, 4, 4, 3, 2]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 4.3), gridspec_kw={"width_ratios": [1.55, 1]})
    x = range(len(dias))
    ax1.bar(x, posts, color=AZUL, width=0.62, label="Posts ingresados")
    ax1.plot(x, eventos, color=NARANJA, marker="o", markersize=3.4, linewidth=1.3,
             label="Ciclos de ingesta con contenido")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(dias, rotation=60, fontsize=7)
    ax1.set_ylabel("Publicaciones", fontsize=8)
    ax1.tick_params(axis="y", labelsize=7)
    ax1.set_title("(a) Ingesta diaria — ventana B5 (2026-10-01 a 2026-10-17)", fontsize=8.6)
    ax1.legend(fontsize=7, frameon=False)
    ax1.grid(axis="y", alpha=0.25)
    ax1.annotate("primer ciclo:\nbackfill del feed\n(287 posts previos)", xy=(0, 307), xytext=(1.1, 250),
                 fontsize=6.6, color=GRIS, arrowprops=dict(arrowstyle="->", color=GRIS, lw=0.8))
    ax1.annotate("sin recolección\nel 10-03", xy=(2, 37), xytext=(2.4, 120), fontsize=6.6, color=ROJO,
                 arrowprops=dict(arrowstyle="->", color=ROJO, lw=0.8))

    ypos = range(len(cats))[::-1]
    ax2.barh(list(ypos), n_cat, color=VERDE, height=0.62)
    ax2.set_yticks(list(ypos))
    ax2.set_yticklabels(cats, fontsize=7)
    ax2.set_xlabel("Publicaciones clasificadas", fontsize=8)
    ax2.tick_params(axis="x", labelsize=7)
    ax2.set_title("(b) Categorías detectadas (n = 170)", fontsize=8.6)
    ax2.grid(axis="x", alpha=0.25)
    for y, v in zip(ypos, n_cat):
        ax2.text(v + 1.4, y, str(v), fontsize=7, va="center", color="#222222")
    ax2.text(0, -1.55, "La categoría «Ingeniería Social» (20 términos) no registró coincidencias.\n"
                       "El residual «No relevante» (554) no se grafica.", fontsize=6.4, color=GRIS)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "Figura_4_serie_temporal.png"), dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    figura_1()
    figura_2()
    figura_3()
    figura_4()
    for nombre in ("Figura_1_arquitectura.png", "Figura_2_der.png", "Figura_3_workflow.png", "Figura_4_serie_temporal.png"):
        ruta = os.path.join(FIG, nombre)
        print(nombre, os.path.getsize(ruta), "bytes")
