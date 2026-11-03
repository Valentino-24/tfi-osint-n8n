# Spec Delta

## Purpose

Especifica las correcciones metodológicas obligatorias: interpretación por idioma, composición de la referencia de etiquetado, régimen de operación, versión del código/esquema transcritos y trazabilidad de versiones.

## ADDED Requirements

### Requirement: Correct language-based interpretation (N-15)
The system SHALL present sensitivity by community and language with weights and exact confidence intervals, rename the "Omisión" column to "proporción de amenazas en la muestra del estrato negativo", and rewrite affected sections/conclusions stating evidence is insufficient for Rioplatense lexicon with low point estimate where applicable.

#### Scenario: Tables 5.9/5.9.b updated
- **WHEN** reviewing validation
- **THEN** sensitivity per community/idioma is shown with weights/IC and conclusions corrected

### Requirement: Clarify labeling reference (N-16)
The system SHALL state 50 cases with consensus of three annotators and 302 with single annotator label, identify the annotator, report agreement on 50 common cases (binary/category), show range across annotators, and unify tool usage description.

#### Scenario: Reference composition explicit
- **WHEN** reading Resumen/Abstract/3.3.2/5.5/E.4
- **THEN** composition is unambiguous with required details

### Requirement: Document intermittent operation (N-17)
The system SHALL add a day-by-day operation table (start/end/auto/manual runs), compute operation fraction over same interval, explain evaluations 16/10-17/10, use "instancia de n8n" consistently, rewrite affected sections, and unify OE1 status.

#### Scenario: Regime clearly documented
- **WHEN** reviewing 5.1/5.3/6.2/7.2/7.3
- **THEN** regime is explicit and consistent

### Requirement: Clarify transcribed code/schema (N-18)
The system SHALL identify transcribed version vs operated (date/commit or differences), reconcile contradictory comments, clarify Anexo A (real schema or migration with date), quantify extractor errors and >=6 overlap pairs, and transcribe Parse Reddit Posts.

#### Scenario: Versioning explicit
- **WHEN** reviewing Anexos A/B/C
- **THEN** differences are stated and critical elements transcribed/clarified
