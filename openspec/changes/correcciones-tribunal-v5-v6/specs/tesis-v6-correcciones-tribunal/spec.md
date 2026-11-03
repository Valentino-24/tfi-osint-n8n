# Spec Delta

## Purpose

Especifica el proceso trazable para generar la Versión 6 del TFI (tesis_v6.md/pdf) aplicando todas las correcciones obligatorias de la devolución V5 que pueden resolverse con el material existente, manteniendo trazabilidad ítem por ítem y documentando explícitamente las acciones que requieren instancia institucional.

## ADDED Requirements

### Requirement: Generate V6 from V5 with traceable corrections
The system SHALL generate `docs/informe/tesis_v6.md` from `docs/informe/tesis_v5.md` applying corrections mapped to N-15..N-19, H-01/H-07/H-09/H-11/H-12/H-13/H-14/H-15, N-01/N-02/N-05/N-06/N-07/N-08/N-09/N-10/N-11/N-12/N-13/N-14 and all m- items identified in the V5 review.

#### Scenario: All major corrections applied
- **WHEN** building V6
- **THEN** N-15 (idioma), N-16 (etiquetado), N-17 (régimen), N-18 (código/esquema), N-19 (inconsistencias) are addressed with explicit changes

### Requirement: Document institutional pending items
The system SHALL explicitly document in V6 that signatures for Anexo E/Hoja de firmas and delivery of frozen copy/repo with verifiable hash require institutional action, without inventing them.

#### Scenario: Anexo E shows pending institutional items
- **WHEN** reviewing Anexo E
- **THEN** (a) firmas and (b)-(f) are handled as specified, with clear "pendiente / acción institucional" notes where applicable

### Requirement: Generate PDF and validate
The system SHALL generate `docs/informe/tesis_v6.pdf` using the existing pipeline and run validation.

#### Scenario: PDF pipeline executed
- **WHEN** conversion runs
- **THEN** `python docs/scripts/convertir_pdf.py` is executed and `docs/scripts/verificar_pdf.py` results are reviewed
