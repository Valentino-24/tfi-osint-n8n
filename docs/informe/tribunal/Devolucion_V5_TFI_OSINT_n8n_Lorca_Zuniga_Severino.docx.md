**UNIVERSIDAD TECNOLÓGICA NACIONAL — FACULTAD REGIONAL MENDOZA**

Tecnicatura Universitaria en Programación — Tribunal Evaluador de Trabajos Finales

**DEVOLUCIÓN DE AUDITORÍA ACADÉMICA**

*Quinta instancia de revisión (V5)*

| Título del TFI | Sistema automatizado de monitoreo de foros y redes sociales para la detección de tendencias y alertas en ciberseguridad en comunidades técnicas de Reddit mediante OSINT y n8n |
| :---- | :---- |
| **Autores** | Valentino Lorca — Jerónimo Zúñiga — Enzo Severino |
| **Directores** | Prof. Alberto Cortez — Prof. Ariel Enferrel |
| **Archivo auditado** | tesis\_v5.pdf (114 páginas, 4 figuras embebidas) |
| **Instancia** | V5 — revisión con cotejo contra la devolución V4 del 20/10/2026 |
| **Fecha de devolución** | 30 de octubre de 2026 |
| **Calificación V4 (referencia)** | 6,9 / 10 |
| **Calificación de esta instancia** | 7,8 / 10 — APROBADO CON CORRECCIONES OBLIGATORIAS. VERSIÓN FINAL V6 |
| **Habilitación a defensa** | Condicionada a la V6: cierre de los 5 ítems bloqueantes de la Sección 9 y resolución de la instancia académica correspondiente sobre la declaración del Anexo E (Sección 4\) |

# **1\. Alcance y método de la auditoría**

La presente devolución audita la versión 5 del documento con dos propósitos. Primero, verificar uno por uno el estado de los 17 hallazgos de la V2 (H-01 a H-17), de los 14 hallazgos de la V3 y la V4 (N-01 a N-14) y de las observaciones menores pendientes. Segundo, auditar la V5 como pieza autónoma, con las mismas cinco dimensiones de las instancias anteriores: consistencia numérica interna, trazabilidad entre objetivos y evidencia, solidez metodológica de las métricas, correspondencia entre cuerpo y anexos, y cumplimiento formal.

El estado de cada hallazgo se clasifica como **RESUELTO**; **RESUELTO CON OBSERVACIONES** (la objeción de fondo está cerrada y persisten ajustes); **PARCIAL**; o **NO RESUELTO**. Los hallazgos surgidos en esta instancia continúan la numeración: N-15 a N-19 (mayores) y m-31 a m-38 (menores).

Se mantiene la restricción de las instancias anteriores: la auditoría se realiza sobre el documento entregado. La V5 declara un repositorio y una copia congelada con su SHA-256, pero ninguno de los dos formó parte de los archivos recibidos para esta auditoría, de modo que el código y el SQL del Anexo B se auditaron por su consistencia interna y contra lo que el cuerpo afirma, no contra el artefacto. Se inspeccionaron las cuatro figuras y se recalcularon todas las cifras verificables: intervalos exactos de Clopper-Pearson, tamaño de muestra con corrección por población finita, kappa de Fleiss, estimadores ponderados (también por comunidad), umbrales de Poisson del recálculo del motor y número esperado de falsas alarmas (Sección 7).

# **2\. Avances reconocidos respecto de la V4**

La V5 es la mejor versión del trabajo y la que más se acerca a un informe defendible. Corresponde reconocerlo expresamente:

* Se incorporó la **declaración de trazabilidad entre versiones** (Anexo E), con inventario de los resultados retirados, su origen y el ciclo de vida de los datos. Su contenido se trata en la Sección 4\.

* Se hizo una **validación nueva sobre el corte exacto del corpus B5**: censo de las 170 detecciones y muestra aleatoria de 182 de las 554 «No relevante», con tamaño justificado y corrección por población finita, semilla y orden deterministas, hojas ciegas, guía previa al etiquetado, tres anotadores con kappa de Fleiss sobre 50 casos comunes, estimadores ponderados e intervalos exactos. Todas las cifras de las Tablas 5.7 a 5.10 se verificaron sin errores aritméticos.

* Los resultados se informan **contra los umbrales y sin maquillaje**: sensibilidad (0,612) y F1 (0,711) NO CUMPLIDOS, acuerdo (κ \= 0,509) por debajo del 0,61 comprometido y una estimación de 235 amenazas en el corpus frente a las 170 detectadas.

* La latencia se corrigió y se explicó: se rectificó la afirmación sobre el «piso», se descompuso por estado de ejecución y por comunidad, y se identificó la causa real del P95 —la operación intermitente del sistema—. También se identificó la causa del hueco del 03/10.

* El motor de anomalías se **recalculó retrospectivamente** sobre la fecha de creación, se informó el número esperado de falsas alarmas (0,95, verificado), se explicó el disparo del 13/10 como discontinuidad de la línea base y OE5 se reclasificó como «implementado; eficacia no demostrada».

* El throughput se declara NO EVALUADO de forma uniforme; la tasa de falsos descubrimientos pasó a complemento informativo; la Tabla 1.1 fecha cada umbral.

* El Anexo B transcribe el código de los cuatro nodos de código, el SQL de los tres nodos de base de datos y las quince consultas de evidencia. El Anexo D declara repositorio y copia congelada con hash.

* El DDL incorpora DEFAULT 'PENDIENTE' y UNIQUE (categoria, ventana\_inicio); la sentencia de upsert transcribe su lista SET (m-21, m-29).

* El diccionario se auditó reimplementando el clasificador y reproduciendo las 724 clasificaciones; las erratas se corrigieron, los términos genéricos y los guiones se cuantificaron, y la decisión de congelarlo se fundamenta en el marco muestral. Se publicó la traza de coincidencias de los casos.

* La extracción de entidades tiene resultados por familia, comunidad y categoría, y su principal modo de error («ios» dentro de otras palabras, 96,1 %) está medido.

* La privacidad mejoró: códigos de caso en lugar de identificadores, riesgo residual ampliado al identificador de plataforma, al determinismo del HMAC y a los metadatos, y retiro fundamentado de «irreversible».

* El alcance se reformuló por la vía (b) de N-13 de manera coherente: título, objetivo general, PI-2, brecha e iteración declarada en la Tabla 3.1.

* Se corrigieron las referencias normativas (m-25), el Abstract (m-26) y se identificaron las herramientas generativas (m-27).

Persisten, sin embargo, problemas que afectan la lectura de los resultados: la interpretación del desempeño por idioma está invertida (N-15); la referencia de la validación es de un único anotador en el 86 % de los casos y el uso de herramientas en el etiquetado se describe de dos maneras (N-16); la operación intermitente, ya medida, no se trasladó a las conclusiones (N-17); el código y el esquema transcriptos no se presentan con la versión que operó (N-18); y aparece un nuevo conjunto de contradicciones internas (N-19). A ello se suman aspectos formales y de contenido de la declaración del Anexo E (Sección 4).

# **3\. Estado de los hallazgos de la V4**

## **3.1. Tablero de seguimiento**

