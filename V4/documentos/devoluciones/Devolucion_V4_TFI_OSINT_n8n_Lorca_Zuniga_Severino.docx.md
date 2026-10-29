**UNIVERSIDAD TECNOLÓGICA NACIONAL — FACULTAD REGIONAL MENDOZA**

Tecnicatura Universitaria en Programación — Tribunal Evaluador de Trabajos Finales

**DEVOLUCIÓN DE AUDITORÍA ACADÉMICA**

*Cuarta instancia de revisión (V4)*

| Título del TFI | Sistema automatizado de monitoreo de foros y redes sociales para la detección de tendencias y alertas en ciberseguridad en Argentina mediante OSINT y n8n |
| :---- | :---- |
| Autores | Valentino Lorca — Jerónimo Zúñiga — Enzo Severino |
| Directores | Prof. Alberto Cortez — Prof. Ariel Enferrel |
| Archivo auditado | tesis\_v4.pdf (75 páginas, 4 figuras embebidas) |
| Instancia | V4 — revisión sobre versión reconstruida, con cotejo contra la devolución V3 del 22/09/2026 |
| Fecha de devolución | 20 de octubre de 2026 |
| Calificación V3 (referencia) | 5,5 / 10 |
| Calificación de esta instancia | **6,9 / 10 — APROBADO CON CORRECCIONES OBLIGATORIAS. REENTREGA V5** |
| Habilitación a defensa | Condicionada a la V5: se habilita con el cierre de los 5 ítems bloqueantes de la Sección 9\. La declaración del ítem 1 es requisito previo indispensable |

# **1\. Alcance y método de la auditoría**

La presente devolución audita la versión 4 del documento con dos propósitos. Primero, verificar uno por uno el estado de los 17 hallazgos de la V2 (H-01 a H-17), de los 6 hallazgos nuevos de la V3 (N-01 a N-06) y de las observaciones menores (M-01 a M-12 y m-13 a m-20). Segundo, auditar la V4 como pieza autónoma, con las mismas cinco dimensiones de las instancias anteriores: consistencia numérica interna, trazabilidad entre objetivos y evidencia, solidez metodológica de las métricas, correspondencia entre cuerpo y anexos, y cumplimiento formal (APA 7.ª edición y estructura de TFI).

El estado de cada hallazgo se clasifica como **RESUELTO**; **RESUELTO CON OBSERVACIONES** (la objeción de fondo está cerrada y persisten ajustes no bloqueantes); **PARCIAL**; o **NO RESUELTO**. Los hallazgos surgidos en esta instancia continúan la numeración: N-07 a N-14 (críticos y mayores) y m-21 a m-30 (menores).

Se mantiene la restricción de las instancias anteriores: la auditoría se realiza exclusivamente sobre el documento entregado. La V4 remite a unos quince archivos de evidencia y a un repositorio, pero no informa URL ni medio de acceso, de modo que ninguno pudo consultarse. Se inspeccionó la estructura del PDF (cuatro imágenes embebidas a 200 ppi), se revisaron las figuras y se recalcularon todas las cifras verificables, incluidos los intervalos de confianza exactos y los umbrales de Poisson del motor (Sección 7).

# **2\. Avances reconocidos respecto de la V3**

La V4 es un documento sustancialmente distinto y mejor que la V3, y corresponde reconocerlo expresamente:

* Se reconstruyó sobre la base textual de la V2, como se exigió: 75 páginas, con los Capítulos 3 y 4 más desarrollados que en la V2 y con el contenido perdido restituido (protocolo de validación, entorno de ejecución, tabla de atributos, ejemplos de modismos, recomendaciones priorizadas). N-03 queda cerrado.

* Los resultados provienen de un sistema real y de datos fechados. Todas las sumas y porcentajes de las Tablas 5.1 a 5.6 se verificaron sin errores.

* La latencia se midió desde la base (ingested\_at − created\_utc), con n, media, P50 y P95, y se declaró NO CUMPLIDA sin mover el umbral ni redefinir la métrica. Es la corrección que la V3 pidió para N-01.

* La métrica de cobertura se retiró de manera consistente del Resumen, del Capítulo 5 y del Capítulo 7, con nota metodológica (H-05).

* Las métricas se definen con fórmula explícita (3.3.5), se publica la matriz binaria y se informan intervalos de confianza exactos, verificados por este tribunal. El cambio de umbrales entre versiones se declara y se justifica (H-04, N-05).

* El motor de anomalías se rediseñó sobre ventanas diarias con cuantil de Poisson y piso absoluto —exactamente las alternativas sugeridas en la V3— y persiste también las decisiones negativas (H-03, N-04).

* El DDL incorpora nlp\_score con restricción CHECK, entities en JSONB y las tablas anomalias y alertas; adopta RESTRICT; elimina pg\_trgm; y la Tabla 4.2 vuelve a reflejar el esquema (N-06, H-16, m-20).

* Las cuatro figuras son reales, el índice de tablas y figuras existe y la paginación de los diez capítulos, veintidós tablas y cuatro figuras es correcta (H-11, H-14).

* Existen los Anexos C (diccionario de 201 términos, recuento verificado) y D (estructura del repositorio).

* La seudonimización se describe como HMAC-SHA-256 con clave por despliegue, se documenta la configuración de n8n que la habilita, el procedimiento de rotación y el riesgo residual (H-01).

* El contraste con Dengra y Rivas (2026) es serio, en seis dimensiones y con la Tabla 6.1; todas las referencias se citan; Liao et al. (2016) se usa como antecedente; se restituyeron los modismos (H-09, H-10, m-14).

* El documento distingue con honestidad el protocolo diseñado del ejecutado, declara un único anotador, el sorteo no reproducible y dos defectos silenciosos del sistema. Esa actitud se valora.

Sin embargo, la V4 reemplaza íntegramente el corpus y los resultados de las versiones anteriores sin declarar el origen de las cifras retiradas (N-07), y la nueva evidencia muestra que la validación del clasificador no mide el desempeño sobre el corpus evaluado (N-08). A eso se suman problemas de interpretación y de consistencia interna (N-09 a N-14). El balance se explica en la Sección 8\.

# **3\. Estado de los hallazgos de la V3**

## **3.1. Tablero de seguimiento**

| ID | Hallazgo | Estado V4 | Síntesis |
| :---- | :---- | ----- | :---- |
| **H-01** | Seudonimización de autores | **RESUELTO CON OBSERVACIONES** | HMAC y configuración documentados; persiste «irreversible» |
| **H-02** | Alcance de OE6 (alertas) | **RESUELTO CON OBSERVACIONES** | Alcance explícito; objetivo general y título sin ajustar |
| **H-03** | Motor de anomalías (OE5) | **RESUELTO CON OBSERVACIONES** | Formalizado y con disparos; eficacia no demostrada (N-11) |
| **H-04** | Fórmula de FP y matriz | **RESUELTO CON OBSERVACIONES** | Fórmulas y matriz binaria; falta matriz por categoría |
| **H-05** | Métrica de cobertura | **RESUELTO** | Retirada de forma consistente |
| **H-06** | Throughput | **PARCIAL** | Criterio de capacidad evaluado con la demanda |
| **H-07** | Reproducibilidad y anexos | **PARCIAL** | Anexos C y D presentes; sin URL ni SQL |
| **H-08** | Fuentes del Capítulo 6 | **RESUELTO** | Cifras externas retiradas con el corpus anterior |
| **H-09** | Ejemplos de modismos | **RESUELTO** | Restituidos en 2.2 (ver N-12) |
| **H-10** | Referencias | **RESUELTO** | Todas citadas; contraste con el antecedente |
| **H-11** | Figuras | **RESUELTO CON OBSERVACIONES** | Cuatro figuras reales; defectos de legibilidad |
| **H-12** | Medidas de dispersión | **RESUELTO CON OBSERVACIONES** | n, P50 y P95; falta DS en subconjuntos |
| **H-13** | Validación endógena | **NO RESUELTO** | De tres evaluadores declarados a uno (N-08) |
| **H-14** | Índice general | **RESUELTO CON OBSERVACIONES** | Paginación correcta; índice de un solo nivel |
| **H-15** | Anexo B (workflow) | **PARCIAL** | Inventario sin código de los nodos |
| **H-16** | Modelo relacional | **RESUELTO** | Tabla 4.2 restituida; pg\_trgm eliminada |
| **H-17** | Puntuación y casos | **RESUELTO CON OBSERVACIONES** | Función definida; se publican IDs (N-10) |
| **N-01** | Latencia vs. scheduler | **RESUELTO CON OBSERVACIONES** | Medida y declarada no cumplida; explicación errónea (N-09) |
| **N-02** | Fila «No relevante / FP» | **RESUELTO CON OBSERVACIONES** | Rotulada como salida del clasificador |
| **N-03** | Contracción del documento | **RESUELTO** | Reconstruido sobre la V2 |
| **N-04** | Umbral μ \+ 2σ | **RESUELTO CON OBSERVACIONES** | Poisson diario con piso; ver N-11 |
| **N-05** | Criterios a priori | **RESUELTO CON OBSERVACIONES** | Cambios declarados; redundancia en el recuento |
| **N-06** | Modelo de datos incompleto | **RESUELTO CON OBSERVACIONES** | DDL completo; entidades sin resultados |

