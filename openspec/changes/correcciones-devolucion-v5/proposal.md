# Proposal

## Why

La devolucion V5 del tribunal (7,8/10, APROBADO CON CORRECCIONES OBLIGATORIAS. VERSION FINAL V6) identifica 5 items bloqueantes para habilitar la defensa y un conjunto de mayores/altos. La version actual en docs/informe/tesis_v5.md/.pdf necesita correcciones para satisfacer los requisitos antes de pasar a V6.

## What Changes

- Trazabilidad entre versiones (N-07): Formalizar declaracion con firmas manuscritas/digitales (autores + direccion), corregir ciclo de vida del corpus (poblacion al 30/09, eliminaciones del 01/10), precisar alcance a V3, corregir remisiones y definir codigos IN-07/C-25.
- Referencia de validacion (N-16): Declarar composicion real (50 consenso + 302 un anotador), identificar anotador, medir coincidencia con consenso y rango de metricas, unificar uso de herramientas generativas.
- Desempeno por idioma (N-15): Estimar sensibilidad por comunidad/idioma con pesos propios e intervalos, corregir lectura del lexico local en secciones afectadas.
- Regimen de operacion + consistencia (N-17, N-19): Tabla de regimen por dia, recalcular fraccion de operacion, explicar evaluaciones del 16/10 y 17/10, trasladar a conclusiones/discusion, corregir las 16 contradicciones.
- Evidencia reproducible (H-07): Entregar copia congelada evidencia_v5.zip o acceso de lectura al repo, verificar SHA-256, cotejar Anexo B.
- Codigo/esquema/transcripcion (N-18): Identificar version transcripta vs ejecutada, conciliar comentarios B.2, tabla de transicion caso por caso, esquema desde produccion o migracion fechada, transcribir Parse Reddit Posts.
- Privacidad/exposicion (N-10, H-01): Retirar titulos literales de 5.4, decidir/tratar menciones, mantener correspondencia fuera de repo publico, corregir 3.4.
- Diccionario/extractor/motor: Completar auditoria de solapamientos, corregir extractor (afi p, subdominios, doble conteo), recalculo con ventana movil de dias operados, zona horaria.
- Formales/menores: Indice multinivel, denominacion del trabajo, figuras/epigrafes/numeracion/hoja de firmas, suscriptores, etc.

## Capabilities

### New Capabilities
- trazabilidad-versiones-v6: Declaracion formal de trazabilidad entre V2/V3/docs/V5 con firmas, ciclo de vida de datos, alcance y remisiones corregidas.
- validacion-clasificador-v6: Validacion con referencia mixta (consenso + un anotador), herramientas declaradas, sensibilidad por comunidad/idioma con intervalos ponderados.
- evidencia-reproducible-v6: Acceso verificable a evidencia, codigo/SQL transcritos con version, esquema desde produccion.
- privacidad-casos-v6: Eliminacion de IDs/titulos literales, tratamiento de menciones, riesgo residual ampliado.
- consistencia-operativa-v6: Regimen de operacion por dia, fraccion corregida, transferido a conclusiones, correccion de contradicciones.

### Modified Capabilities
- (ninguna)

## Impact
- Archivos: docs/informe/tesis_v5.md, docs/informe/tesis_v5.pdf, docs/informe/Anexos/*, docs/evidencias/*, docs/documentos/devoluciones/*
- Requiere generar PDF con docs/scripts/convertir_pdf.py tras cambios
- Requiere commit/push con verificacion
