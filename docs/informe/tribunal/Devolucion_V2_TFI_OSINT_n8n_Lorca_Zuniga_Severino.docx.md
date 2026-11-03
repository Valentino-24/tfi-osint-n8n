**UNIVERSIDAD TECNOLÓGICA NACIONAL — FACULTAD REGIONAL MENDOZA**

Tecnicatura Universitaria en Programación — Tribunal Evaluador de Trabajos Finales

**DEVOLUCIÓN DE AUDITORÍA ACADÉMICA**

Segunda instancia de revisión (V2)

| Campo | Detalle |
| :---- | :---- |
| Título del TFI | Sistema automatizado de monitoreo de foros y redes sociales para la detección de tendencias y alertas en ciberseguridad en Argentina mediante OSINT y n8n |
| Autores | Valentino Lorca — Jerónimo Zúñiga — Enzo Severino |
| Directores | Prof. Alberto Cortez — Prof. Ariel Enferrel |
| Archivo auditado | tesis\_v2.pdf |
| Instancia | V2 — revisión sobre versión corregida |
| Fecha de devolución | 17 de septiembre de 2026 |
| Calificación de esta instancia | 6,0 / 10 — APROBADO CON CORRECCIONES OBLIGATORIAS |
| Habilitación a defensa | Condicionada al cierre de los 7 hallazgos críticos (Sección 3\) |

# **1\. Alcance y método de la auditoría**

La presente devolución audita la versión 2 del documento, verificando cinco dimensiones: (i) consistencia interna de las cifras declaradas, contrastando todas las tablas entre sí y contra el texto; (ii) trazabilidad entre objetivos específicos, resultados presentados y evidencia efectivamente incluida en el documento; (iii) solidez metodológica de las métricas y de sus protocolos de medición; (iv) correspondencia entre el cuerpo del trabajo y los anexos técnicos (SQL y JSON del workflow); y (v) cumplimiento formal de normas APA 7.ª edición y de estructura de TFI.

Los hallazgos se clasifican en tres niveles. CRÍTICO: compromete la validez de un resultado declarado o contradice otra parte del propio documento; su corrección es condición para la defensa. MAYOR: debilita la consistencia académica o la verificabilidad, sin invalidar el trabajo. MENOR: cuestiones de forma, estilo o precisión terminológica.

Se deja constancia de que la auditoría se realiza exclusivamente sobre el documento entregado. No se tuvo acceso al repositorio de código, a la base de datos ni al entorno de ejecución, por lo que ninguna afirmación cuantitativa del Capítulo 5 pudo verificarse contra evidencia primaria. Esta restricción es en sí misma un hallazgo (ver H-07).

# **2\. Avances reconocidos respecto de la instancia anterior**

Corresponde reconocer que esta versión incorpora mejoras sustantivas y que varias de ellas resuelven objeciones metodológicas de fondo. En particular:

* Incorporación de la Sección 1.6 con criterios de éxito definidos a priori y justificados. Declarar los umbrales antes de la evaluación y no después es una corrección metodológica mayor, correctamente ejecutada.

* Incorporación de la Sección 3.3 con el protocolo de validación del clasificador: tamaño muestral, muestreo aleatorio estratificado, etiquetado independiente, coeficiente Kappa y regla de resolución de discrepancias. Es el aporte metodológico más sólido del documento.

* Honestidad epistémica en la respuesta a PI-1 (Sección 7.2), donde se declara explícitamente que la comparación contra soluciones propietarias no se ejecutó y se la reconoce como la principal limitación de alcance. Esta autocrítica es valorada positivamente y debe conservarse.

* Explicitación de que el clasificador es heurístico basado en reglas y diccionarios, y no un modelo estadístico entrenado (Secciones 2.1.3 y 4.4). La decisión de ingeniería está ahora declarada y justificada, no encubierta.

* Especificación del entorno de benchmarking de throughput y latencia (Sección 5.2), con hardware, versión de motor y protocolo de carga.

* Cierre del Capítulo 8 con recomendaciones priorizadas por esfuerzo e impacto, ligadas a las limitaciones declaradas.

Los hallazgos que siguen no desconocen estos avances: señalan lo que aún impide considerar cerrado el expediente.

# **3\. Hallazgos críticos (bloqueantes para la defensa)**

**H-01 — Contradicción entre el cuerpo del trabajo y el Anexo B: el salt de anonimización es fijo, no dinámico  \[CRÍTICO\]**

**Ubicación:** Sección 3.4 vs. Anexo B (nodo node-04-anonymize).

**Evidencia:** La Sección 3.4 afirma que los nombres de usuario se procesan "mediante hash SHA-256 con una clave de salado (salt) dinámica y privada", y que ello constituye un "protocolo de anonimización irreversible". El Anexo B contiene el código efectivamente ejecutado:

