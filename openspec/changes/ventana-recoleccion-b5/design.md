## Context

B4 está verificada: el 2026-09-24 se ejecutó `Schedule Ingesta` con el workflow RSS/Plan C y la base `tesi_osint` quedó con 201 posts verificados (`r/argentina` 101, `r/devsarg` 100, `r/derechogenial` 0 por rate limiting). Desde entonces el scheduler de 15 minutos quedó activo, pero nadie sabe cuántos días lleva corriendo ni qué se recolectó.

Las métricas del Capítulo 5 (E4 Tabla 3, E5 matriz de confusión, E6 latencia, E7 anomalías, E8 captura–recaptura) se calculan sobre el corpus de la ventana. Sin fecha de inicio y sin bitácora, cualquier cifra de resultados no es trazable y viola RN-GL-01.

Restricciones que gobiernan el diseño:

- **El DDL y la lógica del pipeline están congelados.** `V4/anexos/A_DDL.sql` y `V4/scripts/generar_workflow.py` no se tocan. Ninguna tabla, columna, índice o sentencia cambia.
- **La fecha de corte es una decisión de los autores con sus directores.** No se propone un plazo por defecto ni se deja un campo tipo "a definir" que después se pueda leer como una fecha implícita.
- **La ventana de rate limiting es un hecho observado, no un parámetro.** Reddit impone su propia ventana; el sistema solo la registra y la reporta.
- **El corpus pre-B5 no es la ventana.** Los 201 posts de B4 son del 2026-09-24, un día antes del inicio.

## Goals / Non-Goals

**Goals:**

- Dejar la ventana real de recolección escrita, fechada y con inicio explícito (2026-09-25).
- Producir, día a día, evidencia consultable de lo que el sistema recolectó y de lo que falló.
- Caracterizar la ventana real de rate limiting de Reddit observada en las corridas y su efecto sobre la cobertura por subreddit.
- Definir y dejar registrado el criterio por el cual la ventana se declara suficiente, y el estado de acumulación día a día.
- Dejar la decisión de cierre como una decisión trazable y explícitamente abierta (RN-GL-03).

**Non-Goals:**

- No modificar DDL, workflow, diccionarios ni scripts del pipeline.
- No ejecutar operaciones destructivas sobre `tesi_osint`: solo consultas `SELECT` de conteo y agregación.
- No habilitar Telegram ni tocar credenciales, tokens ni la clave HMAC.
- No cerrar la ventana ni producir E4, E5, E6, E7 ni E8: eso es C-08 a C-11.
- No cambiar el scheduler de 15 minutos ni reinterpretar RN-AN-02; solo observar su efecto.
- No tocar `ingested_at` ni verificar la semántica del upsert: eso es C-07.

## Decisions

### D-1 — La fecha de inicio es 2026-09-25 y la ventana se define por acceso a datos, no por fecha de calendario

**Qué**: el corpus de la ventana B5 es exactamente el conjunto de posts con `ingested_at >= 2026-09-25 00:00:00` en la zona horaria de la ejecución del sistema, y `ingested_at <` la fecha de corte cuando esta se defina.

**Por qué**: define la ventana con el mismo campo que usa C-08 para E6, así que latencia, Tabla 3 y E7 comparten un criterio y no dos. Filtrar por `created_utc` mezclaría fechas de publicación externas al sistema, que no son evidencia de lo que el sistema recolectó.

**Alternativas consideradas**: (a) fechar por `created_utc`, rechazado porque incluye posts que el sistema nunca vio; (b) definir la ventana como "últimos N días" en vez de fechas fijas, rechazado porque una ventana móvil no es auditable ni comparable entre dos momentos del Cap. 5.

**Consecuencia**: los 201 posts de B4 quedan **fuera** de la ventana. Toda cifra de C-08 se calcula sobre el corpus B5 y se reporta con su `n` y su ventana.

### D-2 — El bitácora es un archivo de texto por día en Markdown, generado por script

**Qué**: un script en `V4/scripts/` emite `V4/evidencias/bitacora_b5/YYYY-MM-DD.md` por día, con una cabecera que incluye la consulta SQL usada, la fecha, el nombre de la ventana y el `n` total.

**Por qué**: es texto plano versionable y legible sin herramientas, a diferencia de CSV o binarios. El encabezado lleva la consulta literal, que es lo que exige RN-GL-01: ninguna cifra sin su consulta, fecha, ventana y número de observaciones. Las salidas crudas de `psql` van en el mismo directorio como `.txt` adjunto cuando el volumen lo justifique.

**Alternativas consideradas**: (a) tabla `bitacora_diaria` en la base, rechazado porque agregaría DDL a un change que debe ser documental; (b) una sola tabla acumulativa en Markdown, rechazado porque un diff por día mezcla filas y hace imposible auditar una fecha puntual; (c) CSV, rechazado porque no admite el bloque de contexto de la consulta sin convención extra.

### D-3 — Las consultas del bitácora son de solo lectura y parametrizadas por fecha

