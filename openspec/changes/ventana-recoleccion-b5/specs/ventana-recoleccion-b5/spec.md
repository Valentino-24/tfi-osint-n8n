# ventana-recoleccion-b5

## ADDED Requirements

### Requirement: Ventana real de recolección con inicio fechado

El sistema de documentación del proyecto MUST definir la ventana real de recolección B5 con una fecha de inicio explícita e inmutable de **2026-09-25**, y MUST reemplazarla en toda mención a la ventana ficticia de seis meses de V2/V3 (SU-02).

La ventana MUST definirse sobre el campo `posts.ingested_at`, no sobre `posts.created_utc`, porque `ingested_at` es la evidencia de lo que el sistema efectivamente recolectó.

#### Scenario: La fecha de inicio está escrita y es verificable

- **WHEN** un lector busca la fecha de inicio de la ventana en la documentación del proyecto
- **THEN** encuentra la fecha 2026-09-25, explícitamente rotulada como inicio de la ventana real B5

#### Scenario: La ventana ficticia de seis meses ya no aparece

- **WHEN** se revisa la documentación del proyecto en busca de una ventana de recolección de seis meses
- **THEN** no queda ninguna afirmación de que la recolección cubra seis meses; toda mención apunta a la ventana real y a su duración declarada

#### Scenario: El corpus de la ventana se define por ingested_at

- **WHEN** se calcula el corpus de la ventana
- **THEN** el criterio es el conjunto de posts con `ingested_at` dentro del rango de la ventana, y ese criterio queda escrito junto a la definición

#### Scenario: Los posts previos a la ventana no se mezclan silenciosamente

- **WHEN** un post fue ingerido antes de 2026-09-25, como los 201 posts verificados de la corrida B4 del 2026-09-24
- **THEN** ese post no pertenece al corpus de la ventana salvo decisión explícita de los autores registrada como cambio de alcance; si no hay decisión, la exclusión queda declarada en la evidencia

### Requirement: Fecha de corte como decisión abierta

La fecha de corte de la ventana MUST representarse como una decisión explícitamente pendiente de los autores con sus directores, y MUST NOT recibir un valor por defecto ni una fecha tentativa sin rotular.

El valor en la documentación MUST ser un estado explícito de "no fijada" acompañado de su motivo, nunca un campo vacío que pueda leerse como un olvido (RN-GL-03).

#### Scenario: El corte aparece como no fijado y con motivo

- **WHEN** se lee la definición de la ventana
- **THEN** el corte figura con el estado explícito "no fijada", la razón de que depende de los autores con sus directores, y el nombre de la tarea o decisión que lo cierra

#### Scenario: Ninguna fecha se inventa como corte

- **WHEN** se busca en los artefactos de esta change una fecha de corte propuesta, incluida una dentro de un texto que la sugiera como aceptable
- **THEN** no existe: el corte no tiene valor hasta que los autores lo decidan

#### Scenario: La decisión pendiente es rastreable

- **WHEN** se necesita saber quién decide el corte y qué lo desbloquea
- **THEN** la documentación identifica a los autores con sus directores como decisores y lista los changes que dependen del corte

### Requirement: Criterio de suficiencia de la ventana

La ventana MUST declarar un criterio de suficiencia verificable, basado en que el motor de anomalías tenga **10 días completos de evaluaciones** registradas en `anomalias`, porque RN-AN-02 usa la media diaria de los diez días previos y sin esa historia la base comparativa no existe.

El estado de acumulación MUST registrarse de forma consultable día a día, y MUST NOT estimarse.

#### Scenario: El umbral de suficiencia está declarado y justificado

- **WHEN** se lee el criterio de suficiencia de la ventana
- **THEN** declara las 10 evaluaciones completas requeridas y explica que ese número proviene de la base comparativa de RN-AN-02, no de una elección arbitraria

#### Scenario: Antes del umbral la ventana se declara abierta

- **WHEN** la ventana acumula menos de 10 días completos de evaluaciones
- **THEN** se declara abierta y el estado se reporta como limitación de la base comparativa, nunca como ausencia de anomalías (RN-AN-06)

#### Scenario: El estado de acumulación es verificable

- **WHEN** se consulta el estado de acumulación de la ventana
- **THEN** se obtiene un conteo de días completos evaluados derivado de las filas de `anomalias`, con la consulta usada y no con una estimación manual