**Síntesis:** 6 resueltos, 13 resueltos con observaciones, 3 parciales y 1 no resuelto. De los ocho ítems bloqueantes del plan de la V3, siete quedan cerrados con o sin observaciones (ítems 1, 2, 3, 5, 6, 7 y 8\) y uno queda parcial (ítem 4: acceso al workflow, al código y al repositorio). El único hallazgo no resuelto (H-13) no empeoró por omisión sino por sinceramiento: el documento ahora declara un único anotador donde antes declaraba tres.

## **3.2. Detalle por hallazgo**

**H-01 — Seudonimización de autores \[RESUELTO CON OBSERVACIONES\]**

**Corregido:** la Sección 3.4 describe HMAC-SHA-256 con clave secreta provista por variable de entorno (OSINT\_HMAC\_KEY), con aborto del flujo si falta; documenta NODE\_FUNCTION\_ALLOW\_BUILTIN=crypto y N8N\_BLOCK\_ENV\_ACCESS\_IN\_NODE=false; incorpora el procedimiento de rotación y reconoce que el dato seudonimizado sigue siendo dato personal.

**Persiste:** (a) la expresión «seudonimización irreversible» aparece en el Resumen, en el Abstract («irreversible pseudonymization»), en 2.2 y en el encabezado de la medida en 3.4. Con HMAC, quien conserva la clave puede recalcular el hash de cualquier nombre de usuario candidato —y esos nombres son públicos y enumerables desde la misma fuente—, de modo que la operación es reversible por comparación para el custodio de la clave. (b) El código del nodo HMAC Anonymize no está transcripto: no puede verificarse que el valor original se descarte. (c) No se indica si la clave anterior a la rotación del 26/09 fue destruida; si se conserva, la «no vinculación entre períodos» no se sostiene.

**Exigido para V5:** eliminar «irreversible» en todo el documento; transcribir el código del nodo (Anexo B); declarar el destino de la clave rotada.

**H-02 — Objetivo OE6 (alertas) \[RESUELTO CON OBSERVACIONES\]**

**Corregido:** 4.5, 5.4, 5.7 y 7.2 describen con precisión lo implementado: nodo de Telegram presente, envío deshabilitado, seis alertas registradas en estado PENDIENTE; OE6 figura como parcial y el Resumen y el Abstract lo reflejan.

**Persiste:** el título y el objetivo general conservan «alertas tempranas». Con un motor que corre una vez por día a las 12:05 y evalúa el día local anterior, un hecho ocurrido al comienzo de un día genera su aviso unas 36 horas después aun con latencia de ingesta nula; con el P95 medido de 22,9 horas, la promesa de alerta temprana no está sostenida por el diseño. No se muestra el contenido (payload) de ninguna alerta registrada. La frase «la credencial se asigna por interfaz» (Anexo B) contradice la regla de 4.6 de no modificar el flujo desde la interfaz.

**Exigido para V5:** ajustar el objetivo general (y evaluar el título) a lo que el sistema hace —avisos diarios— o justificar «temprana» con la latencia de alerta; incluir un payload de alerta enmascarado; aclarar el manejo de la credencial.

**H-03 — Objetivo OE5 (motor de anomalías) \[RESUELTO CON OBSERVACIONES\]**

La Sección 4.5 formaliza conteo, línea base, umbral max(q95(λ) \+ 1, 3), decisión y persistencia, y las Tablas 5.5 y 5.6 informan 112 evaluaciones y 6 disparos, con la corrección de la recurrencia documentada. La especificación pedida está cumplida; lo que no está demostrado es la eficacia del motor, que sin embargo se declara CUMPLIDA. Ver N-11.

**H-04 — Fórmula y matriz de confusión \[RESUELTO CON OBSERVACIONES\]**

Las fórmulas están en 3.3.5, la matriz binaria en la Tabla 5.7 y los intervalos exactos en la Tabla 5.8 (verificados). Falta la matriz por categoría (nueve categorías más «No relevante») que se pidió: el documento solo informa 42/50 de acierto exacto y cuatro desacuerdos en la Tabla 5.10. Publicarla en anexo para la nueva muestra de control (N-08).

**H-05 — Métrica de cobertura \[RESUELTO\]**

Retirada de 1.6 con nota metodológica y ausente del Resumen, del Capítulo 5 y del Capítulo 7, conforme a la alternativa admitida en la V3.

**H-06 — Throughput \[PARCIAL\]**

**Corregido:** se describe el entorno (dos contenedores en un único equipo, n8n 2.40.6 en modo regular, PostgreSQL 18, sin aislamiento de CPU ni memoria) y se declara la limitación.

**Persiste:** (a) el criterio mide capacidad («throughput del pipeline ≥ 1.000 posts/hora») y la V4 informa demanda operativa (1,8 posts/hora, limitada por la fuente) para declararlo NO CUMPLIDO. Una demanda baja no demuestra una capacidad insuficiente: el criterio no fue evaluado, no fue incumplido. La propia Sección 5.7 admite que «el sistema no es el factor limitante». (b) La capacidad nominal de 1.200 posts/hora es aritmética, no medida. (c) El Resumen dice que el criterio «no se verifica»; las Tablas 1.1, 5.12 y 7.1 dicen NO CUMPLIDO. (d) El banco de pruebas de 1.450 posts/hora de la V2 y la V3 desaparece sin explicación (N-07).

**Exigido para V5:** medir la capacidad mediante una reproducción controlada (reprocesar los 724 textos almacenados por los nodos de transformación, clasificación y persistencia, informando n, posts/hora, dispersión y características del equipo) o clasificar el criterio como NO EVALUADO en todo el documento y excluirlo del recuento de 7.2.

**H-07 — Reproducibilidad y anexos \[PARCIAL\]**

**Corregido:** existen los Anexos C y D; todas las cifras del Capítulo 5 se atribuyen a consultas fechadas; la tabla de clasificación tiene recuentos exactos y coherentes.

**Persiste:** (a) no hay URL de repositorio ni medio de acceso: el Anexo D es un árbol de directorios y todos los archivos de evidencia citados son inaccesibles para el tribunal. (b) El SQL de las consultas Q1 a Q15 no figura en el documento, aunque la V3 exigió «la consulta SQL con su salida». (c) No se explica el reemplazo del corpus de las versiones anteriores (N-07).

**Exigido para V5:** URL accesible para el tribunal o copia congelada (ZIP) con su hash SHA-256 declarado en el documento; anexo con el SQL de las consultas que producen las Tablas 5.1 a 5.6; cumplimiento de N-07.

