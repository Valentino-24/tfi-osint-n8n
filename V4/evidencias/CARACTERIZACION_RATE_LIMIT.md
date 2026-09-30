# Caracterización del rate limiting de Reddit — observación acumulada

> Change OpenSpec: `ventana-recoleccion-b5` (C-05), tareas 4.1 a 4.5. Decisión D-4.
> Cierra el criterio pendiente de US-002 ("documentar la ventana exacta de rate limiting que se
> observe en las corridas finales"), con lo **observado**. Lo no aislado se declara como
> **no determinado**; no se estima ni se copia de documentación externa.

## 1. Comportamiento observado

| Campo | Valor |
|---|---|
| Fuente | Feeds RSS/Atom públicos de Reddit (`new/.rss`), modo Plan C |
| Síntoma | Reddit responde **HTTP 429** (Too Many Requests) ante el **exceso de requests desde la IP del proyecto** |
| Alcance del síntoma | Afecta a la descarga del feed: el subreddit habilitado puede quedar en **0 posts** en el ciclo |
| Mitigación vigente | **Reintento hasta 3 veces con hasta 5 segundos de espera** entre intentos ante 429/403, y continuación con el resto del flujo (RN-FU-03, revisada el 2026-09-30 por D-10) |
| Requests por ciclo | 3 (uno por subreddit monitorizado), ciclo de ingesta de 15 minutos |
| Umbral exacto de requests que dispara el 429 | **`no determinado`** (ver §3) |
| Efecto sobre la cobertura | Sesgo por subreddit: un subreddit habilitado puede no aportar datos (ver §4) |

**Por qué se characterizes en lugar de parametrizar** (D-4): la ventana de rate limiting es un
hecho impuesto por Reddit, no un parámetro del sistema. El sistema la registra y la reporta.

## 2. Contexto de por qué el sistema usa RSS

Los endpoints `.json` públicos de Reddit devuelven **HTTP 403 "blocked by network security"**
desde la IP del proyecto y la creación de apps está bloqueada por la *Responsible Builder
Policy* (decisión del 2026-09-24, Plan C). Por eso el pipeline consulta los feeds RSS/Atom
públicos, que **sí** aplican el rate limit por requests. Los dos comportamientos son distintos
y no deben mezclarse:

| Comportamiento | Código | Naturaleza |
|---|---|---|
| Bloqueo del endpoint `.json` | 403 | Política de acceso a la API; no es rate limiting |
| Exceso de requests sobre el feed | **429** | Rate limiting; es el objeto de esta caracterización |

## 3. Umbral que dispara el 429: `no determinado`

**Estado: `no determinado`.** No se pudo aislar con evidencia la cantidad exacta de requests por
unidad de tiempo que dispara el 429 desde esta IP.

| Lo que se sabe | Lo que no se sabe |
|---|---|
| El ciclo hace 3 requests (uno por subreddit monitorizado) | Cuántos requests seguidos se toleran antes del 429 |
| La mitigación reduce el impacto pero no elimina el síntoma | Si el límite es por request, por ventana temporal o por subreddit |
| La guía de ejecución menciona un rate limit público de referencia de ~10/min | Si ese valor de referencia es el que aplica a esta IP (no fue aislado empíricamente en este proyecto) |

El valor de referencia `~10/min` que aparece en `V4/GUIA_EJECUCION.md` es una **nota de
referencia documentada, no una medición de este proyecto**, y por eso no se adopta como umbral.
Expermentar de más para aislarlo generaría más 429, es decir más sesgo de cobertura, y eso
contradice RN-GL-02. La caracterización crece con la observación de las corridas, no con
experimentos que degradan la recolección.

Cuando la observación acumulada permita aislarlo, se agrega aquí el valor con la corrida que lo
aisló. Mientras tanto, el estado `no determinado` es la respuesta honesta y utilizable.

## 4. Efecto sobre la cobertura por subreddit

### Caso verificado: `r/derechogenial`, corrida B4 del 2026-09-24

| Campo | Valor |
|---|---|
| Corrida | B4 — ingesta RSS real (Plan C), 2026-09-24 |
| Subreddit afectado | `r/derechogenial` |
| Síntoma | **0 posts ingeridos** en la corrida |
| Posts de los otros dos | `r/argentina` 101, `r/devsarg` 100 — **total 201 verificados** |
| Causa | Rate limiting de Reddit sobre el feed (atribución registrada en el proyecto; la confirmación primaria es el log de ejecuciones de n8n, pendiente de transcripción en la tarea 3.2) |
| `active_monitoring` | **`true`** — el subreddit **permanece habilitado** |
| Consulta de verificación | Ver la entrada de estado de la base en la bitácora; el `n` del día es un conteo operativo, no una métrica de resultados |

**El subreddit NO se desactiva.** Desactivar un subreddit habilitado que no aporta datos
maquillaría la cobertura y ocultaría una limitación real. `active_monitoring = true` es el
estado honesto de un subreddit que Reddit sirve pero cuya descarga no completa en el ciclo.

**El 0 entra en la tabla.** En todo desglose por subreddit, `r/derechogenial` aparece con su
`n` real —incluido el 0— y con la causa anotada, y el denominador de cualquier porcentaje son
los **tres** subreddit monitorizados (D-5, RN-GL-02).

### El sesgo se reporta, no se compensa

- La cobertura por subreddit de la ventana B5 está **sesgada por el rate limiting**: los `n` de
  cada subreddit no son comparables entre sí sin tener esto en cuenta.
- El sesgo se declara como **limitación** en el Capítulo 5 y en
  [`VENTANA_B5.md`](VENTANA_B5.md) §6. No se compensa.
- No se compensa con: datos de otra fuente, cifras de V2/V3, tasas supuestas, reasignación de
  posts entre subreddits, ni desactivación de un subreddit habilitado (RN-GL-02).
- Ningún porcentaje de la ventana se completa con datos ajenos al sistema.

## 5. Tabla acumulativa de incidentes

Una fila por incidente **realmente observado**. Sin filas de relleno ni ejemplos ilustrativos
presentados como datos. Se suma una fila por cada corrida que sufra rate limiting.

| # | Fecha | Subreddit afectado | Síntoma observado | Ciclo de ingesta |
|---|---|---|---|---|
| 1 | 2026-09-24 | `r/derechogenial` | 0 posts ingeridos en la corrida; atribuido a rate limiting de Reddit sobre el feed (respuesta 429 tras los reintentos de RN-FU-03) | Corrida B4 — ejecución de la ingesta RSS (Plan C) con 3 requests, uno por subreddit |
| 2 | 2026-09-30 | `r/devsarg` | 0 posts ingeridos. `netsec` y `r/Malware` completaron con 100 posts cada uno. El tercer request recibió **429** y **abortó la ejecución completa** (status `error`, 04:30:13 → 04:31:47) | Corrida de control del grupo 5 bis (D-9), corpus `netsec`/`Malware`/`devsarg`, 3 requests separados por 30 s |

**Total de incidentes registrados: 2.** La tabla crece únicamente con observación: cada corrida
de la ventana B5 que sufra 429 suma su fila con fecha, subreddit, síntoma y ciclo.

### Nota sobre el incidente 2: no fue un fallo del rate limit, sino de la mitigación

A diferencia del incidente 1, acá el 429 **no fue una limitación tolerada**: cortó la ejecución
entera. La causa se aisló leyendo el motor de n8n 2.40.6 y no fue el espaciado de 30 s, que
funcionó correctamente.

Los settings de mitigación estaban escritos bajo la clave `node.settings`, y el motor los lee
desde la **raíz** del nodo:

| Referencia en n8n 2.40.6 | Campo que lee |
|---|---|
| `n8n-core/dist/execution-engine/workflow-execute.js:933` | `node.retryOnFail` |
| `:937` | `node.maxTries` |
| `:938` | `node.waitBetweenTries` |
| `:563` | `node.continueOnFail` |
| `:564` | `node.onError` |

Bajo `node.settings` los cinco campos quedaban ignorados: no hubo reintentos ni continuación.
Dos firmas lo confirman en la ejecución 9: el intento fallido duró **400 ms** cuando
`maxTries: 3` con `waitBetweenTries: 3000` exigirían ≥6 s, y la ejecución terminó en `error`
global pese a `onError: continueRegularOutput`.

La misma línea `:938` fija el techo del backoff nativo:

```
Math.min(5000, Math.max(0, node.waitBetweenTries || 1000))
```

Por eso los 30 s por reintento que pedía la redacción original de RN-FU-03 eran imposibles por
configuración. La regla se relajó a "3 intentos con hasta 5 s" (D-10) y el espaciado de 30 s
**entre** subreddits lo mantiene el nodo `Espera Rate Limit`, que sí es configuración propia.

**Este incidente no se comptabiliza como límite de cobertura.** El 0 de `r/devsarg` es
*no intentado*, no * Reddit no sirvió posts*: el flujo se detuvo antes de consumir el feed.
Registrado aparte para no contaminar la comparación con el incidente 1.

## 6. Alcance de este change: qué NO se toca

Este documento es **descriptivo**. No se modificó ninguna configuración:

| Elemento | Estado | Por qué |
|---|---|---|
| Requests por ciclo de ingesta (3) | **Sin cambios** | Ajustarlo corresponde a **C-03 / C-07** (tarea 4.5) |
| Reintentos x3 con 30 s de espera (RN-FU-03) | **Cambiado el 2026-09-30 (D-10)** | El motor topa `waitBetweenTries` a 5000 ms, así que 30 s por reintento es imposible. La regla queda en "3 intentos con hasta 5 s". Los settings además estaban bajo `node.settings` y el motor los leía desde la raíz del nodo, con lo que la mitigación no se aplicaba: se corrigió la ubicación |
| `active_monitoring` de los tres subreddits | **Sin cambios**, todos en `true` | Regla dura: no desactivar un subreddit con posts |
| DDL y workflow | **Cambiado solo el nodo `Fetch Posts RSS`** | D-10 movió los settings a la raíz del nodo y subió el backoff a 5000 ms. No se tocó el DDL, el corpus, el clasificador ni el resto del grafo |

## 7. Documentos relacionados

| Documento | Qué aporta |
|---|---|
| [`VENTANA_B5.md`](VENTANA_B5.md) | Definición de la ventana, criterio de suficiencia y reglas de desglose por subreddit |
| [`bitacora_b5/`](bitacora_b5/) | Conteo diario con su consulta, fecha, ventana y `n` |
| `knowledge-base/05_reglas_de_negocio.md` | RN-FU-03 (reintentos), RN-AN-02, RN-GL-02, RN-GL-03 |
| `knowledge-base/06_funcionalidades.md` | US-002, criterio pendiente que este documento cierra |
| `V4/GUIA_EJECUCION.md` | Plan C, reintentos configurados y nota de referencia del límite público |
