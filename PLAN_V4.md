# PLAN DE TRABAJO — TFI OSINT/n8n — Versión 4 (V4)

**Autores:** Valentino Lorca · Jerónimo Zúñiga · Enzo Severino
**Instancia actual:** V3 = 5,5/10 — NO APROBADO — Reentrega obligatoria (V4)
**Objetivo:** Habilitar la defensa cerrando los **8 ítems bloqueantes** y la mayor cantidad posible de los de prioridad alta → proyección del tribunal: **8,0–8,5**. Con evaluador externo + estimación de amenazas reales: **> 8,5**.

> ⚠️ **REALIDAD CONFIRMADA (2026-09-23): el sistema NO está construido.** No existe base PostgreSQL, no existe workflow n8n, no existen datos medidos. Los números de V2/V3 (8.240 posts, F1 0,815, Kappa 0,78, etc.) fueron inventados por las IAs que redactaron las versiones anteriores. El auditor de los directores es una IA que corrige sobre el documento — detecta inconsistencias pero no accede a un sistema real. **La V4 se convierte en un TFI de PROTOTIPO REAL: construir el sistema, correrlo, y documentar lo que produce.** No se fabrica nada; los números salen del sistema que vamos a construir.

---

## 0. La idea central (leer primero)

**Dos frentes simultáneos:**

1. **La V4 se construye sobre la base textual de la V2, NO sobre la V3.** El auditor fue explícito (N-03): la V3 respondió las correcciones **borrando contenido** en vez de **agregar evidencia**, y pasó de 34 a 24 páginas. *"Construir la V4 sobre la base textual de la V2, incorporando sobre ella las correcciones de ambas instancias. Los Capítulos 3 y 4 deben recuperar al menos la extensión y el nivel de detalle que tenían en V2."*
2. **El sistema se construye DE CERO y produce la evidencia.** Ya no se pide "material que solo los autores aportan" porque no existe nada que aportar: hay que **montar el prototipo real** (workflow n8n + PostgreSQL + clasificador), **dejarlo correr semanas**, y de esa corrida salen las evidencias E1–E15.

**Modelo de trabajo (dos columnas paralelas):**

| Columna A — Documento (hace la IA desde acá) | Columna B — Sistema real (los autores EXECUTAN; la IA les entrega el código) |
|---|---|
| Reconstruir y redactar capítulos sobre base V2 | Instalar entorno (Docker / PostgreSQL / n8n / Node.js) |
| Aplicar correcciones de método y redacción | Importar workflow n8n (lo genera la IA, se importa en 2 clics) |
| Figuras 1, 2 y 4 (arquitectura, DER, series) | Correr el flujo y dejar que recolecte datos reales |
| Matriz de trazabilidad y verificación numérica | Ejecutar consultas SQL → salidas para Tabla 3, latencia, etc. |
| Índice, formato APA 7, anexos C y D | Capturas del workflow y de las tablas pobladas (Figura 3) |
| Auto-auditoría final tipo auditor-doc | Matriz de confusión 6×6, protocolo captura-recaptura, repo URL |

⚠️ **Regla de honestidad (absoluta):** NO se fabrican datos. El sistema real se construye, corre y produce los números. Si algo no alcanza a medirse, se reclasifica el objetivo o se retira la métrica — el auditor ya demostró que detecta cifras inventadas (N-02 llegó a deducir que una fila de la Tabla 3 fue *derivada aritméticamente*, no contada).

---

## 1. Fase 0 — Preparación del entorno (desde acá)

1. ✅ Estructura de trabajo creada (2026-09-23):
   ```
   C:\Users\valen\Desktop\Tesis\V4\
   ├── capítulos\        (un .md por capítulo, se ensambla al final)
   ├── figuras\          (PNG generados — Figura 1 ya generada)
   ├── anexos\           (A: DDL, B: workflow exportado, C: diccionario, D: repo)
   ├── evidencias\       (SQL, salidas, capturas producidas por el sistema)
   ├── scripts\          (consultas SQL, scripts de métricas, ensamblador docx, figuras)
   └── devoluciones\     (copias de las dos devoluciones, ya extraídas a texto)
   ```