const salt \= 'UTN\_FRM\_CIBERSEG\_2026';

**Problema:** El salt es una constante hardcodeada en el workflow, ni dinámica ni privada: está publicada en el propio TFI. Con un salt conocido y fijo, el espacio de nombres de usuario de Reddit es enumerable por fuerza bruta o por diccionario, de modo que el hash es reversible en la práctica. Técnicamente esto es seudonimización, no anonimización.

**Impacto legal:** La conclusión de cumplimiento de la Ley 25.326 (OE8 y respuesta a PI-4) se apoya sobre esta premisa. Si el dato es reidentificable, sigue siendo dato personal en los términos del art. 2 de la ley, y el argumento de cumplimiento se cae. Este es el hallazgo de mayor gravedad del documento.

**Corrección exigida:** Optar por una de dos vías y documentarla con precisión: (a) implementar un salt secreto generado en el despliegue, almacenado fuera del workflow (variable de entorno o gestor de credenciales de n8n), nunca publicado, y reemplazar el Anexo B en consecuencia; o (b) mantener la implementación actual y reescribir la Sección 3.4 y las conclusiones abandonando el término "anonimización irreversible" en favor de "seudonimización", con el análisis de riesgo residual de reidentificación que ello obliga. No se acepta que el cuerpo afirme una cosa y el anexo demuestre otra.

**Observación adicional:** El texto habla de "hash SHA-256 con salt" mientras el código usa createHmac (HMAC-SHA-256). Son construcciones distintas; unificar la terminología.

**H-02 — El objetivo OE6 (generación de alertas) se declara CUMPLIDO sin que el artefacto documentado lo implemente  \[CRÍTICO\]**

**Ubicación:** OE6 (1.5), Sección 5.3, Sección 7.1 vs. Anexo B.

**Evidencia:** La Sección 7.1 declara OE6 CUMPLIDO mediante "nodos webhook que notifican instantáneamente", y la Sección 5.3 reporta un disparo de alerta en Telegram con latencia de 3,8 minutos. Sin embargo, el workflow del Anexo B tiene exactamente cinco nodos —scheduler, OAuth2, fetch, anonimizar, persistir en PostgreSQL— y el bloque connections termina en "Persist to PostgreSQL (Upsert)". No existe nodo de webhook, de Telegram, ni de evaluación de criticidad.

**Problema:** Tal como está documentado, el sistema no emite alertas. Un objetivo específico declarado cumplido sin evidencia en el artefacto es la observación más severa que puede recibir un TFI de desarrollo, porque afecta la credibilidad del resto de las declaraciones de cumplimiento.

**Corrección exigida:** Incorporar al Anexo B el subflujo completo de alertas (nodo de clasificación de criticidad, condicional y nodo de Telegram/webhook), con captura de pantalla del workflow en n8n y captura de al menos un mensaje de alerta real recibido. Alternativamente, si el módulo no está implementado, reclasificar OE6 como PARCIALMENTE CUMPLIDO o NO CUMPLIDO y eliminar las latencias de alerta de 5.3 y 7.1.

**H-03 — El objetivo OE5 (motor de detección de anomalías y tendencias) no tiene método descrito en ningún capítulo  \[CRÍTICO\]**

**Ubicación:** OE5 (1.5) y Sección 7.1.

**Evidencia:** OE5 compromete "un motor de reglas semánticas para la detección automática de anomalías y tendencias emergentes en el flujo continuo de datos". La Sección 7.1 lo declara CUMPLIDO y como prueba ofrece el 82 % de precisión de clasificación en cinco categorías.

**Problema:** Clasificar un texto en una categoría temática no es detectar una anomalía ni una tendencia. La detección de anomalías exige una línea de base, una ventana temporal de comparación y un umbral de disparo (por ejemplo, desvíos estándar sobre la media móvil de publicaciones por hora y categoría). Nada de eso aparece en el Capítulo 4, que es donde debería estar. La evidencia ofrecida no corresponde al objetivo declarado.

**Corrección exigida:** Agregar una subsección 4.5 que especifique formalmente el algoritmo de detección de picos: variable monitoreada, ventana, línea de base, umbral y regla de disparo. Si tal motor no existe y la detección de los picos de marzo y mayo fue un análisis posterior manual sobre la base de datos, debe decirse así y OE5 debe reclasificarse.

**H-04 — Inconsistencia aritmética entre la precisión (82 %) y la tasa de falsos positivos (15 %)  \[CRÍTICO\]**

**Ubicación:** Sección 5.2 y Resumen.

