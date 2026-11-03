**UNIVERSIDAD TECNOLÓGICA NACIONAL — FACULTAD REGIONAL MENDOZA**

Tecnicatura Universitaria en Programación — Tribunal Evaluador de Trabajos Finales

**DEVOLUCIÓN DE AUDITORÍA ACADÉMICA**

*Tercera instancia de revisión (V3)*

| Título del TFI | Sistema automatizado de monitoreo de foros y redes sociales para la detección de tendencias y alertas en ciberseguridad en Argentina mediante OSINT y n8n |
| :---- | :---- |
| **Autores** | Valentino Lorca — Jerónimo Zúñiga — Enzo Severino |
| **Directores** | Prof. Alberto Cortez — Prof. Ariel Enferrel |
| **Archivo auditado** | tesis\_v3.pdf (24 páginas) |
| **Instancia** | V3 — revisión sobre versión corregida, con cotejo contra la devolución V2 del 17/09/2026 |
| **Fecha de devolución** | 22 de septiembre de 2026 |
| **Calificación V2 (referencia)** | 6,0 / 10 |
| **Calificación de esta instancia** | **5,5 / 10 — NO APROBADO EN ESTA INSTANCIA. REENTREGA OBLIGATORIA (V4)** |
| **Habilitación a defensa** | No habilitada. Condicionada al cierre de los 8 ítems bloqueantes del plan de la Sección 9 |

# **1\. Alcance y método de la auditoría**

La presente devolución audita la versión 3 del documento con dos propósitos. Primero, verificar uno por uno el estado de los 17 hallazgos (H-01 a H-17) y de las 12 observaciones menores (M-01 a M-12) formulados en la devolución V2. Segundo, auditar la V3 como pieza autónoma, aplicando las mismas cinco dimensiones de la instancia anterior: consistencia numérica interna, trazabilidad entre objetivos y evidencia, solidez metodológica de las métricas, correspondencia entre cuerpo y anexos, y cumplimiento formal (APA 7.ª edición y estructura de TFI).

El estado de cada hallazgo de V2 se clasifica como: **RESUELTO**; **RESUELTO CON OBSERVACIONES** (la objeción de fondo está cerrada y persisten ajustes no bloqueantes); **PARCIAL** (se atendió solo una parte de la corrección exigida); **NO RESUELTO**. Los hallazgos surgidos en esta instancia se numeran N-01 a N-06 (críticos y mayores) y m-13 a m-20 (menores), manteniendo los niveles CRÍTICO, MAYOR y MENOR definidos en V2.

Se mantiene la restricción de la instancia anterior: la auditoría se realiza exclusivamente sobre el documento entregado, sin acceso a repositorio, base de datos ni entorno de ejecución. En esta instancia se inspeccionó además la estructura del archivo PDF: no contiene ninguna imagen embebida, y las cuatro figuras del cuerpo aparecen únicamente como marcadores de texto entre corchetes.

# **2\. Avances reconocidos respecto de la V2**

La V3 atiende varias objeciones de fondo y corresponde reconocerlo expresamente:

* Se eliminó la contradicción entre el cuerpo y el Anexo B respecto de la seudonimización: la clave ya no está escrita en el código sino que se lee de una variable de entorno, y el texto abandona la expresión "anonimización irreversible". Era el hallazgo de mayor peso legal y la corrección va en la dirección correcta.

* OE6 fue reclasificado como parcialmente cumplido y se retiró la latencia de alerta de 3,8 minutos que no tenía respaldo. Es una corrección honesta y se valora.

* La precisión (82 %) y la tasa de falsos positivos (18 %) son ahora aritméticamente coherentes, y el F1 declarado (0,815) se verifica.

* El throughput de 1.450 posts/hora quedó separado en una tabla de banco de pruebas, con nota explícita sobre el techo real de ingesta (\~400 posts/hora) y su vínculo con la respuesta a PI-3.

* Se incorporó la Sección 4.5 con un algoritmo explícito de detección de anomalías (ventana móvil, línea de base y umbral).

* La Tabla 3 incorpora una categoría residual y sus porcentajes ya no son números redondos.

* Se declaró el sesgo de evaluación endógena como limitación (6.3) y se adoptó el Kappa de Fleiss.

* Se retiró el 30 % contrafáctico, se citaron CABASE (2025) y Fortinet (2025), se corrigió la autoría del Decreto 1558/2001, el gentilicio "mendocino", la numeración de Referencias y Anexos, y se agregó la declaración de autoría y la política de enmascaramiento de entidades en los casos de 5.3.

Sin embargo, una parte importante de estas correcciones se resolvió declarando en una línea lo que la V2 pidió documentar o evidenciar, y en el proceso el documento perdió contenido que en V2 había sido valorado positivamente (ver N-03). El balance de la instancia se explica en la Sección 8\.

# **3\. Estado de los hallazgos de la V2**

## **3.1. Tablero de seguimiento**