2. ✅ Figura 1 (arquitectura E2E) generada: `V4\figuras\Figura_1_arquitectura.png` (ver §8).
3. Normalizar base textual V2: limpiar el texto extraído de `tesis_v2.pdf` (acentos, saltos de línea de la extracción) y seccionarlo por capítulo.
4. Inicializar `git` en la carpeta para versionar cada iteración.
5. Herramientas: Python 3.14 + `pypdf` + `python-docx` + `matplotlib` (instaladas). El docx final se genera con un script de ensamblado.

---

## 1b. Fase 0.5 — Los autores aprenden el sistema (NO negociable, 2-3 días)

Sin entender el sistema, la defensa es imposible. Material (lo entrega la IA desde acá):

- [ ] **Guía de conceptos en criollo** (`V4\GUIA_CONCEPTOS.md`): qué es OSINT, qué es n8n (nodos, workflow, trigger, credenciales), qué es PostgreSQL, qué hace cada etapa del pipeline de la Figura 1.
- [ ] **Recorrer la Figura 1** con la guía: entender por qué hay un trigger cada 15 min, qué hace el HTTP Request, qué es la seudonimización HMAC, qué guarda la base, cómo clasifica y cómo "suena" la alarma.
- [ ] **Definir en una frase cada objeto de estudio** (OE1–OE8) con palabras propias — si no pueden explicarlo, todavía no está aprendido.
- [ ] Reglas de forma: separador decimal (0,78), APA 7, declaración de autoría precisa (m-17).

---

## 2. Fase 1 — Construir el prototipo real (Columna B — autores ejecutan, IA entrega código)

**Objetivo:** que exista un sistema REAL andando y recolectando datos. Sin esto no hay evidencia. Orden:

| Paso | Qué | Quién |
|---|---|---|
| B1 | **Instalar el entorno** en la máquina: Docker Desktop (o PostgreSQL + Node.js) y n8n (npm o Docker) | Autores (guía paso a paso que entrega la IA) |
| B2 | **Crear la base** con el DDL real (Anexo A corregido según N-06: columnas score, entidades, anomalías, alertas, latencias) | Autores ejecutan el SQL que entrega la IA |
| B3 | **Importar el workflow n8n** (JSON generado por la IA, importable en 2 clics) y configurar credenciales (Reddit OAuth2, Telegram opcional) | Autores importan; IA entrega |
| B4 | **Correr el flujo** y verificar que puebla la base (sample de filas + captura) | Autores |
| B5 | **Dejar recolectar semanas** (ventana REAL de datos: la tesis ya NO dirá "6 meses" — se redefinirá la ventana al período real, ajustando criterios y tablas; el auditor acepta ajustes justificados) | Autores (el sistema corre solo) |
| B6 | **Producir evidencias E1–E15** desde el sistema real (export, SQL, capturas, matriz) | Autores + IA (consultas listas en §7) |

