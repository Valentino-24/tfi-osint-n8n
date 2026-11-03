# -*- coding: utf-8 -*-
"""
Estimacion postestratificada de la sensibilidad por comunidad e idioma.

Origen de los datos: docs/evidencias/informe_v5_2026-10-20/evidencia_v5.zip
  -> evidencia-muestreo/resultados_v5.json  (TP censados, k observados y n0 por comunidad)
  -> y Tabla 5.1 del informe (tamano del estrato negativo N0 por comunidad).

Metodo (3.3.5 del informe):
  sensibilidad_comunidad = TP / (TP + N0 * p), con p = k/n0 la proporcion de amenazas
  observada en la muestra del estrato negativo de esa comunidad.
  IC 95 %: Clopper-Pearson exacto sobre p, transformado a la sensibilidad.

Entrada del calculo (fecha: 2026-11-02):
  comunidad    TP   N0   n0    k
  r/devsarg     3  421  135    2
  r/netsec     60   84   29   15
  r/Malware    81   49   18   13
  Total       144  554  182   30   (N0 = 554 no relevante; n0 = 182 sorteadas)

Uso: python docs/evidencias/informe_v6_2026-11-02/sensibilidad_por_comunidad.py
"""

import math

# --------------------------------------------------------------------------
# Distribucion beta incompleta regularizada e inversa (Clopper-Pearson)
# Implementacion de Numerical Recipes; no requiere scipy.
# --------------------------------------------------------------------------


def _betacf(a, b, x):
    MAXIT, EPS, FPMIN = 300, 3e-16, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < EPS:
            break
    return h


def _betai(a, b, x):
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def _beta_ppf(q, a, b):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if _betai(a, b, mid) < q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def clopper_pearson(k, n, alpha=0.05):
    """IC exacto al (1-alpha) para una proporcion binomial k/n."""
    lo = 0.0 if k == 0 else _beta_ppf(alpha / 2.0, k, n - k + 1)
    hi = 1.0 if k == n else _beta_ppf(1.0 - alpha / 2.0, k + 1, n - k)
    return lo, hi


# --------------------------------------------------------------------------
# Datos
# --------------------------------------------------------------------------

COMUNIDADES = [
    # nombre, TP censado, N0 (no relevante), n0 (sorteadas), k (amenazas en la muestra)
    ("r/devsarg", 3, 421, 135, 2),
    ("r/netsec", 60, 84, 29, 15),
    ("r/Malware", 81, 49, 18, 13),
]


def estimar(tp, N0, n0, k):
    peso = N0 / n0
    omisiones = k * peso
    sens = tp / (tp + omisiones)
    p_lo, p_hi = clopper_pearson(k, n0)
    ic_lo = tp / (tp + N0 * p_hi)   # limite inferior: p maxima
    ic_hi = tp / (tp + N0 * p_lo)   # limite superior: p minima
    return {
        "peso": peso, "omisiones": omisiones, "p": k / n0,
        "sens": sens, "ic": (ic_lo, ic_hi), "ic_p": (p_lo, p_hi),
    }


def main():
    print("Validacion del metodo contra las cifras publicadas (resultados_v5.json)")
    lo, hi = clopper_pearson(30, 182)
    print("  omision 30/182        CP95 = [%.4f, %.4f]   publicado [0.1141, 0.2269]" % (lo, hi))
    a, b = clopper_pearson(144, 170)
    print("  precision 144/170     CP95 = [%.4f, %.4f]   publicado [0.7840, 0.8976]" % (a, b))
    w = 554 / 182
    print("  sensibilidad agregada (w uniforme 3,044) = %.4f [%.4f, %.4f]  publicado 0.6119 [0.5339, 0.6950]"
          % (144 / (144 + 554 * (30 / 182)), 144 / (144 + 554 * hi), 144 / (144 + 554 * lo)))
    print()

    print("Postestratificacion por comunidad")
    total_om = 0.0
    for nombre, tp, N0, n0, k in COMUNIDADES:
        r = estimar(tp, N0, n0, k)
        total_om += r["omisiones"]
        print("  %-11s TP=%3d N0=%3d n0=%3d k=%2d  peso=%.4f  omisiones_est=%6.2f  sens=%.4f  IC95=[%.4f, %.4f]"
              % (nombre, tp, N0, n0, k, r["peso"], r["omisiones"], r["sens"], r["ic"][0], r["ic"][1]))

    tp_en = 60 + 81
    N0_en = 84 + 49
    n0_en = 29 + 18
    k_en = 15 + 13
    r_en = estimar(tp_en, N0_en, n0_en, k_en)
    om_en_suma = estimar(60, 84, 29, 15)["omisiones"] + estimar(81, 49, 18, 13)["omisiones"]
    print("  %-11s TP=%3d N0=%3d n0=%3d k=%2d  peso=%.4f  omisiones_est=%6.2f (%6.2f por peso unico)"
          "  sens=%.4f  IC95=[%.4f, %.4f]"
          % ("INGLES", tp_en, N0_en, n0_en, k_en, r_en["peso"], om_en_suma, r_en["omisiones"],
             r_en["sens"], r_en["ic"][0], r_en["ic"][1]))

    print()
    print("Agregado")
    print("  postestratificado (suma de omisiones por comunidad): omisiones=%.2f  sens=%.4f  amenazas_est=%.1f"
          % (total_om, 144 / (144 + total_om), 144 + total_om))
    print("  uniforme (Tabla 5.8, w = 554/182):                 omisiones=%.2f  sens=%.4f  amenazas_est=%.1f"
          % (30 * w, 144 / (144 + 30 * w), 144 + 30 * w))
    print("  No se informa IC para el total postestratificado: es una suma de tres estimadores")
    print("  independientes, no una proporcion binomial unica. El IC del estimador uniforme es el de 5.8.")


if __name__ == "__main__":
    main()
