# CHANGES — Secuencia de Implementación

> Índice canónico de todos los changes del proyecto **TFI OSINT/n8n (V4)**.
> Cada change es atómico: un agente puede ejecutarlo en una sesión (~4-6 horas).
> **Leer este archivo antes de ejecutar cualquier `/opsx:propose`.**

> **Estado real al momento de generar este roadmap:** el prototipo **ya está construido y corriendo** (pasos B1–B4 verificados sobre la fuente RSS / Plan C). Los changes `C-01` a `C-04` están marcados `[x]` porque se ejecutaron **antes** de inicializar OpenSpec: no están en `openspec/changes/archive/`, su artefacto verificable es `V4/anexos/A_DDL.sql`, `V4/anexos/B_workflow.json` y la base `tesi_osint`. Todo lo que sigue (B5, B6 y la reconstrucción del documento) está `[ ]`.
> **Regla de honestidad vigente (RN-GL-01):** ninguna cifra de este roadmap ni de la tesis se inventa. Las cifras quoted abajo provienen de la corrida verificada de B4 y de la base real.

---

## Cómo usar este documento

1. Identificar el change a implementar (verificar que sus dependencias están en `openspec/changes/archive/`; los `C-01`–`C-04` son la excepción y se validan contra `V4/anexos/` y la base).
2. Leer los docs de la knowledge-base indicados en "Leer antes".
3. Ejecutar `/opsx:propose <nombre-del-change>`.
4. Al terminar el change, archivarlo con `/opsx:archive <nombre-del-change>`.
5. Marcar el checkbox `[x]` en este archivo.

---

## Árbol de dependencias

```text
═══ RAMA SISTEMA — produce la evidencia (B5 → B6) ═══

C-01 entorno-postgres-n8n  [x]
  └── C-02 modelo-ddl-tesi-osint  [x]
        └── C-03 workflow-n8n-generado-e-importado  [x]
              └── C-04 corrida-b4-ingesta-rss  [x]     ← desbloquea todo lo pendiente
                    ├── C-05 ventana-recoleccion-b5
                    │     ├── C-08 evidencias-e4-tabla3-y-e6-latencia
                    │     │     ├── C-09 evidencias-e7-motor-anomalias
                    │     │     └── C-10 evidencias-e5-matriz-confusion
                    │     │             └── C-15 evaluador-externo-e14
                    │     └── C-11 evidencias-e8-captura-recaptura
                    ├── C-07 semantica-ingested-at
                    └── C-06 sincronizacion-documental-v4
                          ├── C-12 evidencias-artefacto-e1-e2-e3-e10
                          ├── C-13 anexo-c-diccionario-taxonomico-e11
                          ├── C-14 entorno-y-canales-e9-e12-e13
                          └── C-18 capitulo-1-2   ◄── C-16, C-17
                                └── C-19 capitulo-3-4   ◄── C-13, C-07, C-12
                                      └── C-20 capitulo-5-6   ◄── C-08, C-09, C-10, C-11
                                            └── C-21 capitulo-7-8-resumen-titulo
                                                  └── C-23 auto-auditoria-final   ◄── C-22

═══ RAMA DOCUMENTO — independiente del sistema ═══

C-16 normalizacion-base-textual-v2  ──┐
C-17 antecedente-e15-rivas-dengra   ──┴──► C-18

C-22 figuras-2-3-4-e-indices   ◄── C-12, C-08
```

### Paralelismo por fase

> Cada "gate" es un punto de sincronización. Los changes dentro de un grupo pueden ejecutarse en paralelo.

```text
GATE 0: ninguna
  → C-16 normalizacion-base-textual-v2   [Agente C]
  → C-17 antecedente-e15-rivas-dengra    [Agente B]
  (C-01 a C-04 ya están ✓ — foundation verificada sobre la base real)

GATE 1: C-01 ✓
  → C-02 modelo-ddl-tesi-osint  (solo)

GATE 2: C-02 ✓
  → C-03 workflow-n8n-generado-e-importado  (solo)

GATE 3: C-03 ✓
  → C-04 corrida-b4-ingesta-rss  (solo)

GATE 4: C-04 ✓                       ← PRIMER FORK (3 paralelos sobre el sistema)
  → C-05 ventana-recoleccion-b5      [Agente A]
  → C-06 sincronizacion-documental-v4 [Agente B]
  → C-07 semantica-ingested-at        [Agente C]

GATE 5: C-05 ✓ + C-07 ✓              ← FORK
  → C-08 evidencias-e4-tabla3-y-e6-latencia      [Agente A]
  → C-11 evidencias-e8-captura-recaptura         [Agente B]

GATE 6: C-06 ✓                       ← FORK
  → C-12 evidencias-artefacto-e1-e2-e3-e10  [Agente A]
  → C-13 anexo-c-diccionario-taxonomico-e11 [Agente B]
  → C-14 entorno-y-canales-e9-e12-e13       [Agente C]

GATE 7: C-08 ✓                       ← FORK
  → C-09 evidencias-e7-motor-anomalias   [Agente A]
  → C-10 evidencias-e5-matriz-confusion  [Agente B]

GATE 8: C-10 ✓
  → C-15 evaluador-externo-e14  [Agente B]

GATE 9: C-16 ✓ + C-17 ✓
  → C-18 capitulo-1-2  [Agente C]

GATE 10: C-18 ✓ + C-13 ✓ + C-07 ✓ + C-12 ✓
  → C-19 capitulo-3-4  [Agente C]

GATE 11: C-19 ✓ + C-08 ✓ + C-09 ✓ + C-10 ✓ + C-11 ✓
  → C-20 capitulo-5-6  [Agente C]

GATE 12: C-20 ✓                      ← FORK
  → C-21 capitulo-7-8-resumen-titulo  [Agente C]
  → C-22 figuras-2-3-4-e-indices      [Agente A]

GATE 13: C-21 ✓ + C-22 ✓
  → C-23 auto-auditoria-final  [Agente A]
```