**H-08 — Fuentes de las cifras del Capítulo 6 \[RESUELTO\]**

Las comparaciones con CABASE y Fortinet se retiraron junto con el corpus anterior; el Capítulo 6 ya no usa cifras externas sin fuente.

**H-09 — Ejemplos de modismos \[RESUELTO\]**

Restituidos en 2.2 e incorporados al diccionario. Dos de ellos están mal escritos en el código y nunca coinciden (N-12).

**H-10 — Referencias bibliográficas \[RESUELTO\]**

Las dieciséis referencias se citan en el cuerpo; Zong et al. se corrige a 2019 (NAACL) con DOI; el contraste con el antecedente local es adecuado. Ajustes formales pendientes en m-25.

**H-11 — Figuras \[RESUELTO CON OBSERVACIONES\]**

Cuatro figuras reales y un índice de figuras. Persisten defectos de legibilidad (m-22) y una contradicción sobre el estado del workflow entre la Figura 1 y la Figura 3 (N-14).

**H-12 — Medidas de dispersión \[RESUELTO CON OBSERVACIONES\]**

La Tabla 5.4 informa n, media, P50, P95, máximo y proporción por encima de 5 minutos. Falta el desvío estándar de los dos subconjuntos operativos y el máximo de la fila «desde el 02/10», que además no se comenta. La latencia de consulta analítica de la V2 desapareció: informarla o declarar que no se midió.

**H-13 — Validación endógena del clasificador \[NO RESUELTO\]**

La V3 declaraba tres evaluadores y un Kappa de Fleiss de 0,78. La V4 declara un único anotador «sin formación formal en ciberseguridad y con asistencia de herramientas» (6.3) y kappa no calculable, y no hay evaluador externo. El sinceramiento se valora, pero la debilidad que la V3 pedía reducir es ahora mayor. Se trata en N-08 y, en cuanto a la cifra de 0,78, en N-07.

**H-14 — Índice general \[RESUELTO CON OBSERVACIONES\]**

La paginación de los diez capítulos, las veintidós tablas y las cuatro figuras es correcta. El índice general tiene un solo nivel y omite el Resumen, el Abstract, la Declaración de autoría y las Siglas (m-28).

**H-15 — Anexo B \[PARCIAL\]**

**Corregido:** inventario de los 17 nodos, Figura 3 generada desde el archivo exportado y referencia a B\_workflow.json (32.842 bytes).

**Persiste:** el JSON solo existe en el repositorio inaccesible, y el documento no transcribe el código de ninguno de los seis nodos de código ni el SQL de los nodos de PostgreSQL. La lógica que produce todos los resultados —normalización, clasificación, entidades y motor— solo se describe en prosa, y un caso observado sugiere que la prosa no coincide con el código (N-12, d).

**Exigido para V5:** Anexo B con el código de HMAC Anonymize, Classify Dictionary, Extract Entities y Anomaly Engine, y el SQL de Upsert Posts, Query Daily Counts y Registrar Anomalias y Alertas.

**H-16 — Modelo relacional \[RESUELTO\]**

La Tabla 4.2 es espejo del DDL, pg\_trgm y el índice GIN se eliminaron con fundamento y la denormalización está declarada.

**H-17 — Casos y puntuación \[RESUELTO CON OBSERVACIONES\]**

La función min(1, coincidencias/4) está definida y justificada, y la escala es fija. Sin embargo, la Tabla 5.11 y la Sección 5.4 publican identificadores de plataforma y títulos literales (N-10).

**N-01 — Latencia extremo a extremo \[RESUELTO CON OBSERVACIONES\]**

El intervalo está definido (created\_utc → ingested\_at), se midió desde la base con n \= 724 y n \= 437, y el criterio se declaró NO CUMPLIDO. La explicación causal del incumplimiento es incorrecta: ver N-09.

**N-02 — Fila residual de la tabla de clasificación \[RESUELTO CON OBSERVACIONES\]**

La fila se rotula como salida residual del clasificador y el texto aclara que no equivale a ausencia de amenaza. No hay estimación de amenazas reales: la V4 argumenta, con razón, que la muestra de control no proviene del corpus B5. Ese argumento traslada la exigencia a N-08: con una muestra extraída de B5 la estimación es posible y debe hacerse.

**N-03 — Contracción del documento \[RESUELTO\]**

Documento reconstruido sobre la V2, con 75 páginas y el contenido perdido restituido.

**N-04 — Umbral del motor de anomalías \[RESUELTO CON OBSERVACIONES\]**

Ventanas diarias, cuantil de Poisson y piso de tres reemplazan μ \+ 2σ sobre ventanas horarias, y se informan los disparos reales. Los problemas de la nueva formulación se tratan en N-11.

**N-05 — Criterios a priori \[RESUELTO CON OBSERVACIONES\]**

**Corregido:** el cambio de 82 % / 18 % a 80 % / 20 % se declara y se justifica, el F1 se incorpora a 1.6 y se informan intervalos exactos.

**Persiste:** (a) la tasa de falsos descubrimientos se mantiene como criterio separado aunque la propia nota de 1.6 reconoce que es el complemento de la precisión; las Tablas 5.12 y 7.1 y la Sección 7.2 cuentan «cuatro se alcanzaron» cuando son tres criterios distintos. (b) La frase «los criterios no fueron modificados después de observar los resultados» contradice la nota que declara una modificación hecha después de conocerse los resultados de la V3. (c) El F1 se incorporó en la V4: es previo a la ventana B5, no al proyecto.

**Exigido para V5:** presentar la tasa de falsos descubrimientos como complemento informativo, no como criterio; precisar cuándo se fijó cada umbral.

**N-06 — Modelo de datos \[RESUELTO CON OBSERVACIONES\]**

El DDL incorpora nlp\_score, entities, anomalias y alertas, y la extracción de entidades se describe (cinco familias por expresión regular). El Capítulo 5 no informa ningún resultado de esa extracción —cuántas publicaciones tienen entidades, cuántos CVE, ejemplos, errores—, de modo que el componente de entidades de OE4 no tiene evidencia. Tampoco se explica cómo una expresión regular reconoce «nombres de productos o tecnologías». Ver además m-21 sobre la tabla alertas.

# **4\. Nuevos hallazgos críticos**

**N-07 — Sustitución integral del corpus y de los resultados sin declaración de trazabilidad entre versiones \[CRÍTICO\]**

**Ubicación:** nota de versión de la portada, 1.4, 3.1, 3.3, 5.1 y 6.2.

**Evidencia:** las afirmaciones de la V4 sobre el sistema real son incompatibles con los resultados que la V3 presentó como obtenidos:

| Elemento | V3 (evaluada el 22/09/2026) | V4 (20/10/2026) |
| :---- | :---- | :---- |
| **Corpus** | 8.240 publicaciones en 181 días | 724 publicaciones en 17 días; primer registro el 01/10/2026 |
| **Comunidades** | r/argentina, r/devsarg, r/derechogenial | r/devsarg, r/netsec, r/Malware |
| **Comentarios** | 42.150 | Cero: «las fuentes RSS/Atom no exponen el árbol de comentarios» y el endpoint JSON respondió 403 |
| **Etiquetado** | Tres evaluadores; Kappa de Fleiss \= 0,78 | Un anotador; «kappa no calculable» |
| **Latencia E2E** | Media 4,2 min; P95 4,9 min | P95 1.376,2 min |
| **Throughput** | 1.450 posts/hora en banco de pruebas | No medido |
| **Precisión** | 82 % | 93,1 % (otra muestra, otro clasificador) |

