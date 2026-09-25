# Preguntas Abiertas

## Inconsistencias detectadas

### IN-01 — La guía declara 15 nodos y la verificación final 14
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