### Camino crítico (10 changes — mínimo irreducible)

```text
C-01 → C-02 → C-03 → C-04 → C-05 → C-08 → C-09  → C-20 → C-21 → C-23
                                                        (cola alternativa: C-10 *)
```

> `*` C-09 y C-10 están al mismo nivel y ambos alimentan C-20: cualquiera de los dos puede cerrar el camino crítico, pero **ambos** son necesarios para que el Cap. 5 no tenga capítulos vacíos.
> **Los cuatro primeros ya están ejecutados.** El tramo crítico *pendiente* es: `C-05 → C-08 → C-09 → C-20 → C-21 → C-23` (6 changes). La ventana de recolección (C-05) es el reloj del proyecto: todo lo cuantitativo depende de cuánto tiempo se deje correr el sistema.

### Plan óptimo con 3 agentes

```text
Paso │ Agente A (Pipeline y Datos)   │ Agente B (Evidencias y Anexos)  │ Agente C (Documento y Redacción)
─────┼───────────────────────────────┼────────────────────────────────┼──────────────────────────────
  1  │ C-01 entorno-postgres-n8n  ✓  │ C-17 antecedente-e15           │ C-16 normalizacion-base-v2
  2  │ C-02 modelo-ddl-tesi-osint ✓ │              —                 │              —
  3  │ C-03 workflow-n8n          ✓ │              —                 │              —
  4  │ C-04 corrida-b4-ingesta-rss ✓│              —                 │              —
  5  │ C-05 ventana-recoleccion-b5  │ C-06 sincronizacion-documental │ C-07 semantica-ingested-at
  6  │ C-08 evidencias-e4 / e6     │ C-12 evid. artefacto + C-13     │ C-18 capitulo-1-2
  7  │ C-09 e7-motor + C-10 e5-mtz │ C-11 e8-captura + C-14 entorno │ C-19 capitulo-3-4
  8  │              —              │ C-15 evaluador-externo-e14      │ C-20 capitulo-5-6
  9  │ C-22 figuras-2-3-4-indices  │              —                 │ C-21 capitulo-7-8-resumen
 10  │ C-23 auto-auditoria-final    │              —                 │              —
```

> El Agente B arranca su cadena larga (C-17 → C-06 → C-12/C-13/C-14 → C-22) desde el paso 1 porque es la que más encadenamientos tiene. El Agente C no puede empezar C-18 hasta cerrar C-16, C-17 y C-06 — es la restricción de paralelismo más fuerte del plan.

---

## FASE 0 — Fundaciones del prototipo (B1–B4 verificadas)

> Esta fase ya está ejecutada contra el sistema real. Se documenta para que nadie la repita ni la contradiga con la evidencia.

### [C-01] `entorno-postgres-n8n`
- **Estado**: `[x]` verificado
- **Scope**:
  - PostgreSQL 18 instalado con cluster del proyecto en `V4/pgdata`, escuchando en puerto `5433`; base `tesi_osint` creada
  - Scripts de arranque/parada: `V4/scripts/arrancar_postgres.bat`, `arrancar_postgres_silencioso.bat`, `parar_postgres.bat`
  - n8n 2.22.6 instalado y accesible en `http://localhost:5678` con cuenta local del operador
  - Rol de aplicación `tesi_app` con acceso a `tesi_osint` (credencial de desarrollo; nunca versionada)
  - Variables de entorno documentadas en `V4/GUIA_EJECUCION.md` §1: `OSINT_HMAC_KEY`, `NODE_FUNCTION_ALLOW_BUILTIN=crypto`, `N8N_BLOCK_ENV_ACCESS_IN_NODE=false`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `PGPASSWORD`
  - Verificación: cluster arriba + n8n responde + `psql` conecta a `tesi_osint` en `localhost:5433`