| ID | Hallazgo | Estado V5 | Síntesis |
| :---- | :---- | :---- | :---- |
| H-01 | Seudonimización de autores | **RESUELTO CON OBSERVACIONES** | Código transcripto; «irreversible» retirado; errores sobre las 237 publicaciones previas |
| H-02 | Alcance de OE6 (alertas) | **RESUELTO** | «Avisos diarios» en objetivo y título; payload publicado; credencial aclarada |
| H-03 | Motor de anomalías (OE5) | **RESUELTO CON OBSERVACIONES** | Reclasificado como implementado sin eficacia demostrada; ver N-11 |
| H-04 | Matriz de confusión | **RESUELTO** | Matriz por categoría con marginales verificados |
| H-05 | Métrica de cobertura | **RESUELTO** | Se mantiene retirada |
| H-06 | Throughput | **RESUELTO** | NO EVALUADO de forma uniforme |
| H-07 | Reproducibilidad y anexos | **RESUELTO CON OBSERVACIONES** | URL, copia con hash y Q1–Q15 en el documento; copia no recibida |
| H-08 | Fuentes del Capítulo 6 | **RESUELTO** | Se mantiene |
| H-09 | Ejemplos de modismos | **RESUELTO CON OBSERVACIONES** | Errata corregida en el código, no en 2.2 |
| H-10 | Referencias | **RESUELTO** | Normativa corregida; antecedente como inédito |
| H-11 | Figuras | **RESUELTO CON OBSERVACIONES** | Figura 4 con eje continuo; defectos menores (m-34) |
| H-12 | Medidas de dispersión | **RESUELTO CON OBSERVACIONES** | DS informado; falta declarar la latencia de consulta analítica |
| H-13 | Validación endógena | **RESUELTO CON OBSERVACIONES** | Tres anotadores y κ informado; referencia de un anotador en 302 casos (N-16) |
| H-14 | Índice general | **PARCIAL** | Sigue con un solo nivel |
| H-15 | Anexo B (workflow) | **RESUELTO CON OBSERVACIONES** | Código y SQL transcriptos; versión no identificada (N-18) |
| H-16 | Modelo relacional | **RESUELTO** | Se mantiene |
| H-17 | Casos y puntuación | **RESUELTO** | Códigos de caso y traza de coincidencias |
| N-01 | Latencia extremo a extremo | **RESUELTO** | Medida, descompuesta y no cumplida |
| N-02 | Fila residual | **RESUELTO** | Estimación de 235 amenazas en el corpus |
| N-03 | Contracción del documento | **RESUELTO** | Se mantiene |
| N-04 | Umbral del motor | **RESUELTO** | Se mantiene |
| N-05 | Criterios a priori | **RESUELTO** | FDR como complemento; fecha de cada umbral |
| N-06 | Modelo de datos y entidades | **RESUELTO CON OBSERVACIONES** | Resultados de extracción publicados; defectos del extractor (N-18) |
| N-07 | Trazabilidad entre versiones | **RESUELTO CON OBSERVACIONES** | Declaración completa; firmas e inconsistencias pendientes (Sección 4\) |
| N-08 | Validación del clasificador | **RESUELTO CON OBSERVACIONES** | Rehecha sobre B5; ver N-15, N-16 y N-18 (b) |
| N-09 | Explicación de la latencia | **RESUELTO CON OBSERVACIONES** | Causa identificada; régimen de operación no trasladado (N-17) |
| N-10 | Exposición de identificadores | **RESUELTO CON OBSERVACIONES** | Códigos de caso; títulos literales y menciones pendientes |
| N-11 | Eficacia del motor | **RESUELTO CON OBSERVACIONES** | Recalculado; variante de línea base no declarada (m-31) |
| N-12 | Diccionario | **RESUELTO CON OBSERVACIONES** | Auditado y congelado con fundamento; solapamientos incompletos |
| N-13 | Alcance «Argentina» | **RESUELTO** | Vía (b) aplicada de forma consistente |
| N-14 | Inconsistencias internas | **PARCIAL** | 9 de 14 corregidas; nuevas en N-19 |

**Síntesis:** 14 resueltos, 15 resueltos con observaciones, 2 parciales y ninguno no resuelto. De los cinco ítems bloqueantes de la V4, cuatro quedan cerrados con observaciones (1, 2, 3 y 4\) y uno queda parcial (5: contradicciones internas). Los ocho ítems de prioridad alta (6 a 13\) quedan cerrados, con o sin observaciones. Es el mejor nivel de cumplimiento de todas las instancias.

## **3.2. Detalle por hallazgo**

**H-01 — Seudonimización de autores \[RESUELTO CON OBSERVACIONES\]**

**Corregido:** «irreversible» se retiró del Resumen, del Abstract y de 3.4, que ahora explica por qué el procedimiento no lo es; el código del nodo HMAC Anonymize está transcripto (Código B.1) y descarta el valor original; se declara que la clave anterior se perdió el 25/09/2026.

**Persiste:** 3.4 afirma que las 237 publicaciones previas a la rotación «conservan» un hash y «no son vinculables entre sí». Según E.3 esas publicaciones se eliminaron el 01/10/2026; y si existieran, al haberse calculado con una misma clave, las de un mismo autor sí serían vinculables entre sí (no lo serían con las posteriores). Además, la clave vigente se guarda en un archivo de texto en el perfil de usuario del equipo: declarar sus permisos de acceso. **Exigido para V6:** corregir 3.4 (N-19, ítem 13).

**H-02 — Objetivo OE6 (alertas) \[RESUELTO\]**

El objetivo general habla de avisos diarios y 4.5 explica por qué; el título ya no promete alertas tempranas; se publica un payload enmascarado, verificado como coherente con el disparo de Infraestructura y Ataques del 01/10; y el Anexo B aclara la diferencia entre editar el flujo y vincular una credencial.

**H-03 — Objetivo OE5 (motor de anomalías) \[RESUELTO CON OBSERVACIONES\]**

OE5 se declara «implementado; eficacia no demostrada» en 5.4.1, 7.1 y 7.2, como se exigió. Las observaciones sobre el recálculo se tratan en m-31.

**H-04 — Matriz de confusión por categoría \[RESUELTO\]**

La Tabla 5.10 cruza referencia y clasificador sobre los 352 casos; sus marginales coinciden con las Tablas 5.3 y 5.7 (verificado). La lectura de las dos categorías peor resueltas requiere un ajuste (N-19, ítem 11).

**H-05 / H-08 / H-16 — Cobertura, fuentes del Capítulo 6 y modelo relacional \[RESUELTO\]**

Se mantienen resueltos.

**H-06 — Throughput \[RESUELTO\]**

El criterio se declara NO EVALUADO en el Resumen, la Tabla 1.1, la Tabla 5.15 y la Tabla 7.1, con la distinción entre capacidad y demanda y con el techo de diseño presentado como cota, no como medición. Es la alternativa admitida en la V4.

**H-07 — Reproducibilidad y anexos \[RESUELTO CON OBSERVACIONES\]**

**Corregido:** el Anexo D declara la URL del repositorio, una copia congelada con tamaño, cantidad de archivos y SHA-256, su inventario y el procedimiento de verificación; el Anexo B.4 transcribe Q1 a Q15.

**Persiste:** la copia congelada no formó parte de los archivos recibidos para esta auditoría y el acceso al repositorio se condiciona a una invitación, de modo que el hash no pudo verificarse ni el código del Anexo B cotejarse con el workflow exportado. **Exigido para V6:** entregar la copia por canal institucional o el acceso de lectura (bloqueante 5). El tribunal verificará el hash y cotejará por muestreo el Anexo B con el artefacto.

**H-09 — Ejemplos de modismos \[RESUELTO CON OBSERVACIONES\]**

La errata «caeron los servidores» se corrigió en el código y en el Anexo C, pero 2.2 sigue citando la forma errónea como término del diccionario (N-19, ítem 7).

**H-10 — Referencias bibliográficas \[RESUELTO\]**

