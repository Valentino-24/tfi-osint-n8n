# Preguntas Abiertas

## Inconsistencias detectadas

### ~~IN-01 — La guía declara 15 nodos y la verificación final 14~~ — RESUELTA 2026-09-30

**Estado**: resuelta. El workflow tiene **16 nodos** (`B_workflow.json`, 16 nodos;
`generar_workflow.py` declara 16). Las dos ramas, ingesta y anomalías, fueron
ejecutadas en runtime y verificadas. La guía decía 15 y la verificación previa 14;
ambas cifras quedaron desactualizadas al crecer el workflow. La guía ya dice 16.
**Documento A dice**: `GUIA_EJECUCION.md` describe el workflow como 15 nodos.
**Documento B dice**: la sesión de verificación reportó 14 nodos.
**Impacto**: afecta la Figura 3, el Anexo B y la trazabilidad del artefacto.
**Resolución propuesta**: regenerar el export desde `generar_workflow.py`, contar los nodos en la versión final y actualizar la guía y la figura con ese número.

### IN-02 — El estado de B4 en la guía quedó desactualizado
**Documento A dice**: la tabla de estado inicial muestra B4 como pendiente.
**Documento B dice**: la corrida real verificó 201 posts y un post de phishing.
**Impacto**: un lector puede pensar que la ingesta nunca fue ejecutada.
**Resolución propuesta**: actualizar la tabla de estado con la fecha, la corrida y la limitación de `r/derechogenial`.

### IN-03 — Semántica de `ingested_at` en el upsert
**Documento A dice**: `ingested_at` no debe tocarse para preservar la latencia.
**Documento B dice**: el DDL solo define el default y no expresa la regla del `ON CONFLICT`.
**Impacto**: puede cambiar la latencia calculada si un post se reprocesa.
**Resolución propuesta**: fijar la sentencia final de upsert y verificarla con una segunda corrida controlada.

### IN-04 — Paleta de evidencia de la alerta externa
**Documento A dice**: el sistema tiene nodo Telegram.
**Documento B dice**: Telegram está deshabilitado y no hay captura real.
**Impacto**: no se puede afirmar que OE6 esté cumplido con una alerta enviada.
**Resolución propuesta**: mantener Telegram como opcional y reclasificar OE6 si no se obtiene evidencia real.

### IN-05 — Idioma y correcciones de redacción en la KB
**Documento A dice**: la KB se genera en español técnico.
**Documento B dice**: algunos borradores iniciales pueden contener términos en inglés o errores de tipeo.
**Impacto**: reduce calidad editorial y puede filtrar términos no deseados a la tesis.
**Resolución propuesta**: revisar la KB antes de usarla como fuente del documento final.

### IN-06 — El extractor de entidades matchea por subcadena, sin límites de palabra
**Detectado**: 2026-10-01, durante la jornada 1 de la ventana B5, al revisar el campo `entities`
de los posts ingeridos.
**Documento A dice**: `Extract Entities` extrae CVE, emails, IPs, dominios y productos, y es la
fuente del campo `entities` que la tesis usa como evidencia de OE4.
**Documento B dice**: el nodo busca el término con `includes()` sobre el texto normalizado, sin
exigir límites de palabra. Un término que aparece **dentro** de otra palabra se cuenta como
mención.
**Caso verificado**: el post *"WordPress malware in official WooCommerce theme (**Kiosko**):
hidden admin users and corrupt..."* quedó con `entities->'products' = ["ios"]`, extraído de
"K**ios**ko". El término del diccionario es `ios` (iOS de Apple) y no aparece en el texto.
**Impacto acotado**: la **clasificación no se ve afectada** — ese post fue clasificado
`Malware` por otros términos del diccionario. Lo que se degrada es la **calidad del campo
`entities`**, que queda con falsos positivos y por lo tanto no es confiable como evidencia
cuantitativa de menciones sin un ajuste posterior.
**Por qué no se corrige ahora**: la ventana B5 está en curso. Cambiar el extractor a mitad de
ventana haría incomparables los `entities` de los días anteriores y posteriores. El cambio de
comportamiento debe ocurrir **fuera de la ventana** y declararse como cambio de versión.
**Resolución propuesta**: agregar límites de palabra al extractor (regex con `\b`, o
comparación por token) en `V4/scripts/generar_workflow.py`, regenerar el artefacto, y tratar el
campo `entities` ya recolectado como afectado por la limitación conocida. Requiere change
propio en el roadmap y decisión de los autores sobre si se recalcula `entities` sobre el
corpus ya ingerido o se declara la limitación tal cual.

### IN-07 — El denominador por subreddit de la ventana no coincide con el alcance real
**Detectado**: 2026-10-02, al regenerar la bitácora del 2026-10-01 con `V4/scripts/bitacora_b5.py`.
**Documento A dice**: `V4/evidencias/VENTANA_B5.md` §6 fija el denominador de **todo** desglose por
subreddit de la ventana en tres comunidades: `r/argentina`, `r/devsarg`, `r/derechogenial`. Es el
alcance del Plan B.
**Documento B dice**: el workflow en ejecución (`Prepare Subreddits`, fuente de verdad
`V4/scripts/generar_workflow.py`) monitorea **otro** conjunto: `r/netsec`, `r/Malware`, `r/devsarg`
(Plan C). Los posts ingeridos lo confirman: `SELECT subreddit_id, COUNT(*) FROM posts GROUP BY 1`
devuelve solo esas tres claves.
**Estado verificado de `subreddits`** (6 filas, con duplicados):

