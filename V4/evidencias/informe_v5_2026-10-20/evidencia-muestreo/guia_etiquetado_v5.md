# Guía de etiquetado — Validación V5

**Objeto**: clasificar cada post del corpus B5 como una de las 10 categorías (9 tipos de amenaza + "No relevante").

## 1. Principio fundamental (ciego)

Cada anotador clasifica **sin ver** la etiqueta del clasificador. La hoja **no incluye** `nlp_category`, `nlp_score`, el identificador de Reddit **ni el estrato de origen**. Esta guía es la única referencia.

## 2. Categorías válidas

| Categoría | Alcance |
|---|---|
| **No relevante** | No es un hecho o discusión sobre ciberseguridad. General, educativo, laboral, personal o irrelevante para amenazas. |
| **Phishing** | Intentos de engaño para obtener credenciales o información sensible (smishing, vishing, BEC, sitios/login falsos). |
| **Robo de Credenciales** | Compromiso efectivo o explotación para acceder a cuentas (credential stuffing, account takeover, session hijacking, MFA bypass, SIM swap). |
| **Malware** | Software malicioso: troyanos, droppers/loaders, keyloggers, infostealers, criptominería, etc. |
| **Ransomware** | Extorsión cifrando datos (ransom, nota de rescate, cifrado, leaksite asociado a ransomware). |
| **Vulnerabilidades** | Divulgaciones CVE, PoC, exploits, advisories, afectación de productos/versiones. |
| **Filtración de Datos** | Exposición o filtrado de datos (leaks, dumps, breaches, datos personales expuestos). |
| **Infraestructura y Ataques** | Ataques a infraestructura/red (DDoS, botnets, C2, tráfico malicioso, ataques a servicios). |
| **Hacktivismo** | Activismo digital con fines políticos/sociales (defacement, leaks con motivación hacktivista). |
| **Ingeniería Social** | Manipulación psicológica para engañar (sin caer forzosamente en phishing clásico). |

> En Excel, la columna `categoria_asignada` tiene **lista desplegable** con estas 10 opciones. Usarla evita errores de tipeo.

## 3. Regla de oro (posts link-only)

Muchos posts tienen `texto = "[link] [comments]"` o vacío. **Etiquetar por el título + contexto.** Si el título no permite decidir con seguridad → **No relevante**.

## 4. Reglas de desempate

1. **Un post puede tocar 2 categorías → elegir la dominante.**
2. **Ambiguo / insustancial → No relevante.**
3. **Consulta/curiosidad educativa → No relevante.**
4. **Incidente vs noticia/advisory**: una divulgación de CVE → **Vulnerabilidades**. Un ataque ejecutado → evaluar según el efecto.
5. **Filtración vs robo de credenciales**: datos personales/volúmenes filtrados → **Filtración de Datos**. Acceso a cuentas → **Robo de Credenciales**.
6. **Discusión administrativa/argentina local genérica → No relevante.** Clave para r/devsarg: muchas consultas y opiniones no describen una amenaza.
7. **Términos genéricos**: "filtrado", "clonar repo", "memory leak", "payload" fuera de contexto → tender a **No relevante**.

## 5. Columnas de la hoja

- `codigo_interno` — código ciego (C-001…). **No modificar.**
- `titulo` — título del post.
- `texto` — cuerpo del post (hasta 3000 caracteres).
- `comunidad` — r/devsarg / r/netsec / r/Malware (contexto legítimo).
- `categoria_asignada` — **llenar OBLIGATORIAMENTE** con una de las 10 categorías (lista desplegable).
- `comentario` — opcional, para dudas o casos límite.

**Restricciones**: no ver la etiqueta automática; no comunicarse con los otros anotadores mientras se etiqueta la submuestra común; una sola categoría por fila; nombres exactos de la guía.

## 6. Qué archivo usa cada uno

| Quién | Archivo | Qué contiene |
|---|---|---|
| **Autor 3 (vos)** | `muestra_v5_etiquetado.xlsx` | **Los 352 casos** (170 del censo + 182 de la muestra). Etiquetás TODO. |
| **Compañero 1** | `muestra_v5_anot1.xlsx` | Solo los **50 comunes**. |
| **Compañero 2** | `muestra_v5_anot2.xlsx` | Solo los **50 comunes**. |

Los 50 comunes están contenidos en la hoja completa del Autor 3. **No hay que llenar una planilla aparte**: las etiquetas del Autor 3 sobre esos 50 se extraen por `codigo_interno`.

## 7. Flujo completo (5 pasos)

1. **Etiquetado.** Cada uno llena su archivo, a ciegas y sin comunicarse.
2. **Entrega.** Los 3 archivos se envían al agente.
3. **Kappa.** El agente calcula el **kappa de Fleiss** sobre los 50 comunes y genera `adjudicacion_v5.xlsx` con **solo los casos donde los 3 no coinciden**.
4. **Consenso.** Los 3 autores discuten **solo esos desacuerdos** y completan en `adjudicacion_v5.xlsx` las columnas `etiqueta_final` y `motivo`.
5. **Métricas.** El agente aplica la etiqueta final y calcula precisión, sensibilidad, F1, IC, resultados por comunidad y matriz por categoría.

> **El consenso se anota en `adjudicacion_v5.xlsx`**, hoja "Adjudicacion". La decisión es humana: **nunca** la toma una IA. Si no hay acuerdo, se adopta la opción más conservadora (**No relevante**).

## 8. Criterio de calidad

Si hay duda razonable tras leer título + texto → **No relevante**. Mejor ser conservador que forzar una amenaza.

## 9. Trazabilidad

Sorteo reproducible con semilla `20261020` (`ORDER BY md5(id || '20261020')`), orden de presentación mezclado de forma determinista. La correspondencia `codigo_interno ↔ id` no se publica (protege la identidad y resuelve N-10).