| ID | Hallazgo V2 | Estado V3 | Síntesis |
| :---- | :---- | ----- | :---- |
| H-01 | Salt fijo vs. "dinámico" (seudonimización) | **RESUELTO CON OBSERVACIONES** | Contradicción cerrada; terminología y entorno pendientes |
| H-02 | OE6 declarado cumplido sin alertas | **RESUELTO CON OBSERVACIONES** | Reclasificado; falta definir qué es "demostrativo" |
| H-03 | OE5 sin método | **PARCIAL** | Método de dos líneas; sin resultados del motor |
| H-04 | Precisión vs. falsos positivos | **PARCIAL** | Aritmética corregida; sin fórmula ni matriz |
| H-05 | Cobertura sin protocolo | **NO RESUELTO** | Solo se nombra "captura-recaptura" |
| H-06 | Throughput incompatible con la configuración | **RESUELTO CON OBSERVACIONES** | Separado; criterio y medición no coinciden |
| H-07 | Reproducibilidad y Tabla 3 | **NO RESUELTO** | Anexos C y D anunciados pero inexistentes |
| H-08 | Cifras sin fuente en Cap. 6 | **PARCIAL** | Fuentes citadas; referencias incompletas |
| H-09 | Afirmación del 30 % | **RESUELTO** | Retirada |
| H-10 | Referencias no citadas | **PARCIAL** | Siguen 8 huérfanas; sin contraste con Rivas y Dengra |
| H-11 | Ausencia de figuras | **NO RESUELTO** | Solo marcadores de texto |
| H-12 | Métricas sin dispersión | **PARCIAL** | DS y P95 de latencia; sin n |
| H-13 | Validación endógena | **RESUELTO CON OBSERVACIONES** | Declarado; falta regla de desempate |
| H-14 | Índice desactualizado | **PARCIAL** | Estructura alineada; paginación ficticia |
| H-15 | Defectos del Anexo B | **NO RESUELTO** | Anexo reducido a un nodo; sigue "conceptual" |
| H-16 | Sección 4.2 vs. DDL; 3FN | **PARCIAL** | Denormalización declarada; pg\_trgm sin uso |
| H-17 | Casos de 5.3 y "confianza" | **PARCIAL** | Enmascaramiento sí; fórmula del score no |

**Síntesis:** 1 resuelto, 4 resueltos con observaciones, 8 parciales y 4 no resueltos. De los siete hallazgos críticos de V2, tres quedan cerrados (H-01, H-02, H-06), dos parciales (H-03, H-04) y dos abiertos (H-05, H-07). Los dos abiertos son precisamente los que exigían aportar evidencia y no solo corregir redacción.

## **3.2. Detalle por hallazgo**

**H-01 — Seudonimización de autores  \[RESUELTO CON OBSERVACIONES\]**

**Corregido:** el Anexo B lee la clave desde \$env.SALT\_SECRET y la Sección 3.4 adopta el término "seudonimización".

**Persiste:** (a) la Sección 3.4 sigue describiendo "SHA-256 con salt" cuando el código implementa HMAC-SHA-256 con clave secreta; la observación terminológica de V2 no se atendió. (b) La clave no es "dinámica": es un secreto fijo por despliegue, y debe serlo, porque si variara el mismo autor produciría hashes distintos y se perdería la vinculación longitudinal que el análisis requiere. (c) El fragmento invoca crypto.createHmac sin importar el módulo; en Node.js el objeto global crypto corresponde a la Web Crypto API, que no expone createHmac, de modo que su funcionamiento depende de la configuración del entorno n8n (habilitación del módulo nativo mediante NODE\_FUNCTION\_ALLOW\_BUILTIN). El acceso a \$env también puede estar bloqueado por configuración (N8N\_BLOCK\_ENV\_ACCESS\_IN\_NODE). (d) No se documenta la gestión de la clave (generación, custodia, rotación) ni el riesgo residual: mientras la clave exista, el dato seudonimizado sigue siendo dato personal en los términos de la Ley 25.326.

**Exigido para V4:** reemplazar la expresión por "HMAC-SHA-256 con clave secreta por despliegue"; documentar la configuración del entorno que habilita crypto y \$env (o transcribir el código efectivamente ejecutado); agregar un párrafo de gestión de clave y riesgo residual.

**H-02 — Objetivo OE6 (alertas)  \[RESUELTO CON OBSERVACIONES\]**

**Corregido:** OE6 figura como "PARCIALMENTE CUMPLIDO / DEMOSTRATIVO" y se eliminó la latencia de alerta de 5.3.

**Persiste:** el documento no dice qué parte existe. ¿Hay un nodo de Telegram que envía mensajes? ¿Se ejecutó alguna vez, con qué disparador y con qué contenido? El Anexo B no contiene ningún nodo de este subflujo. Además, el título del TFI, el objetivo general ("generar alertas tempranas") y el propio OE6 ("en tiempo real vía webhook y Telegram") conservan la promesa completa, el Resumen no menciona la reclasificación y el Abstract afirma que se superaron todos los umbrales.

**Exigido para V4:** describir en el Capítulo 4 el alcance exacto de lo implementado, con al menos una captura si existe; si nunca se ejecutó, reclasificar como NO CUMPLIDO. Alinear objetivo general, Resumen y Abstract con el estado real y evaluar el ajuste del título.

**H-03 — Objetivo OE5 (motor de anomalías)  \[PARCIAL\]**

**Corregido:** la Sección 4.5 declara ventana móvil de 7 días, μ y σ por categoría y umbral μ \+ 2σ sobre ventanas de 60 minutos.

