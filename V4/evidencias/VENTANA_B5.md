# Ventana de recolección B5 — definición real

> Change OpenSpec: `ventana-recoleccion-b5` (C-05). Decisiones: D-1, D-5, D-6, D-7.
> Documento de evidencia, no de resultados: acá no se declara ninguna métrica de resultados,
> solo el contorno de la ventana y el estado de su acumulación (RN-GL-01).

## 1. Identificación de la ventana

| Campo | Valor |
|---|---|
| Identificador de la ventana | **B5** |
| Fecha de inicio (primer intento, **abortado**) | 2026-09-25 — ver §7.1. La recolección se interrumpió y los datos se descartaron |
| Fecha de reinicio del corpus | **2026-10-01 13:05:59** (`America/Argentina/Buenos_Aires`) — `TRUNCATE` de `posts`, `comments`, `anomalias`, `alertas` |
| **Fecha de inicio operativa** | **2026-10-01 13:15:12** (`America/Argentina/Buenos_Aires`) — instante de la **ejecución automática #15**, la primera que corrió con el workflow publicado tras el reinicio. Es la fecha que define la ventana |
| Fecha de corte | **`no fijada`** — decisión abierta de los autores con sus directores (ver §3) |
| Duración | 10 días desde el inicio operativo, y 11 en total si se cuenta el día evaluado del motor de anomalías (§4) |
| Zona horaria de los límites | `America/Argentina/Buenos_Aires` (zona de ejecución del sistema) |
| Bitácora diaria | [`V4/evidencias/bitacora_b5/`](bitacora_b5/) — una entrada `YYYY-MM-DD.md` por día |
| Criterio de suficiencia | 10 días completos de evaluaciones en `anomalias` (ver §4) |
| Estado al redactar este documento | **ABIERTA** — 0 de 10 días completos evaluados |

> **Por qué el inicio es 13:15:12 y no 13:05:59.** El `TRUNCATE` vació las tablas a
> las 13:05:59, pero el workflow seguía sin publicar en ese momento: la recolección
> no había empezado. El primer disparador de `Schedule Ingesta` corrió a las
> 13:15:12 (ejecución `#15`, `mode = trigger`, `status = success`) y los primeros
> posts quedaron con `ingested_at` entre 13:15:43 y 13:16:49. Tomar el corte del
> `TRUNCATE` daría una ventana con minutos sin datos, que no es lo que el sistema
> recolectó. El disparador no acumula intervalos perdidos: `Schedule Ingesta`
> corre cada 15 minutos alineados al reloj y no recupera las corrida perdidas
> mientras el workflow estuvo inactivo.

## 2. Criterio del corpus

El corpus de la ventana B5 es **exactamente el conjunto de filas de `posts` cuyo
`ingested_at` cae dentro del rango de la ventana**:

```text
ingested_at >= 2026-09-25 00:00:00 (America/Argentina/Buenos_Aires)
ingested_at <  <fecha de corte> 00:00:00
```

Mientras el corte sea `no fijada`, el límite superior aplicado por el script de bitácora es el
**instante de ejecución** de la consulta, y así queda anotado en la cabecera de cada entrada.

**Por qué `ingested_at` y no `created_utc`** (D-1): `ingested_at` es la evidencia de lo que el
sistema efectivamente recolectó; `created_utc` es la fecha de publicación en Reddit e incluye
posts que el sistema nunca vio. Es además el mismo campo que usa C-08 para E6, de modo que
latencia, Tabla 3 y E7 comparten un único criterio de ventana y no dos.

## 3. Fecha de corte: `no fijada` (decisión abierta)

| Campo | Valor |
|---|---|
| Estado | **`no fijada`** |
| Motivo | Es una decisión de los **autores con sus directores**, no una decisión técnica. Fijarla desde la ejecución sería inventar un parámetro de investigación. |
| Tarea que la cierra | **6.1** de este change (`decision-cierre-ventana`) |
| Changes que dependen del corte | C-08 → C-09 → C-20 → C-21 → C-23 |
| Fecha tentativa propuesta | **Ninguna.** No existe en este documento ni en los demás artefactos del change. |

Al cerrarse, la tarea 6.1 debe registrar en este archivo: la fecha, el responsable, la fecha de
la decisión, el motivo y los changes que habilita (RN-GL-03).

Un campo de fecha en blanco podría leerse más adelante como un olvido; por eso el valor es el
estado explícito `no fijada` con su motivo, y no un espacio vacío.

## 4. Criterio de suficiencia (10 días completos evaluados)

La ventana se declara **suficiente** cuando el motor de anomalías tiene **10 días completos de
evaluaciones** registrados en `anomalias`.

**Justificación**: no es un número elegido para la ocasión. RN-AN-02 define la base comparativa
como la media diaria de los **diez días previos**; sin esa historia la base comparativa no
existe, y toda evaluación previa al umbral se haría contra una base incompleta. Un umbral
menor daría evaluaciones con base incompleta; uno mayor retrasaría el cierre sin ganancia.

**Estado consultable, no estimado** (tarea 2.4): el script `V4/scripts/bitacora_b5.py` cuenta
los días completos evaluados con una consulta `SELECT` sobre `anomalias`, agrupada por
`ventana_fin`, y lo escribe en la sección 4 de cada entrada de bitácora:

```sql
SELECT (ventana_fin AT TIME ZONE 'America/Argentina/Buenos_Aires')::date AS dia,
       COUNT(*) AS n_evaluaciones
FROM anomalias
WHERE ventana_fin >= TIMESTAMPTZ '2026-09-25T00:00:00-03:00'
  AND ventana_fin <  TIMESTAMPTZ '<instante de ejecución>'
GROUP BY (ventana_fin AT TIME ZONE 'America/Argentina/Buenos_Aires')::date
ORDER BY dia;
```

**Nota operativa**: el motor de anomalías corre a las 00:05 y evalúa la ventana de ayer, así que
las primeras evaluaciones con base completa aparecen hacia el **día 12** de la ventana.

**Antes del umbral, la ventana se declara abierta** y el estado se reporta como **limitación de
la base comparativa**, nunca como ausencia de anomalías (RN-AN-06).

## 5. Los 201 posts de B4 (2026-09-24) quedan fuera del corpus

La corrida B4 del **2026-09-24** dejó **201 posts verificados** en `tesi_osint`
(`r/argentina` 101, `r/devsarg` 100, `r/derechogenial` 0 por rate limiting). Todos tienen
`ingested_at` del 2026-09-24, es decir **un día antes del inicio de la ventana**.

| Punto | Estado |
|---|---|
| ¿Pertenecen al corpus B5? | **No**, por el criterio de `ingested_at` de §2 |
| Motivo | El corpus pre-B5 no es la ventana: son evidencia de la corrida técnica y de la caracterización del rate limiting, no del período recolectado de la ventana (D-1) |
| Excepción | **Solo si los autores lo deciden** (tarea **6.3**). Es un cambio de alcance y debe registrarse con su motivo y su efecto sobre las métricas publicadas; no se aplica como ajuste silencioso de una consulta |
| Estado de la decisión | Abierta (6.3). Por defecto quedan fuera. |

Los 201 posts **se conservan** en la base y se los sigue usando como evidencia técnica de B4 y
como caso verificado de rate limiting (ver
[`CARACTERIZACION_RATE_LIMIT.md`](CARACTERIZACION_RATE_LIMIT.md)).

## 6. Reglas de desglose por subreddit (D-5, RN-GL-02)

Estas reglas gobiernan **todo** desglose por subreddit producido dentro de la ventana:

1. **Denominador completo.** Todo desglose o porcentaje por subreddit usa como denominador los
   **tres subreddit monitorizados** del alcance — `r/argentina`, `r/devsarg`, `r/derechogenial` —
   **incluidos los que aportan 0**. Nunca se calcula sobre el subconjunto que sí aportó posts.
2. **El cero entra en la tabla.** Los tres subreddits aparecen siempre con su recuento real,
   incluido el `0`, y con la causa declarada cuando el cero proviene del rate limiting.
3. **Cada desglose declara su `n`.** Toda cifra va acompañada de su `n` de observaciones, de la
   consulta que la produjo, de la fecha de ejecución y de la ventana (RN-GL-01).
4. **Sin completados.** Ningún porcentaje se completa con datos de fuentes ajenas al sistema, ni
   con datos de V2/V3, ni con tasas supuestas (RN-GL-02).
5. **Sesgo reportado, no compensado.** La cobertura por subreddit está **sesgada por el rate
   limiting** de Reddit. El sesgo se declara como **limitación** en el Capítulo 5 y en
   [`CARACTERIZACION_RATE_LIMIT.md`](CARACTERIZACION_RATE_LIMIT.md); no se compensa con
   reasignaciones, con fuentes externas ni desactivando subreddits.
6. **Ningún subreddit se desactiva para maquillar la cobertura.** Un subreddit habilitado que no
   aporta datos permanece con `active_monitoring = true` y su ausencia se reporta con su causa.

## 7. Estado de la acumulación al redactar este documento

> **Actualizado 2026-09-25 (re-verificación de instancia).** Este documento se redactó cuando n8n
> estaba caída y la ventana tenía `n = 0`. Al cierre de la pasada de las 15:07 la recolección
> **está activa**: el workflow fue publicado ese mismo día. La tabla de abajo refleja el estado
> vigente. El `n = 0` inicial queda como registro histórico de un estado de instancia distinto, en
> [`VERIFICACION_INSTANCIA_2026-09-25.md`](VERIFICACION_INSTANCIA_2026-09-25.md) §2, §4 y §10.

**Estado de la recolección: ACTIVA.** Workflow `TFIOsintV4Monitor01` **publicado** el 2026-09-25
(`active = 1`, `versionId` `abe9e78c-4854-4243-b2ea-58dbc4a57a9f`).

### 7.1 Incidente del 2026-09-26: interrupción de la recolección y motor de anomalías roto

> **Actualizado 2026-09-26.** La tabla de §7 (abajo) queda como el registro de la pasada de las
> 15:07. Este bloque es el estado **posterior** y el que describe el corte real de la ventana.

La recolección del 2026-09-25 **no cubrió el día entero**: se detuvo a las **16:00:05** hora local
(`max(ingested_at) = 2026-09-25 16:00:05-03`) y no se restableció hasta la corrección del
2026-09-26. El día queda declarado **parcial**.

Cronología, con el identificador de ejecución de n8n como evidencia:

| Momento (local) | Ej. | Qué pasó | Causa |
|---|---|---|---|
| 14:55:43 | 9 | 33 posts de `r/argentina` (ejecución **manual**, no programada) | — |
| 15:30 → 16:00 | 10–14 | 3 posts más; los ticks **programados** de 15 min funcionaron | — |
| 23:30 | 15 | `Connection refused ::1:5433` en `Upsert Subreddits` | PostgreSQL caído; los nodos Postgres **no tienen `retryOnFail`** |
| 00:00:01 (26/9) | 26 | `Module 'crypto' is disallowed` en `HMAC Anonymize` | instancia arrancada con `n8n start` **sin las variables de entorno** |
| 00:01:39 / 00:01:46 | 27 / 28 | 27 error; 28 **`success` con 0 posts** | los 3 feeds devolvieron **HTTP 429** y `Fetch Posts RSS` tiene `continueOnFail` |
| 00:05:43 | 29 | `no existe la función json_to_recordset(jsonb)` en `Registrar Anomalias y Alertas` | **bug del workflow**, dos veces |

**El motor de anomalías nunca escribió una sola fila.** La tabla `anomalias` tiene 0 registros y
`anomalias_id_seq.last_value = 1`: la secuencia nunca avanzó, o sea que el `INSERT` no llegó a
ejecutarse ni una vez. El criterio de suficiencia de 10 días completos (`dias_completos_evaluados`)
estaba **estructuralmente inalcanzable** mientras el SQL fuera incorrecto.

El bug sobrevivió porque el trigger de las 00:05 **nunca se había ejecutado** antes: la ventana
arrancó el 2026-09-25 y la instancia estuvo caída en todos los 00:05 previos. La primera ejecución
posible lo destapó. Eran **dos** defectos encadenados en el mismo statement:

1. `json_to_recordset` solo tiene la firma `(json)`; para `jsonb` la función se llama
   `jsonb_to_recordset`.
2. `*to_recordset` exige un **array** JSON en el nivel superior, y el nodo liga `$1` a
   `JSON.stringify($json)`, que es un objeto suelto → `no se puede invocar ... en un no-array`.

Corregido en `V4/scripts/generar_workflow.py` y revalidado con `PREPARE` sobre PostgreSQL 18
(resuelve y planifica sin ejecutar). **Pendiente: reimportar el workflow y reasignar la credencial
Postgres.** La rotación de clave HMAC y el reinicio con variables quedan en
[`ROTACION_HMAC_2026-09-26.md`](ROTACION_HMAC_2026-09-26.md).

Estado de la base al cierre del 2026-09-26 00:40:

| Métrica operativa | Valor | Origen |
|---|---|---|
| Día `2026-09-25` (cerrado) | `n = 36`, **parcial** (cubre 14:55–16:00) | `SELECT` acotado por día local; [`bitacora_b5/2026-09-25.md`](bitacora_b5/2026-09-25.md) regenerado al cierre del día |
| Posts en la base completa | **237** = 201 (B4, 24/9) + 36 (ventana) | `SELECT` de solo lectura |
| Último post ingerido | `2026-09-25 16:00:05-03` | `max(ingested_at)` |
| Distribución acumulada | `r/argentina` 137, `r/devsarg` 100, `r/derechogenial` 0 | `SELECT` con join a `subreddits` |
| `anomalias` / `alertas` | **0 / 0**, `anomalias_id_seq.last_value = 1` | `SELECT` de solo lectura |
| Días completos evaluados | **0 / 10** | script `V4/scripts/bitacora_b5.py` |

| Métrica operativa | Valor al cierre de la pasada del 2026-09-25 15:07 | Origen |
|---|---|---|
| Estado de la recolección | **Activa** — workflow publicado (`active = 1`) el 2026-09-25 | `SELECT` de solo lectura sobre la base de n8n, `mode=ro` — [`n8n_2026-09-25_estado_y_ejecuciones.txt`](n8n_2026-09-25_estado_y_ejecuciones.txt) |
| Entradas de bitácora | **1** → [`bitacora_b5/2026-09-25.md`](bitacora_b5/2026-09-25.md) | script `V4/scripts/bitacora_b5.py` |
| `n` de posts dentro de la ventana al cierre de esta pasada | **33** | `SELECT` sobre `posts` acotado por `ingested_at >= 2026-09-25T00:00:00-03:00` — [Q-C1] de [`psql_2026-09-25_ventana_b5_dia_2026-09-25.txt`](psql_2026-09-25_ventana_b5_dia_2026-09-25.txt) |
| Posts acumulados en la ventana | **33** (la ventana arrancó hoy; no pasó ningún día completo) | `SELECT` sobre `posts` acotado por `ingested_at` — [Q-C1b] del mismo archivo |
| Posts en la base completa | **234** = 201 de la corrida B4 del 2026-09-24 + 33 de la ventana | [Q-C3] del mismo archivo |
| Distribución **dentro** de la ventana | `r/argentina` **33**, `r/devsarg` **0**, `r/derechogenial` **0** (denominador: los 3 monitorizados) | [Q-C2] del mismo archivo |
| Distribución **acumulada** en la base | `r/argentina` **134**, `r/devsarg` **100**, `r/derechogenial` **0** | [Q-C2b] del mismo archivo. **No** es la distribución de la ventana |
| Primer ciclo **programado** | **Pendiente**: ocurre dentro de los 15 minutos de publicado el workflow. Al cierre de esta pasada el log de n8n registra **0** ejecuciones con `mode` distinto de `manual` | [§3] de [`n8n_2026-09-25_estado_y_ejecuciones.txt`](n8n_2026-09-25_estado_y_ejecuciones.txt) |
| Días completos evaluados | **0 de 10** | `SELECT` sobre `anomalias` agrupado por `ventana_fin` — §4 de la entrada de bitácora |
| Primera evaluación diaria esperada | `2026-09-26` a las 00:05 | el motor de anomalías evalúa la ventana de ayer |
| Estado de la ventana | **ABIERTA** | no alcanza el criterio de suficiencia de §4 |