- **Dependencias**: ninguna
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/02_descripcion_general.md` §Stack tecnológico
  - `knowledge-base/08_arquitectura_propuesta.md` §Variables de entorno
  - `knowledge-base/03_actores_y_roles.md` §Rutas públicas
  - `knowledge-base/01_vision_y_objetivos.md` §Fuera de alcance

---

### [C-02] `modelo-ddl-tesi-osint`
- **Estado**: `[x]` verificado
- **Scope**:
  - `V4/anexos/A_DDL.sql` como fuente de verdad del esquema, con las correcciones aplicadas (no el borrador original)
  - Tablas: `subreddits`, `posts`, `comments`, `anomalias`, `alertas` — las cinco verificadas en `tesi_osint`
  - `posts.id VARCHAR(50)` derivado de `/r/{sub}/comments/{id}/`; `author_hash CHAR(64)`; `nlp_score REAL CHECK (nlp_score BETWEEN 0 AND 1)`; `entities JSONB`; `nlp_processed BOOLEAN`; `ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP`
  - `posts.subreddit_id` con `ON DELETE RESTRICT` + baja lógica vía `subreddits.active_monitoring` (m-20)
  - Índices en `posts`: `created_utc`, `nlp_category`, `ingested_at`
  - `anomalias` con `ventana_inicio`/`ventana_fin`/`categoria`/`n_observado`/`base_media`/`umbral`/`disparo`; `alertas` con FK a `anomalia_id`, `canal`, `payload JSONB`, `estado`
  - Seed de los tres subreddits monitorizados: `argentina`, `devsarg`, `derechogenial`
  - `comments` se crea y se conserva aunque el pipeline RSS no la puebla (DD-02); resolver `pg_trgm` (H-16) queda en C-19
  - Verificación: `\dt` devuelve las 5 tablas y el seed de subreddits existe
- **Dependencias**: C-01
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Entidades
  - `knowledge-base/04_modelo_de_datos.md` §ERD
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-02, §DD-06
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: persistencia (RN-PE)

---

### [C-03] `workflow-n8n-generado-e-importado`
- **Estado**: `[x]` verificado
- **Scope**:
  - `V4/scripts/generar_workflow.py` como generador (fuente de verdad); `V4/anexos/B_workflow.json` como artefacto importable
  - Trigger 1 `Schedule Ingesta` cada 15 min: `Prepare Subreddits` → upsert `subreddits` → `RSS Read` (`new/.rss`) → parse (id y subreddit desde el link) → `HMAC-SHA-256` → clasificador por diccionario (5 categorías + `No relevante`, score `[0,1]`) → extracción de entidades (CVE, emails, IPs, dominios, productos) → `Upsert Posts` con `ON CONFLICT (id) DO UPDATE`
  - Trigger 2 `Schedule Anomalias` diario 00:05: counts por categoría de ayer + media diaria de los 10 días previos → umbral `max(cuantil 95 de Poisson, 3)` → registro en `anomalias` → `alertas` con estado inicial si hubo disparo → `Send Telegram Alert` **deshabilitado por defecto**
  - `continueOnFail` + retry x3 con espera de 30 s ante 429/403 de Reddit (RN-FU-03)
  - Fuente RSS / Atom público (Plan C, DD-01): la API `.json` da 403 "blocked by network security" y la creación de apps está bloqueada por la Responsible Builder Policy
  - Import verificado con `n8n import:workflow`; credencial Postgres reasignada en la interfaz tras cada importación
  - **Pendiente de verificación (IN-01):** la guía declara 15 nodos y la sesión de verificación reportó 14 — se resuelve en C-06
- **Dependencias**: C-02
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/07_flujos_principales.md` §Flujo 1: Ingesta programada de publicaciones
  - `knowledge-base/07_flujos_principales.md` §Flujo 2: Evaluación diaria de anomalías
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-01, §DD-05, §DD-07
  - `knowledge-base/02_descripcion_general.md` §Arquitectura general
  - `knowledge-base/08_arquitectura_propuesta.md` §Patrones aplicados

---

### [C-04] `corrida-b4-ingesta-rss`
- **Estado**: `[x]` verificado
- **Scope**:
  - Ejecución manual de `Schedule Ingesta` con n8n y variables de entorno seteadas (clave HMAC generada por despliegue, nunca versionada)
  - Resultado verificado de la corrida registrada: **201 posts** — `r/argentina` 101, `r/devsarg` 100, `r/derechogenial` **0 por rate limit** (limitación declarada, no completada con datos ajenos, RN-GL-02)
  - Clasificador: 1 post real de `Phishing` en `r/devsarg` (`nlp_score` 0.2) y 200 posts `No relevante`
  - Verificación en base: `SELECT COUNT(*) FROM posts` > 0, `nlp_category` no nulo, `author_hash` de 64 hexadecimales, `entities` en JSONB
  - Capturas de la corrida y salidas `psql` archivadas como evidencia de la corrida B4
  - Limitación registrada: RSS no entrega `score`, `num_comments` ni `subscribers` — quedan en 0 y el motor de anomalías no los usa (RN-FU-04)
  - **Estas cifras son de esta corrida y no se proyectan**: cualquier tabla de la tesis se reconstruye con SQL sobre la base al momento de producir la evidencia (C-08)
- **Dependencias**: C-03
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/02_descripcion_general.md` §Estado de implementación
  - `knowledge-base/07_flujos_principales.md` §Flujo 1 (casos de error)
  - `knowledge-base/06_funcionalidades.md` §US-001, §US-002, §US-003
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: fuentes y recolección (RN-FU)
  - `knowledge-base/05_reglas_de_negocio.md` §Excepciones globales

---

## FASE 1 — Ventana de datos y sincronización documental

> Primer fork real del proyecto. `C-05` es puramente temporal (el sistema tiene que correr), por eso se lanza primero y en paralelo con las correcciones documentales.

### [C-05] `ventana-recoleccion-b5`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - Fijar por escrito la **fecha de inicio** y la **fecha de corte** de la ventana real de recolección; reemplazar toda mención a la ventana ficticia de 6 meses de V2/V3 (SU-02)
  - Mantener el `Schedule Ingesta` de 15 min activo durante la ventana; registrar en `V4/evidencias/` una entrada por día con: fecha, posts ingeridos, posts por subreddit, ejecuciones fallidas y su causa
  - Caracterizar la ventana real de rate limiting de Reddit observada en las corridas (cierra el criterio pendiente de US-002) y documentar el efecto de `r/derechogenial` en el corpus (m-16)
  - Dejar acumular días hasta que la media de los 10 días previos del motor de anomalías sea interpretable (RN-AN-02)
  - **Decisión de los autores, con los directores**: fecha de cierre de la ventana y si se conserva la actual o se reinicia la recolección con métricas corregidas
  - No declarar ninguna métrica de resultados hasta cerrar la ventana (RN-GL-01)
  - **Bloqueado por**: pregunta abierta de prioridad alta (fecha de inicio/cierre) — decisión de los autores con sus directores
- **Dependencias**: C-04
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/09_decisiones_y_supuestos.md` §SU-02
  - `knowledge-base/10_preguntas_abiertas.md` §Preguntas abiertas priorizadas
  - `knowledge-base/01_vision_y_objetivos.md` §Alcance v4.0
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: anomalías y alertas (RN-AN-02)

---