**Persiste:** la especificación ocupa dos líneas y no aclara la serie sobre la que se calculan μ y σ (se infiere: conteos horarios por categoría durante las 168 horas previas). El Capítulo 5 no reporta un solo resultado del motor: cuántas anomalías disparó, cuándo, y si los casos de 5.3 fueron detectados por él o identificados después sobre la base. OE5 sigue declarado CUMPLIDO sin evidencia de ejecución. Ver además N-04 sobre la adecuación estadística del umbral.

**Exigido para V4:** formalizar el algoritmo con su fórmula, publicar el registro de disparos del semestre y validarlo contra los tres casos de 5.3.

**H-04 — Precisión y tasa de falsos positivos  \[PARCIAL\]**

**Corregido:** FP \= 18,0 %, complemento exacto de la precisión del 82,0 %.

**Persiste:** la fórmula no se escribe en la Sección 3.3, como se exigió, y no se publica la matriz de confusión 6×6, que es la única pieza que permite al tribunal verificar precisión, recall, F1 y FP en un solo paso. Con la definición adoptada, precisión y FP son la misma medida expresada dos veces (ver N-05). La corrección aritmética introdujo además un error conceptual en la Tabla 3 (ver N-02).

**Exigido para V4:** fórmula explícita en 3.3 y matriz de confusión completa de la muestra de control.

**H-05 — Métrica de cobertura  \[NO RESUELTO\]**

**Evidencia:** la única mención es una frase en 3.3: "Cobertura evaluada por captura-recaptura".

**Problema:** nombrar un método no es describir un procedimiento. No se informa la ventana, los dos canales de captura, los tamaños n₁ y n₂, el solapamiento m, el estimador utilizado (Lincoln-Petersen o Chapman) ni cómo se llega al 84 %. El supuesto de independencia es además decisivo: si el segundo canal usa la misma API y los mismos listings topeados en 1.000 ítems, ambos comparten el mismo punto ciego y el estimador sobrestima la cobertura. El 84 % sigue sin denominador verificable.

**Exigido para V4:** tabla con ventana, n₁, n₂, m, N̂ estimado, cobertura \= n₁ / N̂ e intervalo de confianza, y discusión de la independencia de los canales. En su defecto, retirar la métrica de 1.6, 5.2, Resumen y conclusiones.

**H-06 — Throughput  \[RESUELTO CON OBSERVACIONES\]**

**Corregido:** Tabla 5 separada, con nota explícita sobre el techo de \~400 posts/hora.

**Persiste:** el criterio de 1.6 habla del "throughput máximo del pipeline" y lo medido es, según la propia nota, la capacidad aislada del componente NLP: son objetos distintos, por lo que el rótulo SUPERADO no corresponde al criterio tal como fue enunciado. Además se eliminó la especificación del entorno de pruebas (hardware, versión del motor, protocolo de carga) que V2 había reconocido como avance: la cifra de 1.450 queda sin condiciones de medición.

**Exigido para V4:** hacer coincidir criterio y medición; restituir la especificación del entorno; reportar n y dispersión.

**H-07 — Reproducibilidad y Tabla 3  \[NO RESUELTO\]**

**Evidencia:** el índice anuncia el Anexo C (Diccionario Taxonómico) y el Anexo D (Repositorio del Proyecto) en la página 39; el documento termina en la página 24 con el Anexo B. Ninguno de los dos anexos existe. La Sección 7.3 afirma que el código fuente y los diccionarios están disponibles en los Anexos, afirmación que no se corresponde con el documento entregado. No se informa URL de repositorio.

**Tabla 3:** se incorporó la categoría residual, pero no la consulta SQL exigida. Además, todos los recuentos por categoría cambian respecto de V2 sobre el mismo corpus y la misma ventana (la categoría más frecuente pasa de 3.131 a 2.840) sin ninguna explicación: no se indica si hubo reprocesamiento, cambio de diccionario o de versión del clasificador. Ver N-02.

**Exigido para V4:** incorporar los Anexos C y D con contenido real, la URL del repositorio, la consulta SQL con su salida, y un párrafo que explique las diferencias de recuento entre V2 y V3.

**H-08 — Fuentes de las cifras del Capítulo 6  \[PARCIAL\]**

Se citan CABASE (2025) y Fortinet (2025), pero las entradas carecen de URL, fecha de recuperación y título exacto del informe, que APA 7 exige para documentos institucionales. La Sección 6.1 afirma que los resultados son consistentes con Fortinet sin indicar qué dato del informe se contrasta (categoría, porcentaje, página). Completar ambas referencias y precisar el dato comparado.

**H-09 — Afirmación del 30 %  \[RESUELTO\]**

La cifra fue retirada. Observación: con ella se eliminaron también los ejemplos de modismos ("caer", "pescar", "cangrejo") que V2 había considerado suficientes para sostener el argumento en forma cualitativa. Como consecuencia, la brecha declarada en 2.2 —NLP adaptado a modismos argentinos— queda sin ningún sustento en el texto. Restituir los ejemplos.

**H-10 — Referencias bibliográficas  \[PARCIAL\]**

