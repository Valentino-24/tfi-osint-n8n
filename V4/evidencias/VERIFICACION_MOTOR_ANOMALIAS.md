# Verificación del motor de anomalías (rama 2 del workflow)

**Fecha de la corrida:** 2026-09-30
**Instancia:** n8n 2.40.6 en Docker, workflow `KkotjSD5uO4CXI4D`
**Modo:** ejecución manual desde la UI
**Carácter:** verificación técnica. **No es un día de la ventana B5.**

## 1. Qué se probó

El workflow tiene dos ramas disparadas por dos triggers independientes:

| Rama | Trigger | Cadencia | Qué hace |
|---|---|---|---|
| 1 — Ingesta | `Schedule Ingesta` | cada 15 min | lee Reddit, anonimiza, clasifica y hace upsert de posts |
| 2 — Anomalías | `Schedule Anomalias` | 00:05 daily | compara el conteo de ayer contra la media de los 10 días previos y registra la evaluación |

Hasta esta corrida, **la rama 2 nunca se había ejecutado**. El riesgo conocido estaba
en el nodo `Registrar Anomalias y Alertas`, cuya query depende de
`jsonb_to_recordset(jsonb_build_array($1::jsonb))` con un `queryReplacement` que
manda `JSON.stringify($json)`. Si ese encadenamiento estuviera mal, no se insertaría
ninguna fila y el fallo sería silencioso.

## 2. Método: predecir antes de ejecutar

Antes de tocar la UI se replicó en Python la query exacta del nodo `Query Daily Counts`
y la lógica exacta del nodo `Anomaly Engine` (`poissonCdf`, `MIN_ABS = 3`,
`umbral = max(t + 1, 3)`), para saber qué tenía que aparecer.

Predicción: **7 filas en `anomalias`, 0 en `alertas`, 0 mensajes de Telegram.**

Motivo de los ceros: la rama 2 evalúa **ayer** (2026-09-29) y los 520 posts de la base
tienen `ingested_at` del 2026-09-30 únicamente. Ayer no tiene datos, así que
`n_observado = 0` en toda categoría y `disparo = false` en todas.

## 3. Cómo se ejecutó solo la rama 2

La UI de n8n arranca la ejecución manual **desde el primer trigger del workflow**, que
es `Schedule Ingesta`. Esto se comprobó en la corrida manual anterior: `posts` subió de
503 a 520 mientras `anomalias` quedó en 0 filas, o sea que solo corrió la rama 1.

Para ejecutar solo la rama 2 se desactivó el nodo `Schedule Ingesta` en el canvas, de
modo que el único trigger elegible pasó a ser `Schedule Anomalias`, y luego se ejecutó
el workflow. El nodo se reactivó después.

> Esta modificación existe únicamente en la copia de la instancia n8n.
> `V4/anexos/B_workflow.json` no se tocó.

## 4. Resultado medido

| Medición | Predicción | Observado | Resultado |
|---|---|---|---|
| Filas en `anomalias` | 7 | **7** | coincide |
| Filas en `alertas` | 0 | **0** | coincide |
| Mensajes de Telegram | 0 | 0 (nodo no alcanzado) | coincide |

Contenido de `anomalias` tras la corrida:

| categoría | n_observado | base_media | umbral | disparo | ventana |
|---|---|---|---|---|---|
| Filtración de Datos | 0 | 0.0 | 3.0 | false | 2026-09-29 00:00 → 2026-09-30 00:00 |
| Infraestructura y Ataques | 0 | 0.0 | 3.0 | false | 2026-09-29 00:00 → 2026-09-30 00:00 |
| Malware | 0 | 0.0 | 3.0 | false | 2026-09-29 00:00 → 2026-09-30 00:00 |
| Phishing | 0 | 0.0 | 3.0 | false | 2026-09-29 00:00 → 2026-09-30 00:00 |
| Ransomware | 0 | 0.0 | 3.0 | false | 2026-09-29 00:00 → 2026-09-30 00:00 |
| Robo de Credenciales | 0 | 0.0 | 3.0 | false | 2026-09-29 00:00 → 2026-09-30 00:00 |
| Vulnerabilidades | 0 | 0.0 | 3.0 | false | 2026-09-29 00:00 → 2026-09-30 00:00 |

Consultas de verificación:

```sql
SELECT count(*) FROM anomalias;                          -- 7
SELECT count(*) FROM alertas;                            -- 0
SELECT count(*) FROM anomalias WHERE disparo;            -- 0
SELECT count(*) FROM anomalias WHERE base_media > 0;     -- 0
SELECT count(*) FROM anomalias WHERE umbral <> 3;        -- 0
```

Las cinco comprobaciones de coherencia pasan. Los valores son los esperables:
`base_media = 0` porque no hay histórico de 10 días, el umbral de Poisson colapsa a 1
y manda el piso `MIN_ABS = 3`.

## 5. Nota sobre la zona horaria

Las primeras consultas de verificación mostraron la ventana como `03:00 → 03:00`. Es
un artefacto de presentación, **no un error de la query**: la sesión de PostgreSQL está
en `Etc/UTC`, así que el cliente renderiza el `timestamptz` en UTC. Expresada en hora de
Buenos Aires la ventana es exactamente `2026-09-29 00:00 → 2026-09-30 00:00`.

```sql
SHOW TimeZone;   -- Etc/UTC
SELECT ventana_inicio AT TIME ZONE 'America/Argentina/Buenos_Aires' FROM anomalias LIMIT 1;
-- 2026-09-29 00:00:00
```

La conversión de la query es correcta y el corte diario cae a medianoche local.

## 6. Qué NO probó esta corrida

- **El envío de la alerta.** No se alcanzó el nodo `Send Telegram Alert` porque
  `disparo` fue `false` en las 7 categorías.
- **Que el umbral detecte una anomalía real.** Con `base_media = 0` el umbral es
  siempre 3 y nunca hay nada que comparar. La sensibilidad del detector queda sin
  verificar hasta tener días de histórico.
- **El nodo de Telegram no tiene credenciales.** `TELEGRAM_BOT_TOKEN` y
  `TELEGRAM_CHAT_ID` no están definidas ni en el archivo de entorno de n8n ni en el
  contenedor. Con el estado actual el nodo resolvería la URL contra un token
  indefinido. Es una limitación conocida, no un defecto del encadenamiento.

## 7. Limitaciones declaradas para la tesis

1. **No hay latido.** La alerta solo se emite cuando hay anomalía. Si el workflow
   dejara de ejecutarse, no se emite ninguna señal: el silencio es indistinguible del
   de una jornada sin novedad. Es la limitación operativa más relevante del sistema
   de alertas.
2. **El umbral depende del histórico.** Durante los primeros días el piso `MIN_ABS = 3`
   hace que cualquier categoría con 3 o más posts dispare. Con 11 días cargados el
   umbral de Poisson pasa a gobernar.
3. **Los subreddits desactivados no se reevalúan.** `r/argentina` y `r/DerechoGenial`
   tienen `active_monitoring = false`, el loop de ingesta no los recorre y sus posts
   conservan la clasificación de versiones anteriores del clasificador.
