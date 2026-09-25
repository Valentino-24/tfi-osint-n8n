# TFI OSINT/n8n — Base de Conocimiento

Base de conocimiento generada para el TFI OSINT/n8n. Describe el sistema real implementado, el alcance de la tesis y el trabajo pendiente de B5/B6.

## Índice de archivos

| Archivo | Contenido |
|---|---|
| [01_vision_y_objetivos.md](01_vision_y_objetivos.md) | Propósito, actores, alcance, límites y métricas de éxito |
| [02_descripcion_general.md](02_descripcion_general.md) | Stack, arquitectura, integraciones y estado de implementación |
| [03_actores_y_roles.md](03_actores_y_roles.md) | Actores, responsabilidades y permisos operativos |
| [04_modelo_de_datos.md](04_modelo_de_datos.md) | Tablas, relaciones, constraints, índices y seed data |
| [05_reglas_de_negocio.md](05_reglas_de_negocio.md) | Reglas RN de fuentes, persistencia, seudonimización, clasificación y anomalías |
| [06_funcionalidades.md](06_funcionalidades.md) | Historias de usuario y estado de cada épica |
| [07_flujos_principales.md](07_flujos_principales.md) | Flujos extremo a extremo y manejo de errores |
| [08_arquitectura_propuesta.md](08_arquitectura_propuesta.md) | Patrones, estructura de directorios, seguridad y variables de entorno |
| [09_decisiones_y_supuestos.md](09_decisiones_y_supuestos.md) | Decisiones de diseño, alternativas, trade-offs y supuestos |
| [10_preguntas_abiertas.md](10_preguntas_abiertas.md) | Inconsistencias y preguntas pendientes priorizadas |

## Quick Start para autores

1. Entender el propósito y el alcance → [01](01_vision_y_objetivos.md), [02](02_descripcion_general.md).
2. Revisar quién opera y qué puede tocar → [03](03_actores_y_roles.md).
3. Entender cómo están modelados los datos → [04](04_modelo_de_datos.md).
4. Revisar las reglas antes de modificar el pipeline → [05](05_reglas_de_negocio.md).
5. Entender funcionalidades y flujos → [06](06_funcionalidades.md), [07](07_flujos_principales.md).
6. Antes de implementar, consultar decisiones y preguntas abiertas → [08](08_arquitectura_propuesta.md), [09](09_decisiones_y_supuestos.md), [10](10_preguntas_abiertas.md).

## Resumen ejecutivo

El TFI OSINT/n8n es un pipeline de recolección y análisis de publicaciones públicas de Reddit. Actualmente usa RSS porque la API pública está restringida para la IP del proyecto; cada post se persiste idempotentemente con clasificación, score, entidades y autor seudonimizado. La base actual contiene una corrida verificada de B4; B5 debe cerrar la ventana real de datos y B6 debe producir las evidencias E1–E15.

## Fuente principal

La KB se contrastó con `PLAN_V4.md`, `V4/GUIA_EJECUCION.md`, `V4/GUIA_CONCEPTOS.md`, `V4/GUIA_INSTALACION.md`, `V4/anexos/A_DDL.sql`, `V4/anexos/B_workflow.json` y `V4/scripts/generar_workflow.py`. Las cifras y afirmaciones de estado deben volver a verificarse contra la base y la corrida más reciente antes de publicarse.
