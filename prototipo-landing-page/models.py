"""Modelos Pydantic para las respuestas de la API.

Definen el schema de cada endpoint para que FastAPI genere
documentacion automatica y valide las respuestas.
"""

from datetime import date
from datetime import date, time
from pydantic import BaseModel


class Resumen(BaseModel):
    total_posts: int
    con_senal: int
    sin_senal: int
    comunidades: int
    dias_recoleccion: int
    desde: date
    hasta: date
    ultima_carga: date
    publicado_desde: date
    publicado_hasta: date


class Comunidad(BaseModel):
    display_name: str
    total: int
    con_senal: int
    pct_senal: float | None = None


class ComunidadEstado(BaseModel):
    display_name: str
    active_monitoring: bool
    total: int
    con_senal: int
    pct_senal: float | None = None


class Categoria(BaseModel):
    categoria: str
    total: int
    score_promedio: float | None = None


class SerieDiaria(BaseModel):
    dia: date
    total: int
    con_senal: int


class Anomalia(BaseModel):
    id: int
    dia: date
    categoria: str
    n_observado: int
    base_media: float
    umbral: float
    disparo: bool
    genero_alerta: bool


class Entidad(BaseModel):
    entidad: str
    menciones: int


class DistribucionScore(BaseModel):
    tramo: str
    desde: float | None = None
    hasta: float | None = None
    total: int


class UltimoPost(BaseModel):
    id: str
    display_name: str
    title: str
    nlp_category: str | None = None
    nlp_score: float | None = None
    publicado: date
    ingests: time
    url: str


class Suficiencia(BaseModel):
    dias_completos: int
    primer_dia: date | None = None
    ultimo_dia: date | None = None
    disparos: int
    minimo: int
    objetivo: int
    estado: str


class Alerta(BaseModel):
    id: int
    fecha: date
    categoria: str
    n_observado: int
    umbral: float
    estado: str
    canal: str


class Latencia(BaseModel):
    grupo: str
    n: int
    p50_min: float | None = None
    p95_min: float | None = None
    max_min: float | None = None


class RegimenDia(BaseModel):
    fecha: date
    publicaciones: int
    primera_ingesta: time | None = None
    ultima_ingesta: time | None = None
