# muestra-control-etiquetada

## ADDED Requirements

### Requirement: El criterio de etiquetado se acuerda antes de etiquetar

El proyecto MUST acordar con los autores y sus directores el criterio que define qué es un post de amenaza y qué es un post sin señal, antes de etiquetar la muestra. Ese criterio MUST quedar escrito y MUST considerar la variable dependiente del estudio, porque las métricas sobre ella no son defendibles sin un acuerdo explícito.

El etiquetado MUST cubrir las nueve categorías del diccionario más la categoría sin señal, de modo que la matriz de confusión tenga una clase por cada valor que el clasificador puede emitir.

#### Scenario: El criterio está escrito antes de la primera etiqueta

- **WHEN** se abre la muestra de control para etiquetar
- **THEN** existe un documento con el criterio acordado, su fecha y los responsables, y ninguna etiqueta se asigna antes de que ese documento exista

#### Scenario: El criterio cubre la categoría sin señal

- **WHEN** se lee el criterio de etiquetado
- **THEN** define explícitamente cuándo un post se etiqueta como sin señal, porque esa clase es la más frecuente del corpus generalista y sin ella la matriz no tiene columna de casos negativos

#### Scenario: Una discrepancia de criterio se resuelve antes de seguir

- **WHEN** dos etiquetadores clasifican el mismo post en categorías distintas
- **THEN** la discrepancia se resuelve por acuerdo y la resolución se registra como regla del criterio, no como excepción de ese post

### Requirement: La muestra tiene tamaño declarado y su límite de confianza es explícito

La muestra de control MUST tener un tamaño declarado, y el tamaño MUST reportarse junto a cada métrica que se calcule sobre ella. El proyecto MUST declarar que un tamaño pequeño con clases desbalanceadas produce métricas de confianza baja, y MUST NOT presentar esas métricas sin ese límite.

El tamaño MUST declararse antes de calcular cualquier métrica, de modo que el número no pueda ajustarse después de conocer el resultado.

#### Scenario: El tamaño se declara antes de medir

- **WHEN** se calcula la primera métrica sobre la muestra
- **THEN** el tamaño de la muestra ya estaba declarado y archivado, y no se modificó después de conocer el resultado

#### Scenario: Cada métrica viaja con su tamaño

- **WHEN** se lee cualquier cifra de desempeño calculada sobre la muestra
- **THEN** aparece acompañada del número de observaciones de la muestra, de la matriz de confusión que la produjo y de su fecha

#### Scenario: La inestabilidad de la muestra se declara

- **WHEN** el tamaño de la muestra y el desbalance de clases hacen que el acuerdo entre anotadores sea inestable
- **THEN** el proyecto declara esa inestabilidad y agranda la muestra en lugar de reportar la métrica como si fuera precisa

### Requirement: La muestra es independiente del corpus de resultados

La muestra de control MUST NOT ser el mismo conjunto de posts sobre el que se reportan resultados de la ventana, porque usar el conjunto de prueba como conjunto de evaluación produce sobreajuste y una cifra que mide el ajuste del diccionario a esos mismos posts.

El proyecto MUST muestrear la muestra antes de conocer el resultado de la clasificación sobre ella.

#### Scenario: La muestra y el corpus de resultados son conjuntos distintos

- **WHEN** se compara el conjunto de la muestra de control con el corpus de la ventana de resultados
- **THEN** no comparten posts, y esa no superposición está verificada y documentada

#### Scenario: La muestra se sortea antes de clasificar

- **WHEN** se extrae la muestra de control
- **THEN** la extracción ocurre antes de ejecutar el clasificador sobre esos posts, de modo que la muestra no queda sesgada por el resultado

#### Scenario: La muestra no se reetiqueta para coincidir con el modelo

- **WHEN** el modelo falla en un post de la muestra
- **THEN** la etiqueta se conserva y el error se reporta como falso negativo, sin reetiquetar el post ni excluirlo de la muestra

### Requirement: Las etiquetas se persisten de forma versionable y auditable

Las etiquetas MUST persistirse en un archivo versionable bajo `V4/evidencias/`, MUST identificar quién etiquetó cada post y cuándo, y MUST permitir reconstruir la matriz de confusión sin volver a consultar a los autores.

