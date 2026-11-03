# PAQUETE ANOTADORES V5

## Contenido
- guia_etiquetado_v5.md        (LEER PRIMERO)
- muestra_v5_etiquetado.xlsx   (352 casos) — PARA EL AUTOR 3 (etiquetar TODO)
- muestra_v5_anot1.xlsx        (50 casos)  — PARA EL COMPANERO 1
- muestra_v5_anot2.xlsx        (50 casos)  — PARA EL COMPANERO 2
- adjudicacion_v5.xlsx         (plantilla, se usa en el paso 4)

Los CSV equivalentes se incluyen para trazabilidad; usar los XLSX para etiquetar.

## Reparto
- AUTOR 3 (vos): etiqueta los 352 casos de muestra_v5_etiquetado.xlsx (incluye los 50 comunes).
- COMPANERO 1: etiqueta SOLO muestra_v5_anot1.xlsx (50 casos), a ciegas, sin comunicarse.
- COMPANERO 2: etiqueta SOLO muestra_v5_anot2.xlsx (50 casos), a ciegas, sin comunicarse.

## Reglas
1. LEER guia_etiquetado_v5.md ANTES de empezar.
2. NO consultar el clasificador ni la etiqueta automatica. La hoja no la trae.
3. Los 50 comunes los etiquetan los 3 SIN comunicarse entre si.
4. Solo una categoria por fila (lista desplegable en la columna amarilla).
5. Si hay duda razonable tras titulo+texto -> "No relevante".

## Flujo (5 pasos)
1. Cada uno llena su archivo.
2. Enviar los 3 archivos al agente.
3. El agente calcula el kappa de Fleiss y genera adjudicacion_v5.xlsx con los desacuerdos.
4. Los 3 discuten SOLO esos casos y completan etiqueta_final + motivo.
5. El agente calcula las metricas finales.

## Trazabilidad
Sorteo reproducible: semilla 20261020, ORDER BY md5(id || '20261020').
Orden de presentacion mezclado (no revela el estrato de origen).
La correspondencia codigo<->id no se publica.