La Ley 25.326 figura en la lista; el Decreto 1558/2001 se atribuye al Poder Ejecutivo Nacional; Pastor-Galindo et al. ya no se cita como fuente de los umbrales; Dengra y Rivas se cita como trabajo inédito con versión y fecha de consulta.

**H-11 — Figuras \[RESUELTO CON OBSERVACIONES\]**

La Figura 4 (a) usa un eje continuo con el 03/10 en cero, y la Figura 3 ya no superpone nodos. Quedan defectos menores (m-34) y el texto de 5.1 contradice ahora la figura corregida (N-19, ítem 1).

**H-12 — Medidas de dispersión \[RESUELTO CON OBSERVACIONES\]**

La Tabla 5.4 informa el desvío estándar de los subconjuntos operativos y comenta los máximos. Sigue sin declararse que la latencia de consulta analítica que informaba la V2 no se midió, como se pidió en la V4.

**H-13 — Validación endógena del clasificador \[RESUELTO CON OBSERVACIONES\]**

Se pasó de un anotador a tres, con kappa de Fleiss informado tal como se obtuvo (0,509) y discusión de su consecuencia. Siguen siendo anotadores internos, lo que el documento declara. La composición real de la referencia se trata en N-16.

**H-14 — Índice general \[PARCIAL\]**

El índice general sigue teniendo un solo nivel y omite el Resumen, el Abstract, la Declaración y las Siglas (m-28).

**H-15 — Anexo B (workflow) \[RESUELTO CON OBSERVACIONES\]**

**Corregido:** se transcriben los nodos HMAC Anonymize, Classify Dictionary, Extract Entities y Anomaly Engine, y el SQL de Upsert Posts, Query Daily Counts y Registrar Anomalias y Alertas, exactamente lo exigido en la V4. La transcripción permitió verificar varias afirmaciones del cuerpo: la lista SET, la fórmula de Poisson corregida, el centinela y la mecánica de coincidencia.

**Persiste:** la versión transcripta no es la que operó durante la ventana y sus comentarios contradicen el Capítulo 5 (N-18).

**H-17 — Casos y puntuación \[RESUELTO\]**

Los casos se identifican con códigos C-01 a C-13 y se publica la lista de términos que coincidieron en cada uno, lo que hace visible el mecanismo de los falsos positivos.

**N-01 — Latencia extremo a extremo \[RESUELTO\]**

Medida desde la base, descompuesta por subconjunto, por estado de ejecución y por comunidad, y declarada NO CUMPLIDA sin excluir publicaciones.

**N-02 — Fila residual de la tabla de clasificación \[RESUELTO\]**

Con la muestra extraída de B5 se estimaron 235 amenazas en el corpus (32,5 %), como se exigió.

**N-03 / N-04 — Contracción del documento y umbral del motor \[RESUELTO\]**

Se mantienen resueltos.

**N-05 — Criterios a priori \[RESUELTO\]**

La tasa de falsos descubrimientos es un complemento informativo y no se cuenta como criterio; la Tabla 1.1 y la cronología de 1.6 fechan cada umbral. Una frase de 1.6 requiere precisión (N-19, ítem 14).

**N-06 — Modelo de datos y extracción de entidades \[RESUELTO CON OBSERVACIONES\]**

La sección 5.6 publica los resultados de la extracción por familia, comunidad y categoría, explica que los productos se reconocen por lista blanca y mide su principal modo de error. Quedan defectos del extractor sin declarar ni cuantificar (N-18, d).

**N-07 — Trazabilidad entre versiones \[RESUELTO CON OBSERVACIONES\]**

Ver Sección 4\.

**N-08 — Validación del clasificador \[RESUELTO CON OBSERVACIONES\]**

**Corregido:** la validación se rehízo sobre el corpus evaluado con el diseño exigido: censo del estrato positivo, muestra aleatoria reproducible del negativo con tamaño justificado, cegamiento, guía escrita, tres anotadores con kappa sobre 50 casos comunes, estimadores ponderados con intervalos exactos y resultados por comunidad e idioma. La muestra del 30/09 se conserva solo como antecedente de la corrección del umbral. Los puntos (a), (b), (d) y (e) de la V4 quedan cerrados.

**Persiste:** la lectura del desempeño por idioma (N-15); la composición de la referencia y la descripción del uso de herramientas en el etiquetado (N-16, que retoma el punto c); y la tabla de transición caso por caso de la muestra del 30/09, que no se presentó (punto f; N-18, b).

**N-09 — Explicación de la latencia \[RESUELTO CON OBSERVACIONES\]**

La V5 corrige el «piso», compara la espera observada con la esperada por diseño (7,5 minutos frente a una mediana de 9,0 con el sistema en ejecución), descompone por comunidad y revisa las 254 publicaciones con más de una hora de espera. La causa real queda identificada: el sistema estuvo en ejecución alrededor del 19 % de la ventana. Esa medición tiene inconsistencias de cálculo y no se trasladó al resto del informe (N-17).

**N-10 — Exposición de identificadores \[RESUELTO CON OBSERVACIONES\]**

**Corregido:** los identificadores se reemplazaron por códigos con la correspondencia fuera del cuerpo, y el riesgo residual se amplió al identificador de plataforma, al determinismo del HMAC con nombres de baja entropía y a los metadatos.

**Persiste:** (a) 5.4 transcribe los títulos literales de C-05, C-11, C-12 y C-13; un título es buscable y conduce a la publicación, y C-13 es una consulta personal de un usuario, no una divulgación técnica; para las de r/netsec corresponde citar el aviso o el CVE, como pidió la V4. (b) No se decidió ni se documentó el tratamiento de las menciones a usuarios en el cuerpo (N-10, c de la V4). (c) El archivo de correspondencia figura en el árbol del repositorio (D.2), aunque 3.3.2 dice que «no se publica»: declarar que el repositorio es privado o excluir el archivo del versionado.

**N-11 — Eficacia del motor de anomalías \[RESUELTO CON OBSERVACIONES\]**

El recálculo por fecha de creación se hizo, los umbrales y el número esperado de falsas alarmas se verificaron, la referencia externa para el disparo del 12/10 se aplicó y OE5 se reclasificó. El procedimiento de línea base del recálculo difiere del motor sin que se declare (m-31).

**N-12 — Diccionario \[RESUELTO CON OBSERVACIONES\]**

Las erratas se corrigieron; los términos genéricos y el problema de los guiones se cuantificaron sobre el corpus; la decisión de congelar el diccionario se fundamenta en que el marco muestral de la validación depende de él, razonamiento que el tribunal acepta; y se publicó la traza de coincidencias. La auditoría de solapamientos es incompleta (N-18, e).

**N-13 — Alcance «Argentina» \[RESUELTO\]**

Se adoptó la vía (b) de forma consistente: título, objetivo general, delimitación, PI-2, brecha, iteración declarada en la Tabla 3.1 y reemplazo de «se verificó empíricamente» por «se ilustra». La interpretación del rendimiento local se trata en N-15.

**N-14 — Inconsistencias internas de cifras y estados \[PARCIAL\]**

De los catorce ítems de la V4 se corrigieron nueve (2, 4, 5, 6, 9, 10, 11, 13 y 14). Persisten total o parcialmente cinco: el 1 (detecciones correctas de r/devsarg, ahora 3 en 5.7 y 2 en 7.3), el 3 (días de operación), el 7 (falsos positivos de r/DerechoGenial), el 8 (los comentarios del código conservan las cifras contradictorias) y el 12 (la referencia al 03/10 cambió de error). Aparecen además las contradicciones nuevas de N-19.

# **4\. Declaración de trazabilidad entre versiones (N-07)**