Se corrigió la autoría del Decreto 1558/2001 y ahora se citan Liao et al. (2016) y Rivas y Dengra (2026). Sin embargo, siguen sin cita en el cuerpo ocho referencias: Han, Kamber y Pei (2012); Honnibal et al. (2020), pese a que SpaCy se menciona en 2.1.3 y 4.4; Jurafsky y Martin (2009); n8n.io (2026); Pastor-Galindo et al. (2020); PostgreSQL Global Development Group (2026); Reddit Inc. (2026); y Zong et al. (2020). El conjunto cambió respecto de V2 pero el número es el mismo: las referencias que antes estaban citadas quedaron huérfanas al condensarse el Capítulo 2\. Rivas y Dengra (2026) se menciona en una oración, sin la subsección de contraste exigida, de modo que la brecha sigue sin delimitarse frente al antecedente más directo. Los datos de Zong et al. (2020) no fueron verificados. Ver m-14 sobre el uso de Liao et al.

**H-11 — Figuras  \[NO RESUELTO\]**

Las cuatro figuras solicitadas aparecen como texto entre corchetes —por ejemplo, "\[Figura 2: DER\]"— y el PDF no contiene ninguna imagen. Tampoco se incorporó el índice de tablas y figuras. Un marcador de posición en un documento entregado para evaluación indica que la versión no está terminada; se eleva este ítem a bloqueante para la V4.

**H-12 — Medidas de dispersión  \[PARCIAL\]**

La latencia se informa ahora con DS \= 0,5 y P95 \= 4,9 minutos, pero sin el número de mediciones. El throughput se informa sin n, desvío ni percentiles. La latencia de consulta analítica (inferior a 50 ms en V2) desapareció sin explicación. Ver N-01: la latencia reportada es incompatible con la arquitectura declarada.

**H-13 — Validación endógena del clasificador  \[RESUELTO CON OBSERVACIONES\]**

El sesgo figura como limitación (5) en 6.3 y se adoptó Kappa de Fleiss. Falta la regla de desempate cuando los tres votos difieren entre seis categorías, que V2 pedía explicitar. La submuestra con evaluador externo era opcional; dado que la tasa de FP quedó exactamente en el umbral (N-05), se recomienda realizarla para la V4.

**H-14 — Índice general  \[PARCIAL\]**

La estructura de secciones del índice coincide ahora con la del cuerpo en lo sustancial. Persisten: (a) paginación ficticia: el índice asigna páginas hasta la 39 a un documento de 24 páginas (el Resumen figura en la 3 y está en la 6; el Capítulo 7 figura en la 30 y está en la 18); (b) entradas 5.1.1 a 5.1.3 que no existen como títulos en el cuerpo; (c) Anexos C y D inexistentes; (d) títulos de 5.3 y 6.2 que difieren del cuerpo; (e) la Declaración de autoría no figura. El índice fue escrito manualmente y no regenerado, que es exactamente lo que V2 pidió corregir.

**H-15 — Anexo B  \[NO RESUELTO\]**

El Anexo B pasó de cinco nodos a uno solo, el de seudonimización. Se corrigió el uso de \$input.all(), pero no se exportó el workflow real: el anexo sigue rotulado "Estructura JSON Conceptual" y el fragmento no es un JSON de workflow importable (carece de las claves nodes y connections). Las observaciones de V2 sobre el trigger, el endpoint, restrict\_sr y el User-Agent no se resolvieron: desaparecieron junto con los nodos. En consecuencia, el documento ya no contiene ninguna evidencia del flujo de recolección (OE1, OE2) ni del de alertas (OE6). Ver H-01 (c) sobre el uso de crypto.

**H-16 — Modelo relacional  \[PARCIAL\]**

La denormalización de nlp\_category quedó declarada como deliberada, lo que cierra la objeción sobre 3FN. En cambio, la tabla de atributos de 4.2 fue eliminada en lugar de alinearse con el DDL: la inconsistencia desapareció por supresión, y ahora 4.2 no describe el modelo (el DER es un marcador). La extensión pg\_trgm sigue creándose sin uso en el Anexo A, y la Sección 4.2 la presenta como característica del diseño. Ver N-06.

**H-17 — Casos de 5.3 y puntuación  \[PARCIAL\]**

Se incorporó la política de enmascaramiento en 3.4 y se aplicó en los Casos 2 y 3\. La Sección 4.4 afirma que el score está normalizado al intervalo \[0,1\] pero no dice cómo: sigue faltando la función de puntuación y su normalización, necesaria para interpretar el 0,94 del Caso 3\. Ese score, además, no tiene columna en el DDL (N-06). Ver m-19 sobre el Caso 2\.

# **4\. Nuevos hallazgos críticos**

**N-01 — La latencia extremo a extremo es incompatible con el scheduler de 15 minutos \[CRÍTICO\]**

**Ubicación:** Sección 1.6, Sección 4.3 y Tabla 4\.

**Evidencia:** la Sección 4.3 fija un scheduler cada 15 minutos. La Tabla 4 reporta latencia E2E media de 4,2 minutos, DS \= 0,5 y P95 \= 4,9, y la declara SUPERADA frente al umbral de 5 minutos en percentil 95\.

**Problema:** con recolección por sondeo cada 15 minutos, una publicación espera en Reddit hasta la próxima ejecución del workflow. Si las publicaciones llegan en momentos aleatorios, esa espera se distribuye aproximadamente uniforme entre 0 y 15 minutos: media ≈ 7,5 minutos, desvío ≈ 4,3 minutos y P95 ≈ 14,3 minutos, antes de sumar cualquier tiempo de procesamiento. Una latencia extremo a extremo con media de 4,2, desvío de 0,5 y P95 de 4,9 minutos es estructuralmente imposible si se mide desde la publicación. La cifra solo es compatible con un intervalo que comienza en la ejecución del workflow —ingesta a clasificación—, que no es extremo a extremo. Cabe señalar que la base almacena created\_utc e ingested\_at, de modo que la latencia real de ingesta es calculable con una consulta.