**Problema:** 42.150 comentarios no pueden provenir de una fuente que no expone comentarios; un Kappa de Fleiss de tres evaluadores no puede coexistir con un único anotador; un corpus de 181 días no puede provenir de un pipeline cuyo primer registro es del 01/10/2026 y cuya fuente devuelve como máximo 100 elementos recientes por comunidad. La portada dice que la V4 «incorpora el sistema efectivamente implementado y los datos realmente relevados», y 3.3 recuerda que la evaluación previa penalizó «presentar como ejecutado un diseño que no se había ejecutado». La V4 admite así, implícitamente, que los resultados de la V2 y la V3 no provenían de mediciones, pero no dice de dónde provenían. Tampoco documenta el ciclo de vida de los datos entre el corpus B4 (24/09, descartado), el corpus del que se extrajo la muestra del 30/09 (con r/DerechoGenial y r/argentina) y el B5 (primer registro el 01/10; «no hay publicaciones anteriores»), lo que supone una depuración de la base no declarada.

**Por qué es crítico:** el tribunal evaluó dos instancias sobre cifras de origen desconocido. Presentar como medidos resultados que no surgieron de mediciones, en un documento entregado para evaluación, es una cuestión de integridad académica que el tribunal no puede dar por saldada en silencio. El cambio de corpus, en sí mismo, es legítimo, y la V4 es mejor por haberlo hecho: lo que falta es la declaración.

**Corrección exigida:** incorporar como anexo una «Declaración de trazabilidad entre versiones», firmada por los tres autores y con conocimiento de la dirección, que (a) enumere cada resultado cuantitativo de la V2 y la V3 que no figura en la V4 —como mínimo los de la tabla anterior, las Tablas 1 a 5 de la V3 y los tres casos de su Sección 5.3— e indique para cada uno su origen (medición sobre un corpus descartado, proyección, simulación, generación con herramienta de asistencia u otro); (b) documente con fechas el ciclo de vida de los datos (B4, corpus del 25 al 30/09, depuración, B5) y el destino de lo eliminado; y (c) declare si alguna cifra de la V4 deriva de material de la V2 o la V3. El tribunal valorará el contenido de esa declaración conforme al reglamento vigente. Sin ella no se habilita la defensa.

**N-08 — La validación del clasificador no mide el desempeño sobre el corpus evaluado y la estimación estratificada está mal calculada \[CRÍTICO\]**

**Ubicación:** 3.3, 5.5 (Tablas 5.7 a 5.10), 5.7, 7.1 y 7.4.

**(a) Muestra ajena al corpus.** La muestra del 30/09 se extrajo de un corpus anterior a B5 que incluía r/DerechoGenial (10 de los 50 casos) y r/argentina. La V4 advierte que «no debe usarse para estimar la proporción de aciertos de la ventana», pero las Tablas 5.12 y 7.1 declaran CUMPLIDOS criterios que se refieren al sistema evaluado en B5, y 7.4 concluye que «la evidencia respalda el supuesto en la dimensión de clasificación».

**(b) Estratos del clasificador anterior, métricas del vigente, sin ponderar.** El estrato censado son los 28 positivos del clasificador anterior (TP 24 \+ FP 4\) y el estrato sorteado, 22 de sus negativos (FN 5 \+ TN 17). Con el clasificador vigente, 3 de los 29 positivos provienen del estrato sorteado (los 3 FN que pasaron a TP). Por lo tanto, el denominador de la precisión no es «el conjunto censado de predicciones positivas» (Tablas 5.8 y 5.12): mezcla casos censados, que pesan 1, con casos sorteados que representan N₀/22 publicaciones cada uno, donde N₀ es el tamaño del estrato «No relevante» al 30/09, cifra que el documento no informa. Lo mismo vale para la sensibilidad y el F1, calculados como si la muestra fuera aleatoria simple. Por la misma razón, la omisión «2 de 22» mezcla el estrato del clasificador anterior con los errores del vigente: en el estrato sorteado hay 19 negativos del clasificador vigente (2 FN \+ 17 TN).

**Orden de magnitud.** Con un peso w \= N₀/22, la sensibilidad estimada del clasificador vigente es (24 \+ 3w) / (24 \+ 5w). Solo alcanza 0,80 si w ≤ 4,8, es decir, si el corpus del 30/09 tenía como máximo unas 134 publicaciones. Con 300 publicaciones (w ≈ 12,4) sería ≈ 0,71; con 500 (w ≈ 21,5), ≈ 0,67. Sin N₀, el CUMPLIDO de la sensibilidad y del F1 no puede sostenerse, ni siquiera «respecto de la muestra».

**(c) Un anotador asistido por herramientas no identificadas.** La Sección 6.3 dice que el etiquetado lo hizo una persona «sin formación formal en ciberseguridad y con asistencia de herramientas». Si un modelo de lenguaje propuso o revisó etiquetas, la referencia deja de ser independiente de un sistema automático. Además contradice la Declaración de autoría, que atribuye el etiquetado a los autores sin mencionar asistencia.

**(d) Sorteo no reproducible.** 3.3.2 presenta una «semilla declarada (20260930)»; 6.3 reconoce que el ordenamiento por md5() era código muerto y que solo se reproducen 8 de las 50 filas.

**(e) Ninguna amenaza en español.** Las 29 amenazas de la etiqueta humana provienen de r/netsec (9) y r/Malware (20). El componente que sostiene la brecha del trabajo —el léxico rioplatense— no tiene validación cuantitativa.

**(f) Cuentas inconsistentes de la corrección del clasificador.** La Tabla 5.9 atribuye el cambio (TP 24 → 27; FP 4 → 2\) a bajar MIN\_HITS y retirar «dni»; el párrafo siguiente lo atribuye a tres filas con clasificación heredada que «eran exactamente los tres falsos positivos de más», pero los FP bajan en 2, no en 3; y 4.4.1 dice que con MIN\_HITS \= 2 se detectaban 25 de 29 amenazas, mientras la Tabla 5.9 informa 24\.

**Corrección exigida:** construir una nueva muestra de control extraída del corpus B5: censo de las 170 publicaciones clasificadas como amenaza y muestra aleatoria de las 554 «No relevante», con procedimiento reproducible (ORDER BY estable, semilla y hash del archivo) y tamaño justificado (el cálculo de la propia V4 da unas 127 publicaciones para ±5 puntos si la omisión ronda el 9 %, y unas 270 si ronda el 23 %); guía de etiquetado escrita; dos anotadores independientes al menos sobre una submuestra común de 50 casos, con kappa de Cohen; declaración de si alguna herramienta propuso etiquetas; estimadores ponderados por estrato con sus intervalos; resultados separados para r/devsarg. Conciliar la Tabla 5.9 y 4.4.1 con una tabla de transición caso por caso. Si la nueva validación no se realiza, reclasificar sensibilidad y F1 como NO EVALUADOS sobre el corpus, mantener la precisión como valor indicativo y reescribir 7.4.

# **5\. Nuevos hallazgos mayores**

**N-09 — La explicación de la latencia es incorrecta y la causa real no está identificada \[MAYOR\]**

**Ubicación:** 5.3, 6.3, 7.3 (PI-1), 8.2 y 8.3.

**Evidencia:** 5.3 afirma que «el piso teórico del diseño con un ciclo de 15 minutos es \[…\] de alrededor de 15 a 17 minutos en el mejor caso» y concluye que la causa «es estructural y no depende del rendimiento del código».

