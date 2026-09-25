# Verificación de instancia — 2026-09-25

> Change OpenSpec: `ventana-recoleccion-b5` (C-05), tareas 3.1, 3.2, 3.3, 3.5 y estado de 6.5.
> Documento de evidencia operacional, no de resultados: acá no se declara ninguna métrica de
> resultados, solo el estado verificable de la instancia y lo que **no** se pudo verificar
> (RN-GL-01).

> **⚠ ESTADO DE ESTE DOCUMENTO — dos pasadas el mismo día.** Este archivo registra **dos**
> verificaciones del 2026-09-25 y **las dos se conservan**: la primera no se borra ni se corrige,
> porque un registro que se reescribe cuando el resultado cambia no es evidencia de nada.
>
> | Pasada | Instante | Registrada en | Qué pudo observar |
> |---|---|---|---|
> | **1ª pasada** | `2026-09-25` ~14:23 `America/Argentina/Buenos_Aires` | §1 a §9 | Solo el cluster PostgreSQL. La instancia n8n estaba **caída** |
> | **2ª pasada (re-verificación)** | `2026-09-25` 15:07 `America/Argentina/Buenos_Aires` | **[§10](#10-re-verificación-2026-09-25--instancia-arriba-y-workflow-publicado)** | Instancia n8n **arriba** y workflow **publicado** |
>
> **Qué queda SUPERSEDIDO por §10, y qué NO:** §1 (PostgreSQL) **sigue vigente** tal cual. En
> cambio, §2 (n8n no verificable), §3 (no hay log que transcribir) y §4 (`sin observación`) quedan
> **SUPERSEDIDOS** en sus afirmaciones sobre el estado de n8n, y esa fue precisamente la conclusión
> honesta de la primera pasada con la información que había. §5, §6, §7 y §8 se marcan punto por
> punto dentro de §10. Nada de §10 borra lo anterior: la diferencia entre ambas pasadas es
> justamente el objeto de la evidencia.

| Campo | Valor |
|---|---|
| Fecha de la verificación | `2026-09-25` |
| Identificador de la ventana | **B5** (inicio 2026-09-25, corte `no fijada`) |
| Días transcurridos de la ventana al 2026-09-25 | 1 (solo el día de inicio) |
| Zona horaria de los límites | `America/Argentina/Buenos_Aires` |
| Tipo de verificación | Solo lectura. Sin escrituras, sin DDL, sin cambios en el workflow |
| Credenciales | Definidas por variables de entorno de la sesión. Ningún rol, clave o cadena de conexión se registra en este archivo |

## 1. Cluster PostgreSQL en `localhost:5433`: **VERIFICADO arriba**

### 1.1 Estado del servicio

Comando literal:

```powershell
Get-Service -Name "postgresql-x64-18" | Select-Object Name,Status,StartType | Format-List
```

Salida real:

```
Name      : postgresql-x64-18
Status    : Running
StartType : Automatic
```

### 1.2 Puerto 5433

Comando literal:

```powershell
Test-NetConnection -ComputerName localhost -Port 5433 | Select-Object ComputerName,RemotePort,TcpTestSucceeded | Format-List
```

Salida real:

```
ComputerName     : localhost
RemotePort       : 5433
TcpTestSucceeded : True
```

### 1.3 Conexión y versión del servidor

Comando literal (el host, el puerto, la base, el rol y la clave vienen de las variables
`PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER` y `PGPASSWORD` de la sesión; ninguno de esos
valores se transcribe acá):

```powershell
psql -X -q -c "SELECT version();"
```

Salida real:

```
                                 version
------------------------------------------------------------------------
 PostgreSQL 18.0 on x86_64-windows, compiled by msvc-19.44.35217, 64-bit
(1 fila)
```

**Estado registrado: VERIFICADO.** El cluster del proyecto está arriba en `localhost:5433` y
responde consultas de solo lectura a la base de la ventana. Formato de salida de psql:
`(1 fila)` en español, coherente con la locale del cluster.

## 2. Instancia n8n y trigger `Schedule Ingesta`: **NO VERIFICABLE en esta corrida**

### 2.1 Puerto 5678

Comando literal:

```powershell
Test-NetConnection -ComputerName localhost -Port 5678 | Select-Object ComputerName,RemotePort,TcpTestSucceeded | Format-List
```

Salida real:

```
ADVERTENCIA: TCP connect to (::1 : 5678) failed
ADVERTENCIA: TCP connect to (127.0.0.1 : 5678) failed

ComputerName     : localhost
RemotePort       : 5678
TcpTestSucceeded : False
```

### 2.2 Proceso de n8n

Comando literal:

```powershell
Get-Process -Name node,n8n -ErrorAction SilentlyContinue
```

Salida real:

```
(sin procesos node ni n8n)
```

### 2.3 Estado registrado

> **Estado: `no verificable en esta corrida`: la instancia n8n no está levantada
> (`localhost:5678` sin respuesta, sin proceso `node`).**

Consecuencias, sin excepciones:

| Punto | Estado |
|---|---|
| ¿El trigger `Schedule Ingesta` (15 min) está activo? | **No verificable en esta corrida.** No se puede observar el workflow, sus nodos ni su estado de activación con la instancia caída |
| ¿Se afirma que el trigger está activo? | **No.** Afirmarlo sin poder observarlo sería fabricar un dato (RN-GL-01) |
| ¿Hay base de datos de n8n en el cluster para contrastar? | **No.** El cluster solo contiene `postgres` y `tesi_osint`; no hay base de n8n desde la cual reconstruir activaciones o ejecuciones |
| Estado de la verificación del trigger | **Pendiente de re-verificación** cuando la instancia n8n esté levantada. Ninguna tarea de este change depende de ello para continuar: la recolección y la bitácora siguen declarando su propio estado |
| Qué sí quedó verificado | Que el cluster PostgreSQL está arriba (§1) y que la base responde consultas `SELECT` |

## 3. Log de ejecuciones de n8n: **no hay log que transcribir** (tarea 3.2)

La fuente declarada de "ejecuciones fallidas y su causa" es el **log de ejecuciones de la
instancia n8n** (D-3). En esta corrida:

| Campo | Valor |
|---|---|
| ¿Existe log de ejecuciones del 2026-09-25? | **No.** No hay log que transcribir |
| ¿Se transcribió algo del log a la bitácora? | **No**, porque no hay log. No se fabricó ningún registro de ejecución |
| Método de captura cuando exista | **Transcripción manual** al log de n8n, declarando el log como fuente (D-3). La transcripción es verificable contra el log, nunca automática ni supuesta |
| Registros de ejecución inventados | **Ninguno.** No se registró ninguna falla ni ningún éxito inventado |

## 4. Ejecuciones del 2026-09-25: **`sin observación`**, no "exitosas" (tarea 3.3)

| Campo | Valor |
|---|---|
| Ejecuciones de ingesta del 2026-09-25 | **`sin observación`** |
| Ejecuciones de anomalías del 2026-09-25 | **`sin observación`** |
| Se las declara exitosas | **No.** No hay log ni instancia para observarlas; declararlas exitosas sería fabricar un dato |
| Dónde quedó registrado | [`bitacora_b5/2026-09-25.md`](bitacora_b5/2026-09-25.md) §5 y §6, y este documento |

El `n = 0` de posts ingeridos el 2026-09-25 **no distingue** "no se ingirió nada" de "no se
ejecutó", porque el `upsert` idempotente deja el mismo conteo tras un fallo y la base no
persiste bitácora de ejecuciones. Por eso el día queda como observación, no como falla
atribuida ni como éxito supuesto.

## 5. Cobertura de la bitácora en los días transcurridos (tarea 3.4)

| Campo | Valor |
|---|---|
| Inicio de la ventana | `2026-09-25` |
| Fecha de esta verificación | `2026-09-25` |
| Días transcurridos | **1** |
| Entradas de bitácora existentes | **1** → [`bitacora_b5/2026-09-25.md`](bitacora_b5/2026-09-25.md) |
| Días faltantes de bitácora | **Ninguno** |
| `n` de posts ingeridos el 2026-09-25 | **0** — valor honesto y verificado: los 201 posts de la base son del 2026-09-24 (ver [`psql_2026-09-25_ventana_b5_dia_2026-09-25.txt`](psql_2026-09-25_ventana_b5_dia_2026-09-25.txt) [Q-C4]) |

Un día con total 0 se registra igual, con su causa declarada: omitirlo dejaría un hueco
indistinguible de un olvido de registro.

## 6. Limitación conocida: el log de ejecuciones no se conserva (tarea 3.5)

**Limitación registrada:** el log de ejecuciones de n8n **no está disponible ni preservado**
en este workspace (instancia no levantada, sin base de n8n en el cluster, sin directorio de
datos de n8n en el repositorio). En consecuencia:

1. El **éxito o fracaso de la ingesta día por día no puede probarse desde el log**. El campo
   de ejecuciones de la bitácora queda en `sin observación` mientras el log no esté
   disponible.
2. Cuando el log esté disponible, su contenido se **transcribe manualmente** a la entrada
   del día correspondiente, declarando el log como fuente y la transcripción como manual
   (D-3). Ese es el único camino válido; no se automatiza en este change.
3. La limitación se reporta en el Capítulo 5 de la tesis como limitación de la evidencia de
   falla, no como ausencia de fallas.
4. En la base de conocimiento queda referenciada en
   [`knowledge-base/10_preguntas_abiertas.md`](../../knowledge-base/10_preguntas_abiertas.md)
   junto a la pregunta abierta priorizada.

**Consecuencia sobre el diseño, no un defecto a corregir acá:** automatizar la captura del
log implicaría tocar el workflow, que está congelado en este change (D-8). Se deja como
deuda consciente, declarada.

## 7. Estado de suficiencia al 2026-09-25 (tarea 6.5: **NO cumplida**)

| Métrica de suficiencia | Valor | Origen |
|---|---|---|
| Días completos evaluados en `anomalias` dentro de la ventana B5 | **0** | `SELECT` agrupado por `ventana_fin` — [`psql_2026-09-25_suficiencia_anomalias.txt`](psql_2026-09-25_suficiencia_anomalias.txt) [Q-D1] |
| Umbral de suficiencia (D-6, base comparativa de RN-AN-02) | **10** | criterio declarado, no medido |
| Estado | **0 de 10 → 0 % del umbral** | consultable, no estimado |
| Estado de la ventana | **ABIERTA** | no alcanza el criterio de §4 de [`VENTANA_B5.md`](VENTANA_B5.md) |

**La tarea 6.5 queda BLOQUEADA**: el criterio de suficiencia (10 días completos de
evaluaciones) **no se alcanzó** al 2026-09-25. Como 6.5 es la condición previa de la
decisión de cierre, también quedan bloqueadas, y por la misma razón, las tareas **6.1**
(fijar la fecha de corte), **6.2** (conservar o reiniciar la recolección) y **6.3**
(incluir o excluir los posts previos al 2026-09-25): las cuatro dependen del acumulado de
evaluaciones y de una decisión de los autores, no de esta ejecución técnica. Ninguna se
marca como cumplida.

La tabla `anomalias` está **vacía en toda la base**, no solo dentro de la ventana
([Q-D3] del archivo de suficiencia): no hay historia de evaluaciones que sirva de base
comparativa. Antes del umbral, el estado se reporta como **limitación** de la base
comparativa, nunca como ausencia de anomalías (RN-AN-06).

## 8. Estado verificado de la base (solo lectura)

Consultas `SELECT` de control, con su salida real archivada en
[`psql_2026-09-25_caso_429_b4_derechogenial.txt`](psql_2026-09-25_caso_429_b4_derechogenial.txt)
y [`psql_2026-09-25_ventana_b5_dia_2026-09-25.txt`](psql_2026-09-25_ventana_b5_dia_2026-09-25.txt):

| Punto | Valor verificado | Consulta |
|---|---|---|
| Subreddits monitorizados | **3 de 3** con `active_monitoring = t`: `r/argentina`, `r/derechogenial`, `r/devsarg` | [Q-B3] / [Q-C2] |
| Posts de B4 conservados | **201**, todos con `ingested_at` del **2026-09-24** | [Q-B2] / [Q-C3] |
| Días locales con ingesta | **1** (2026-09-24) | [Q-C4] |
| Posts dentro de la ventana B5 | **0** | [Q-C1] |
| Filas en `anomalias` | **0** | [Q-C3] / [Q-D3] |
| Escrituras realizadas por este change | **0** (solo `SELECT`) | §8 de `design.md` |

Ningún subreddit se desactivó y ningún dato de B4 se modificó: el change es documental.

## 9. Documentos relacionados

| Documento | Qué aporta |
|---|---|
| [`VENTANA_B5.md`](VENTANA_B5.md) | Definición de la ventana, criterio de suficiencia y reglas de desglose por subreddit |
| [`bitacora_b5/2026-09-25.md`](bitacora_b5/2026-09-25.md) | Entrada del día transcurrido, con su consulta, fecha, ventana y `n` |
| [`CARACTERIZACION_RATE_LIMIT.md`](CARACTERIZACION_RATE_LIMIT.md) | Comportamiento observado de Reddit ante el exceso de requests y su efecto en la cobertura |
| [`psql_2026-09-25_caso_429_b4_derechogenial.txt`](psql_2026-09-25_caso_429_b4_derechogenial.txt) | Salida de psql del caso de rate limiting de la corrida B4 |
| [`psql_2026-09-25_ventana_b5_dia_2026-09-25.txt`](psql_2026-09-25_ventana_b5_dia_2026-09-25.txt) | Salida de psql de los conteos de la ventana al 2026-09-25 |
| [`psql_2026-09-25_suficiencia_anomalias.txt`](psql_2026-09-25_suficiencia_anomalias.txt) | Salida de psql del estado de suficiencia (0 de 10) |
| [`n8n_2026-09-25_estado_y_ejecuciones.txt`](n8n_2026-09-25_estado_y_ejecuciones.txt) | Salida SQLite de solo lectura: `active = 1`, `versionId` y log de ejecuciones con su columna `mode` (consultado en §10) |
| `openspec/changes/ventana-recoleccion-b5/design.md` | Decisiones D-1 a D-8; en particular D-3 (origen del dato de fallo) y D-6 (suficiencia) |

---

## 10. Re-verificación 2026-09-25 — instancia arriba y workflow publicado

| Campo | Valor |
|---|---|
| Fecha de la re-verificación | **2026-09-25**, `15:07:58` `America/Argentina/Buenos_Aires` |
| Motivo de la re-verificación | tareas 3.1, 3.2 y 3.3 quedaron **pendientes de re-verificación** en la 1ª pasada (§2) porque la instancia n8n estaba caída. La instancia quedó levantada y el workflow publicado, así que la observación ya es posible |
| Supersede | §2 (n8n no verificable), §3 (no hay log que transcribir) y §4 (`sin observación`), **solo** en lo que afirman sobre el estado de n8n al cierre de esta pasada |
| No supersede | §1 (PostgreSQL arriba, sigue vigente), §7 (suficiencia 0 de 10, sin cambios) y la §6 como registro histórico de la limitación de la 1ª pasada |
| Tipo de verificación | **Solo lectura.** `SELECT` sobre `tesi_osint` y consultas SQLite en modo `mode=ro`. Sin escrituras, sin DDL, sin cambios en el workflow |
| Salida archivada | [`n8n_2026-09-25_estado_y_ejecuciones.txt`](n8n_2026-09-25_estado_y_ejecuciones.txt) y [`psql_2026-09-25_ventana_b5_dia_2026-09-25.txt`](psql_2026-09-25_ventana_b5_dia_2026-09-25.txt) |
| Credenciales | Ninguna registrada. La base de n8n es local y no requiere rol ni clave; la de PostgreSQL se accede por variables de entorno de la sesión |

### 10.1 Tarea 3.1 — trigger `Schedule Ingesta` y cluster: **VERIFICADO**

**Estado registrado: VERIFICADO.** Los tres puntos de la tabla de §2 quedan resueltos.

| Punto de §2 que quedó pendiente | Estado al 2026-09-25 15:07 | Cómo se verificó |
|---|---|---|
| ¿El cluster PostgreSQL está arriba en `localhost:5433`? | **VERIFICADO arriba** | §1 de este documento. Sin cambios: sigue en pie, no se re-declaró |
| ¿La instancia n8n responde en `localhost:5678`? | **VERIFICADO arriba** | La consulta de §10.1.1 responde y devuelve el workflow publicado |
| ¿El workflow está activo (`active = 1`)? | **VERIFICADO: `active = 1` → PUBLICADO** | Consulta de §10.1.1 y su salida real |
| ¿Hay base de datos de n8n desde la cual reconstruir activaciones y ejecuciones? | **Sí, y se usó**: la base SQLite local de la instancia, `~/.n8n/database.sqlite`, consultada **en modo solo lectura** | Consulta de §10.1.1 y su salida real |

#### 10.1.1 Consulta literal (SQLite, solo lectura)

La conexión se abre con la URI `file:.../database.sqlite?mode=ro`: en ese modo SQLite no puede
escribir en la base. La consulta es un `SELECT` sobre `workflow_entity`.

```sql
SELECT id, name, active, versionId, triggerCount
FROM workflow_entity
WHERE name = 'TFI OSINT V4 - Monitor de Amenazas';
```

Salida real:

```
id                  | name                               | active | versionId                            | triggerCount
--------------------+------------------------------------+--------+--------------------------------------+-------------
TFIOsintV4Monitor01 | TFI OSINT V4 - Monitor de Amenazas | 1      | abe9e78c-4854-4243-b2ea-58dbc4a57a9f | 2
(1 fila)
```

| Punto | Valor verificado |
|---|---|
| `id` del workflow | **`TFIOsintV4Monitor01`** |
| `active` | **`1`** — el workflow está **publicado** y su trigger de ingesta quedó activo |
| `versionId` de la versión publicada | **`abe9e78c-4854-4243-b2ea-58dbc4a57a9f`** |
| `triggerCount` | `2` — nodos de disparo registrados (ingesta cada 15 min + anomalías diario a las 00:05). **No** es una cantidad de ticks ejecutados |

**Consecuencia sobre la 1ª pasada:** la fila "¿Se afirma que el trigger está activo?" de §2 decía
**No**, y así era lo correcto entonces: afirmar la activación sin poder observarla habría sido
fabricar un dato (RN-GL-01). Hoy el trigger **sí** se afirma activo, y se afirma **porque se
observó** (`active = 1`), no porque el tiempo haya pasado.

### 10.2 Tarea 3.2 — el log de ejecuciones **SÍ** está disponible y **SÍ** se transcribió

La fuente declarada de "ejecuciones fallidas y su causa" es el log de ejecuciones de la instancia
n8n (D-3). Al cierre de esta pasada esa fuente está disponible y su transcripción se realizó.

#### 10.2.1 Consulta literal (SQLite, solo lectura)

```sql
SELECT id, status, mode, finished, startedAt, stoppedAt,
       ROUND((julianday(stoppedAt) - julianday(startedAt)) * 86400, 1) AS duracion_s
FROM execution_entity
ORDER BY id DESC
LIMIT 5;
```

Salida real:

```
id | status  | mode   | finished | startedAt               | stoppedAt               | duracion_s
---+---------+--------+----------+-------------------------+-------------------------+-----------
9  | success | manual | 1        | 2026-09-25 17:55:35.332 | 2026-09-25 17:55:43.715 | 8.4
8  | success | manual | 1        | 2026-09-24 20:46:03.710 | 2026-09-24 20:46:06.030 | 2.3
7  | success | manual | 1        | 2026-09-24 20:44:02.141 | 2026-09-24 20:44:04.583 | 2.4
6  | success | manual | 1        | 2026-09-24 20:41:59.179 | 2026-09-24 20:42:03.381 | 4.2
5  | error   | manual | 0        | 2026-09-24 20:39:32.515 | 2026-09-24 20:39:37.048 | 4.5
(5 filas)
```

#### 10.2.2 Registro de la ejecución del 2026-09-25 — transcripción **manual**

| Campo | Valor transcrito |
|---|---|
| Método de captura | **Transcripción MANUAL** (D-3). Copia de la salida de la consulta de §10.2.1, archivada en [`n8n_2026-09-25_estado_y_ejecuciones.txt`](n8n_2026-09-25_estado_y_ejecuciones.txt). **No** es una captura automática: el script de bitácora sigue sin leer la base de n8n y el campo de la entrada del día es una declaración del operador, con ese origen declarado |
| `id` de la ejecución | **9** |
| `status` | **`success`** |
| `finished` | `1` — terminó, no quedó en cola |
| `mode` | **`manual`** — ver §10.2.3, que es el punto metodológico central de esta pasada |
| `startedAt` (UTC, como lo persiste n8n) | `2026-09-25 17:55:35.332` |
| `stoppedAt` (UTC, como lo persiste n8n) | `2026-09-25 17:55:43.715` |
| `startedAt` en `America/Argentina/Buenos_Aires` | `2026-09-25 14:55:35.332` |
| `stoppedAt` en `America/Argentina/Buenos_Aires` | `2026-09-25 14:55:43.715` |
| Duración | **8.4 s** |
| Ejecuciones **fallidas** del 2026-09-25 | **0**. La única ejecución del día es la 9 y fue `success` |
| Ejecuciones del 2026-09-24 (fuera de la ventana B5) | `id 8` success, `id 7` success, `id 6` success, `id 5` **error** (`finished = 0`) — todas de la validación técnica de B4 |

Conversión de zona horaria: n8n persiste `startedAt` y `stoppedAt` en **UTC**; la zona de ejecución
del sistema es `America/Argentina/Buenos_Aires` (UTC−03:00, sin horario de verano desde 2009), de
modo que `hora local = UTC − 03:00`.

#### 10.2.3 **MANUAL** vs **PROGRAMADA** — la distinción que este change tenía que declarar

> **La ejecución 9 fue disparada manualmente desde la UI de n8n con el botón *Execute workflow*. NO
> fue un tick del trigger `Schedule Ingesta` de 15 minutos. La ingesta del 2026-09-25 fue MANUAL, no
> PROGRAMADA.**

La distinción no es una interpretación: sale de la columna `mode` de `execution_entity`, consultada
literalmente.

Consulta literal (control: ¿existe alguna ejecución programada en toda la historia de la instancia?):

```sql
SELECT mode, status, COUNT(*) AS n
FROM execution_entity
GROUP BY mode, status
ORDER BY mode, status;
```

Salida real:

```
mode   | status  | n
-------+---------+--
manual | error   | 5
manual | success | 4
(2 filas)
```

Consulta literal (conteo de ejecuciones no manuales):

```sql
SELECT COUNT(*) FROM execution_entity WHERE mode != 'manual';
```

Salida real:

```
0
```

| Punto | Estado verificado al 2026-09-25 15:07 |
|---|---|
| Ejecuciones de la instancia con `mode = manual` | **9 de 9** (5 `error` + 4 `success`). Ninguna excepción |
| Ejecuciones con `mode` distinto de `manual` en toda la historia | **0** |
| Origen de los 33 posts de la ventana | La ejecución **9** (manual). Corroborado desde `tesi_osint`: los 33 posts tienen `ingested_at` dentro del segundo `2026-09-25 17:55:43 UTC`, dentro de la ventana `17:55:35.332` → `17:55:43.715` de esa ejecución ([Q-C8] del archivo de psql) |
| Primera ingesta **PROGRAMADA** | **PENDIENTE al cierre de esta pasada.** Ocurre dentro de los **15 minutos** siguientes a la publicación del workflow. No hay ninguna ejecución programada registrada que la contradiga: el conteo es 0 |
| Por qué era esperable | Un `Schedule` de 15 minutos recién publicado no puede haber producido ticks anteriores a su publicación. La primera ingesta programada es consecuencia de la publicación, no un hecho pasado |

**Por qué esta distinción es metodológica y no un detalle de forma:** un `n` de posts recolectado
por una ejecución manual prueba que el pipeline funciona; uno recolectado por el trigger programado
es lo que sostiene la continuidad de la ventana. Presentarlos como la misma cobertura falsearía la
continuidad de la ventana B5. La entrada de bitácora del día lo declara en su §5 y en el detalle
del operador, y por eso el número **no** se lee como "el día recolectó 33 posts de forma sostenida".

#### 10.2.4 Estado de la limitación conocida de la tarea 3.5

La §6 de la 1ª pasada ("el log de ejecuciones no se conserva") queda **actualizada, no borrada**:

| Punto de la §6 | Estado al 2026-09-25 15:07 |
|---|---|
| ¿Está disponible el log de ejecuciones? | **Sí**, mientras la instancia n8n esté levantada y su directorio de datos local sea legible. Consulta en modo `mode=ro` |
| ¿Entonces la limitación 1 ("el éxito o fracaso no puede probarse desde el log")? | **Resuelta para el 2026-09-25**: el log existe y se transcribió (§10.2.2). El `0` de posts de la 1ª pasada, que era indistinguible entre "no se ingirió" y "no se ejecutó", **ahora se explica**: la instancia estaba caída, no la ingesta |
| ¿Entonces la limitación 2 ("cuando el log esté disponible, se transcribe manualmente")? | **Se aplicó**: la transcripción es manual y quedó declarada como tal (D-3) |
| ¿La limitación desaparece? | **No.** Sigue vigente en su forma real: el log de n8n **no se versiona ni se preserva** en el repositorio. Vive en el directorio de datos local de la instancia, que es volátil. Si ese directorio se pierde o se reinstala, el histórico de ejecuciones de la ventana se pierde con él. La evidencia de cada día queda en la transcripción archivada con su fecha, que es la única copia durable |
| Consecuencia de diseño | Se mantiene la deuda consciente de §6: automatizar la captura implicaría tocar el workflow, congelado en este change (D-8) |

### 10.3 Tarea 3.3 — para el 2026-09-25 **ya no aplica**; la regla se conserva

La tarea 3.3 exige marcar `sin observación` **cuando no hay log**. Para el 2026-09-25 **hay log** y
hay ejecución observada:

| Punto | Estado al 2026-09-25 15:07 |
|---|---|
| ¿Hay observación para el 2026-09-25? | **Sí**: ejecución `id 9`, `status = success`, `finished = 1`, transcrita en §10.2.2 y en la entrada de bitácora del día |
| Estado de las ejecuciones del 2026-09-25 en la bitácora | **`observadas`**: 1 ejecución, `success`, 0 fallidas. **Ya no es `sin observación`** |
| ¿Se mantienen las 201 de B4 y el `n = 0` de la 1ª pasada como estado actual? | **No.** Quedan como el registro histórico de un estado de instancia distinto (§10.5) |

> **La regla de 3.3 sigue vigente para los días futuros, sin excepción:** cuando el log de
> ejecuciones no esté disponible para una fecha, esa ejecución se marca **`sin observación`** y
> **nunca** como exitosa. Asumir éxito sin log sería fabricar un dato (RN-GL-01). El 2026-09-25 no
> cae en ese caso porque el log estuvo disponible.

Para que esa regla no dependa de que alguien recuerde escribirla, el script de bitácora la
implementa: el estado de n8n es un parámetro **declarado por el operador** y su valor por defecto es
`no_observado`, que produce literalmente **"no observado en la generación de esta entrada"**. El
script no consulta la base de n8n, no deduce el estado y **no tiene forma de asumir un éxito**.

### 10.4 Tarea 3.4 — cobertura de la bitácora y cifras del día

| Campo | Valor | Origen |
|---|---|---|
| Inicio de la ventana | `2026-09-25` | `VENTANA_B5.md` §1 |
| Fecha de esta re-verificación | `2026-09-25` | — |
| Días transcurridos | **1** (el día de inicio, **aún no cerrado**) | — |
| Entradas de bitácora existentes | **1** → [`bitacora_b5/2026-09-25.md`](bitacora_b5/2026-09-25.md) | script `V4/scripts/bitacora_b5.py` |
| Días faltantes de bitácora | **Ninguno** | — |
| `n` de posts dentro de la ventana al cierre de esta pasada | **33** | [Q-C1] |
| `n` acumulado en la ventana | **33** (la ventana arrancó hoy, no pasó ningún día completo) | [Q-C1b] |
| `n` de posts en la base completa | **234** = 201 de B4 + 33 de la ventana | [Q-C3] |
| Distribución **dentro** de la ventana | `r/argentina` **33**, `r/devsarg` **0**, `r/derechogenial` **0** | [Q-C2] |
| Distribución **acumulada** en la base | `r/argentina` **134**, `r/devsarg` **100**, `r/derechogenial` **0** | [Q-C2b] |
| Filas en `anomalias` | **0** | [Q-C3] |
| Escrituras realizadas por esta re-verificación | **0** (solo `SELECT` y SQLite en `mode=ro`) | §10 |

> **Las dos distribuciones no se intercambian.** La que describe la ventana B5 es 33 / 0 / 0; la que
> describe toda la base es 134 / 100 / 0. Confundirlas cambiaría el denominador del desglose de la
> ventana y es exactamente el error que RN-GL-02 busca evitar.

> **`n = 33` es un corte a mitad de día, no un total de día cerrado.** El día no había terminado al
> cierre de esta pasada y la recolección programada sigue pendiente, así que el número va a crecer.
> La entrada de bitácora del día lo declara en su §1 y lo repite en su §6.

> **El `0` de `r/devsarg` dentro de la ventana no tiene causa atribuida.** La causa **no es observable
> desde `tesi_osint`**: no se puede distinguir entre "el feed no traía posts nuevos" y "el feed
> falló". Queda como observación, no como falla. El `0` histórico de `r/derechogenial` **sí** tiene
> causa verificada (rate limiting de Reddit del 2026-09-24) y está documentado aparte.

### 10.5 Qué se conserva de la 1ª pasada

| Registro de la 1ª pasada | Estado |
|---|---|
| §1 — PostgreSQL arriba en `localhost:5433` | **Vigente**, sin cambios |
| §2 — n8n no verificable | **Supersedido** por §10.1. Se conserva el texto: era la conclusión honesta con la información disponible |
| §3 — no hay log que transcribir | **Supersedido** por §10.2. Se conserva el texto |
| §4 — ejecuciones del día `sin observación` | **Supersedido** por §10.3. Se conserva el texto |
| §5 — `n = 0` del día, 201 posts de B4 | **Histórico.** Ya no es el estado actual (33 y 234), pero es el registro exacto de la instancia caída |
| §6 — limitación de no preservación del log | **Actualizada** por §10.2.4, no borrada: la versión vigente es "el log existe mientras la instancia esté viva, pero no se versiona" |
| §7 — suficiencia 0 de 10, 6.5 bloqueada | **Vigente**, sin cambios (ver §10.6) |
| §8 — estado de la base | **Actualizada**: 201 → 234 posts; 0 → 33 posts en la ventana. La conserve el resto igual |

### 10.6 Tarea 6.5 — estado de suficiencia: **NO cambia, sigue bloqueada al 2026-09-25**

| Métrica de suficiencia | Valor | Origen |
|---|---|---|
| Días completos evaluados en `anomalias` dentro de la ventana B5 | **0** | [Q-C3] de este documento y [Q-D1] de [`psql_2026-09-25_suficiencia_anomalias.txt`](psql_2026-09-25_suficiencia_anomalias.txt) |
| Umbral de suficiencia (D-6, base comparativa de RN-AN-02) | **10** | criterio declarado, no medido |
| Estado | **0 de 10 → 0 % del umbral** | consultable, no estimado |
| Estado de la ventana | **ABIERTA** | no alcanza el criterio de §4 de [`VENTANA_B5.md`](VENTANA_B5.md) |
| Primera evaluación diaria esperada | **`2026-09-26` a las 00:05** `America/Argentina/Buenos_Aires` | el motor de anomalías corre a las 00:05 y evalúa la ventana de ayer |
| Proyección de acumulación | Con un día de evaluaciones por noche, el umbral de 10 días se alcanzaría hacia el **día 12** de la ventana. **Proyección declarada, no medida** | `VENTANA_B5.md` §4, nota operativa |

**Lo que la publicación del workflow NO cambia:** que ahora haya recolección **no** acelera la
suficiencia. El criterio de 1.3 mide **días completos de evaluaciones** en `anomalias`, y la tabla
sigue vacía. Haber publicado el workflow habilita las evaluaciones futuras; no produce ninguna por
sí solo.

**Estado de las tareas de decisión al 2026-09-25 15:07:**

| Tarea | Estado | Motivo |
|---|---|---|
| **6.1** — fijar la fecha de corte | **ABIERTA** | Suficiencia 0/10 y decisión de los autores con sus directores |
| **6.2** — conservar o reiniciar la recolección | **ABIERTA** | Decisión de los autores. La recolección ahora está activa, lo que **reduce** el costo de conservarla, pero no decide por los autores |
| **6.3** — incluir o excluir los posts previos al 2026-09-25 | **ABIERTA** | Decisión de los autores. Por defecto los 201 posts de B4 quedan **fuera** del corpus |
| **6.5** — confirmar la suficiencia antes de 6.1 | **BLOQUEADA** | Suficiencia **0 de 10**. No se cumple la condición previa |

**Ninguna de las cuatro se marca como cumplida en esta pasada.** Ninguna es una decisión técnica y
esta re-verificación no las toca.
