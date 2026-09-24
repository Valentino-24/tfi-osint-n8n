# GUÍA DE CONCEPTOS — TFI OSINT/n8n (en criollo)

> **Para leer con la Figura 1 al lado** (`V4\figuras\Figura_1_arquitectura.png`).
> Si entendés esta guía, entendés tu tesis. No la leas de memoria: **explicá cada sección con tus palabras** antes de avanzar.

---

## 1. Tu TFI en una frase

> **"Armamos un sistema que cada 15 minutos junta lo que se publica en subreddits argentinos, lo guarda en una base, lo clasifica por tipo de amenaza de ciberseguridad, detecta picos anormales y avisa."**

Eso es TODO el trabajo. La tesis documenta *cómo* está armado ese sistema, *cómo* se midió, y *qué* midió corriendo de verdad.

---

## 2. Los 4 conceptos base

| Concepto | Qué es | Analogía |
|---|---|---|
| **OSINT** | Recolectar y analizar información **pública** (lo que cualquiera puede ver) | Es como un periodista que lee todos los diarios del kiosco y saca conclusiones. No hackea nada: usa lo que ya está a la vista. |
| **Reddit API** | La "ventanilla oficial" que Reddit abre para que programas pidan datos | Como el menú de un restaurante: no podés pedir lo que no está en la carta, y si pedís demasiado rápido te hacen esperar (límites de uso). |
| **n8n** | Herramienta donde armás **workflows** visualmente: cajas conectadas por flechas, cada caja hace un paso | Como una línea de montaje de una fábrica: cada estación hace una tarea y pasa el producto a la siguiente. |
| **PostgreSQL** | La base de datos (guardado estructurado) | La bodega de un depósito: cada caja (tabla) tiene un rótulo (columnas) y un lugar fijo. |

---

## 3. El pipeline paso a paso (recorré la Figura 1)

La Figura 1 muestra 7 cajas adentro de n8n, en orden:

1. **Trigger (cron 15 min)** — el despertador. Cada 15 minutos arranca el flujo. Es lo que define la **frecuencia de recolección**. (De acá sale el tema de la latencia: si juntás cada 15 min, lo máximo que podés tardar en "enterarte" de un post es ~14 min + procesamiento. El auditor te agarró acá, N-01.)

2. **HTTP Request (Reddit JSON)** — sale a pedirle a Reddit los posts nuevos de los subreddits que te interesan (r/argentina, r/derechogenial, etc.). Usa credenciales de la API de Reddit (gratis).

3. **Code: normalizar + seudonimizar (HMAC-SHA-256)** — acá se procesa cada post:
   - **Normalizar**: limpiar (mayúsculas, espacios, formato de fechas).
   - **Seudonimizar**: el nombre de usuario se transforma con una **fórmula secreta (HMAC)** que produce un código irreversible. Así guardás el dato sin identificar a la persona — esto es lo que la Ley 25.326 exige (H-01).

4. **PostgreSQL: upsert posts** — guarda el post en la tabla `posts`. "Upsert" = si ya existe, lo actualiza; si no existe, lo inserta. Esto hace que el sistema sea **idempotente** (ejecutarlo 2 veces no duplica datos — m-18).

5. **Code: clasificador por diccionario** — asigna una **categoría** a cada post (por ejemplo: *Estafas, Phishing, Vulnerabilidades, Ransomware, No relevante*). ¿Cómo? Con un **diccionario de palabras clave** por categoría (el Anexo C): si el post contiene "estafa", "estampita", "caer", va a Estafas. Es un clasificador simple y auditable — el corazón de la tesis.

6. **Code: motor de anomalías** — compara cuántos posts de cada categoría entraron hoy contra el **historial** (días anteriores). Si de golpe hay un pico (ej.: 30 posts de estafas cuando el promedio es 5), **dispara una alerta**. La regla y el umbral tienen que estar justificados (N-04): acá se usa un umbral por **cuantil de Poisson** o similar, no el "promedio + 2 desvíos" que criticó el auditor.

7. **Alertas (Telegram / webhook)** — si el motor disparó, manda un aviso (por ejemplo un mensaje de Telegram a un canal privado). Es el **OE6**: el sistema "genera alertas tempranas". Si esto no llega a funcionar, el objetivo se reclasifica — el auditor lo acepta.

**Abajo a la derecha: PostgreSQL** — la base. No es solo "dónde se guarda": **es la fuente de toda la evidencia** (las consultas SQL que producen la Tabla 3, la latencia, las series).

---

## 4. La base de datos (por qué el DDL importa)

La base tiene (como mínimo) estas tablas:

| Tabla | Guarda |
|---|---|
| `posts` | Cada post: id, subreddit, título, texto, usuario seudonimizado, fecha, categoría (`nlp_category`), score, `ingested_at` (cuándo lo agarró el sistema) y `created_utc` (cuándo se publicó). |
| `comments` | Comentarios de los posts (si el sistema los junta). |
| `anomalias` | Los disparos del motor: fecha, categoría, n de la ventana, umbral superado. |
| `alertas` | Las alertas enviadas. |