**Problema:** (a) 15 a 17 minutos es la cota superior de la espera por sondeo, no el piso: una publicación creada justo antes de un ciclo se captura en alrededor de un minuto; con llegadas uniformes la espera media es de unos 7,5 minutos más hasta 2 minutos por la espera entre comunidades. (b) Si cada ciclo funcionara, prácticamente todas las publicaciones tendrían latencia de 17 minutos o menos. La mediana observada es de 126,9 minutos (unas 7,5 veces la cota) y el P95 de 1.376,2 minutos (unas 80 veces): el scheduler explica, como mucho, alrededor del 1 % del P95. El exceso tiene otras causas que el propio documento menciona sin conectarlas: las corridas incompletas (15 de 28 el 02/10, 53,6 %), la interrupción de 44 horas y, posiblemente, demoras de visibilidad ajenas al sistema (publicaciones retenidas por moderación que aparecen en el listado con su created\_utc original). (c) Estimación indicativa, bajo el supuesto de llegadas uniformes: con unas 25,7 publicaciones nuevas por día (437 en 17 días) y 96 ciclos diarios, si todos los ciclos funcionaran cabría esperar unos 22 a 23 ciclos por día con contenido nuevo; la Figura 1 informa 171 ciclos con contenido en toda la ventana, unos 10 a 11 por día. Sugiere que alrededor de la mitad de los ciclos no completó. (d) En consecuencia, «el límite no proviene \[…\] de la capacidad del artefacto, sino de la cadencia de recolección» (7.3, PI-1) es cierto solo a medias: la cadencia hace inalcanzable el umbral de 5 minutos, pero no explica un P95 de 22,9 horas; eso lo explica la operación.

**Corrección exigida:** corregir la afirmación sobre el piso; descomponer la latencia por comunidad, excluyendo el intervalo de la interrupción y comparándola con la distribución esperada por diseño; informar el registro de ejecuciones de n8n de la ventana (ciclos programados, ejecutados, completos, con 429/403 y con contenido) y definir «ciclo con contenido»; revisar una muestra de publicaciones con latencia mayor a 60 minutos para determinar si la demora es del sistema o de la visibilidad en la plataforma; reescribir 5.3, 6.3, 7.3 y 8.2 según el resultado.

**N-10 — Exposición de identificadores en el propio informe y riesgo residual subestimado \[MAYOR\]**

**Ubicación:** 3.4, 4.3, 5.4 y Tabla 5.11.

**Evidencia:** 5.4 transcribe título e identificador de plataforma de las cuatro publicaciones del disparo del 12/10. La Tabla 5.11 publica diez identificadores, seis de r/devsarg, entre ellos publicaciones de carácter personal: un usuario que relata un falso reclutador que le pidió credenciales (1x5acdz), una consulta sobre almacenamiento de datos personales (1x2vur9) y una reflexión personal (1wr7qwo). La Sección 3.4 afirma que el informe se limita a «no reproducir identificadores en los casos del Capítulo 5».

**Problema:** (a) Un identificador de publicación lleva en un paso, en la plataforma, a la publicación y al perfil de su autor: publicarlo anula, en el propio documento, la seudonimización aplicada en la base. (b) El mismo vector existe en la base: posts.id y url son los identificadores de la plataforma, de modo que cualquiera con acceso de lectura a tesi\_osint recupera al autor sin necesidad de la clave mientras la publicación exista. El análisis de riesgo residual de 3.4 solo contempla la reidentificación indirecta por contenido. (c) En la normalización «se descarta el prefijo /u/ de las menciones»: los nombres de usuario mencionados en el cuerpo se conservan en claro y, sin el prefijo, son más difíciles de detectar después. (d) La calificación de «irreversible» (H-01).

**Corrección exigida:** reemplazar en el informe los identificadores y los títulos literales de las publicaciones de r/devsarg por códigos internos (C-01, C-02…) y descripciones genéricas, con la tabla de correspondencia fuera del documento y a disposición del tribunal; para las divulgaciones técnicas de r/netsec y r/Malware, citar la fuente original (aviso del fabricante, CVE) en lugar de la publicación de Reddit; ampliar el riesgo residual al vector del identificador de plataforma y a las menciones; decidir y documentar si las menciones se eliminan o se seudonimizan.

**N-11 — La eficacia del motor de anomalías no está demostrada y OE5 no puede declararse CUMPLIDO \[MAYOR\]**

**Ubicación:** 3.2, 4.5, 5.4, 6.1, 7.2 y 7.3.

**(a) Serie por fecha de ingesta.** El motor cuenta por ingested\_at, de modo que su serie refleja la operación del sistema (carga inicial del 01/10, interrupción del 02 al 04/10) tanto como la actividad de las comunidades. La V4 lo reconoce para el 01/10, pero no su efecto posterior.

**(b) Línea base contaminada por la carga inicial.** El 01/10 (55 publicaciones de Malware, 41 de Vulnerabilidades) queda dentro de la línea base de diez días de todas las evaluaciones del 02/10 al 11/10, y la eleva en \+5,5 y \+4,1 respectivamente. De los 15 días evaluados, solo los del 12/10 al 17/10 tienen una línea base libre de esa carga; y el único disparo considerado legítimo ocurre exactamente el primer día en que el 01/10 sale de la ventana (evaluación del 12/10, ventana del 02 al 11/10).

**(c) Interrupción computada como cero.** La línea base siempre divide por diez, incluido el 03/10, en que no hubo recolección. Un día sin servicio baja λ y favorece los disparos.

**(d) Falsa alarma nominal.** Con la regla X ≥ q95(λ) \+ 1 la probabilidad de disparo bajo la hipótesis nula llega hasta el 5 % por evaluación (con λ \= 0,8, el caso del 12/10, P(X ≥ 3\) ≈ 4,7 %; observar 4 tiene probabilidad ≈ 0,9 %). Es estadísticamente defendible, pero con un centenar de evaluaciones algún disparo por azar es esperable. La «legitimidad» que argumenta 5.4 descansa en que las cuatro publicaciones describen vulnerabilidades reales, que es el contenido ordinario de r/netsec cualquier día, y no en que la jornada haya sido inusual.

**(e) Sin referencia para evaluar.** No se define qué cuenta como anomalía verdadera ni cuáles se omitieron, de modo que el motor no tiene medida de eficacia. Además, 4.5 afirma que «todas las evaluaciones analizadas en 5.4 son posteriores a la corrección» del 05/10, pero la Tabla 5.5 incluye los cinco disparos de la corrida del 02/10; y el criterio de cierre «dos ciclos semanales completos para la calibración de la línea base» (3.2) no coincide con una línea base de diez días.

**Corrección exigida:** el motor es determinista sobre la base: recalcularlo retrospectivamente, sin tocar la tabla de producción, con (i) conteos por created\_utc de las publicaciones creadas en la ventana y (ii) exclusión de la carga inicial y de los días sin operación de la línea base, dividiendo por los días efectivamente operados; informar el resultado junto con el número esperado de falsas alarmas bajo la hipótesis nula (suma de P(X ≥ u | λ) sobre las evaluaciones) frente a los disparos observados; definir una referencia externa, aunque sea cualitativa, para juzgar los disparos (por ejemplo, coincidencia con divulgaciones o avisos relevantes de esa fecha); reclasificar OE5 como «implementado; eficacia no demostrada» salvo que el análisis sostenga más; corregir las afirmaciones de 4.5 y 3.2.

**N-12 — El diccionario contiene términos inactivos y genéricos, y su mecánica descrita no coincide con un caso observado \[MAYOR\]**

**Ubicación:** 2.2, 4.4, 4.4.1, Anexo C y Tablas 5.3 y 5.11.

**(a) Términos inactivos por errata.** «caeron los servidores» (forma correcta: cayeron) y «sequestro de datos» (secuestro). Como la comparación es exacta tras la normalización, nunca coincidirán con un texto bien escrito. «caeron los servidores» es, además, uno de los modismos que 2.2 exhibe como prueba de la brecha.

**(b) Términos genéricos en el dominio de desarrollo.** «filtrado» (Filtración de Datos) es de uso corriente en programación («filtrado de resultados»); «datos personales» activó el falso positivo 1x2vur9; «leak» coincide con «memory leak»; «clonar» (Robo de Credenciales) coincide con «clonar el repositorio»; «acceso remoto», «cambio de contrasena» y «segundo factor» describen configuración ordinaria; «payload», «loader», «packed» y «miner» (Malware) son vocabulario cotidiano de desarrollo. La Sección 4.4.1 formula la regla correcta —«un término que coincide con trámites administrativos es demasiado general»— pero la aplica a un solo término (dni). Es coherente con que r/devsarg aporte 7 detecciones, en su mayoría falsas.

