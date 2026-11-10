"""Conexion a la base. SOLO LECTURA.

La garantia de que este prototipo no puede alterar la evidencia no depende
de que el codigo se porte bien: depende del rol. `tfi_lectura` tiene
`SELECT` y nada mas, asi que un `INSERT` escrito por error falla en la base,
no en el codigo.
"""

from config import cargar_config, obtener_zona

import psycopg2
import psycopg2.extras

ZONA = obtener_zona()


def conectar():
    cfg = cargar_config()
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
