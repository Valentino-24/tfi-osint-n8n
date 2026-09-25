# GUÍA DE EJECUCIÓN — B3 / B4 (delivered 2026-09-24)

> **B5** agrega la ventana de recolección real: ver la sección *Ventana de recolección real (B5)*.

## Estado actual

| Paso | Estado |
|---|---|
| B1 Entorno | ✅ PostgreSQL 18 (5433) + n8n 2.22.6 + base `tesi_osint` |
| B2 DDL | ✅ **Verificado**: las 5 tablas existen (`subreddits`, `posts`, `comments`, `anomalias`, `alertas`) — todas vacías |
| B3 Workflow | ✅ **Generado y validado** `V4\anexos\B_workflow.json` (15 nodos, import exitoso con `n8n import:workflow`) |
| B4 Correr | ⏳ Este documento |
| B5 Ventana | ⏳ **Ventana real abierta y con recolección activa**: inicio **2026-09-25**, corte **`no fijada`** (decisión de los autores con sus directores). Workflow **publicado el 2026-09-25** (`active = 1`): **33 posts** dentro de la ventana al cierre de la pasada de las 15:07, primer ciclo **programado pendiente**. Evidencia y bitácora diaria en `V4\evidencias\VENTANA_B5.md` y `V4\evidencias\bitacora_b5\`. Cierre pendiente (C-05, tarea 6.1) |

---

## El workflow (qué hace)

**Trigger 1 — Ingesta (cada 15 min):**
`Schedule` → `Prepare Subreddits` (r/argentina, r/devsarg, r/derechogenial)
→ rama A: upsert de subreddits (subscribers en 0 — no disponible via RSS)
→ rama B: `new/.rss` (feed Atom público) → parse (id y subreddit salen del link del post) → **HMAC-SHA-256** (seudonimiza author) → **clasificador por diccionario** (5 categorías + "No relevante", score [0,1]) → **extracción de entidades** (CVE, emails, IPs, dominios, productos) → **upsert `ON CONFLICT (id) DO UPDATE`** (idempotente; `ingested_at` no se toca → sirve para latencia).

> **Decisión 2026-09-24 (Plan C):** la cuenta Reddit está bloqueada para crear apps (`prefs/apps` → banner Responsible Builder Policy, requiere developer account) y los endpoints `.json` públicos dan **403 "blocked by network security"** desde esta IP. El workflow usa entonces los **feeds RSS públicos (Atom)** con el nodo *RSS Read*: 3 requests por ciclo de 15 min (rate limit público ~10/min, retry x3 cada 30 s por si pega 429). **Limitación:** el RSS no trae `score`, `num_comments` ni suscriptores → quedan en 0 (ningún nodo del pipeline depende de ellos; el motor de anomalías usa counts por categoría). Si en el futuro se consigue una app de Reddit (developer account), se regenera el workflow con OAuth desde `V4/scripts/generar_workflow.py` y se recuperan esos campos.

**Trigger 2 — Motor de anomalías (diario 00:05):**
`Schedule` → counts por categoría de ayer + media diaria de los 10 días previos
→ **umbral = max(cuantil 95 de Poisson + 1, mínimo absoluto 3)** → registra TODAS las evaluaciones en `anomalias` → si hubo disparo, inserta en `alertas` (estado `PENDIENTE`) → Send Telegram (deshabilitado por defecto).

> Decisiones técnicas a revisar en la defensa: umbral del motor (Poisson, no μ+2σ), comentarios FUERA de alcance (Tabla 2 se reconstruye solo con posts), Telegram opcional.

---

## B4 — Paso a paso

### 1. Variables de entorno (ANTES de arrancar n8n)

Abrí PowerShell y seteá (persisten solo en esa ventana; para que persistan usá `setx`):

```powershell
# Clave secreta HMAC por despliegue — GENERALA (no uses una fija):
$hmac = python -c "import secrets; print(secrets.token_hex(32))"
$env:OSINT_HMAC_KEY = $hmac
$env:NODE_FUNCTION_ALLOW_BUILTIN = "crypto"      # para require('crypto') en nodos Code
$env:N8N_BLOCK_ENV_ACCESS_IN_NODE = "false"      # para que $env funcione en nodos Code
```

> 📌 Guardá el valor de `$hmac` en anotaciones locales: es la "clave secreta por despliegue" (H-01) y se documenta en el Anexo E9 (entorno). Si n8n ya estaba abierto, cerrarlo y reabrirlo con estas variables.

### 2. Arrancar n8n y crear cuenta

```powershell
n8n start
```
Abrí http://localhost:5678 → creá la cuenta local (usuario/contraseña que quieras).

### 3. Importar el workflow

- **Puede que ya esté importado**: la validación técnica usó `n8n import:workflow`, así que al abrir Workflows probablemente ya ves **"TFI OSINT V4 - Monitor de Amenazas"**.
- Si no aparece: **Workflows → Add workflow → ⋯ → Import from File** → `V4\anexos\B_workflow.json`. El import sobrescribe por id (no duplica).

### 4. Crear y asignar credenciales (1 obligatoria + 1 opcional)

| Credencial | Dónde | Valores |
|---|---|---|
| **Postgres** | Nodos `Upsert Subreddits`, `Upsert Posts`, `Query Daily Counts`, `Registrar Anomalias y Alertas` (4 nodos) | Host `localhost`, Puerto `5433`, DB `tesi_osint`, Usuario `tesi_app`, Password `tesi_app_2026` |
| **Telegram** (opcional) | Nodo `Send Telegram Alert` | Crear bot con @BotFather → `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` como env; luego habilitar el nodo |

> No hace falta credencial Reddit: el workflow consulta los endpoints públicos sin OAuth (ver nota en "El workflow"). Si en el futuro se vuelve a OAuth, se agrega la credential tipo httpBasicAuth en el nodo `Get Reddit Token` regenerando el workflow desde el generador.

### 5. Probar el flujo (sin esperar los 15 min)

1. En el workflow, abrí el nodo `Schedule Ingesta` → **Execute workflow** (o el botón "Test workflow").
2. Esperá a que los nodos queden verdes.
3. Verificá en la base:

```powershell
$env:PGPASSWORD = "tesi_app_2026"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -w -U tesi_app -h localhost -p 5433 -d tesi_osint -c "SELECT COUNT(*) FROM posts;"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -w -U tesi_app -h localhost -p 5433 -d tesi_osint -c "SELECT subreddit_id, title, nlp_category, nlp_score FROM posts ORDER BY ingested_at DESC LIMIT 10;"
```

> Si `posts` tiene filas y `nlp_category` no es todo NULL → **B4 cumplido**, el sistema quedó recolectando. Desde ahí se edita la ventana real (B5) y se sacan evidencias (B6).

---

## Ventana de recolección real (B5)

La ventana de recolección **no dura seis meses**: la ventana ficticia de V2/V3 quedó derogada
(SU-02). La ventana vigente es la **B5** y su definición completa está en
[`evidencias\VENTANA_B5.md`](evidencias/VENTANA_B5.md).

| Campo | Valor |
|---|---|
| Identificador | **B5** |
| Inicio | **2026-09-25** (fijo) |
| Corte | **`no fijada`** — decisión abierta de los autores con sus directores (tarea 6.1 del change C-05) |
| Criterio del corpus | `posts.ingested_at` dentro del rango de la ventana (no `created_utc`: `ingested_at` es la evidencia de lo que el sistema recolectó) |
| Zona horaria de los límites | `America/Argentina/Buenos_Aires` |
| Criterio de suficiencia | 10 días completos de evaluaciones en `anomalias` (base comparativa de RN-AN-02) |
| Estado | **ABIERTA** — recolección activa, cierre pendiente |

### Estado de la recolección (actualizado 2026-09-25)

| Campo | Valor |
|---|---|
| Estado de la recolección | **Activa** — la ventana **está recolectando** |
| Workflow | `TFIOsintV4Monitor01` — *TFI OSINT V4 - Monitor de Amenazas*, **publicado** el 2026-09-25 (`active = 1`, `versionId` `abe9e78c-4854-4243-b2ea-58dbc4a57a9f`) |
| `n` dentro de la ventana al cierre de la pasada del 2026-09-25 15:07 | **33 posts** — corte a mitad de día, **no** un total de día cerrado |
| Distribución dentro de la ventana | `r/argentina` 33, `r/devsarg` 0, `r/derechogenial` 0 (denominador: los 3 monitorizados) |
| Posts en la base completa | **234** = 201 de la corrida B4 del 2026-09-24 + 33 de la ventana |
| Primer ciclo **programado** | **Pendiente** — ocurre dentro de los 15 minutos de publicado el workflow. Al cierre de la pasada el log de n8n registra **0** ejecuciones programadas |
| Origen de los 33 posts | La ejecución `id 9` de n8n, `status = success`, duración 8.4 s, **`mode = manual`**: la disparó el operador desde la UI con *Execute workflow*, **no** un tick del trigger de 15 minutos |
| Días completos evaluados | **0 de 10** — `anomalias` sigue vacía. La primera evaluación diaria se espera el `2026-09-26` a las 00:05 |
| Evidencia | `V4\evidencias\VERIFICACION_INSTANCIA_2026-09-25.md` §10, `V4\evidencias\n8n_2026-09-25_estado_y_ejecuciones.txt`, `V4\evidencias\psql_2026-09-25_ventana_b5_dia_2026-09-25.txt` |

> El `n = 33` prueba que el pipeline funciona, pero **no** es todavía evidencia de recolección
> sostenida: viene de una ejecución manual. La continuidad de la ventana la sostiene el trigger
> programado de 15 minutos, que al cierre de esa pasada todavía no había producido ninguna
> ejecución. Publicar el workflow no acelera la suficiencia: el criterio de 10 días mide
> **días completos de evaluaciones** en `anomalias`, y esa tabla sigue vacía.

Qué queda **fuera** del corpus de la ventana: los 201 posts de la corrida B4 del 2026-09-24
tienen `ingested_at` del 2026-09-24, un día antes del inicio. Se conservan como evidencia
técnica de B4 y de la caracterización del rate limiting, pero no se mezclan con el corpus de
resultados salvo decisión explícita de los autores (tarea 6.3).

### Bitácora diaria de la ventana

Cada día de la ventana tiene una entrada en `V4\evidencias\bitacora_b5\YYYY-MM-DD.md`, generada
por `V4\scripts\bitacora_b5.py` con consultas `SELECT` de solo lectura. El script toma la fecha
como parámetro y no escribe nada en la base:

```powershell
$env:PGUSER     = "<rol de la base>"          # el rol debe venir del entorno
$env:PGPASSWORD = "<clave del rol local>"     # nunca en el código
python V4\scripts\bitacora_b5.py --fecha 2026-09-25
```

> El script **no** lee la instancia n8n ni su base: el estado de ejecución de n8n **no** sale de la
> base de datos. Lo **declara el operador** con dos parámetros opcionales, y su valor por defecto es
> `no_observado` ("no observado en la generación de esta entrada"). El script nunca infiere ni
> asume un resultado:
>
> ```powershell
> python V4\scripts\bitacora_b5.py --fecha 2026-09-25 `
>     --n8n-estado instancia_arriba_workflow_publicado `
>     --n8n-detalle "<descripción literal de lo observado, con su ejecución y sus marcas de tiempo>"
> ```
>
> Valores admitidos por `--n8n-estado`: `no_observado` (por defecto), `instancia_caida`,
> `instancia_arriba_workflow_inactivo`, `instancia_arriba_workflow_publicado`. `--n8n-detalle`
> exige un estado explícito. Para una fecha sin log de ejecuciones, se omiten los dos y la entrada
> dice `no observado` — nunca `exitoso` (RN-GL-01).

Cada entrada declara la consulta SQL literal, la fecha de ejecución, el identificador de la
ventana y el `n` de la observación, y lista los **tres** subreddits monitorizados con su recuento
real, incluido el 0 (RN-GL-01, RN-GL-02). El script marca solo el `n` como **corte a mitad de día**
cuando el día todavía no terminó, para que ese número no se lea como un total de día cerrado. Si la
conexión falla, el script termina con error explícito y **no** escribe una entrada parcial.

### Troubleshooting rápido

| Síntoma | Causa probable | Fix |
|---|---|---|
| CODE: "Falta la variable de entorno OSINT_HMAC_KEY" | n8n arrancó sin el env | Setear env y reiniciar n8n |
| "NODE_FUNCTION_ALLOW_BUILTIN" requerido pero no seteado | `require('crypto')` bloqueado | `$env:NODE_FUNCTION_ALLOW_BUILTIN = "crypto"` y reiniciar |
| HTTP 403/429 de Reddit (RSS) | Reddit bloquea/rate-limita el IP temporalmente | El nodo RSS Read tiene retry x3 cada 30 s; si persiste, esperar 1 min (ventana de rate limit público); última opción: volver a OAuth con otra cuenta |
| PostgreSQL: connection refused | Cluster del proyecto apagado | `V4\scripts\arrancar_postgres.bat` |
| El trigger de anomalías no da alertas | No hay datos o nada superó el umbral | Es esperable — es la evidencia E7 (registro de evaluaciones) |