**(c) Términos solapados que duplican coincidencias.** «zero day» está contenido en «zero day vulnerability»; «ejecucion remota» (Malware) en «ejecucion remota de codigo» (Vulnerabilidades); «filtracion» en «filtracion publicada» (Hacktivismo); «vishing» (Phishing) en «vishing script» (Ingeniería Social). Una sola expresión suma dos coincidencias, eleva la puntuación y puede decidir la categoría.

**(d) Guiones.** 4.4.1 sostiene que un término con guion «se fragmenta en el texto —zero-day se convierte en dos palabras— y por eso los términos de varias palabras se buscan por coincidencia de subcadena». Pero la búsqueda por subcadena se hace sobre el texto normalizado, que según 2.1.3 y 4.4 solo pasa a minúsculas y quita diacríticos: «zero-day» no contiene la subcadena «zero day». La publicación 1x4xuvc («…Critical Zero-Day CVE», 5.4) obtuvo 0,25, es decir, una sola coincidencia, compatible con «cve» sola; si «zero day» hubiera coincidido, su puntuación sería 0,50. Sugiere que los compuestos con guion no se reconocen; debe verificarse con el código (H-15).

**Corrección exigida:** corregir las erratas; revisar los términos genéricos con el mismo criterio aplicado a «dni» e informar el efecto sobre la tabla de clasificación y sobre r/devsarg; eliminar los solapamientos o contar solo la coincidencia más larga; verificar con el código el tratamiento de guiones y, si corresponde, normalizarlos a espacio; publicar, para los casos de la Tabla 5.11 y del disparo del 12/10, la lista de términos que coincidieron.

**N-13 — El alcance «Argentina» y la brecha del léxico local no están sostenidos por el corpus evaluado \[MAYOR\]**

**Ubicación:** título, 1.4, 1.7 (PI-2), 2.2, 5.1, 6.2 y 7.3.

**Evidencia:** r/devsarg, la única comunidad argentina, aporta el 59,12 % del corpus y 7 de las 170 detecciones (4,1 %); las otras 163 (95,9 %) provienen de r/netsec y r/Malware, comunidades internacionales en inglés. r/argentina y r/DerechoGenial se dieron de baja tras la evaluación preliminar, y r/netsec y r/Malware se incorporaron «por su densidad de reportes verificables». La muestra de validación no contiene amenazas en español (N-08, e). La Sección 6.2 afirma que el aporte del léxico bilingüe «se verificó empíricamente» con dos casos.

**Problema:** las fuentes se cambiaron después de comprobar que las locales no producían detecciones. Es una iteración legítima de la DSR, pero cambia el objeto: el corpus ya no representa «comunidades digitales vinculadas a Argentina», y la respuesta a PI-2 descansa en una sola comunidad con unas dos detecciones correctas en 17 días —cuyo recuento, además, es contradictorio (N-14)—. Dos casos ilustran; no verifican.

**Corrección exigida:** optar por una de dos vías y aplicarla de forma consistente: (a) incorporar al menos otra fuente argentina o hispanohablante con contenido de ciberseguridad e informar métricas y detecciones por idioma; o (b) reformular título, objetivo general, PI-2, brecha (2.2) y conclusiones al alcance real (comunidades técnicas de Reddit, léxico bilingüe evaluado principalmente en inglés, componente local exploratorio), declarando el cambio de fuentes como iteración en la Tabla 3.1. En ambos casos, reemplazar «se verificó empíricamente» por «se ilustra con dos casos».

**N-14 — Inconsistencias internas de cifras y estados \[MAYOR\]**

Se detectaron las siguientes contradicciones entre secciones, figuras y anexos. Cada una es menor por separado; en conjunto afectan la confianza en el documento y deben corregirse antes de la defensa.

| \# | Tema | Contradicción | Corrección |
| :---- | :---- | :---- | :---- |
| 1 | Falsos positivos de r/devsarg | 5.1: «seis de ellas son falsos positivos o discusiones administrativas». 6.1: «tres de las siete detecciones son falsos positivos». 7.3: 85,7 % (6/7) falsos o administrativos y, a la vez, dos casos locales verificados (2 \+ 6 \= 8 \> 7\) | Publicar la clasificación de las 7 detecciones y unificar la cifra |
| 2 | Estado del workflow | 4.1: «en estado activo»; Figura 1: «active \= 1»; Figura 3: «active \= false» | Verificar y unificar |
| 3 | Días de operación | «16 fechas con recolección» (portada, 2.2, Tabla 6.1, 7.2); «15 días completos» (Figura 1); «17 días de operación continua» (7.3) pese a la interrupción de 44 h | Unificar y no llamar continua a una operación interrumpida |
| 4 | Fecha de corte | Portada: «cerrada con corte 17/10/2026»; 3.2: «17/10/2026, fecha fijada como corte el 19/10/2026»; Capítulo 5 y Anexo D: «inicio del 18/10/2026» | Una sola definición |
| 5 | Corrección del motor | 4.5: «todas las evaluaciones analizadas en 5.4 son posteriores a la corrección» (05/10); la Tabla 5.5 incluye la corrida del 02/10 | Corregir 4.5 |
| 6 | Diferencia 167 / 170 | 5.4 atribuye las 3 publicaciones a «los días 02/10 y 03/10»; el 03/10 no tuvo ingesta (Tabla 5.2) | Las tres son del 02/10 |
| 7 | Falsos positivos de r/DerechoGenial | 1.4: «3 falsos positivos del clasificador»; Tabla 5.10: 1 FP de esa comunidad con el clasificador vigente | Indicar la versión del clasificador |
| 8 | Tabla 5.9 vs. 4.4.1 | TP con MIN\_HITS \= 2: 24 vs. 25; «tres FP de más» vs. reducción de 2 | Ver N-08 (f) |
| 9 | Tamaño de muestra | 6.4 y 8.2: «del orden de 270 publicaciones», que corresponde a una omisión del 22,7 % (5/22, clasificador anterior); con el 9,1 % informado son ≈ 127 | Recalcular con el valor vigente |
| 10 | Throughput | Resumen: «no se verifica»; Tablas 1.1, 5.12 y 7.1: «NO CUMPLIDO» | Ver H-06 |
| 11 | Códigos internos | «IN-06» (Figura 1\) e «IN-08» (Tabla 7.2) no se definen en el documento | Definir o retirar |
| 12 | Fechas | 5.1: «El panel (a) no incluye el 10/03» (es el 03/10) | Corregir |
| 13 | Criterios a priori | 1.6: «no fueron modificados después de observar los resultados» frente a la nota que declara la modificación | Ver N-05 |
| 14 | Semilla | 3.3.2: «semilla declarada (20260930)»; 6.3: sorteo no reproducible, ordenamiento por md5() como código muerto | Ver N-08 (d) |

**Corrección exigida:** corregir cada ítem y hacer una pasada final de consistencia entre Resumen, Abstract, cuerpo, figuras y anexos.

# **6\. Hallazgos menores y de forma**

## **6.1. Estado de las observaciones menores de las instancias anteriores**

