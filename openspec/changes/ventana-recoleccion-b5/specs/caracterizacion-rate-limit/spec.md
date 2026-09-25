# caracterizacion-rate-limit

## ADDED Requirements

### Requirement: Caracterización de la ventana de rate limiting observada

El proyecto MUST mantener un documento de caracterización de la ventana real de rate limiting de Reddit observada en las corridas, que describa el comportamiento observado, su evidencia y su efecto sobre la recolección, cerrando el criterio pendiente de US-002.

La caracterización MUST describir lo observado y MUST NOT afirmar un umbral de requests que no se haya aislado con evidencia; lo no determinado MUST declararse como no determinado.

#### Scenario: La caracterización describe lo observado

- **WHEN** se lee el documento de caracterización
- **THEN** describe que Reddit devuelve 429 ante un exceso de requests desde la IP del proyecto, y cita la corrida o fecha en que se observó

#### Scenario: Lo no determinado se declara como tal

- **WHEN** no se pudo aislar la cantidad exacta de requests que dispara el 429
- **THEN** el documento lo declara como no determinado en lugar de estimarlo o de copiar un valor de documentación externa

#### Scenario: La mitigación configurada queda documentada

- **WHEN** se lee la caracterización
- **THEN** documenta la mitigación vigente: reintento hasta tres veces con 30 segundos de espera ante 429/403 y continuación con el resto del flujo (RN-FU-03)

### Requirement: La caracterización es acumulativa con evidencia fechada

Cada corrida que sufra rate limiting MUST sumar una fila fechada a la evidencia de caracterización, con la fecha, el subreddit afectado, el síntoma observado y la ejecución del ciclo.

#### Scenario: Cada incidente queda con fecha y traza

- **WHEN** ocurre un 429 en una corrida
- **THEN** la evidencia de caracterización suma una entrada con la fecha, el subreddit afectado, el síntoma y el ciclo de ingesta en que ocurrió

#### Scenario: La caracterización crece con la observación, no con suposiciones

- **WHEN** se consulta la evidencia de caracterización
- **THEN** su tamaño refleja los incidentes realmente observados en la ventana, sin filas de relleno ni ejemplos ilustrativos presentados como datos

### Requirement: El efecto del rate limiting sobre la cobertura se documenta

El proyecto MUST documentar el efecto del rate limiting sobre la cobertura por subreddit, con el caso verificado de `r/derechogenial` con 0 posts en la corrida B4 del 2026-09-24 (m-16, RN-GL-02).

#### Scenario: El caso de r/derechogenial queda documentado

- **WHEN** se busca el efecto del rate limiting en la cobertura
- **THEN** el documento registra que `r/derechogenial` está habilitado en `active_monitoring` pero no aportó posts por rate limiting, con la corrida y la fecha de la evidencia

#### Scenario: Ningún subreddit se desactiva para maquillar la cobertura

- **WHEN** un subreddit habilitado no aporta datos por rate limiting
- **THEN** permanece con `active_monitoring` en `true` y su ausencia se reporta con su causa; la cobertura nunca se completa con datos de otra fuente

### Requirement: La cobertura por subreddit conserva el denominador completo

Toda métrica expressada en porcentaje por subreddit MUST calcularse sobre el denominador de los tres subreddits monitorizados, incluyendo los que aportan 0, y MUST declarar ese `n` (RN-GL-02).

#### Scenario: El cero entra en el denominador

- **WHEN** se calcula un porcentaje de posts por subreddit en la ventana
- **THEN** el denominador es el total de los tres subreddits monitorizados, no solo el de los que aportaron posts

#### Scenario: Cada subreddit aparece con su n real

- **WHEN** se publica un desglose por subreddit
- **THEN** los tres subreddits aparecen con su recuento real, incluido el 0, y con la causa declarada cuando el 0 proviene del rate limiting
