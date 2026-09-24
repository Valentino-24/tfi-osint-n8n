# GUÍA DE EJECUCIÓN — B3 / B4 (delivered 2026-09-24)

## Estado actual

| Paso | Estado |
|---|---|
| B1 Entorno | ✅ PostgreSQL 18 (5433) + n8n 2.22.6 + base `tesi_osint` |
| B2 DDL | ✅ **Verificado**: las 5 tablas existen (`subreddits`, `posts`, `comments`, `anomalias`, `alertas`) — todas vacías |
| B3 Workflow | ✅ **Generado y validado** `V4\anexos\B_workflow.json` (15 nodos, import exitoso con `n8n import:workflow`) |
| B4 Correr | ⏳ Este documento |

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

### Troubleshooting rápido

| Síntoma | Causa probable | Fix |
|---|---|---|
| CODE: "Falta la variable de entorno OSINT_HMAC_KEY" | n8n arrancó sin el env | Setear env y reiniciar n8n |
| "NODE_FUNCTION_ALLOW_BUILTIN" requerido pero no seteado | `require('crypto')` bloqueado | `$env:NODE_FUNCTION_ALLOW_BUILTIN = "crypto"` y reiniciar |
| HTTP 403/429 de Reddit (RSS) | Reddit bloquea/rate-limita el IP temporalmente | El nodo RSS Read tiene retry x3 cada 30 s; si persiste, esperar 1 min (ventana de rate limit público); última opción: volver a OAuth con otra cuenta |
| PostgreSQL: connection refused | Cluster del proyecto apagado | `V4\scripts\arrancar_postgres.bat` |
| El trigger de anomalías no da alertas | No hay datos o nada superó el umbral | Es esperable — es la evidencia E7 (registro de evaluaciones) |