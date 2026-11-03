"""Conexion a la base. SOLO LECTURA.

La garantia de que este prototipo no puede alterar la evidencia no depende
de que el codigo se porte bien: depende del rol. `tfi_lectura` tiene
`SELECT` y nada mas, asi que un `INSERT` escrito por error falla en la base,
no en el codigo.

Se lee la configuracion de un `.env` en esta misma carpeta. Ese archivo esta
en `.gitignore` y no se versiona: aca hay una contrasena real.
"""

import os
from pathlib import Path

import psycopg2
import psycopg2.extras

BASE = Path(__file__).resolve().parent
ZONA = "America/Argentina/Buenos_Aires"

_DEFAULTS = {
    "TFI_DB_HOST": "localhost",
    "TFI_DB_PORT": "5433",
    "TFI_DB_NAME": "tesi_osint",
    "TFI_DB_USER": "tfi_lectura",
}


def _config() -> dict:
    env = dict(_DEFAULTS)
    archivo = BASE / ".env"
    if archivo.exists():
        for linea in archivo.read_text(encoding="utf-8-sig").splitlines():
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            clave, valor = linea.split("=", 1)
            env[clave.strip()] = valor.strip()
    # una variable de entorno real gana sobre el .env
    for clave in list(env) + ["TFI_DB_PASSWORD"]:
        if os.environ.get(clave):
            env[clave] = os.environ[clave]
    if not env.get("TFI_DB_PASSWORD"):
        raise RuntimeError(
            "Falta TFI_DB_PASSWORD. Copia .env.example a .env y completalo, "
            "o exporta la variable antes de arrancar."
        )
    return env


def conectar():
    cfg = _config()
    return psycopg2.connect(
        host=cfg["TFI_DB_HOST"],
        port=int(cfg["TFI_DB_PORT"]),
        dbname=cfg["TFI_DB_NAME"],
        user=cfg["TFI_DB_USER"],
        password=cfg["TFI_DB_PASSWORD"],
        connect_timeout=5,
    )


def consultar(sql: str, params: tuple = ()) -> list[dict]:
    """Ejecuta un SELECT y devuelve filas como diccionarios.

    Abre y cierra una conexion por consulta. Es lo mas simple y para un
    prototipo que se usa a mano no vale la pena un pool.
    """
    with conectar() as cn:
        with cn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return [dict(f) for f in cur.fetchall()]