**Evidencia:** Se reportan, sobre la misma muestra de control de 500 publicaciones, una precisión de clasificación del 82,0 % y una tasa de falsos positivos del 15,0 %.

**Problema:** Si la tasa de falsos positivos se define como la proporción de ítems marcados como amenaza que no lo son —la lectura operativa que el propio trabajo adopta en 1.6 al justificarla por la "saturación del canal de alertas"—, entonces debe ser exactamente el complemento de la precisión: 18,0 %, no 15,0 %. Si en cambio se la define como FP/(FP+VN), es decir, sobre el total de negativos reales, el valor puede ser 15 % pero se trata de otra métrica y el documento nunca lo aclara. Tal como está, dos cifras del mismo párrafo se contradicen.

**Corrección exigida:** Definir la fórmula de la tasa de falsos positivos de manera explícita en la Sección 3.3, y recalcular el valor de la Sección 5.2, del Resumen y del Abstract de modo que sea aritméticamente coherente con la precisión reportada. Se sugiere además publicar la matriz de confusión 6×6 completa de la muestra de 500, de la cual todas estas métricas se derivan y con la cual el tribunal puede verificarlas en un solo paso.

**H-05 — La métrica de cobertura (84 %) carece de protocolo de medición y de denominador verificable  \[CRÍTICO\]**

**Ubicación:** Sección 1.6, Sección 5.2, OE7 y respuesta a PI-3.

**Evidencia:** Se define la cobertura como "Recall de ingesta", con umbral ≥ 80 %, y se reporta un valor obtenido de 84,0 %. El protocolo de la Sección 3.3 valida únicamente al clasificador; no describe cómo se midió la cobertura.

**Problema:** La cobertura es un cociente y el documento nunca informa su denominador. Para conocer qué porcentaje del universo se capturó haría falta conocer el universo total de publicaciones coincidentes, y el propio trabajo argumenta en 2.1.2 y 6.3 que ese universo es inaccesible porque Pushshift fue discontinuado y los listings de la API topean en 1.000 ítems. El trabajo afirma medir precisamente aquello que declara no poder observar. El 84 % queda, hoy, sin sustento.

**Corrección exigida:** Describir el procedimiento real de estimación. Una vía metodológicamente admisible y al alcance del TFI es la captura-recaptura: recolectar una ventana acotada (por ejemplo, una semana) por dos canales independientes —el pipeline y una extracción manual exhaustiva del subreddit— y estimar la cobertura por solapamiento. Si no se ejecuta un procedimiento de este tipo, la métrica de cobertura debe retirarse de 1.6, 5.2, 7.1, el Resumen y el Abstract.

**H-06 — El throughput declarado es incompatible con la configuración de ingesta documentada  \[CRÍTICO\]**

**Ubicación:** Sección 4.3 y Anexo B vs. Sección 5.2 y OE7.

**Evidencia:** La Sección 4.3 y el Anexo B fijan un scheduler cada 15 minutos y un parámetro limit: 100 por consulta. La Sección 5.2 reporta un throughput de 1.450 posts/hora como métrica SUPERADA frente al umbral de ≥ 1.000 posts/hora.

**Problema:** Con cuatro ejecuciones por hora y un tope de 100 ítems por llamada, el techo estructural de ingesta del sistema tal como está desplegado es del orden de 400 posts/hora por consulta configurada, por debajo del umbral declarado. El valor de 1.450 proviene de una prueba sintética de carga sobre el componente de procesamiento, no de la operación real; el documento lo insinúa pero presenta la cifra en la misma tabla y con el mismo estatus que las métricas operativas, lo que induce a error.

**Contraste adicional:** El corpus real —8.240 posts en seis meses— equivale a menos de 2 posts/hora. La distancia entre la operación real y la cifra declarada es de tres órdenes de magnitud.

**Corrección exigida:** Separar la tabla de la Sección 5.2 en dos bloques rotulados: métricas operativas (medidas sobre el corpus real) y métricas de capacidad en banco de pruebas (carga sintética). Renombrar la fila como "Throughput máximo de procesamiento (banco de pruebas)" y agregar un párrafo que discuta explícitamente el techo de ingesta impuesto por el scheduler y por las cuotas de la API, enlazándolo con la respuesta a PI-3.

**H-07 — Reproducibilidad declarada sin artefactos disponibles y clasificación del corpus sin categoría residual  \[CRÍTICO\]**

**Ubicación:** Sección 7.3, Tabla 3 (Sección 5.1) y Sección 3.3.

**Evidencia (a):** La Sección 7.3 afirma aportar una base "documentada y reproducible", pero el documento no informa repositorio de código, versión del workflow exportado, ni política de disponibilidad del dataset o del diccionario taxonómico completo. Las cinco familias de amenazas se mencionan, pero el diccionario que las define —el corazón del clasificador— nunca se publica.

