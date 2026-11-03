# Design

## Context

El pipeline `docs/scripts/convertir_pdf.py` genera el PDF de la tesis a partir del Markdown. Incluye un paso de numeración de índices (`numerar_indices`, L730-795) que asigna número de página a cada entrada del índice general, de tablas y de figuras. El algoritmo asume que cada entrada del índice general tiene un número secuencial (1-N) que corresponde a un capítulo (1-10). Con un índice multinivel (61 entradas), esa correspondencia se rompe.

**Funciones relevantes:**
- `mapa_cuerpo(doc, desde)` (L657-694): construye `etiquetas` (rótulos Tabla/Figura → página) y `capitulos` (int→página, solo 1-10).
- `recolectar_entradas(doc)` (L709-727): extrae entradas del índice. Para rótulos, clave = string ("Tabla 5.1.1."); para el resto, clave = int (primer número).
- `numerar_indices(doc)` (L730-795): para cada entrada, busca `capitulos.get(clave)` o `etiquetas.get(clave)`. Si no encuentra → SIN PAGINA → aborta.

**Ver también:** `docs/scripts/verificar_pdf.py` compuertas `indices_numerados` y `rotulos`.

## Goals / Non-Goals

**Goals:**
- Soportar índices multinivel (61+ entradas) sin abortar el build
- Asignar número de página correcto a cada entrada del índice general
- Mantener la verificación automática (compuertas) funcional
- No modificar el Markdown del informe ni su estructura

**Non-Goals:**
- No cambiar el formato visual del índice en el PDF
- No modificar el contenido del informe
- No reescribir todo `convertir_pdf.py` (solo `mapa_cuerpo` y `numerar_indices`)

## Decisions

### Decisión 1: Matching por texto normalizado en lugar de por número

**Problema:** El número secuencial del índice (39) no corresponde al número jerárquico del encabezado (1.1). No hay forma de mapear 39→1.1 por número.

**Solución:** En `mapa_cuerpo`, construir un diccionario `texto_a_pagina` que mapee el texto normalizado del encabezado (H1, H2, H3) a su página. En `numerar_indices`, para entradas que no se resuelvan por número de capítulo, normalizar el texto de la entrada (quitar "39. 1.1. ") y buscar en `texto_a_pagina`.

**Normalización:** lowercase, sin acentos (NFD), strip de patrones numéricos iniciales (`^\d+\.\s*` y `^\d+\.\d+\.\s*`), trim.

**Alternativa considerada:** Fuzzy matching (Levenshtein). Descartado porque puede asignar páginas equivocadas a encabezados similares. El matching exacto por texto normalizado es más seguro.

### Decisión 2: Manejo de colisiones

Si dos entradas del índice normalizan al mismo texto (ej: "Régimen de operación por día" aparece una vez), usar la primera coincidencia. Si no hay coincidencia exacta, intentar matching por subcadena (el texto del índice contiene el texto del encabezado o viceversa).

### Decisión 3: Registrar H2 y H3 en mapa_cuerpo

Actualmente solo se registran H1 (capítulos). Agregar registro de H2 y H3 para que sus textos estén disponibles en `texto_a_pagina`. No se necesita su número de capítulo, solo su texto y página.

### Decisión 4: Ajustar compuertas del verificador

- `INDICES`: `{"Índice general": 61, "Índice de tablas": 29, "Índice de figuras": 4}`
- `rotulos`: tablas == 29, tablas_docx == 33 (ya actualizado)
- El umbral de similitud contra el PDF aprobado se mantiene en 0.97 (el contenido cambió pero la estructura es la misma)

## Risks / Trade-offs

- [Risk] Matching por texto puede asignar páginas equivocadas si hay encabezados con texto idéntico → Mitigation: usar matching exacto por texto normalizado; si hay colisión, tomar la primera; si no hay coincidencia, mantener SIN PAGINA como warning (no abortar).
- [Risk] El índice tiene 61 entradas pero solo ~10 son capítulos; las 51 restantes son secciones → Mitigation: registrar H2/H3 en `texto_a_pagina` para cubrir todas las entradas.
- [Trade-off] El build será más lento (más lookups por texto) pero el impacto es mínimo (61 entradas × ~86 encabezados = ~5200 comparaciones).

## Migration Plan

1. Modificar `mapa_cuerpo` para agregar `texto_a_pagina` dict (normalizado H1/H2/H3 → página)
2. Modificar `numerar_indices` para intentar text matching cuando `capitulos.get(clave)` falla
3. Revertir el cambio de `raise SystemExit` a warning (ya hecho) para no abortar
4. Actualizar `INDICES` en `verificar_pdf.py` a 61
5. Build + verificar
6. Si todo pasa, restaurar el `raise SystemExit` (o dejar como warning)

## Open Questions

- ¿El índice debe tener 61 entradas o se puede reducir a ~21 (como V5 + 5.1.1)? El tribunal pide multinivel, pero 61 puede ser excesivo. Decisión: mantener 61 (ya está en el MD y el tribunal lo pide).
- ¿El matching por texto debe ser exacto o fuzzy? Decisión: exacto por texto normalizado, con fallback a subcadena si no hay coincidencia exacta.
