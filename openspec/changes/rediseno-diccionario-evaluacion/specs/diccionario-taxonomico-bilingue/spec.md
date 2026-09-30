# diccionario-taxonomico-bilingue

## ADDED Requirements

### Requirement: La taxonomía usa un único eje de tipo de amenaza

El diccionario taxonómico MUST definir sus categorías sobre un único eje semántico: el **tipo de amenaza**. Toda categoría MUST nombrar un tipo de amenaza y MUST NOT nombrar un origen geográfico, una nacionalidad, un sector económico ni un contexto cultural como criterio de pertenencia.

El conjunto MUST ser de nueve categorías: `Phishing`, `Robo de Credenciales`, `Malware`, `Ransomware`, `Vulnerabilidades`, `Filtración de Datos`, `Infraestructura y Ataques`, `Hacktivismo` e `Ingenieria Social`.

El contexto geográfico MUST NOT implementarse como categoría. El proyecto MUST capturarlo por las entidades ya extraídas en `posts.entities`, que registran productos y servicios de la jurisdicción.

#### Scenario: Ninguna categoría nombra un contexto geográfico

- **WHEN** se lee la lista completa de categorías del diccionario
- **THEN** las nueve categorías nombran tipos de amenaza y ninguna nombra un país, una región o una población; el contexto argentino no figura como categoría

#### Scenario: El contexto argentino sigue capturándose

- **WHEN** un post menciona un producto o servicio de la jurisdicción, como `mercado pago`, `dni` o `cvu`
- **THEN** ese término se registra en `posts.entities` por la extracción de entidades existente, sin requerir una categoría del diccionario

#### Scenario: Dos posts de la misma amenaza y contextos distintos reciben la misma categoría

- **WHEN** un post describe ransomware publicado en Argentina y otro describe ransomware publicado en España
- **THEN** ambos reciben `Ransomware`, porque la taxonomía clasifica por tipo de amenaza y no por procedencia

#### Scenario: La taxonomía es reconciliable con un estándar externo

- **WHEN** un evaluador externo busca la equivalencia entre las nueve categorías y MITRE ATT&CK
- **THEN** cada categoría tiene un nombre en inglés que corresponde a una técnica o a una clase de técnica de ATT&CK, sin necesidad de una tabla de equivalencia en el modelo de datos

### Requirement: La taxonomía no requiere migración de esquema

El proyecto MUST admitir las nueve categorías sin modificar el DDL, dado que `posts.nlp_category` es un `VARCHAR(100)` sin `CHECK`, sin `ENUM` y sin tipo dominio, y que `nlp_score` tiene un `CHECK (nlp_score BETWEEN 0 AND 1)` que toda fórmula válida debe respetar.

#### Scenario: Ninguna tarea de esta change altera el esquema

- **WHEN** se revisan las tareas de esta change
- **THEN** ninguna modifica `A_DDL.sql`, ninguna añade columnas, índices ni constraints, y ninguna ejecuta `ALTER` sobre `tesi_osint`

#### Scenario: El nombre más largo de la taxonomía cabe en la columna

- **WHEN** se evalúa la longitud del valor persistido
- **THEN** el nombre de categoría más largo cabe en el `VARCHAR` declarado, sin truncar el valor

#### Scenario: El score persistido respeta el constraint

- **WHEN** se verifica un valor de `nlp_score` producido por el clasificador vigente
- **THEN** está dentro de `[0, 1]` y por tanto satisface el `CHECK` sin necesidad de ampliarlo

### Requirement: El diccionario es bilingüe y su construcción es reproducible

El diccionario MUST incluir términos en castellano y en inglés, porque el corpus monitorizado puede ser de cualquiera de los dos idiomas y un diccionario de un solo idioma estructuralmente no puede cubrir el otro.

El diccionario MUST construirse desde una definición del alcance de la tesis, MUST NOT ajustarse agregando términos porque hayan producido detecciones en los datos de producción, y su procedimiento de construcción MUST estar documentado en el Code node.

#### Scenario: El procedimiento de construcción está declarado

- **WHEN** se lee el comentario de cabecera de `CLASSIFY_CODE`
- **THEN** declara que el diccionario se construye desde la definición del alcance y que no se ajusta contra los datos de producción

#### Scenario: Ningún término se agrega por su rendimiento observado

- **WHEN** se revisa la historia del diccionario
- **THEN** ningún término fue incorporado porque elevara la tasa de detección sobre posts ya ingeridos, y toda adición posterior exige evidencia de la muestra de control

#### Scenario: Ambos idiomas están representados

- **WHEN** se cuentan los términos del diccionario por idioma
- **THEN** existen términos en castellano y en inglés, y el recuento de cada idioma es verificable

### Requirement: Los términos del diccionario evitan la coincidencia trivial

El diccionario MUST excluir todo término cuya presencia en un texto no aporte evidencia de la categoría a la que pertenece. La exclusión de un término atómico con valor genérico en su idioma MUST declararse por su coincidencia trivial, y MUST NOT compensarse subiendo o bajando el umbral global.

Los términos genéricos MUST NOT reingresar al diccionario bajo otra grafía, plural o conjugación.

#### Scenario: Ningún término genérico permanece en el diccionario

- **WHEN** se busca en el diccionario cada término retirado por coincidencia trivial, y también sus plurales y conjugaciones
- **THEN** ninguno está presente en ninguna forma