**Evidencia (b):** La Tabla 3 distribuye los 8.240 posts entre las cinco categorías de amenaza sumando 100,0 %, sin ninguna fila de "No relevante". Sin embargo, la Sección 3.3 incluye "No relevante" como sexta categoría del etiquetado y la Sección 5.2 reporta un 15 % de falsos positivos. Ambas cosas no pueden ser simultáneamente ciertas: si hay falsos positivos, una fracción del corpus no es una amenaza real y la tabla no puede cerrar en 100 % sobre cinco categorías de amenaza.

**Observación sobre las cifras:** Los cinco porcentajes de la Tabla 3 son exactamente 38,0 / 26,0 / 16,0 / 12,0 / 8,0 %, es decir, números redondos sin un solo decimal residual, sobre un total de 8.240. Una distribución empírica que arroja cinco valores exactos y suma exacta es estadísticamente improbable y sugiere que los recuentos fueron derivados desde porcentajes elegidos, y no al revés. El tribunal requerirá explicación sobre este punto.

**Corrección exigida:** Publicar el diccionario taxonómico completo como Anexo C y el workflow exportado íntegro como Anexo D, e informar la URL del repositorio. Reconstruir la Tabla 3 desde una consulta SQL sobre la base real —incluyendo la fila "No relevante"— y adjuntar dicha consulta. Los recuentos deben provenir de la base, con los decimales que arrojen.

# **4\. Hallazgos mayores**

**H-08 — Afirmaciones cuantitativas sin fuente en el Capítulo 6  \[MAYOR\]**

**Evidencia:** La Sección 6.2 informa penetración de plataformas con precisión decimal (WhatsApp ≈93 %, Instagram ≈86,7 %, X ≈47,2 %, Telegram ≈44,1 %) atribuyéndolas a "relevamientos sectoriales" sin citar ninguno. La Sección 6.1 invoca "reportes sectoriales de ciberseguridad en Argentina durante el período 2025-2026" igualmente sin referencia.

**Problema:** Cifras con un decimal exigen fuente identificable, año y fecha de consulta. Sin ella son inverificables y, en una defensa, indefendibles.

**Corrección exigida:** Citar la fuente primaria de cada cifra con norma APA 7 (informe, organismo, año, URL y fecha de recuperación) o eliminar los valores numéricos y reformular en términos cualitativos.

**H-09 — Afirmación del 30 % sin experimento que la sustente  \[MAYOR\]**

**Evidencia:** Sección 6.2: "un clasificador genérico en inglés hubiera categorizado incorrectamente más del 30 % de los incidentes reales".

**Problema:** Es una afirmación contrafáctica cuantificada. No se ejecutó ningún clasificador en inglés sobre el corpus, de modo que el 30 % no tiene origen. Es además uno de los argumentos con los que se defiende el aporte del trabajo, lo que agrava la observación.

**Corrección exigida:** Ejecutar la prueba de ablación —correr el mismo pipeline con el diccionario en inglés sin adaptación de modismos sobre la muestra de control de 500 posts y reportar la caída de F1— o eliminar el porcentaje y sostener el argumento de manera cualitativa con los ejemplos de "caer", "pescar" y "cangrejo", que son ilustrativos y suficientes.

**H-10 — Ocho referencias bibliográficas no citadas en el cuerpo, en contra de APA 7  \[MAYOR\]**

**Evidencia:** El Capítulo 9 declara referencias "verificadas contra las publicaciones originales". No obstante, no se encuentran citadas en el texto: Honnibal et al. (2020), ISO/IEC 27001:2022, Liao et al. (2016), n8n.io (2026), PostgreSQL Global Development Group (2026), Reddit Inc. (2026), Rivas y Dengra (2026) y Zong et al. (2020).

**Problema:** APA 7 exige correspondencia biunívoca entre la lista de referencias y las citas en el texto. Adicionalmente, Rivas y Dengra (2026) es un TFI previo de la propia UTN FRM sobre el mismo tema: no citarlo en el estado del arte es una omisión de fondo, no de forma, porque es el antecedente más directo del trabajo y la brecha declarada en 2.2 debería delimitarse respecto de él.

**Corrección exigida:** Citar cada referencia en el punto del texto que corresponda —SpaCy en 4.4, las documentaciones técnicas al describir las herramientas, ISO 27001 en el marco legal o eliminarla, Liao et al. y Zong et al. en el estado del arte— e incorporar una subsección en 2.2 que contraste explícitamente este TFI con el de Rivas y Dengra (2026). Verificar además los datos de publicación de Zong et al. (2020): el DOI consignado corresponde a la revista Cybersecurity de SpringerOpen y el volumen y las páginas indicadas deben confirmarse contra el original.

