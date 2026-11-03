# Design

## Context

Ver proposal.md. La devolución V5 identifica correcciones obligatorias para avanzar a V6. El entregable actual es `docs/devoluciones/tesis_v5.md` / `tesis_v5.pdf`. Debemos generar `docs/informe/tesis_v6.md` y `docs/devoluciones/tesis_v6.pdf` aplicando correcciones trazables sin recolectar/etiquetar nuevo.

## Goals / Non-Goals

**Goals:**
- Crear `docs/informe/tesis_v6.md` basado en `docs/devoluciones/tesis_v5.md` con correcciones sistemáticas por ítem V5.
- Corregir N-15 (idioma), N-16 (etiquetado/referencia), N-17 (régimen operación), N-18 (código/esquema), N-19 (inconsistencias).
- Actualizar Anexo E atendiendo (b)-(f), documentando (a) firmas y entrega de copia/repositorio como pendientes institucionales.
- Corregir formales m-28, m-30, m-34, m-35, m-36, m-37, m-38.
- Generar `tesis_v6.pdf` con pipeline existente y validar con `verificar_pdf.py`.
- Mantener trazabilidad de cambios por sección/tabla/figura.

**Non-Goals:**
- Recolectar datos nuevos o re-etiquetar corpus.
- Inventar firmas manuscritas/digitales o copiar repositorio con hash.
- Publicar/activar workflow en n8n.
- Modificar `docs/devoluciones/tesis_v5.md` (mantener como referencia).
- Resolver todo lo institucional fuera del alcance del informe (solo documentar).

## Decisions

| Decisión | Rationale | Alternativas consideradas |
|---|---|---|
| Partir de `docs/devoluciones/tesis_v5.md` y escribir `docs/informe/tesis_v6.md` | Mantiene estructura, figuras, tablas y datos ya validados; aplica correcciones mínimas trazables. | Reescribir desde cero (alto riesgo de introducir errores). **Elegida.** |
| Documentar pendientes institucionales explícitamente | Tribunal exige firmas/copia repo (bloqueantes) pero no podemos generarlos; mejor dejar claro estado y qué falta. | Omitir (riesgoso) o inventar (inaceptable). **Elegida.** |
| Corregir interpretación por idioma con cálculos existentes | Usar datos de tablas 5.7/5.9/5.9.b para estimar sensibilidad por comunidad con pesos (postestratificación) tal como indica V5. | Re-etiquetar (imposible/no pedido). **Elegida.** |
| Usar "instancia de n8n" vs "motor" | Elimina ambigüedad señalada en N-17. | Mantener (causa confusión). **Elegida.** |
| Clarificar versión transcripta vs operada en Anexo B | V5 señala diferencias (diccionario post-ventana). Documentar diferencia sin afirmar que es la ejecutada. | Ocultar (contradice auditoría). **Elegida.** |

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Errores al reescribir texto crean nuevas inconsistencias | Hacer pasadas por N-19, verificar tablas/figuras referenciadas, usar checklist item por item. |
| Cambios afectan numeración/índices | Revisar índice general, numeración secciones/tablas/figuras, epígrafes. |
| Pipeline PDF falla por formato | Usar `convertir_pdf.py` tal como documentado, revisar salida con `verificar_pdf.py`. |
| Olvidar algún ítem menor | Seguir tabla comparativa completa de la conversación. |
| Confundir "motor de anomalías" vs "instancia n8n" | Buscar/reemplazar con contexto y revisar secciones señaladas. |