#### Scenario: Un post no trivial no se clasifica por un término vacío de significado

- **WHEN** un post que no describe una amenaza menciona palabras como «cuenta», «correo», «enlace» o «banco»
- **THEN** esas palabras por sí solas no producen ninguna clasificación, porque no pertenecen a ninguna categoría

#### Scenario: La cobertura de un término retirado no se recupera por otra vía

- **WHEN** se verifica que un término genérico no reapareció como su propio nombre, ni como plural, ni como forma conjugada
- **THEN** la cobertura perdida por retirarlo se acepta como limitación y no se compensa con sinónimos igualmente genéricos

### Requirement: La ausencia de lematización se compensa y se declara

El clasificador MUST tokenizar el texto en tokens alfanuméricos y MUST hacer coincidencia por token exacto, sin lematización. El diccionario MUST incluir, por esa razón, las formas conjugadas en castellano que de otro modo no se encontrarían, y el proyecto MUST declarar esta limitación como parte del método en lugar de ocultarla.

Los términos del diccionario MUST escribirse sin acentos, sin guiones y sin formas que el tokenizador no pueda producir como token único.

#### Scenario: La limitación está declarada como parte del método

- **WHEN** se lee la documentación del método de clasificación
- **THEN** declara que no hay lematización y que el diccionario compensa la flexión con formas conjugadas, y registra la lematización como deuda técnica

#### Scenario: Las formas conjugadas del castellano están presentes

- **WHEN** se busca en el diccionario las formas conjugadas frecuentes del castellano, como `filtraron`, `filtran`, `hackearon`, `suplantan` y `clonar`
- **THEN** están presentes, porque de lo contrario el término de diccionario nunca las encontraría

#### Scenario: Ningún término contiene un guion

- **WHEN** se revisa el diccionario en busca de guiones
- **THEN** no hay ningún término con guion, y los conceptos que normalmente se escriben con guion están escritos con espacio

#### Scenario: Ningún término contiene un acento

- **WHEN** se revisa el diccionario en busca de caracteres acentuados
- **THEN** no hay ninguno, porque la normalización del texto los elimina antes de la comparación y un término acentuado nunca coincidiría

#### Scenario: Ningún término queda inaplicable por el tokenizador

- **WHEN** se evalúa cada término contra la regla de coincidencia por token exacto
- **THEN** todo término presente puede coincidir con el texto, y los que no podrían se han escrito o retirado

### Requirement: La fórmula de score es una confianza estable e interpretable

`nlp_score` MUST expressar una confianza normalizada en `[0, 1]` que MUST NOT depender del tamaño del diccionario de ninguna categoría. La fórmula MUST ser `min(1, hits / SATURATION)` con `SATURATION` declarado como constante, MUST producir un valor interpretable sin conocer el diccionario, y MUST quedar documentada según RN-CL-02.

#### Scenario: La escala no cambia al ampliar el diccionario

- **WHEN** se amplía el número de términos de una categoría y se reclasifica el mismo post
- **THEN** su `nlp_score` no cambia, porque la fórmula no divide por el tamaño del diccionario

#### Scenario: La confianza es legible sin conocer la implementación

- **WHEN** se lee un `nlp_score` persistido
- **THEN** se puede interpretar a partir del número de coincidencias y de la constante de saturación, sin consultar la tabla de términos

#### Scenario: La saturación está acotada

- **WHEN** el número de coincidencias iguala o supera la constante de saturación
- **THEN** el score es `1.0` y no excede el límite superior del intervalo ni el `CHECK` del DDL

#### Scenario: El valor cero es alcanzable

- **WHEN** un post no alcanza el umbral mínimo de coincidencias
- **THEN** su score es `0.0` y su categoría es la categoría de posts sin señal, nunca una categoría con score cero

### Requirement: El umbral de señal se calibra contra muestra etiquetada, no contra producción

El número mínimo de coincidencias necesario para clasificar un post MUST tratarse como un hiperparámetro calibrado contra la muestra de control etiquetada, y MUST NOT ajustarse para elevar la tasa de detecciones sobre los datos de producción.

La revisión del umbral MUST garantizar que ningún término específico basta por sí solo para producir una clasificación, salvo que la muestra de control lo justifique de forma explícita.

#### Scenario: Ninguna cifra de desempeño se declara sin muestra

- **WHEN** se busca cualquier cifra de precisión, recall, F1, Kappa o matriz de confusión en los artefactos de esta change
- **THEN** no existe ninguna, porque la muestra de control todavía no está etiquetada

#### Scenario: Los conteos operativos se declaran como conteos

- **WHEN** se reporta el número de clasificaciones positivas o la tasa de señal por comunidad
- **THEN** se presenta como conteo operativo accompanied de su consulta, su fecha y su `n`, y explícitamente como no equivalente a una métrica de desempeño

#### Scenario: El umbral se revisa con evidencia etiquetada

- **WHEN** se modifica el número mínimo de coincidencias
- **THEN** la modificación viene con el resultado sobre la muestra de control etiquetada, nunca con una tasa observada en producción

#### Scenario: La importancia de los términos de muestra no se reordena

- **WHEN** un término de muestra resulta estar en un lugar distinto al esperado
- **THEN** se registra como discrepancia, con la debida justificación metodológica, sin reescribir a posteriori los resultados ya obtenidos sobre esa misma muestra