### [C-06] `sincronizacion-documental-v4`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **IN-01**: regenerar `V4/anexos/B_workflow.json` desde `V4/scripts/generar_workflow.py`, contar los nodos de esa versión final y corregir la cifra en `V4/GUIA_EJECUCION.md` y en la Figura 3 (la discrepancia 15 vs 14 es un bloqueante de trazabilidad del Anexo B)
  - **IN-02**: actualizar la tabla de estado de `V4/GUIA_EJECUCION.md` con B4 marcado como ejecutado, la fecha de la corrida y la limitación de `r/derechogenial`
  - **IN-05**: revisión editorial de los 10 archivos de `knowledge-base/` — español técnico, sin términos en inglés ni errores de tipeo, antes de que la KB se use como fuente del documento final
  - Congelar la versión del workflow que se usa como Anexo B y registrar su hash, para que E1 y la Figura 3 sean el mismo artefacto
  - Actualizar `knowledge-base/02_descripcion_general.md` §Estado de implementación si la corrida más reciente difiere de la registrada
  - Sin tocar el DDL ni la lógica del pipeline: este change es documental
- **Dependencias**: C-04
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/10_preguntas_abiertas.md` §Inconsistencias detectadas
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios
  - `knowledge-base/02_descripcion_general.md` §Estado de implementación
  - `V4/GUIA_EJECUCION.md` §Estado actual

---

### [C-07] `semantica-ingested-at`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **IN-03**: fijar la sentencia final de `Upsert Posts` dejando explícito qué campos se actualizan en el `ON CONFLICT (id) DO UPDATE` y que `ingested_at` **no** se toca, para preservar la latencia de la primera ingesta (RN-PE-03, DD-04)
  - Verificar la semántica con una **segunda corrida controlada**: comprobar que `COUNT(*)` no crece y que `ingested_at` es idéntico al de la corrida original para los mismos ids
  - Registrar la sentencia final en `V4/anexos/A_DDL.sql` o en un anexo de workflow, para que el Cap. 4 pueda mostrar la persistencia que garantiza la idempotencia (m-18)
  - Si la corrección implica regenerar el workflow, hacerlo desde `V4/scripts/generar_workflow.py` y reasignar la credencial Postgres tras la importación
  - Debe cerrar **antes** de C-08: E6 (latencia) se calcula sobre `ingested_at` y sería inválida si el upsert lo sobreescribe
- **Dependencias**: C-04
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/10_preguntas_abiertas.md` §IN-03
  - `knowledge-base/04_modelo_de_datos.md` §Entidades (posts)
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: persistencia (RN-PE-02, RN-PE-03)
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-04

---

## FASE 2 — Evidencias cuantitativas del sistema (B6)

> Todo se cuenta con SQL sobre la base real. Si una consulta no alcanza, se retira la métrica — no se completa con datos de versiones anteriores.

### [C-08] `evidencias-e4-tabla3-y-e6-latencia`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **E4 (Tabla 3 reconstruida)**: `SELECT COALESCE(nlp_category,'No relevante') AS categoria, COUNT(*) AS n, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (),2) AS pct FROM posts GROUP BY nlp_category ORDER BY n DESC` — recuentos **contados**, con la fila residual rotulada `No relevante (salida del clasificador)`; prohibido derivar el residual de una tasa (N-02)
  - **E6 (latencia publicación→ingesta)**: `SELECT COUNT(*), AVG/PERCENTILE_CONT(0.50)/PERCENTILE_CONT(0.95) de EXTRACT(EPOCH FROM (ingested_at - to_timestamp(created_utc)))/60.0` con `WHERE created_utc IS NOT NULL AND created_utc > 0`; reportar `n`, media, DS, P50 y P95
  - Decidir el criterio de latencia del §1.6: si P95 supera 5 min, **declarar NO CUMPLIDO con justificación** o ajustar el scheduler a 5 min verificando la cuota — nunca ambos (N-01)
  - Exportar cada salida a `V4/evidencias/` con la consulta usada, la fecha y el `n` de la ventana (Flujo 3, RN-GL-01)
  - Separar throughput operativo (4 ejecuciones/h × 100 ítems = 400/h) de métricas de banco de pruebas (H-06)
- **Dependencias**: C-05, C-07
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/07_flujos_principales.md` §Flujo 3: Consulta de evidencia
  - `knowledge-base/04_modelo_de_datos.md` §Entidades (posts)
  - `knowledge-base/05_reglas_de_negocio.md` §Excepciones globales
  - `knowledge-base/01_vision_y_objetivos.md` §Métricas de éxito

---

### [C-09] `evidencias-e7-motor-anomalias`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **E7**: volcado de `anomalias` con `ventana_inicio`, `ventana_fin`, `categoria`, `n_observado`, `base_media`, `umbral`, `disparo` — **todas** las evaluaciones, disparen o no (RN-AN-04)
  - Reportar el **número real de disparos** de la ventana; con base histórica corta se reporta como limitación, no como ausencia de anomalías (RN-AN-06)
  - Validar los casos de phishing detectados contra el motor real: informar si fueron **detectados por el motor** o **identificados después** en el análisis (H-03)
  - Justificar formalmente el umbral `max(cuantil 95 de Poisson, 3)` frente a la media de los 10 días previos, con el argumento de por qué `μ+2σ` no explica conteos pequeños y variables (N-04, DD-05)
  - Export de `alertas` con `canal`, `estado` y `payload`, aclarando que Telegram está deshabilitado por defecto
- **Dependencias**: C-05, C-08
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/07_flujos_principales.md` §Flujo 2: Evaluación diaria de anomalías
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: anomalías y alertas (RN-AN)
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-05, §DD-07
  - `knowledge-base/06_funcionalidades.md` §US-007, §US-008

