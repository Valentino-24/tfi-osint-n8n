"""Evaluacion reproducible de la muestra de control, INDEPENDIENTE de la base de datos.

Por que existe: la tabla `posts` se trunca al iniciar la ventana B5. El CSV de
etiquetas trunca el `cuerpo` de 26 de los 50 posts, asi que no alcanza para
reproducir. Este script usa `muestra_control_50_2026-09-30_TEXTO_EXACTO.jsonl`, que
guarda el `selftext` tal como quedo almacenado.

No reimplementa el clasificador: ejecuta el Code node real de
`V4/anexos/B_workflow.json` en Node. Reimplementarlo en Python fue justamente lo que
produjo la cifra optimista de F1 0,931 cuando el real es 0,900.

Uso:
    python V4/scripts/evaluar_muestra_reproducible.py

Requiere `node` en el PATH. No toca la base de datos.
"""
import csv, io, json, os, subprocess, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EV = os.path.join(REPO, "V4", "evidencias")
JSONL = os.path.join(EV, "muestra_control_50_2026-09-30_TEXTO_EXACTO.jsonl")
WF = os.path.join(REPO, "V4", "anexos", "B_workflow.json")

AMENAZA = {"Phishing", "Robo de Credenciales", "Malware", "Ransomware",
           "Vulnerabilidades", "Filtración de Datos", "Infraestructura y Ataques",
           "Hacktivismo", "Ingenieria Social"}

RUNNER = r"""
const fs = require('fs');
const W = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const N = {}; for (const n of W.nodes) N[n.name] = n;
const filas = fs.readFileSync(process.argv[3], 'utf8').trim().split('\n').map(JSON.parse);
const items = filas.map(f => ({ json: { title: f.titulo, selftext: f.selftext } }));
const out = new Function('$input', N['Classify Dictionary'].parameters.jsCode)({ all: () => items });
console.log(JSON.stringify(out.map(o => ({ c: o.json.nlp_category, s: o.json.nlp_score }))));
"""


def clasificar():
    """Ejecuta el Code node real sobre el JSONL y devuelve [(categoria, score), ...]."""
    tmpdir = tempfile.mkdtemp()
    runner = os.path.join(tmpdir, "runner.js")
    with io.open(runner, "w", encoding="utf-8", newline="\n") as f:
        f.write(RUNNER)
    proc = subprocess.run(
        ["node", runner, WF, JSONL],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit("fallo la ejecucion del Code node real")
    return json.loads(proc.stdout.strip())


def main():
    if not os.path.exists(JSONL):
        raise SystemExit(f"falta {JSONL}")

    filas = [json.loads(l) for l in io.open(JSONL, encoding="utf-8") if l.strip()]
    print("muestra de control, evaluada con el Code node real del workflow")
    print("fuente: " + os.path.relpath(JSONL, REPO))
    print(f"posts: {len(filas)}\n")

    pred = clasificar()
    if len(pred) != len(filas):
        raise SystemExit("la cantidad de predicciones no coincide con la muestra")

    tp = fp = fn = tn = 0
    exactas = 0
    fp_list, fn_list, cat_list = [], [], []
    for f, p in zip(filas, pred):
        h = f["categoria_humana"].strip()
        cat, score = p["c"], p["s"]
        if h == cat:
            exactas += 1
        if h in AMENAZA and cat not in AMENAZA:
            fn += 1
            fn_list.append((f, cat, score))
        elif h not in AMENAZA and cat in AMENAZA:
            fp += 1
            fp_list.append((f, cat, score))
        elif h != cat:
            cat_list.append((f, cat, score))
        if h in AMENAZA and cat in AMENAZA:
            tp += 1
        elif h not in AMENAZA and cat not in AMENAZA:
            tn += 1

    total = len(filas)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0

    print("=" * 62)
    print("MATRIZ DE CONFUSION")
    print("=" * 62)
    print(f"  TP {tp:>3}   FP {fp:>3}   FN {fn:>3}   TN {tn:>3}   (total {tp+fp+fn+tn})")
    print(f"  precision {prec:.3f}   recall {rec:.3f}   F1 {f1:.3f}")
    print(f"  acierto exacto de categoria {exactas}/{total} = {100*exactas/total:.1f} %")

    print()
    print("=" * 62)
    print(f"FALSOS NEGATIVOS ({len(fn_list)}) -- amenaza real, 'No relevante'")
    print("=" * 62)
    for f, cat, s in fn_list:
        print(f"  [{f['subreddit']}] {f['titulo'][:60]}")
        print(f"      humano={f['categoria_humana']}  modelo={cat}  score={s}")

    print()
    print("=" * 62)
    print(f"FALSOS POSITIVOS ({len(fp_list)}) -- no amenaza, el modelo dice amenaza")
    print("=" * 62)
    for f, cat, s in fp_list:
        print(f"  [{f['subreddit']}] {f['titulo'][:60]}")
        print(f"      humano={f['categoria_humana']}  modelo={cat}  score={s}")

    print()
    print("=" * 62)
    print(f"ACIERTOS CON CATEGORIA DISTINTA ({len(cat_list)}) -- ni FP ni FN")
    print("=" * 62)
    for f, cat, s in cat_list:
        print(f"  [{f['subreddit']}] humano={f['categoria_humana']:<26} modelo={cat:<20} score={s}")


if __name__ == "__main__":
    main()
