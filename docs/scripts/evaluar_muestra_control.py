"""Calculo de metricas de la muestra de control etiquetada (tarea 6.3/6.5).

Solo lee el CSV de etiquetas y el de la clave del modelo. No toca la base.

Advertencia: ponderar una muestra estratificada da una estimacion puntual con
intervalo muy ancho. Este script imprime el intervalo para que la cifra no se
lea como precisa. Con n=50 el recall NO es publicable.
"""
import csv
import io
import json
import math
import os
import sys
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding="utf-8")

EV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "evidencias")
ETIQUETAS = os.path.join(EV, "muestra_control_50_2026-09-30_ETIQUETAS.csv")
MODELO = os.path.join(EV, "muestra_control_50_2026-09-30_RESPUESTA_MODELO.csv")
SALIDA = os.path.join(EV, "evaluacion_muestra_control_2026-09-30.json")

AMENAZA = {"Phishing", "Robo de Credenciales", "Malware", "Ransomware",
           "Vulnerabilidades", "Filtración de Datos",
           "Infraestructura y Ataques", "Hacktivismo", "Ingenieria Social"}


def leer(ruta):
    with io.open(ruta, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    eti = leer(ETIQUETAS)
    mod = {r["post_id"]: r for r in leer(MODELO)}
    n = len(eti)

    TP = FP = FN = TN = 0
    exacto = 0
    confusion_cat = {}
    por_sub = {}

    for f in eti:
        pid = f["post_id"]
        h = f["categoria_humana"].strip()
        m = mod[pid]
        mc = m["categoria_modelo"]
        peso = float(m["peso_muestreo"])

        hv, mv = h in AMENAZA, mc in AMENAZA
        TP += hv and mv
        FP += (not hv) and mv
        FN += hv and (not mv)
        TN += (not hv) and (not mv)
        exacto += (h == mc)
        confusion_cat[f"{h} | {mc}"] = confusion_cat.get(f"{h} | {mc}", 0) + 1

        s = por_sub.setdefault(f["subreddit"], {"n": 0, "hum": 0, "mod": 0, "exacto": 0})
        s["n"] += 1
        s["hum"] += hv
        s["mod"] += mv
        s["exacto"] += (h == mc)

    prec = TP / (TP + FP) if (TP + FP) else 0.0
    rec = TP / (TP + FN) if (TP + FN) else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0

    # fiabilidad del recall sobre el estrato muestreado
    n_no_rel = sum(1 for f in eti if f["estrato"] == "no_relevante")
    p = FN / n_no_rel
    se = math.sqrt(p * (1 - p) / n_no_rel)
    lo, hi = max(0.0, p - 1.96 * se), min(1.0, p + 1.96 * se)
    poblacion = 473  # estrato No relevante de la poblacion de 501
    n_para_5p = math.ceil(p * (1 - p) * (1.96 / 0.05) ** 2)

    salida = {
        "generado": datetime.now(timezone(timedelta(hours=-3))).isoformat(),
        "muestra": {
            "n": n,
            "archivo": os.path.basename(ETIQUETAS),
            "anotador": sorted({f["anotador"].strip() for f in eti}),
            "fecha_etiquetado": sorted({f["etiquetado_el"].strip() for f in eti}),
            "diseno": "estratificada: censo de 28 amenazas + 22 sorteados de No relevante",
            "semilla": "20260930",
        },
        "criterio": {
            "estado": "acordado 2026-09-30 (tarea 6.1)",
            "texto": ("Cuenta como amenaza lo que describe un ataque o campana en curso, "
                      "real y verificable, aunque se publique como reporte. No cuenta el "
                      "material puramente educativo, de prevencion o catalogo."),
            "anotadores": 1,
            "kappa": None,
            "kappa_motivo": ("Cohen's Kappa no es calculable con un solo anotador. "
                             "No hay acuerdo entre anotadores que reportar y esta cifra "
                             "no puede presentarse como tal."),
        },
        "matriz_confusion_binaria": {
            "TP": TP, "FP": FP, "FN": FN, "TN": TN,
            "definicion": "amenaza si/no; TP = el modelo detecto una amenaza real",
        },
        "metricas_no_ponderadas": {
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "acierto_exacto_categoria": round(exacto / n, 4),
            "acierto_exacto_sobre": f"{exacto}/{n}",
        },
        "fiabilidad_del_recall": {
            "estrato_no_relevante": f"{FN}/{n_no_rel}",
            "proporcion_amenazas_ocultas": round(p, 4),
            "ic95": [round(lo, 4), round(hi, 4)],
            "proyeccion_no_detectadas_en_473": [round(poblacion * lo), round(poblacion * hi)],
            "n_requerido_para_ic_de_5_puntos": n_para_5p,
            "nota": ("Con n=50 el intervalo es demasiado ancho para publicar una cifra de "
                     "recall. El punto de partida es orientativo, no una metrica de la ventana."),
        },
        "concordancia_por_subreddit": {
            s: {"n": v["n"], "amenazas_humano": v["hum"],
                "amenazas_modelo": v["mod"], "categoria_exacta": v["exacto"]}
            for s, v in sorted(por_sub.items())
        },
        "confusion_por_categoria": confusion_cat,
    }

    with io.open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    print("matriz  TP=%d FP=%d FN=%d TN=%d  n=%d" % (TP, FP, FN, TN, n))
    print("precision=%.3f recall=%.3f F1=%.3f exacto=%d/%d" % (prec, rec, f1, exacto, n))
    print("ocultas en estrato No relevante: %d/%d = %.1f%% IC95 [%.1f%%, %.1f%%]"
          % (FN, n_no_rel, 100 * p, 100 * lo, 100 * hi))
    print("n para IC de +-5 puntos: ~%d" % n_para_5p)
    print("kappa: no calculable (1 anotador)")
    print("escrito:", SALIDA)


if __name__ == "__main__":
    main()
