# Spec Delta

## Purpose

Garantiza que la validación del clasificador se realice sobre el corpus B5 con metodología reproducible, consenso entre anotadores, acuerdo medido y estimadores ponderados por estrato.

## ADDED Requirements

### Requirement: Validation on B5 corpus
The system SHALL validate the classifier on a sample drawn from the B5 corpus (not from the preliminary 30/09 sample alone) with censo of threats and random sample of "No relevante".

#### Scenario: Sample is from B5
- **WHEN** reviewing validation results
- **THEN** the validation is performed on B5 with documented strata and sizes

### Requirement: Inter-annotator agreement
The validation SHALL include agreement between annotators (measured) and a clear description of consensus/adjudication. Given three authors, agreement SHALL be reported with appropriate measure.

#### Scenario: Agreement is reported
- **WHEN** reviewing the validation
- **THEN** inter-annotator agreement is reported with the methodology used

### Requirement: Weighted estimation
Performance metrics SHALL use weighted estimators by stratum with confidence intervals, and results SHALL be disaggregated for r/devsarg.

#### Scenario: Metrics are weighted
- **WHEN** reviewing precision/sensitivity/F1
- **THEN** they are reported with weighting and intervals, and disaggregated by community where relevant