---

### [C-10] `evidencias-e5-matriz-confusion`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **E5**: construir la **matriz de confusión 6×6** (5 categorías taxonómicas + `No relevante`) de la muestra de control: etiquetas humanas vs. `nlp_category` predicha
  - Constituir la muestra de control con el **n declarado** y el criterio de muestreo documentado; muestreo estratificado sobre la base real, nunca sobre cifras de V2/V3
  - Script en `V4/scripts/` que calcula la matriz desde dos CSV (etiquetas humanas + predicciones) y la persiste como evidencia fechada
  - Fórmula explícita de la **tasa de falsos positivos** en 3.3 (H-04) y reportar intervalos de confianza
  - Regla de desempate del etiquetado a 3 votos (H-13); evaluar y documentar el sesgo de evaluación endógena
  - Mantener separados los conteos de comentarios: `comments` no es poblada por el pipeline RSS, la Tabla 2 se reconstruye solo con posts (m-16)
  - **Bloqueado por**: definir la submuestra de control y obtener los 3 votos (decisión de los autores)
- **Dependencias**: C-08
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-010
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: clasificación y entidades (RN-CL-01, RN-CL-05)
  - `knowledge-base/10_preguntas_abiertas.md` §Preguntas abiertas priorizadas
  - `knowledge-base/01_vision_y_objetivos.md` §Métricas de éxito

---

### [C-11] `evidencias-e8-captura-recaptura`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **E8**: ejecutar el protocolo captura–recaptura sobre la ventana real — dos capturas, `n₁`, `n₂`, `m`, `N̂`, cobertura `n₁/N̂` e intervalo de confianza — con la tabla completa archivada en `V4/evidencias/`
  - Discutir la **independencia de los canales** de captura; es la debilidad conocida del método y debe declararse (H-05)
  - **Decisión de cierre explícita**: si el protocolo no puede sostenerse con la fuente RSS, **retirar la métrica de cobertura** de §1.6, §5.2, Resumen y Conclusiones — retirarla es la salida honesta, no dejarla como "parcial" sin justificar
  - Registrar la decisión en OpenSpec como cambio de alcance (RN-GL-03)
- **Dependencias**: C-05
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/01_vision_y_objetivos.md` §Métricas de éxito
  - `knowledge-base/05_reglas_de_negocio.md` §Excepciones globales (RN-GL-01, RN-GL-02)
  - `knowledge-base/10_preguntas_abiertas.md` §Preguntas abiertas priorizadas

---

## FASE 3 — Evidencias estructurales, anexos y evaluación externa

> No dependen de que la ventana se cierre: se producen sobre artefactos que ya existen. Conviene lanzarlas en paralelo con la FASE 2.

### [C-12] `evidencias-artefacto-e1-e2-e3-e10`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **E1**: export JSON del workflow desde la instancia real de n8n, **verificado como importable** y sin secretos (la credencial Postgres no viaja en el JSON)
  - **E2**: captura de pantalla del workflow en la interfaz de n8n mostrando los nodos visibles, incluido el subflujo de alertas; alimenta la Figura 3
  - **E3**: volcado del DDL realmente ejecutado en B2 (`\d+` o export del esquema), que es la fuente de la tabla de atributos del Cap. 4 y de la Figura 2 (DER)
  - **E10**: URL pública del repositorio Git con acceso para el auditor → Anexo D; **hoy `V4/anexos/` solo contiene A y B, C y D no existen** (H-07)
  - Verificar que `crypto` y `$env` están habilitados en la configuración de n8n y dejarlo asentado junto al export (H-01c)
  - Archivar todo en `V4/anexos/` y `V4/evidencias/` con fecha en el nombre
- **Dependencias**: C-06
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios
  - `knowledge-base/04_modelo_de_datos.md` §Entidades
  - `knowledge-base/06_funcionalidades.md` §US-009

---

### [C-13] `anexo-c-diccionario-taxonomico-e11`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **E11**: extraer del nodo Code del workflow el **diccionario taxonómico completo** — las 5 categorías y todas sus palabras — y publicarlo como `V4/anexos/C_diccionario.md` (cierra US-005)
  - Documentar la **fórmula exacta del score** y su normalización a `[0,1]`, con ejemplos calculados a mano que se puedan verificar contra `posts.nlp_score` de la base (H-17)
  - Documentar el **componente de extracción de entidades**: qué reconoce (CVE, emails, IPs, dominios, productos), con qué expresión y con 3–5 ejemplos reales tomados de `posts.entities` (N-06)
  - Si el diccionario no puede documentarse completo, **reclasificar OE4** en lugar de dejarlo en el respaldo de la categoría vacía
  - La matriz de confusión de C-10 se calcula contra estas categorías: cualquier cambio acá obliga a recalcularla
- **Dependencias**: C-06
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: clasificación y entidades (RN-CL)
  - `knowledge-base/06_funcionalidades.md` §US-005, §US-006
  - `knowledge-base/04_modelo_de_datos.md` §Entidades (posts)
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-05

---

### [C-14] `entorno-y-canales-e9-e12-e13`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **E9**: especificación del entorno de pruebas **real** usado en B1 — hardware, versiones exactas (PostgreSQL 18, n8n 2.22.6), puerto `5433`, sistema operativo — con fecha de relevamiento
  - **E12**: si el motor de anomalías dispara y el nodo Telegram se habilita, obtener **captura de la alerta real**; si no se obtiene, **reclasificar OE6** y ajustar título, Resumen, Abstract y §7.1 (IN-04, H-02, M-01)
  - **E13**: datos de los subreddits con **fecha de relevamiento** de suscriptores, obtained del relevamiento real y no de la API de Reddit (M-08)
  - Dejar asentado que `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` nunca se versionan
  - **Bloqueado por**: decisión de los autores sobre habilitar Telegram o retirar/reclasificar OE6
- **Dependencias**: C-06
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/02_descripcion_general.md` §Integraciones externas
  - `knowledge-base/08_arquitectura_propuesta.md` §Variables de entorno
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-07, §SU-03
  - `knowledge-base/10_preguntas_abiertas.md` §IN-04