> **`n = 33` es un corte a mitad de día, no un total de día cerrado.** El día `2026-09-25` no había
> terminado al cierre de esta pasada y el ciclo programado seguía pendiente, así que el número va
> a crecer. Lo que ese `33` afirma es "cuánto había recolectado al instante de la pasada".

> **Los 33 posts provienen de una ejecución MANUAL, no programada.** La única ejecución del día en
> el log de n8n es la `id 9` con `mode = manual`: la disparó el operador desde la UI con *Execute
> workflow*, y no un tick del trigger de 15 minutos. Prueba que el pipeline funciona; **no** es
> todavía evidencia de recolección sostenida. Esa distinción está declarada en la §5 de la entrada
> de bitácora del día y en el §10.2.3 del documento de verificación de instancia.

> **El `0` de `r/devsarg` dentro de la ventana no tiene causa atribuida:** no es observable desde
> `tesi_osint`, que no registra ni las respuestas de Reddit ni el log de n8n. No se puede distinguir
> entre "el feed no traía posts nuevos" y "el feed falló", así que queda como observación y **no**
> como falla. El `0` histórico de `r/derechogenial` sí tiene causa verificada y documentada — el
> rate limiting de Reddit del 2026-09-24 — en
> [`CARACTERIZACION_RATE_LIMIT.md`](CARACTERIZACION_RATE_LIMIT.md).

> **Sobre el campo de ejecuciones de la bitácora.** La fuente de verdad de "ejecuciones fallidas y
> su causa" es el **log de ejecuciones de la instancia n8n** (D-3). Para el 2026-09-25 el log estuvo
> disponible y su transcripción **manual** quedó registrada en la entrada del día. Para cualquier
> fecha en la que el log no esté disponible, el estado se declara `no observado`: el script de
> bitácora no deduce ni asume un resultado, y su valor por defecto no puede ser un éxito
> (RN-GL-01).

## 8. Documentos relacionados

| Documento | Qué aporta |
|---|---|
| [`bitacora_b5/`](bitacora_b5/) | Evidencia día por día de lo recolectado y de lo no observable |
| [`VERIFICACION_INSTANCIA_2026-09-25.md`](VERIFICACION_INSTANCIA_2026-09-25.md) | Estado verificable de la instancia por día, con las dos pasadas del 2026-09-25 y qué quedó supersedido |
| [`n8n_2026-09-25_estado_y_ejecuciones.txt`](n8n_2026-09-25_estado_y_ejecuciones.txt) | Salida SQLite de solo lectura: workflow publicado (`active = 1`), `versionId` y log de ejecuciones con su `mode` manual vs programado |
| [`psql_2026-09-25_ventana_b5_dia_2026-09-25.txt`](psql_2026-09-25_ventana_b5_dia_2026-09-25.txt) | Salida de psql con los conteos vigentes de la ventana y las dos distribuciones (dentro de la ventana vs acumulada) |
| [`CARACTERIZACION_RATE_LIMIT.md`](CARACTERIZACION_RATE_LIMIT.md) | Comportamiento observado de Reddit ante el exceso de requests y su efecto en la cobertura |
| `V4/scripts/bitacora_b5.py` | Generador de la bitácora (solo lectura) |
| `openspec/changes/ventana-recoleccion-b5/design.md` | Decisiones D-1 a D-8 que gobiernan este documento |
| `openspec/changes/ventana-recoleccion-b5/specs/decision-cierre-ventana/spec.md` | Requisitos de la decisión de cierre, abierta (tareas 6.1 a 6.5) |

## 9. Registro de arranque de la ventana operativa (2026-10-01)

Bitácora del reinicio del corpus y del comienzo efectivo de la recolección.

| HORA (Buenos Aires) | HECHO | VERIFICADO POR |
|---|---|---|
| 13:05:59 | `TRUNCATE posts, comments, anomalias, alertas RESTART IDENTITY` ejecutado. `subreddits` intacta con sus 6 filas | salida de `V4/scripts/reset_ventana.py` |
| 13:15:12 | Ejecución automática `#15` (`mode = trigger`, `status = success`). **Inicio operativo de la ventana** | SQLite de n8n, tabla `execution_entity` |
| 13:15:43 | Primer `ingested_at` de la ventana, en `r/netsec` | consulta sobre `posts` |
| 13:16:16 | Primer `ingested_at` en `r/Malware` | ídem |
| 13:16:49 | Primer `ingested_at` en `r/devsarg` | ídem |

Primera corrida, verificada a las 13:17:

```sql
SELECT s.display_name, COUNT(*) AS n,
       MIN(p.ingested_at AT TIME ZONE 'America/Argentina/Buenos_Aires') AS primero
FROM posts p JOIN subreddits s ON s.id = p.subreddit_id
GROUP BY s.display_name ORDER BY s.display_name;
```

