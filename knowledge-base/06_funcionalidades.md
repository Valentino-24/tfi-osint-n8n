# Funcionalidades

Las funcionalidades se organizan por épica y se expresan como historias de usuario. El estado indicado distingue funcionalidades implementadas de las que forman parte de B5/B6.

## Épica 1: Recolección de fuentes

### US-001 — Monitorear subreddits públicos
**Como** operador del sistema
**Quiero** consultar los feeds RSS de los subreddits configurados
**Para** obtener publicaciones nuevas sin depender de la API autenticada.

**Criterios de aceptación**:
- [x] Se consultan `r/argentina`, `r/devsarg` y `r/derechogenial`.
- [x] El ciclo se dispara cada 15 minutos.
- [x] Un error temporal de una fuente no descarta los resultados de las demás.

**Reglas relacionadas**: RN-FU-01, RN-FU-02, RN-FU-03, RN-FU-05.

### US-002 — Reintentar bajo rate limiting
**Como** operador
**Quiero** reintentar ante 429/403
**Para** no perder toda la corrida por un límite temporal de Reddit.

**Criterios de aceptación**:
- [x] Se reintenta hasta tres veces con espera de 30 segundos.
- [x] El flujo tiene comportamiento `continueOnFail` para conservar lo ya traído.
- [ ] Documentar la ventana exacta de rate limiting que se observe en las corridas finales.

**Reglas relacionadas**: RN-FU-03, RN-GL-02.

## Épica 2: Persistencia y seudonimización

### US-003 — Persistir posts idempotentemente
**Como** investigador
**Quiero** que los posts se guarden sin duplicados
**Para** poder consultar recuentos y latencias confiables.

**Criterios de aceptación**:
- [x] El id se deriva del enlace del post.
- [x] El upsert usa la clave primaria `posts.id`.
- [x] Una segunda corrida no duplica filas.

**Reglas relacionadas**: RN-PE-01, RN-PE-02, RN-PE-03.

### US-004 — Proteger la identidad del autor
**Como** responsable de la investigación
**Quiero** seudonimizar el autor
**Para** reducir exposición de datos personales.

**Criterios de aceptación**:
- [x] Se genera HMAC-SHA-256 con clave por despliegue.
- [x] Se persiste `author_hash` de 64 hexadecimales.
- [ ] Completar la política de gestión, rotación y retención de la clave.

**Reglas relacionadas**: RN-PS-01, RN-PS-02, RN-PS-03, RN-PS-04.

## Épica 3: Clasificación y extracción

### US-005 — Clasificar publicaciones
**Como** analista
**Quiero** una categoría y un score por post
**Para** separar señales de phishing de conversaciones no relevantes.

**Criterios de aceptación**:
- [x] Se usa un diccionario taxonómico de cinco categorías más `No relevante`.
- [x] `nlp_score` está normalizado entre 0 y 1.
- [ ] Publicar el diccionario completo como Anexo C.

**Reglas relacionadas**: RN-CL-01, RN-CL-02, RN-CL-04, RN-CL-05.

### US-006 — Extraer entidades tecnológicas
**Como** analista
**Quiero** CVE, emails, IPs, dominios y productos detectados
**Para** caracterizar las señales de amenaza.

**Criterios de aceptación**:
- [x] Las entidades se guardan en `posts.entities` como JSONB.
- [x] La extracción ocurre en el pipeline de n8n.
- [ ] Documentar el modelo/algoritmo exacto y sus ejemplos en la tesis.

**Reglas relacionadas**: RN-CL-03.

## Épica 4: Detección de anomalías

### US-007 — Evaluar el volumen de una categoría
**Como** operador
**Quiero** evaluar los conteos diarios
**Para** detectar picos de publicación por categoría.

**Criterios de aceptación**:
- [x] Se usa la ventana de ayer y la media de los diez días previos.
- [x] Se registra cada evaluación en `anomalias`.
- [x] El umbral combina cuantil 95 de Poisson y mínimo absoluto 3.

**Reglas relacionadas**: RN-AN-01, RN-AN-02, RN-AN-03, RN-AN-04.

### US-008 — Registrar y notificar alertas
**Como** responsable del monitoreo
**Quiero** registrar las alertas
**Para** conservar evidencia incluso si el canal externo no está habilitado.

**Criterios de aceptación**:
- [x] Las alertas se relacionan con su anomalía.
- [x] El canal Telegram es opcional.
- [ ] Obtener una captura de alerta real si se habilita el canal.

**Reglas relacionadas**: RN-AN-05.

## Épica 5: Evidencias y sustentación de la tesis

### US-009 — Producir evidencia reproducible
**Como** autor del TFI
**Quiero** exportar el workflow, el DDL y las salidas SQL
**Para** sustentar capítulos, tablas y figuras sin inventar cifras.

**Criterios de aceptación**:
- [x] Existe `V4/anexos/B_workflow.json` importable.
- [x] Existe `V4/anexos/A_DDL.sql` con las correcciones aplicadas.
- [ ] Completar E1–E15 según disponibilidad real de datos.

**Reglas relacionadas**: RN-GL-01, RN-GL-03.

### US-010 — Evaluar la clasificación con una muestra
**Como** tribunal
**Quiero** comparar etiquetas humanas y predicciones
**Para** medir el desempeño sin confundir salida cruda con amenaza real.

**Criterios de aceptación**:
- [ ] Constituir la muestra de control.
- [ ] Completar la matriz de confusión 6×6.
- [ ] Obtener la submuestra del evaluador externo cuando sea posible.

**Reglas relacionadas**: RN-GL-01, RN-CL-05.