| ID | Observación | Estado V4 | Comentario |
| :---- | :---- | ----- | :---- |
| **M-01** | Abstract espejo del Resumen | **RESUELTO** | Incluye métricas y alcance; ver m-26 |
| **M-03** | Tamaños por estrato | **RESUELTO CON OBSERVACIONES** | 28 / 22 informados; falta N₀ (N-08) |
| **M-04** | Tablas sin rótulo | **RESUELTO** | 22 tablas numeradas y tituladas |
| **M-05** | Subsecciones de 5.1 | **RESUELTO** | Capítulo 5 reestructurado |
| **M-07** | Fecha de consulta de límites | **RESUELTO** | Caracterización fechada (25/09, revisada 30/09) |
| **M-08** | Suscriptores sin fecha | **PARCIAL** | Ya no se informa el tamaño de las comunidades; agregarlo con fecha |
| **M-10** | Supuesto no contrastable | **RESUELTO** | Vinculado a los umbrales de 1.6 |
| **m-13** | Ratios de la Tabla 2 (V3) | **RESUELTO** | No aplica: tabla retirada con el corpus anterior |
| **m-14** | Uso de Liao et al. | **RESUELTO** | Usado como antecedente; autores completos |
| **m-15** | Separador decimal | **RESUELTO** | Coma decimal uniforme en castellano |
| **m-16** | Inclusión de r/derechogenial | **RESUELTO** | Dada de baja con fundamento |
| **m-17** | Herramientas generativas | **PARCIAL** | Tareas indicadas, herramientas no identificadas (m-27) |
| **m-18** | Sentencia de persistencia | **RESUELTO CON OBSERVACIONES** | ON CONFLICT descrito; SQL no transcripto (m-29) |
| **m-19** | Atributos indirectos | **RESUELTO CON OBSERVACIONES** | Superado por N-10 |
| **m-20** | ON DELETE CASCADE | **RESUELTO** | RESTRICT con baja lógica |

M-02, M-06, M-09, M-11 y M-12 ya estaban resueltas en la V3 y se mantienen.

## **6.2. Nuevas observaciones menores**

* **m-21.** En el DDL, alertas.estado tiene DEFAULT 'ENVIADA' y los comentarios dicen «Alertas enviadas» y «mensaje completo enviado», mientras las seis filas están PENDIENTE y el envío deshabilitado: una inserción sin estado explícito quedaría registrada como enviada. Usar DEFAULT 'PENDIENTE'. La tabla anomalias carece de restricción UNIQUE (categoria, ventana\_inicio): reejecutar el flujo de análisis duplica evaluaciones, de modo que la idempotencia afirmada para la ingesta no se extiende al análisis.

* **m-22.** Figuras. En la Figura 3 el subtítulo se superpone con la primera fila de nodos, las cajas «Send Telegram Alert» y «Upsert Posts» se solapan y algunas aristas son ambiguas (una parece ir de Parse Reddit Posts a Extract Entities salteando HMAC y clasificación; si es la rama del centinela, rotularla). La Figura 4 (a) usa un eje categórico que omite el 03/10 y oculta la interrupción que el texto destaca: usar un eje de fechas continuo con la barra en cero. En la Figura 4 (b) la nota se superpone con el título del eje. Cada figura lleva un título dentro de la imagen y otro epígrafe debajo, con redacción distinta: dejar uno solo, según APA.

* **m-23.** La Tabla 5.4 omite el desvío estándar de los subconjuntos operativos y el máximo de la fila «desde el 02/10», que no se comenta en el texto. El título de la Tabla 5.6 precede a su párrafo introductorio.

* **m-24.** Causas no identificadas. No se informa la causa de la interrupción del 02/10 18:47 al 04/10 14:54 (apagado del equipo, caída de un contenedor, error del flujo), relevante para la «recuperación ante fallos» de OE2. El 17/10 registra 8 publicaciones (19 % del promedio diario) y se atribuye al «cierre de la ventana» aunque se declara día completo: informar los ciclos ejecutados ese día.

* **m-25.** Referencias. La Ley 25.326 se cita en todo el documento pero no figura en la lista de referencias. El Decreto 1558/2001 se atribuye a la Dirección Nacional de Protección de Datos Personales, cuando lo dictó el Poder Ejecutivo Nacional (es el decreto que reglamenta la ley y organiza esa Dirección). Pastor-Galindo et al. (2020) se cita como fuente de «estándares de referencia de la industria» para los umbrales del 80 %, pero ese relevamiento no fija umbrales de clasificación: declararlos como decisión de diseño propia o citar una fuente que los establezca. Si Dengra y Rivas (2026) no está aprobado y depositado en el repositorio institucional, citarlo como trabajo inédito con versión y fecha de consulta, porque sus cifras pueden variar.

* **m-26.** El Abstract dice «false positive rate of 6.9 %»; con la definición adoptada corresponde «false discovery rate».

* **m-27.** La Declaración de uso de herramientas no identifica las herramientas (nombre y versión), como pidió la V3 (m-17), y no menciona la asistencia en el etiquetado que reconoce 6.3.

* **m-28.** El índice general tiene un solo nivel. Regenerarlo con secciones y subsecciones e incluir Resumen, Abstract, Declaración y Siglas.

* **m-29.** La Figura 1 dice «ON CONFLICT … DO UPDATE sobre 13 columnas»; la tabla posts tiene exactamente 13 columnas además de la clave, de modo que la frase sugiere que también se sobrescriben ingested\_at y created\_utc, mientras 4.3 enumera siete campos sobrescritos. Si ingested\_at se actualizara en cada relectura del feed (que devuelve los mismos elementos cada 15 minutos), se alterarían la latencia y los conteos diarios del motor. La distribución de la Tabla 5.2 sugiere que no ocurre, pero debe mostrarse: transcribir la sentencia con su lista SET.

* **m-30.** La portada y el Resumen dicen «Trabajo Final de Inserción», y el antecedente se cita como «Trabajo Final de Carrera»: verificar la denominación reglamentaria del trabajo y usarla de manera uniforme.

# **7\. Verificación de consistencia numérica**

Se recalcularon todas las cifras verificables de la V4. Se deja constancia de lo que resultó correcto para que el equipo no revise lo que ya está bien.

| Verificación | Resultado | Detalle |
| :---- | ----- | :---- |
| Tabla 5.1 — sumas y porcentajes | **CORRECTO** | 428 \+ 150 \+ 146 \= 724; 421 \+ 84 \+ 49 \= 554; porcentajes por comunidad verificados |
| Tabla 5.2 — serie diaria | **CORRECTO** | Los 17 valores suman 724; porcentajes verificados |
| Composición por fecha de creación | **CORRECTO** | 8 \+ 19 \+ 28 \+ 28 \+ 204 \= 287; 437 \+ 287 \= 724 |
| Tabla 5.3 — categorías por comunidad | **CORRECTO** | Filas y columnas cierran (150 / 146 / 428\) |
| Distribución de la puntuación | **CORRECTO** | 554 \+ 130 \+ 26 \+ 7 \+ 7 \= 724; suma ponderada 57,75 coincide con las medias por categoría |
| Proporciones de 5.2 | **CORRECTO** | 52/66 \= 78,8 %; 73/97 \= 75,3 %; 130/170 \= 76,47 % |
| Tabla 5.4 — conversiones | **CORRECTO** | 16.483,8 min \= 11,4 días; 191.368,8 min \= 132,9 días (21/05 → 01/10); 1.376,2 min \= 22,9 h; 398/437 \= 91,1 % |
| Latencia vs. diseño | **INCONSISTENTE** | Cota superior ≈ 17 min frente a P50 \= 126,9 min (N-09) |
| Tablas 5.5 y 5.6 | **CORRECTO** | 6 disparos; 5 × 15 \+ 14 \+ 14 \+ 9 \= 112 evaluaciones; 167 observados |
| Diferencia 167 / 170 | **CORRECTO CON OBSERVACIÓN** | Las 3 publicaciones son del 02/10, no del 03/10 |
| Umbrales de Poisson | **CORRECTO** | q95(0,8) \= 2 → 3; q95(2,95) \= 6 → 7; q95(4,0) \= 8 → 9; coherentes con 6,87 y 8,33 |
| Tablas 5.7 y 5.8 | **CORRECTO** | 27/29 \= 0,931; F1 \= 54/58; IC exactos \[0,772; 0,992\], \[0,008; 0,228\], \[0,011; 0,292\] |
| Tabla 5.9 — aritmética | **CORRECTO** | 24/28 \= 0,857; 24/29 \= 0,828; F1 \= 48/57 \= 0,842 |
| Tabla 5.9 — texto | **INCONSISTENTE** | «Tres FP de más» frente a reducción de 2; TP \= 25 en 4.4.1 (N-08) |
| Estimación estratificada | **NO VÁLIDA** | Estratos del clasificador anterior sin ponderar (N-08) |
| Throughput operativo | **CORRECTO** | 724 / 408 h \= 1,77 posts/h; 42,6 por día |
| Tamaño de muestra «≈ 270» | **INCONSISTENTE** | Corresponde a p \= 0,227; con p \= 0,091 son ≈ 127 |
| Falsos positivos de r/devsarg | **INCONSISTENTE** | 6/7, 3/7 y 2 correctas en distintas secciones (N-14) |
| Anexo C — recuento | **CORRECTO** | 22 \+ 29 \+ 24 \+ 15 \+ 30 \+ 29 \+ 16 \+ 16 \+ 20 \= 201; listados contados uno por uno |
| Índices vs. paginación | **CORRECTO** | 10 capítulos, 22 tablas y 4 figuras en la página indicada |