**Corrección exigida:** definir formalmente el intervalo medido (evento inicial y final); calcular la latencia publicación → ingesta desde la base (ingested\_at − created\_utc) y reportar n, media, P50 y P95. Si no cumple el umbral, declarar el criterio NO CUMPLIDO o justificar un rediseño (scheduler de 5 minutos o menos, verificando la cuota de la API), y vincularlo con PI-3.

**N-02 — La fila "No Relevante / FP" de la Tabla 3 es conceptualmente incorrecta y aparece derivada de la tasa de FP \[CRÍTICO\]**

**Ubicación:** Tabla 3 (Sección 5.1) y Sección 6.1.

**Evidencia:** la fila registra 1.483 posts, 18,0 % del corpus. El 18 % de 8.240 es 1.483,2. La tasa de FP del 18 % se midió en la muestra de control, no en el corpus.

**Problema conceptual:** un falso positivo es, por definición, un ítem que el sistema clasificó como amenaza y no lo es. El sistema no puede asignar sus propios falsos positivos a una categoría "FP": si los hubiese reconocido como no relevantes, serían verdaderos negativos. La fila mezcla una salida del clasificador ("No relevante") con un resultado de la validación humana ("FP").

**Consecuencia:** si 6.757 posts fueron clasificados como amenaza con una precisión del 82 %, alrededor de 1.216 de ellos serían falsos positivos distribuidos dentro de las cinco categorías de amenaza. Por lo tanto, los porcentajes que la Sección 6.1 contrasta con la literatura (Estafas 34,5 %, Phishing 24,0 %) describen salidas del clasificador, no amenazas reales. La coincidencia a la unidad entre la fila y el producto 18 % × 8.240 sugiere que el valor fue calculado desde la tasa y no contado en la base, lo que refuerza el pedido de la consulta SQL (H-07).

**Corrección exigida:** rotular la fila como "No relevante (salida del clasificador)" con el recuento obtenido de la base; presentar por separado una estimación de amenazas reales corregida por la precisión de cada categoría (derivable de la matriz de confusión), y reescribir la comparación de 6.1 sobre esa estimación.

**N-03 — Contracción del documento y pérdida de contenido evaluado en V2 \[CRÍTICO\]**

**Evidencia:** la V3 tiene 24 páginas, mientras su propio índice declara 39\. Gran parte de las secciones se resuelven en una a tres líneas (1.1 a 1.3, 2.1.2 a 2.1.4, 3.1 a 3.4, 4.1 a 4.5, 6.1 a 6.3, 7.3). La Sección 4.1, "Arquitectura del Pipeline de Datos", es una oración más un marcador de figura. Desapareció contenido de V2 que había sido valorado: el diseño muestral y la regla de resolución de discrepancias del protocolo 3.3 (el "aporte metodológico más sólido" según V2), la especificación del entorno de benchmarking de 5.2, la tabla de atributos de 4.2, la priorización de recomendaciones por esfuerzo e impacto del Capítulo 8, los ejemplos de modismos de 6.2, las citas del marco conceptual de 2.1.3 y cuatro de los cinco nodos del Anexo B.

**Problema:** las correcciones de V2 pedían agregar evidencia; la V3 respondió en muchos casos quitando el texto observado. La contradicción desaparece, pero también el contenido evaluable. Un TFI no puede reducirse a un resumen ejecutivo de sí mismo: el tribunal no puede evaluar lo que no está escrito, y en la defensa los autores deberán sostener afirmaciones que el documento no desarrolla. Este es el factor principal del descenso de la calificación.

**Corrección exigida:** construir la V4 sobre la base textual de la V2, incorporando sobre ella las correcciones de ambas instancias, y no sobre la versión condensada. Los Capítulos 3 y 4 deben recuperar al menos la extensión y el nivel de detalle que tenían en V2.

# **5\. Nuevos hallazgos mayores**

**N-04 — El umbral μ \+ 2σ en ventanas de 60 minutos no es adecuado para series de conteo tan dispersas \[MAYOR\]**

**Evidencia:** el corpus reúne 8.240 posts en 181 días (4.344 horas), es decir, 1,9 posts por hora sumando todas las categorías. Por categoría, las tasas horarias son del orden de 0,46 (Phishing), 0,14 (Vulnerabilidades) y 0,06 (Ransomware).

**Problema:** para conteos de ese orden, que se comportan aproximadamente como un proceso de Poisson, μ \+ 2σ cae por debajo de una o dos publicaciones. En Ransomware (μ ≈ 0,06; σ ≈ 0,25) el umbral es ≈ 0,56, de modo que una única publicación en una hora dispara una anomalía; lo mismo ocurre en Vulnerabilidades (umbral ≈ 0,90). Una estimación indicativa bajo el supuesto de Poisson arroja del orden de 260 horas anómalas de Ransomware, 580 de Vulnerabilidades y 330 de Phishing en el semestre: ruido operativo, no detección de picos. El umbral μ \+ 2σ presupone además una distribución aproximadamente normal, que estas series no tienen.