**Recepción y contenido.** La V5 incorpora el Anexo E con carácter de declaración jurada de los autores. Declara que los valores cuantitativos publicados en la V2 y la V3 —corpus de 8.240 publicaciones y 42.150 comentarios, series por mes, aporte por comunidad, distribución temática, cobertura, precisión, sensibilidad, F1, tasa de falsos positivos, latencia, throughput en banco de pruebas, kappa de Fleiss de 0,78 con tres evaluadores y los tres casos de su sección 5.3— no provienen de ninguna medición; que se produjeron como parte del texto redactado con asistencia de herramientas generativas; que no existe respaldo de ellos; que no deben citarse como resultados; y que ninguna cifra de la V4 ni de la V5 deriva de ellos. Documenta además el ciclo de vida de los datos (Tabla E.2) y retira las afirmaciones de diseño no implementadas (E.5).

**Valoración del tribunal.** La declaración cumple el contenido exigido en la V4 y lo hace sin atenuantes: no invoca errores de transcripción ni corpus extraviados, asume la responsabilidad de los autores y extiende su alcance a cualquier otro valor que el tribunal identifique. El tribunal lo valora. Al mismo tiempo, deja constancia de lo que la declaración establece: en dos instancias de evaluación (V2 y V3) se presentaron como resultados medidos —con tablas, umbrales, un coeficiente de acuerdo entre evaluadores y casos fechados— valores que no surgieron de ninguna medición. Esa cuestión excede la evaluación técnica del documento. **El tribunal eleva la declaración a la instancia académica que corresponda conforme al reglamento vigente.** La calificación de esta devolución se refiere exclusivamente a la V5 como documento y no prejuzga lo que esa instancia resuelva; la habilitación a defensa queda sujeta, además, a esa resolución.

**Observaciones a subsanar en la V6:**

* **(a) Firmas.** Las líneas de firma del Anexo E y de la Hoja de firmas (4.7) están en blanco, y el «original firmado» se identifica como un archivo .md, que no admite firma. Debe entregarse por canal institucional un original con firmas manuscritas o digitales de los tres autores y de la dirección.

* **(b) Quién toma conocimiento.** E.6 dice que «la dirección de la carrera toma conocimiento», pero las líneas corresponden a los directores del trabajo. La V4 pidió el conocimiento de la dirección del trabajo; corregir la frase.

* **(c) Ciclo de vida del corpus.** La Tabla E.2 indica que al 25/09 había 237 publicaciones (r/argentina, r/devsarg y r/DerechoGenial) y que el TRUNCATE del 01/10 «elimina las 237 publicaciones anteriores». Pero la muestra del 30/09 contiene publicaciones de r/netsec y r/Malware —comunidades incorporadas el 25/09—, y la propia V5 (5.5) sostiene que las 22 sorteadas como «No relevante» representaban «una de cada veinticinco», es decir unas 550 publicaciones negativas. La base del 30/09 tenía, por lo tanto, bastante más de 237 publicaciones, y la tabla omite la recolección entre el 25 y el 30/09. Informar cuántas publicaciones había el 30/09 por comunidad, cuántas eliminó el TRUNCATE y si alguna se recuperó después por el arrastre inicial del 01/10.

* **(d) Alcance a la V3.** E.1 dice que «las versiones V1 y V2 se redactaron con asistencia de herramientas generativas», mientras los valores inventariados también figuraban en la V3 y E.6 habla de las versiones V1 a V3. Precisar el alcance.

* **(e) Origen de latencia y throughput.** E.1 los califica como «estimación del diseño inicial», pero en la V2 y la V3 se presentaron como medidos (el throughput, «en banco de pruebas»). Declarar que se presentaron como mediciones sin serlo.

* **(f) Errores puntuales.** La fila de cobertura dice que esta «no alcanza ese valor» en la ventana real, cuando el criterio se retiró y no se evaluó. Las remisiones a «5.3» y «5.3.2, Tabla 5.8» corresponden a 5.5 y 3.3.2. Los códigos IN-07 y C-25 y la ruta openspec/changes/recoleccion-secundaria/ no se definen ni figuran en el inventario del Anexo D; C-25 además colisiona con la serie de códigos de caso.

# **5\. Nuevos hallazgos mayores**

**N-15 — La lectura del desempeño por idioma confunde la omisión del estrato negativo con la sensibilidad e invierte la conclusión sobre el léxico local \[MAYOR\]**

**Ubicación:** 5.5 (Tablas 5.9 y 5.9.b y su comentario), 6.1, 6.2, 6.4 y 7.3 (PI-2).

**Evidencia:** la Tabla 5.9.b informa para el español una «omisión» de 1,5 % (2 de 135 sorteadas) y el texto concluye que «en español rioplatense (r/devsarg) la omisión es baja». La Sección 6.1 sostiene que la omisión «se concentra en las comunidades en inglés \[...\], no en la local».

**Problema:** el 1,5 % es la proporción de amenazas dentro de lo que el clasificador descartó en r/devsarg, no la proporción de amenazas que el clasificador omite. Es baja porque r/devsarg tiene 421 publicaciones descartadas y casi todas son ajenas al tema; esa dilución no dice cuántas amenazas encuentra el clasificador. Aplicando a cada comunidad el mismo estimador ponderado que el informe usa para el agregado, con su peso propio:

| Comunidad | TP (censo) | Omitidas en muestra | Peso | Omisiones estimadas | Sensibilidad estimada |
| :---- | :---- | :---- | :---- | :---- | :---- |
| r/devsarg (español) | 3 | 2 de 135 | 421/135 \= 3,12 | 6,2 | ≈ 0,32 (≈ 0,12 a 0,80) |
| r/netsec | 60 | 15 de 29 | 84/29 \= 2,90 | 43,4 | ≈ 0,58 |
| r/Malware | 81 | 13 de 18 | 49/18 \= 2,72 | 35,4 | ≈ 0,70 |
| Inglés (ambas) | 141 | 28 de 47 | — | 78,8 | ≈ 0,64 |
| Agregado postestratificado | 144 | 30 de 182 | — | 85,1 | ≈ 0,63 |

El intervalo de r/devsarg se obtiene con la misma transformación del intervalo exacto de la omisión que usa 3.3.5. En el corpus evaluado, el léxico local detecta alrededor de una de cada tres amenazas de su comunidad, con una precisión de 3/7: la lectura opuesta a la del informe. La estimación es muy incierta —descansa en dos omisiones observadas—, pero eso impide afirmar que la omisión local sea baja, no habilita afirmarlo. Para el agregado, la postestratificación da unas 229 amenazas y una sensibilidad de 0,63, cercanas a las informadas (235 y 0,612): la conclusión global no cambia.

**Corrección exigida:** agregar a las Tablas 5.9 y 5.9.b la sensibilidad estimada por comunidad e idioma, con su peso y su intervalo; renombrar la columna «Omisión» como «proporción de amenazas en la muestra del estrato negativo»; reescribir el comentario de 5.9.b, el segundo hallazgo de 6.1, 6.2, 6.4 y la respuesta a PI-2, declarando que la evidencia sobre el léxico rioplatense es insuficiente para estimar su sensibilidad y que la estimación puntual disponible es baja.

**N-16 — La referencia de 302 de los 352 casos es de un único anotador, y el uso de herramientas generativas en el etiquetado se describe de dos maneras \[MAYOR\]**

**Ubicación:** Declaración de autoría, Resumen, Abstract, 3.3.2, 3.3.3, 5.5, 5.5.2, 6.3 y E.4.