**Nota adicional:** La referencia del Decreto 1558/2001 atribuye su autoría a la Dirección Nacional de Protección de Datos Personales. Un decreto reglamentario es dictado por el Poder Ejecutivo Nacional; corregir la entrada.

**H-11 — Capítulo 4 insuficiente: no hay diagrama de arquitectura ni evidencia de implementación  \[MAYOR\]**

**Evidencia:** La Sección 4.1, titulada "Arquitectura del Pipeline de Datos", se resuelve en un único párrafo descriptivo. El documento completo no contiene ni una sola figura: no hay diagrama de arquitectura, ni diagrama entidad-relación de la base, ni captura del workflow en n8n, ni captura del canal de alertas, ni gráfico de la serie temporal que sostiene los picos de marzo y mayo.

**Problema:** En un TFI de desarrollo, el capítulo de construcción del artefacto es el núcleo de la evaluación y aquí es el más breve del trabajo. La ausencia total de figuras obliga al lector a reconstruir mentalmente el sistema desde prosa, y priva al tribunal de la evidencia visual habitual de que el artefacto existe y funciona.

**Corrección exigida:** Incorporar como mínimo cuatro figuras numeradas y referenciadas desde el texto: Figura 1, diagrama de arquitectura extremo a extremo; Figura 2, DER de la base PostgreSQL; Figura 3, captura del workflow desplegado en n8n; Figura 4, serie temporal mensual de publicaciones por categoría. Añadir un índice de tablas y figuras luego del índice general.

**H-12 — Métricas sin medidas de dispersión ni tamaño muestral  \[MAYOR\]**

**Evidencia:** La latencia extremo a extremo se informa como 4,2 minutos y la de consulta analítica como inferior a 50 ms, sin indicar sobre cuántas mediciones, ni desvío estándar, ni percentiles.

**Problema:** En un sistema de alerta temprana con umbral de 5 minutos, el promedio es la medida menos informativa: lo que determina si el umbral se cumple operativamente es la cola de la distribución. Un promedio de 4,2 minutos es compatible con un percentil 95 muy superior a 5 minutos, en cuyo caso el criterio de éxito no estaría satisfecho en la práctica.

**Corrección exigida:** Reportar n, media, desvío estándar y percentiles 50/95 para latencia y throughput, y discutir el cumplimiento del umbral en términos del percentil 95 y no solo de la media.

**H-13 — Validación del clasificador realizada por los propios desarrolladores  \[MAYOR\]**

**Evidencia:** Las 500 publicaciones de la muestra de control fueron etiquetadas por los tres autores del TFI, que son también quienes construyeron el diccionario taxonómico contra el cual se evalúa el clasificador.

**Problema:** El ciego declarado es entre evaluadores, no respecto del sistema. Quien escribió las reglas tiende a etiquetar de acuerdo con ellas, lo que infla precisión y recall por construcción. Es un sesgo conocido y debe al menos declararse.

**Corrección exigida:** Incorporar el sesgo de evaluación endógena a la Sección 6.3 como limitación explícita. Si el cronograma lo permite, hacer etiquetar por un evaluador externo al equipo una submuestra de 100 publicaciones y reportar el Kappa contra el consenso interno. Considerar además el uso de Kappa de Fleiss, más apropiado que el de Cohen para tres evaluadores, y explicitar la regla de desempate cuando los tres votos difieren entre seis categorías.

**H-14 — Índice general desactualizado respecto del cuerpo del documento  \[MAYOR\]**

**Evidencia:** El índice no refleja la estructura real. Lista 1.6 como "Preguntas de Investigación" cuando en el cuerpo 1.6 es "Supuesto de Trabajo y Criterios de Éxito" y 1.7 las preguntas. Lista el Capítulo 2 con cinco secciones de primer nivel cuando el cuerpo lo organiza en 2.1 (con 2.1.1 a 2.1.4) y 2.2. Omite la Sección 3.3, "Protocolo de Validación del Clasificador NLP", que es una de las incorporaciones más valiosas de esta versión, y desplaza "Aspectos Legales" de 3.4 a 3.3. Omite la Sección 7.2 y renombra 7.3. El Capítulo 8 figura como "RECOMENDACIONES" y en el cuerpo es "RECOMENDACIONES Y TRABAJOS FUTUROS". La paginación declarada también es inconsistente: el índice se autoubica en la página 5 cuando precede físicamente al Resumen, consignado en la página 3\.

