"""Tests basicos para las consultas del prototipo.

Ejecutar con: pytest tests/ -v
Requiere que el contenedor tfi-postgres este arriba y accesible.
"""

import pytest

import queries


def test_resumen():
    r = queries.resumen()
    assert isinstance(r, list)
    assert len(r) == 1
    assert r[0]["total_posts"] > 0
    assert r[0]["con_senal"] >= 0
    assert r[0]["sin_senal"] >= 0
    assert r[0]["total_posts"] == r[0]["con_senal"] + r[0]["sin_senal"]


def test_por_comunidad():
    r = queries.por_comunidad()
    assert isinstance(r, list)
    assert len(r) == 3
    nombres = {row["display_name"] for row in r}
    assert "r/devsarg" in nombres
    assert "r/netsec" in nombres
    assert "r/Malware" in nombres


def test_comunidades_con_estado():
    r = queries.comunidades_con_estado()
    assert isinstance(r, list)
    assert len(r) >= 3
    # Al menos una comunidad activa
    assert any(row["active_monitoring"] for row in r)


def test_por_categoria():
    r = queries.por_categoria()
    assert isinstance(r, list)
    assert len(r) >= 9  # 9 categorias + No relevante
    categorias = {row["categoria"] for row in r}
    assert "No relevante" in categorias


def test_serie_diaria():
    r = queries.serie_diaria()
    assert isinstance(r, list)
    assert len(r) >= 1
    for row in r:
        assert "dia" in row
        assert "total" in row
        assert row["total"] > 0


def test_anomalias():
    r = queries.anomalias()
    assert isinstance(r, list)
    # Puede estar vacio si no hay evaluaciones
    if r:
        assert "id" in r[0]
        assert "categoria" in r[0]
        assert "disparo" in r[0]


def test_alertas():
    r = queries.alertas()
    assert isinstance(r, list)
    if r:
        assert "id" in r[0]
        assert "categoria" in r[0]
        assert "estado" in r[0]
        assert r[0]["estado"] in ("PENDIENTE", "ENVIADO")


def test_entidades_valido():
    r = queries.entidades("products")
    assert isinstance(r, list)
    if r:
        assert "entidad" in r[0]
        assert "menciones" in r[0]


def test_entidades_invalido():
    with pytest.raises(ValueError):
        queries.entidades("invalido")


def test_distribucion_score():
    r = queries.distribucion_score()
    assert isinstance(r, list)
    assert len(r) >= 1
    tramos = {row["tramo"] for row in r}
    assert "0.00" in tramos


def test_suficiencia():
    r = queries.suficiencia()
    assert isinstance(r, list)
    assert len(r) == 1
    assert "dias_completos" in r[0]
    assert "estado" in r[0]
    assert r[0]["estado"] in ("abierta", "minimo_alcanzado", "objetivo_alcanzado")


def test_ultimos_posts_limite():
    r = queries.ultimos_posts(5)
    assert isinstance(r, list)
    assert len(r) <= 5
    if r:
        assert "id" in r[0]
        assert "title" in r[0]


def test_ultimos_posts_max():
    r = queries.ultimos_posts(1000)
    assert isinstance(r, list)
    assert len(r) <= 1000  # la query respeta el limite, la app lo capea a 100


def test_regimen_operacion():
    r = queries.regimen_operacion()
    assert isinstance(r, list)
    assert len(r) >= 1
    assert "fecha" in r[0]
    assert "publicaciones" in r[0]


def test_latencia_por_estado():
    r = queries.latencia_por_estado()
    assert isinstance(r, list)
    assert len(r) >= 1
    grupos = {row["grupo"] for row in r}
    assert "en_ventana" in grupos
