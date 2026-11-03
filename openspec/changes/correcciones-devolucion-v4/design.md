# Design

## Context

Ver devolución V4: bloqueantes N-07 y N-08. Ya hay V5 regenerado con PDFs/registro. El tribunal acepta correcciones incrementales por Excel. Hay evidencias en `docs/evidencias/informe_v5_2026-10-20/` incluyendo validación y declaración de trazabilidad parcial.

## Goals / Non-Goals

**Goals:**
- Cerrar o dejar en estado aceptable N-07 y N-08
- Corregir mayores (N-09 a N-14) y observaciones V3 con mayor impacto
- Mantener coherencia entre MD, tablas, figuras y anexos
- Poder regenerar PDF con `python docs/scripts/convertir_pdf.py` tras cambios

**Non-Goals:**
- Rehacer todo el informe desde cero
- Firmar físicamente las declaraciones (se dejan espacios si aplica)
- Agregar nuevas secciones masivas si no son necesarias

## Decisions

- **Trazabilidad (N-07):** Completar Anexo E con ciclo de vida claro, citas a evidencias, y dejar explícito que cifras no provienen de V2/V3. Si se solicita firma de autores/dirección, dejar espacios como ya está.
- **Validación (N-08):** Usar lo ya existente en `informe_v5_2026-10-20/` (muestra, consenso, análisis) y asegurar que se reporte acuerdo entre anotadores, ponderación por estrato, intervalos, desglose por r/devsarg, conciliación de transición. Aprovechar que ya hay kappa/consenso.
- **Identificadores (N-10):** Ya corregido mayormente con códigos C-XX; verificar que no queden IDs/títulos literales.
- **Motor anomalías (N-11):** Ya recalculado con created_utc; mantener declaración honesta "eficacia no demostrada".
- **Edición incremental:** Trabajar por bloques (anexos primero para bloquear, luego cuerpo, luego figuras/formales) para poder ir subiendo al Excel.

## Risks / Trade-offs

- [Riesgo] Tocar tablas puede romper numeración → Mitigación: revisar índices tras cambios
- [Riesgo] Regenerar PDF varias veces con Word COM puede colgar en OneDrive → Mitigación: usar `%TEMP%\tfi_tesis_build` (ya implementado)
- [Riesgo] No cerrar N-07/N-08 completamente → Mitigación: dejar claro qué falta y asegurarnos de tener evidencia para el Excel
