# Reglas de Negocio

Cada regla tiene un código único `RN-{DOMINIO}-{NN}` para trazabilidad. Las reglas documentadas aquí reflejan el comportamiento que se debe observar y documentar; cualquier cambio debe quedar registrado en OpenSpec.

## Dominio: fuentes y recolección (RN-FU)

- **RN-FU-01**: el sistema monitorea únicamente subreddits habilitados en `subreddits.active_monitoring`.
- **RN-FU-02**: la fuente operativa actual es el feed RSS/Atom público `new/.rss`; no se requiere OAuth para esa fuente.
- **RN-FU-03**: cada subreddit se consulta una vez por ciclo de ingesta; ante 429/403 se reintenta hasta tres veces con 30 segundos de espera y se continúa con el resto del flujo.
- **RN-FU-04**: no se Consideran noticias las métricas ausentes del feed; `score`, `num_comments` y `subscribers` quedan en 0 y no se usan para el motor de anomalías.
- **RN-FU-05**: la recolección programada ejecuta la ingesta cada 15 minutos; el equipo puede ejecutar una corrida manual para verificar el pipeline.

## Dominio: persistencia (RN-PE)

- **RN-PE-01**: cada post se identifica por el id numérico derivado del enlace público de Reddit.
- **RN-PE-02**: la escritura de posts debe ser idempotente mediante `ON CONFLICT (id) DO UPDATE`; reejecutar el flujo no debe duplicar filas.
- **RN-PE-03**: `ingested_at` no se modifica en una actualización repetida si se necesita preservar la latencia de la primera ingesta; cualquier semántica definitiva debe quedar explicitada en la evidencia.
- **RN-PE-04**: no se puede borrar un subreddit que tenga posts asociados; se desactiva con `active_monitoring`.
- **RN-PE-05**: la clasificación se persiste en la misma operación de upsert para que el post quede trazable desde la fuente hasta la etiqueta.

## Dominio: seudonimización (RN-PS)

- **RN-PS-01**: nunca se persiste el nombre de usuario de Reddit en texto plano en el pipeline operativo.
- **RN-PS-02**: `author_hash` debe tener 64 caracteres hexadecimales y generarse con HMAC-SHA-256.
- **RN-PS-03**: la clave HMAC es secreta por despliegue; se documentan generación, custodia y rotación, pero no se publica su valor en el repositorio.
- **RN-PS-04**: un hash seudonimizado sigue siendo dato personal y debe manejarse con acceso restringido y política de retención documentada.

## Dominio: clasificación y entidades (RN-CL)

- **RN-CL-01**: cada post recibe una categoría del diccionario taxonómico o `No relevante`.
- **RN-CL-02**: `nlp_score` representa una confianza normalizada en `[0, 1]`; la fórmula y su interpretación deben estar documentadas en la tesis.
- **RN-CL-03**: la extracción de entidades reconoce al menos CVE, emails, IPs, dominios y productos, y guarda el resultado como JSONB.
- **RN-CL-04**: el diccionario taxonómico es la fuente de las categorías y palabras; sus entradas completas constituyen el Anexo C.
- **RN-CL-05**: un post sin señal relevante conserva su categoría y score; no se descartan silenciosamente filas de la evidencia.

## Dominio: anomalías y alertas (RN-AN)

- **RN-AN-01**: el motor de anomalías se ejecuta diariamente a las 00:05 y usa la ventana de ayer.
- **RN-AN-02**: la base comparativa es la media diaria de los diez días previos.
- **RN-AN-03**: el umbral se calcula como el máximo entre el cuantil 95 de Poisson para el volumen observado y un mínimo absoluto de 3.
- **RN-AN-04**: cada evaluación de categoría se registra en `anomalias`, tanto si dispara como si no; `disparo` diferencia ambos casos.
- **RN-AN-05**: una anomalía puede originar una alerta en `alertas`; Telegram es un canal opcional y no reemplaza el registro en base.
- **RN-AN-06**: no se afirma que el detector haya detectado un caso histórico hasta validar la corrida real contra la evidencia.

## Excepciones globales

- **RN-GL-01**: no se fabrican métricas. Cualquier cifra de la tesis debe provenir de la base real, de un export o de una captura fechada.
- **RN-GL-02**: una limitación de la fuente RSS debe declararse en resultados y no compensarse con datos inventados.
- **RN-GL-03**: los cambios de diseño se documentan como decisiones trazables antes de modificar la implementación.