La persistencia MUST NOT modificar `tesi_osint`. Las etiquetas son evidencia externa al pipeline, no una columna nueva.

#### Scenario: Cada etiqueta tiene autor y fecha

- **WHEN** se lee una etiqueta de la muestra
- **THEN** indica quién la asignó y en qué fecha, de modo que el criterio aplicado por cada persona es auditable

#### Scenario: La matriz se reconstruye desde el archivo

- **WHEN** se necesita recalcular la matriz de confusión
- **THEN** se reconstruye desde el archivo de etiquetas versionado, sin requerir intervención de los autores

#### Scenario: El pipeline no depende de la muestra

- **WHEN** se revisa el esquema de la base
- **THEN** no existe ninguna tabla de etiquetas, y el clasificador del pipeline funciona sin conocer la existencia de la muestra

#### Scenario: El acuerdo entre anotadores es verificable

- **WHEN** se calculan las métricas de desempeño
- **THEN** el proyecto reporta el acuerdo entre anotadores, porque un Cohen's Kappa calculado sobre un solo anotador no es un acuerdo y no puede presentarse como tal

### Requirement: Las métricas de desempeño se calculan solo con muestra y se reportan con su evidencia

El proyecto MUST calcular precisión, recall, F1, matriz de confusión y Kappa únicamente sobre la muestra de control etiquetada. Toda métrica MUST acompañarse de su matriz de confusión, su consulta o su procedimiento, su fecha y su `n`, y MUST NOT derivarse de conteos sobre datos no etiquetados.

Mientras la muestra no esté etiquetada, los cinco criterios de aceptación del estudio MUST permanecer en estado retirado y el proyecto MUST NOT declarar desempeño del clasificador.

#### Scenario: Sin muestra etiquetada no hay desempeño declarado

- **WHEN** se busca una afirmación de desempeño del clasificador en los artefactos del proyecto
- **THEN** existe únicamente si la muestra de control está etiquetada y las métricas fueron calculadas sobre ella; mientras no lo esté, los criterios de aceptación figuran como retirados

#### Scenario: Cada métrica tiene su evidencia delante

- **WHEN** se lee una cifra de desempeño
- **THEN** la matriz de confusión que la produce, su fecha y su `n` aparecen junto a ella, nunca la cifra sola

#### Scenario: Los conteos no se presentan como métricas

- **WHEN** se reporta el número de posts clasificados en una categoría sobre datos no etiquetados
- **THEN** se lo llama conteo, se declara que no equivale a precisión ni a recall, y no se lo usa para afirmar calidad de la detección

#### Scenario: La derivación desde datos previos está prohibida

- **WHEN** se busca el origen de cualquier cifra de desempeño
- **THEN** el origen es la muestra de control etiquetada o una consulta de solo lectura sobre `tesi_osint` fechada; nunca una cifra de V2, V3 ni una tasa supuesta

### Requirement: El resultado de la evaluación alimenta cambios, no ajustes silenciosos

Todo hallazgo de la evaluación MUST traducirse en una tarea trazable: retirar un término, ajustar el umbral, ampliar el diccionario o documentar una limitación. El proyecto MUST NOT aplicar un cambio al diccionario como consecuencia de la evaluación sin registrarlo, y MUST NOT reetiquetar la muestra después de conocer el resultado.

#### Scenario: Un falso positivo lleva a una tarea trazable

- **WHEN** la evaluación identifica un falso positivo por un término concreto
- **THEN** ese término queda registrado para revisión en un change, y el post conserva su etiqueta original

#### Scenario: El ajuste del umbral se registra con su resultado

- **WHEN** la evaluación justifica un cambio del número mínimo de coincidencias
- **THEN** el cambio queda registrado con el resultado sobre la muestra que lo justifica, y no se aplica en silencio

#### Scenario: Una limitación que no se corrige se declara

- **WHEN** un hallazgo no se corrige en el change actual
- **THEN** se declara como limitación conocida en lugar de omitirse, porque un hallazgo omitido se convierte en un criterio de aceptación no evaluado