**Problema:** Un índice que no coincide con el cuerpo sugiere que las correcciones se incorporaron sin regenerar la tabla de contenidos, y además oculta al lector la mejora metodológica más importante de la V2.

**Corrección exigida:** Regenerar el índice automáticamente a partir de los estilos de título y verificar la paginación de todo el preliminar.

**H-15 — Defectos técnicos en el código del Anexo B  \[MAYOR\]**

**Evidencia:** El nodo Code utiliza input.all como propiedad e itera sobre ella:

for (let item of input.all) { ... }  return input.all;

**Problema:** En el nodo Code de n8n la forma correcta es \$input.all(), que es una función y no una propiedad; tal como está, el nodo lanza una excepción en tiempo de ejecución. A ello se suman: el uso de require('crypto') sin la habilitación de módulos correspondiente en el entorno de n8n; el tipo de nodo n8n-nodes-base.interval, reemplazado por scheduleTrigger en las versiones actuales; el endpoint https\://oauth.reddit.com/r/devsarg/search.json, que en el dominio OAuth no lleva sufijo .json y requiere restrict\_sr=1 para acotar la búsqueda al subreddit; y la ausencia del encabezado User-Agent identificatorio, que la API de Reddit exige y cuya omisión deriva en bloqueos.

**Impacto:** El anexo que debería probar que el sistema funciona contiene código que, tal como está transcripto, no se ejecuta. Dado que el Anexo B se presenta como "modelo lógico conceptual", corresponde o bien exportar el JSON real del workflow, o bien rotular el fragmento inequívocamente como pseudocódigo ilustrativo.

**Corrección exigida:** Reemplazar el Anexo B por la exportación literal del workflow desde n8n, verificada como importable. Si se conserva una versión reducida por extensión, indicarlo y adjuntar el archivo completo como material suplementario.

**H-16 — Inconsistencias entre la Sección 4.2 y el Anexo A, y claim de 3FN discutible  \[MAYOR\]**

**Evidencia:** La tabla de la Sección 4.2 omite campos que el DDL del Anexo A sí define (url, score, num\_comments, nlp\_category, nlp\_processed, ingested\_at, subscribers, active\_monitoring) y la descripción de la tabla comments queda truncada en dos atributos. Además, el Anexo A crea la extensión pg\_trgm y nunca la utiliza, ya que el índice GIN se construye sobre to\_tsvector('spanish', ...), que no la requiere.

**Problema adicional:** Se afirma un diseño "bajo estrictas reglas de normalización (3FN)", pero nlp\_category se almacena como VARCHAR(100) libre y repetido en posts y comments, sin tabla de categorías ni clave foránea. Es una denormalización deliberada y defendible por rendimiento, pero entonces debe declararse como tal y no presentarse como 3FN estricta.

**Corrección exigida:** Completar la tabla de 4.2 para que sea espejo exacto del DDL; eliminar la creación de pg\_trgm o justificar su uso; y o bien normalizar nlp\_category en una tabla de catálogo con FK, o bien documentar explícitamente la denormalización y su motivo.

**H-17 — Tratamiento de los casos del Capítulo 5.3: entidades identificables y puntaje de confianza sin definir  \[MAYOR\]**

**Evidencia:** El Caso 2 refiere un ataque de ransomware a "los servidores de un hospital mendoceño", con variante y fecha. El Caso 3 reporta una filtración de "una cadena de comercio electrónico argentina" con volumen de registros. El Caso 3 consigna además "una puntuación de confianza del 94 %".

**Problema (a):** El trabajo construye todo un capítulo sobre el cuidado de la privacidad de los usuarios y luego reproduce, sin verificación con fuente secundaria, incidentes atribuibles a instituciones concretas —una institución de salud es, además, un caso sensible— tomados de publicaciones anónimas de un foro. Es una inconsistencia ética interna que un tribunal señalará.

**Problema (b):** Un clasificador heurístico por coincidencia ponderada de lemas no produce, sin una definición explícita, una probabilidad. El 94 % carece de fórmula: no se explica cómo la puntuación de coincidencia se normaliza a un porcentaje de confianza.

**Corrección exigida:** Definir formalmente en 4.4 la función de puntuación y su normalización al intervalo \[0,1\], o retirar la expresión "confianza" y hablar de puntuación de coincidencia. Incorporar en 3.4 una política explícita de tratamiento de incidentes no confirmados que afecten a organizaciones identificables, y aplicarla al Capítulo 5.3.

# **5\. Hallazgos menores y de forma**

* **M-01.** El Abstract no es espejo del Resumen: el texto en español informa los resultados obtenidos (F1 0,815; falsos positivos 15 %) mientras el inglés solo enumera los umbrales y afirma que fueron superados. Ambos deben transmitir la misma información.