**Corrección exigida:** reportar el número real de disparos del motor en el semestre; justificar ventana y umbral, o adoptar alternativas apropiadas para conteos bajos (ventanas diarias, umbral por cuantil de Poisson, mínimo absoluto de publicaciones, EWMA); y validar el motor contra los tres casos de 5.3.

**N-05 — Criterios a priori: umbral de F1 no declarado, criterios redundantes y FP en el límite exacto \[MAYOR\]**

**Evidencia:** la Tabla 4 evalúa el F1 contra un "Umbral ≥ 0,800" que no figura en la lista de criterios de la Sección 1.6. La tasa de FP es 18,0 % frente a un umbral de ≤ 18 %, y se declara CUMPLIDO.

**Problema:** un umbral que aparece por primera vez en la tabla de resultados no es un criterio a priori. Por otra parte, con la definición adoptada (FP \= 1 − precisión), el criterio FP ≤ 18 % equivale a precisión ≥ 82 % y vuelve redundante el criterio de precisión ≥ 80 %: es un único criterio expresado dos veces con umbrales distintos. Finalmente, con una muestra de a lo sumo 500 publicaciones, el intervalo de confianza del 95 % de una proporción cercana al 18 % tiene una semiamplitud de al menos ±3,4 puntos, por lo que un resultado exactamente sobre el umbral no permite afirmar cumplimiento con robustez.

**Corrección exigida:** certificar que los umbrales de 1.6 son idénticos a los de V2 y, si alguno se modificó entre versiones, declararlo y justificarlo; incorporar el F1 a 1.6 o retirarlo de la evaluación; eliminar la redundancia entre precisión y FP; reportar intervalos de confianza.

**N-06 — El modelo de datos no respalda funciones que el documento declara cumplidas \[MAYOR\]**

**Evidencia:** el DDL del Anexo A define tres tablas: subreddits, posts y comments. No existe columna para el score normalizado de 4.4 (el 0,94 del Caso 3), ni tabla de entidades extraídas, ni tablas de anomalías o de alertas, ni registro de mediciones de latencia.

**Problema:** resultados sin lugar de persistencia no son reconstruibles. En particular, OE4 compromete "extraer entidades" y se declara CUMPLIDO, pero la Sección 4.4 describe solo lematización y clasificación: no hay reconocimiento de entidades descrito ni almacenado. Lo mismo vale para OE5, cuyo motor no tiene dónde registrar sus disparos.

**Corrección exigida:** completar el DDL con las estructuras que correspondan o explicar dónde se persisten esos resultados; describir el componente de extracción de entidades (modelo, etiquetas, ejemplos) o reclasificar OE4 como parcialmente cumplido.

# **6\. Hallazgos menores y de forma**

## **6.1. Estado de las observaciones menores de V2**

| ID | Observación | Estado V3 | Comentario |
| :---- | :---- | ----- | :---- |
| M-01 | Abstract no es espejo del Resumen | **NO RESUELTO** | El Abstract sigue sin métricas y afirma que se superaron todos los umbrales, aunque FP está en el límite y OE6 es parcial |
| M-02 | Gentilicio "mendoceño" | **RESUELTO** | — |
| M-03 | Redondeo de la estratificación | **PARCIAL** | Los tamaños por estrato se eliminaron en lugar de corregirse; restituirlos |
| M-04 | Tablas sin rótulo numerado | **PARCIAL** | Tablas 1 a 3 rotuladas; las Tablas 4 y 5 son listas, no tablas |
| M-05 | Subsecciones de 5.1 sin numerar | **NO RESUELTO** | Figuran en el índice pero no existen como títulos en el cuerpo |
| M-06 | Redacción del Upsert | **RESUELTO** | Por supresión; ver m-18 |
| M-07 | Fecha de consulta de límites de la API | **NO RESUELTO** | — |
| M-08 | Suscriptores sin fecha | **PARCIAL** | Solo r/argentina, sin fecha de relevamiento |
| M-09 | Numeración de Referencias y Anexos | **RESUELTO** | — |
| M-10 | Supuesto no contrastable | **RESUELTO CON OBSERVACIONES** | "Técnicamente robustos" es vago; remitir a los criterios de 1.6 |
| M-11 | "Encriptado" | **RESUELTO** | — |
| M-12 | Declaración de autoría | **RESUELTO CON OBSERVACIONES** | Ver m-17 |

## **6.2. Nuevas observaciones menores**

* **m-13.** Ratios de la Tabla 2 mal redondeados: 8.680 / 1.840 \= 4,717 (corresponde 4,72, se consigna 4,71) y 42.150 / 8.240 \= 5,115 (corresponde 5,12, se consigna 5,11). Se deja constancia de que el error ya existía en V2 y que la tabla de verificación de aquella devolución los consignó como correctos; se rectifica en la Sección 7\.

* **m-14.** Liao et al. (2016) se cita para respaldar que SpiderFoot, Maltego, theHarvester y Recon-ng se orientan al reconocimiento activo de infraestructura. Ese trabajo trata la extracción automatizada de indicadores de compromiso desde fuentes técnicas abiertas: no respalda la afirmación, pero es un antecedente directo del presente TFI y debería usarse como tal. Además, APA 7 no admite "et al." en la lista de referencias (Liao, Pastor-Galindo): consignar los autores.