```
 r/devsarg  | 100 | 2026-10-01 13:16:49.358551
 r/Malware | 100 | 2026-10-01 13:16:16.508202
 r/netsec   | 100 | 2026-10-01 13:15:43.944968
```

**300 posts en la primera corrida.** El volumen inicial no indica el ritmo de la
ventana: el feed Atom devuelve las publicaciones recientes de cada comunidad, no
solo las publicaciones nuevas. El ritmo sostenido se observa a partir del
segundo día.

### Estado de la instancia al arrancar

- Contenedores `tfi-n8n` (n8n 2.40.6) y `tfi-postgres` (PostgreSQL 18) levantados.
- Workflow `KkotjSD5uO4CXI4D` **publicado**: `active = 1`, `activeVersionId = 564b10c4-680d-4369-a292-e542b813b1ea`.
- 16 nodos. `Schedule Ingesta` y `Schedule Anomalias` habilitados; único nodo
  deshabilitado: `Send Telegram Alert`, sin credenciales disponibles.
- En n8n 2.x el control de ejecución programada es el botón **Publish**, no un
  toggle **Active** como en la 1.x. Publicar fija `activeVersionId`.

### Incidencia durante el arranque

El primer intento de `reset_ventana.py` **falló y no borró nada**: el `TRUNCATE`
omitía la tabla `comments`, que referencia `posts` por clave foránea, y
PostgreSQL revierte la sentencia entera. Se corrigió el script para descubrir
las tablas hijas por FK desde `pg_constraint` en lugar de hardcodear la lista, y
verificar que cada una quede en cero. La segunda ejecución sí completó.

## 10. Cambio declarado dentro de la ventana: evaluacion de anomalias al mediodia

**2026-10-01, ~17:00 Buenos Aires.** Ventana en curso, 4 horas de recolección. Motivo: la
máquina que corre la instancia **no está encendida de noche**, así que el trigger de las
`00:05` se perdía todos los días y la tabla `anomalias` no llenaba nunca.

### Qué cambió

| | Antes | Después |
|---|---|---|
| `Schedule Anomalias` | `00:05` | **`12:05`** |
| `Registrar Anomalias y Alertas` | `INSERT` directo | **`INSERT` idempotente** (guardia `NOT EXISTS`) |
| `Schedule Ingesta` | cada 15 min | **cada 15 min, sin cambios** |
| `Anomaly Engine` | Poisson + `MIN_ABS = 3` | **sin cambios** |
| Versión publicada | `564b10c4-680d-4369-a292-e542b813b1ea` | **`cfa84977-223a-460e-87a1-5bf0e5557699`** |

El texto íntegro de los 4 nodos Postgres y las 2 credenciales se preservaron; verificado en
la instancia: 16 nodos, 14 conexiones, 4/4 nodos con `Postgres account`.

### Por qué el horario no altera el resultado

La ventana que evalúa el trigger no depende de la hora de ejecución. `Query Daily Counts`
la calcula con `date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires')`, o
sea **siempre el día calendario `[00:00, 00:00)` de ayer**. A las `12:05` ese día ya está
cerrado y el resultado es idéntico al que daría a las `00:05`. Cambiar la hora no cambia
ni el período evaluado ni los conteos ni el umbral.

### Por qué el candado `NOT EXISTS`

`anomalias` **no tiene restricción de unicidad** sobre `(ventana_inicio, ventana_fin,
categoria)`; solo la clave primaria por `id`. Sin el guardia, ejecutar el nodo dos veces el
mismo día inserta la misma evaluación dos veces y `dias_completos_evaluados` —que cuenta
filas por día— queda inflado. Con el guardia, relanzar el nodo a mano para recuperar un
día perdido no duplica nada, y tampoco se generan alertas repetidas porque el `INSERT` de
`alertas` sale de la CTE `ins`, que queda vacía si la evaluación ya existía.

Probado sobre la base antes de publicar, dentro de una transacción revertida: tres
ejecuciones consecutivas de la misma ventana y categoría dieron **1 fila y 1 alerta**; una
categoría distinta en la misma ventana se insertó normal. La base quedó en
`anomalias=0, alertas=0` tras el `ROLLBACK`.

### Incidencia durante la aplicación

La primera importación **agregó** una segunda cadena de 16 nodos con sufijo `1` en lugar de
reemplazar: el workflow quedó con 32 nodos. Se detectó antes de publicar (la versión de 32
nodos `f4369d88` nunca llegó a activarse). Se resolvió borrando los 32 nodos y reimportando
sobre el lienzo vacío. **Si se hubiera publicado, habrían corrido dos `Schedule Ingesta` y
la recolección se habría duplicado.** Publicada la versión correcta, las cuatro ejecuciones
programadas siguientessiguieron con un único trigger.

### Efecto sobre la suficiencia

Ninguno en el cómputo de días: el corte de la ventana sigue siendo la primera ejecución
automática del 2026-10-01 13:15:12. Lo que cambia es la **viabilidad**: con el trigger de las
`00:05` la tabla `anomalias` no podía llenarse en esta máquina. La primera evaluación con el
horario nuevo corresponde al día completo del 2026-10-01 y debe dispararse el 2026-10-02 a
las 12:05; su ejecución queda registrada como evidencia de que el horario quedó operativo.

