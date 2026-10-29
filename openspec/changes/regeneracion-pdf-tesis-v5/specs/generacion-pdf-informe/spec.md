# Spec Delta

## Purpose

Define cómo se produce el PDF del informe a partir de una fuente Markdown versionada, con paridad
de estilo respecto de la versión anterior y compuertas de aceptación que impiden publicar un
artefacto con índices incompletos, páginas vacías o contenido alterado.

## ADDED Requirements

### Requirement: Fuente única versionada

El PDF SHALL generarse desde un archivo Markdown versionado en el repositorio. El build SHALL
fallar si la fuente no existe o si no está registrada en Git.

#### Scenario: Fuente disponible y versionada
- **WHEN** se ejecuta el build con la ruta de la fuente Markdown
- **THEN** el proceso lee esa fuente y produce el PDF sin depender de documentos intermedios editados a mano

#### Scenario: Fuente ausente
- **WHEN** la ruta de la fuente no existe o el archivo no está versionado
- **THEN** el build termina con error y no genera un PDF

### Requirement: Índices con número de página

Toda entrada del índice general, del índice de tablas y del índice de figuras SHALL mostrar el
número de página real donde aparece el destino. Ninguna entrada MAY quedar sin número ni conservar
marcadores de posición.

#### Scenario: Índices completos
- **WHEN** el documento se compone y se exporta
- **THEN** cada una de las tres listas de índice muestra un número de página para todas sus entradas

#### Scenario: Entrada sin resolver
- **WHEN** una entrada de índice queda sin número o conserva un marcador de posición
- **THEN** la verificación falla y el artefacto no se publica

### Requirement: Paridad tipográfica con la versión anterior

El PDF SHALL usar papel A4, cuerpo en Times New Roman 12 y márgenes de 25 mm superior e inferior,
30 mm izquierdo y 20 mm derecho, con la misma estructura de portada, resumen, abstract, capítulos,
referencias y anexos que el informe de la versión anterior.

#### Scenario: Comparación de formato
- **WHEN** se inspecciona el PDF generado
- **THEN** el tamaño de página, la fuente del cuerpo y los márgenes coinciden con los de la versión anterior

#### Scenario: Estructura del documento
- **WHEN** se recorre el PDF generado
- **THEN** aparecen, en orden, portada, índices, resumen, abstract, capítulos 1 a 8, referencias y anexos

### Requirement: Sin páginas vacías ni portada desbordada

El PDF SHALL NOT contener páginas sin texto y la portada SHALL ocupar una sola página.

#### Scenario: Página sin contenido
- **WHEN** la verificación recorre el PDF y encuentra una página sin caracteres
- **THEN** el build falla e informa el número de página

#### Scenario: Portada en una página
- **WHEN** se revisa la primera página del PDF
- **THEN** la portada y su nota de versión caben completas en esa página

### Requirement: Build reproducible en un solo paso

Un único comando SHALL producir el PDF final a partir de la fuente, sin parches manuales posteriores
ni edición del documento en un procesador de texto.

#### Scenario: Ejecución limpia
- **WHEN** se ejecuta el comando sobre un árbol de trabajo limpio
- **THEN** se obtiene el PDF final y el informe de verificación sin intervención manual

#### Scenario: Dependencia faltante
- **WHEN** falta una herramienta requerida (Pandoc o el procesador de texto)
- **THEN** el build falla con un mensaje que indica cuál falta y cómo instalarla

### Requirement: Contenido congelado

La regeneración SHALL NOT alterar cifras, tablas ni prosa del contenido aprobado. Cualquier cambio
de contenido SHALL tramitarse como un cambio separado y explícito.

#### Scenario: Texto sin cambios
- **WHEN** se compara el texto del PDF generado con el del PDF aprobado
- **THEN** las diferencias se limitan a artefactos de extracción y no a cifras ni párrafos

#### Scenario: Cambio de contenido detectado
- **WHEN** la comparación encuentra una cifra o un párrafo distinto
- **THEN** el cambio se reporta y no se da por válido el build

### Requirement: Registro de verificación

Cada build SHALL dejar un registro con la fecha, la fuente utilizada, el hash del PDF, la cantidad
de páginas y el resultado de cada compuerta de aceptación.

#### Scenario: Registro completo
- **WHEN** el build termina correctamente
- **THEN** existe un archivo de verificación con fecha, fuente, hash, páginas y resultados

#### Scenario: Compuerta fallida
- **WHEN** una compuerta no se cumple
- **THEN** el registro indica cuál falló y el build no se considera exitoso
