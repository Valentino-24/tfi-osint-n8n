"""API de lectura para el panel.

Regla unica: este servicio no escribe nada. No expone POST, ni PUT, ni DELETE.
No importa a n8n, no genera artefactos, no toca la ventana de recoleccion.
Solo lee lo que la ingesta ya escribio.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import queries
from models import (
    Alerta,
    Anomalia,
    Categoria,
    Latencia,
    Comunidad,
    ComunidadEstado,
    DistribucionScore,
    Entidad,
    RegimenDia,
    Resumen,
    SerieDiaria,
    Suficiencia,
    UltimoPost,
)

app = FastAPI(
    title="Panel OSINT - prototipo",
    description=(
        "Capa de lectura sobre tesi_osint. No escribe, no altera la evidencia "
        "y no interviene en la recoleccion de la ventana B5."
    ),
    version="0.2.0",
)


# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/api/resumen", response_model=Resumen)
def api_resumen():
    return queries.resumen()[0]


@app.get("/api/por-comunidad", response_model=list[Comunidad])
def api_comunidad():
    return queries.por_comunidad()


@app.get("/api/por-categoria", response_model=list[Categoria])
def api_categoria():
    return queries.por_categoria()


@app.get("/api/comunidades-estado", response_model=list[ComunidadEstado])
def api_comunidades_estado():
    return queries.comunidades_con_estado()


@app.get("/api/serie-diaria", response_model=list[SerieDiaria])
def api_serie(categoria: str | None = None):
    return queries.serie_diaria(categoria)


@app.get("/api/anomalias", response_model=list[Anomalia])
def api_anomalias():
    return queries.anomalias()


@app.get("/api/alertas", response_model=list[Alerta])
def api_alertas():
    return queries.alertas()


@app.get("/api/regimen", response_model=list[RegimenDia])
def api_regimen():
    return queries.regimen_operacion()


@app.get("/api/latencia", response_model=list[Latencia])
def api_latencia():
    return queries.latencia_por_estado()


@app.get("/api/entidades/{tipo}", response_model=list[Entidad])
def api_entidades(tipo: str):
    try:
        return queries.entidades(tipo)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/api/distribucion-score", response_model=list[DistribucionScore])
def api_score():
    return queries.distribucion_score()


@app.get("/api/suficiencia", response_model=Suficiencia)
def api_suficiencia():
    """Dias completos evaluados y estado de la ventana B5 (minimo 10 / objetivo 15)."""
    return queries.suficiencia()[0]


@app.get("/api/ultimos-posts", response_model=list[UltimoPost])
def api_ultimos(limite: int = 15, categoria: str | None = None,
                desde: str | None = None, hasta: str | None = None):
    return queries.ultimos_posts(min(max(limite, 1), 100), categoria, desde, hasta)


@app.get("/api/export/csv")
def api_export_csv(categoria: str | None = None, limite: int = 100):
    """Exporta posts como CSV. Solo lectura."""
    from fastapi.responses import StreamingResponse
    import csv, io
    rows = queries.ultimos_posts(min(max(limite, 1), 1000), categoria)
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "comunidad", "titulo", "categoria", "score", "publicado", "url"])
    for r in rows:
        writer.writerow([r["id"], r["display_name"], r["title"], r["nlp_category"],
                        r["nlp_score"], r["publicado"], r["url"]])
    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=posts_export.csv"},
    )


@app.get("/api/salud")
def api_salud():
    """Comprueba que la base responde. Sirve para descartar el panel como causa."""
    try:
        return {"ok": True, "posts": queries.resumen()[0]["total_posts"]}
    except Exception as exc:  # pragma: no cover - diagnostico
        return JSONResponse(status_code=503, content={"ok": False, "error": str(exc)})


@app.get("/")
def panel():
    return FileResponse("static/v1/index.html")


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


@app.get("/v4")
def panel_v4():
    """Landing v4: incluye alertas Telegram y regimen de operacion.

    Convive con /, /v2 y /v3. Agrega secciones de alertas y regimen.
    """
    return FileResponse("static/v4/index.html")