* **m-15.** Separador decimal inconsistente: "Kappa de Fleiss \= 0.78" frente a la coma decimal del resto del documento.

* **m-16.** La inclusión de r/derechogenial como fuente de ciberseguridad no está justificada, y aporta más publicaciones coincidentes (1.840) que r/devsarg (1.540). Explicitar el criterio de selección de subreddits y discutir el efecto de esa comunidad sobre la composición temática del corpus.

* **m-17.** La declaración de autoría admite implícitamente el uso de herramientas generativas ("sin la debida supervisión") sin identificar cuáles ni para qué tareas. Precisarlo conforme al reglamento vigente e incluir la declaración en el índice.

* **m-18.** OE2 compromete la idempotencia del pipeline, pero la V3 eliminó la mención de la operación Upsert y el DDL por sí solo no la garantiza. Mostrar la sentencia de persistencia (ON CONFLICT o equivalente).

* **m-19.** El Caso 2 combina sector (hospital), provincia (Mendoza), tipo de incidente y fecha exacta: en un universo pequeño esa combinación puede permitir identificar a la institución pese al enmascaramiento del nombre. Revisar la política de 3.4 para generalizar también los atributos indirectos.

* **m-20.** La clave foránea de posts hacia subreddits usa ON DELETE CASCADE: eliminar un subreddit borra toda su evidencia histórica. Para un archivo de inteligencia es preferible RESTRICT, apoyándose en el campo active\_monitoring que ya existe para desactivar el monitoreo.

# **7\. Verificación de consistencia numérica**

Se recalcularon todas las cifras verificables de la V3. Se deja constancia de lo que resultó consistente para que el equipo no revise lo que ya está correcto.

| Verificación | Resultado | Detalle |
| :---- | ----- | :---- |
| Tabla 1 — sumas de posts y comentarios | **CORRECTO** | 8.240 y 42.150; totales mensuales suman 50.390 |
| Tabla 2 — sumas por subreddit | **CORRECTO** | 4.860 \+ 1.540 \+ 1.840 \= 8.240; comentarios \= 42.150 |
| Tabla 2 — ratios r/argentina y r/devsarg | **CORRECTO** | 4,60 y 7,22 |
| Tabla 2 — ratio r/derechogenial | **REDONDEO** | 4,717 → 4,72 (consignado 4,71). Rectifica V2 (m-13) |
| Tabla 2 — ratio general | **REDONDEO** | 5,115 → 5,12 (consignado 5,11). Rectifica V2 (m-13) |
| Tabla 3 — suma de recuentos y porcentajes | **CORRECTO** | Recuentos suman 8.240; porcentajes suman 100,0 |
| Tabla 3 — fila "No Relevante / FP" | **INCONSISTENTE** | 18 % × 8.240 \= 1.483,2; derivada de la tasa (N-02) |
| Tabla 3 — cambios respecto de V2 | **SIN EXPLICAR** | Mismo corpus, recuentos distintos (H-07) |
| Precisión vs. falsos positivos | **CORRECTO** | 1 − 0,82 \= 0,18 (H-04 corregido aritméticamente) |
| F1-score | **CORRECTO** | 2 · 0,82 · 0,81 / 1,63 \= 0,8150 |
| Latencia E2E vs. scheduler de 15 min | **INCONSISTENTE** | Espera esperada ≈ 7,5 min; P95 ≈ 14,3 min (N-01) |
| Throughput vs. configuración | **RESUELTO** | Separado como banco de pruebas (H-06) |
| Umbral de anomalías vs. tasas horarias | **INADECUADO** | Umbral \< 1 post/h en dos categorías (N-04) |
| Casos de 5.3 vs. picos de la Tabla 1 | **CONSISTENTE** | 14/03 y 05/05 caen en los meses de mayor volumen |
| Índice vs. paginación real | **INCONSISTENTE** | Índice hasta p. 39; documento de 24 páginas (H-14) |

# **8\. Rúbrica de evaluación y calificación**

| Dimensión | Peso | V2 | V3 | Fundamento V3 |
| :---- | :---- | :---- | :---- | :---- |
| Estructura y forma académica | 10 % | 6,0 | 5,0 | Figuras como marcadores, índice con paginación ficticia y anexos inexistentes; se valoran autoría y numeración (H-11, H-14) |
| Marco teórico y estado del arte | 15 % | 8,0 | 6,0 | Capítulo condensado, ocho referencias huérfanas, sin contraste con Rivas y Dengra (H-10, N-03) |
| Diseño metodológico | 20 % | 7,0 | 6,0 | Fleiss y sesgo declarados; cobertura sin procedimiento, F1 sin criterio a priori, protocolo empobrecido (H-05, N-05) |
| Desarrollo del artefacto | 20 % | 4,5 | 4,5 | Se agrega 4.5, pero el Anexo B pierde cuatro nodos, sin figuras y con DDL incompleto (H-15, N-04, N-06) |
| Resultados y validez | 20 % | 4,5 | 5,0 | FP y throughput corregidos; latencia imposible y fila de FP derivada (N-01, N-02) |
| Discusión y conclusiones | 10 % | 7,5 | 6,5 | Fuentes y reclasificación de OE6 valoradas; 7.3 remite a anexos inexistentes |
| Aspectos legales y éticos | 5 % | 5,0 | 7,0 | Contradicción del salt resuelta y política de enmascaramiento; ajustes de terminología |
| PROMEDIO PONDERADO | 100 % | 6,0 | 5,5 | Descenso de 0,5 puntos respecto de V2 |

