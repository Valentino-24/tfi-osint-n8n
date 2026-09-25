# -*- coding: utf-8 -*-
r"""
Bitácora diaria de la ventana de recolección B5 (C-05) — TFI OSINT/n8n V4
=======================================================================

Genera `V4/evidencias/bitacora_b5/YYYY-MM-DD.md`: una entrada por día de la
ventana B5 con el total de posts ingeridos, el desglose por los TRES
subreddits monitorizados (incluidos los que aportan 0) y el conteo consultable
de `días_completos_evaluados` derivado de `anomalias`.

Garantías del script (D-3, spec `bitacora-evidencia-diaria`)
------------------------------------------------------------
* Toma la fecha como parámetro (`--fecha YYYY-MM-DD`).
* Ejecuta ÚNICAMENTE consultas `SELECT` agregadas contra `tesi_osint`.
  No emite ninguna sentencia de escritura ni de definición de esquema; cada
  sentencia se valida en tiempo de ejecución y el script aborta si alguna no
  arranca con la palabra `SELECT` o si trae más de una sentencia.
* Es idempotente: no modifica datos ni esquema. Reejecutarlo regenera la misma
  entrada a partir del mismo estado de la base.
* Si falla la conexión (o cualquier consulta) termina con error explícito y
  NO escribe una entrada parcial: el archivo se arma en memoria y solo se
  escribe al final, de forma atómica.
* Toda cifra sale de una consulta `SELECT` sobre `tesi_osint`; nunca de V2/V3
  ni de tasas supuestas (RN-GL-01).
* Credenciales: se leen del entorno estándar de PostgreSQL
  (`PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` o
  `TESI_PG_PASSWORD`). No hay contraseña en el código. El rol debe venir del
  entorno (`PGUSER` / `TESI_PG_USER`): si falta, el script aborta con un
  mensaje explícito en vez de dejar que el sistema operativo imponga un rol.

Uso
---
    $env:PGUSER   = "<rol de la base>"      # p. ej. el rol local de la guía
    $env:PGPASSWORD = "<clave del rol local>"  # o definirla por otro medio
    python V4\scripts\bitacora_b5.py --fecha 2026-09-25

    # con el estado de n8n observado por el operador (fuera de la base):
    python V4\scripts\bitacora_b5.py --fecha 2026-09-25 `
        --n8n-estado instancia_arriba_workflow_publicado `
        --n8n-detalle "<descripción literal de lo observado>"

Estado de ejecución de n8n: lo DECLARA el operador, no lo deduce el script
--------------------------------------------------------------------------
La base `tesi_osint` no persiste el estado de la instancia n8n ni su log de
ejecuciones, y este script **no** lee la base de n8n ni su API. Por eso el
estado se toma de un parámetro explícito:

* `--n8n-estado`   conjunto cerrado de valores (ver `ESTADOS_N8N`). El valor por
  defecto es `no_observado`: "no observado en la generación de esta entrada".
  El script **jamás** infiere, comprueba ni asume un estado exitoso.
* `--n8n-detalle`  texto libre con la observación literal del operador. Es
  obligatorio declarar `--n8n-estado` cuando se lo usa; sin estado, el detalle
  no se acepta.

Ambos valores se escriben en la entrada **como declaración del operador**, con
ese origen explícito, para que nadie los lea como un dato que el script midió.

Códigos de salida
-----------------
    0  entrada escrita
    2  error de conexión a la base (no se escribe entrada)
    3  error al ejecutar una consulta (no se escribe entrada)
    4  argumentos inválidos
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date, datetime, timedelta

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python < 3.9
    ZoneInfo = None

# --------------------------------------------------------------------- config
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../V4
DIR_EVIDENCIAS = os.path.join(RAIZ, "evidencias")
DIR_BITACORA = os.path.join(DIR_EVIDENCIAS, "bitacora_b5")

VENTANA_ID = "B5"
VENTANA_INICIO = "2026-09-25"          # D-1: inicio inmutable de la ventana
VENTANA_CORTE_ESTADO = "no fijada"     # D-7: decisión abierta de los autores
VENTANA_CORTE_TAREA = "6.1"            # tarea del change que la cierra

SUBSIDIOS_ESPERADOS = 3                # RN-GL-02: denominador completo
SUBSIDIOS_MONITORIZADOS = ["r/argentina", "r/derechogenial", "r/devsarg"]

DIAS_SUFICIENTES = 10                  # D-6: base comparativa de RN-AN-02

# Zona horaria de la ejecución del sistema. Los límites del día se calculan en
# esta zona y se escriben ya resueltos en el SQL, para que la consulta que figura
# en la cabecera sea literalmente reproducible.
TZ_SISTEMA = os.environ.get("TESI_TZ", "America/Argentina/Buenos_Aires")
TZ_ARGENTINA_FIJA = timedelta(hours=-3)  # Argentina sin horario de verano desde 2009

# Estados de n8n que el operador PUEDE declarar. Conjunto cerrado: el script no
# acepta texto libre acá porque no puede verificarlo — no lee la instancia.
# `no_observado` es el valor por defecto y significa literalmente "no observado
# en la generación de esta entrada", nunca "exitoso" (RN-GL-01, D-3).
ESTADOS_N8N = {
    "no_observado": "no observado en la generación de esta entrada",
    "instancia_caida": "declarado por el operador: instancia n8n caída (sin respuesta en su puerto)",
    "instancia_arriba_workflow_inactivo":
        "declarado por el operador: instancia n8n arriba y workflow NO publicado",
    "instancia_arriba_workflow_publicado":
        "declarado por el operador: instancia n8n arriba y workflow publicado (activo)",
}
ESTADO_N8N_POR_DEFECTO = "no_observado"


# ------------------------------------------------------------------- helpers
def zona():
    """Devuelve la zona horaria de la ejecución; respaldo de desplazamiento fijo."""
    if ZoneInfo is not None:
        try:
            return ZoneInfo(TZ_SISTEMA)
        except Exception:
            pass
    return TZ_ARGENTINA_FIJA


def limites_del_dia(fecha: date, tz):
    """(inicio, fin) del día local, como timestamptz resueltos."""
    inicio = datetime(fecha.year, fecha.month, fecha.day, 0, 0, 0, tzinfo=tz)
    fin = datetime(fecha.year, fecha.month, fecha.day, 0, 0, 0, tzinfo=tz) + timedelta(days=1)
    return inicio, fin


def iso(dt: datetime) -> str:
    return dt.isoformat()


def ts_literal(dt: datetime) -> str:
    """timestamptZ en ISO-8601, apta para incrustar en el SQL de la evidencia."""
    return dt.isoformat()


def texto_declarado(valor: str) -> str:
    """Texto del operador, seguro para una celda de tabla Markdown."""
    plano = " ".join(str(valor).split())  # colapsa saltos de línea y espacios
    return plano.replace("|", "\\|")


def parametros_conexion() -> dict:
    """Ajustes de conexión desde el entorno estándar. Sin claves en el código."""
    usuario = os.environ.get("TESI_PG_USER") or os.environ.get("PGUSER")
    clave = os.environ.get("TESI_PG_PASSWORD") or os.environ.get("PGPASSWORD")
    if not usuario:
        raise RuntimeError(
            "falta el rol de la base: definí PGUSER (o TESI_PG_USER) antes de correr el script. "
            "No se escribe ninguna entrada.")
    cfg = {
        "host": os.environ.get("PGHOST", "localhost"),
        "port": int(os.environ.get("PGPORT", "5433")),
        "dbname": os.environ.get("PGDATABASE", "tesi_osint"),
        "user": usuario,
    }
    if clave:
        cfg["password"] = clave
    return cfg


def solo_lectura(sql: str) -> str:
    """Valida que la sentencia sea un único SELECT. Aborta si no lo es."""
    limpio = sql.strip().rstrip(";").strip()
    if not limpio.upper().startswith("SELECT"):
        raise ValueError("sentencia no permitida: solo se admiten consultas SELECT")
    if ";" in limpio:
        raise ValueError("sentencia no permitida: solo se admite una sentencia por consulta")
    return limpio


def ejecutar(cur, sql: str):
    sentencia = solo_lectura(sql)
    cur.execute(sentencia)
    return cur.fetchall()


# ------------------------------------------------------------------- queries
def sql_total_dia(inicio: datetime, fin: datetime) -> str:
    return (
        "SELECT COUNT(*) AS total_posts\n"
        "FROM posts\n"
        f"WHERE ingested_at >= TIMESTAMPTZ '{ts_literal(inicio)}'\n"
        f"  AND ingested_at <  TIMESTAMPTZ '{ts_literal(fin)}';"
    )


def sql_distribucion(inicio: datetime, fin: datetime) -> str:
    # LEFT JOIN desde subreddits: el cero del subreddit sin posts NO se pierde.
    return (
        "SELECT s.display_name,\n"
        "       s.active_monitoring,\n"
        "       COUNT(p.id) AS n\n"
        "FROM subreddits s\n"
        "LEFT JOIN posts p\n"
        "       ON p.subreddit_id = s.id\n"
        f"      AND p.ingested_at >= TIMESTAMPTZ '{ts_literal(inicio)}'\n"
        f"      AND p.ingested_at <  TIMESTAMPTZ '{ts_literal(fin)}'\n"
        "GROUP BY s.display_name, s.active_monitoring\n"
        "ORDER BY s.display_name;"
    )


def sql_acumulado_ventana(inicio_ventana: datetime, corte_efectivo: datetime) -> str:
    return (
        "SELECT COUNT(*) AS total_posts_ventana\n"
        "FROM posts\n"
        f"WHERE ingested_at >= TIMESTAMPTZ '{ts_literal(inicio_ventana)}'\n"
        f"  AND ingested_at <  TIMESTAMPTZ '{ts_literal(corte_efectivo)}';"
    )


def sql_dias_evaluados(inicio_ventana: datetime, corte_efectivo: datetime) -> str:
    return (
        "SELECT (ventana_fin AT TIME ZONE 'America/Argentina/Buenos_Aires')::date AS dia,\n"
        "       COUNT(*) AS n_evaluaciones\n"
        "FROM anomalias\n"
        f"WHERE ventana_fin >= TIMESTAMPTZ '{ts_literal(inicio_ventana)}'\n"
        f"  AND ventana_fin <  TIMESTAMPTZ '{ts_literal(corte_efectivo)}'\n"
        "GROUP BY (ventana_fin AT TIME ZONE 'America/Argentina/Buenos_Aires')::date\n"
        "ORDER BY dia;"
    )


def sql_subreddits_monitorizados() -> str:
    return (
        "SELECT id, display_name, active_monitoring\n"
        "FROM subreddits\n"
        "ORDER BY display_name;"
    )


# ------------------------------------------------------------------ render
def bloque_sql(sql: str, resultado) -> str:
    filas = "\n".join("    " + " | ".join("NULL" if v is None else str(v) for v in f) for f in resultado)
    return f"```sql\n{sql}\n```\n\nResultado (filas devueltas):\n\n```\n{filas if filas else '    (sin filas)'}\n```\n"


def render_entrada(fecha, tz, ejecucion, inicio, fin, inicio_ventana, corte_efectivo,
                   q_total, r_total, q_dist, r_dist, q_acum, r_acum,
                   q_dias, r_dias, q_subs, r_subs,
                   estado_n8n=ESTADO_N8N_POR_DEFECTO, detalle_n8n=None) -> str:
    total_dia = int(r_total[0][0]) or 0
    acumulado = int(r_acum[0][0]) or 0
    filas_dist = [(f[0], f[1], int(f[2]) or 0) for f in r_dist]
    denominador = sum(n for _, _, n in filas_dist)
    dias_completos = len(r_dias)

    monitorizados = [f[1] for f in r_subs if f[2] is True]
    subs_faltantes = sorted(set(SUBSIDIOS_MONITORIZADOS) - {f[1] for f in r_subs})

    # El día solo está "cerrado" si la generación ocurre en/después de su fin local.
    # Mientras no lo esté, el `n` del día es un corte parcial: se dice explícito.
    dia_cerrado = ejecucion >= fin
    estado_txt = ESTADOS_N8N[estado_n8n]
    observado = estado_n8n != ESTADO_N8N_POR_DEFECTO
    detalle_txt = texto_declarado(detalle_n8n) if detalle_n8n else ""

    L = []
    A = L.append
    A(f"# Bitácora B5 — {fecha.isoformat()}\n")
    A(f"> Entrada generada por `V4/scripts/bitacora_b5.py`. Conteo operativo de la ventana, "
      f"no métrica de resultados (RN-GL-01).\n")

    A("## Cabecera (RN-GL-01: consulta, fecha, ventana y `n`)\n")
    A("| Campo | Valor |")
    A("|---|---|")
    A(f"| Fecha de la entrada | `{fecha.isoformat()}` |")
    A(f"| Identificador de la ventana | `{VENTANA_ID}` |")
    A(f"| Ventana | inicio `{VENTANA_INICIO}`, corte `{VENTANA_CORTE_ESTADO}` "
      f"(decisión abierta de los autores; la cierra la tarea {VENTANA_CORTE_TAREA}) |")
    A(f"| Fecha y hora de ejecución | `{iso(ejecucion)}` |")
    A(f"| Zona horaria de los límites | `{TZ_SISTEMA}` |")
    A(f"| Límite inferior del día | `{iso(inicio)}` |")
    A(f"| Límite superior del día (excluido) | `{iso(fin)}` |")
    A(f"| `n` de la observación | **{total_dia}** posts ingeridos en el día |")
    A(f"| Naturaleza del `n` | **{'día cerrado' if dia_cerrado else 'corte a mitad de día (snapshot)'}**"
      + ("" if dia_cerrado else
         f" — el día `{fecha.isoformat()}` todavía no termina en el momento de esta ejecución "
         f"(`{iso(ejecucion)}` < `{iso(fin)}`); este `n` NO es el total del día y va a crecer") + " |")
    A(f"| Denominador de cobertura | **{len(filas_dist)}** subreddit(s) monitorizado(s) "
      f"(se incluyen los que aportan 0) |")
    A("| Origen del dato | consultas `SELECT` sobre `tesi_osint` |")
    A(f"| Límite superior aplicado a la ventana | corte `no fijada` → se usa el instante de "
      "ejecución de la consulta |")
    A("")

    A("## 1. Total de posts ingeridos en el día\n")
    A(f"Criterio del corpus de la ventana: `posts.ingested_at` (D-1). "
      f"Rango del día `ingested_at >= {iso(inicio)}` y `ingested_at < {iso(fin)}`.\n")
    if not dia_cerrado:
        A(f"> **El `n = {total_dia}` de esta sección es un corte a mitad de día, no un total de "
          f"día cerrado.** Cuando se generó esta entrada el día `{fecha.isoformat()}` no había "
          f"terminado: el rango consultado llega hasta `{iso(fin)}` pero la recolección seguía "
          f"activa, de modo que el total del día solo se conoce al cierre del día local "
          f"`{iso(fin)}`. Cualquier lectura de este número como \"cuánto se recolectó ese día\" "
          f"es una lectura incorrecta; lo que afirma es \"cuánto había recolectado al instante "
          f"`{iso(ejecucion)}`\".\n")
    A(bloque_sql(q_total, r_total))

    A("## 2. Desglose por subreddit (denominador completo)\n")
    A(f"Los {len(filas_dist)} subreddit(s) monitorizado(s) de `subreddits` se listan todos, "
      f"incluido el que aporta 0. El denominador de todo porcentaje de esta ventana son los "
      f"**{len(filas_dist)} subreddit(s) monitorizado(s)**, no solo los que aportaron posts "
      f"(RN-GL-02); el `n` observado del día es **{total_dia}** y la suma de los `n` de la tabla "
      f"coincide con él. Un subreddit sin fila propia se reportaría con `n = 0` y su causa "
      f"declarada.\n")
    A("| subreddit | n (día) | % sobre el día | `active_monitoring` | causa cuando n = 0 |")
    A("|---|---|---|---|---|")
    for nombre, activo, n in filas_dist:
        pct = "no aplica (n del día = 0)" if total_dia == 0 else f"{100.0 * n / total_dia:.1f} %"
        causa = "sin datos ingeridos en el día" if n == 0 and total_dia > 0 else (
            "el día no aporta datos" if n == 0 else "—")
        A(f"| {nombre} | {n} | {pct} | {str(bool(activo)).lower()} | {causa} |")
    A("")
    A(f"Subreddits con `active_monitoring = true` en la base: "
      f"{', '.join(monitorizados) if monitorizados else '(ninguno)'} "
      f"({len(monitorizados)} de {SUBSIDIOS_ESPERADOS} esperados). Ninguno se desactiva para "
      f"ajustar la cobertura.\n")
    if subs_faltantes:
        A(f"> **Alerta de cobertura**: no se encontraron filas en `subreddits` para "
          f"{', '.join(subs_faltantes)}. El denominador declarado ({len(filas_dist)}) no coincide "
          f"con los {SUBSIDIOS_ESPERADOS} subreddits monitorizados del alcance; se reporta, no se "
          f"rellena.\n")
    A(f"Consulta de control de los monitorizados:\n")
    A(bloque_sql(q_subs, r_subs))

    A(f"## 3. Acumulado de la ventana `{VENTANA_ID}`\n")
    A(f"Rango: `ingested_at >= {iso(inicio_ventana)}` y `ingested_at < {iso(corte_efectivo)}` "
      f"(corte `{VENTANA_CORTE_ESTADO}`, por eso el límite superior es el instante de ejecución).\n")
    A(bloque_sql(q_acum, r_acum))

    A("## 4. Días completos evaluados (criterio de suficiencia)\n")
    A(f"Criterio: la ventana se declara suficiente con **{DIAS_SUFICIENTES} días completos de "
      f"evaluaciones** en `anomalias` (base comparativa de RN-AN-02: media diaria de los diez "
      f"días previos). El estado es consultable, no estimado: sale de las filas reales de "
      f"`anomalias` agrupadas por `ventana_fin`.\n")
    A(bloque_sql(q_dias, r_dias))
    A("| Métrica de suficiencia | Valor |")
    A("|---|---|")
    A(f"| Días completos evaluados (distintos) | **{dias_completos}** |")
    A(f"| Umbral de suficiencia | {DIAS_SUFICIENTES} |")
    A(f"| Estado de la ventana | **{'ABIERTA' if dias_completos < DIAS_SUFICIENTES else 'SUFICIENTE'}** |")
    A("")
    A(f"> Con {dias_completos} de {DIAS_SUFICIENTES} días completos evaluados, la base "
      f"comparativa de RN-AN-02 está incompleta: el estado se reporta como limitación "
      f"(RN-AN-06) y **no** como ausencia de anomalías.\n")

    A("## 5. Ejecuciones fallidas y su causa\n")
    if not observado:
        A("**Sin observación.**\n")
        A("**Estado de ejecución de n8n: `no observado en la generación de esta entrada`.** "
          "La bitácora no observa la instancia n8n: el estado del trigger `Schedule Ingesta`, el "
          "estado de los nodos y el log de ejecuciones están fuera de `tesi_osint` y no se "
          "presumen. La verificación de instancia del día (cluster PostgreSQL, puerto de n8n, "
          "disponibilidad del log) se registra aparte, con su comando y su salida real, en el "
          "documento de verificación de instancia de la fecha cuando esa verificación se "
          "realizó.\n")
    else:
        A(f"**Estado de ejecución de n8n: `{estado_txt}`.**\n")
        A("Este estado **no lo midió este script**: la base `tesi_osint` no lo persiste y el "
          "script no lee la base de n8n ni su API. Es una **declaración del operador** "
          "recibida por parámetro al generar la entrada, y por eso se registra como declaración "
          "y no como medición. La evidencia literal que la respalda (consulta y salida real) "
          "está en el documento de verificación de instancia de la fecha y en los archivos de "
          "salida archivados con esa fecha.\n")
        if detalle_txt:
            A(f"**Detalle declarado por el operador:** {detalle_txt}\n")
    A("| Campo | Valor |")
    A("|---|---|")
    A("| Ejecuciones fallidas del día | `sin observación directa` — este script no consulta el "
      "log de n8n. " + (f"El único dato disponible es el detalle declarado por el operador de la "
                         "fila siguiente" if observado else
                         "No hay fuente observada para esta fecha") + " |")
    A(f"| Estado de ejecución de n8n (instancia y trigger `Schedule Ingesta`) | **{estado_txt}**"
      + (" — declarado por el operador; no verificado por el script" if observado
         else " — no observable desde `tesi_osint`; se declara, no se supone") + " |")
    A("| Origen del estado | " + ("declaración del operador, vía `--n8n-estado` al generar esta "
                                  "entrada" if observado else
                                  "sin observación: no se pasó `--n8n-estado`") + " |")
    A("| Detalle declarado por el operador | " + (detalle_txt if detalle_txt else
                                                 "(ninguno: no se pasó `--n8n-detalle`)") + " |")
    A("| Fuente declarada | log de ejecuciones de la instancia n8n (fuera de `tesi_osint`) |")
    A("| Por qué la base no alcanza | la base no persiste bitácora de ejecuciones: el `upsert` "
      "idempotente deja el mismo conteo tras un fallo, así que el total de la sección 1 no "
      "distingue \"no se ingirió nada\" de \"no se ejecutó\" |")
    A("| Método de captura | transcripción **manual** al log de n8n (D-3) — "
      + ("transcrito por el operador al generar esta entrada" if observado
         else "no realizada en esta corrida del script") + " |")
    A("| Estado | " + ("cerrado para esta fecha: el estado quedó declarado y su evidencia "
                       "archivada con la fecha del día" if observado else
                       "abierto: la transcripción del log del día corresponde a la tarea 3.2 "
                       "del change") + " |")
    A("")
    A("> No se asume que las ejecuciones hayan sido exitosas: asumir éxito sería fabricar un "
      "dato (RN-GL-01). Cuando no hay estado declarado, esta entrada dice literalmente `no "
      "observado`, nunca `exitoso`; el valor por defecto del script no puede ser un éxito.\n")

    A("## 6. Observaciones del día\n")
    if total_dia == 0:
        A(f"- El día `{fecha.isoformat()}` tiene `n = 0` posts ingeridos. La causa **no es "
          f"observable desde `tesi_osint`**: hay que contrastar con el log de ejecuciones de n8n "
          f"(tarea 3.2). Queda registrado como observación, no como falla atribuida.\n")
    else:
        A(f"- El día `{fecha.isoformat()}` acumula `n = {total_dia}` posts al instante de esta "
          f"generación. El día no estaba cerrado cuando se generó la entrada (§1), así que el "
          f"número es un **corte parcial** y no el total del día.\n")
    if observado:
        A(f"- **Estado de ejecución de n8n: {estado_txt}.** No se registró ninguna falla "
          f"atribuida desde `tesi_osint`; la única observación disponible es la declaración del "
          f"operador de §5, transcrita manualmente desde el log de la instancia (D-3).\n")
    else:
        A("- **Estado de ejecución de n8n: `no observado en la generación de esta entrada`.** No "
          "se registró ninguna ejecución exitosa ni ninguna falla atribuida: la fuente (log de "
          "la instancia n8n) no es observable desde esta base y su transcripción es manual "
          "cuando exista (D-3).\n")
    A(f"- Los conteos provienen exclusivamente de consultas `SELECT` sobre `tesi_osint`: "
      f"ninguna cifra de esta entrada se deriva de resultados de V2/V3 ni de tasas supuestas.\n")
    A(f"- Ningún porcentaje de esta entrada se completa con datos de fuentes ajenas al sistema "
      f"(RN-GL-02). Los ceros se reportan con su causa y no se compensan.\n")
    A(f"- La cobertura por subreddit está sesgada por el rate limiting de Reddit; el sesgo se "
      f"reporta como limitación en `V4/evidencias/CARACTERIZACION_RATE_LIMIT.md` y no se "
      f"compensa (D-5).\n")
    A("- Entrada idempotente: reejecutar el script con la misma fecha regenera este archivo desde "
      "el mismo estado de la base, sin modificar datos ni esquema. Los conteos, la distribución "
      "por subreddit y el estado de suficiencia se mantienen; lo único que cambia entre corridas "
      "es la marca de tiempo de ejecución, que figura en la cabecera y actúa de límite superior "
      "de la ventana mientras el corte siga `no fijada`.\n")

    return "\n".join(L)


def escribir_atomico(ruta: str, contenido: str) -> None:
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    tmp = ruta + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenido)
    os.replace(tmp, ruta)


# --------------------------------------------------------------------- main
class ArgumentosInvalidos(argparse.ArgumentParser):
    """ argparse sale con 2 por defecto; acá los argumentos inválidos salen con 4. """

    def error(self, message):
        self.print_usage(sys.stderr)
        print(f"ERROR: {message}", file=sys.stderr)
        print("       No se escribe ninguna entrada.", file=sys.stderr)
        sys.exit(4)


def main(argv=None) -> int:
    ap = ArgumentosInvalidos(
        description="Genera la entrada de bitácora diaria de la ventana B5 (solo lectura).")
    ap.add_argument("--fecha", help="Fecha de la entrada en formato YYYY-MM-DD (por defecto: hoy)")
    ap.add_argument("--n8n-estado", choices=sorted(ESTADOS_N8N), default=ESTADO_N8N_POR_DEFECTO,
                    help="Estado de la instancia n8n DECLARADO por el operador. El script no lo "
                         f"consulta. Por defecto: {ESTADO_N8N_POR_DEFECTO} "
                         "(\"no observado en la generación de esta entrada\").")
    ap.add_argument("--n8n-detalle", default=None,
                    help="Detalle literal de lo observado por el operador, para transcribirlo a "
                         "la entrada. Requiere --n8n-estado explícito.")
    args = ap.parse_args(argv)

    try:
        if args.fecha:
            fecha = date.fromisoformat(args.fecha)
        else:
            fecha = datetime.now(zona()).date()
    except ValueError:
        print("ERROR: --fecha debe tener formato YYYY-MM-DD (ej. 2026-09-25).", file=sys.stderr)
        return 4

    # El detalle sin estado no se acepta: un observación suelta, sin el estado al que
    # corresponde, no es un dato registrable. Y el estado por defecto nunca se infiere.
    detalle = (args.n8n_detalle or "").strip() or None
    if detalle and args.n8n_estado == ESTADO_N8N_POR_DEFECTO:
        print("ERROR: --n8n-detalle requiere declarar --n8n-estado con el valor observado "
              "(no con el valor por defecto). No se escribe ninguna entrada.", file=sys.stderr)
        return 4

    tz = zona()
    inicio, fin = limites_del_dia(fecha, tz)
    inicio_ventana = datetime.fromisoformat(VENTANA_INICIO).replace(tzinfo=tz)
    ejecucion = datetime.now(tz)
    corte_efectivo = ejecucion  # corte "no fijada": el límite superior es el instante de ejecución

    try:
        import psycopg2
    except ImportError:
        print("ERROR: falta el driver psycopg2. No se escribe ninguna entrada.", file=sys.stderr)
        return 2

    cfg = None
    destino = os.path.join(DIR_BITACORA, f"{fecha.isoformat()}.md")
    try:
        cfg = parametros_conexion()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    # --- conexión (si falla, se aborta sin escribir nada) ---------------------
    try:
        conexion = psycopg2.connect(connect_timeout=5, **cfg)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: no se pudo conectar a la base ({cfg['host']}:{cfg['port']}/{cfg['dbname']}): "
              f"{type(exc).__name__}: {exc}".replace("\n", " "), file=sys.stderr)
        print("       No se escribió ninguna entrada: no se genera evidencia parcial "
              "(tarea 2.6).", file=sys.stderr)
        return 2

    try:
        conexion.set_session(readonly=True, autocommit=True)
    except Exception:  # noqa: BLE001
        pass

    try:
        with conexion.cursor() as cur:
            q_total = sql_total_dia(inicio, fin)
            r_total = ejecutar(cur, q_total)

            q_dist = sql_distribucion(inicio, fin)
            r_dist = ejecutar(cur, q_dist)

            q_acum = sql_acumulado_ventana(inicio_ventana, corte_efectivo)
            r_acum = ejecutar(cur, q_acum)

            q_dias = sql_dias_evaluados(inicio_ventana, corte_efectivo)
            r_dias = ejecutar(cur, q_dias)

            q_subs = sql_subreddits_monitorizados()
            r_subs = ejecutar(cur, q_subs)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: falló una consulta de solo lectura: {type(exc).__name__}: {exc}".replace("\n", " "),
              file=sys.stderr)
        print("       No se escribió ninguna entrada: no se genera evidencia parcial "
              "(tarea 2.6).", file=sys.stderr)
        return 3
    finally:
        conexion.close()

    contenido = render_entrada(
        fecha, tz, ejecucion, inicio, fin, inicio_ventana, corte_efectivo,
        q_total, r_total, q_dist, r_dist, q_acum, r_acum, q_dias, r_dias, q_subs, r_subs,
        estado_n8n=args.n8n_estado, detalle_n8n=detalle,
    )
    escribir_atomico(destino, contenido)

    total_dia = int(r_total[0][0]) or 0
    print(f"OK -> {destino}")
    print(f"   ventana={VENTANA_ID} fecha={fecha.isoformat()} n={total_dia} "
          f"dias_completos_evaluados={len(r_dias)}/{DIAS_SUFICIENTES}")
    print(f"   n8n_estado={args.n8n_estado} ({ESTADOS_N8N[args.n8n_estado]})")
    return 0


if __name__ == "__main__":
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            pass
    sys.exit(main())
