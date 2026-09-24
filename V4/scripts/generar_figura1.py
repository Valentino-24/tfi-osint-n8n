# -*- coding: utf-8 -*-
"""
Figura 1 — Arquitectura E2E del sistema (TFI OSINT/n8n V4)
Genera el diagrama de arquitectura que se va a usar en el Capítulo 4.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(14, 8.2), dpi=150)
ax.set_xlim(0, 14)
ax.set_ylim(0, 8.2)
ax.axis("off")

# ---------------------------------------------------------------- helpers
def box(x, y, w, h, text, fc="#eaf2fb", ec="#2f6db3", fs=9, weight="bold"):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle="round,pad=0.06,rounding_size=0.12",
                       linewidth=1.4, edgecolor=ec, facecolor=fc)
    ax.add_patch(p)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fs, weight=weight, linespacing=1.35)

def arrow(x1, y1, x2, y2, color="#3a3a3a", lw=1.6, style="-|>"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                        mutation_scale=16, linewidth=lw, color=color)
    ax.add_patch(a)

# ---------------------------------------------------------------- fuente
box(0.45, 6.55, 1.7, 1.15, "Reddit\nsubreddits AR\n(r/argentina,\nr/derechogenial)", fc="#fdeeee", ec="#b3382c")

# ---------------------------------------------------------------- contenedor n8n
n8n = FancyBboxPatch((2.55, 3.9), 10.9, 4.1,
                     boxstyle="round,pad=0.08,rounding_size=0.15",
                     linewidth=1.8, edgecolor="#5b5b5b", facecolor="#f5f5f5")
ax.add_patch(n8n)
ax.text(2.8, 7.78, "n8n — workflow E2E (estimación cada 15 min)",
        fontsize=11, weight="bold", color="#333")

# nodos del pipeline (x, y, w, h)
bx = 2.85
bw = 1.62
bh = 2.55
by = 4.55
step = 1.78

nodos = [
    ("Trigger\ncron\n15 min", "every node", "#eef3fa"),
    ("HTTP Request\nReddit JSON", "HTTP", "#eef3fa"),
    ("Code\nnormalizar +\nseudonimizar\n(HMAC-SHA-256)", "normalize", "#fff8e1"),
    ("PostgreSQL\nupsert posts", "persist", "#e8f5e9"),
    ("Code\nclasificador\ndiccionario", "classify", "#e3f0ff"),
    ("Code\nmotor de\nanomalias", "anomalies", "#f3e5f5"),
]
for i, (txt, tag, fc) in enumerate(nodos):
    box(bx + i*step, by, bw, bh, txt, fc=fc, fs=8.2)

# flechas entre nodos
for i in range(len(nodos) - 1):
    arrow(bx + i*step + bw, by + bh/2, bx + (i+1)*step, by + bh/2)

# Reddit -> primer nodo
arrow(2.15, 7.1, bx, by + bh/2)

# nodo persist -> PostgreSQL  / nodo clasificador -> PostgreSQL (update)
pg_x, pg_y, pg_w, pg_h = 9.35, 1.6, 2.5, 1.05
box(pg_x, pg_y, pg_w, pg_h, "PostgreSQL\nposts · comments\nanomalias · alertas", fc="#e8f5e9", ec="#2e7d32", fs=8.5)
arrow(bx + 3*step + bw/2, by - 0.06, pg_x + pg_w/2, pg_y + pg_h + 0.06, color="#2e7d32")
arrow(bx + 4*step + bw/2, by - 0.06, pg_x + pg_w/2 - 0.55, pg_y + pg_h + 0.06, color="#2e7d32")

# nodo anomalias -> Alertas
box(4.6, 1.6, 2.05, 1.05, "Alertas\nTelegram /\nwebhook (OE6)", fc="#fdeeee", ec="#b3382c", fs=8.2)
arrow(bx + 5*step + bw/2, by - 0.06, 5.6, pg_y + pg_h + 0.06, color="#b3382c")

# ---------------------------------------------------------------- evidencias
box(12.0, 6.55, 1.75, 1.15, "Evidencias\nexport JSON\n(Anexo B)", fc="#f3e5f5", ec="#6a1b9a", fs=8.2)
arrow(pg_x + pg_w, pg_y + pg_h/2, 12.0, 6.15, color="#6a1b9a")
ax.text(7.0, 0.9, "Consultas SQL (Tabla 3 · latencia · serie horaria)  →  evidencias E4/E6/E7/E13",
        ha="center", fontsize=8.5, style="italic", color="#444")

ax.set_title("Figura 1. Arquitectura extremo a extremo del sistema de monitoreo OSINT (flujo real propuesto para V4)",
             fontsize=11.5, weight="bold", pad=14)

plt.tight_layout()
out = r"C:\Users\valen\Desktop\Tesis\V4\figuras\Figura_1_arquitectura.png"
plt.savefig(out, bbox_inches="tight", facecolor="white")
print("OK ->", out)