---

### [C-15] `evaluador-externo-e14`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **E14**: obtener la **submuestra de 100 posts etiquetada por un evaluador externo** (no por los autores del pipeline) para la evaluation independiente
  - Calcular **Kappa de Fleiss** contra el consenso interno de C-10 y reportarlo con su `n` e intervalo de confianza
  - Definir el **control de acceso mínimo** del evaluador: extract exportable con `nlp_category` y las entidades, sin `author_hash` ni datos que permitan reidentificación (RN-PS-04, m-19)
  - Documentar la política de **enmascaramiento de atributos indirectos**: sector + provincia + tipo + fecha pueden reidentificar aunque el autor esté seudonimizado
  - Si no se consigue evaluador externo, **declararlo como limitación explícita** del Cap. 6 y no simular el consenso
  - **Bloqueado por**: pregunta abierta de prioridad alta — disponibilidad de la submuestra (autores / facultad)
- **Dependencias**: C-10
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §Actores del sistema
  - `knowledge-base/06_funcionalidades.md` §US-010
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: seudonimización (RN-PS-04)
  - `knowledge-base/10_preguntas_abiertas.md` §Preguntas abiertas priorizadas

---

## FASE 4 — Reconstrucción del documento sobre base V2

> Regla de la devolución V3 (N-03): la V4 se construye **sobre la base textual de la V2**, no sobre la V3. Corregir significa **agregar evidencia**, nunca borrar contenido. Los Capítulos 3 y 4 deben recuperar la extensión que tenían en V2.

### [C-16] `normalizacion-base-textual-v2`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - `V4/devoluciones/tesis_v2.txt` ya existe (extracción hecha); falta **normalizar**: acentos rotos, saltos de línea de la extracción, caracteres de viñeta, comillas
  - Seccionar el texto normalizado **un archivo por capítulo** en `V4/capitulos/`, respetando la numeración original de V2 para que las restituciones sean verificables contra la fuente
  - Marcar en cada capítulo los **tramos que V3 eliminó** y que deben restituirse: entorno de benchmarking 5.2, tabla de atributos 4.2, diseño muestral y regla de resolución de discrepancias 3.3, priorización del Cap. 8, citas del marco conceptual 2.1.3, nodos del Anexo B, ejemplos de modismos ("caer", "pescar", "cangrejo")
  - Entregable: corpus base limpio del cual los capítulos se reescriben sin copiar-pegar a ciegas
  - Reglas de forma a aplicar de arranque: separador decimal coma (`0,78`), APA 7, declaración de autoría precisa (m-17)
- **Dependencias**: ninguna
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/01_vision_y_objetivos.md` §Propósito del sistema
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios
  - `knowledge-base/10_preguntas_abiertas.md` §IN-05

---

### [C-17] `antecedente-e15-rivas-dengra`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **E15**: conseguir en la biblioteca de la facultad una **copia del TFI de Rivas y Dengra (2026)**, el antecedente más directo (H-10)
  - Si se consigue: subsección de **contraste explícito** con ese trabajo en §2.2, con la diferencia de alcance, fuente de datos y método
  - Si no se consigue: documentar en §2.2 que el antecedente se cita por referencia bibliográfica sin acceso al texto completo, y ajustar la afirmación de "antecedente directo" en lugar de simular la lectura
  - Registrar el intento de búsqueda con fecha, para que la ausencia sea una decisión trazable y no un olvido
  - **Bloqueado por**: pregunta abierta de prioridad baja — disponibilidad en biblioteca
- **Dependencias**: ninguna
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/10_preguntas_abiertas.md` §Preguntas abiertas priorizadas
  - `knowledge-base/01_vision_y_objetivos.md` §Objetivos por actor
  - `knowledge-base/09_decisiones_y_supuestos.md` §Supuestos inferidos

---

### [C-18] `capitulo-1-2`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **Cap. 1 (§1.6)**: certificar que los umbrales de éxito son **idénticos a los de V2**; si alguno cambió, declararlo y justificarlo (N-05); incorporar el umbral de **F1** o retirarlo de la evaluación; eliminar la redundancia `precisión ≥ 82% ⇔ FP ≤ 18%` (misma medida dos veces); revisar coherencia entre el criterio de latencia y el scheduler de 15 min contra la latencia real de C-08
  - **Cap. 2 (§2.1, §2.1.3, §2.2)**: citar las fuentes del marco con APA 7; **usar Liao et al. (2016) como antecedente directo** y no como apoyo de una afirmación que describe (m-14); restituir los ejemplos de modismos que sostienen la brecha de NLP argentino (H-09); agregar el contraste con Rivas y Dengra (C-17) o su ausencia documentada; verificar CABASE y Fortinet con URL y fecha de consulta
  - Si se conserva la métrica de cobertura, exigir el protocolo de C-11; si no, retirarla de §1.6 (H-05)
  - Extensión: recuperar el detalle de V2 en el marco teórico, sin agregar afirmaciones sin fuente