## 11. Corte diario del 2026-10-01 y su alcance

**2026-10-01, 19:02–19:07 Buenos Aires.** Fin de la jornada de recolección del primer día de
la ventana. El día quedó **parcial**, no cerrado.

### Qué se cortó y cómo se cortó

| HECHO | VALOR | VERIFICADO POR |
|---|---|---|
| Última ejecución programada | **`#38`**, `mode = trigger`, `status = success` | SQLite de n8n, `execution_entity` |
| Inicio de `#38` | `2026-10-01 19:00:29` (BA) | `startedAt` convertido desde UTC |
| Fin de `#38` | **`2026-10-01 19:02:05`** (BA) | `stoppedAt` convertido desde UTC |
| Último `ingested_at` | `2026-10-01 19:02:05.767799` (BA) | `max(ingested_at)` sobre `posts` |
| Ejecuciones programadas en el día | **24**, todas `success` | `execution_entity` con `mode = trigger` desde `#15` |
| Estado del workflow al cierre | **`active = 0`**, `activeVersionId = NULL` — despublicado | `workflow_entity` |
| Tick de las 19:15 | **no ocurrió** (no existe ejecución `#39`) | `max(id) = 38` |

### El corte quedó acotado a un intervalo, no a un instante

El instante exacto del **Unpublished** **no es observable**: n8n no registra la marca de la
despublicación y `workflow_entity.updatedAt` no se modifica al despublicar (su valor
`2026-10-01 17:06:28` UTC corresponde a una edición anterior de la jornada, no al corte). Lo
que sí queda acotado por evidencia es:

```text
despublicación ∈ (2026-10-01 19:02:05 BA , 2026-10-01 19:15:00 BA)
```

El cota inferior es el fin de `#38`. El superior es el tick de las 19:15, que habría
disparado `Schedule Ingesta` si el workflow hubiera seguido publicado. Dentro de ese
intervalo se observó `active = 0` a las **19:07:38** BA.

Se declara el intervalo y no un instante porque el instante no se midió. Fijar
`19:07:38` como hora de corte sería afirmar algo que la evidencia no muestra (RN-GL-01).

### Zona horaria: las marcas de n8n no están en hora local

El contenedor `tfi-n8n` corre en **UTC** y la base SQLite guarda las marcas como texto naive
en UTC. **Todas las horas de este documento se convirtieron a `America/Argentina/Buenos_Aires`
antes de anotarse.** Convertir con `.astimezone()` sobre una marca naive sin marcarla como UTC
produce un valor corrido tres horas y hace creer que la recolección terminó a las 22:02.

| Evento | Valor crudo en n8n (UTC) | En Buenos Aires |
|---|---|---|
| Inicio de `#38` | `2026-10-01 22:00:29` | `2026-10-01 19:00:29` |
| Fin de `#38` | `2026-10-01 22:02:05` | `2026-10-01 19:02:05` |
| `updatedAt` del workflow | `2026-10-01 17:06:28` | `2026-10-01 14:06:28` |

### Estado de la base al cierre de la jornada

| Métrica operativa | Valor | Origen |
|---|---|---|
| Posts en `posts` | **307** | `COUNT(*)` de solo lectura |
| Posts ingeridos el 2026-10-01 | **307** — ninguno de la corrida B4 (24/9) sobrevivió al `TRUNCATE` | `COUNT(*)` por fecha local |
| Distribución acumulada | `r/netsec` **101**, `r/Malware` **100**, `r/devsarg` **106** | `SELECT` con join a `subreddits` |
| Con señal clasificada | **112** (36,5 %) | `nlp_category <> 'No relevante'` |
| `anomalias` / `alertas` | **0 / 0** | `SELECT` de solo lectura |
| Días completos evaluados | **0 / 10** | script `V4/scripts/bitacora_b5.py` |

Sobre `anomalias = 0`: es el estado **esperado**. La primera evaluación con el horario de las
`12:05` corresponde al día completo del 2026-10-01 y se dispara el **2026-10-02 a las 12:05**,
con el equipo encendido. Mientras la ventana siga abierta, un `0` en `anomalias` es
**limitación de la base comparativa**, nunca ausencia de anomalías (RN-AN-06).

### Consecuencias para la ventana

1. **El día 2026-10-01 es parcial** por corte de jornada a las 19:02:05. Queda declarado como
   tal, no como día completo.
2. **Se abre un intervalo sin recolección** desde el corte hasta que el equipo vuelva a
   encenderse y el workflow se publique de nuevo. Los disparos perdidos **no se recuperan**:
   `Schedule Ingesta` no acumula los ticks que no llegaron a dispararse mientras el workflow
   estuvo inactivo.
3. **La reanudación es idempotente.** Republicar y volver a disparar no duplica posts: el
   `upsert` resuelve por `id` y el motor de anomalías tiene el guardia `NOT EXISTS` de §10.
4. **El corte no altera la fecha de inicio** de la ventana ni su criterio de suficiencia: sigue
   siendo `2026-10-01 13:15:12` y 10 días completos evaluados.
5. **Ningún subreddit se desactiva** para compensar el hueco. Los tres del alcance siguen con
   `active_monitoring = true` y sus ceros, si aparecen, se reportan con su causa (RN-GL-02).

### Procedimiento de reanudación

Cuando el equipo vuelva a estar disponible:

1. Levantar `tfi-postgres` y `tfi-n8n`.
2. Publicar el workflow `KkotjSD5uO4CXI4D` (**Publish**, no *Active*: en n8n 2.x el control es
   *Publish*) y verificar que siga siendo el de 16 nodos, versión
   `cfa84977-223a-460e-87a1-5bf0e5557699`, con 4/4 credenciales `Postgres account`.
3. Registrar en este documento el intervalo sin recolección y la hora de reanudación.
4. Regenerar la entrada de bitácora del día con `V4/scripts/bitacora_b5.py`.

## 12. Primera ejecucion real del motor de anomalias (2026-10-02)

**2026-10-02 12:23:39 Buenos Aires.** La tabla `anomalias` paso de 0 a 7 filas. Es la **primera
vez en toda la historia del proyecto que el motor de anomalias ejecuta e inserta**, desde que se
corregio el bug `jsonb_to_recordset` del 2026-09-26 (§7.1). Lo anterior fueron pruebas sobre
`PREPARE` y una transaccion revertida (§10); esto es una ejecucion completa en la instancia viva.

### Por que fue manual y no programada

El workflow se republico el 2026-10-02 con los contenedores recien levantados, despues de las
**12:05**. El disparador de las `12:05` no ocurrio porque la instancia no estaba en ejecucion:
la ventana horaria de las 12:05 perdio ese dia por poco mas de un minuto.

| HECHO | VALOR | VERIFICADO POR |
|---|---|---|
| Fin del intervalo sin recolección | entre 2026-10-01 19:02:05 y 2026-10-02 12:15 BA | §11 y `min(ingested_at)` del 2026-10-02 |
| Tick de las `12:05` del 2026-10-02 | **no ocurrio** | sin fila en `anomalias` anterior a las 12:23:39 |
| Reanudacion de la ingesta | **12:16:02** BA | `min(ingested_at)` del 2026-10-02 |
| Ultima ingesta verificada | `2026-10-02 12:17:06.849557` | `max(ingested_at)` |
| Posts ingeridos el 2026-10-02 al verificar | **18** | `COUNT(*)` acotado por fecha local |
| Instante de la evaluacion | **`2026-10-02 12:23:39.692033`** BA | `anomalias.created_at` |

La ejecucion fue **manual**, launched desde el nodo `Schedule Anomalias` con *Execute step*, para
no disparar la rama de ingesta. El identificador de ejecucion de n8n y su `mode` **aun no fueron
transcritos** del log: la lectura de la base SQLite de n8n exige detener el contenedor, y el
verificador se hizo a las 12:26 con el tick de las 12:30 a cuatro minutos. No se arriesga un hueco
de recoleccion por un identificador. Queda pendiente para un instante con margen.

### Lo que se registro

Siete evaluaciones, una por categoria con señal, todas sobre la ventana del **2026-10-01**.

| id | Categoria | `n_observado` | `base_media` | `umbral` | `disparo` | Alerta |
|---|---|---|---|---|---|---|
| 5 | Malware | 55 | 0,00 | 3,00 | **sí** | sí |
| 9 | Vulnerabilidades | 41 | 0,00 | 3,00 | **sí** | sí |
| 6 | Phishing | 6 | 0,00 | 3,00 | **sí** | sí |
| 7 | Ransomware | 3 | 0,00 | 3,00 | **sí** | sí |
| 4 | Infraestructura y Ataques | 3 | 0,00 | 3,00 | **sí** | sí |
| 3 | Filtracion de Datos | 2 | 0,00 | 3,00 | no | no |
| 8 | Robo de Credenciales | 2 | 0,00 | 3,00 | no | no |

La suma de `n_observado` es **112**, igual al conteo de posts con señal del 2026-10-01
(`nlp_category <> 'No relevante'`): la ventana evaluada y la ventana recolectada coinciden.

Cinco filas en `alertas`, todas con `canal = 'telegram'`, `destinatario = 'canal_tfi'` y
**`estado = 'PENDIENTE'`**. El nodo `Send Telegram Alert` está **deshabilitado** y no hay
`TELEGRAM_BOT_TOKEN` ni `TELEGRAM_CHAT_ID`, de modo que **ninguna alerta fue enviada**. El estado
`PENDIENTE` es correcto: no se affirmará que OE6 se cumplio con una alerta real (IN-04).

Los `id` arrancan en **3** y no en 1: los identificadores 1 y 2 fueron consumidos por la
transaccion revertida de la prueba de §10. Es la firma forense de que aquel test existio.

### Advertencia: estas cinco anomalias son un artefacto, NO un hallazgo

**`base_media = 0` en las siete categorias.** La base comparativa no esta en cero por la actividad
de las comunidades: esta en cero porque el `TRUNCATE` del 2026-10-01 13:05:59 borro los 201 posts
de B4. Verificado: `COUNT(*) FROM posts WHERE ingested_at < 2026-10-01` devuelve **0**.

Contra una base de cero, el umbral del motor es `max(umbral_poisson(0) + 1, MIN_ABS = 3) = 3`, de
modo que dispara toda categoria con tres o mas posts. Cinco de siete lo superan.