**Evidencia:** según 3.3.2, dos anotadores etiquetaron una submuestra común de 50 casos y el tercero etiquetó los 352; la adjudicación por consenso resolvió los 20 desacuerdos de esos 50\. El Resumen y el Abstract («con un protocolo de tres anotadores y adjudicación por consenso»), 5.5 («con tres anotadores y consenso registrado») y E.4 («352 casos etiquetados \[...\] con tres anotadores y adjudicación por consenso») presentan la referencia como si las 352 etiquetas fueran de consenso.

**Problema:** (a) En 302 casos (85,8 %) la referencia es la etiqueta de una sola persona. Con un acuerdo moderado —16 de los 50 casos comunes (32 %) tuvieron desacuerdo sobre si había amenaza—, la etiqueta individual puede diferir del consenso en una proporción que afecta directamente TP, FP y las omisiones del estrato negativo. Los intervalos informados recogen solo la incertidumbre del muestreo, no la de la etiqueta. (b) No se identifica quién etiquetó los 352 casos, dato necesario porque la V4 declaraba un anotador único «sin formación formal en ciberseguridad y con asistencia de herramientas». (c) La Declaración de autoría dice que las herramientas generativas asistieron en la «preparación y revisión del proceso de etiquetado \[...\] y verificación de coherencia entre casos»; 3.3.2 dice que la asistencia «se limitó a la preparación de la guía». Verificar la coherencia entre casos supone que la herramienta procesó casos etiquetados: si señaló incoherencias y alguna etiqueta se modificó, influyó en la referencia aunque no haya decidido la etiqueta final.

**Corrección exigida:** declarar en el Resumen, el Abstract, 3.3.2, 5.5 y E.4 la composición real de la referencia (50 casos con consenso de tres anotadores; 302 con la etiqueta de un anotador) e identificar a ese anotador; informar, sobre los 50 casos comunes, la coincidencia entre la etiqueta del anotador de los 352 casos y la de consenso, en la decisión binaria y por categoría, y recalcular precisión, omisión y sensibilidad con la etiqueta de cada anotador para mostrar el rango; unificar la descripción del uso de herramientas en el etiquetado, indicando qué material procesó la herramienta, qué produjo y si alguna etiqueta se modificó a partir de su salida.

**N-17 — La operación intermitente del sistema está medida pero no trasladada al resto del informe, y su cuantificación tiene inconsistencias \[MAYOR\]**

**Ubicación:** 2.2, 5.1, 5.3, 5.4, 5.8, 6.2, 6.3, 7.1, 7.2, 7.3 (PI-1), 7.4 y Figura 1\.

**Evidencia:** 5.3 establece que la instancia de n8n estuvo en ejecución 4.929 de 25.920 minutos (19,0 %), en jornadas diurnas iniciadas por el operador, y que el 71,2 % de las publicaciones creadas en la ventana se creó con el sistema detenido. Es el hallazgo que explica la latencia, y el tribunal lo valora (N-09).

**Problema:** (a) Ese régimen no es un detalle de la latencia: el artefacto evaluado recolecta mientras el operador mantiene el equipo encendido y el flujo activo. El resto del documento sigue describiendo otro sistema. La brecha (2.2) es «la ausencia de un sistema de monitoreo continuo»; 6.2 presenta como aporte el «monitoreo temporal continuo»; 7.2 concluye que el sistema «recolecta, normaliza y persiste de forma autónoma y sostenida»; PI-1 habla de «un único servidor en contenedores»; 7.4 atribuye la latencia a que «el ritmo de la fuente manda sobre la capacidad del artefacto», cuando 5.3 demuestra que la causa fue la operación; y 5.8 declara OE1 «cumplido» mientras la Tabla 7.2 lo declara «cumplido con reparos».

(b) El denominador de 25.920 minutos equivale a 18 días, mientras la ventana tiene 17 (24.480 minutos), y el numerador proviene de un registro que solo conserva corridas desde el 05/10: los dos términos del cociente no cubren el mismo intervalo. Tampoco se explica cómo se clasificaron como «creadas con el motor detenido» o «en ejecución» las publicaciones del 01 al 04/10, para las que no hay registro de ejecuciones.

(c) 5.3 dice que las jornadas «terminan entre las 19:00 y las 23:00» y, en la oración siguiente, que «en ninguno de los 17 días hubo ingesta entre las 19:00 y las 12:00».

(d) 5.3 dice que el registro cubre «del 05/10 al 18/10» y 5.1 que el 18/10 «no hubo ninguna ejecución del disparador». Sin embargo, el día 17/10 figura como evaluado por el motor de anomalías (5.4), y esa evaluación solo puede provenir de la corrida de las 12:05 del 18/10. Del mismo modo, la evaluación del 16/10 corresponde a la corrida de las 12:05 del 17/10, día en que la jornada comenzó a las 12:12 según 5.1. Si esas evaluaciones se ejecutaron manualmente debe declararse, porque la consulta de conteo usa now() y el instante de ejecución determina qué día se evalúa.

(e) En 5.3 y 6.3 «motor» designa la instancia de n8n, y en el resto del documento, el motor de anomalías. Varias frases quedan ambiguas («el motor operó solo el 19,0 % del período»).

**Corrección exigida:** incorporar en 5.1 una tabla del régimen de operación por día —inicio y fin de la jornada, corridas automáticas y manuales del flujo de ingesta y del flujo de análisis con su hora—, construida desde el registro de ejecuciones y, para los días sin registro, desde ingested\_at, declarando el método; recalcular la fracción de operación con numerador y denominador sobre el mismo intervalo; explicar cómo se produjeron las evaluaciones del 16/10 y del 17/10; resolver la contradicción de (c); usar «instancia de n8n» donde corresponda; y reescribir 2.2, 6.2, 7.2, 7.3 (PI-1) y 7.4 para describir el sistema evaluado: recolección periódica durante jornadas operadas, con arranque manual. Unificar el estado de OE1 y OE2 entre 5.8 y la Tabla 7.2.

**N-18 — El código y el esquema transcriptos no se presentan con la versión que operó, y los comentarios del propio código contradicen el capítulo de resultados \[MAYOR\]**

**Ubicación:** 4.4, 4.4.1, 4.6, 5.5.1, 5.6 y Anexos A, B.2, B.3 y C.

**(a) Versión del código.** B.2 afirma que el código transcripto «es el que efectivamente corrió durante la ventana B5». Sin embargo, el diccionario transcripto contiene las formas corregidas «secuestro de datos» y «cayeron los servidores», y 4.4.1 informa que esas erratas se corrigieron en la auditoría de la V5, después de la ventana. El tamaño declarado del workflow pasó además de 32.842 bytes (V4) a 32.843 bytes (V5). La corrección tiene efecto nulo y así se acepta, pero la transcripción es entonces una versión posterior a la ejecutada, y debe decirse.

**(b) Comentarios contradictorios.** La cabecera de Classify Dictionary, que se presenta como evidencia, dice que con MIN\_HITS \= 2 se detectaban 25 de 29 amenazas y que los falsos positivos pasaron de 1/21 a 3/21; la Tabla 5.11 y 4.4.1 informan 24 de 29 y una reducción de FP de 4 a 2\. Es la inconsistencia señalada en N-08 (f), que el cuerpo corrigió y el anexo conserva. Tampoco se presentó la tabla de transición caso por caso exigida en la V4, única forma de conciliar las dos explicaciones del cambio (umbral y retiro de «dni», frente a tres filas con clasificación heredada).

