# seleccion-corpus-evaluada

## ADDED Requirements

### Requirement: La señal por comunidad se mide antes de fijar el corpus

El proyecto MUST medir la señal del clasificador por comunidad, sobre un número declarado de posts por comunidad, ANTES de decidir qué comunidades integran el corpus. La medición MUST usar el mismo diccionario para todas las comunidades, para que la comparación entre ellas sea válida.

El proyecto MUST separar en el informe dos cosas que la medición permite distinguir: la capacidad del clasificador y la temática de la comunidad.

#### Scenario: La medición usa el mismo diccionario en todas las comunidades

- **WHEN** se compara la señal de dos comunidades
- **THEN** la medición de ambas usa la misma versión del diccionario y el mismo umbral, de modo que la diferencia observada no proviene de un ajuste distinto por comunidad

#### Scenario: Cada comunidad aporta un número declarado

- **WHEN** se lee la medición de señal por comunidad
- **THEN** cada comunidad aparece con el número de posts efectivamente evaluados, no solo con su porcentaje

#### Scenario: Una comunidad con cero señal aparece en el informe

- **WHEN** una comunidad monitorizada aporta cero detecciones
- **THEN** aparece en el informe con su cero y con el denominador usado, porque su ausencia es un dato y no un hueco de la tabla

#### Scenario: El informe distingue clasificador de comunidad

- **WHEN** se lee el informe de medición
- **THEN** declara explícitamente que una tasa alta indica señal en el corpus y no mejor capacidad del clasificador, y viceversa

### Requirement: La evidencia de medición se archiva y es reproducible

La medición MUST archivarse en `V4/evidencias/` con la consulta que la produjo, su fecha, el identificador de la ventana, el `n` por comunidad y la versión del diccionario usada. La evidencia MUST ser reproducible por reejecución de la consulta.

#### Scenario: La cabecera documenta la procedencia

- **WHEN** se lee la cabecera de la evidencia de medición
- **THEN** incluye la consulta SQL usada, la fecha de ejecución, el identificador de la ventana, el `n` por comunidad y la versión del diccionario

#### Scenario: Reejecutar la consulta reproduce la cifra

- **WHEN** alguien reejecuta la consulta de la cabecera en la fecha archivada
- **THEN** obtiene la misma cifra, porque la consulta es de solo lectura y está acotada por la fecha de la ventana

#### Scenario: Ninguna cifra de esta evidencia se deriva de V2 o V3

- **WHEN** se busca el origen de cualquier cifra de la evidencia
- **THEN** el origen es una consulta sobre `tesi_osint` o un export fechado, nunca una cifra de V2/V3 ni una tasa supuesta

### Requirement: Elegir el corpus por su rendimiento está descartado

El proyecto MUST NOT seleccionar la composición del corpus en función de la tasa de detección que produce en él, porque esa tasa es la variable que se quiere medir y usarla para elegir el conjunto de prueba es sobreajuste del diseño experimental. Una comunidad con baja señal MUST NOT excluirse del corpus, y una comunidad con alta señal MUST NOT preferirse, por su tasa.

La decisión de composición MUST tomar como entrada la evidencia de medición y el criterio acordado con los autores, y MUST quedar registrada con su motivo.

#### Scenario: Una comunidad de alta señal no se prefiere por su tasa

- **WHEN** una comunidad muestra una tasa de señal alta
- **THEN** su inclusión en el corpus no se justifica por esa tasa, y el motivo declarado de su inclusión es otro

#### Scenario: Una comunidad de baja señal no se excluye por su tasa

- **WHEN** una comunidad muestra una tasa de señal baja o nula
- **THEN** permanece en la consideración del corpus y su señal se reporta como hallazgo, porque excluirla por su rendimiento sesgaría la medición

#### Scenario: La decisión queda registrada con su motivo

- **WHEN** los autores fijan la composición final del corpus
- **THEN** la decisión queda registrada con su fecha, su responsable, el motivo y la evidencia de medición que la sustentó

### Requirement: La tasa de señal del corpus fijado no es una estimación de desempeño

Cuando el corpus de la ventana MUST haberse compuesto después de medir la señal por comunidad, el proyecto MUST declarar que la tasa observada en ese corpus no puede usarse como estimación de desempeño, porque la composición se apoyó en esa misma tasa. La cifra MUST archivarse como caracterización del corpus y MUST NOT presentarse como recall, como precisión ni como medida de la capacidad del clasificador.

La estimación de desempeño MUST provenir exclusivamente de la muestra de control etiquetada, que es independiente del corpus de resultados.

La discontinuidad de cobertura MUST quedar registrada: la ventana pasa a tener dos segmentos con corpus distintos, y toda métrica por comunidad MUST declarar a cuál segmento pertenece.

#### Scenario: La cifra del corpus carries la advertencia de selección

- **WHEN** se lee la evidencia de señal del corpus final
- **THEN** declara que el corpus se fijó después de la medición, que dos de sus comunidades se eligieron por su tasa, y que la cifra no es una estimación de desempeño

#### Scenario: Ninguna cifra de señal se usa como recall

- **WHEN** se busca una afirmación de recall o precisión del clasificador
- **THEN** no puede provenir de la tasa de señal por comunidad, porque esa tasa depende de la composición del corpus y la composición se derivó de ella

#### Scenario: La discontinuidad de cobertura es visible

- **WHEN** se consulta cualquier métrica agrupada por comunidad sobre la ventana
- **THEN** se distingue el segmento previo al cambio de corpus del posterior, con la fecha de corte entre ambos y el `n` de cada segmento

#### Scenario: Los posts previos no se reprocesan

- **WHEN** el corpus cambia
- **THEN** los posts existentes conservan su clasificación, no se reclasifican ni se reprocesan, y su exclusión del corpus de resultados queda declarada con su motivo

