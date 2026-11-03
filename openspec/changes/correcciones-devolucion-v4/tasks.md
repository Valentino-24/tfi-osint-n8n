# Tasks

## 1. Bloqueantes (N-07, N-08)
- [x] 1.1 Revisar y completar Anexo E (Declaración de trazabilidad) con ciclo de vida completo (B4, 25-30/09, TRUNCATE 01/10, B5, corte). Verificar referencias. (Ver `docs/evidencias/informe_v5_2026-10-20/Declaracion_trazabilidad_versiones.md`)
- [x] 1.2 Verificar validación N-08 sobre B5: reproducibilidad, consenso/adjudicación, acuerdo entre anotadores, ponderación por estrato, intervalos, desglose por `r/devsarg`, conciliación tabla de transición. Documentar hallazgos en el informe. (Ver `docs/evidencias/informe_v5_2026-10-20/`)

## 2. Mayores (N-09 a N-14)
- [x] 2.1 N-09: Corregir explicación de latencia (cadencia vs operación, descomposición por estado motor). Revisar 5.3, 6.3, 7.3, 8.2.
- [x] 2.2 N-10: Eliminar IDs/títulos literales restantes, usar códigos C-XX y descripciones genéricas. Revisar riesgo residual.
- [x] 2.3 N-11: Mantener recálculo retrospectivo por `created_utc` y declaración "eficacia no demostrada" para OE5.
- [x] 2.4 N-12: Atender diccionario (erratas, genéricos, solapamientos, guiones). Revisar Anexo C y 4.4.
- [x] 2.5 N-13: Alinear alcance a comunidades técnicas de Reddit, matizar aporte léxico local.
- [x] 2.6 N-14: Pasada de inconsistencias internas con tabla del tribunal. Unificar cifras/estados.

## 3. V3 pendientes (H-01, H-02, H-06, H-07, H-15)
- [x] 3.1 H-01: Evitar "irreversible", clarificar reversible por custodio de clave, rotación, destino clave anterior.
- [x] 3.2 H-02: Ajustar "alertas tempranas" a lo implementado (diario) o justificar. Revisar 4.5, 5.4, 7.2.
- [x] 3.3 H-06/H-07: Mantener throughput NO EVALUADO con medición faltante. Asegurar consistencia Resumen/Tablas y reproducibilidad.
- [x] 3.4 H-15: Fortalecer Anexo B con código SQL/nodos clave si falta.

## 4. Formales/menores y verificación
- [x] 4.1 Pasada m-21 a m-30 (figuras, herramientas, índice, ON CONFLICT, etc.)
- [x] 4.2 Verificar coherencia con devolución V4 ítem por ítem (usar Excel del tribunal)
- [x] 4.3 Regenerar PDF con `python docs/scripts/convertir_pdf.py` y verificar gates con `verificar_pdf.py`
- [x] 4.4 Revisar diff vs V4 aprobado y asegurar que no se reintroducen marcadores `@@@`

## Workflow follow-up
- Seguir correcciones incrementalmente por el Excel del tribunal
- No bloquear por firma de declaraciones hasta tener lo sustantivo listo
- Si se modifican tablas/índices, regenerar PDF y actualizar registro