**(c) Esquema.** El Anexo A se presenta como el DDL real «conservado sin modificaciones», pero incorpora los cambios pedidos en la V4 (DEFAULT 'PENDIENTE' y UNIQUE) y usa CREATE TABLE IF NOT EXISTS: ejecutado sobre una base donde las tablas ya existían, no modifica nada. No se sabe, por lo tanto, si la base que operó durante la ventana tenía esas restricciones, y de eso depende la afirmación de idempotencia del análisis en el período evaluado (4.5 y 7.2).

**(d) Extractor de entidades.** La lista blanca contiene «afi p» en lugar de «afip»: el organismo con más peso en el vocabulario local nunca se reconoce. El filtro de dominios excluye solo los que comienzan con «reddit.com» y no sus subdominios (www\.reddit.com, old.reddit.com); y el dominio de cada dirección de correo se cuenta también como dominio. Ninguno de estos efectos se cuantifica en 5.6.

**(e) Solapamientos.** La auditoría de 4.4.1 analiza cuatro pares, pero el diccionario tiene al menos seis más dentro de una misma categoría: phishing / spear phishing, troyano / virus troyano, sim swap / sim swapping, session hijack / session hijacking, breach / breach notification y harvesting / credential harvest. Toda publicación que mencione «spear phishing» suma dos coincidencias. La conclusión de efecto nulo vale solo para los cuatro pares auditados.

**(f) Nodo no transcripto.** Parse Reddit Posts genera el centinela del lazo y aplica la normalización que afecta la privacidad (retiro de la línea de autoría y tratamiento de las menciones), pero no se transcribe.

**Corrección exigida:** identificar la versión transcripta (fecha y commit) y declarar sus diferencias con la ejecutada, o transcribir la ejecutada; conciliar o anotar los comentarios del código con los valores vigentes y publicar la tabla de transición caso por caso de la muestra del 30/09; reemplazar el Anexo A por el esquema extraído de la base de producción (pg\_dump \--schema-only, con fecha) o agregar la migración ALTER TABLE con la fecha en que se aplicó; declarar «afi p» como errata y cuantificar los efectos de (d) y (e) con el procedimiento de 4.4.1, publicando los diez dominios más frecuentes; transcribir Parse Reddit Posts.

**N-19 — Nuevas inconsistencias internas de cifras y estados \[MAYOR\]**

Las contradicciones siguientes son nuevas o persisten de la V4. Cada una es menor por separado; en conjunto afectan la confianza en el documento y deben corregirse antes de la defensa.

| \# | Tema | Contradicción | Corrección |
| :---- | :---- | :---- | :---- |
| 1 | Figura 4 y texto | 5.1: «El panel (a) no incluye el 03/10»; la figura corregida usa eje continuo e incluye el 03/10 en cero | Corregir el texto |
| 2 | Días de operación | Figura 1: «724 posts en 15 días completos»; 5.8: «16 días efectivos»; Tabla 7.2 y PI-1: «17 jornadas» | Unificar: 16 fechas con recolección en 17 días calendario |
| 3 | FP de r/DerechoGenial | 1.4: «3 falsos positivos del clasificador»; Tabla 5.12: 1 FP de esa comunidad con el clasificador vigente (persiste el ítem 7 de N-14) | Indicar la versión del clasificador |
| 4 | Notificación | 6.1: el aviso del 13/10 muestra que «la cadena de generación, registro y notificación funciona de punta a punta»; 5.4 y 7.2: envío deshabilitado, ninguna entrega | Corregir 6.1 |
| 5 | Estado de OE1 | 5.8: «cumplido»; Tabla 7.2: «cumplido con reparos» | Unificar (N-17) |
| 6 | Detecciones locales correctas | 5.7 y Tabla 5.9: tres; 6.2: «al menos dos»; 7.3 (PI-2): «se limita a dos detecciones locales verificadas» | Unificar o explicar por qué se cuentan dos |
| 7 | Modismos | 2.2 cita «caeron los servidores» como término del diccionario; Anexo C y B.2: «cayeron los servidores» | Corregir 2.2 |
| 8 | Uso de los índices | 4.2 asigna created\_utc a las series y ingested\_at a la latencia, y dos párrafos después lo inverso | Corregir |
| 9 | Columnas fuera del SET | 4.3: «las dos columnas restantes» (created\_utc e ingested\_at); fuera de la lista SET quedan cuatro (también subreddit\_id y author\_hash) | Corregir |
| 10 | Casos de la Tabla 5.14 | 4.4.1 e índice: «trece casos de la Tabla 5.14»; la tabla tiene diez filas (C-11 a C-13 solo aparecen en el texto de 5.4 y 5.7) | Incorporarlos o corregir la referencia |
| 11 | Categorías peor resueltas | 5.5: «no hay evidencia suficiente para afirmar ni negar su funcionamiento»; Tabla 5.10: 0 de 4 y 0 de 5 predicciones correctas en Filtración de Datos y Robo de Credenciales | Informar la precisión por categoría |
| 12 | Registro de ejecuciones | 5.3: cubre «del 05/10 al 18/10»; 5.1: el 18/10 sin ejecuciones; nota de la Figura 3: «382 corridas» durante la ventana (361 según 5.3) | Ver N-17 |
| 13 | Publicaciones previas a la rotación | 3.4: las 237 publicaciones «conservan» un hash y «no son vinculables entre sí»; E.3: se eliminaron el 01/10, y con una misma clave sí son vinculables entre sí | Corregir 3.4 |
| 14 | Cronología de umbrales | 1.6: el cambio a 80 % «es previo a la observación de resultados»; la cronología del mismo apartado lo fecha después de conocida la evaluación del 30/09 | Precisar «previo a la validación V5» |
| 15 | Anexo E | Cobertura «no alcanza» (fue retirada); remisiones a 5.3 y 5.3.2; IN-07 y C-25 sin definir | Ver Sección 4 (f) |
| 16 | Numeración y rótulos | 5.5.2 precede a 5.5.1; los epígrafes de la Figura 1 y de la Tabla 5.11 difieren del índice; 4.7: «base esi\_osint» | Corregir |

**Corrección exigida:** corregir cada ítem y hacer una pasada final de consistencia entre Resumen, Abstract, cuerpo, figuras y anexos.

# **6\. Hallazgos menores y de forma**

## **6.1. Estado de las observaciones menores de las instancias anteriores**

| ID | Observación | Estado V5 | Comentario |
| :---- | :---- | :---- | :---- |
| M-03 | Tamaños por estrato | **RESUELTO** | N₀ \= 554 y n₀ \= 182 informados |
| M-08 | Tamaño de las comunidades | **PARCIAL** | Se muestra 0 como dato (m-36) |
| m-17 | Herramientas generativas | **RESUELTO** | Identificadas en la Declaración |
| m-18 / m-29 | Sentencia de persistencia | **RESUELTO** | SQL con lista SET transcripta |
| m-19 | Atributos indirectos | **RESUELTO** | Superado por el riesgo residual ampliado |
| m-21 | DDL de alertas y anomalías | **RESUELTO CON OBSERVACIONES** | Corregido en el archivo; aplicación en producción no demostrada (N-18, c) |
| m-22 | Figuras | **RESUELTO CON OBSERVACIONES** | Defectos residuales (m-34) |
| m-23 | Tabla 5.4 y orden de la 5.6 | **RESUELTO** | DS y máximos informados |
| m-24 | Causas no identificadas | **RESUELTO** | Apagado del 03/10 y jornada del 17/10 explicados |
| m-25 | Referencias | **RESUELTO** | Ver H-10 |
| m-26 | Abstract | **RESUELTO** | «False discovery rate» |
| m-27 | Declaración de herramientas | **RESUELTO CON OBSERVACIONES** | Versión de opencode/big-pickle sin precisar; contradicción en N-16 (c) |
| m-28 | Índice multinivel | **NO RESUELTO** | Un solo nivel |
| m-30 | Denominación del trabajo | **NO RESUELTO** | «Trabajo Final de Inserción» frente a «Trabajo Final de Carrera» |

