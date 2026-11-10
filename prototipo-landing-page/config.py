"""Configuracion centralizada del prototipo.

Lee la configuracion de .env y variables de entorno.
Unica fuente de verdad para host, puerto, base, usuario y password.
"""

import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
ZONA = "America/Argentina/Buenos_Aires"

_DEFAULTS = {
    "TFI_DB_HOST": "localhost",
    "TFI_DB_PORT": "5433",
    "TFI_DB_NAME": "tesi_osint",
    "TFI_DB_USER": "tfi_lectura",
}


def cargar_config() -> dict:
    """Lee .env y variables de entorno. Las env vars ganan sobre .env."""
    env = dict(_DEFAULTS)
    archivo = BASE / ".env"
    if archivo.exists():
        for linea in archivo.read_text(encoding="utf-8-sig").splitlines():
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            clave, valor = linea.split("=", 1)
            env[clave.strip()] = valor.strip()
    for clave in list(env) + ["TFI_DB_PASSWORD"]:
        if os.environ.get(clave):
            env[clave] = os.environ[clave]
    if not env.get("TFI_DB_PASSWORD"):
        raise RuntimeError(
            "Falta TFI_DB_PASSWORD. Copia .env.example a .env y completalo, "
            "o exporta la variable antes de arrancar."
        )
    return env


def obtener_zona() -> str:
    return ZONA
