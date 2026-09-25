# Ventana de recolección B5 — definición real

> Change OpenSpec: `ventana-recoleccion-b5` (C-05). Decisiones: D-1, D-5, D-6, D-7.
> Documento de evidencia, no de resultados: acá no se declara ninguna métrica de resultados,
> solo el contorno de la ventana y el estado de su acumulación (RN-GL-01).

## 1. Identificación de la ventana

| Campo | Valor |
|---|---|
| Identificador de la ventana | **B5** |
| Fecha de inicio | **2026-09-25** (fija, inmutable) |
| Fecha de corte | **`no fijada`** — decisión abierta de los autores con sus directores (ver §3) |
| Duración | No declarada: depende de la fecha de corte, que todavía no existe |
| Zona horaria de los límites | `America/Argentina/Buenos_Aires` (zona de ejecución del sistema) |
| Bitácora diaria | [`V4/evidencias/bitacora_b5/`](bitacora_b5/) — una entrada `YYYY-MM-DD.md` por día |
| Criterio de suficiencia | 10 días completos de evaluaciones en `anomalias` (ver §4) |
| Estado al redactar este documento | **ABIERTA** — 0 de 10 días completos evaluados |

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