Las restantes observaciones menores de instancias anteriores (M-01, M-02, M-04 a M-07, M-09 a M-12, m-13 a m-16 y m-20) se mantienen resueltas.

## **6.2. Nuevas observaciones menores**

* **m-31.** Recálculo del motor (5.4.1). La línea base se calcula como la media de los mismos quince días que se evalúan, no como la ventana móvil de diez días previos que usa el motor; el 03/10 se excluye de la línea base «por no haber recolección», aunque por fecha de creación sí tiene publicaciones (y se lo cita como día de máximo de Malware); y el 17/10 queda truncado, porque las publicaciones creadas después del cierre de esa jornada no llegaron a ingerirse. La conclusión no cambia, pero el procedimiento debe describirse como variante del motor o rehacerse con una ventana móvil de días operados.

* **m-32.** Query Daily Counts compara ingested\_at (con zona) con un timestamp sin zona: el resultado depende del parámetro TimeZone de la sesión de PostgreSQL. Declarar ese parámetro o usar AT TIME ZONE explícito en los filtros. El comentario del nodo Registrar Anomalias («relanzar el nodo a mano para recuperar un día perdido») no es posible con una consulta anclada en now(): el 02/10 no podía recuperarse de ese modo.

* **m-33.** El desempate «por orden de gravedad» (4.4) no está fundamentado: en el código el orden es Phishing, Robo de Credenciales, Malware, Ransomware, Vulnerabilidades, Filtración de Datos, Infraestructura y Ataques, Hacktivismo e Ingeniería Social. Justificarlo o describirlo como orden de declaración.

* **m-34.** Figuras. En la Figura 3 los rótulos de los dos carriles se superponen. En la Figura 1 el texto de «Controles transversales» excede el recuadro, las líneas de continuación aparecen como viñetas nuevas y se conserva «15 días completos». En la Figura 4 (b) la etiqueta «79» queda cortada. Los epígrafes de la Figura 1 y de la Tabla 5.11 difieren del índice.

* **m-35.** La Hoja de firmas figura como sección 4.7, dentro del Capítulo 4, sin firmas y con la errata «esi\_osint». Ubicarla en los preliminares o junto al Anexo E.

* **m-36.** La Tabla 5.1 muestra 0 suscriptores «al alta» para las tres comunidades, como si fuera un dato. Reemplazar por «no disponible en la fuente» o informar el tamaño con fecha desde otra fuente (M-08).

* **m-37.** En HMAC Anonymize, String(undefined) produce el texto «undefined»: todas las publicaciones sin autor compartirían un mismo hash. Declarar si hubo casos y cómo se tratan.

* **m-38.** 5.6 transcribe el patrón de CVE como cve-\\d{4}\\d{4,7}, sin el guion que sí tiene el código. Corregir.

# **7\. Verificación de consistencia numérica**

Se recalcularon todas las cifras verificables de la V5. Se deja constancia de lo que resultó correcto para que el equipo no revise lo que ya está bien.

| Verificación | Resultado | Detalle |
| :---- | :---- | :---- |
| Tablas 5.1 a 5.3 | **CORRECTO** | Sin cambios respecto de la V4; sumas y porcentajes verificados |
| Tabla 5.4 — subconjuntos | **CORRECTO** | 126 \+ 311 \= 437; 97/126 \= 77,0 %; 301/311 \= 96,8 %; 374/409 \= 91,4 %; 254/311 \= 81,7 %; 105 \+ 8 \+ 13 \= 126 |
| Fracción de operación | **INCONSISTENTE** | 4.929/25.920 \= 19,0 %, pero 25.920 min son 18 días (la ventana tiene 17: 24.480 min) y el registro cubre desde el 05/10 (N-17) |
| Tamaño de muestra | **CORRECTO** | p \= 0,227 y e \= 0,05: n \= 269,6; con N \= 554, n₀ \= 181,6 → 182 |
| Kappa de Fleiss | **CORRECTO** | (0,700 − 0,389)/(1 − 0,389) \= 0,509 |
| Tabla 5.7 | **CORRECTO** | 144 \+ 26 \= 170; 30 \+ 152 \= 182; total 352 |
| Tabla 5.8 | **CORRECTO** | Precisión 144/170 \= 0,847, IC \[0,784; 0,898\]; omisión 30/182 \= 0,165, IC \[0,114; 0,227\]; sensibilidad 0,612, IC \[0,534; 0,695\]; F1 0,711, IC \[0,635; 0,783\]; FDR IC \[0,102; 0,216\]; 144 \+ 91,3 \= 235 (32,5 %) |
| Tablas 5.9 y 5.9.b — aritmética | **CORRECTO** | 60 \+ 81 \+ 3 \= 144; 6 \+ 16 \+ 4 \= 26; 29 \+ 18 \+ 135 \= 182; 15 \+ 13 \+ 2 \= 30 |
| Tablas 5.9 y 5.9.b — interpretación | **INCORRECTO** | La omisión del estrato negativo se lee como complemento de la sensibilidad; sensibilidad estimada en r/devsarg ≈ 0,32 (N-15) |
| Estimación postestratificada | **OBSERVACIÓN** | Con pesos por comunidad: ≈ 229 amenazas y sensibilidad ≈ 0,63, frente a 235 y 0,612; misma conclusión |
| Tabla 5.10 | **CORRECTO** | Marginales del clasificador iguales a la Tabla 5.3 (79, 61, 12, 5, 4, 4, 3, 2 y 182); FP \= 26; FN \= 30; diagonal 116 \+ 152 \= 268 (76,1 %) |
| Tabla 5.11 | **CORRECTO** | 24/28 \= 0,857; 24/29 \= 0,828; 27/29 \= 0,931; F1 0,842 y 0,931 |
| Comentarios del Código B.2 | **INCONSISTENTE** | 25/29 y FP de 1/21 a 3/21, frente a 24/29 y FP de 4 a 2 (N-18, b) |
| Recálculo del motor | **CORRECTO CON OBSERVACIÓN** | λ \= 1,40 / 1,27 / 0,40 / ≤ 0,20 → umbrales 5 / 4 / 3 / 3; suma de P(X ≥ u \| λ) sobre 105 evaluaciones \= 0,954. Línea base intra-muestra (m-31) |
| Tablas 5.5 y 5.6 | **CORRECTO** | Sin cambios; 6 disparos y 112 evaluaciones |
| Payload publicado | **CORRECTO** | Ventana 2026-10-01T03:00Z \= 00:00 local del 01/10; coincide con el disparo de Infraestructura y Ataques |
| Tabla 5.13 | **CORRECTO** | 162 \+ 51 \+ 73 \= 286; CVE 0 \+ 27 \+ 5 \= 32; dominios 27 \+ 9 \+ 41 \= 77; productos 150 \+ 23 \+ 47 \= 220; 242 \+ 93 \+ 47 \+ 10 \+ 8 \= 400; 123/128 \= 96,1 % |
| Auditoría de términos genéricos | **CORRECTO** | (170 − 159)/170 \= 6,5 % |
| Diccionario (Anexo C y Código B.2) | **CORRECTO** | 22 \+ 29 \+ 24 \+ 15 \+ 30 \+ 29 \+ 16 \+ 16 \+ 20 \= 201, recontado sobre el código |
| Solapamientos del diccionario | **INCOMPLETO** | Cuatro pares auditados; al menos seis adicionales (N-18, e) |
| Throughput operativo | **CORRECTO** | 724 / 408 h \= 1,77 posts/h |