| `id` | `display_name` | `active_monitoring` | posts |
|---|---|---|---|
| `argentina` | `r/argentina` | false | 0 |
| `derechogenial` | `r/derechogenial` | **true** | 0 |
| `DerechoGenial` | `r/DerechoGenial` | false | 0 |
| `devsarg` | `r/devsarg` | true | 120 |
| `Malware` | `r/Malware` | true | 101 |
| `netsec` | `r/netsec` | true | 104 |

**Tres problemas encadenados**:
1. **§6 de `VENTANA_B5.md` está desactualizada**: nombra un conjunto de tres comunidades que el
   sistema ya no monitorea. Como §6 gobierna todo porcentaje por subreddit de la ventana,
   cualquier cifra calculada con ese denominador sería incorrecta.
2. **`r/derechogenial` figura con `active_monitoring = true` pero el workflow nunca la ingiere.**
   Es un resto del Plan B: la base declara activa una comunidad que el pipeline no consulta, y por
   eso el script de bitácora advierte `4 de 3 esperados`.
3. **Duplicados en `subreddits`**: `derechogenial`/`r/derechogenial` y `DerechoGenial`/`r/DerechoGenial`
   son la misma comunidad con distinta capitalización, en dos filas. Ninguna tiene posts.
**Por qué no se corrige unilateralmente**: definir cuál es el conjunto de comunidades del alcance y
qué hacer con las filas del Plan B es una decisión de los **autores con sus directores**, no una
corrección técnica. La regla dura del proyecto impide **eliminar** un subreddit; la vía prevista es
desactivarlo con `active_monitoring`, y en este caso además habría que decidir si las filas
duplicadas se consolidan o se conservan.
**Resolución propuesta**: (a) actualizar §6 de `VENTANA_B5.md` con el conjunto del Plan C una vez
confirmado por los autores; (b) poner `active_monitoring = false` en `r/derechogenial` para que la
base no declare activa una comunidad que el pipeline no consulta; (c) decidir el destino de
`r/argentina` y de las dos filas de derechogenial, conservando la evidencia histórica de B4.

## Preguntas abiertas priorizadas

| Prioridad | Pregunta | Bloquea | Decisor |
|---|---|---|---|
| Alta | ¿Cuál es la fecha de inicio de la ventana real y cuándo se cierra? | B5, métricas del Cap. 5 | Autores con sus directores |
| Alta | ¿Se puede conseguir una submuestra de 100 posts para el evaluador externo? | E14, Kappa y matriz de confusión | Autores / facultad |
| Alta | ¿Se habilita Telegram para obtener E12 o se retira/reclasifica OE6? | E12, alcance de alertas | Autores |
| Media | ¿Se conserva la ventana actual o se reinicia la recolección con métricas corregidas? | Comparabilidad de resultados | Autores con tribunal |
| Media | ¿Se obtiene una developer account de Reddit para recuperar score/comentarios? | Alcance de la fuente y OE2 | Autores |
| Media | ¿La tabla `comments` queda como parte del modelo no implementada? | Descripción del artefacto y alcance | Autores |
| Media | ¿Cuál es la fórmula exacta y documentada del score? | Sección 4.4 y evaluación | Autores / técnica |
| Media | ¿Se corrigen los límites de palabra del extractor de entidades fuera de la ventana B5, y se recalcula `entities` sobre el corpus ya ingerido? (IN-06) | Calidad del campo `entities`, evidencia de OE4 | Autores / técnica |
| **Alta** | ¿Cuál es el conjunto de comunidades del alcance: Plan B (`r/argentina`, `r/devsarg`, `r/derechogenial`) o Plan C (`r/netsec`, `r/Malware`, `r/devsarg`)? (IN-07) | **Todo porcentaje por subreddit** de la ventana, §6 de VENTANA_B5.md | **Autores con sus directores** |
| Baja | ¿Se puede obtener E15 (copia del antecedente de Rivas y Dengra)? | Marco teórico H-10 | Autores / biblioteca |
| Baja | ¿Se versionan las evidencias binarias grandes o solo exports reproducibles? | Tamaño y higiene del repositorio | Autor operador |

## Estado de seguimiento de las preguntas priorizadas

Actualizado el **2026-09-25** por el change `ventana-recoleccion-b5` (C-05). Ninguna pregunta de
la tabla cambia de identidad ni se cierra: se registra su estado de avance.

| Pregunta | Estado | Constancia |
|---|---|---|
| ¿Cuál es la fecha de inicio de la ventana real y cuándo se cierra? (prioridad **Alta**) | **Parcialmente resuelta — sigue abierta.** Inicio **fijado el 2026-09-25** (inmutable); **fecha de corte `no fijada`**, pendiente de la decisión de los autores con sus directores (tarea **6.1** del change C-05) | `V4/evidencias/VENTANA_B5.md` §1 y §3 |
| ¿Se conserva la ventana actual o se reinicia la recolección con métricas corregidas? (prioridad **Media**) | **Abierta.** Sin decisión de los autores (tarea 6.2). Su acumulación es de 0/10 días completos evaluados al 2026-09-25, así que tampoco hay base para decidir | `V4/evidencias/VERIFICACION_INSTANCIA_2026-09-25.md` §7 |

**Limitación conocida de la evidencia de falla:** el log de ejecuciones de la instancia n8n no
está disponible ni preservado, por lo que el éxito de la ingesta **día por día no puede probarse
desde el log**; la bitácora lo declara como `sin observación` y su transcripción es manual
cuando el log exista (tarea 3.5 del change C-05, decisión D-3). Ver
`V4/evidencias/VERIFICACION_INSTANCIA_2026-09-25.md` §6.

## Decisiones pendientes para el próximo change

1. Definir la ventana de B5 y sus parámetros de corte.
2. Congelar el export del workflow y corregir la diferencia de conteo de nodos.
3. Ejecutar las consultas E4 y E6 sobre la base real.
4. Decidir si se completa o se retira la submuestra externa.