**Evidencias que produce el sistema → listas E1–E15 (se entregan en `V4\evidencias\`):**

| # | Material | Sirve para | Detalle técnico |
|---|---|---|---|
| E1 | **Export JSON real del workflow n8n** | H-15, Anexo B | n8n → Export workflow. Verificar que sea importable (borra secretos). |
| E2 | **Captura del workflow en n8n** (pantalla) | H-11, Figura 3 | Mostrar nodos visibles, incluido el subflujo de alertas. |
| E3 | **DDL real de la base** (el que se ejecutó en B2) | H-16, N-06, Anexo A | Con columnas score, entidades, anomalías, alertas. |
| E4 | **Salida de la consulta SQL de la Tabla 3** | H-07, N-02 | Consulta lista en §7 — recuentos CONTADOS con residual. |
| E5 | **Matriz de confusión 6×6** de la muestra de control | H-04 | Etiquetas humanas vs. predicciones del sistema (500+ posts). |
| E6 | **Medición de latencia publicación→ingesta** | N-01, H-12 | `ingested_at − created_utc`, n, media, P50, P95. Query en §7. |
| E7 | **Registro de disparos del motor de anomalías** | H-03, N-04, OE5 | Tabla `anomalias` poblada por el motor real. |
| E8 | **Protocolo captura-recaptura ejecutado** | H-05 | Ventana, n₁, n₂, m, N̂, IC — o retirar la métrica de cobertura. |
| E9 | **Especificación del entorno de pruebas** (hardware, versiones) | H-06 | Del entorno REAL usado en B1. |
| E10 | **URL del repositorio** (git) con acceso al auditor | Anexo D, H-07 | Inicializado en Fase 0. |
| E11 | **Diccionario taxonómico completo** (palabras por categoría) | Anexo C, H-07, H-17 | El corazón del clasificador — el que entra en el nodo Code. |
| E12 | **Captura de al menos una alerta real** (Telegram/webhook) | H-02, OE6 | Si el motor disparó → captura. Si no → reclasificar OE6. |
| E13 | **Datos de subreddits con fecha de relevamiento** (suscriptores) | M-08 | Del relevamiento REAL. |
| E14 | **Submuestra etiquetada por evaluador EXTERNO** (100 posts) | H-13 (sube nota) | Kappa de Fleiss contra consenso interno. |
| E15 | **Copia del TFI de Rivas y Dengra (2026)** si existe en la facultad | H-10 | Antecedente directo de la UTN. |

**Prioridad para desbloquear (lo que más aporta):** E4, E6, E7, E3, E1, E2. Con esos 6 + la ventana real, se cierran los bloqueantes 2, 3, 4, 7 y 8.

---

## 3. Fase 2 — Reconstrucción del cuerpo (base V2 + correcciones)

Estrategia: tomar el texto de la V2, y **mientras se reescribe**, aplicar las correcciones. No copiar-pegar a ciegas: cada sección se revisa contra las dos devoluciones.

### Capítulo 1 — Introducción
- [ ] 1.6: criterios de éxito → **certificar que los umbrales son idénticos a los de V2**; si alguno cambió, declararlo y justificarlo (N-05).
- [ ] 1.6: incorporar el **umbral de F1** (o retirarlo de la evaluación) (N-05).
- [ ] 1.6: **eliminar la redundancia** precisión ≥ 82% ⇔ FP ≤ 18% (misma medida dos veces) (N-05).
- [ ] 1.6: revisar el criterio de latencia: el de V2 dice "P95 ≤ 5 min" — verificar coherencia con el scheduler (N-01).
- [ ] 1.6: si se conserva cobertura, exigir protocolo; si no, **retirar la métrica** (H-05).

### Capítulo 2 — Marco teórico y estado del arte
- [ ] 2.2: **agregar subsección de contraste explícito con Rivas y Dengra (2026)**, el antecedente más directo (H-10).
- [ ] 2.2: **restituir los ejemplos de modismos** ("caer", "pescar", "cangrejo") que sostienen la brecha de NLP argentino (H-09, N-03).
- [ ] 2.1.3: citar las fuentes del marco (Honnibal et al. 2020, Liao et al. 2016, etc.) (H-10, m-14).
- [ ] 2.1: verificar el uso de **Liao et al. (2016)**: es extracción de IoC desde fuentes técnicas, no reconocimiento activo de infraestructura → usarlo como antecedente directo, no como apoyo de esa afirmación (m-14).

### Capítulo 3 — Marco metodológico y legal *(debe recuperar extensión de V2)*
- [ ] 3.3: **fórmula explícita de la tasa de falsos positivos** (se pedía desde V2) (H-04).
- [ ] 3.3: **restituir el diseño muestral y la regla de resolución de discrepancias** (era "el aporte metodológico más sólido" según V2; V3 lo borró) (N-03).
- [ ] 3.3: declarar n de la muestra de control y de cada métrica (H-12).
- [ ] 3.4: terminología → "**HMAC-SHA-256 con clave secreta por despliegue**", no "SHA-256 con salt" ni "dinámica" (H-01).
- [ ] 3.4: **política de enmascaramiento**: generalizar a atributos indirectos (sector + provincia + tipo + fecha del Caso 2 puede reidentificar) (m-19).
- [ ] 3.4: párrafo de **gestión de clave** (generación, custodia, rotación) y **riesgo residual** (dato seudonimizado sigue siendo dato personal, Ley 25.326) (H-01d).

### Capítulo 4 — Desarrollo del artefacto *(núcleo de la evaluación; debe ser el más extenso)*
- [ ] 4.1: **descripción completa de la arquitectura** + Figura 1 (la V3 lo redujo a una oración) (N-03, H-11).
- [ ] 4.2: **restituir la tabla de atributos** como espejo EXACTO del DDL (V3 la eliminó en vez de alinearla) (H-16, N-03).
- [ ] 4.2: resolver `pg_trgm`: eliminar la creación o justificar su uso (H-16).
- [ ] 4.3: scheduler 15 min vs. latencia → **medir y ajustar** (N-01).
- [ ] 4.3: **mostrar la sentencia de persistencia** (`ON CONFLICT` o equivalente) que garantice la idempotencia de OE2 (m-18).
- [ ] 4.4: **definir formalmente la función de puntuación y su normalización a [0,1]** (el 0,94 del Caso 3 no tiene fórmula) (H-17).
- [ ] 4.4: **describir el componente de extracción de entidades** (modelo, etiquetas, ejemplos) o reclasificar OE4 (N-06).
- [ ] 4.4: citar SpaCy (Honnibal et al. 2020) donde corresponda (H-10).
- [ ] 4.5 (nueva): **formalizar el motor de anomalías**: variable, ventana, base, umbral, regla de disparo + **justificar o reemplazar el umbral μ+2σ** (N-04: ventanas diarias, cuantil de Poisson, mínimo absoluto, EWMA).

### Capítulo 5 — Resultados
- [ ] Tabla 3: **reconstruir desde SQL** sobre la base real, con la fila residual rotulada "No relevante (salida del clasificador)" y el recuento CONTADO (no derivado de la tasa de FP) (H-07, N-02).
- [ ] Tabla 3: **explicar por qué los recuentos cambiaron vs. V2** (mismo corpus, mismas ventanas) (H-07).
- [ ] 5.2: **matriz de confusión 6×6** completa de la muestra de control (H-04).
- [ ] 5.2: separar **métricas operativas vs. métricas de banco de pruebas** (throughput 1.450 vs. techo ~400) (H-06).
- [ ] 5.2: reportar **n, media, DS, P50, P95** de latencia y throughput (H-12).
- [ ] 5.3: **validar los 3 casos contra el motor real** (¿fueron detectados por el motor o identificados después?) (H-03).
- [ ] 5.3: reportar el **número real de disparos de anomalías** del semestre (N-04).

### Capítulo 6 — Discusión
- [ ] 6.1: **reescribir la comparación con la literatura** sobre la estimación de amenazas REALES (corregida por precisión), no sobre salidas crudas del clasificador (N-02).
- [ ] 6.1: **precisar qué dato del informe Fortinet se contrasta** (categoría, porcentaje, página) (H-08).
- [ ] 6.2: citar fuentes primarias de penetración de plataformas con URL y fecha, o reformular en términos cualitativos (H-08).
- [ ] 6.3: mantener sesgo de evaluación endógena como limitación; **agregar regla de desempate del etiquetado** a 3 votos (H-13).

### Capítulo 7 — Conclusiones
- [ ] 7.1: alinear el estado de **OE5 y OE6** con lo realmente implementado (H-02, H-03).
- [ ] 7.2: **conservar la honestidad epistémica de PI-1** (comparación con soluciones propietarias no ejecutada) — el tribunal la valoró (V2).
- [ ] 7.3: corregir la afirmación de anexos disponibles (hoy C y D no existen) (H-07).

### Capítulo 8 — Recomendaciones
- [ ] **Restituir la priorización por esfuerzo e impacto** de las recomendaciones (N-03).

### Resumen / Abstract
- [ ] Resumen y Abstract: **espejo exacto**, con métricas reales y coherentes; **no afirmar "se superaron todos los umbrales"** (M-01) ya que FP está en el límite y OE6 es parcial.

### Título
- [ ] evaluar si el título ("generar alertas tempranas") sigue siendo correcto si OE6 se reclasifica (H-02).

---

## 4. Fase 3 — Los 8 bloqueantes (acciones críticas con método)

Ordenados como los enumera la devolución V3 Sección 9:

1. **Reconstruir sobre base V2** (N-03) → Fase 2 completa. [Bloqueante]
2. **Latencia E2E real** (N-01, H-12): definir el intervalo medido (publicación→ingesta), calcular en la base:
   `SELECT COUNT(*), AVG(.../60), PERCENTILE_CONT(0.5), PERCENTILE_CONT(0.95) FROM posts WHERE created_utc IS NOT NULL AND created_utc > 0` usando `ingested_at − to_timestamp(created_utc)`.
   - Si P95 supera 5 min → **ajustar el scheduler a 5 min o menos** (verificando la cuota de la API) O declarar el criterio NO CUMPLIDO con justificación y vínculo a PI-3. [Bloqueante]
3. **Tabla 3 desde SQL** (N-02, H-07): query en §7; rotular residual; estimar amenazas reales corregidas por precisión; explicar cambios vs. V2. [Bloqueante]
4. **Anexos reales** (H-07, H-15): Anexo B = export real importable (+ verificar `crypto` y `$env` en config n8n, H-01c); Anexo C = diccionario taxonómico; Anexo D = repositorio con URL. [Bloqueante]
5. **Captura-recaptura** (H-05): tabla con ventana, n₁, n₂, m, N̂, cobertura = n₁/N̂, intervalo de confianza, discusión de independencia de canales. Si no: **retirar la métrica** de 1.6, 5.2, Resumen y conclusiones. [Bloqueante]
6. **Fórmula FP + matriz 6×6** (H-04): fórmula en 3.3; matriz como Anexo o en 5.2. [Bloqueante]
7. **Motor de anomalías** (H-03, N-04): algoritmo formal (ventana, base, umbral justificado), registro de disparos del semestre, validación contra los 3 casos de 5.3. [Bloqueante]
8. **Figuras reales + índice de tablas** (H-11): Figura 1 arquitectura, Figura 2 DER, Figura 3 captura n8n (E2), Figura 4 serie temporal por categoría; índice de tablas y figuras tras el índice general. [Bloqueante]

---

## 5. Fase 4 — Hallazgos mayores y de prioridad alta (V3 Sección 9, ítems 9-18)

| # | Acción | Hallazgo | Nota |
|---|---|---|---|
| 9 | Certificar umbrales a priori; F1 en 1.6 o retirarlo; eliminar redundancia precisión/FP; **reportar intervalos de confianza** | N-05 | |
| 10 | **Completar DDL** (score, entidades, anomalías, alertas, latencias) o explicar dónde se persisten; describir extracción de entidades o reclasificar OE4 | N-06 | |
| 11 | Precisar alcance de OE6 (con captura si existe); alinear título, Resumen, Abstract | H-02, M-01 | |
| 12 | Terminología HMAC, config n8n (crypto, $env relativo a NODE_FUNCTION_ALLOW_BUILTIN y N8N_BLOCK_ENV_ACCESS_IN_NODE), gestión de clave y riesgo residual | H-01 | |
| 13 | Criterio y medición de throughput coincidentes; restituir especificación del entorno de pruebas | H-06 | |
| 14 | Citar o retirar las 8 referencias huérfanas; contraste con Rivas y Dengra; completar CABASE y Fortinet (URL, fecha); corregir uso de Liao et al. | H-08, H-10, m-14 | |
| 15 | Regenerar índice automáticamente (TOC de Word); verificar paginación | H-14, M-05 | |
| 16 | Definir función de puntuación y normalización; justificar o eliminar pg_trgm | H-16, H-17 | |
| 17 | Regla de desempate del etiquetado; evaluador externo (recomendado) | H-13 | |
| 18 | Restituir ejemplos de modismos (sostienen la brecha 2.2) | H-09 | |

**Además:** restaurar contenido valorado de V2 (verificado en N-03): entorno de benchmarking 5.2, tabla de atributos 4.2, priorización del Cap. 8, citas del marco conceptual 2.1.3, nodos del Anexo B.

---

## 6. Fase 5 — Menores y forma (checklist rápido)

- [ ] M-01 Abstract = Resumen (métricas reales, sin "todos los umbrales superados").
- [ ] M-03 restituir tamaños por estrato corregidos (93/112, no 94/111).
- [ ] M-04 Tablas 4 y 5 como tablas formales con rótulo numerado.
- [ ] M-05 numerar o eliminar subsecciones 5.1.x en índice.
- [ ] M-07 fecha de consulta de límites de API de Reddit.
- [ ] M-08 suscriptores con fecha (E13).
- [ ] m-13 redondeos: 8.680/1.840 = **4,72** (no 4,71) y 42.150/8.240 = **5,12** (no 5,11).
- [ ] m-15 separador decimal consistente (Kappa 0,78, no 0.78).
- [ ] m-16 justificar r/derechogenial y discutir su efecto en el corpus.
- [ ] m-17 declaración de autoría precisa: identificar las herramientas generativas y sus usos (clave: la V3 admitió uso "sin la debida supervisión" sin especificar).
- [ ] m-19 política de enmascaramiento para atributos indirectos (ver 3.4).
- [ ] m-20 `ON DELETE CASCADE` → `RESTRICT` en FK posts→subreddits, usando `active_monitoring` para desactivar monitoreo.
- [ ] M-02/M-06/M-09/M-10/M-11 verificados en V3: revisar que las correcciones sobrevivan a la reescritura (M-09: confirmar numeración de Referencias/Anexos contra reglamento).
- [ ] Declaración de autoría visible en el índice (m-17/M-12).

---

## 7. Consultas SQL de evidencia (para correr sobre la base real)

```sql
-- 1) Tabla 3 reconstruida (recuentos CONTADOS con residual, no derivados)
SELECT COALESCE(nlp_category, 'No relevante') AS categoria,
       COUNT(*)                              AS n,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