**CALIFICACIÓN DE ESTA INSTANCIA: 5,5 / 10**

**Condición: NO APROBADO EN ESTA INSTANCIA. REENTREGA OBLIGATORIA (V4).**

La nota desciende medio punto respecto de V2, y corresponde explicar por qué, dado que varias correcciones son buenas —la de la seudonimización, la reclasificación de OE6 y la separación del throughput cierran objeciones de fondo—. El descenso responde a tres razones: (1) se perdió contenido evaluable que V2 había valorado, y el documento pasó a ser en buena medida un resumen de sí mismo (N-03); (2) cuatro de los siete hallazgos críticos de V2 siguen abiertos total o parcialmente, incluidos los dos que exigían aportar evidencia (H-05, H-07), y el propio documento anuncia anexos que no contiene; (3) aparecieron dos inconsistencias críticas nuevas en el capítulo de resultados (N-01, N-02).

Se mantiene la proyección de la instancia anterior: el cierre completo de los ítems bloqueantes de la Sección 9 y de al menos siete de los ítems de prioridad alta ubica el trabajo en el rango de 8,0 a 8,5 en la V4. La inclusión adicional de la validación con evaluador externo (H-13) y de la estimación de amenazas reales corregida por precisión (N-02) lo ubicaría por encima de 8,5.

**No se habilita la defensa. La V4 debe construirse sobre la base textual de la V2 e incorporar las correcciones de ambas instancias.**

# **9\. Plan de correcciones exigido para la V4**

Ordenado por prioridad de ejecución. Los ítems 1 a 8 son condición de habilitación a defensa.

| \# | Acción requerida | Hallazgo | Prioridad |
| :---- | :---- | :---- | ----- |
| 1 | Reconstruir la V4 sobre la base textual de la V2, recuperando el contenido perdido (protocolo 3.3, entorno de pruebas, tabla de 4.2, ejemplos de modismos, priorización de recomendaciones) | N-03 | **Bloqueante** |
| 2 | Definir el intervalo de latencia y medir publicación → ingesta desde la base (n, media, P50, P95); ajustar el criterio o el diseño | N-01, H-12 | **Bloqueante** |
| 3 | Rehacer la Tabla 3 desde SQL, rotular correctamente la fila residual, estimar amenazas reales corregidas por precisión y explicar los cambios respecto de V2 | N-02, H-07 | **Bloqueante** |
| 4 | Incorporar el workflow exportado real (Anexo B), el diccionario taxonómico (Anexo C) y el repositorio (Anexo D), o corregir 7.3 y el índice | H-07, H-15 | **Bloqueante** |
| 5 | Documentar la captura-recaptura (ventana, n₁, n₂, m, estimador, independencia) o retirar la métrica de cobertura | H-05 | **Bloqueante** |
| 6 | Escribir la fórmula de FP en 3.3 y publicar la matriz de confusión 6×6 | H-04 | **Bloqueante** |
| 7 | Formalizar el motor de anomalías, reportar sus disparos reales, justificar o reemplazar el umbral y validarlo contra los casos de 5.3 | H-03, N-04 | **Bloqueante** |
| 8 | Reemplazar los marcadores por las cuatro figuras reales y agregar índice de tablas y figuras | H-11 | **Bloqueante** |
| 9 | Certificar los umbrales a priori, incorporar o retirar el F1, eliminar la redundancia precisión/FP y reportar intervalos de confianza | N-05 | **Alta** |
| 10 | Completar el DDL (score, entidades, anomalías, alertas) y describir la extracción de entidades o reclasificar OE4 | N-06 | **Alta** |
| 11 | Precisar el alcance implementado de OE6 y alinear objetivo general, Resumen y Abstract | H-02, M-01 | **Alta** |
| 12 | Corregir la terminología HMAC, documentar la configuración de n8n (crypto, \$env) y la gestión de la clave | H-01 | **Alta** |
| 13 | Hacer coincidir criterio y medición de throughput y restituir la especificación del entorno de pruebas | H-06 | **Alta** |
| 14 | Citar las ocho referencias huérfanas o retirarlas, contrastar con Rivas y Dengra (2026), completar CABASE y Fortinet, corregir el uso de Liao et al. | H-08, H-10, m-14 | **Alta** |
| 15 | Regenerar el índice automáticamente y verificar la paginación | H-14, M-05 | **Alta** |
| 16 | Definir la función de puntuación y su normalización; justificar o eliminar pg\_trgm | H-16, H-17 | **Alta** |
| 17 | Explicitar la regla de desempate del etiquetado; se recomienda submuestra con evaluador externo | H-13 | **Alta** |
| 18 | Restituir los ejemplos de modismos que sostienen la brecha de 2.2 | H-09 | **Alta** |
| 19 | Correcciones de forma pendientes: M-03, M-04, M-07, M-08 y m-13 a m-20 | Menores | **Media** |

*Devolución emitida por el tribunal evaluador — Tecnicatura Universitaria en Programación, UTN Facultad Regional Mendoza. Documento de uso académico interno, destinado a los autores y a la dirección del trabajo.*