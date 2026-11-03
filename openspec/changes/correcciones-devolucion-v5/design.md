# Design

## Context

Se trata de corregir el informe `docs/informe/tesis_v5.md` para pasar a V6 tras la devolucion V5. Los cambios son mayoritariamente de redaccion, consistencia numerica, evidencia y anexos. No hay cambio de arquitectura del sistema n8n/Postgres.

## Goals / Non-Goals

**Goals:**
- Cerrar los 5 items bloqueantes (N-07, N-16, N-15, N-17/N-19, H-07)
- Cerrar mayores/altos restantes
- Mantener trazabilidad con consultas SQL sobre datos reales
- Regenerar PDF con verificacion OK

**Non-Goals:**
- Recolectar nueva ventana completa
- Reescribir todo el informe
- Cambiar el pipeline

## Decisions

- Seguir usando el mismo generador `docs/scripts/convertir_pdf.py` (Word COM) para pasar las compuertas
- Mantener evidencias en `docs/evidencias/` versionadas
- Formalizar Anexo E con firmas por canal institucional
- Declarar version transcripta vs ejecutada cuando difiera

## Risks / Trade-offs

- [Riesgo] Word COM bloqueado -> Mitigacion: limpiar temp y matar procesos, usar ruta fuera de OneDrive
- [Riesgo] Cambios en MD rompen numeracion -> Mitigacion: regenerar PDF y correr verificar_pdf.py
- [Riesgo] Firmas pendientes -> Mitigacion: documentar en Anexo E y entregar por canal institucional
