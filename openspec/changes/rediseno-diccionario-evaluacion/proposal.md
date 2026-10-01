## Why

El clasificador por diccionario está alineado con un alcance que la tesis no tiene. `DICT` en `V4/scripts/generar_workflow.py:91-97` define cinco categorías de **fraude al consumidor en español** —estafa, Mercado Pago, DNI, clonación de tarjeta— y ninguna de seguridad técnica. Su cobertura léxica es de 51 términos, de los cuales 8 están en inglés (`phishing`, `leak`, `cve`, `exploit`, `pwn`, `ransomware`, `wannacry`, `smishing`).

Dos consecuencias medidas sobre los 301 posts ingeridos en la corrida del 2026-09-30, con el diccionario vigente:

- El sistema produjo **3 clasificaciones positivas en total** (todas `Phishing`, todas en `r/DerechoGenial`).
- Al inspeccionar esas 3 una por una, **1 es un falso positivo**: *"Multinacional retiene mi sueldo y quiere que renuncie"* fue clasificado `Phishing` por los términos genéricos `whatsapp` y `cuenta`, que no tienen relación con phishing. Las otras 2 son detecciones correctas sostenidas por un segundo término también genérico (`cuenta`, `correo`).

Sobre el mismo corpus, sustituyendo el diccionario por uno bilingüe de nueve categorías, la tasa de posts con señal baja a **0 de 301**. La causa no es el diccionario: es que el corpus monitorizado no contiene tráfico de amenazas. Medido sobre 100 posts por comunidad con el diccionario nuevo: `r/malware` 19%, `r/netsec` 6%, `r/cybersecurity` 3%, `r/reverseengineering` 3%, `r/devsarg` 0%.

Estos conteos son **operativos, no métricas de desempeño**: no hay muestra de control etiquetada, así que no son precisión, recall ni F1. RN-GL-01 impide declararlos como tales. Lo que síConsta es que el sistema no puede medirse, y eso arrastra la consecuencia más grave del proyecto: cinco criterios de aceptación están **RETIRADOS** en `Facultad-2026/Proyecto-Final/Versiones-Tesis/tesis_v4.md:441-444` y `:2315` por falta de muestra etiquetada.

Además, RN-GL-03 exige documentar los cambios de diseño **antes** de modificar la implementación. Ampliar el diccionario de cinco a nueve categorías rompe el criterio de aceptación de US-005 (`knowledge-base/06_funcionalidades.md:65`, "un diccionario taxonómico de cinco categorías") y obliga a recalcular la matriz de confusión que C-10 debe construir contra estas categorías (`CHANGES.md:398`).

## What Changes

- **Redefinir `DICT`**: de 5 a **9 categorías**, sobre un único eje —*tipo de amenaza*— y en dos idiomas (castellano e inglés). Se elimina "Estafas Virtuales" como categoría propia: sus términos se redistribuyen en `Phishing`, `Robo de Credenciales` e `Ingeniería Social`. El contexto geográfico argentino deja de ser una categoría y pasa a capturarse por las entidades ya extraídas (`PRODUCTS`).
- **Retirar los términos léxicos genéricos** (`mp`, `cuenta`, `enlace`, `correo`, `bug`, `falla`, `transferencia`, `banco`, `filtrar`, `cangrejo`, `pescar`, `actualizacion`) que producen falsos positivos por coincidencia trivial.
- **Agregar formas conjugadas en castellano** (`filtraron`, `hackearon`, `clonar`, `suplantan`, `filtran`). El clasificador hace match por token exacto sobre `text.split(/[^a-z0-9]+/)` y no aplica lematización, por lo que la forma de diccionario nunca encuentra la forma flexionada. La limitación se documenta como parte del método, no se oculta.
- **Cambiar la fórmula de `nlp_score`** de `hits / |keywords(categoría)|` a `min(1, hits / SATURATION)` con `SATURATION = 4`. La fórmula anterior se normaliza contra el tamaño del diccionario, de modo que ampliar el diccionario degrada la escala sin que cambie el resultado de la clasificación: un post con 2 aciertos pasa de `0.22` a `0.07` por el solo hecho de agregar términos. La fórmula nueva es estable ante cambios del diccionario y es la que RN-CL-02 obliga a documentar.
- **Mantener `MIN_HITS = 2`** y tratar el umbral como hiperparámetro a calibrar contra la muestra de control, no contra los datos de producción.
- **Sincronizar `generar_workflow.py` con el workflow en ejecución**: incorporar los nodos `Loop Over Items` y `Espera Rate Limit` y su cableado, y corregir el `subreddit_id` de `r/derechogenial` a `r/DerechoGenial`. Sin esto, regenerar el artefacto revierte el rate limiting espaciado y reintroduce la violación de clave foránea.
- **Constituir la muestra de control etiquetada** —50 posts etiquetados a mano por los autores— como condición previa y suficiente para calcular precisión, recall, F1 y matriz de confusión, y para rehabilitar los cinco criterios de aceptación retirados.
- **Registrar la evidencia de selección de corpus**: la medición de señal por comunidad pasa a ser un artefacto consultable, y la decisión de qué comunidades integrar pasa a justificarse con datos y no con intuición.
- **Fijar el corpus de la ventana como mixto**: `r/netsec`, `r/Malware` y `r/devsarg`, con criterio de inclusión temático declarado de antemano. `r/argentina` y `r/DerechoGenial` se desactivan con `active_monitoring = false` y conservan sus 201 posts. La discontinuidad de cobertura se registra como dos segmentos de corpus.
- **Declarar que la tasa de señal del corpus fijado no estima desempeño**, porque la composición se apoyó en esa misma tasa. La estimación válida de desempeño viene solo de la muestra de control.
- **Documentar la caracterización del rate limiting** con lo medido: 30 s entre llamadas es suficiente, 3 s no lo es, y el reintento acelerado es contraproducente.
- **Ninguna métrica de desempeño se declara en este change** (RN-GL-01). Los conteos citados en `Why` son operativos, se acompañan de su consulta y de su `n`, y no habilitan ninguna afirmación sobre calidad de la detección.