# **8\. Rúbrica de evaluación y calificación**

| Dimensión | Peso | V2 | V3 | V4 | Fundamento V4 |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Estructura y forma académica** | 10 % | 6,0 | 5,0 | 8,0 | Figuras reales, índices correctos y anexos A–D; legibilidad de la Figura 3 y códigos internos sin definir (m-22, N-14) |
| **Marco teórico y estado del arte** | 15 % | 8,0 | 6,0 | 8,0 | Capítulo restituido, todas las referencias citadas y contraste sólido con el antecedente; ajustes normativos (m-25) |
| **Diseño metodológico** | 20 % | 7,0 | 6,0 | 6,0 | Definiciones, fórmulas e IC correctos y brecha diseño/ejecución declarada; muestra ajena al corpus, estratos sin ponderar y un anotador (N-08) |
| **Desarrollo del artefacto** | 20 % | 4,5 | 4,5 | 7,5 | Sistema real de 17 nodos, DDL completo, motor reformulado y defectos documentados; código no transcripto y diccionario con defectos (H-15, N-12) |
| **Resultados y validez** | 20 % | 4,5 | 5,0 | 6,0 | Datos trazables e incumplimientos informados sin maquillaje; clasificación no medida sobre el corpus, latencia mal explicada, motor sin eficacia demostrada (N-08, N-09, N-11, N-14) |
| **Discusión y conclusiones** | 10 % | 7,5 | 6,5 | 7,0 | Discusión honesta y limitaciones exhaustivas; sobreafirmaciones en 6.2, 7.3 y 7.4 (N-13) |
| **Aspectos legales y éticos** | 5 % | 5,0 | 7,0 | 6,5 | Configuración y rotación de clave documentadas; publicación de identificadores y «irreversible» (N-10, H-01) |
| **PROMEDIO PONDERADO** | 100 % | 6,0 | 5,5 | 6,9 | Ascenso de 1,4 puntos respecto de la V3 |

**CALIFICACIÓN DE ESTA INSTANCIA: 6,9 / 10**

**Condición: APROBADO CON CORRECCIONES OBLIGATORIAS. REENTREGA V5.**

La nota sube 1,4 puntos porque el documento volvió a ser evaluable y porque los autores cerraron siete de los ocho ítems bloqueantes de la V3: reconstruyeron el texto sobre la V2, midieron la latencia desde la base, retiraron la cobertura, publicaron fórmulas, matriz e intervalos, reformularon el motor, completaron el DDL e incorporaron figuras reales. A eso se suma un cambio de actitud que el tribunal valora: los criterios incumplidos se informan como incumplidos y las limitaciones se declaran sin atenuantes.

La nota no alcanza la proyección de 8,0 a 8,5 formulada en la V3, y corresponde explicar por qué. Aquella proyección suponía que los resultados presentados se sostendrían; al reemplazarlos por datos reales aparecieron dos problemas que la V3 no podía ver: no se sabe de dónde provenían las cifras anteriores (N-07) y la validación del clasificador —que es el aporte central del trabajo— no mide el desempeño sobre el corpus evaluado (N-08). Pesan además la explicación errónea de la latencia (N-09), la falta de evidencia de eficacia del motor (N-11), el desajuste entre el alcance «Argentina» y el corpus (N-13) y las contradicciones internas (N-14).

**Proyección:** el cierre de los cinco ítems bloqueantes de la Sección 9 y de al menos seis de los de prioridad alta ubica el trabajo en el rango de 8,0 a 8,5 en la V5. Una validación nueva con dos anotadores, acuerdo sustancial (κ ≥ 0,61) y resultados separados por idioma lo ubicaría por encima de 8,5.

**La defensa se habilitará con la V5, una vez cerrados los ítems bloqueantes 1 a 5\. La declaración del ítem 1 es requisito previo indispensable.**

# **9\. Plan de correcciones exigido para la V5**

Ordenado por prioridad de ejecución. Los ítems 1 a 5 son condición de habilitación a defensa.

| \# | Acción requerida | Hallazgo | Prioridad |
| :---- | :---- | :---- | ----- |
| 1 | Declaración de trazabilidad entre versiones (origen de cada cifra de la V2 y la V3 retirada; ciclo de vida de los datos con fechas), firmada por los autores y con conocimiento de la dirección | N-07 | **Bloqueante** |
| 2 | Nueva validación sobre el corpus B5: censo de las 170 detecciones y muestra aleatoria reproducible de «No relevante», dos anotadores con kappa, estimadores ponderados con IC y resultados por idioma; conciliar la Tabla 5.9. En su defecto, declarar sensibilidad y F1 como no evaluados y reescribir 7.4 | N-08, H-13, H-04 | **Bloqueante** |
| 3 | Acceso verificable a la evidencia (URL o copia con hash) y anexo con el código de los cuatro nodos de código y el SQL de persistencia y de las consultas del Capítulo 5 | H-07, H-15, m-29 | **Bloqueante** |
| 4 | Retirar del informe identificadores y títulos literales de publicaciones de r/devsarg; ampliar el riesgo residual; eliminar «irreversible» | N-10, H-01 | **Bloqueante** |
| 5 | Corregir las 14 contradicciones de la tabla de N-14 y hacer una pasada final de consistencia | N-14 | **Bloqueante** |
| 6 | Corregir la explicación de la latencia y descomponerla con el registro de ejecuciones de n8n | N-09, H-12 | **Alta** |
| 7 | Recalcular el motor por fecha de creación, sin carga inicial ni días sin servicio en la línea base; informar falsas alarmas esperadas; reclasificar OE5 | N-11, H-03 | **Alta** |
| 8 | Depurar el diccionario (erratas, términos genéricos, solapamientos, guiones) y publicar la traza de coincidencias de los casos | N-12 | **Alta** |
| 9 | Definir el alcance: incorporar una fuente local adicional o reformular título, objetivo general, PI-2, brecha y conclusiones | N-13 | **Alta** |
| 10 | Throughput: medir capacidad por reproducción controlada o declararlo NO EVALUADO de forma uniforme | H-06 | **Alta** |
| 11 | Ajustar «alertas tempranas» en objetivo general y título; incluir un payload de alerta; aclarar la credencial | H-02 | **Alta** |
| 12 | Presentar la tasa de falsos descubrimientos como complemento y precisar cuándo se fijó cada umbral | N-05 | **Alta** |
| 13 | Informar resultados de la extracción de entidades y publicar la matriz por categoría | N-06, H-04 | **Alta** |
| 14 | Corregir figuras y epígrafes | m-22, H-11 | **Media** |
| 15 | DDL: DEFAULT 'PENDIENTE' en alertas y UNIQUE en anomalias | m-21 | **Media** |
| 16 | Restantes observaciones de forma | m-23 a m-28, m-30, M-08, m-17 | **Media** |

*Devolución emitida por el tribunal evaluador — Tecnicatura Universitaria en Programación, UTN Facultad Regional Mendoza. Documento de uso académico interno, destinado a los autores y a la dirección del trabajo.*