# **8\. Rúbrica de evaluación y calificación**

| Dimensión | Peso | V2 | V3 | V4 | V5 | Fundamento V5 |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Estructura y forma académica | 10 % | 6,0 | 5,0 | 8,0 | 8,0 | Anexos A–E completos, código y SQL transcriptos, figuras corregidas; índice de un nivel, numeración y firmas fuera de lugar (m-28, m-34, m-35) |
| Marco teórico y estado del arte | 15 % | 8,0 | 6,0 | 8,0 | 8,5 | Brecha reformulada al alcance real, referencias normativas corregidas, antecedente citado como inédito; errata en los modismos (N-19) |
| Diseño metodológico | 20 % | 7,0 | 6,0 | 6,0 | 7,5 | Validación sobre el corpus con censo, muestreo reproducible, cegamiento, pesos e IC; referencia de un anotador en el 86 % de los casos y uso de herramientas sin precisar (N-16) |
| Desarrollo del artefacto | 20 % | 4,5 | 4,5 | 7,5 | 8,0 | Código, SQL y DDL transcriptos; motor y diccionario auditados; versión transcripta distinta de la ejecutada, errata del extractor y solapamientos (N-18) |
| Resultados y validez | 20 % | 4,5 | 5,0 | 6,0 | 7,5 | Resultados trazables y verificados, incumplimientos informados, latencia explicada, motor recalculado; lectura por idioma invertida y régimen de operación inconsistente (N-15, N-17) |
| Discusión y conclusiones | 10 % | 7,5 | 6,5 | 7,0 | 7,0 | Discusión franca y limitaciones exhaustivas; conclusiones que describen un sistema continuo y un aporte local que la evidencia no sostiene (N-15, N-17, N-19) |
| Aspectos legales y éticos | 5 % | 5,0 | 7,0 | 6,5 | 7,5 | Códigos de caso, riesgo residual ampliado, «irreversible» retirado; títulos literales, menciones y errores de 3.4 (N-10, H-01) |
| PROMEDIO PONDERADO | 100 % | 6,0 | 5,5 | 6,9 | 7,8 | Ascenso de 0,9 puntos respecto de la V4 (valor exacto 7,75) |

**CALIFICACIÓN DE ESTA INSTANCIA: 7,8 / 10**

**Condición: APROBADO CON CORRECCIONES OBLIGATORIAS. VERSIÓN FINAL V6.**

La nota sube 0,9 puntos porque la V5 cerró, con o sin observaciones, cuatro de los cinco ítems bloqueantes y los ocho de prioridad alta de la V4. El cambio decisivo es la validación: el desempeño del clasificador se mide ahora sobre el corpus evaluado, con un diseño correcto y cifras verificadas, y los resultados desfavorables —sensibilidad, F1 y acuerdo por debajo de lo comprometido— se informan como tales. A eso se suman la explicación de la latencia, el recálculo del motor, la transcripción del código y la declaración de trazabilidad.

La nota no alcanza el rango de 8,0 a 8,5 proyectado en la V4, que suponía el cierre de los cinco ítems bloqueantes. El quinto —las contradicciones internas— quedó parcial y aparecieron otras (N-19). Pesan además dos problemas de interpretación que alteran las conclusiones: la lectura del desempeño por idioma (N-15) y la ausencia del régimen de operación en la discusión y las conclusiones (N-17). La composición de la referencia (N-16) y la versión del código transcripto (N-18) completan el cuadro. Ninguno exige recolectar ni etiquetar de nuevo: se resuelven con el material que el equipo ya tiene.

**Proyección:** el cierre de los cinco ítems bloqueantes y de los de prioridad alta de la Sección 9 ubica el trabajo en el rango de 8,2 a 8,6 en la V6. Esta calificación evalúa el documento y no prejuzga lo que resuelva la instancia académica sobre la declaración del Anexo E (Sección 4).

**La defensa se habilitará con la V6, una vez cerrados los ítems bloqueantes 1 a 5 y conocida la resolución de la instancia académica sobre la declaración del Anexo E.**

# **9\. Plan de correcciones exigido para la V6**

Ordenado por prioridad de ejecución. Los ítems 1 a 5 son condición de habilitación a defensa.

| \# | Acción requerida | Hallazgo | Prioridad |
| :---- | :---- | :---- | :---- |
| 1 | Formalizar la declaración: original con firmas manuscritas o digitales de los tres autores y de la dirección del trabajo, entregado por canal institucional; corregir el ciclo de vida de la Tabla E.2 (publicaciones existentes al 30/09 por comunidad y cantidad eliminada el 01/10); precisar el alcance a la V3; corregir E.1 y E.4; definir IN-07 y C-25 | N-07 | **Bloqueante** |
| 2 | Declarar la composición real de la referencia (50 casos de consenso y 302 de un anotador) e identificar al anotador; medir su coincidencia con el consenso y el rango de las métricas según la etiqueta; precisar la intervención de herramientas generativas en el etiquetado | N-16 | **Bloqueante** |
| 3 | Estimar la sensibilidad por comunidad e idioma con pesos propios e intervalos; corregir la lectura del léxico local en 5.5, 6.1, 6.2, 6.4 y 7.3 | N-15 | **Bloqueante** |
| 4 | Tabla del régimen de operación por día; recalcular la fracción de operación; explicar las evaluaciones del 16/10 y del 17/10; trasladar la operación intermitente a 2.2, 6.2, 7.2, 7.3 y 7.4; corregir las 16 contradicciones de N-19 y hacer una pasada final de consistencia | N-17, N-19, N-14 | **Bloqueante** |
| 5 | Entregar al tribunal la copia congelada evidencia\_v5.zip, o el acceso de lectura al repositorio, para verificar el SHA-256 declarado y cotejar el Anexo B con el artefacto | H-07 | **Bloqueante** |
| 6 | Identificar la versión del código transcripto; conciliar los comentarios de B.2; publicar la tabla de transición caso por caso del 30/09; presentar el esquema extraído de producción o la migración fechada; transcribir Parse Reddit Posts | N-18 (a–c, f), N-08 | **Alta** |
| 7 | Extractor: declarar «afi p» como errata; cuantificar subdominios de Reddit y doble conteo de dominios; publicar los diez dominios más frecuentes | N-18 (d), N-06 | **Alta** |
| 8 | Completar la auditoría de solapamientos con su efecto medido; justificar el desempate | N-18 (e), m-33 | **Alta** |
| 9 | Privacidad: retirar los títulos literales de 5.4; decidir y documentar el tratamiento de las menciones; mantener la correspondencia fuera de todo repositorio público; corregir 3.4 | N-10, H-01 | **Alta** |
| 10 | Recálculo del motor con ventana móvil de días operados, o declararlo como variante; aclarar el tratamiento del 03/10 y del 17/10 | m-31, N-11 | **Media** |
| 11 | Zona horaria de la consulta de conteo y comentario sobre la recuperación de días | m-32 | **Media** |
| 12 | Figuras, epígrafes, numeración de secciones y ubicación de la hoja de firmas | m-34, m-35, H-11 | **Media** |
| 13 | Índice multinivel; denominación del trabajo; suscriptores; latencia de consulta analítica; restantes observaciones | m-28, m-30, m-36 a m-38, H-12, m-27 | **Media** |

*Devolución emitida por el tribunal evaluador — Tecnicatura Universitaria en Programación, UTN Facultad Regional Mendoza. Documento de uso académico interno, destinado a los autores y a la dirección del trabajo.*