- **Dependencias**: C-16, C-17, C-06
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/01_vision_y_objetivos.md` §Alcance v4.0, §Métricas de éxito
  - `knowledge-base/02_descripcion_general.md` §Estado de implementación
  - `knowledge-base/10_preguntas_abiertas.md` §Inconsistencias detectadas
  - `knowledge-base/06_funcionalidades.md` §US-009

---

### [C-19] `capitulo-3-4`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **Cap. 3 (§3.3, §3.4)**: fórmula explícita de la **tasa de falsos positivos** (pedida desde V2); **restituir el diseño muestral y la regla de resolución de discrepancias** — el aporte metodológico más sólido según V2, borrado en V3; declarar el `n` de la muestra de control y de cada métrica; terminología exacta **"HMAC-SHA-256 con clave secreta por despliegue"** (no "SHA-256 con salt" ni "dinámica"); párrafo de gestión de clave (generación, custodia, rotación) y **riesgo residual** (el seudonimizado sigue siendo dato personal, Ley 25.326); política de enmascaramiento de atributos indirectos
  - **Cap. 4 (§4.1–§4.5)**: descripción **completa** de la arquitectura + Figura 1 (V3 la redujo a una oración); **tabla de atributos como espejo EXACTO del DDL** de E3 (V3 la eliminó en vez de alinearla); resolver `pg_trgm` (eliminarlo o justificarlo); **sentencia de persistencia** de C-07 que garantiza la idempotencia de OE2; scheduler 15 min vs. latencia medida en C-08; **función de puntuación y normalización** de C-13; **componente de extracción de entidades** de C-13; **§4.5 nueva: formalizar el motor de anomalías** (variable, ventana, base, umbral, regla de disparo) con la justificación de C-09
  - **Cap. 4 es el núcleo de la evaluación**: debe ser el capítulo más extenso
  - Ninguna afirmación de diseño sin respaldo en `V4/anexos/` o en la base
- **Dependencias**: C-18, C-13, C-07, C-12
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Entidades
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: seudonimización (RN-PS)
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: anomalías y alertas (RN-AN)
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-03, §DD-04, §DD-05

---

### [C-20] `capitulo-5-6`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **Cap. 5 (§5.2, §5.3)**: **Tabla 3 desde SQL** con la salida de C-08 y el residual rotulado; **explicar por qué los recuentos difieren de V2** (la ventana cambió, RN-GL-02); **matriz de confusión 6×6** de C-10; reportar `n`, media, DS, P50, P95 de latencia y el throughput de C-08; separar métricas **operativas vs. banco de pruebas**; validar los 3 casos contra el motor real y reportar el **número real de disparos** de C-09
  - **Cap. 6 (§6.1–§6.3)**: reescribir la comparación con la literatura sobre **estimación de amenazas reales corregida por precisión**, no sobre salidas crudas del clasificador (N-02); precisar **qué dato exacto** del informe Fortinet se contrasta (categoría, porcentaje, página); citar fuentes primarias de penetración de plataformas con URL y fecha o reformular en términos cualitativos; mantener el sesgo de evaluación endógena como **limitación declarada** e incorporar la regla de desempate del etiquetado
  - Cada tabla y cada cifra del capítulo **deben apuntar a su archivo en `V4/evidencias/`** con fecha y consulta
  - Ninguna cifra que provenga de V2/V3 sobrevive sin recalcularse contra la base
- **Dependencias**: C-19, C-08, C-09, C-10, C-11
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/07_flujos_principales.md` §Flujo 3: Consulta de evidencia
  - `knowledge-base/01_vision_y_objetivos.md` §Métricas de éxito
  - `knowledge-base/05_reglas_de_negocio.md` §Excepciones globales
  - `knowledge-base/06_funcionalidades.md` §US-009, §US-010

---

### [C-21] `capitulo-7-8-resumen-titulo`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **Cap. 7 (§7.1–§7.3)**: alinear el estado de **OE5 y OE6** con lo realmente implementado (H-02, H-03); **conservar la honestidad epistémica de PI-1** — la comparación con soluciones propietarias no ejecutada, que el tribunal valoró en V2; corregir la afirmación de anexos disponibles según lo que exista realmente en `V4/anexos/` al momento del cierre
  - **Cap. 8**: **restituir la priorización por esfuerzo e impacto** de las recomendaciones (N-03)
  - **Resumen y Abstract**: espejo exacto el uno del otro, con las métricas reales del Cap. 5; **no afirmar "se superaron todos los umbrales"** (M-01)
  - **Título**: evaluar si sigue siendo correcto si OE6 se reclasifica (H-02)
  - Separador decimal coma de forma consistente en todo el documento (Kappa `0,78`, no `0.78`) y **arreglar los redondeos** de los ítems heredados de V2/V3 (m-13, m-15)
