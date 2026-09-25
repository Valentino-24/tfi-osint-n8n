# decision-cierre-ventana

## ADDED Requirements

### Requirement: La decisión de cierre se registra como decisión trazable

La decisión de los autores sobre la fecha de cierre de la ventana MUST registrarse en OpenSpec como decisión trazable, con su fecha, su responsable, su motivo y su efecto sobre los changes dependientes (RN-GL-03).

Mientras la decisión no exista, el estado MUST permanecer abierto y visible, no resuelto por omisión.

#### Scenario: La decisión queda registrada con su trazabilidad

- **WHEN** los autores fijan la fecha de corte
- **THEN** el registro contiene la fecha, quién la decidió, la fecha en que se decidió, el motivo y los changes que habilita

#### Scenario: Antes de la decisión el estado es abierto

- **WHEN** no hay decisión de cierre registrada
- **THEN** el estado de la ventana figura como abierto con el nombre de la decisión pendiente, y no como cerrado por default ni como pendiente sin responsable

### Requirement: La decisión sobre conservar o reiniciar la recolección queda registrada

La decisión de los autores sobre si se conserva la recolección actual o se reinicia con métricas corregidas MUST registrarse por separado de la fecha de corte, porque tiene consecuencias distintas sobre la comparabilidad de los resultados (pregunta abierta de prioridad Media).

#### Scenario: Reiniciar redefine el inicio de la ventana

- **WHEN** los autores deciden reiniciar la recolección con métricas corregidas
- **THEN** la fecha de inicio vigente pasa a ser la del reinicio y la ventana que empieza el 2026-09-25 queda documentada como descartada, con su razón

#### Scenario: Conservar deja el inicio vigente sin cambios

- **WHEN** los autores deciden conservar la recolección actual
- **THEN** el inicio 2026-09-25 permanece vigente y la decisión queda registrada con su motivo

### Requirement: Incluir o excluir los posts previos a la ventana es una decisión de los autores

Si los posts ingeridos antes del 2026-09-25, como los 201 verificados en la corrida B4 del 2026-09-24, se incluyen o no en el corpus de resultados, esa decisión MUST registrar de los autores.

#### Scenario: Por defecto los posts previos quedan fuera

- **WHEN** no hay decisión registrada sobre los posts previos a la ventana
- **THEN** el corpus de resultados los excluye y la exclusión queda declarada con su motivo

#### Scenario: Incluirlos es un cambio de alcance registrado

- **WHEN** los autores deciden incluir los posts previos al inicio de la ventana
- **THEN** el cambio queda registrado con su motivo, el criterio de inclusión y su efecto sobre las métricas ya publicadas; no se aplica como un ajuste silencioso de una consulta

### Requirement: El estado de la decisión no bloquea la recolección en curso

La resolución pendiente de la decisión de cierre MUST NOT interrumpir la recolección de la ventana ni requerir intervenciones sobre la base `tesi_osint`.

#### Scenario: La recolección sigue mientras la decisión está abierta

- **WHEN** la decisión de cierre sigue abierta
- **THEN** el sistema sigue recolectando normalmente y la bitácora sigue acumulando, sin que esta change requiera ninguna operación sobre `tesi_osint`

#### Scenario: Ninguna tarea de esta change altera la base

- **WHEN** se revisan las tareas de esta change
- **THEN** ninguna ejecuta una operación de escritura, `DELETE`, `TRUNCATE` ni `ALTER` sobre `tesi_osint`; las únicas interacciones son consultas `SELECT` de conteo y agregación
