# Proposal

## Why

La quinta versión del TFI (V5) fue aprobada con correcciones obligatorias por el tribunal. Tras comparar la devolución V5 con el entregable `docs/devoluciones/tesis_v5.pdf`, se identificaron múltiples hallazgos mayores (N-15 a N-19), menores (m-28, m-30, m-31-m-38) y observaciones al Anexo E (firmas, ciclo de vida, alcance V3, origen de latencia/throughput, errores puntuales), así como el bloqueante de entrega relacionado con la copia congelada/repositorio con hash verificable. Es necesario avanzar a la **Versión 6 (tesis_v6.md / tesis_v6.pdf)** atendiendo todas las correcciones que pueden resolverse con el material existente, sin recolectar ni etiquetar de nuevo, dejando explícitas las decisiones que requieren acción institucional (firmas/copia repositorio) sin inventarlas.

## What Changes

- **Generar nueva versión del informe**: Crear `docs/informe/tesis_v6.md` como base para `tesis_v6.pdf`, partiendo de `docs/devoluciones/tesis_v5.md` con correcciones sistemáticas.
- **Corregir interpretación por idioma (N-15)**: Agregar sensibilidad estimada por comunidad/idioma con pesos e intervalos exactos, renombrar columna "Omisión" a "proporción de amenazas en la muestra del estrato negativo", reescribir 5.5, 6.1, 6.2, 6.4 y respuesta a PI-2.
- **Corregir composición de referencia y etiquetado (N-16)**: Declarar explícitamente 50 casos con consenso de tres anotadores + 302 con etiqueta de un solo anotador, identificar al anotador, informar coincidencia sobre 50 casos (binaria/categoría), mostrar rango por anotador, unificar descripción de uso de herramientas generativas en etiquetado.
- **Corregir régimen de operación (N-17)**: Agregar tabla de régimen por día (inicio/fin/corridas auto/manual), recalcular fracción de operación con mismo intervalo, explicar evaluaciones 16/10-17/10, usar "instancia de n8n" donde corresponda, reescribir 2.2, 5.1, 5.3, 6.2, 7.2, 7.3, 7.4, unificar estado OE1.
- **Corregir código/esquema transcriptos (N-18)**: Identificar versión transcripta vs operada (fecha/commit o diferencia), conciliar comentarios contradictorios, reemplazar/clarificar Anexo A con esquema real o migración con fecha, cuantificar errores extractor (afi p, subdominios, dominios correo), auditar solapamientos >=6 pares, transcribir Parse Reddit Posts.
- **Corregir inconsistencias internas (N-19)**: Atender los 16 ítems listados (Figura 4/texto, días operación, FP r/DerechoGenial, notificación, OE1, detecciones locales, modismos, índices, columnas SET, casos Tabla 5.14, categorías peor resueltas, registro ejecuciones, publicaciones previas rotación, cronología umbrales, Anexo E, numeración/rótulos).
- **Corregir Anexo E (N-07)**: Corregir (b) "quién toma conocimiento", (c) ciclo de vida (recolección 25-30/09, base 30/09, TRUNCATE), (d) alcance V3, (e) latencia/throughput como mediciones sin serlo, (f) errores puntuales. Dejar explícito que firmas y entrega de copia/repositorio con hash requieren acción institucional (sin inventar).
- **Correcciones formales**: Índice multinivel (m-28), denominación trabajo (m-30), corregir figuras menores (m-34), ubicar hoja de firmas (m-35), tabla 5.1 suscriptores (m-36), HMAC undefined (m-37), patrón CVE (m-38), desempate/m-31-m-33 según corresponda.
- **Generar PDF V6**: Ejecutar pipeline de conversión `docs/scripts/convertir_pdf.py` para generar `docs/devoluciones/tesis_v6.pdf` (o destino acorde al proceso), validando con `verificar_pdf.py`.

## Capabilities

### New Capabilities
- `tesis-v6-correcciones-tribunal`: Sistema de correcciones trazables desde devolución V5 hasta versión V6 del informe, con mapeo ítem por ítem, validación numérica y generación de PDF.
- `validacion-metodologica-v6`: Correcciones metodológicas (muestreo/etiquetado, interpretación por idioma, régimen de operación, trazabilidad de versiones).

### Modified Capabilities
- `<none>`: No se modifican capacidades existentes bajo `openspec/specs/` (cambio documental/organizativo del informe).

## Impact

**Archivos afectados:**
- `docs/informe/tesis_v6.md` (nuevo)
- `docs/devoluciones/tesis_v6.pdf` (nuevo, generado por pipeline)
- `docs/devoluciones/tesis_v5.md` (referencia, no modificar)
- `openspec/changes/correcciones-tribunal-v5-v6/*` (artifacts)
- Posibles ajustes a anexos mencionados en texto (A-E) solo si necesario para consistencia

**Sistemas/herramientas:**
- Pipeline de conversión PDF existente (`docs/scripts/convertir_pdf.py`, `docs/scripts/verificar_pdf.py`)
- Git (commits atómicos)

**Restricciones:**
- Solo lectura para análisis V5 vs V5 actual; no recolectar/etiquetar nuevo
- No hardcodear credenciales
- No publicar/activar workflow en n8n
- No inventar firmas/copia repositorio - documentar como pendientes institucionales
- Seguir reglas duras del proyecto