* **M-02.** Error ortográfico en la Sección 5.3, Caso 2: el gentilicio correcto es "mendocino", no "mendoceño".

* **M-03.** Estratificación de la muestra de control con redondeo inexacto: la proporción de r/devsarg sobre 500 arroja 93,4 (consignado 94\) y la de r/derechogenial 111,7 (consignado 111). Corregir a 93 y 112, o explicitar el criterio de redondeo empleado.

* **M-04.** Las tablas de los Capítulos 5 y 4 carecen de título numerado formal sobre el cuerpo de la tabla. El texto las llama "Tabla 1", "Tabla 2" y "Tabla 3", pero el rótulo no aparece junto a ellas; las del Capítulo 4 ni siquiera están numeradas.

* **M-05.** Las subsecciones de la Sección 5.1 ("Distribución Temporal", "Distribución por Comunidad", "Clasificación Temática") no están numeradas, a diferencia del resto del documento.

* **M-06.** Redacción confusa en la Sección 4.3: "n8n ejecuta una operación Upsert antes de intentar la inserción". El upsert es la inserción; reformular como "la persistencia se resuelve mediante una operación Upsert sobre la clave única del identificador de Reddit".

* **M-07.** El Capítulo 2 declara un límite de "100 consultas por minuto por identificador de cliente". Consignar la fecha de consulta de la documentación de la API de Reddit, ya que estos límites cambian y el dato es el fundamento de PI-3.

* **M-08.** Los subreddits se caracterizan sin datos verificables ("más de un millón de usuarios"). Consignar el recuento de suscriptores con fecha de relevamiento, coherentemente con el campo subscribers que la propia base almacena.

* **M-09.** Numerar como capítulos las Referencias (9) y los Anexos (10) es inusual en el formato de TFI; habitualmente van sin numeración de capítulo. Verificar contra el reglamento vigente de la carrera.

* **M-10.** El supuesto de trabajo de la Sección 1.6 postula niveles "comparables a soluciones propietarias", comparación que —como el propio trabajo reconoce— no se ejecutó. Reformular el supuesto de modo que sea contrastable con la evidencia efectivamente producida, y dejar la comparación con soluciones propietarias como pregunta abierta.

* **M-11.** En el diccionario de la Tabla 3 se emplea "encriptado"; se sugiere "cifrado" en la redacción académica, conservando el término coloquial solo cuando se cite el léxico de los usuarios.

* **M-12.** Falta una declaración de autoría y de uso de herramientas de asistencia, exigible en la mayoría de los reglamentos vigentes.

# **6\. Verificación de consistencia numérica realizada**

Se recalcularon todas las cifras verificables del documento. Se deja constancia expresa de lo que sí resultó consistente, para que el equipo no revise lo que ya está correcto:

| Verificación | Resultado | Detalle |
| :---- | :---- | :---- |
| Tabla 1 — suma de posts mensuales | CORRECTO | 1.120+980+1.740+1.250+1.850+1.300 \= 8.240 |
| Tabla 1 — suma de comentarios | CORRECTO | Suma \= 42.150; total general 50.390 coherente |
| Tabla 2 — suma por subreddit | CORRECTO | 4.860+1.540+1.840 \= 8.240; comentarios \= 42.150 |
| Tabla 2 — ratios comentario/post | CORRECTO | 4,60 / 7,22 / 4,71; general 5,11 |
| Tabla 3 — suma de recuentos | CORRECTO | 3.131+2.142+1.318+989+660 \= 8.240 |
| Tabla 3 — porcentajes | SOSPECHOSO | Exactos a un decimal en las cinco filas (ver H-07) |
| F1-score declarado | CORRECTO | 2·0,82·0,81/(0,82+0,81) \= 0,8149 ≈ 0,815 |
| Precisión vs. falsos positivos | INCONSISTENTE | 1 − 0,82 \= 18 %, no 15 % (ver H-04) |
| Estratificación de la muestra | REDONDEO | 93,4→94 y 111,7→111 (ver M-03) |
| Throughput vs. configuración | INCONSISTENTE | Techo de \~400 posts/h con scheduler de 15 min (ver H-06) |
| Kappa vs. umbral de Landis y Koch | CORRECTO | κ \= 0,78 \> 0,61; acuerdo sustancial bien clasificado |

# **7\. Rúbrica de evaluación y calificación**