**Qué**: el script toma la fecha como parámetro y emite consultas `SELECT` agregadas: total de posts ingeridos, posts por subreddit, ejecuciones fallidas detectadas y su causa.

**Por qué**: cumplir la regla dura de no ejecutar pruebas destructivas sin corrida controlada, y hacer la bitácora reproducible: cualquiera puede reejecutar la misma consulta y obtener el mismo número.

**Detección de fallos**: n8n no persiste un log de errores de ejecución en la base. La fuente de verdad de "ejecuciones fallidas y su causa" es el log de ejecuciones de la instancia n8n, y su transcripción manual a la bitácora declara su origen. Si el log no está disponible, la bitácora registra la ejecución como "sin observación" en vez de asumir que fue exitosa — asumir éxito sería fabricar un dato.

**Alternativas consideradas**: (a) parsear el log de n8n automáticamente, diferido: el formato del log no está versionado y agrega acoplamiento frágil a un change documental; (b) contar fallos desde `posts` (imposible: el upsert idempotente deja el mismo conteo tras un fallo).

### D-4 — La caracterización del rate limiting se describe, no se parametriza

**Qué**: un documento de caracterización en `V4/evidencias/` describe la ventana de rate limiting observada — Reddit devuelve 429 tras una cantidad de requests por unidad de tiempo desde la IP del proyecto — y su efecto: el ciclo de 15 minutos hace 3 requests (uno por subreddit), `r/derechogenial` quedó en 0, y el reintento x3 con 30 s de espera es la mitigación configurada (RN-FU-03).

**Por qué**: cierra el criterio pendiente de US-002, que quedó sin definir por la ausencia de la API `.json`. La caracterización es una observación empírica acumulativa: cada corrida que sufra 429 suma una fila a la evidencia. El número de requests que dispara el límite **no se afirma de memoria**: se registra lo observado y, si no se pudo aislar, se declara como no determinado.

**Alternativas consideradas**: (a) fijar un límite de requests por ciclo como constante del workflow, rechazado porque es C-03/C-07, no C-05, y porque el valor correcto no está determinado; (b) desactivar `r/derechogenial` para evitar el 429, rechazado por la regla dura de no eliminar ni desactivar un subreddit con datos, y porque `active_monitoring` en `true` es el estado honesto de un subreddit que Reddit sirve pero cuya descarga no completa.

### D-5 — `r/derechogenial` se reporta como presente en el alcance y ausente en el corpus

**Qué**: en toda cifra por subreddit, `r/derechogenial` aparece con su `n` real, incluido el 0, y con la causa anotada. Ningún percentage por subreddit se calcula sin el denominador completo de los tres.

**Por qué**: m-16 y RN-GL-02. Un subreddit habilitado que no aporta datos sesga cualquier porcentaje si se omite en silencio; reportarlo con su causa declarada convierte un sesgo en una limitación documentada.

**Alternativas consideradas**: (a) excluir el subreddit de los porcentajes, rechazado porque el alcance de v4.0 lo incluye; (b) completar con datos de otra fuente, rechazado explícitamente por RN-GL-02.

### D-6 — El criterio de suficiencia se declara con un umbral de días y su justificación

**Qué**: la ventana se declara suficiente cuando el motor de anomalías tiene **10 días completos de evaluaciones** registrados en `anomalias`, porque RN-AN-02 usa la media diaria de los diez días previos y sin esa historia la base comparativa no existe. Antes de ese umbral, la ventana se declara abierta y el estado se reporta como limitación (RN-AN-06), no como ausencia de anomalías.

**Por qué**: es el mismo número que el motor usa, no uno inventado para la ocasión. Un umbral menor daría evaluaciones con base incompleta; uno mayor retrasaría el cierre sin ganancia.

**Nota operativa**: el motor corre a las 00:05 y evalúa la ventana de ayer, así que las primeras evaluaciones con base completa aparecen hacia el día 12 de la ventana. El bitácora registra `días_completos_evaluados` para que el estado sea verificable y no una estimación.

**Alternativas consideradas**: (a) esperar 30 días, rechazado porque es arbitrario y retrasa el tramo crítico sin aportar criterio; (b) declarar suficiente con menos días "si la base parece estable", rechazado porque "parece estable" no es verificable contra una media de diez días.

### D-7 — La fecha de corte se modela como decisión abierta con un valor explícito de "no fijada"

**Qué**: la documentación de la ventana declara el inicio 2026-09-25 y el corte como `no fijada`, con la razón (decisión de los autores pendiente con sus directores) y la tarea que la cierra. Nunca se escribe una fecha tentativa sin marcarla como tal.

**Por qué**: RN-GL-03 y la pregunta abierta de prioridad Alta. Un campo de fecha en blanco puede leerse más adelante como un olvido; un valor explícito de "no fijada" con su motivo es una decisión trazable. Inventar un plazo —"treinta días"— sería fabricar un parámetro de investigación.

**Alternativas consideradas**: (a) proponer 30 días como default por si los autores no responden, rechazado explícitamente: una fecha sin decisión es una fecha inventada; (b) dejar el campo vacío, rechazado por el motivo de ambigüedad anterior.