- **Dependencias**: C-20
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/01_vision_y_objetivos.md` §Alcance v4.0, §Fuera de alcance
  - `knowledge-base/02_descripcion_general.md` §Estado de implementación
  - `knowledge-base/10_preguntas_abiertas.md` §Inconsistencias detectadas
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-07

---

## FASE 5 — Cierre, figuras y auto-auditoría

### [C-22] `figuras-2-3-4-e-indices`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - **Figura 2 (DER)**: generar desde el DDL real de C-12, con `matplotlib` o herramienta equivalente; debe reflejar `RESTRICT` en `posts.subreddit_id` y las cinco tablas
  - **Figura 3 (captura n8n)**: usar la captura E2 de C-12, con el conteo de nodos **corregido** según C-06
  - **Figura 4 (serie temporal por categoría)**: generar desde la salida real de la serie horaria (`date_trunc('hour', ingested_at)` × `nlp_category`); **nunca** con datos de V2/V3
  - **Figura 1** ya existe (`V4/figuras/Figura_1_arquitectura.png`): solo verificar que coincide con la arquitectura descrita en Cap. 4 tras C-19
  - Índice de tablas y figuras automático tras el índice general, con numeración verificada (H-14, M-05)
  - Guardar los PNG en `V4/figuras/` y el script generador en `V4/scripts/` para que sean reproducibles
- **Dependencias**: C-12, C-08
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §ERD
  - `knowledge-base/02_descripcion_general.md` §Arquitectura general
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios
  - `knowledge-base/07_flujos_principales.md` §Flujo 3: Consulta de evidencia

---

### [C-23] `auto-auditoria-final`
- **Estado**: `[ ]` pendiente
- **Scope**:
  - Recalcular **todas** las cifras verificables del documento (Tablas 1–5, F1, FP, latencias, ratios, redondeos) con un script en `V4/scripts/` y contrastarlas contra la base
  - Verificar **correspondencia** cuerpo ↔ anexos ↔ índice ↔ figuras, y que cada anexo citado exista en `V4/anexos/`
  - Construir la **matriz de trazabilidad final** OE ↔ resultados ↔ evidencia, con una fila por objetivo de estudio
  - Recorrer la **lista completa de hallazgos** H-01…H-17, M-01…M-12, N-01…N-06, m-13…m-20 y marcar cada uno **RESUELTO / PARCIAL / NO RESUELTO** con su evidencia
  - Chequeo **APA 7**: cada referencia citada y cada cita referenciada, con URL y fecha de recuperación en fuentes institucionales
  - Ensamblado final en `.docx` (ya disponible: `python-docx` + `matplotlib`) con estilos de título, TOC automático y anexos; verificar que **ninguna cifra del documento final provenga de V2/V3**
  - Declarar con precisión las herramientas generativas usadas y su uso (m-17)
- **Dependencias**: C-21, C-22
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/05_reglas_de_negocio.md` §Excepciones globales
  - `knowledge-base/10_preguntas_abiertas.md` §Inconsistencias detectadas
  - `knowledge-base/01_vision_y_objetivos.md` §Métricas de éxito
  - `knowledge-base/03_actores_y_roles.md` §Actores del sistema
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-01

---

## Resumen de changes

| ID | Change | Fase | Estado | Dep. | Governance |
|---|---|---|---|---|---|
| C-01 | `entorno-postgres-n8n` | 0 | `[x]` verificado | — | BAJO |
| C-02 | `modelo-ddl-tesi-osint` | 0 | `[x]` verificado | C-01 | CRITICO |
| C-03 | `workflow-n8n-generado-e-importado` | 0 | `[x]` verificado | C-02 | ALTO |
| C-04 | `corrida-b4-ingesta-rss` | 0 | `[x]` verificado | C-03 | ALTO |
| C-05 | `ventana-recoleccion-b5` | 1 | `[ ]` pendiente | C-04 | MEDIO |
| C-06 | `sincronizacion-documental-v4` | 1 | `[ ]` pendiente | C-04 | BAJO |
| C-07 | `semantica-ingested-at` | 1 | `[ ]` pendiente | C-04 | ALTO |
| C-08 | `evidencias-e4-tabla3-y-e6-latencia` | 2 | `[ ]` pendiente | C-05, C-07 | MEDIO |
| C-09 | `evidencias-e7-motor-anomalias` | 2 | `[ ]` pendiente | C-05, C-08 | ALTO |
| C-10 | `evidencias-e5-matriz-confusion` | 2 | `[ ]` pendiente | C-08 | ALTO |
| C-11 | `evidencias-e8-captura-recaptura` | 2 | `[ ]` pendiente | C-05 | MEDIO |
| C-12 | `evidencias-artefacto-e1-e2-e3-e10` | 3 | `[ ]` pendiente | C-06 | MEDIO |
| C-13 | `anexo-c-diccionario-taxonomico-e11` | 3 | `[ ]` pendiente | C-06 | MEDIO |
| C-14 | `entorno-y-canales-e9-e12-e13` | 3 | `[ ]` pendiente | C-06 | MEDIO |
| C-15 | `evaluador-externo-e14` | 3 | `[ ]` pendiente | C-10 | ALTO |
| C-16 | `normalizacion-base-textual-v2` | 4 | `[ ]` pendiente | — | BAJO |
| C-17 | `antecedente-e15-rivas-dengra` | 4 | `[ ]` pendiente | — | BAJO |
| C-18 | `capitulo-1-2` | 4 | `[ ]` pendiente | C-16, C-17, C-06 | MEDIO |
| C-19 | `capitulo-3-4` | 4 | `[ ]` pendiente | C-18, C-13, C-07, C-12 | ALTO |
| C-20 | `capitulo-5-6` | 4 | `[ ]` pendiente | C-19, C-08, C-09, C-10, C-11 | ALTO |
| C-21 | `capitulo-7-8-resumen-titulo` | 4 | `[ ]` pendiente | C-20 | MEDIO |
| C-22 | `figuras-2-3-4-e-indices` | 5 | `[ ]` pendiente | C-12, C-08 | BAJO |
| C-23 | `auto-auditoria-final` | 5 | `[ ]` pendiente | C-21, C-22 | ALTO |

**Cobertura de evidencias E1–E15:** E1, E2, E3, E10 → C-12 · E4, E6 → C-08 · E5 → C-10 · E7 → C-09 · E8 → C-11 · E9, E12, E13 → C-14 · E11 → C-13 · E14 → C-15 · E15 → C-17.

**Primer change recomendado:** `C-05` `ventana-recoleccion-b5` — no produciría artefactos por sí solo, pero es el **reloj del proyecto**: la ventana real define qué métricas son calculables, y todo el tramo crítico pendiente cuelga de ella. Si los autores quieren producir artefactos visibles en el primer paso, el paralelo natural es `C-16` (normalizar la base textual de V2), que no depende de nada.

```text
/opsx:propose C-05-ventana-recoleccion-b5
```
