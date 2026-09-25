# bitacora-evidencia-diaria

## ADDED Requirements

### Requirement: Una entrada de bitácora por día de la ventana

El proyecto MUST mantener una entrada de bitácora por cada día de la ventana de recolección, en `V4/evidencias/bitacora_b5/`, con nombre de archivo `YYYY-MM-DD.md` y formato de texto plano versionable.

Cada entrada MUST registrar: fecha, total de posts ingeridos, distribución de posts por subreddit, ejecuciones fallidas y la causa de cada una.

#### Scenario: La entrada del día existe y cubre los campos exigidos

- **WHEN** se abre la entrada de bitácora de una fecha de la ventana
- **THEN** contiene la fecha, el total de posts ingeridos, el desglose por subreddit y las ejecuciones fallidas con su causa

#### Scenario: Un día sin recolección igualmente se registra

- **WHEN** en una fecha de la ventana el sistema no ingirió posts
- **THEN** existe una entrada para esa fecha con total 0 y la causa, en lugar de omitir el día y dejar un hueco indistinguible de un forgot de registro

#### Scenario: La bitácora no se salta días

- **WHEN** se revisa el directorio de la bitácora contra el rango de fechas de la ventana
- **THEN** hay exactamente una entrada por día dentro de la ventana, sin fechas faltantes

### Requirement: Cada cifra de la bitácora lleva su consulta, fecha, ventana y n

Toda cifra registrada en la bitácora MUST estar acompañada de la consulta SQL literal que la produjo, la fecha de ejecución, el nombre de la ventana y el número de observaciones `n` (RN-GL-01, Flujo 3).

#### Scenario: La cabecera de la entrada documenta la procedencia

- **WHEN** se lee la cabecera de una entrada de bitácora
- **THEN** incluye la consulta SQL usada, la fecha de ejecución, el identificador de la ventana y el `n` de la observación

#### Scenario: Toda cifra es reproducible

- **WHEN** alguien reejecuta la consulta que figura en la cabecera de una entrada
- **THEN** obtiene la misma cifra, porque la consulta es de solo lectura y está acotada por la fecha de la ventana

#### Scenario: Ninguna cifra se deriva de V2 o V3

- **WHEN** se busca el origen de cualquier cifra de la bitácora
- **THEN** el origen es una consulta sobre `tesi_osint` o un export fechado, nunca una cifra de V2/V3 ni una tasa supuesta

### Requirement: La bitácora se genera por script de solo lectura

La bitácora MUST generarse con un script en `V4/scripts/` que tome la fecha como parámetro y ejecute únicamente consultas `SELECT` agregadas sobre `tesi_osint`. El script MUST NOT ejecutar sentencias de escritura, `DELETE`, `TRUNCATE`, `DROP` ni `ALTER`.

#### Scenario: El script está acotado a lectura

- **WHEN** se revisa el script de la bitácora
- **THEN** todas sus sentencias contra la base son `SELECT` y ninguna modifica datos ni esquema

#### Scenario: Reejecutar el script es inofensivo

- **WHEN** se ejecuta el script de la bitácora para una fecha ya registrada
- **THEN** el estado de la base no cambia y la entrada se regenera idéntica

#### Scenario: El script falla sin dejar la evidencia a medias

- **WHEN** la conexión a la base falla durante la generación
- **THEN** el script termina con error explícito y no escribe una entrada parcial que aparente una recolección completa

### Requirement: El origen de los datos de fallo queda declarado

El campo de ejecuciones fallidas MUST declarar su fuente, y cuando la fuente no esté disponible la entrada MUST registrar la ejecución como "sin observación" en lugar de asumir que fue exitosa (RN-GL-01).

#### Scenario: El campo de fallos declara su fuente

- **WHEN** se lee el campo de ejecuciones fallidas de una entrada
- **THEN** declara que la fuente es el log de ejecuciones de la instancia n8n y que fue transcrito manualmente a esa entrada

#### Scenario: Sin log disponible no se asume éxito

- **WHEN** no hay log de ejecuciones disponible para una fecha
- **THEN** la entrada marca esa ejecución como "sin observación" y la ausencia de log queda declarada, nunca como una ejecución exitosa