| Dimensión | Peso | Nota | Fundamento |
| :---- | :---- | :---- | :---- |
| Estructura y forma académica | 10 % | 6,0 | Índice desactualizado, tablas sin rótulo, sin índice de figuras (H-14, M-04) |
| Marco teórico y estado del arte | 15 % | 8,0 | Sólido y bien articulado; omite el antecedente directo de la propia facultad (H-10) |
| Diseño metodológico | 20 % | 7,0 | DSR bien aplicado y protocolo de validación del clasificador ejemplar; cobertura sin protocolo (H-05) |
| Desarrollo del artefacto | 20 % | 4,5 | Capítulo más breve del trabajo, sin figuras, con módulos declarados y no documentados (H-02, H-03, H-11, H-15) |
| Resultados y validez | 20 % | 4,5 | Inconsistencias métricas y cifras no reconstruibles desde evidencia (H-04, H-06, H-07) |
| Discusión y conclusiones | 10 % | 7,5 | Interpretación madura y autocrítica explícita en PI-1; afirmaciones sin fuente (H-08, H-09) |
| Aspectos legales y éticos | 5 % | 5,0 | Buen encuadre normativo invalidado por la contradicción del salt (H-01, H-17) |
| PROMEDIO PONDERADO | 100 % | 6,0 | Aprobado con correcciones obligatorias |

**CALIFICACIÓN DE ESTA INSTANCIA: 6,0 / 10**

Condición: APROBADO CON CORRECCIONES OBLIGATORIAS. El trabajo tiene un núcleo metodológico correcto y un tema pertinente y bien delimitado; lo que lo mantiene en 6,0 no es el diseño sino la distancia entre lo que se declara logrado y lo que el documento efectivamente demuestra. Los siete hallazgos críticos son todos subsanables sin rehacer el sistema: cuatro exigen corregir o acotar afirmaciones, y tres exigen adjuntar evidencia que presumiblemente ya existe.

Se deja asentado que el cierre completo de los hallazgos críticos y de al menos siete de los diez mayores ubica el trabajo en el rango de 8,0 a 8,5 en la instancia siguiente. La resolución adicional de H-09 mediante la prueba de ablación y de H-11 con las figuras solicitadas lo ubicaría por encima de 8,5.

**No se habilita la defensa hasta la presentación de la versión 3 con los siete hallazgos críticos resueltos.**

# **8\. Plan de correcciones exigido para la V3**

Ordenado por prioridad de ejecución. Los ítems 1 a 7 son condición de habilitación.

| \# | Acción requerida | Hallazgo | Prioridad |
| :---- | :---- | :---- | :---- |
| 1 | Resolver la contradicción del salt: implementar salt secreto fuera del workflow o reescribir como seudonimización con análisis de riesgo residual | H-01 | Bloqueante |
| 2 | Documentar el subflujo de alertas con captura del workflow y de una alerta real, o reclasificar OE6 | H-02 | Bloqueante |
| 3 | Especificar el algoritmo de detección de anomalías en una nueva Sección 4.5, o reclasificar OE5 | H-03 | Bloqueante |
| 4 | Definir la fórmula de la tasa de falsos positivos y publicar la matriz de confusión de la muestra de 500 | H-04 | Bloqueante |
| 5 | Describir el protocolo de medición de cobertura (se sugiere captura-recaptura) o retirar la métrica | H-05 | Bloqueante |
| 6 | Separar métricas operativas de métricas de banco de pruebas y discutir el techo de ingesta | H-06 | Bloqueante |
| 7 | Publicar diccionario taxonómico, workflow exportado y repositorio; reconstruir la Tabla 3 desde SQL con categoría residual | H-07 | Bloqueante |
| 8 | Citar todas las fuentes cuantitativas del Capítulo 6 y contrastar con Rivas y Dengra (2026) | H-08, H-10 | Alta |
| 9 | Ejecutar la ablación del clasificador en inglés o retirar el 30 % | H-09 | Alta |
| 10 | Incorporar las cuatro figuras mínimas e índice de tablas y figuras | H-11 | Alta |
| 11 | Reportar n, desvío y percentil 95 de latencia y throughput | H-12 | Alta |
| 12 | Declarar el sesgo de evaluación endógena y evaluar Kappa de Fleiss | H-13 | Alta |
| 13 | Regenerar el índice y verificar la paginación del preliminar | H-14 | Alta |
| 14 | Reemplazar el Anexo B por el JSON real exportado y verificado | H-15 | Alta |
| 15 | Alinear Sección 4.2 con el DDL y resolver el claim de 3FN | H-16 | Alta |
| 16 | Definir la puntuación de confianza y fijar política de entidades identificables | H-17 | Alta |
| 17 | Correcciones de forma M-01 a M-12 | Menores | Media |

 

Devolución emitida por el tribunal evaluador — Tecnicatura Universitaria en Programación, UTN Facultad Regional Mendoza. Documento de uso académico interno, destinado a los autores y a la dirección del trabajo.