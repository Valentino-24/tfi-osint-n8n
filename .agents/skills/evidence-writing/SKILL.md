---
name: evidence-writing
description: Evidence-first technical writing for TFI OSINT/n8n. Use when writing V4/evidencias/*, bitácoras, VENTANA_B5.md, verifications, or any document that must state metrics with traceability. Enforces "no metric without query/date/window/n" and RN-GL-01/RN-GL-02.
---

# Evidence Writing (TFI OSINT/n8n)

## Goal
Produce documents that are **evidence, not results**. Every numeric claim must be reproducible from `tesi_osint` with a literal query and context.

## Mandatory structure
For any evidentiary document include:
- **Objetivo / alcance** - What is being evidenced (window, date, artifact)
- **Fuente** - DB/table/script (`psql`, `V4/scripts/...`, n8n SQLite read-only, etc.)
- **Consulta SQL literal** - Copy/pasteable, no paraphrases
- **Fecha/hora de ejecución** - With timezone (`America/Argentina/Buenos_Aires`) when relevant
- **Ventana** - Define `ingested_at`/`created_utc` range explicitly
- **n / observaciones** - Count of observations used
- **Cifras** - Only counts/operational numbers. Do NOT present E4-E8/Table 3/Kappa/matrix as "results" unless explicitly produced
- **Limitaciones** - Rate limiting, partial day, instance down, no log, single annotator, etc.
- **Trazabilidad** - Link to related files (bitácora, verification, change)

## Hard rules (project)
- **RN-GL-01:** Never declare a metric of results without its query, date, window and number of observations.
- **RN-GL-02:** Never complete percentages with V2/V3 data or assumed rates. Use only system data.
- **Ventana B5:** Prefer `posts.ingested_at` for "what the system collected". `created_utc` is publication time.
- **Subreddits:** Always use the **3 monitored subreddits of the scope** as denominator (include zeros). Never drop zeros.
- **B4 vs B5:** Posts from 2026-09-24 (B4) are outside B5 unless authors explicitly decide (task 6.3). Don't merge silently.
- **Rate limiting:** Report bias, don't compensate.
- **Anomalías:** If base incomplete, say "limitación de base comparativa", never "no anomalies".

## Writing checklist
- [ ] Query is literal and read-only (`SELECT`)
- [ ] Window defined explicitly
- [ ] `n` stated
- [ ] Timezone declared if mixing local/UTC
- [ ] No secrets/tokens/HMAC values
- [ ] No fabricated logs ("sin observación" if missing)
- [ ] References to changes/specs where decisions made

## Anti-patterns
- "Se observa que..." without numbers + query
- Percentages with missing denominator
- "Exitoso" when log not available
- Mixing B4/B5 totals without splitting
- Declaring F1/precision/recall from future changes as done
