# recoleccion-secundaria

## ADDED Requirements

### Requirement: El corpus de B5 queda delimitado por un límite temporal fijo y único

El corpus de la ventana B5 MUST definirse por el intervalo `posts.ingested_at ∈ [2026-09-25 00:00:00 -03:00, 2026-10-18 00:00:00 -03:00)`, y todo post ingerido a partir del instante superior MUST tratarse como recolección secundaria, no como parte de la ventana. El criterio análogo en `anomalias` es `ventana_fin <= 2026-10-18 00:00:00 -03:00`.

La frontera MUST ser temporal y fija: MUST NOT depender del instante de ejecución de la consulta, ni del estado del workflow, ni de la fecha en que se lea la evidencia.

#### Scenario: Un post posterior al corte no entra al corpus

- **WHEN** un post tiene `ingested_at >= 2026-10-18 00:00:00 -03:00`
- **THEN** no cuenta en el acumulado de B5 ni en ninguna métrica de la ventana, aunque resida en la misma tabla `posts`

#### Scenario: El acumulado no se mueve con el paso del tiempo

- **WHEN** se repite la consulta del corpus en fechas distintas
- **THEN** devuelve siempre el mismo acumulado (**724** posts) y el mismo conteo de días (**15**), porque el límite superior es un instante fijo y no el instante de ejecución

#### Scenario: El track queda fuera del conteo de días evaluados

- **WHEN** se cuenta el criterio de suficiencia de la ventana sobre `anomalias`
- **THEN** solo cuentan las filas con `ventana_fin <= 2026-10-18 00:00:00 -03:00` y las posteriores quedan excluidas

### Requirement: La recolección posterior al corte se registra como track secundario con bitácora propia

La recolección posterior al corte MUST continuar registrándose día a día en la bitácora, y cada entrada de un día posterior al corte MUST declararlo como tal en su título y en su cuerpo, con la naturaleza del `n` y congelados el acumulado y el conteo de días de B5.

Si durante un día posterior al corte el workflow permanece inactivo sin ninguna ejecución, ese día MUST registrarse como **constancia de un día sin recolección**, no como falla del pipeline ni como silencio de los subreddits (RN-GL-01).

#### Scenario: Día posterior al corte con recolección

- **WHEN** hay recolección en un día posterior al `2026-10-17`
- **THEN** se genera su entrada de bitácora con el rótulo de día posterior al corte, su `n` propio, y el acumulado de B5 permanece en 724 y los días en 15

#### Scenario: Día posterior al corte sin recolección

- **WHEN** el workflow permanece inactivo durante un día entero posterior al corte
- **THEN** la entrada declara `n = 0`, el estado del workflow como inactivo y el hecho como decisión de jornada sin operación, con su evidencia

#### Scenario: El total de la base no se confunde con el acumulado de la ventana

- **WHEN** se consulta el total de `posts` en la base
- **THEN** el total (ventana + previos + track) se reporta separado del acumulado de B5, con cada cifra identificada

### Requirement: Ninguna métrica del track secundario se presenta como evidencia de B5

Ningún conteo ni resultado derivado de datos posteriores al corte MUST presentarse como métrica de la ventana B5 ni del capítulo 5 de la tesis. Las cifras de la ventana (acumulado, días, serie diaria, anomalías) MUST permanecer congeladas en sus valores de cierre.

Toda métrica producida desde el track MUST acompañarse de su consulta, su fecha, su ventana de observación y su número de observaciones (RN-GL-01).

#### Scenario: Se produce un conteo con datos del track

- **WHEN** se calcula un conteo que incluye datos posteriores al corte
- **THEN** se declara explícitamente que pertenece al track secundario y no a B5, con su consulta, su ventana y su `n`

#### Scenario: Se publica el acumulado de la ventana

- **WHEN** se reporta el acumulado de B5
- **THEN** es **724** posts y **15** días con su corte `2026-10-17`, sin incluir ningún dato del track

### Requirement: Extender el corte es una enmienda documentada de la decisión de cierre

Si se decide extender la ventana más allá del `2026-10-17`, la decisión MUST registrarse como enmienda de DD-08 y de `VENTANA_B5.md` §3, con la nueva fecha de corte, el responsable, la fecha de la decisión, el motivo y el efecto sobre las métricas ya publicadas, **antes** de recalcular el acumulado o los días.

#### Scenario: Se pide extender la ventana

- **WHEN** los autores o sus directores deciden cerrar en una fecha posterior al `2026-10-17`
- **THEN** la enmienda queda registrada con su trazabilidad y recién entonces se recalculan el acumulado y el conteo de días, actualizando también `V4/scripts/bitacora_b5.py`

#### Scenario: No hay enmienda registrada

- **WHEN** no existe una enmienda de DD-08 con la trazabilidad completa
- **THEN** el corte sigue siendo `2026-10-17` y los datos posteriores siguen siendo track secundario, aunque estén en la misma base

### Requirement: El track no publica ni modifica el workflow

Este change MUST NOT publicar ni activar el workflow en n8n: la republicación es del operador, manualmente desde la UI (regla dura del proyecto). El change MUST NOT modificar el DDL, el artefacto del workflow, los nodos, las credenciales ni la clave HMAC.

#### Scenario: Implementación sin publicación

- **WHEN** se ejecutan las tareas de este change
- **THEN** ninguna publica ni activa un workflow, ninguna altera `V4/anexos/B_workflow.json` ni `V4/scripts/generar_workflow.py`, y ninguna toca credenciales o HMAC

#### Scenario: Base intacta

- **WHEN** se revisan las interacciones con `tesi_osint`
- **THEN** son solo consultas `SELECT` de conteo y agregación: sin escrituras, `DELETE`, `TRUNCATE` ni `ALTER`