### Requirement: La composición del corpus se decide por criterio declarado, no por rendimiento

La inclusión y la exclusión de una comunidad MUST justificarse por un criterio declarado de antemano —su tema, su alcance o su rol en la pregunta de investigación— y MUST NOT justificarse por su tasa de detección. El proyecto MUST registrar la composición con su fecha, su responsable y el criterio aplicado.

Cuando una comunidad se desactive por decisión de alcance, sus posts MUST conservarse y su ausencia MUST reportarse con su causa. La cobertura MUST NOT completarse con datos de otra fuente para disimular el cero resultante.

#### Scenario: La composición declara su criterio

- **WHEN** se lee la decisión de composición del corpus
- **THEN** enuncia el criterio de inclusión, la fecha, el responsable, y no invoca la tasa de detección como motivo

#### Scenario: Desactivar es la vía, borrar no

- **WHEN** una comunidad con posts deja de formar parte del corpus
- **THEN** se desactiva con `active_monitoring = false` y sus posts permanecen en la base; ninguna fila con posts se elimina

#### Scenario: El cero de una comunidad desactivada se declara

- **WHEN** una comunidad desactivada aporta cero posts en el segmento de la ventana que la contiene
- **THEN** ese cero se declara con su causa y no se sustituye por el volumen de otra comunidad

#### Scenario: El intercambio de cobertura se declara como intercambio

- **WHEN** el cambio de corpus reduce la cobertura local del resultado
- **THEN** se declara que la ventana pierde contexto local generalista y gana contexto local técnico, como intercambio deliberado y no como mejora de la representatividad

### Requirement: El identificador de comunidad se declara en su forma canónica

El identificador de cada comunidad MUST declararse en `PREPARE_SUBS` con la misma forma de mayúsculas y minúsculas con la que aparece en los permalinks de sus posts, porque `subreddit_id` se deriva del enlace y se compara de forma exacta contra la clave foránea.

El proyecto MUST verificar esa forma contra un feed real antes de fijar la composición, y MUST corregir el identificador en el origen que lo genera.

#### Scenario: La forma canónica está verificada contra un feed real

- **WHEN** se incorpora una comunidad al corpus
- **THEN** su identificador se verificó contra los permalinks de su feed, y se registró la forma observada

#### Scenario: Una comunidad con mayúscula inicial no falla por clave foránea

- **WHEN** una comunidad aparece con mayúscula inicial en sus permalinks
- **THEN** su identificador en `PREPARE_SUBS` la reproduce, y la inserción no viola la clave foránea

#### Scenario: El identificador incorrecto se corrige en el origen

- **WHEN** el identificador declarado no coincide con la forma de los enlaces
- **THEN** se corrige en la fuente que lo genera y se regenera el artefacto, sin desactivar la comunidad ni borrar sus filas

### Requirement: La mitigación del rate limiting se aplica por espaciado y se documenta

Cuando una fuente imponga un límite de frecuencia, el proyecto MUST espaciar las llamadas lo suficiente para que la fuente responda, y MUST registrar en la evidencia qué espaciado se usó, qué espaciado falló y con qué síntoma. Los reintentos acelerados MUST NOT usarse como mecanismo principal de mitigación, porque cada intento dentro de la ventana de bloqueo renueva el bloqueo y aumenta el tiempo de recuperación.

El reintento con espera MUST conservarse únicamente como red de seguridad ante fallos transitorios, con su número de intentos y su espera declarados.

#### Scenario: La mitigación configurada coincide con la documentada

- **WHEN** se lee la evidencia de caracterización del rate limiting
- **THEN** la mitigación que documenta es la que el workflow ejecuta, incluida la espera entre llamadas, y no una espera entre reintentos que el workflow no aplica

#### Scenario: El espaciado que falló queda registrado

- **WHEN** un espaciado menor produjo errores de la fuente
- **THEN** el documento registra el espaciado que falló, el síntoma observado y la fecha, para que nadie lo vuelva a elegir sin evidencia

#### Scenario: El síntoma de la fuente se distingue del fallo del sistema

- **WHEN** la fuente rechaza una consulta
- **THEN** la evidencia distingue un rechazo de la fuente de un fallo del pipeline, y el flujo continúa con el resto de las comunidades en lugar de abortar la corrida completa

#### Scenario: La superposición de ciclos se reporta

- **WHEN** una corrida excede el intervalo del scheduler y se superpone con la siguiente
- **THEN** la superposición se reporta en la bitácora, no se oculta ni se resuelve silenciosamente ajustando parámetros sin registro

### Requirement: El rate limiting nunca se resuelve desactivando una comunidad con datos

Un subreddit habilitado que no aporta posts por rate limiting MUST permanecer habilitado, y su ausencia MUST reportarse con su causa. La cobertura MUST NOT completarse con datos de otra fuente para disimular un cero.

#### Scenario: Ninguna comunidad se desactiva para mejorar la cobertura

- **WHEN** un subreddit habilitado no aporta datos por rate limiting
- **THEN** permanece con `active_monitoring` en `true` y su ausencia se reporta con la causa del rate limiting

#### Scenario: El cero no se rellena con datos de otro origen

- **WHEN** una comunidad aporta cero posts en la ventana
- **THEN** ese cero se conserva en el denominador de cualquier métrica por comunidad y no se sustituye por el volumen de otra

#### Scenario: Una comunidad con inconsistencias de identificador se corrige en el origen

- **WHEN** el identificador de una comunidad en la tabla no coincide con la forma que aparece en la URL de sus posts
- **THEN** la corrección se aplica en el origen que la genera, y no se resuelve desactivando la comunidad ni borrando sus filas
