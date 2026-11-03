"""API de lectura para el panel.

Regla unica: este servicio no escribe nada. No expone POST, ni PUT, ni DELETE.
No importa a n8n, no genera artefactos, no toca la ventana de recoleccion.
Solo lee lo que la ingesta ya escribio.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse

import queries

app = FastAPI(
    title="Panel OSINT - prototipo",
    description=(
        "Capa de lectura sobre tesi_osint. No escribe, no altera la evidencia "
        "y no interviene en la recoleccion de la ventana B5."
    ),
    version="0.1.0",
)


@app.get("/api/resumen")
def api_resumen():
    return queries.resumen()[0]


@app.get("/api/por-comunidad")
def api_comunidad():
    return queries.por_comunidad()


@app.get("/api/por-categoria")
def api_categoria():
    return queries.por_categoria()


@app.get("/api/comunidades-estado")
def api_comunidades_estado():
    return queries.comunidades_con_estado()


@app.get("/api/serie-diaria")
def api_serie():
    return queries.serie_diaria()


@app.get("/api/anomalias")
def api_anomalias():
    return queries.anomalias()


@app.get("/api/entidades/{tipo}")
def api_entidades(tipo: str):
    try:
        return queries.entidades(tipo)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/api/distribucion-score")
def api_score():
    return queries.distribucion_score()


@app.get("/api/suficiencia")
def api_suficiencia():
    """Dias completos evaluados y estado de la ventana B5 (minimo 10 / objetivo 15)."""
    return queries.suficiencia()[0]


@app.get("/api/ultimos-posts")
def api_ultimos(limite: int = 15):
    return queries.ultimos_posts(min(max(limite, 1), 100))


@app.get("/api/salud")
def api_salud():
    """Comprueba que la base responde. Sirve para descartar el panel como causa."""
    try:
        return {"ok": True, "posts": queries.resumen()[0]["total_posts"]}
    except Exception as exc:  # pragma: no cover - diagnostico
        return JSONResponse(status_code=503, content={"ok": False, "error": str(exc)})


@app.get("/")
def panel():
    return FileResponse("static/index.html")


@app.get("/v2")
def panel_v2():
    """Landing v2: convive con la v1 en / . No toca lo que usa la v1."""
    return FileResponse("static/v2/index.html")


@app.get("/v3")
def panel_v3():
    """Landing v3: el diseno nuevo, con los mismos endpoints de lectura.

    Convive con / y /v2. Igual que ellas, solo lee: los numeros salen de
    /api/* en el navegador, asi que la pagina nunca muestra datos viejos.
    """
    return FileResponse("static/v3/index.html")
