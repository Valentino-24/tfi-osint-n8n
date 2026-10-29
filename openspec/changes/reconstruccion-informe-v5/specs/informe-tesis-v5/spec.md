# informe-tesis-v5

## ADDED Requirements

### Requirement: El informe declara la trazabilidad entre versiones

El informe MUST incluir una **Declaración de trazabilidad entre versiones** firmada por los tres autores y conocida por la dirección, que enumere cada resultado cuantitativo de la V2 y la V3 ausente en la V5, indique su origen con una clasificación explícita (medición sobre corpus descartado, proyección, simulación, generación con herramienta de asistencia u otro), documente con fechas el ciclo de vida de los datos y el destino de lo eliminado, y declare si alguna cifra de la V5 deriva de material de la V2 o la V3.

#### Scenario: Cifra retirada con origen declarado

- **WHEN** el tribunal lee la Declaración y busca el corpus de la V3 de 8.240 publicaciones en 181 días
- **THEN** encuentra esa cifra, la versión de la que provino y su origen clasificado, sin ambigüedad

#### Scenario: Ciclo de vida de los datos fechado

- **WHEN** se recorre la línea de tiempo de datos
- **THEN** figuran B4 (24/09, descartado), el corpus del 25 al 30/09 con r/DerechoGenial y r/argentina, la depuración y B5 (01/10–17/10, corte 19/10), cada uno con fecha y con el destino de lo eliminado

#### Scenario: Declaración ausente bloquea la habilitación

- **WHEN** la V5 se entrega sin la Declaración firmada
- **THEN** la condición de habilitación a defensa no se cumple

### Requirement: El desempeño del clasificador se mide sobre el corpus evaluado

Si se realiza una validación nueva, el informe MUST construir una muestra extraída del corpus B5, con censo de las detecciones y muestra aleatoria reproducible de las publicaciones «No relevante»; MUST informar el tamaño del estrato «No relevante» (N₀); MUST usar dos o más anotadores independientes sobre una submuestra común con acuerdo interanotador (kappa); MUST ponderar los estimadores por estrato con sus intervalos de confianza; y MUST informar resultados separados por comunidad o idioma.

Si la validación nueva no se realiza, el informe MUST declarar la sensibilidad y el F1 como **NO EVALUADOS sobre el corpus**, mantener la precisión como valor indicativo debidamente rotulado, y MUST reescribir la conclusión general para no afirmar que la evidencia respalda el supuesto en la dimensión de clasificación.

#### Scenario: Estimadores ponderados con N₀ publicado

- **WHEN** se lee la sección de desempeño del clasificador
- **THEN** la precisión se calcula sobre el censo de detecciones y las métricas de sensibilidad y F1 usan pesos por estrato w = N₀/n₀, con N₀ informado y con intervalos de confianza

#### Scenario: Acuerdo interanotador informado

- **WHEN** el tribunal busca la fiabilidad del etiquetado
- **THEN** encuentra el kappa calculado sobre la submuestra común y la declaración de si alguna herramienta propuso o revisó etiquetas

#### Scenario: Sin segunda validación, todo queda declarado

- **WHEN** no hay un segundo anotador y se opta por no repetir la validación
- **THEN** la sensibilidad y el F1 figuran como NO EVALUADOS sobre el corpus y la conclusión general ya no sostiene el cumplimiento en clasificación

### Requirement: La evidencia es accesible y el código está transcripto

El informe MUST dar acceso verificable a la evidencia mediante una URL o una copia congelada con su hash SHA-256 declarado. El Anexo B MUST transcribir el código de los nodos HMAC Anonymize, Classify Dictionary, Extract Entities y Anomaly Engine, y el SQL de los nodos de persistencia y de las consultas que producen las tablas del Capítulo 5.

#### Scenario: Copia congelada con hash

- **WHEN** el tribunal intenta acceder a la evidencia
- **THEN** encuentra una URL accesible o un ZIP con su hash SHA-256 declarado en el documento

#### Scenario: Código auditable

- **WHEN** el tribunal quiere verificar la lógica que produce los resultados
- **THEN** encuentra el código de los cuatro nodos de código y el SQL de persistencia y de consultas transcriptos en el Anexo B

### Requirement: El informe no expone identificadores de publicaciones

El informe MUST NOT publicar identificadores de plataforma ni títulos literales de publicaciones de r/devsarg; MUST reemplazarlos por códigos internos con la tabla de correspondencia fuera del documento. Para las divulgaciones técnicas de otras comunidades, MUST citar la fuente original (CVE o aviso del fabricante) en lugar de la publicación de Reddit. El análisis de riesgo residual MUST contemplar el vector del identificador de plataforma y el de las menciones de usuario. El informe MUST NOT calificar la seudonimización como «irreversible».

#### Scenario: Cero identificadores de r/devsarg

- **WHEN** se recorre el informe en busca de identificadores o títulos de r/devsarg
- **THEN** no aparece ninguno; los casos se citan por código interno y descripción genérica

#### Scenario: Riesgo residual completo

- **WHEN** se lee el análisis de riesgo residual
- **THEN** contempla que el identificador de plataforma almacenado permite recuperar al autor sin la clave y que las menciones de usuario se conservan en claro

#### Scenario: Sin la calificación «irreversible»

- **WHEN** se busca la palabra «irreversible» en el informe
- **THEN** no aparece; la seudonimización se describe como HMAC-SHA-256 con clave de despliegue, reversible por comparación para el custodio de la clave

### Requirement: La consistencia interna es verificable

El informe MUST corregir las contradicciones internas entre secciones, figuras y anexos detectadas por el tribunal (falsos positivos de r/devsarg, estado del workflow, días de operación, fecha de corte, corrección del motor, diferencia 167/170, tabla de clasificación, tamaño de muestra, throughput, códigos internos, fechas, criterios a priori y semilla), y MUST presentar los estados de los criterios de forma uniforme entre Resumen, Abstract, cuerpo y tablas.

#### Scenario: Estado del workflow unificado

- **WHEN** se compara la Figura 1, la Figura 3 y el texto sobre el estado del workflow
- **THEN** los tres informan el mismo estado, coherente con el artefacto exportado

#### Scenario: Un solo recuento de criterios

- **WHEN** se cuentan los criterios alcanzados en el Resumen y en las tablas del Capítulo 5 y del Capítulo 7
- **THEN** el recuento es el mismo en todos los lugares y no incluye la tasa de falsos descubrimientos como criterio separado