## Capabilities

### New Capabilities

- `diccionario-taxonomico-bilingue`: diccionario taxonómico de nueve categorías sobre un eje único de tipo de amenaza, en castellano e inglés, con la limitación de no lematización declarada y la fórmula de score documentada y estable.
- `muestra-control-etiquetada`: conjunto de 50 posts etiquetados a mano por los autores, con su protocolo de etiquetado, el cálculo de métricas de desempeño sobre él y la rehabilitación de los criterios de aceptación retirados.
- `seleccion-corpus-evaluada`: evidencia consultable de señal por comunidad y criterio trazable de inclusión de comunidades en el corpus, con la mitigación del rate limiting por espaciado temporal.

### Modified Capabilities

Ninguna. `openspec/specs/` está vacío: no existen specs previos cuyos requisitos cambien. El criterio de US-005 que este change rompe está en `knowledge-base/06_funcionalidades.md`, que es KB y no spec, y se actualiza como tarea documental.

## Impact

- **Código**: `V4/scripts/generar_workflow.py` — `PREPARE_SUBS` (línea 33), `CLASSIFY_CODE` (líneas 89-128), `PRODUCTS` sin cambios, definición de nodos y conexiones.
- **Artefacto generado**: `V4/anexos/B_workflow.json` pasa de 14 a **16 nodos**. Se regenera; nunca se edita a mano.
- **Sin impacto en el DDL**: `A_DDL.sql` no cambia. `posts.nlp_category` es `VARCHAR(100)` sin `CHECK`, `ENUM` ni tipo dominio, y `nlp_score` tiene `CHECK (nlp_score BETWEEN 0 AND 1)` que la fórmula saturante respeta. Ninguna tabla, columna ni índice se altera.
- **Documentación a actualizar**: `knowledge-base/06_funcionalidades.md` (US-005, "cinco categorías" → nueve), `knowledge-base/05_reglas_de_negocio.md` (RN-CL-04, referencia al Anexo C), `Facultad-2026/Proyecto-Final/Versiones-Tesis/tesis_v4.md` (Tabla 6 en `:1450-1458` y `:2889-2895`, Anexo C en `:2876-2938`, fórmula del score en OE4 `:2492`), `CHANGES.md`.
- **Reconciliación de datos**: la tabla `subreddits` conserva la fila huérfana `derechogenial` (minúscula) de las corridas previas, con 0 posts. **No se borra en este change**: la regla dura prohíbe eliminar un subreddit con datos y la limpieza requiere su propio change. Se documenta como inconsistencia conocida. Las filas `argentina` y `DerechoGenial` se desactivan, no se borran.
- **Identificadores con mayúscula inicial**: `r/Malware` y `r/DerechoGenial` aparecen con mayúscula en sus permalinks, verificado contra feed real el 2026-09-30. `subreddit_id` se deriva del enlace y se compara exacto contra la PK, así que `PREPARE_SUBS` debe declarar `Malware` y no `malware`. Es el mismo modo de falla que el ya corregido en `DerechoGenial`.
- **Dependencias**: requiere C-05 (`ventana-recoleccion-b5`) para el criterio de fecha de la ventana. **Bloquea a C-10** (matriz de confusión) y a C-13 (`anexo-c-diccionario-taxonomico-e11`), que deben construirse contra estas categorías y contra este diccionario.
- **Riesgo asumido**: la ventana de recolección se reanuda después de la ventana abierta en C-05, cuya fecha de inicio (2026-09-25) y corte abierto se conservan; este change no modifica la definición de la ventana ni reinicia la recolección.