**DDL** = el "plano" de la base: las sentencias `CREATE TABLE` que definen columnas y tipos. El auditor te marcó (N-06) que tu DDL anterior no tenía las columnas de score/entidades/anomalías/alertas — se corrige y el DDL del Anexo A **tiene que ser exactamente el que se ejecutó** (por eso es evidencia real E3).

**Por qué `ingested_at` y `created_utc` son oro:** la diferencia entre los dos es la **latencia** (cuánto tardó el sistema en enterarse de un post). Medirla real es el bloqueante N-01.

---

## 5. Las métricas que pide el auditor (que van a salir de lo real)

| Métrica | Qué mide | Cómo se entiende |
|---|---|---|
| **Latencia** | Tiempo entre que un post se publica y que el sistema lo ingesta | Si promedio es 4,2 min pero el trigger es cada 15 min → **imposible**: algo está mal. Ese era el hallazgo N-01. |
| **Throughput** | Cuántos ítems procesa por hora | Techo teórico = ejecuciones/hora × ítems por ejecución. Si declarás más que el techo → inconsistencia (H-06). |
| **Precisión** | De lo que el clasificador dijo "Estafa", ¿cuánto era estafa de verdad? | Alto = pocas alarmas falsas. |
| **Falsos positivos (FP)** | Posts clasificados como amenaza que NO eran amenaza | Es el "complemento" de la precisión (si precisión ≥ 82% ⇔ FP ≤ 18% — redundante, N-05: no pongas las dos como criterios distintos). |
| **F1** | Combinación de precisión y recall (0 a 1) | Un número solo para resumir qué tan equilibrado anda el clasificador. |
| **Cobertura (captura-recaptura)** | Qué porcentaje del total de posts peruanos... digo, **argentinos** relevantes capturaste | Se estima con la técnica de captura-recaptura (dos muestreos, ver cuántos se repiten). Si no podés hacer el protocolo → **retirar la métrica** (H-05). |
| **Kappa** | Acuerdo entre dos personas etiquetando lo mismo | 0,78 = acuerdo "sustancial" (casi perfecto). |

> Regla mental: **nunca un número sin saber de dónde salió.** El auditor (IA de los directores) recalcula todo. Los números de la tesis vienen de la base real, con las consultas SQL del plan.

---

## 6. Los Objetivos Específicos (OE) — ejercicio obligatorio

Abrí la base textual de la V2 (`tesis_v2.txt` en `V4\devoluciones\` cuando la normalice) y andá al capítulo de objetivos. Para CADA OE (OE1 a OE8) escribí **una frase con tus palabras** de qué significa. Ejemplo de cómo se hace:

> **OE6 — "Generar alertas tempranas..."** → Mi frase: *"El sistema me avisa en Telegram cuando una categoría de golpe tiene muchos posts"*.

Si no podés escribir esa frase, todavía no entendés el objetivo. **No avances hasta completar los 8.**

---

## 7. Glosario relámpago

- **Nodo**: una caja en n8n que hace UNA tarea.
- **Workflow**: el flujo completo de cajas conectadas.
- **Credencial**: los datos de acceso (usuario/clave/API key) que un nodo usa para hablar con un servicio.
- **Seudonimización**: reemplazar el identificador real (nombre de usuario) por un código irreversible. No es anonimización total (el dato sigue siendo personal — riesgo residual, H-01d).
- **HMAC-SHA-256**: fórmula de hash con **clave secreta**. Misma clave + mismo texto = mismo código; sin clave no se puede invertir.
- **Upsert**: "INSERT ... ON CONFLICT DO UPDATE" en PostgreSQL — insertar o actualizar sin duplicar.
- **Scheduler**: el cron (cada X minutos) que dispara el flujo.
- **Query / SQL**: pedidos a la base ("dame todos los posts de estafas de ayer").
- **Matriz de confusión**: tabla que cruza lo que el sistema dijo vs. lo que era realmente (es la evidencia E5, 6×6).
- **Ventana**: período de tiempo que se analiza (ej.: "últimos 7 días" para el motor de anomalías).

---

## 8. Qué hace cada uno (y el roadmap)

| Actor | Qué le toca |
|---|---|
| **Ustedes (autores)** | Aprender con esta guía, correr los pasos de instalación, dejar el sistema corriendo semanas, juntar las capturas/evidencias, etiquetar la muestra de control, y poder EXPLICAR el sistema en la defensa. |
| **La IA (este entorno)** | Les entrega: DDL correcto, workflow n8n importable, diccionario taxonómico, consultas SQL, guías paso a paso, y reconstruye todo el documento sobre la V2. |

**Roadmap inmediato (B1→B6):**
1. **B1** — Instalar n8n y crear la base de datos (guía: `GUIA_INSTALACION.md`).
2. **B2** — Ejecutar el DDL que te voy a pasar (`V4\anexos\A_DDL.sql`).
3. **B3** — Importar el workflow n8n (`V4\anexos\B_workflow.json`).
4. **B4** — Correrlo y verificar que la base se llena.
5. **B5** — Dejarlo corriendo y acumular datos reales.
6. **B6** — Sacar las evidencias (consultas del plan §7) → E1–E15.

---

*Si algo de esta guía no se entiende, decímelo y lo reexplico con otra analogía. No sigas hasta que te cierre.*