**Consecuencia metodologica**: `"Malware 55 contra una base de 0"` es trivialmente cierto y no
sostiene ninguna afirmacion sobre el comportamiento de `r/netsec`, `r/Malware` o `r/devsarg`. Estas
filas **no pueden presentarse como anomalias detectadas** ni como evidencia de que el sistema
detecte picos. Su valor es exclusivamente técnico: demonstrates que la cadena
`Schedule Anomalias` → `Query Daily Counts` → `Anomaly Engine` → `Registrar Anomalias y Alertas`
funciona de punta a punta en la instancia viva.

Mientras la base comparativa siga incompleta, la ventana se declara **abierta** y el estado se
reporta como **limitación de la base comparativa** (RN-AN-06). La base dejara de estar vacia a
partir de la **segunda** evaluacion, cuando el 2026-10-01 entre en la ventana de 10 dias y aporte
`112 / 10 = 11,2` como media diaria.

> **Correccion 2026-10-02.** Una version anterior de este parrafo decia "tercera evaluacion". Es
> incorrecto. La evaluacion que produjo estas siete filas ya es la **primera** (la del
> 2026-10-02 12:23:39, sobre la ventana del 2026-10-01). En la **segunda** evaluacion —la que
> evalúe el 2026-10-02— la media de los 10 dias previos ya incluye el 2026-10-01, y por lo tanto
> `base_media` deja de valer cero.

### Que queda pendiente

1. Transcribir del log de n8n el `id` y el `mode` de esta ejecucion manual.
2. Regenerar la bitacora del 2026-10-01 con `V4/scripts/bitacora_b5.py`: el dia pasa a tener una
   evaluacion registrada y `dias_completos_evaluados` pasa de 0 a **1 de 10**.
3. Verificar la primera evaluacion **programada** del 2026-10-03 a las 12:05, que evaluara el
   2026-10-02 y es la que demuestra que el horario quedo operativo en produccion.

> **Punto 1 resuelto el 2026-10-02 19:05.** Del log preservado: las ejecuciones **#40**
> (12:23:04) y **#41** (12:23:39) son las dos unicas del dia con `mode = manual`, y #41 es la que
> inserto las siete filas de `anomalias` (`created_at = 12:23:39.692033`). La #40 quedo en cero
> segundos y sin `runData` util: fue un intento previo del operador. Queda transcrito como
> **ejecucion #41, `mode = manual`**.

## 13. Cierre de la jornada 2 (2026-10-02)

**Corte de la jornada: 2026-10-02 ~19:00 BA.** El workflow fue despublicado por el operador. No es
el corte de la ventana B5, que sigue `no fijada` (§3).

| HECHO | VALOR | VERIFICADO POR |
|---|---|---|
| Ejecuciones automaticas del dia | **30** (`#39`–`#68`), todas `status = success` | log de n8n |
| Corridas completas (3/3 subreddits) | **13** | `runData.Fetch Posts RSS` = 3 pasos |
| Corridas incompletas (2/3 subreddits) | **17** | `runData.Fetch Posts RSS` = 2 pasos |
| Causa de las 17 | **HTTP 429** de Reddit en el segundo subreddit (`r/Malware`) | ver IN-08 |
| Ultima ejecucion | **#68**, 19:00:29 → 19:01:42 BA | log de n8n |
| Posts acumulados en B5 al cierre | **339** | `COUNT(*) FROM posts` |
| Posts nuevos del 2026-10-02 | **32** | bitacora `2026-10-02.md` |
| Dias completos evaluados | **1 de 10** (sin cambio: hoy no corrio el motor) | `anomalias` |

### El 429 es mas frecuente de lo que se creia

IN-08 se redacto cuando solo se habian observado **3 de 8** corridas. Con el dia completo, la
tasa real es **17 de 30 incompletas (57 %)**. La magnitud del problema se corrige a la baja en un
commit posterior (ver §14): la conclusion tecnica no cambia —el 429 corta el ciclo y la corrida
figura `success`—, pero la frecuencia es el doble de la estimada.

### Distribucion de cobertura

| Subreddit | Posts acumulados | Ultimo `ingested_at` |
|---|---|---|
| `r/devsarg` | 131 | 2026-10-02 18:47 |
| `r/netsec` | 107 | 2026-10-02 14:01 |
| `r/Malware` | 101 | 2026-10-02 12:16 |

`r/Malware` aparece con `ingested_at` congelado en las 12:16: no es que no haya collected datos, es
que **no publicó posts nuevos** y que ademas fue el subreddit que recibio el 429 en 17 de las 30
corridas. El contraste con `r/devsarg` (131 posts, activo toda la tarde) muestra que el pipeline
sigue funcionando cuando el rate limit no lo corta.

## 14. Correccion de la frecuencia del 429

Al cerrar la jornada 2 se corrijo la magnitud registrada en IN-08. Cuando esa inconsistencia se
detecto (3 de 8 corridas observadas), el dia estaba a mitad de camino. El dato correcto para el
2026-10-02 es **17 de 30 corridas incompletas**, no 3 de 8.

El cambio no altera el diagnostico ni la severidad: sigue siendo cierto que el 429 produce un item
de error que el parser descarta, que el loop se cierra y que `status` queda en `success`. Lo que se
corrige es la base sobre la cual estimar el riesgo de perder posts: con 57 % de ticks
incompletos, la probabilidad de que un subreddit activo pierda posts que caen fuera de la ventana
de ~100 entradas de Reddit ya no es marginal. Es el argumento central para priorizar el arreglo
del 429 al cierre de B5.