FROM posts
GROUP BY nlp_category
ORDER BY n DESC;

-- 2) Latencia publicación → ingesta (N-01)
SELECT COUNT(*)                                                                          AS n,
       ROUND(AVG(EXTRACT(EPOCH FROM (ingested_at - to_timestamp(created_utc))) / 60.0), 2) AS media_min,
       ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP
             (ORDER BY EXTRACT(EPOCH FROM (ingested_at - to_timestamp(created_utc))) / 60.0), 2) AS p50_min,
       ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP
             (ORDER BY EXTRACT(EPOCH FROM (ingested_at - to_timestamp(created_utc))) / 60.0), 2) AS p95_min
FROM posts
WHERE created_utc IS NOT NULL AND created_utc > 0;

-- 3) Serie horaria por categoría (insumo para Figura 4 y para el motor de anomalías)
SELECT date_trunc('hour', ingested_at) AS hora, nlp_category, COUNT(*) AS n
FROM posts
GROUP BY hora, nlp_category
ORDER BY hora;

-- 4) Techo de ingesta vs. configuración (H-06): 4 ejecuciones/hora × 100 ítems = 400/h
-- 5) Disparos de anomalías: depende de la estructura real (ver N-06); si no existe tabla, crearla.
```

El script de **matriz de confusión 6×6** (Python) se genera cuando los autores entreguen E5.

---

## 8. Fase 6 — Figuras y formato final

1. **Figura 1** (arquitectura E2E): generada con matplotlib desde el contenido del Cap. 4 (IA).
2. **Figura 2** (DER): generada a partir del DDL real (E3).
3. **Figura 3** (captura n8n): aportada por autores (E2).
4. **Figura 4** (serie temporal mensual por categoría): generada con matplotlib desde la tabla de la base (IA; datos de la Tabla 1 + query 3).
5. Índice de tablas y figuras automático (Word).
6. Ensamblado final: script `python-docx` que arma el `.docx` con estilos de título, TOC automático, numeración APA 7 y anexos.

---

## 9. Fase 7 — Auto-auditoría final (tipo tribunal)

Antes de entregar, correr el mismo procedimiento que el tribunal:
1. **Re-calcular TODAS las cifras** verificables (tablas 1-5, F1, FP, latencias, ratios, redondeos) — script Python.
2. **Verificar correspondencia** cuerpo ↔ anexos ↔ índice ↔ figuras.
3. **Verificar trazabilidad OE ↔ resultados ↔ evidencia** (matriz de trazabilidad final).
4. Recorrer la **lista completa de hallazgos** (H-01…H-17, M-01…M-12, N-01…N-06, m-13…m-20) y marcar cada uno RESUELTO / PARCIAL / NO RESUELTO.
5. Chequear APA 7: cada referencia citada y cada cita referenciada; URL + fecha de recuperación en fuentes institucionales.

---

## 10. Orden de ejecución recomendado

1. **Fase 0 + 0.5**: entorno listo; los autores aprenden el sistema con la guía. *(Días 1–3)*
2. **Fase 1 (B1–B4)**: instalar entorno real + base + workflow + primera corrida. *(Días 3–7)*
3. En paralelo → **Fase 2** (reconstrucción completa del cuerpo sobre V2). *(Columna A, no bloquea)*
4. **B5**: dejar recolectando datos REALES (semana a mes según lo que decidan con los directores).
5. Con la base poblada → **B6 / Fase 3 bloqueantes** (E4, E6, E7, E3, E1, E2 → latencia, Tabla 3, anexos, motor, figuras).
6. **Fase 4 y 5**: mayores y forma.
7. **Fase 6**: figuras (2 y 4 con datos reales) y ensamblado.
8. **Fase 7**: auto-auditoría + ajustes.
9. Entrega V4 (docx + PDF) con los 8 bloqueantes cerrados y trazos de prioridad alta.

> ⚠️ **Ventana de datos:** la V2/V3 afirmaban un corpus de 6 meses que no existe. La V4 documentará una **ventana REAL de recolección** (ej.: 4–8 semanas). Esto obliga a ajustar: criterios de §1.6, tablas del Cap. 5, umbrales del motor de anomalías y cualquier cifra derivada. Es un ajuste justificado que el auditor acepta — siempre que se declare con honestidad y coherencia (nunca mezclar la ventana nueva con números viejos).

---

## 11. Límites (lo que la IA NO fabrica)

- **Cifras medidas sobre la base real** (latencia, recuentos, disparos, cobertura) — salen del sistema construido en Fase 1.
- Exports del workflow, capturas, URLs de repositorios, datos del sistema desplegado.
- La matriz de confusión y la validación con evaluador externo.
- Fuentes bibliográficas inventadas.

Si un ítem de evidencia no se puede producir, la salida honesta es **reclasificar el objetivo o retirar la métrica** — opción que el auditor explícitamente acepta en múltiples hallazgos (H-02, H-05, H-09, H-17, N-01, N-04).