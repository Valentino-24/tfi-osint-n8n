# Spec Delta

## Purpose

Asegura la trazabilidad entre versiones del informe (V2/V3/docs/V5), documentando el ciclo de vida de los datos, el origen de las cifras y dejando verificable qué se retiró. Debe quedar reflejado en el Anexo E y referenciado desde el cuerpo del informe.

## ADDED Requirements

### Requirement: Declaration of version traceability
The system SHALL include a *Declaración de trazabilidad entre versiones* in the report that documents the data lifecycle (B4, preliminary sample 25-30/09, TRUNCATE, window B5), what was removed from previous versions, and that no figures in the current report derive from V2/V3 figures. 

#### Scenario: Traceability is present
- **WHEN** reviewing the report
- **THEN** Anexo E exists with the traceability declaration and it is referenced from section 4.7

### Requirement: Traceability reflects actual data flow
The declaration MUST state the TRUNCATE on 01/10/2026, the change of subreddits (removal of r/argentina/r/DerechoGenial, addition of r/netsec/r/Malware), and the cutoff dates.

#### Scenario: Lifecycle dates are explicit
- **WHEN** reading the traceability declaration
- **THEN** key dates (24/09 B4, 25-30/09 sample, 01/10 TRUNCATE/restart, 17/10 cutoff, 18/10 corpus cutoff) are documented