### D-8 — Las actualizaciones documentales se limitan a sustituir la ventana ficticia por la real

**Qué**: `V4/GUIA_EJECUCION.md`, `knowledge-base/02_descripcion_general.md` §Estado de implementación y `knowledge-base/09_decisiones_y_supuestos.md` §SU-02 se editan solo en lo relativo a la ventana. El resto de las correcciones documentales de esos archivos son C-06.

**Por qué**: C-06 ya es el responsable de IN-01, IN-02 e IN-05 sobre los mismos archivos. Tocar de más genera conflictos entre changes paralelos de la Fase 1.

**Alternativas consideradas**: (a) corregir de paso la tabla de estado de B4 (IN-02), rechazado porque pertenece a C-06; (b) no tocar la KB y dejarlo todo para el cierre, rechazado porque SU-02 pide fechar la ventana antes de producir las tablas finales.

## Risks / Trade-offs

- **[El corpus B5 crece lento por el rate limiting]** → El plan C puede producir muy pocos posts por ciclo, y el Capítulo 5 puede quedar con un `n` modesto. Mitigación: declarar el `n` y la ventana junto a cada cifra y tratarlo como resultado honesto, nunca rellenarlo con datos ajenos (RN-GL-02). Se eleva a los autores en la decisión de cierre.

- **[Los 201 posts de B4 quedan fuera de la ventana y el trabajo de B4 se pierde como evidencia de resultados]** → Se preservan como evidencia de la corrida técnica y de la caracterización de rate limiting, pero no se mezclan con el corpus B5. Si los autores prefieren incluirlos, es una decisión de ellos y se registra en `decision-cierre-ventana` como cambio de alcance, no como ajuste silencioso de una consulta.

- **[Los fallos de ejecución no quedan registrados en la base, solo en el log de n8n]** → La bitácora declara el origen de cada dato de fallo y marca "sin observación" cuando el log no está disponible. La transcripción manual es verificable contra el log. Dejar esto como deuda consciente: automatizarlo implicaría tocar el workflow, fuera de alcance.

- **[La caracterización de rate limiting puede no alcanzar un umbral de certeza antes del cierre]** → Se reporta lo observado y se declara como no determinado lo que no se pudo aislar. Una caracterización parcial declarada es utilizable; una cifra inventada no lo es.

- **[El cierre de la ventana depende de una decisión externa a la ejecución técnica]** → La bitácora y `días_completos_evaluados` permiten retomar el estado sin depender de memoria ni de esta sesión. El criterio de suficiencia (D-6) reduce la dependencia del calendario: el cierre se dispara por evidencia acumulada, no por una fecha límite arbitraria.

- **[C-06, C-07 y C-05 corren en paralelo y tocan documentación relacionada]** → D-8 acota el perímetro de C-05 a la ventana. Si C-06 edita los mismos párrafos, el merge se resuelve a favor de C-06, que tiene el perímetro documental más amplio.

- **[C-07 puede cambiar la semántica de `ingested_at` y con ella el filtro de la ventana]** → El filtro de D-1 usa `ingested_at`, que es justo el campo que C-07 examina. Si C-07 confirma que el upsert no lo toca, el filtro es estable; si determinara lo contrario, la ventana debe recalcularse. Se deja asentado como dependencia blanda, no como bloqueo.

## Migration Plan

No hay migración: el change no altera esquema, ni datos, ni código ejecutable. Es documental y de evidencia.

Orden de aplicación:

1. Script de bitácora en `V4/scripts/` y primera entrada fechada 2026-09-25.
2. Documento de caracterización de rate limiting.
3. Registro de la ventana (inicio 2026-09-25, corte no fijada, criterio de suficiencia de D-6).
4. Ediciones documentales acotadas por D-8.
5. Tarea de seguimiento para la decisión de cierre, abierta hasta que los autores decidan.

Rollback: revertir los archivos de texto creados o modificados. No hay estado en base que deshacer.

## Open Questions

1. **Fecha de corte de la ventana** — decisión de los autores con sus directores. Sin fecha tentativa. Bloquea el cierre de la ventana y, en cascada, C-08, C-11, C-09, C-20, C-21 y C-23.
2. **Conservar la recolección actual o reiniciarla con métricas corregidas** — pregunta abierta de prioridad Media. Si se reinicia, la fecha de inicio se convierte en la del reinicio y la de 2026-09-25 pasa a ser la de la ventana descartada, documentada como tal.
3. **Si los 201 posts de B4 se incluyen o no en el corpus B5** — consecuencia directa de D-1. Por defecto quedan fuera; incluirlos es una decisión de los autores y debe quedar registrada.
4. **Disponibilidad del log de ejecuciones de n8n durante la ventana** — condiciona la calidad del campo "ejecuciones fallidas y su causa" (D-3). Si no se conserva, la bitácora lo declara y la limitación se reporta en el Capítulo 5.
5. **Umbral exacto de requests que dispara el 429 de Reddit** — probablemente no se pueda aislar sin experimentar, y experimentar de más genera más 429. Se registra como no determinado si la observación no lo sugiere.
