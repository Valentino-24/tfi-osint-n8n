# SISTEMA AUTOMATIZADO DE MONITOREO DE FOROS Y REDES SOCIALES PARA LA DETECCIÓN DE TENDENCIAS Y ALERTAS EN CIBERSEGURIDAD EN COMUNIDADES TÉCNICAS DE REDDIT MEDIANTE OSINT Y N8N

**Universidad Tecnológica Nacional — Facultad Regional Mendoza**  
Tecnicatura Universitaria en Programación

Trabajo Final de Inserción para optar al título de Técnico Universitario en Programación

**Autores:** Valentino Lorca · Jerónimo Zúñiga · Enzo Severino  
**Directores / Profesores:** Prof. Alberto Cortez · Prof. Ariel Enferrel  
Mendoza, Argentina — 2026

> **Versión del documento (V5).** Esta es la quinta versión del informe y la reentrega solicitada por el tribunal tras la evaluación de la V4, atendiendo las correcciones obligatorias de la devolución (6,9/10, APROBADO CON CORRECCIONES OBLIGATORIAS). Se reconstruye sobre la base textual de la V2 e incorpora el sistema efectivamente implementado y los datos realmente relevados. El corpus evaluado es el correspondiente a la ventana de recolección **B5**, con **último día de recolección 17/10/2026** y corte del corpus en el **inicio del 18/10/2026**, compuesto por **724 publicaciones** de **3 subreddits** relevadas en **16 fechas** (el 03/10/2026 no hubo recolección). Los datos que respaldan cada tabla y figura de este informe están archivados con su consulta, su fecha y su `n` en `V4/evidencias/informe_v5_2026-10-20/` y en las evidencias previas del repositorio del proyecto.
>
> **Declaración de autoría y de uso de herramientas de asistencia.** La concepción del problema, el diseño del sistema, la operación del pipeline, el etiquetado de la validación (n = 352, con tres anotadores) y la interpretación de los resultados son de los autores. Para la elaboración de este trabajo se utilizaron **herramientas generativas de gran modelo de lenguaje (LLM)** con fines de asistencia: **OpenCode** con el modelo **opencode/big-pickle** (versión utilizada en el entorno de desarrollo, octubre de 2026), **Anthropic Claude Sonnet 4.5** y **Anthropic Claude Opus 4.5** (mediante las interfaces correspondientes). Su uso fue el siguiente: redacción y refactorización de código JavaScript para los nodos de n8n, generación y revisión de scripts SQL y Python (`V4/scripts/`), redacción y corrección de documentación técnica, verificación de formato y estructura del informe, y **apoyo en la preparación y revisión del proceso de etiquetado** de la validación (guía de anotación, definición de criterios y verificación de coherencia entre casos), sin delegar la decisión final de etiqueta ni la adjudicación de desacuerdos. Ninguna cifra publicada fue generada por un asistente: todas provienen de consultas `SELECT` sobre la base `tesi_osint` o de archivos de evidencia fechados que se citan en el propio texto. El trabajo final y su contenido son responsabilidad exclusiva de los autores.

## 

## Índice general

1\. Introducción

2\. Marco teórico y estado del arte

3\. Marco metodológico

4\. Desarrollo del sistema

5\. Resultados

6\. Discusión

7\. Conclusiones

8\. Recomendaciones y trabajos futuros

9\. Referencias bibliográficas

10\. Anexos A–E

##  Índice de tablas

Tabla 1.1. Criterios de éxito, momento de fijación y estado en la V5

Tabla 3.1. Aplicación de las fases de la DSR al trabajo

Tabla 4.1. Inventario de nodos del workflow desplegado

Tabla 4.2. Atributos del esquema físico (espejo de `A_DDL.sql`)

Tabla 5.1. Corpus de la ventana B5 por subreddit

Tabla 5.2. Recolección diaria de la ventana B5

Tabla 5.3. Clasificación temática del corpus

Tabla 5.4. Latencia extremo a extremo de la ingesta

Tabla 5.5. Disparos del motor de anomalías

Tabla 5.6. Evaluaciones del motor por categoría

Tabla 5.7. Matriz de confusión estratificada de la validación V5 (352 casos etiquetados)

Tabla 5.8. Métricas de clasificación e intervalos de confianza exactos (validación V5)

Tabla 5.9. Desempeño del clasificador por comunidad (validación V5)

Tabla 5.9.b. Desempeño por idioma (español/inglés), validación V5

Tabla 5.10. Matriz de confusión por categoría (referencia × clasificador)

Tabla 5.11. Efecto de la corrección del umbral del clasificador (muestra 30/09/2026)

Tabla 5.12. Análisis de errores del clasificador vigente (muestra 30/09/2026)

Tabla 5.13. Extracción de entidades sobre el corpus

Tabla 5.14. Casos representativos del corpus B5

Tabla 5.15. Síntesis del cumplimiento de los criterios de éxito

Tabla 6.1. Contraste con el antecedente local (Dengra y Rivas, 2026)

Tabla 7.1. Trazabilidad de los criterios de éxito

Tabla 7.2. Trazabilidad de los objetivos específicos

Tabla 8.1. Recomendaciones para el sistema en producción

Tabla B.1. Inventario de nodos y responsabilidades (Anexo B)

Tabla C.1. Diccionario de categorías y términos (Anexo C)

Tabla E.1. Resultados de V2/V3 retirados y su origen

Tabla E.2. Ciclo de vida del corpus, con fechas y destino

##  Índice de figuras

Figura 1. Arquitectura del sistema OSINT: capas, nodos y artefactos reales

Figura 2. Modelo entidad-relación del esquema físico

Figura 3. Grafo de nodos y conexiones del workflow desplegado

Figura 4. Serie temporal de la ingesta y categorías detectadas

##  Siglas

**B5**: ventana de recolección. **DDL**: *Data Definition Language*. **DSR**: *Design Science Research*. **ETL**: *Extract, Transform, Load*. **FN/FP**: falso negativo/positivo. **HMAC**: *Hash-based Message Authentication Code*. **NLP**: *Natural Language Processing*. **OE**: objetivo específico. **OSINT**: *Open Source Intelligence*. **PI**: pregunta de investigación. **P50/P95**: percentiles. **RSS/Atom**: formatos de sindicación. **SOCMINT**: *Social Media Intelligence*. **TTP**: tácticas, técnicas y procedimientos. **TN/TP**: verdadero negativo/positivo.

# RESUMEN

El presente Trabajo Final de Inserción detalla el diseño, desarrollo, implementación y evaluación de un sistema automatizado de monitoreo de comunidades digitales, concebido para recolectar, procesar, almacenar y analizar información pública relevante en el ámbito de la ciberseguridad en comunidades técnicas de Reddit, con atención al léxico rioplatense, enmarcado en el paradigma de la Inteligencia de Fuentes Abiertas (OSINT). El proyecto aborda la problemática de la dispersión, heterogeneidad y falta de estructuración de los datos disponibles en internet, que dificultan la detección oportuna de amenazas y vulnerabilidades. La solución implementada integra herramientas de código abierto: n8n 2.40.6 para la orquestación de un pipeline ETL, PostgreSQL 18 para el almacenamiento relacional estructurado y un clasificador heurístico bilingüe, ejecutado dentro del propio orquestador, para la categorización de incidentes.

La recolección se realizó sobre la fuente pública de Reddit en formato RSS/Atom (`new/.rss`) de tres comunidades con monitoreo activo: r/netsec, r/Malware y r/devsarg. El corpus analizado corresponde a la ventana de recolección cerrada el 17/10/2026 y está compuesto por **724 publicaciones** persistidas entre el 01/10/2026 y el 17/10/2026, con **15 fechas de evaluación** registradas por el motor de anomalías. El flujo se ejecutó cada 15 minutos durante jornadas diurnas —4.929 minutos de los 25.920 de la ventana, el 19,0 %—, con una espera fija entre comunidades para respetar los límites de la plataforma, y aplicó una seudonimización de los autores mediante HMAC-SHA-256 con clave por despliegue antes de persistir cada registro.

Sobre ese corpus, el clasificador —9 categorías y 201 términos, con una puntuación saturante `min(1, hits/4)` y umbral mínimo de una coincidencia— determinó que el 76,52 % de las publicaciones no era relevante y asignó las 170 restantes a 8 categorías de amenaza, con predominio de Malware (79) y Vulnerabilidades (61). El motor de detección evaluó 8 categorías en 15 fechas mediante un umbral de Poisson calibrado sobre una ventana móvil de 11 días, con un piso absoluto de 3 eventos, y registró 6 disparos.

La validación se hizo sobre el corte exacto del corpus: se etiquetaron **352 publicaciones** —el censo de las 170 que el clasificador marcó como amenaza y una muestra aleatoria de 182 de las 554 marcadas como «No relevante»— con un protocolo de **tres anotadores** y adjudicación por consenso. La precisión fue de **0,847** (IC 95 % \[0,784; 0,898\]), la sensibilidad ponderada por el muestreo de **0,612** (\[0,534; 0,695\]) y el F1-score de **0,711** (\[0,635; 0,783\]); la tasa de falsos descubrimientos fue del **15,3 %** y la estimación de amenazas en el corpus, de **235 publicaciones (32,5 %)**, frente a las 170 que marcó el clasificador. **Solo el criterio de precisión se cumple**: la sensibilidad y el F1 quedan por debajo del 80 % comprometido, y el acuerdo entre anotadores (κ de Fleiss = 0,509) también queda por debajo del 0,61 comprometido. Las tres brechas se informan como resultados y no se atenúan.

Los resultados son deliberadamente presentados con su alcance: el criterio de cobertura se retira por no ser verificable con una única fuente y una única captura; el criterio de latencia extremo a extremo (≤ 5 minutos) **no se cumple** (P95 medido de 1.376 minutos sobre las publicaciones creadas dentro de la ventana), y el criterio de throughput (≥ 1.000 posts/hora) se declara **no evaluado**, porque no se midió la capacidad del artefacto: el ritmo observado (alrededor de 45 publicaciones por día) describe la demanda de la fuente, no la capacidad del sistema. El módulo de alertas quedó implementado y deshabilitado por defecto, sin evidencia de envío real. El motor de anomalías está implementado, pero **su eficacia no está demostrada**: recalculado sobre la fecha de creación de las publicaciones y con una línea base libre de la carga inicial, no emite ningún aviso en quince días. El informe documenta el marco legal de protección de datos personales bajo la Ley Nacional 25.326 y el Decreto 1558/2001, los principios de minimización y seudonimización aplicados y el riesgo residual que persiste sobre datos potencialmente reidentificables.

**Palabras clave:** OSINT, ciberseguridad, n8n, Reddit, NLP, automatización, léxico rioplatense.

# ABSTRACT

This Final Insertion Project presents the design, development, implementation and evaluation of an automated monitoring system for digital communities, built to harvest, process, store and analyze publicly available information relevant to cybersecurity in technical Reddit communities, with attention to Rioplatense Spanish, within the Open Source Intelligence (OSINT) paradigm. The project addresses the dispersion, heterogeneity and lack of structure of publicly available data, which hinder the timely detection of threats and vulnerabilities. The implemented solution integrates open-source tools: n8n 2.40.6 for ETL pipeline orchestration, PostgreSQL 18 for structured relational storage, and a bilingual heuristic classifier running inside the orchestrator for incident categorization.

Collection was performed against Reddit’s public RSS/Atom feeds (`new/.rss`) of three actively monitored communities: r/netsec, r/Malware and r/devsarg. The analyzed corpus corresponds to the collection window closed on 2026-10-17 and comprises **724 posts** persisted between 2026-10-01 and 2026-10-17, with **15 evaluation dates** recorded by the anomaly engine. The workflow ran every 15 minutes during daytime operation —4,929 of the window’s 25,920 minutes, i.e. 19.0%—, with a fixed wait between communities to respect platform limits, and applied keyed pseudonymization of authors through HMAC-SHA-256 with a per-deployment key before persisting each record.

On that corpus, the classifier —9 categories and 201 terms, with a saturating score `min(1, hits/4)` and a minimum threshold of one match— found 76.5 % of posts irrelevant and assigned the remaining 170 to 8 threat categories, dominated by Malware (79) and Vulnerabilities (61). The detection engine evaluated 8 categories across 15 dates using a Poisson threshold calibrated on an 11-day moving window with an absolute floor of 3 events, and recorded 6 triggers.

Validation was performed on the exact corpus cut: **352 posts** were labeled —the census of the 170 posts the classifier flagged as threats plus a random sample of 182 of the 554 flagged as “Not relevant”— by a **three-annotator protocol** with consensus adjudication. Precision was **0.847** (95 % CI \[0.784; 0.898\]), sampling-weighted recall **0.612** (\[0.534; 0.695\]) and F1-score **0.711** (\[0.635; 0.783\]); exact category accuracy among detected threats was **80.6 %**, the false discovery rate **15.3 %**, and the estimated number of threats in the corpus **235 (32.5 %)**. **Only the precision criterion is met**: recall and F1 fall below the committed 80 % threshold, and inter-annotator agreement (Fleiss’ κ = 0.509) also falls below the committed 0.61. All three gaps are reported as results rather than softened.

Results are deliberately reported with their scope: the coverage criterion is withdrawn because it is not verifiable with a single source and a single capture; the end-to-end latency criterion (≤ 5 minutes) is **not met** (measured P95 of 1,376 minutes for posts created within the window), and the throughput criterion (≥ 1,000 posts/hour) is declared **not evaluated**, because the artifact’s capacity was not measured: the observed rate (about 45 posts per day) describes the source’s demand, not the system’s capacity. The alerting module is implemented but disabled by default, with no evidence of real delivery. The anomaly engine is likewise implemented, but its efficacy is not demonstrated: recalculated on post creation time with a baseline free of the initial load, it raises no alerts across fifteen days. The report documents the personal data protection legal framework under Argentina’s National Law 25.326 and Decree 1558/2001, the minimization and pseudonymization principles applied, and the residual risk that persists over potentially re-identifiable data.

**Keywords:** OSINT, cybersecurity, n8n, Reddit, NLP, automation, Rioplatense Spanish.

# CAPÍTULO 1: INTRODUCCIÓN

##  1.1. Contextualización del problema

En la era digital contemporánea, las tecnologías de la información y la comunicación han reconfigurado las estructuras socioeconómicas, organizacionales y operativas a nivel global. La digitalización masiva de procesos críticos, transacciones comerciales y canales comunicacionales ha impulsado una proliferación sin precedentes de datos. Diariamente, millones de usuarios generan contenido en redes sociales, blogs, foros y plataformas especializadas, compartiendo experiencias, conocimiento técnico, opiniones e incidentes de diversa índole. Dentro del ámbito de la ciberseguridad, esta dinámica dio origen a un fenómeno de particular relevancia: las comunidades virtuales y los foros abiertos se convirtieron en repositorios primarios de información sobre amenazas emergentes, filtraciones de datos, vectores de ataque activos y vulnerabilidades recién divulgadas.

Con frecuencia, los detalles de un ataque, las tácticas, técnicas y procedimientos (TTP) de un grupo delictivo o la explotación de una nueva vulnerabilidad se discuten e informan en foros abiertos antes de ser publicados en boletines oficiales de ciberseguridad o reportados por los proveedores de software. Esto se debe a que la velocidad con la que opera la comunidad de investigadores, entusiastas y actores maliciosos en internet supera holgadamente los ciclos de auditoría de los organismos tradicionales de seguridad de la información (Glassman y Kang, 2012). En este contexto surge la necesidad de adoptar metodologías de Inteligencia de Amenazas (*Cyber Threat Intelligence*, CTI) respaldadas por el paradigma de la Inteligencia de Fuentes Abiertas (*Open Source Intelligence*, OSINT) para recolectar y procesar esa información pública.

##  1.2. Planteamiento del problema

A pesar del valor estratégico de la información disponible en plataformas abiertas, su explotación efectiva por parte de los equipos de ciberseguridad, los centros de operaciones de seguridad (SOC) y los analistas de la República Argentina se ve obstaculizada por factores técnicos y metodológicos. En primer lugar, el volumen y la tasa de generación de los datos: el monitoreo manual de múltiples foros, canales y redes sociales resulta inviable por las limitaciones del factor humano para procesar flujos continuos de información las 24 horas del día. En segundo lugar, la información se encuentra dispersa de manera heterogénea y fragmentada en decenas de comunidades digitales, cada una con sus propios formatos, terminologías y estructuras de datos (Pastor-Galindo et al., 2020).

En tercer lugar, los datos carecen de estructuración formal: consisten predominantemente en texto libre en lenguaje natural, con modismos, jerga técnica y ruido semántico, lo que impide un análisis cuantitativo directo mediante sistemas de bases de datos tradicionales. En cuarto lugar, la disponibilidad de herramientas automatizadas, accesibles y adaptadas al contexto local es limitada, lo que dificulta la detección oportuna de tendencias específicas y la generación de avisos automáticos. Finalmente, la implementación de sistemas de recolección persistente debe conciliarse con los marcos éticos y legales vigentes, en especial la Ley Nacional 25.326 de Protección de Datos Personales.

Un aspecto que este trabajo incorpora explícitamente al planteamiento del problema es la **restricción de acceso programático** a las plataformas. La disponibilidad de interfaces de programación cambió de forma sustancial durante los últimos años: los accesos gratuitos a archivos históricos de terceros fueron discontinuados y las interfaces oficiales quedaron sujetas a autenticación, cuotas y políticas de uso que condicionan tanto el volumen como la profundidad temporal de la recolección posible. El diseño del sistema debió asumir esa restricción como una variable del problema y no como un detalle de implementación, tal como se documenta en el Capítulo 2 y en el Anexo B.

##  1.3. Justificación del proyecto

La viabilidad de implementar sistemas basados en OSINT en ciberseguridad se fundamenta en su bajo costo operativo, su alta accesibilidad y la riqueza de la información disponible públicamente. Automatizar la captura y el procesamiento de estos datos permite reducir el esfuerzo manual de los equipos de seguridad, de modo que los analistas concentren su capacidad en la toma de decisiones estratégicas de mitigación y en la respuesta ante incidentes (Russell y Klassen, 2019). La justificación de este proyecto radica en proponer una solución tecnológica robusta, modular y de bajo costo para el contexto argentino. La integración de n8n como orquestador de flujos visuales tipo ETL permite una alta adaptabilidad para incorporar nuevas fuentes sin reescribir componentes de infraestructura, mientras que la persistencia en PostgreSQL garantiza un almacenamiento relacional íntegro y auditable, y el clasificador heurístico en español aporta la capacidad de estructurar y categorizar automáticamente el contenido en el idioma local.

La elección de un clasificador por diccionario —en lugar de un modelo estadístico o de un modelo de lenguaje— responde a tres razones explícitas: la interpretabilidad del resultado (cada categoría se puede explicar por los términos que la activaron), el costo computacional nulo en términos de infraestructura de entrenamiento y la adecuación al alcance de un trabajo final de tecnicatura. Esa decisión tiene un costo conocido, que este informe declara: el diccionario no lematiza, de modo que reconoce variantes flexivas solo cuando están incluidas como términos, y su desempeño depende de la cobertura léxica del dominio.

##  1.4. Delimitación y alcance

**Delimitación de fuentes.** Se seleccionó la plataforma Reddit como caso de estudio y fuente principal por su estructura temática organizada en *subreddits*, que permite acotar la búsqueda a comunidades donde se agrupan usuarios con interés en tecnología, desarrollo de software y seguridad informática. La recolección se realiza sobre las **fuentes públicas de sindicación RSS/Atom** que la plataforma expone (`https://www.reddit.com/r/<comunidad>/new/.rss?limit=100`), sin autenticación, y no sobre la interfaz de programación con OAuth2. Las consecuencias de esa elección —menor profundidad temporal, dependencia del tamaño del *feed* y exposición a limitación de tasa— se describen en 2.1.2 y se cuantifican en el Capítulo 5.

**Delimitación de alcance.** El trabajo se orienta al monitoreo de **comunidades técnicas de Reddit**, no a la cobertura territorial de un país. El territorio argentino opera como **caso de aplicación**, no como alcance del corpus: la relevancia local se expresa en el vocabulario y en la incorporación de **r/devsarg** (comunidad de desarrolladores argentinos), junto con **r/Malware** y **r/netsec** (comunidades internacionales de análisis técnico, incorporadas por su densidad de reportes verificables). El diccionario incluye términos de uso local en español rioplatense. Como se documenta en el Capítulo 5, las comunidades internacionales concentran las detecciones verificables; el aporte localizable del sistema es el **léxico rioplatense**, no una cobertura geográfica. Las comunidades **r/argentina** y **r/derechogenial** fueron dadas de baja del monitoreo activo (`active_monitoring = false`) después de la evaluación preliminar, porque no aportaron detecciones de amenaza y su inclusión elevaba el ruido del corpus: el canal legal registró 0 amenazas reales sobre 10 publicaciones etiquetadas y 3 falsos positivos del clasificador. Esa decisión se documenta y se cuantifica en 5.2 y 6.3.

**Delimitación temporal.** La ventana nominal de recolección (B5) se declaró el 25/09/2026; el primer registro persistido corresponde al **01/10/2026** y el último día con recolección oficial es el **17/10/2026**, fecha en la que se fijó el corte. La ventana se cerró al alcanzar el objetivo de **15 fechas de evaluación** registradas por el motor de anomalías (mínimo exigido: 10). La recolección posterior al corte existe y continúa como track secundario de respaldo, pero **no integra el corpus evaluado** de este informe.

**Delimitación temática.** El análisis semántico se restringe a incidentes y discusiones de seguridad de la información: *malware*, vulnerabilidades, *phishing*, robo de credenciales, filtración de datos, *ransomware*, infraestructura y ataques, hacktivismo e ingeniería social. La taxonomía vigente del clasificador contiene 9 categorías y 201 términos; en el corpus analizado se activaron 8 de esas 9 categorías.

**Fuera de alcance.** No forman parte de este trabajo: la recolección de comentarios (la tabla `comments` del modelo existe pero no se pobló en la ventana evaluada), las fuentes que requieren credenciales o consentimiento (mensajería privada, foros cerrados, *dark web*), la ejecución de un banco de pruebas comparativo contra herramientas comerciales o de código abierto sobre el mismo corpus, y la verificación de envío real de alertas a un canal externo.

## 1.5. Objetivos de la investigación

**Objetivo general.** Diseñar, desarrollar, implementar y evaluar un sistema automatizado de monitoreo basado en el paradigma OSINT, utilizando las fuentes públicas de Reddit, la herramienta de orquestación de flujos n8n y el motor de base de datos PostgreSQL, capaz de recolectar, procesar, estructurar, analizar y generar avisos diarios sobre incidentes de ciberseguridad en comunidades técnicas de Reddit, con atención al léxico rioplatense, de manera eficiente, auditable y con estricto apego al marco legal nacional.

**Objetivos específicos.**

**OE1.** Recolectar automáticamente publicaciones desde las **fuentes públicas de Reddit (RSS/Atom)** de las comunidades seleccionadas, gestionando de manera explícita las restricciones de tasa de la plataforma y documentando el efecto de esas restricciones sobre el alcance temporal del corpus.

**OE2.** Diseñar e implementar flujos de trabajo robustos en n8n para la extracción, limpieza, normalización y transformación de los datos, garantizando la **idempotencia** del pipeline y su recuperación ante fallos parciales de las fuentes.

**OE3.** Modelar y desplegar una base de datos relacional PostgreSQL con restricciones de integridad referencial e índices orientados a las consultas analíticas, para el almacenamiento seguro de los metadatos y contenidos recolectados.

**OE4.** Desarrollar un componente de procesamiento de lenguaje natural en español capaz de categorizar semánticamente los textos y extraer entidades tecnológicas críticas, y describir con precisión su alcance y sus límites.

**OE5.** Implementar un motor de reglas estadísticas para la detección automática de anomalías y tendencias emergentes en el flujo continuo de datos.

**OE6.** **Diseñar y configurar** un sistema automatizado de generación de alertas integrado con plataformas de mensajería, dejando explícito su estado operativo al cierre de la ventana.

**OE7.** Evaluar cuantitativamente el rendimiento del sistema mediante métricas de precisión, *recall*, F1-score y latencia en un entorno operativo real, comparando cada resultado con los umbrales declarados en 1.6 —con su momento de fijación— e informando la tasa de falsos descubrimientos como complemento de la precisión, y delimitar explícitamente qué dimensiones del rendimiento no se evaluaron (la capacidad de proceso).

**OE8.** Analizar los aspectos legales, regulatorios y éticos vinculados a la recolección y el procesamiento de datos de fuentes abiertas en Argentina, implementando mecanismos efectivos de seudonimización en cumplimiento de la Ley 25.326.

## 1.6. Supuesto de trabajo y criterios de éxito

De acuerdo con la metodología *Design Science Research* (DSR) adoptada, se establece el siguiente supuesto de trabajo:

> Un sistema de monitoreo OSINT de código abierto, basado en n8n y PostgreSQL, con un componente de clasificación heurística especializado en español, puede automatizar la detección de incidentes de ciberseguridad en comunidades de Reddit con niveles de precisión y sensibilidad operativamente útiles, y a una fracción del costo de las soluciones propietarias.

**Criterios de éxito y momento de fijación.** Los umbrales de evaluación se establecieron en la etapa de diseño, antes de la fase de recolección, como una **decisión de diseño propia** del trabajo, adoptando el valor usual del 80 % en métricas de clasificación como referencia práctica y ajustándolo a los objetivos operativos del usuario final del sistema. No se atribuyen a una fuente que fije esos umbrales: el relevamiento de Pastor-Galindo et al. (2020) describe oportunidades y desafíos del uso de OSINT, pero no prescribe umbrales de precisión ni de sensibilidad, de modo que se lo cita por el contexto del campo y no como origen del valor. No todos los criterios tienen el mismo origen temporal, y la Tabla 1.1 lo declara criterio por criterio: confundir un umbral fijado en el diseño con uno incorporado después de conocer resultados convertiría la evaluación en una validación circular.

**Tabla 1.1. Criterios de éxito, momento de fijación y estado en la V5**

| Criterio | Umbral | Momento de fijación | Estado |
|----|----|----|----|
| Precisión de la clasificación | ≥ 80 % | Diseño, antes de la recolección. Reformulado desde el 82 % inicial en la V4 (19/10/2026), con la razón declarada abajo | Se evalúa en 5.5 |
| Sensibilidad (*recall* de clasificación) | ≥ 80 % | Diseño, antes de la recolección; sin cambios | Se evalúa en 5.5 |
| F1-score de clasificación | ≥ 0,80 | **Incorporado en la V4** (19/10/2026), con posterioridad al cierre de la ventana B5; no es un umbral del diseño | Se evalúa en 5.5 |
| Latencia extremo a extremo | ≤ 5 minutos | Diseño, antes de la recolección; sin cambios | **NO CUMPLIDO** (5.3) |
| Throughput del pipeline | ≥ 1.000 posts/hora | Diseño, antes de la recolección; sin cambios | **NO EVALUADO** (5.8): no se midió capacidad |
| Cobertura de recolección | ≥ 80 % | Diseño, antes de la recolección | **Retirada** (ver nota) |

> **Nota metodológica sobre la cobertura.** La versión previa de este informe declaraba un criterio de cobertura del 80 % y lo reportaba como superado. La V4 **retira ese criterio**. La razón es que su verificación requiere un diseño de captura–recaptura sobre fuentes independientes, y este trabajo dispone de una única fuente y de una única captura: cualquier cifra de cobertura calculada sobre el propio corpus sería un cociente sin denominador verificable. El tribunal de la V3 admitió explícitamente esta salida —retirar la métrica antes que presentarla como parcial sin justificación—. En consecuencia, la cobertura no aparece en el Resumen, en el Capítulo 5 ni en el Capítulo 7, y el análisis de la *representatividad* del corpus se hace de forma cualitativa y con las limitaciones declaradas en 6.3.
>
> **Nota metodológica sobre la tasa de falsos descubrimientos.** La tasa de falsos descubrimientos, `FP / (TP + FP)`, **no se cuenta entre los criterios de éxito**. La razón es algebraica y estaba reconocida en la versión anterior sin consecuencias prácticas: sin falsos negativos en el denominador, esa tasa es exactamente `1 − precisión`, de modo que presentarla como un criterio separado duplicaba el mismo resultado y sugería una validación más amplia que la realmente existente. Se informa en 5.5 como **complemento informativo de la precisión**, con un valor de referencia de ≤ 20 % y su intervalo de confianza, pero no se contabiliza como criterio alcanzado en 5.8 ni en 7.1.
>
> **Nota metodológica sobre el F1-score.** El F1-score se incorpora como criterio **en la V4** (19/10/2026), después del cierre de la ventana B5 y de conocerse la evaluación de la versión anterior, y se declara con esa fecha para no atribuirle un origen que no tiene. Su función es resumir en un solo valor el equilibrio entre precisión y sensibilidad, que hasta entonces se informaban por separado; su umbral de 0,80 se alinea con los de ambas, de modo que no introduce una exigencia adicional, sino una lectura conjunta. Al derivarse algebraicamente de precision y sensibilidad, se informa siempre acompañado de los dos valores que lo componen.
>
> **Nota metodológica sobre el cambio de umbral de clasificación.** La versión previa declaraba los umbrales de clasificación en 82 % de precisión y 18 % de falsos descubrimientos. Se declara aquí que ambos valores **se modificaron a 80 % y 20 % en la V4 (19/10/2026)** y se explicita la razón: las dos cifras eran complementarias —`FP / (TP + FP) = 1 − precisión` cuando no se cuentan los falsos negativos en el denominador—, de modo que no eran dos criterios sino uno expresado dos veces, y el valor 82 % no tenía derivación declarada. En esta versión se conserva un único umbral de precisión del 80 %, alineado con el valor que la tabla aplica también a sensibilidad y a F1, y la tasa de falsos descubrimientos se reporta como su complemento explícito. El cambio es previo a la observación de resultados y **no altera el valor de la precisión**, que supera ambos conjuntos de umbrales (84,7 % frente a 82 % y 80 %). Tampoco altera la conclusión general de la V5, que no depende de él: la sensibilidad (61,2 %) y el F1 (0,711) quedan por debajo del 80 % y se informan como no cumplidos (5.5).

**Cronología de los criterios.** Tres precisiones hacen auditable la evaluación. Primera: la precisión, la sensibilidad, la latencia, el throughput y la cobertura se fijaron en el diseño, antes de que existiera un solo registro de la ventana B5. Segunda: el **F1-score** y la **reformulación de los umbrales de clasificación de 82 %/18 % a 80 %/20 %** se incorporaron en la V4, el 19/10/2026, es decir después del cierre de la ventana (17/10/2026) y de conocerse la evaluación de la versión anterior; se declaran como decisiones posteriores y no se presentan como a priori. Tercera: **desde la V4 no se modificó ningún umbral**, y los resultados del Capítulo 5 se informan contra los valores de la Tabla 1.1. El criterio de latencia no se alcanza y se informa como no cumplido; el de throughput se declara **no evaluado** porque no se midió la capacidad del artefacto. Ambos se retoman en los Capítulos 5, 6 y 7.

## 1.7. Preguntas de investigación

**PI-1.** ¿En qué medida un sistema basado en herramientas de código abierto (n8n y PostgreSQL) puede ofrecer una arquitectura técnicamente viable y de bajo costo en comparación con soluciones propietarias de monitoreo OSINT, en términos de costo, flexibilidad y rendimiento medible sobre el mismo dominio de datos?

**PI-2.** ¿Cuáles son los principales patrones temporales y temáticos de incidentes de ciberseguridad discutidos en comunidades técnicas de Reddit durante el período relevado, y en qué medida el léxico rioplatense aporta detecciones que un léxico solo en inglés no captaría?

**PI-3.** ¿Cómo afectan las restricciones de acceso programático de las plataformas —cuotas, políticas de uso y discontinuación de archivos históricos— a la cobertura y a la profundidad temporal de un pipeline de ingesta automatizado?

**PI-4.** ¿De qué manera se puede proteger la privacidad de los usuarios en un sistema de monitoreo público persistente, en cumplimiento de la normativa argentina?

# CAPÍTULO 2: MARCO TEÓRICO Y ESTADO DEL ARTE

## 2.1. Marco conceptual

### 2.1.1. Inteligencia de fuentes abiertas (OSINT)

El término Inteligencia de Fuentes Abiertas (*Open Source Intelligence*, OSINT) se refiere al proceso sistemático y estructurado de recopilar, procesar, analizar y explotar datos de acceso público en internet para convertirlos en inteligencia accionable destinada a la toma de decisiones estratégicas, operativas o tácticas (Russell y Klassen, 2019). El OSINT se rige por un ciclo de inteligencia clásico de cinco fases: planificación y dirección, recolección de datos, procesamiento y estructuración, análisis y producción de inteligencia, y difusión (Pastor-Galindo et al., 2020). Este trabajo se apoya en ese ciclo como esquema organizativo: la planificación y la dirección corresponden a la definición de objetivos y criterios del Capítulo 1; la recolección y el procesamiento, al pipeline descrito en el Capítulo 4; y el análisis, la producción y la difusión, al motor de anomalías y al módulo de alertas.

Las fuentes OSINT se clasifican en varias categorías: registros de dominios y bases de datos de DNS, repositorios de código público, motores de búsqueda especializados de infraestructura y medios sociales. Los medios sociales y los foros interactivos representan una subcategoría crítica conocida como *Social Media Intelligence* (SOCMINT). A diferencia del OSINT técnico, centrado en infraestructura, SOCMINT se ocupa del contenido generado por usuarios y aporta una perspectiva sobre las dinámicas humanas detrás del ciberdelito: cómo se nombran los incidentes, qué se discute antes de que exista un reporte oficial y qué vocabulario circula en una comunidad determinada (Glassman y Kang, 2012). Este trabajo se ubica en esa subcategoría.

### 2.1.2. Reddit como fuente de inteligencia

Reddit se organiza en foros moderados y autogestionados denominados *subreddits*. Su naturaleza pseudónima y su enfoque comunitario orientado a la discusión técnica atraen a ingenieros de software, administradores de sistemas e investigadores de seguridad. A diferencia de las plataformas de microblogging, Reddit fomenta publicaciones extensas y debates detallados organizados en hilos ramificados (Russell y Klassen, 2019), lo que resulta especialmente adecuado para un clasificador que opera sobre texto.

El acceso automatizado a Reddit atravesó cambios regulatorios sustanciales entre 2023 y 2026. Tras la modificación de los términos de servicio de su interfaz de programación en 2023, se discontinuó el acceso libre a plataformas de archivo histórico de terceros, el acceso programático gratuito pasó a exigir autenticación mediante OAuth2 y quedó sujeto a un límite nominal de consultas por minuto, además de un techo de aproximadamente 1.000 ítems por punto de acceso de listado (Reddit Inc., 2026).

En el contexto de este proyecto, ese régimen de acceso tuvo una consecuencia concreta que condicionó el diseño: el endpoint público en formato JSON resultó inaccesible por política de la plataforma —la respuesta observada fue **HTTP 403**, no un error de cuota—, de modo que la recolección se instrumentó sobre las **fuentes de sindicación RSS/Atom** que la plataforma expone en `https://www.reddit.com/r/<comunidad>/new/.rss?limit=100`, que no requieren autenticación. La caracterización de ese acceso, documentada en `V4/evidencias/CARACTERIZACION_RATE_LIMIT.md` (2026-09-25, revisada el 2026-09-30), establece lo siguiente:

El síntoma relevante es **HTTP 429 (Too Many Requests)** ante el exceso de solicitudes desde la dirección del proyecto, y su alcance es la descarga del *feed*: la comunidad afectada puede quedar con **0 publicaciones en el ciclo**.

El **umbral exacto** de solicitudes que dispara el 429 quedó registrado como `no determinado`: aislarlo empíricamente habría requerido generar más solicitudes, es decir, más bloqueos y más sesgo de cobertura. La guía del proyecto menciona un valor de referencia público del orden de 10 solicitudes por minuto, pero ese valor no fue verificado empíricamente para la dirección del proyecto.

La mitigación vigente combina tres mecanismos: una **espera fija de 60 segundos** entre comunidades (una solicitud por minuto, por debajo del valor de referencia), reintentos acotados ante respuestas 429/403 y un **centinela** que cierra el ciclo del lazo de control cuando una fuente devuelve cero elementos, de modo que el resto de las comunidades no se saltee silenciosamente.

El efecto residual sobre el corpus es un **sesgo por comunidad**: una comunidad puede no aportar datos en un ciclo determinado sin que el sistema lo declare como error. Ese efecto se midió el 02/10/2026: de 28 corridas automáticas, **15 fueron incompletas (53,6 %)**, concentradas en la comunidad que recibe el tercer turno del ciclo (`V4/evidencias/VENTANA_B5.md`, §13).

Las RSS/Atom, a diferencia de la interfaz con autenticación, no exponen métricas de interacción ni el árbol de comentarios, y devuelven solo los elementos más recientes del listado (hasta 100 por consulta). Esas dos limitaciones explican por qué la tabla `comments` del modelo quedó sin poblar y por qué la profundidad temporal del corpus es acotada.

### 2.1.3. Ciencia de datos, minería de datos y procesamiento de lenguaje natural

Para transformar el texto no estructurado en datos cuantitativos legibles por máquinas es indispensable articular técnicas de ciencia de datos, minería de datos y procesamiento de lenguaje natural. La minería de datos se ocupa de la extracción de patrones y relaciones en conjuntos de datos (Han et al., 2012); el procesamiento de lenguaje natural provee el marco algorítmico para que los programas interpreten y procesen lenguaje humano en formato digital (Jurafsky y Martin, 2009).

El pipeline de NLP **previsto en el diseño** contemplaba tokenización, normalización (minúsculas y remoción de caracteres especiales), eliminación de palabras vacías (*stop words*) y lematización morfológica para reducir cada palabra a su raíz. El pipeline **efectivamente implementado** es más acotado y conviene describirlo con precisión, porque de esa diferencia depende la interpretación de los resultados del Capítulo 5:

**Normalización**: conversión a minúsculas y remoción de diacríticos mediante descomposición Unicode NFD. Esto resuelve el tratamiento de tildes sin afectar la comparación, porque la normalización se aplica tanto al texto como a los términos del diccionario.

**Tokenización**: segmentación del texto por todo carácter que no sea alfanumérico, lo que produce un conjunto de palabras.

**Coincidencia**: los términos de una sola palabra se buscan por **igualdad exacta** contra ese conjunto; los términos compuestos se buscan por **coincidencia de subcadena** sobre el texto normalizado.

**Ausencia de lematización y de eliminación de palabras vacías**: no se aplica *stemming* ni lematización morfológica, y no se remueven *stop words*. En consecuencia, una variante flexiva que no esté incluida como término del diccionario no se reconoce por su raíz; la mitigación adoptada es incluir las variantes más frecuentes del dominio como términos independientes.

Esta decisión de ingeniería prioriza la interpretabilidad y el costo computacional nulo en infraestructura: cada categoría asignada es explicable por los términos que la activaron, y no requiere entrenamiento ni dependencias de modelos preentrenados. Su costo es un techo de desempeño asociado a la cobertura léxica, que se discute en 6.3.

### 2.1.4. Arquitecturas ETL y herramientas de automatización

Un pipeline de datos robusto para el monitoreo automatizado se rige por el patrón de diseño ETL (*Extract, Transform, Load*). En este sistema, la extracción consulta las fuentes públicas de sindicación; la transformación limpia, normaliza, seudonimiza y clasifica; y la carga persiste los registros en la base relacional. Para coordinar el flujo de manera modular y tolerante a fallos se adoptó **n8n** en su versión **2.40.6**, desplegada en Docker: una plataforma de automatización de flujos de trabajo de código abierto que permite integrar fuentes, bases de datos y servicios de mensajería mediante una interfaz visual y lógica programática en JavaScript (n8n GmbH, 2026). La persistencia se realiza en **PostgreSQL 18**, con un modelo relacional que se describe en el Capítulo 4 (PostgreSQL Global Development Group, 2026).

La elección de n8n sobre una alternativa basada en scripts propios responde a razones verificables en el desarrollo de este trabajo: el disparador temporal, el control de concurrencia por lotes, la espera entre solicitudes, el manejo de errores por nodo y la sentencia de *upsert* son componentes nativos, y el flujo completo queda exportable como un artefacto versionable (Anexo B). Esa exportabilidad es la que permite auditar que lo descrito en el informe coincida con lo ejecutado.

## 2.2. Estado del arte y brecha de conocimiento

En el ámbito profesional y académico existen herramientas consolidadas para la recolección de información OSINT. Entre las soluciones de código abierto de mayor difusión se destacan SpiderFoot, Maltego CE, theHarvester, Recon-ng:

**SpiderFoot** automatiza el escaneo de infraestructura técnica (direcciones IP, subdominios, certificados) y el enriquecimiento de indicadores, pero no ofrece análisis semántico profundo sobre contenido social en español.

**Maltego CE** provee un motor sólido de visualización de grafos de relaciones, pero requiere ejecuciones manuales y sus transformaciones para foros sociales en español son limitadas.

**theHarvester** y **Recon-ng** están orientadas al reconocimiento pasivo en pruebas de penetración, sin capacidad de monitoreo temporal continuo ni de clasificación temática de texto libre.

En el plano académico, Liao et al. (2016) abordan la extracción automática de indicadores de compromiso desde fuentes abiertas de inteligencia de amenazas y muestran que la calidad de los indicadores depende críticamente de la normalización y del filtrado del texto; ese hallazgo es directamente aplicable a la decisión de este trabajo de priorizar la trazabilidad de cada categoría asignada. Zong et al. (2019) analizan la severidad percibida de las amenazas de ciberseguridad a partir del lenguaje con que se las describe en redes sociales y muestran que ese lenguaje es ruidoso, heterogéneo y dependiente del contexto en que se publica; ese rasgo condiciona cualquier clasificación automática construida sobre texto social. El desafío se manifestó en este proyecto de forma desigual: **una de las tres comunidades relevadas —r/devsarg— publica en español rioplatense**, mientras que las otras dos (r/netsec y r/Malware) escriben en inglés, y **son estas las que concentran la mayoría de las detecciones**. El castellano local, con sus modismos, aparece en una fracción menor del corpus; el diccionario que los incorpora se evalúa, por lo tanto, principalmente sobre texto en inglés, como se declara en 5.5 y 7.3.

**Antecedente directo de la misma casa de estudios.** Dengra y Rivas (2026) presentan el *Observatorio OSINT: Diseño e implementación de un sistema de recolección y análisis del discurso público sobre ciberseguridad en Bluesky en América Latina y el Caribe*, Trabajo Final de Carrera de la misma carrera y facultad, dirigido por el mismo director que este trabajo. Por tratarse de un trabajo inédito, sus cifras se citan según la versión consultada el 15/10/2026 y pueden variar en versiones posteriores (véase Referencias). El antecedente es de lectura obligada porque comparte objetivo general y difiere en decisiones estructurales. El contraste se resume en seis puntos:

**Fuente y acceso.** El antecedente consume la interfaz pública de Bluesky (AT Protocol) con autenticación; este trabajo consume las fuentes públicas RSS/Atom de Reddit, precisamente porque la interfaz JSON resultó inaccesible por política de la plataforma. La vía elegida evita el bloqueo, pero limita los campos disponibles y la profundidad del listado.

**Escala y ventana.** El antecedente reporta **3.908 publicaciones** en **847 fechas** y cinco países; este trabajo reporta **724 publicaciones** en **16 fechas con recolección** y **15 fechas de evaluación**, sobre tres comunidades. La diferencia de escala es de un orden de magnitud y acota el alcance de las conclusiones de este informe.

**Sesgo de recencia.** El antecedente mide un sesgo de paginación severo (la primera página concentra el 54,1 % del contenido de los últimos seis meses y desde la cuarta página la recuperación cae a cero) y lo corrige ampliando la ventana de recolección. Este trabajo opera sobre el listado de novedades, por lo que su corpus está sesgado hacia lo reciente en la misma dirección: se declara en 6.3 y no se corrige.

**Clasificación.** El antecedente recupera por palabras clave y valida manualmente la **relevancia**; no categoriza. Este trabajo añade una taxonomía de 9 categorías y 201 términos, lo que habilita el análisis temático pero introduce una fuente de error que el antecedente no tiene. El antecedente documenta, además, un caso de ruido por coincidencia léxica (la palabra clave «CERT» resultó ruidosa en aproximadamente el **83 %** de los casos por colisión con la raíz «cert-» en portugués y catalán) y opta por retirarla; ese episodio es evidencia externa y contemporánea de que la coincidencia léxica sin lematización produce falsos positivos, exactamente el fenómeno que este trabajo declara como limitación propia.

**Validación y fiabilidad.** El antecedente construye una muestra de **n = 80** con semilla fija, script versionado y hash del archivo de origen, y la anota con **dos** evaluadores para calcular el **kappa de Cohen** (κ = 0,356 para relevancia temática y κ = 0,758 para país). Este trabajo etiqueta **n = 352** —censo de las 170 predicciones positivas y muestra de 182 del estrato negativo— con **tres** anotadores y reporta **κ de Fleiss = 0,509** sobre 50 casos comunes, por debajo del 0,61 comprometido. La comparación sigue siendo incómoda y se declara: el antecedente alcanza un acuerdo sustancial en una de sus dos dimensiones (0,758) y este trabajo no llega al umbral que fijó para sí mismo, aunque ahora dispone del mecanismo de fiabilidad que antes no tenía.

**Marco legal y reutilización.** El antecedente invoca la Ley 25.326 y recomienda seudonimizar los identificadores antes de publicar los datos, además de advertir que la recolección multi-jurisdiccional exige adoptar el criterio más estricto disponible. Este trabajo aplica seudonimización con clave en la etapa de ingesta, lo que respalda y anticipa esa recomendación.

**Brecha de conocimiento.** La brecha que este trabajo aborda no es la ausencia de herramientas OSINT, sino la ausencia de un **sistema de monitoreo continuo y de bajo costo, con clasificación temática auditable y un mecanismo de detección temporal sobre comunidades técnicas de Reddit**, allí donde las herramientas relevadas se orientan al reconocimiento puntual de infraestructura y no al seguimiento sostenido de contenido social. La reformulación del alcance se declara con precisión, porque la versión previa la sostenía sobre un objeto distinto: **el objeto de este trabajo son comunidades técnicas de Reddit, no la cobertura territorial de un país ni las comunidades de habla hispana en general**. Una de las tres comunidades relevadas (r/devsarg) publica en español rioplatense; las otras dos (r/netsec y r/Malware), incorporadas por su densidad de reportes verificables, publican en inglés y **concentran la mayoría de las detecciones**. El componente local de este trabajo es, por lo tanto, **exploratorio**, y así debe leerse.

Lo que la brecha retiene como aporte es acotado y verificable. Las herramientas relevadas asumen el inglés como idioma estándar y no contemplan los modismos con los que los usuarios locales discuten estafas o incidentes: una caída de servicio se narra como «tiraron el sitio» o «se cayeron los servidores», una apropiación de cuenta como «me robaron la contraseña» o «me tomaron el control de la cuenta», y una extorsión como «me piden rescate» o «me bloquearon los archivos». Esos giros no aparecen en los vocabularios técnicos en inglés, y un analista local necesita leerlos. El diccionario de este trabajo los incorpora de forma explícita (`tiraron el sitio`, `caeron los servidores`, `robaron mi contrasena`, `tomaron control de la cuenta`, `piden rescate`, `bloquearon mis archivos`, entre otros; Anexo C), y la contrapartida de esa decisión —comparar cadenas sin lematizar— es la causa de la mayoría de los falsos positivos declarados en 6.3. Ese aporte de vocabulario **se ilustra con los dos casos locales** documentados en 6.2, no se verifica como propiedad poblacional del sistema. Los trabajos académicos disponibles o bien se centran en indicadores técnicos (Liao et al., 2016), o bien analizan el lenguaje de las amenazas sobre plataformas globales en inglés, sin anclaje local (Zong et al., 2019). El antecedente de Dengra y Rivas (2026) cubre el análisis del discurso en otra plataforma y con otro método. Este trabajo aporta, sobre esa base, un artefacto que además de recolectar y clasificar incorpora un motor de detección de anomalías con umbral estadístico explícito (Capítulo 4, sección 4.5) y un corpus fechado, auditable y con trazabilidad por consulta.

# CAPÍTULO 3: MARCO METODOLÓGICO

## 3.1. Tipo y diseño de la investigación

La presente investigación se enmarca en la modalidad de investigación aplicada tecnológica. Su propósito no se restringe a la teorización conceptual, sino al desarrollo, la validación y la evaluación de un artefacto de software concreto orientado a resolver una problemática operativa real. Para estructurar el desarrollo se adoptó el modelo de proceso de la *Design Science Research* (DSR) de seis fases —identificación del problema, definición de objetivos, diseño y desarrollo, demostración, evaluación y comunicación— (Peffers et al., 2007), complementado con los principios generales de diseño de artefactos tecnológicos (Hevner et al., 2004). La Tabla 3.1 explicita cómo se aplicó cada fase y qué producto verificable dejó cada una.

**Tabla 3.1. Aplicación de las fases de la DSR al trabajo**

| Fase DSR | Aplicación en este trabajo | Producto verificable |
|----|----|----|
| 1\. Identificación del problema | Dispersión, volumen y falta de estructura de los datos de ciberseguridad en comunidades técnicas de Reddit, con el léxico local como componente exploratorio; restricciones de acceso programático | Capítulo 1, §1.1–1.2; `CARACTERIZACION_RATE_LIMIT.md` |
| 2\. Objetivos y criterios de éxito | Automatización, estructuración, categorización y alerta; umbrales cuantitativos con su fecha de fijación | Capítulo 1, §1.6 |
| 3\. Diseño y desarrollo | Pipeline en n8n, modelo relacional, clasificador por diccionario, motor de anomalías | Capítulo 4; `A_DDL.sql`; `B_workflow.json` |
| 4\. Demostración | Recolección continua sobre tres comunidades; primera corrida con datos: 01/10/2026; corte: 17/10/2026 | `VENTANA_B5.md`; bitácora diaria |
| 5\. Evaluación | Muestra de control etiquetada (30/09/2026) y lecturas de solo lectura sobre el corpus cerrado (19/10/2026) | `evaluacion_muestra_control_2026-09-30.*`; consultas archivadas |
| 6\. Comunicación | Informe académico y documentación técnica del repositorio | Este documento; anexos A–E |

> **Iteración declarada sobre las fuentes (fase 3 → fase 4).** La composición de comunidades relevadas **cambió durante el desarrollo y esa iteración se declara aquí**: la configuración inicial incluía **r/argentina** y **r/DerechoGenial** junto con **r/devsarg**; tras la evaluación preliminar, las dos primeras se dieron de baja del monitoreo activo (`active_monitoring = false`) por no aportar detecciones de amenaza y elevar el ruido del corpus, y se incorporaron **r/netsec** y **r/Malware** por su densidad de reportes verificables. Es una iteración legítima dentro del ciclo DSR, pero **cambia el objeto de estudio**: el corpus evaluado no representa «comunidades vinculadas a Argentina», sino **comunidades técnicas de Reddit** de las cuales solo `r/devsarg` es local. El alcance real se reformula en consecuencia en 1.4, 2.2, 5.1 y 7.3.

La metodología DSR contempla explícitamente la iteración entre fases. En este trabajo la iteración fue real y dejó huella documental: el primer corpus (denominado B4, 24/09/2026) fue descartado porque el diccionario y el umbral de coincidencia vigentes en ese momento producían una clasificación deficiente, y la recolección se reinició con el clasificador corregido. El corpus evaluado en este informe es el posterior a esa corrección. Una segunda iteración, independiente del clasificador, afectó a las **fuentes**: las comunidades relevadas se reconfiguraron después de la evaluación preliminar, con la baja de `r/argentina` y `r/DerechoGenial` y la incorporación de `r/netsec` y `r/Malware` (véase la nota bajo la Tabla 3.1). Ambas iteraciones se documentan porque, juntas, explican por qué el corpus y el alcance de este informe difieren de los de las configuraciones previas.

## 3.2. Operacionalización del protocolo de recolección

Para garantizar la reproducibilidad del estudio se formalizó el protocolo operativo de extracción con los siguientes parámetros:

**Unidad de análisis.** La publicación (*post*). Cada fila del corpus corresponde a una publicación identificada por su identificador original de la plataforma, que actúa como clave primaria. Los comentarios no se recolectan (ver 1.4 y 4.3).

**Fuente y comunidades.** Tres comunidades con monitoreo activo: `r/netsec`, `r/Malware` y `r/devsarg`. La fuente es el listado público de novedades en formato RSS/Atom de cada comunidad, con un máximo de 100 elementos por consulta.

**Ciclo de ingesta.** El disparador opera cada **15 minutos**; en cada ciclo se recorre la lista de comunidades activas con un tamaño de lote de uno y una **espera fija de 60 segundos** entre solicitudes, por debajo del valor de referencia de tasa observado. Ante una respuesta 429 o 403 se reintenta hasta tres veces con una espera acotada entre intentos, y un centinela garantiza que el ciclo del lazo se cierre de manera consistente cuando una fuente no devuelve elementos.

**Deduplicación e idempotencia.** La clave primaria es el identificador de la publicación y la carga se realiza mediante `INSERT … ON CONFLICT (id) DO UPDATE`, de modo que reprocesar el mismo elemento actualiza el registro en lugar de duplicarlo. La cláusula de actualización enumera nueve campos (sección 4.3, Anexo B) y deja intactas `created_utc` e `ingested_at`, de modo que la relectura del feed no altera las fechas del registro. La propiedad de idempotencia se verificó ejecutando el flujo más de una vez sobre el mismo conjunto de entrada.

**Ventana temporal.** Ventana nominal declarada el **25/09/2026**; primer registro persistido el **01/10/2026**; último día con recolección oficial el **17/10/2026**. El corte del corpus es un **instante** fijo —el inicio del 18/10/2026, 00:00 hora local—, de modo que el acumulado no depende del momento en que se consulte; la ventana se declaró **cerrada el 19/10/2026**, fecha de las consultas de evidencia. Las tres fechas se informan siempre con ese significado: 17/10 último día recolectado, 18/10 instante de corte, 19/10 cierre y verificación.

**Criterio de cierre.** La ventana se cierra al alcanzar el objetivo declarado de **15 fechas de evaluación** registradas por el motor de anomalías, con un mínimo exigido de 10. La línea base del motor se calcula sobre los **diez días calendario previos** (5.4), de modo que diez jornadas de operación efectiva son el mínimo para que esa ventana no quede dominada por los primeros días del corpus, y quince dan margen para observarla evolucionar.

**Naturaleza del corpus.** El corpus es un **censo** de lo recolectado, no una muestra: se analizan todas las publicaciones persistidas en la ventana. No se aplica ningún filtro posterior a la ingesta.

**Muestreo de anomalías.** El motor no muestrea: cuenta las publicaciones por categoría y por día local, y evalúa cada categoría presente en una ventana móvil de once días (sección 4.5).

## 3.3. Protocolo de validación del clasificador NLP

Para hacer auditables las métricas de precisión, sensibilidad y F1-score del Capítulo 5, se describe a continuación el protocolo de construcción de la muestra de referencia. Se distingue de forma explícita entre el **protocolo diseñado** y la **ejecución real**, porque no coinciden, y porque la evaluación previa de este trabajo fue penalizada precisamente por presentar como ejecutado un diseño que no se había ejecutado.

### 3.3.1. Protocolo diseñado

El diseño previsto establecía: (a) una muestra aleatoria estratificada proporcional por comunidad de origen; (b) etiquetado **independiente** y ciego por parte de los integrantes del equipo; (c) cálculo del **acuerdo entre evaluadores** mediante el coeficiente kappa, adoptando el umbral de acuerdo sustancial (κ ≥ 0,61) establecido por Landis y Koch (1977); y (d) resolución de las discrepancias **por mayoría de votos** entre los evaluadores, tomando la etiqueta de consenso como referencia (*ground truth*) contra la cual medir el clasificador automático.

### 3.3.2. Ejecución real

El protocolo se ejecutó dos veces. La primera versión —50 publicaciones, un solo anotador, 30/09/2026— fue **reemplazada** por una validación nueva sobre el corpus B5, construida y etiquetada entre el 20/10/2026 y el 22/10/2026. Se informa la segunda como **medición vigente**; la primera se conserva en 5.5.1 como antecedente y como origen de la corrección del umbral del clasificador, y se explica allí por qué sus cifras no son comparables.

**Marco muestral y tamaño.** La validación se construyó sobre el corte del corpus de la ventana B5 (724 publicaciones; `created_utc < 2026-10-18 03:00:00+00` y `ingested_at < 2026-10-19 00:00:00+00`, que excluye el track posterior), estratificado por la predicción del clasificador:

| Estrato | Definición | Población | Etiquetadas | Fracción |
|----|----|---:|---:|----|
| 1 | Publicaciones marcadas como amenaza por el clasificador | **170** | **170** | censo (100 %) |
| 2 | Publicaciones marcadas como «No relevante» | **554** | **182** | 32,9 % sorteadas |
| **Total** |  | **724** | **352** | — |

El **estrato 1 se censó íntegro**, de modo que la precisión se mide sin error de muestreo. El estrato 2 se sorteó con semilla fija (**20261020**), orden determinista (`md5(id || '20261020')`) y corrección por población finita: con una omisión esperada del 22,7 % y un margen de ±5 pp al 95 %, `n = z²·p(1−p)/e²` con el ajuste `n/(1 + (n−1)/N)` arroja **n₀ = 182**. La diferencia entre esta cifra y las 554 de la población se declara en 3.3.3: es el precio de no censar el estrato negativo, y es lo que el peso de muestreo corrige.

**Cegamiento.** Las hojas de etiquetado excluyen `nlp_category`, `nlp_score`, el identificador de plataforma y el estrato de origen —«estrato 1» equivale a «el clasificador dijo amenaza» y habría revelado la predicción—. Los casos se presentan en **orden mezclado determinista** para que la posición no informe el estrato, y la correspondencia `código interno ↔ id/nlp/estrato` vive en un archivo separado que no se publica. La guía de etiquetado fija antes de anotar la definición operativa de amenaza, las diez categorías con ejemplos límite y las reglas de desempate.

**Anotadores y acuerdo.** Tres anotadores —los tres integrantes del equipo— etiquetaron por separado, sin comunicarse hasta cerrar su planilla. Los dos compañeros etiquetaron una **submuestra común de 50 casos** (25 del estrato 1 y 25 del estrato 2, en órdenes distintos); el tercer anotador etiquetó los 352 casos completos, de los cuales los 50 comunes se extraen por código.

**Kappa de Fleiss** sobre los 50 casos comunes: **κ = 0,509** (P_o = 0,700; P_e = 0,389), es decir **acuerdo moderado**.

Colapsado a la decisión binaria «amenaza / no relevante»: **κ = 0,570**, también moderado pero próximo al umbral sustancial.

**Desacuerdos: 20 de 50**. De ellos, **16** son discrepancias sobre la decisión binaria (alguien marcó «No relevante» y otro una categoría) y solo **4** son discrepancias de categoría con la misma decisión binaria.

**Adjudicación.** Los 20 desacuerdos se resolvieron **por consenso de los tres autores**, caso por caso, con la etiqueta adoptada y el motivo asentados en `evidencia-muestreo/adjudicacion_v5.xlsx`. Ninguna etiqueta fue decidida por un modelo de lenguaje: la asistencia generativa se limitó a la preparación de la guía, como se declara en la portada. La etiqueta de consenso es la referencia contra la cual se mide el clasificador.

**Diferencia con el protocolo diseñado.** El diseño preveía una muestra aleatoria estratificada *proporcional por comunidad*; la ejecución mantiene la estratificación pero **condicionada por la predicción del clasificador**, que es lo que hace estimable la precisión con denominador censado. Además, el umbral de acuerdo comprometido era κ ≥ 0,61 y la medición arrojó 0,509: **el umbral no se alcanzó**. Esa brecha no se corrige retocando la cifra; se declara aquí y se discute en 3.3.3 y 6.3.

### 3.3.3. Consecuencias declaradas del diseño

**El acuerdo está por debajo del umbral comprometido.** κ = 0,509 frente a κ ≥ 0,61. La lectura desagregada muestra dónde está el desacuerdo: 16 de los 20 casos discrepantes son discusiones sobre si hay amenaza, no sobre qué categoría asignarle. Es decir, **la frontera inestable es la definición operativa de amenaza**, no la taxonomía —al contrario de lo que sostenía la evaluación anterior, que atribuía los desacuerdos a la ambigüedad entre categorías—. La consecuencia práctica es que la etiqueta de referencia incorpora una cuota de criterio personal, y que las métricas del clasificador deben leerse con esa banda de incertidumbre y no como una verdad de referencia exenta de error.

**La sensibilidad es estimable, pero con la incertidumbre del muestreo del estrato negativo.** A diferencia de la evaluación previa, el diseño ahora permite estimarla con un intervalo exacto, porque el estrato «No relevante» se sorteó con tamaño calculado y peso declarado. Lo que no desaparece es el supuesto de que la omisión medida sobre las 182 sorteadas representa la de las 554: el intervalo de confianza exacto de esa omisión —**\[11,4 %; 22,7 %\]**— es la medida honesta de esa incertidumbre.

**La muestra ya pertenece al corpus analizado.** La validación previa se hizo sobre un corpus de septiembre que incluía comunidades desactivadas después (10 de sus 50 casos provenían de `r/DerechoGenial`, ausente de la ventana B5); esta se hizo sobre el corte exacto de 5.1. Por lo tanto, **las métricas de 5.5 describen el desempeño sobre el corpus del informe**, no sobre un corpus distinto.

**Sesgo endógeno del diseño.** Como toda muestra estratificada sobre la salida del propio sistema, la precisión se mide mejor que la cobertura: el estrato positivo está censado y el negativo, muestreado. El peso de muestreo corrige el sesgo del estimador, no la incertidumbre.

**El agente no etiqueta.** La preparación de la guía, el sorteo, el cálculo del acuerdo y de los intervalos son reproducibles por script; ninguna etiqueta del conjunto de referencia fue producida por un modelo de lenguaje.

### 3.3.4. Reproducibilidad de la medición

La validación V5 se apoya en tres scripts versionados y en archivos con hash, de modo que un tercero puede reconstruir cada cifra:

| Artefacto | Función |
|----|----|
| `sorteo_v5.py` | sorteó las 182 del estrato 2 y las 50 comunes con semilla 20261020 y `md5` determinista |
| `generar_evidencia_muestreo.py` | generó las hojas ciegas (sin `nlp_*`, sin `id`, sin estrato) en CSV y XLSX |
| `analizar_v5.py` | calculó el kappa de Fleiss, la matriz de confusión, los estimadores ponderados y los intervalos exactos |
| `muestra_v5_correspondencia.csv` | corresponde código interno con id/nlp/estrato; **no se publica** |
| `resultados_v5.json` / `.md` | salida literal de `analizar_v5.py` |

El cálculo no reimplementa el clasificador: parte de la etiqueta ya persistida en la base y de la salida real del nodo `Classify Dictionary`. En la evaluación previa, este mismo principio permitió detectar que **3 filas conservaban la clasificación de una versión anterior** del clasificador, con una puntuación (`0,2`) que no pertenece a la escala vigente; al reclasificarlas con el artefacto actual, la medición de la base subestimaba el desempeño. La corrección se documenta en la sección 5.b de la evidencia anterior y su efecto se cuantifica en la Tabla 5.11.

### 3.3.5. Definición operativa de las métricas

Sobre la clasificación binaria «amenaza / no amenaza» se definen: **TP** (el sistema indicó amenaza y la etiqueta de referencia también), **FP** (el sistema indicó amenaza y la referencia no), **FN** (el sistema no indicó amenaza y la referencia sí) y **TN** (ninguno de los dos indicó amenaza). Como la referencia se construyó con un estrato censado y otro muestreado, los estimadores no son proporciones simples:

**Precisión** = `TP / (TP + FP)`, calculada sobre el **censo de los 170** positivos del clasificador: denominador completo, sin ponderación y sin error de muestreo.

**Sensibilidad (*recall*)** = `TP / (TP + w·k)`, donde **k** son los casos sorteados del estrato 2 que la referencia marca como amenaza y **w = N₀/n₀ = 554/182 = 3,044** es el peso de muestreo. Cada omisión detectada en la muestra representa a `w` omisiones del estrato completo.

**F1-score** = media armónica de precisión y sensibilidad, derivada de las dos anteriores.

**Tasa de falsos descubrimientos** = `FP / (TP + FP)`, complemento exacto de la precisión. Se informa como lectura complementaria y **no como criterio autónomo** (1.6).

**Exactitud de categoría** = proporción de casos en que la categoría asignada coincide exactamente con la etiqueta de referencia, entre las publicaciones que ambos marcan como amenaza.

Los **intervalos de confianza** son exactos de Clopper-Pearson al 95 %. Para la precisión se aplican directamente sobre `TP` de 170. Para la sensibilidad, que es un cociente de estimadores, el intervalo se obtiene transformando el intervalo exacto de la proporción de omisión `k/n₀` del estrato 2, que es la única fuente de incertidumbre de muestreo del cálculo. Para el F1 se informa el intervalo conservador que resulta de evaluar la función en los extremos de los dos intervalos.

## 3.4. Aspectos legales, regulatorios y éticos

Al recolectar y almacenar de manera persistente contenido generado por usuarios, el proyecto debe observar los marcos jurídicos vigentes en la República Argentina. La principal regulación aplicable es la **Ley Nacional 25.326 de Protección de Datos Personales**, reglamentada por el **Decreto 1558/2001**. El artículo 2 de esa ley define los datos personales como información de cualquier tipo referida a personas físicas o de existencia ideal determinadas o determinables. Dado que los identificadores de usuario de una plataforma social permiten individualizar a una persona y, con información adicional, asociarla a su identidad real, su persistencia sin control violaría los principios de finalidad y de proporcionalidad.

Las medidas aplicadas son las siguientes:

**Seudonimización con clave en la etapa de ingesta.** Antes de persistir cada registro, el identificador del autor se reemplaza por el resultado de un código de autenticación de mensajes basado en *hash* (**HMAC-SHA-256**) calculado con una clave secreta. No se almacena el identificador original ni ninguna otra credencial. La terminología correcta es seudonimización: el resultado es un dato que ya no es directamente vinculable a una persona, pero que sigue siendo un dato personal en los términos del artículo 2 de la ley. El procedimiento no es irreversible: el HMAC-SHA-256 no es invertible sin la clave, pero el espacio de nombres de usuario tiene baja entropía, de modo que un atacante que obtuviera la clave podría enumerar candidatos y probarlos contra la columna. Esa es la razón por la que la clave no se versiona, se rota y no existe ninguna tabla que vincule identificadores originales con sus valores HMAC.

**Clave por despliegue, sin valor embebido.** La clave se provee como **variable de entorno** (`OSINT_HMAC_KEY`) y el flujo aborta si no está definida. El artefacto versionado **no contiene la clave**, y se eliminó de la documentación el ejemplo de clave fija embebida en el código que aparecía en una versión anterior del Anexo B. Este punto corrige además la descripción previa de un «*salt* dinámico», que no correspondía al mecanismo implementado. La obtención de la clave desde el nodo de código no es automática: n8n restringe por configuración el acceso a los módulos nativos y a las variables de entorno desde los nodos de función, de modo que el despliegue habilita explícitamente el módulo `crypto` (`NODE_FUNCTION_ALLOW_BUILTIN=crypto`) y el acceso a variables de entorno (`N8N_BLOCK_ENV_ACCESS_IN_NODE=false`). Son las dos condiciones sin las cuales el cálculo del *hash* falla en el nodo: la primera versión del flujo falló por no declararlas.

**Gestión y rotación de la clave.** Se documentó un procedimiento de **rotación de la clave** (`V4/evidencias/ROTACION_HMAC_2026-09-26.md`), con su fecha y su efecto: como el *hash* depende de la clave, una rotación produce valores distintos para un mismo autor antes y después de la rotación. Ese efecto refuerza la no vinculación entre períodos —un mismo autor no es correlacionable a través de la rotación— y, al mismo tiempo, impide el seguimiento longitudinal de autores, operación que el sistema no realiza ni necesita. La clave vigente se guarda en un archivo fuera del árbol versionado (en el despliegue documentado, `%USERPROFILE%\.n8n-hmac-key.txt`) y se carga como variable de entorno al iniciar el motor. La clave de la época anterior **se perdió** el 25/09/2026 al reiniciar el motor sin la variable de entorno, y esa pérdida es la que motivó la rotación. La consecuencia se declara: las 237 publicaciones persistidas antes de la rotación conservan un `author_hash` calculado con esa clave y **no son vinculables entre sí ni con las posteriores**, de modo que la no correlación de autores en ese tramo no depende del diseño sino de la pérdida de la clave.

**Minimización de datos.** Se recolectan únicamente publicaciones públicas; no se accede a comunidades privadas, mensajes, perfiles ni datos de contacto. No se recolectan comentarios, de modo que la tabla correspondiente permanece vacía. El sistema no realiza perfilado de personas ni persigue autores individuales: la unidad de análisis es el texto publicado.

**Riesgo residual declarado.** La seudonimización no elimina la posibilidad de **reidentificación indirecta** a partir del contenido: un texto puede mencionar el nombre de una organización, un cargo, un municipio o un incidente que permita inferir de quién se trata, o el propio autor puede haberse identificado en el cuerpo del mensaje. A ese vector se suman otros tres. Primero, el **identificador de plataforma**: la tabla `posts` conserva `id` y `url`, que permiten abrir el hilo original aunque el autor esté seudonimizado; por eso el informe reemplaza los identificadores por códigos en el cuerpo y mantiene la correspondencia en un archivo separado. Segundo, la **deterministicidad del HMAC** junto con la baja entropía de los nombres de usuario: quien obtuviera la clave podría probar candidatos y reconstruir la correspondencia, de modo que la protección depende de la custodia de la clave y no de la función *hash* en sí. Tercero, los **metadatos**: comunidad y fecha acotan el conjunto posible y, con el contenido, reducen el anonimato efectivo. El riesgo es inherente al análisis de texto y se mitiga, no se elimina, con las medidas anteriores. Por eso el informe describe patrones agregados y no reproduce identificadores en los casos del Capítulo 5.

**Cumplimiento de los términos de la plataforma.** La recolección se realiza sobre las fuentes públicas de sindicación, con una espera deliberada entre solicitudes por debajo del valor de referencia de tasa observado, y con mecanismos explícitos de reintento y de corte del ciclo ante bloqueos. El proyecto no evade controles de acceso: ante el 403 del endpoint JSON se cambió la vía en lugar de forzarla.

**Marco de gestión de la seguridad.** El diseño de los controles de acceso a la base, de la custodia de la clave de seudonimización y de la separación entre artefactos versionados y valores secretos se alineó con las buenas prácticas de gestión de la seguridad de la información (ISO/IEC, 2022). La referencia es de criterio de diseño, no de certificación: no hubo auditoría de conformidad.

# CAPÍTULO 4: DESARROLLO DEL SISTEMA

## 4.1. Arquitectura general

El artefacto se organiza en cinco capas funcionales, tal como se representa en la Figura 1:

**Capa de fuente.** Los listados públicos de novedades en formato RSS/Atom de las comunidades con monitoreo activo.

**Capa de orquestación.** El flujo de trabajo en n8n 2.40.6, desplegado en Docker, que coordina la extracción y la transformación.

**Capa de persistencia.** La base de datos PostgreSQL 18 con el esquema relacional de cinco tablas.

**Capa de análisis.** El motor de detección de anomalías con umbral estadístico.

**Capa de difusión.** El módulo de alertas hacia un canal externo, con el mecanismo de notificación deshabilitado por defecto.

<figure>
<img src="V4/devoluciones/recuperacion/media/media/image1.png" style="width:5.83333in;height:3.38188in" alt="Figura 1. Arquitectura del sistema" />
<figcaption aria-hidden="true"><p>Figura 1. Arquitectura del sistema</p></figcaption>
</figure>

> **Sobre los códigos de incidente de la Figura 1.** Las etiquetas `IN-06` e `IN-08` que aparecen junto a dos componentes remiten al registro de incidentes de implementación del proyecto, no a conceptos del dominio: `IN-06` es la coincidencia por subcadena del extractor de entidades —que puede reconocer una entidad dentro de otra palabra— y `IN-08` es el aborto del ciclo de ingesta ante un `HTTP 429` que quedaba registrado como corrida exitosa. Ambos se declaran como límites conocidos y su corrección es posterior a la ventana (Tabla 8.1).

El workflow desplegado se identifica como `KkotjSD5uO4CXI4D` («TFI OSINT V4 - Monitor de Amenazas»), está compuesto por **17 nodos**. Su estado se informa de forma distinta según el objeto observado, y la diferencia es deliberada: la **instancia desplegada** estuvo activa y publicada durante la ventana de recolección, mientras que el **artefacto versionado** (`V4/anexos/B_workflow.json`) se conserva con `active: false` para que importarlo no reactive la recolección sin una decisión explícita. Se estructura en **dos flujos independientes** que comparten la misma base de datos:

**Flujo de ingesta.** Disparado por un temporizador cada **15 minutos**. Ejecuta las tareas de preparación de comunidades, extracción de las fuentes, normalización, seudonimización, clasificación, extracción de entidades y persistencia. La composición del grafo de nodos y sus conexiones reales se muestran en la Figura 3, generada a partir del propio archivo exportado del workflow y no de un diagrama manual, de modo que refleja el artefacto ejecutado.

**Flujo de análisis.** Disparado por un temporizador diario a las **12:05**. Consulta los conteos diarios por categoría, ejecuta el motor de anomalías y registra las evaluaciones y las alertas correspondientes.

El inventario completo de nodos, con su tipo técnico y su responsabilidad, se presenta en la Tabla 4.1 y se detalla en el Anexo B.

**Tabla 4.1. Inventario de nodos del workflow desplegado**

| \# | Nodo | Tipo | Responsabilidad |
|----|----|----|----|
| 1 | `Schedule Ingesta` | Disparador por intervalo | Inicia el flujo de ingesta cada 15 minutos |
| 2 | `Prepare Subreddits` | Código | Construye la lista de comunidades con monitoreo activo |
| 3 | `Upsert Subreddits` | PostgreSQL | Persiste las comunidades (alta y actualización) |
| 4 | `Loop Over Items` | Lotes | Itera las comunidades con tamaño de lote 1 |
| 5 | `Espera Rate Limit` | Espera | Espera fija de 60 segundos entre comunidades |
| 6 | `Fetch Posts RSS` | Lectura RSS | Descarga el listado público de novedades de la comunidad |
| 7 | `Parse Reddit Posts` | Código | Normaliza campos y limpia el marcado del contenido |
| 8 | `HMAC Anonymize` | Código | Seudonimiza el identificador del autor con HMAC-SHA-256 |
| 9 | `Classify Dictionary` | Código | Asigna categoría y puntuación normalizada |
| 10 | `Extract Entities` | Código | Extrae entidades tecnológicas a JSONB |
| 11 | `Prepare Upsert` | Código | Arma el registro final de la publicación |
| 12 | `Upsert Posts` | PostgreSQL | Inserta o actualiza por clave primaria (idempotente) |
| 13 | `Schedule Anomalias` | Disparador por intervalo | Inicia el flujo de análisis a las 12:05 |
| 14 | `Query Daily Counts` | PostgreSQL | Cuenta publicaciones por categoría y día local |
| 15 | `Anomaly Engine` | Código | Calcula línea base, umbral y decisión de disparo |
| 16 | `Registrar Anomalias y Alertas` | PostgreSQL | Registra la evaluación y la alerta asociada |
| 17 | `Send Telegram Alert` | Solicitud HTTP | Envía la notificación al canal configurado |

Además del lazo principal, el flujo de ingesta incorpora un **centinela** que garantiza que cada comunidad produzca al menos un elemento procesable por ciclo. Sin él, una fuente que devolviera cero elementos —escenario típico ante una respuesta 429— no propagaba ningún elemento a los nodos posteriores y el lazo de control avanzaba sin procesar el resto de la lista, con la consecuencia de que la comunidad ubicada en el tercer turno perdía sistemáticamente sus publicaciones. Este comportamiento se diagnosticó y se corrigió en el artefacto desplegado; el detalle del incidente y de su caracterización consta en `CARACTERIZACION_RATE_LIMIT.md`.

## 4.2. Modelo de datos

El esquema físico reside en una base de datos PostgreSQL 18 desplegada en un clúster propio en el puerto 5433, bajo el rol de aplicación `tesi_app`. La Figura 2 presenta el diagrama entidad-relación. El modelo consta de **cinco tablas** (`subreddits`, `posts`, `comments`, `anomalias` y `alertas`), **cinco índices** y dos restricciones de integridad referencial de comportamiento distinto, elegidas deliberadamente. La Tabla 4.2 reproduce los atributos de cada tabla tal como están definidos en el DDL vigente.

<figure>
<img src="V4/devoluciones/recuperacion/media/media/image2.png" style="width:5.83333in;height:3.40395in" alt="Figura 2. Modelo entidad-relación" />
<figcaption aria-hidden="true"><p>Figura 2. Modelo entidad-relación</p></figcaption>
</figure>

**Tabla 4.2. Atributos del esquema físico (espejo de** `A_DDL.sql`**)**

| Tabla | Atributo | Tipo | Restricción / función |
|----|----|----|----|
| `subreddits` | `id` | `VARCHAR(50)` | Clave primaria |
|  | `display_name` | `VARCHAR(100)` | Único, no nulo |
|  | `subscribers` | `INTEGER` | Suscriptores al momento del alta |
|  | `active_monitoring` | `BOOLEAN` | Interruptor de monitoreo (baja lógica) |
|  | `created_at` | `TIMESTAMPTZ` | Alta del registro |
| `posts` | `id` | `VARCHAR(50)` | Clave primaria (identificador de la publicación) |
|  | `subreddit_id` | `VARCHAR(50)` | Clave foránea → `subreddits(id)`, `ON DELETE RESTRICT` |
|  | `title` | `TEXT` | Título, no nulo |
|  | `selftext` | `TEXT` | Cuerpo del texto (puede estar vacío) |
|  | `url` | `TEXT` | Enlace asociado |
|  | `author_hash` | `CHAR(64)` | Autor seudonimizado con HMAC-SHA-256, no nulo |
|  | `score` | `INTEGER` | Puntaje de la publicación |
|  | `num_comments` | `INTEGER` | Cantidad declarada de comentarios |
|  | `created_utc` | `TIMESTAMPTZ` | Fecha real de publicación, no nula |
|  | `nlp_category` | `VARCHAR(100)` | Categoría asignada por el clasificador |
|  | `nlp_score` | `REAL` | Puntuación normalizada, `CHECK (nlp_score BETWEEN 0 AND 1)` |
|  | `entities` | `JSONB` | Entidades tecnológicas extraídas |
|  | `nlp_processed` | `BOOLEAN` | Marca de procesamiento |
|  | `ingested_at` | `TIMESTAMPTZ` | Instante de ingesta (base del cálculo de latencia) |
| `comments` | `id`, `post_id`, `body`, `author_hash`, `score`, `created_utc`, `nlp_category`, `nlp_score`, `nlp_processed`, `ingested_at` | — | Clave foránea → `posts(id)`, `ON DELETE CASCADE`. Tabla habilitada y sin poblar (ver 4.3) |
| `anomalias` | `id`, `ventana_inicio`, `ventana_fin`, `categoria`, `n_observado`, `base_media`, `umbral`, `disparo`, `created_at` | — | Registra cada evaluación del motor, con o sin disparo |
| `alertas` | `id`, `anomalia_id`, `canal`, `destinatario`, `payload`, `estado`, `created_at` | — | Clave foránea → `anomalias(id)`, `ON DELETE CASCADE` |

**Índices.** Se declaran cinco: `posts.created_utc` (descendente, para las series temporales), `posts.nlp_category` (para los conteos por categoría del motor), `posts.ingested_at` (para las consultas de latencia), `comments.post_id` y `anomalias.created_at`.

Tres decisiones del esquema merecen justificación explícita, porque corrigen el diseño de versiones anteriores del informe:

`posts.subreddit_id` **usa** `ON DELETE RESTRICT`**, no** `CASCADE`**.** Una comunidad con publicaciones no puede eliminarse por accidente arrastrando su corpus: para dejar de monitorearla se cambia `active_monitoring` a falso. El borrado en cascada se reserva para las relaciones donde la dependencia es real (`comments` respecto de `posts`, y `alertas` respecto de `anomalias`).

**No se incluyen extensiones de búsqueda de texto completo.** El esquema anterior declaraba la extensión `pg_trgm` y un índice GIN sobre `to_tsvector` que nunca se utilizaban, porque la clasificación no se realiza en la base de datos sino en el flujo de trabajo mediante un diccionario. Se eliminaron por no estar justificados.

**La latencia no requiere una columna adicional.** Se obtiene por diferencia entre `ingested_at` y `created_utc`, ambas presentes en la tabla `posts`.

**Índices declarados.** El esquema define **cinco índices**, cada uno asociado a un patrón de acceso efectivamente utilizado por los flujos y por las consultas de este informe: `idx_posts_ingested_at` y `idx_posts_created_utc` (descendente) sostienen, respectivamente, el conteo diario del motor de anomalías y el cálculo de latencia extremo a extremo; `idx_posts_nlp_category` sirve a la agregación por categoría; `idx_comments_post_id` habilita la lectura de comentarios por publicación si la tabla llegara a poblarse; y `idx_anomalias_created_at` ordena temporalmente las evaluaciones del motor. La decisión de diseño fue no declarar índices de texto completo: un índice de ese tipo existía en la versión previa del modelo y se retiró por no corresponder a ningún patrón de consulta real, con el costo de mantenimiento que implica en cada carga.

## 4.3. Flujo de ingesta

El flujo de ingesta recorre la siguiente secuencia:

**Preparación de comunidades.** Se construye la lista de comunidades con `active_monitoring` verdadero y se persiste mediante *upsert*, de modo que el alta o la baja de una comunidad no requiere editar el flujo.

**Iteración y control de tasa.** El nodo de lotes procesa una comunidad por vez y, entre una y la siguiente, se interpone una **espera fija de 60 segundos**. La elección no es arbitraria: con tres comunidades activas, un ciclo completo consume tres solicitudes espaciadas un minuto, por debajo del valor de referencia de tasa observado. Los reintentos ante respuestas 429 o 403 quedan acotados y no bloquean el resto del ciclo.

**Extracción.** La lectura de la fuente de sindicación devuelve los elementos publicados más recientemente en la comunidad.

**Normalización.** Se limpia el marcado del contenido y se normalizan los campos a los tipos del esquema: se descarta el prefijo `/u/` de las menciones, se remueve la línea de autoría que la sindicación agrega al cuerpo del texto y se colapsan los espacios repetidos.

**Seudonimización.** Se calcula `HMAC-SHA-256(author, clave)` y se descarta el valor original. El *hash* resultante es determinista dentro de una misma clave: dos publicaciones del mismo autor comparten `author_hash` sin que el autor sea identificable, lo que habilita el conteo de autores únicos sin almacenar identidades.

**Clasificación y entidades.** Se asigna la categoría y la puntuación (sección 4.4) y se extraen las entidades tecnológicas pertinentes a un campo `JSONB`.

**Carga idempotente.** La persistencia se realiza con `INSERT … ON CONFLICT (id) DO UPDATE`, de modo que reprocesar un elemento actualiza el registro en lugar de duplicarlo. La idempotencia no es una propiedad teórica: se verificó ejecutando el flujo sobre el mismo conjunto de entrada y comprobando que el conteo de filas no variara. La sentencia completa —transcrita en el Anexo B— inserta trece columnas y, ante el conflicto de clave, actualiza **nueve** campos mediante una lista `SET` explícita: `title`, `selftext`, `url`, `score`, `num_comments`, `nlp_category`, `nlp_score`, `entities` y `nlp_processed`. Las dos columnas restantes de la tabla, `created_utc` (fecha de publicación original) e `ingested_at` (fecha de primera persistencia), **no integran la lista** `SET`, de manera que una relectura del mismo elemento no las sobrescribe: la antigüedad de la publicación y el instante de su primera ingesta quedan fijos. Esto es lo que sostiene la estabilidad de la latencia (5.3) y de los conteos diarios del motor de anomalías (5.4): si `ingested_at` se reescribiera en cada relectura, la ventana móvil del motor se desplazaría de forma silenciosa. El `UPDATE` sobreescribe entonces únicamente los campos que dependen del contenido, de manera que una misma publicación reprocesada después de una corrección del diccionario queda con la clasificación vigente y no con la heredada. Esta propiedad es la que permite afirmar que el corpus refleja el estado actual del sistema y no una mezcla de versiones.

**Cierre del lazo y centinela.** El lazo de iteración se cierra desde el nodo de extracción de entidades, y no desde el de clasificación. La diferencia no es cosmética: la extracción tiene dos salidas y una de ellas transporta el elemento centinela cuando la comunidad no devolvió publicaciones, de modo que el lazo siempre recibe al menos un elemento y avanza. Si el cierre se hubiera dejado en el nodo de clasificación, una comunidad sin novedades o con respuesta bloqueada habría detenido el ciclo completo y las comunidades siguientes no se habrían consultado, que es exactamente el fallo diagnosticado y corregido.

**Sobre los comentarios.** La tabla `comments` existe en el esquema, con sus columnas, índices y restricciones, pero **no está poblada: contiene cero filas**. La causa es una limitación de la fuente y no un error del flujo: las fuentes RSS/Atom no exponen el árbol de comentarios, y el endpoint que sí lo exponía resultó inaccesible por política de la plataforma. Las publicaciones, en cambio, sí declaran en `num_comments` la cantidad de comentarios que la plataforma informa, lo que permite dimensionar la conversación sin recolectarla. Esta brecha se declara como tal: el sistema **no** analiza comentarios, y por lo tanto ninguna afirmación de este informe puede referirse a texto de comentarios. Se trata de una reducción deliberada del alcance respecto del diseño original, no de una omisión inadvertida.

**Entorno de ejecución.** Todas las mediciones de este informe provienen de la instancia en operación y no de un banco de pruebas construido para la evaluación. El artefacto corre en **dos contenedores sobre un único equipo**: el motor de flujos (`tfi-n8n`, n8n 2.40.6, modo regular, sin *queue mode* ni trabajadores distribuidos) y la base de datos (`tfi-postgres`, PostgreSQL 18, clúster en el puerto 5433), con la zona horaria del equipo fijada en `America/Argentina/Buenos_Aires`. No se configuró aislamiento de CPU ni de memoria por contenedor, ni hardware dedicado: el sistema comparte recursos con el resto del equipo. Esa decisión es deliberada y coherente con el objetivo de costo de la sección 1.3, pero **limita la interpretación de los resultados de rendimiento**: los valores de latencia y throughput de la sección 5.3 describen el comportamiento de una instalación de un solo nodo sobre recursos compartidos y no deben leerse como una medición de capacidad máxima. Los parámetros de CPU, memoria y entrada/salida del equipo anfitrión no se caracterizaron, y ese vacío se declara como limitación en 6.3 en lugar de reemplazarse por una estimación.

## 4.4. Clasificador por diccionario

El clasificador se implementa como un nodo de código con una taxonomía de **9 categorías y 201 términos** en español e inglés, orientados al léxico efectivamente utilizado en las comunidades hispanohablantes y en las angloparlantes de seguridad. La distribución de términos por categoría es la siguiente:

**Vulnerabilidades** (30 términos)

**Robo de Credenciales** (29 términos)

**Filtración de Datos** (29 términos)

**Malware** (24 términos)

**Phishing** (22 términos)

**Ingeniería Social** (20 términos)

**Infraestructura y Ataques** (16 términos)

**Hacktivismo** (16 términos)

**Ransomware** (15 términos)

El listado completo término por término se incluye en el Anexo C (Tabla C.1), de modo que la clasificación de cualquier publicación pueda auditarse contra el diccionario vigente. La lógica de decisión es la siguiente:

Se normaliza el texto combinado de título y cuerpo (minúsculas y remoción de diacríticos).

Para cada categoría se cuentan las coincidencias: los términos de una palabra se buscan por igualdad exacta contra el conjunto de palabras del texto normalizado; los términos compuestos, por coincidencia de subcadena.

La categoría ganadora es la que acumula más coincidencias; ante empate, se aplica el orden de prioridad declarado en el diccionario, que no es alfabético sino de gravedad.

Se exige un **mínimo de una coincidencia** (`MIN_HITS = 1`) para asignar una categoría distinta de «No relevante». El efecto de este umbral se cuantifica en la Tabla 5.11.

La puntuación se calcula con una escala saturante: `nlp_score = min(1, coincidencias / 4)`. La saturación en cuatro coincidencias busca distinguir una publicación inequívoca de una que menciona el tema de forma tangencial, sin que la diferencia entre seis y veinte coincidencias altere el valor. La escala es fija y no se recalibró con posterioridad.

La extracción de entidades produce un objeto con cinco familias: identificadores de vulnerabilidad (patrón `CVE-AAAA-NNNNN`), direcciones de correo, direcciones IPv4, dominios de primer nivel frecuentes —excluyendo los de la propia plataforma de origen— y nombres de productos o tecnologías. Cuatro de las cinco familias —CVE, correos, IPv4 y dominios— se extraen por **expresión regular** sobre el texto normalizado; la quinta, los nombres de productos o tecnologías, **no usa una expresión regular**: se reconoce por coincidencia de subcadena contra una **lista blanca fija de dieciocho términos** (`low.includes(p)`), de modo que es un catálogo cerrado y enumerable. Cada familia se recorta a veinte elementos y el resultado se persiste tanto como objeto `JSONB` como en su forma textual. El rendimiento real de la extracción —cobertura por familia, distribución por comunidad y categoría, y sus modos de error— se informa en la sección 5.6. La limitación es deliberada y debe declararse: **no hay validación de los valores extraídos**, de modo que una dirección IP citada en el cuerpo de una discusión es indistinguible de una que identifique infraestructura de un ataque, y la extracción no resuelve alias ni variantes de un mismo producto. El campo se ofrece, por lo tanto, como material de revisión y no como indicador verificado.

### 4.4.1. Decisiones de diseño del clasificador y sus consecuencias

Tres decisiones de implementación explican el comportamiento medido en el Capítulo 5 y conviene registrarlas antes de ver los resultados.

**La normalización y el tokenizado fijan qué se puede encontrar.** El texto se lleva a minúsculas y se le remueven los diacríticos por descomposición Unicode, y luego se particiona por todo carácter que no sea alfanumérico. Ambas operaciones tienen consecuencias que conviene hacer explícitas. La primera obliga a escribir los términos del diccionario sin acentos: si un término se almacenara con diacríticos, el texto normalizado nunca lo contendría y la coincidencia sería imposible, de modo que el Anexo C reproduce el diccionario tal como está implementado y no en su forma ortográfica. Sobre ese texto normalizado se hacen dos búsquedas distintas. Los términos de **una sola palabra** se comparan por igualdad exacta contra el conjunto de palabras, que se obtiene partiendo el texto por todo carácter no alfanumérico: eso evita que una coincidencia parcial dispare una categoría, pero también implica que `clonar` no coincida con `clonado`. Los términos de **varias palabras** se buscan por coincidencia de subcadena sobre el texto normalizado, y no sobre el conjunto de palabras, porque de otro modo la frase quedaría partida. La normalización **no reemplaza guiones**: el guion sobrevive en el texto y solo desaparece del conjunto de palabras, de modo que un compuesto escrito con guion (`zero-day`) no es alcanzado por su forma en dos palabras (`zero day`); por esa razón el diccionario no contiene términos con guion. El costo de esta mecánica es la ausencia de lematización y de *stemming*: el diccionario debe contener las formas conjugadas y plurales que realmente aparecen en las publicaciones, porque `filtraron` no coincide con `filtrar`.

**La escala de puntuación se fijó después de comprobar que la anterior no era comparable.** La primera versión del clasificador puntuaba dividiendo las coincidencias por la cantidad de términos de la categoría. Esa elección tenía un defecto estructural: como el denominador dependía del tamaño del diccionario, el mismo par de coincidencias pasaba de 0,22 a 0,07 a medida que el diccionario crecía, con lo cual la puntuación no era comparable entre corridas ni entre categorías. La escala vigente elimina el denominador variable y satura en cuatro coincidencias, de modo que dos coincidencias valen 0,5 y tres valen 0,75 con independencia de la categoría y de la versión del diccionario. Esta es la razón por la que la puntuación es interpretable como una medida de intensidad temática y no como una probabilidad.

**El umbral mínimo de coincidencias se bajó con evidencia, no por conveniencia.** Con dos coincidencias exigidas, el clasificador descartaba amenazas evidentes: una campaña de correos fraudulentos que se hacían pasar por una investigación de Interpol contenía un término del diccionario que coincidía sin ambigüedad, y aun así la publicación quedaba clasificada como no relevante porque solo acumulaba una coincidencia. La medición sobre la muestra del 30/09/2026 fijó el costo de ambas alternativas: con el umbral en dos se detectaban 24 de 29 amenazas y con el umbral en uno, 27 de 29. La contrapartida se aceptó de forma explícita: bajar el umbral **también expone los términos demasiado genéricos**, y ese efecto se materializó en un caso concreto. El término `dni`, incluido en la categoría de filtración de datos, coincidía con una publicación sobre la baja de un apoderado previsional, y se retiró del diccionario en la misma corrección; con el umbral anterior ese falso positivo permanecía oculto porque la publicación no alcanzaba las dos coincidencias. El episodio deja una regla: **un término que coincide con trámites administrativos es demasiado general para un clasificador de amenazas**, aunque su presencia en el dominio parezca justificada.

**Auditoría del diccionario.** El diccionario se auditó completo —201 términos en 9 categorías— reimplementando el clasificador y verificando que reproduce las **724** clasificaciones almacenadas **sin una sola discrepancia**. Cuatro hallazgos, cada uno con su efecto medido sobre el corpus:

**Dos erratas.** `sequestro de datos` (por *secuestro*) y `caeron los servidores` (por *cayeron*) no podían coincidir con un texto bien escrito. Se corrigieron en el artefacto; la comprobación previa y posterior da **0 coincidencias en ambas formas**, de modo que la corrección no altera ninguna clasificación.

**Solapamientos.** Cuatro pares donde un término contiene a otro (`zero day` / `zero day vulnerability`, `ejecucion remota` / `ejecucion remota de codigo`, `filtracion` / `filtracion publicada`, `vishing` / `vishing script`) permiten sumar dos coincidencias por una sola expresión. En este corpus **ninguna publicación contenía ambos miembros de un par**, por lo que el efecto medido es nulo; el riesgo queda documentado.

**Guiones.** El defecto descrito arriba afecta a **5 de las 724** publicaciones: en dos cambiaría la categoría asignada y en las otras tres solo la puntuación. En ningún caso se modifica el conjunto de publicaciones clasificadas, que seguiría siendo de **170**, y ninguna de las cinco está entre los trece casos de la Tabla 5.14.

**Términos genéricos.** Once publicaciones se clasificaron **exclusivamente** por un término genérico del dominio de desarrollo (`payload`, `loader`, `clonar`, `datos personales`, `filtrado`, `leak`, entre otros). Retirarlos reduciría el corpus clasificado de **170 a 159** publicaciones (−6,5 %), las detecciones de `r/devsarg` de **7 a 4**, y eliminaría dos de los casos documentados en la Tabla 5.14 (`C-08` y `C-09`), ambos falsos positivos.

**Decisión: el diccionario se congela.** Se corrigen las erratas —de efecto nulo— y se conserva el resto tal como operó durante la ventana. La razón es metodológica: el marco muestral de la validación —554 publicaciones no clasificadas y censo de las 170 clasificadas— está definido sobre esta versión del clasificador, y retirar términos genéricos lo dejaría sobre otro universo, obligando a rehacer el sorteo y el etiquetado. El efecto de los tres hallazgos restantes se informa cuantificado arriba, se retoma como limitación en 6.3 y como recomendación en el Capítulo 8. La verificación completa, con el detalle de las once publicaciones y la traza de coincidencias de los trece casos, se conserva en `V4/evidencias/informe_v5_2026-10-20/auditoria_diccionario.md`.

## 4.5. Motor de detección de anomalías

El motor se ejecuta una vez por día a las 12:05. Su lógica es la siguiente:

**Conteo.** Se cuentan las publicaciones **por su fecha de ingesta** (`ingested_at`) dentro del **día local anterior** (zona `America/Argentina/Buenos_Aires`), agrupadas por categoría y excluyendo la categoría «No relevante». El uso del día local, y no del día UTC, evita que la frontera del día parta la actividad de la tarde y la noche en dos registros; el uso de la fecha de ingesta, y no la de publicación original, mide la actividad **detectada por el sistema** en cada jornada operativa.

**Línea base.** Para cada categoría se calcula el promedio diario de los **diez días previos** al día evaluado, siempre dividiendo por diez. La ventana móvil total es de once días. Cuando una categoría no registra ninguna publicación en esa ventana, no produce fila: el motor no emite juicios sobre categorías ausentes.

**Umbral.** El umbral se deriva del comportamiento esperado de conteos poco frecuentes mediante una distribución de Poisson ajustada a la línea base: se toma el cuantil 95 y se le suma uno, con un piso absoluto de tres. La expresión implementada es `umbral = max(cuantil95(λ) + 1, 3)`, donde `λ` es la línea base. El piso existe porque, durante los primeros días de operación, la línea base es cero y la formulación estadística colapsaría a un umbral de uno, lo que produciría un disparo ante cada publicación.

**Decisión.** Se registra un disparo cuando el conteo observado **alcanza o supera** el umbral calculado. Cada evaluación se persiste en la tabla `anomalias`, **con o sin disparo**, lo que permite auditar las decisiones negativas y no solo los avisos. La idempotencia del registro no depende solo del nodo: la tabla `anomalias` declara la restricción `UNIQUE (categoria, ventana_inicio)`, de modo que la base rechaza una segunda evaluación de la misma categoría en la misma ventana. Con esa restricción, la afirmación de idempotencia que se verifica para la ingesta (§4.3) se extiende también al análisis: reejecutar el motor no duplica evaluaciones.

**Categorías evaluadas.** El motor evalúa las categorías con presencia efectiva en la ventana de once días. No emite juicios sobre categorías que no registran publicaciones, y por esa razón el número de evaluaciones por día no es constante (sección 5.4).

**Registro y alerta.** Cuando la decisión es afirmativa, se registra la alerta asociada en la tabla `alertas` con el canal, el destinatario y el contenido del mensaje. El estado por defecto de una alerta es `PENDIENTE`: una fila sin estado explícito **no** se registra como enviada, coherente con que el envío esté deshabilitado hasta que se confirme (5.4).

**Corrección de fórmula durante el desarrollo.** El motor atravesó dos versiones. La primera calculaba el cuantil de la distribución de Poisson reiterando las masas de probabilidad, pero con un error en la recurrencia: omitía un factor `λ` en todas las masas salvo la de cero, de modo que la función de distribución acumulada resultante saturaba en `1/λ` en lugar de llegar a uno. La consecuencia práctica era severa y silenciosa: para cualquier línea base superior a 1,05 la búsqueda del cuantil 95 nunca convergía y devolvía el valor tope, con lo cual **ninguna categoría con línea base mayor que uno podía disparar jamás**. Se verificó en producción con dos categorías de línea base alta que quedaban con umbral inalcanzable, mientras una tercera disparaba por accidente, con una línea base baja. La fórmula se corrigió el **05/10/2026** implementando la recurrencia correcta (`P(i) = P(i-1) · λ / i`). Las evaluaciones del **05/10 en adelante** son **posteriores a la corrección**, y son las únicas que se usan para juzgar la eficacia del motor: el error afectó a los primeros días de operación, en los que el motor operaba con parámetros degenerados, y su efecto observable es la ausencia de disparos legítimos por línea base alta durante ese tramo, no la producción de falsos positivos. Las evaluaciones del 02/10/2026 se conservan en la base con `base_media = 0`, porque la línea base se calculó sobre días anteriores al inicio efectivo del corpus; se analizan como tales en 5.4.

**Estado del módulo de difusión.** El nodo de notificación está implementado y persiste correctamente cada alerta, pero el envío externo por Telegram está **deshabilitado por defecto**, de modo que las filas de la tabla `alertas` registran la alerta **sin entrega efectiva**. Esto tiene una consecuencia directa sobre la evaluación del objetivo específico OE6, que se declara como cumplimiento parcial en 5.8 y en la Tabla 7.2.

**Por qué el sistema produce «avisos diarios» y no «alertas tempranas».** La cadencia del motor fija el límite de oportunidad del aviso y conviene declararlo con precisión, porque es la razón por la que el objetivo general habla de *avisos diarios*. El motor corre **una vez por día a las 12:05** y evalúa el **día local anterior completo**; por lo tanto, un hecho publicado al comienzo de una jornada no puede generar su aviso antes de la corrida del día siguiente, es decir **unas 36 horas después** aun suponiendo latencia de ingesta nula. Con el P95 de ingesta efectivamente medido, esa demora es mayor. Una alerta que puede tardar un día y medio en emitirse **no es temprana en el sentido operativo del término**; es un aviso diario, y así se la denomina en el objetivo general y en el título del trabajo. La distinción no es nominal: quien lea «alerta temprana» esperaría una notificación en minutos u horas, y el diseño no la provee. La sección 8.3 (línea de trabajo) condiciona cualquier ampliación del alcance a resolver primero esta latencia.

## 4.6. Consideraciones de trazabilidad del artefacto

Tres propiedades del desarrollo se documentan para permitir la auditoría de lo afirmado en este capítulo:

**El workflow es un artefacto versionado.** El flujo se genera mediante el script `V4/scripts/generar_workflow.py` y se exporta a `V4/anexos/B_workflow.json`, consistente con los 17 nodos del sistema en ejecución. La regla de trabajo adoptada es no editar el artefacto exportado a mano ni modificar el flujo desde la interfaz de administración, porque el motor ejecuta el borrador y una edición manual sin publicación posterior diverge silenciosamente de la evidencia.

**El esquema es un artefacto versionado.** `V4/anexos/A_DDL.sql` reproduce el DDL real, y en su encabezado enumeran las correcciones aplicadas respecto de la versión anterior del modelo, lo que hace auditable la evolución del diseño.

**Las figuras se generan desde los artefactos.** Las figuras 1 a 4 se producen con el script `V4/scripts/generar_figuras_v4.py`; la Figura 3, en particular, lee el grafo de nodos y conexiones directamente del archivo exportado del workflow, de modo que no puede divergir del sistema descrito.

<figure>
<img src="V4/devoluciones/recuperacion/media/media/image3.png" style="width:5.83333in;height:3.48904in" alt="Figura 3. Grafo de nodos y conexiones del workflow desplegado" />
<figcaption aria-hidden="true"><p>Figura 3. Grafo de nodos y conexiones del workflow desplegado</p></figcaption>
</figure>

> **Nota sobre el atributo** `active` **de la Figura 3.** La figura se genera leyendo el archivo exportado, que declara `active: false` por diseño: el artefacto se versiona desactivado y la publicación se realiza manualmente desde la interfaz. El estado operativo de la instancia durante la ventana —activa, con **382 corridas** registradas— se informa en 4.1 y en 6.1; la diferencia entre ambos valores es un control de seguridad, no una inconsistencia.

Las limitaciones de implementación que condicionan la interpretación de los resultados —ausencia de lematización, vocabulario de la fuente acotado al listado de novedades, ausencia de comentarios, umbral de coincidencia mínimo y saturación de la escala— se retoman de forma consolidada en la sección 6.3, junto con su efecto observable sobre el desempeño medido.

## 4.7. Declaración de trazabilidad y firma

Los autores declaran que toda la evidencia citada en el presente informe es verificable, reproducible y corresponde al sistema efectivamente implementado y a los datos realmente relevados. Las cifras provienen exclusivamente de consultas `SELECT` sobre la base `tesi_osint`, de archivos de evidencia fechados y de artefactos versionados en el repositorio, tal como se indica en las notas de trazabilidad de los capítulos correspondientes. La sustitución del corpus respecto de las versiones V2/V3 se documenta en la *Declaración de trazabilidad entre versiones* (`V4/evidencias/informe_v5_2026-10-20/Declaracion_trazabilidad_versiones.md`), firmada por los autores y con conocimiento de la dirección.

**Autores:**

------------------------------------------------------------------------

**Valentino Lorca**

------------------------------------------------------------------------

**Jerónimo Zúñiga**

------------------------------------------------------------------------

**Enzo Severino**

**Directores / Profesores:**

------------------------------------------------------------------------

**Prof. Alberto Cortez**

------------------------------------------------------------------------

**Prof. Ariel Enferrel**

Mendoza, Argentina — 2026

# CAPÍTULO 5: RESULTADOS

> **Nota de trazabilidad de este capítulo.** Todas las cifras de este capítulo provienen de consultas de solo lectura ejecutadas sobre la base `tesi_osint` el **19/10/2026**, con el corte del corpus fijado en el inicio del **18/10/2026**. La salida literal de las consultas se conserva en `V4/evidencias/informe_v4_2026-10-19/consultas_corpus_b5.txt`, de modo que cualquier cifra puede reconstruirse. Las excepciones son las métricas de la validación (sección 5.5), cuya fuente es `V4/evidencias/informe_v5_2026-10-20/` (`resultados_v5.json`, `resultados_v5.md` y la correspondencia de la muestra), y las cifras de la evaluación previa del 30/09/2026 (sección 5.5.1), que provienen de `V4/evidencias/evaluacion_muestra_control_2026-09-30.md` y sus archivos asociados.

## 5.1. El corpus B5

La ventana de recolección se cerró el **17/10/2026** con **724 publicaciones** persistidas en el rango correspondiente a la ventana. La base contiene además publicaciones posteriores al corte —**31 al 19/10/2026**, fecha de las consultas—, recolectadas por el mismo sistema en un track paralelo iniciado el 19/10, que **no forman parte de este análisis**; ese track continúa recolectando, de modo que el total de la tabla crece sin afectar las cifras de este informe. No hay publicaciones anteriores al inicio de la ventana.

**Tabla 5.1. Corpus de la ventana B5 por subreddit**

| Comunidad | Suscriptores (al alta) | Publicaciones | % del corpus | No relevante | % dentro de la comunidad |
|----|---:|---:|---:|---:|---:|
| `r/devsarg` | 0 (30/09/2026) | 428 | 59,12 % | 421 | 98,36 % |
| `r/netsec` | 0 (30/09/2026) | 150 | 20,72 % | 84 | 56,00 % |
| `r/Malware` | 0 (30/09/2026) | 146 | 20,17 % | 49 | 33,56 % |
| **Total** | — | **724** | **100,00 %** | **554** | **76,52 %** |

La composición del corpus es desigual y esa desigualdad es un resultado en sí mismo. Las cifras de suscriptores corresponden al momento del alta en la tabla `subreddits` (30/09/2026), valor registrado por el sistema al momento de la incorporación; Reddit no expone ese dato de forma estable a través del feed RSS/Atom utilizado, y el campo se conserva en el esquema con valor 0 (véase 1.4 y 4.3). Dos comunidades de seguridad en inglés aportan el **40,89 %** de las publicaciones y concentran casi la totalidad de las detecciones; la comunidad de desarrolladores en español aporta el **59,12 %** de las publicaciones y solo el **1,64 %** de su propio contenido (7 de 428) resulta clasificado como amenaza. El detalle de esas siete detecciones se discute en 5.7: **cuatro son falsos positivos** —conversaciones técnicas o administrativas que activaron un único término del diccionario— y **tres describen incidentes locales reales**. La distribución diaria de esa recolección se presenta en la Tabla 5.2.

**Tabla 5.2. Recolección diaria de la ventana B5 (por fecha local de ingesta)**

| Fecha     | Publicaciones | % del corpus |
|-----------|--------------:|-------------:|
| 01/10     |           307 |      42,40 % |
| 02/10     |            32 |       4,42 % |
| 03/10     |         **0** |       0,00 % |
| 04/10     |            37 |       5,11 % |
| 05/10     |            25 |       3,45 % |
| 06/10     |            39 |       5,39 % |
| 07/10     |            16 |       2,21 % |
| 08/10     |            35 |       4,83 % |
| 09/10     |            31 |       4,28 % |
| 10/10     |            26 |       3,59 % |
| 11/10     |            17 |       2,35 % |
| 12/10     |            31 |       4,28 % |
| 13/10     |            28 |       3,87 % |
| 14/10     |            28 |       3,87 % |
| 15/10     |            31 |       4,28 % |
| 16/10     |            33 |       4,56 % |
| 17/10     |             8 |       1,10 % |
| **Total** |       **724** | **100,00 %** |

Tres hechos de esta serie requieren explicación:

**El primer día concentra el 42,40 % del corpus.** El 01/10 el sistema ingresó 307 publicaciones, casi la mitad del total de la ventana. No es un pico de actividad de las comunidades: es el efecto del listado de novedades, que en la primera consulta devuelve hasta 100 elementos por comunidad con independencia de cuándo se publicaron. Ese arrastre inicial es la causa de que **287 publicaciones del corpus (39,64 %) fueran creadas antes del 01/10** y de que la latencia bruta de la ventana esté dominada por ellas (sección 5.3).

**El 03/10 no se recolectó ninguna publicación y el 02/10 solo 32.** Las marcas de tiempo del sistema muestran un hueco operativo de aproximadamente **44 horas** entre el 02/10 a las 18:47 y el 04/10 a las 14:53 (hora local), documentado como intervalo sin ciclos con contenido. La causa está identificada y es de **infraestructura, no de la fuente ni del flujo**: el 03/10 el equipo quedó **apagado todo el día**, de modo que la instancia de n8n estuvo inaccesible y no se ejecutó ningún ciclo —ni de ingesta ni del motor—. La bitácora de esa jornada (`V4/evidencias/bitacora_b5/2026-10-03.md`, §5) lo registra como declaración del operador: «Equipo apagado todo el día: no hubo ninguna ejecución del workflow ni ingesta», con la instancia «caída (sin respuesta en su puerto)». El 04/10 la instancia se levantó de nuevo y la recolección se reanudó a las 14:53, con el workflow republicado; la bitácora del 04/10 lo consigna como «instancia n8n arriba y workflow publicado (activo)». En otras palabras, la interrupción no fue una caída de un contenedor ni un error del flujo, sino la **ausencia de la instancia por apagado del equipo**, y su fin fue una **reanudación manual del operador**, no una recuperación automática. Esto es pertinente para la evaluación de la recuperación ante fallos (OE2): el sistema **no** se reanuda por sí solo tras una indisponibilidad de la instancia; requiere intervención humana para volver a ponerla en marcha, y la detección del corte tampoco fue automática (sección 4.5). El hueco no es atribuible a la fuente: las tres comunidades monitoreadas publican con continuidad horaria. El día se registra como **no recolectado** —ausencia de datos— y **no** como un día de cero publicaciones, para no deprimir artificialmente la línea base del motor (sección 5.4).

**El 17/10 la serie se corta en 8 publicaciones.** El corte del corpus se fijó en el inicio del 18/10, de modo que el 17/10 es un día completo en el calendario; su volumen bajo **no** coincide con una interrupción de datos sino con el régimen de operación de ese día. Se ejecutaron **19 ciclos** —2 manuales y 17 automáticos del disparador—, **todos exitosos y ninguno fallido**, con la jornada activa medida entre las **12:12 y las 16:33** (hora local): el primer ciclo automático corrió a las 12:30 y el último a las 16:30, sin corrida a las 16:45 porque el workflow quedó **desactivado** en el hueco 16:30–16:45. El operador declara haber dejado el flujo activo unas cinco horas ese día en lugar de las siete habituales, por haber tenido que retirarse. Dos hechos explican el volumen de 8 publicaciones: primero, el último post **nuevo** del día se ingirió a las **13:16**, de modo que los ciclos posteriores no encontraron elementos nuevos —el `upsert` idempotente no reescribe `ingested_at`—; segundo, la jornada cerró a media tarde. El 18/10 no hubo ninguna ejecución del disparador porque el workflow permaneció inactivo, coherente con el cierre de la ventana. La cifra de 8 no es, por lo tanto, evidencia de un corte anómalo, sino la combinación del agotamiento de novedades de la fuente en la primera hora y una jornada más corta de lo habitual.

**Composición por fecha de creación.** De las 724 publicaciones, **437 (60,36 %) fueron creadas dentro de la ventana** (01/10 a 17/10) y **287 (39,64 %) corresponden al arrastre inicial**, con fechas de creación distribuidas entre mayo y septiembre: 8 de mayo, 19 de junio, 28 de julio, 28 de agosto y 204 de septiembre. Esta distinción entre fecha de creación y fecha de ingesta es la que permite separar el comportamiento del sistema en régimen del comportamiento durante la carga inicial, y es la que se aplica en la sección 5.3 para medir la latencia.

La Figura 4 sintetiza la ventana: su panel (a) presenta la serie de ingesta diaria junto con la cantidad de ciclos que efectivamente aportaron publicaciones y su panel (b) el volumen por categoría detectada. El panel (a) no incluye el 03/10, por no haberse registrado recolección alguna ese día.

<figure>
<img src="V4/devoluciones/recuperacion/media/media/image4.png" style="width:5.83333in;height:2.13811in" alt="Figura 4. Serie temporal de la ingesta y categorías detectadas" />
<figcaption aria-hidden="true"><p>Figura 4. Serie temporal de la ingesta y categorías detectadas</p></figcaption>
</figure>

## 5.2. Clasificación temática del corpus

La Tabla 5.3 presenta la distribución temática resultante de aplicar el clasificador vigente sobre el corpus completo.

**Tabla 5.3. Clasificación temática del corpus (n = 724)**

| Categoría | n | % | Puntuación media | `r/netsec` | `r/Malware` | `r/devsarg` |
|----|---:|---:|---:|---:|---:|---:|
| No relevante | 554 | 76,52 % | 0,000 | 84 | 49 | 421 |
| Malware | 79 | 10,91 % | 0,389 | 6 | 73 | 0 |
| Vulnerabilidades | 61 | 8,43 % | 0,320 | 52 | 9 | 0 |
| Phishing | 12 | 1,66 % | 0,250 | 3 | 8 | 1 |
| Robo de Credenciales | 5 | 0,69 % | 0,250 | 3 | 1 | 1 |
| Filtración de Datos | 4 | 0,55 % | 0,250 | 1 | 0 | 3 |
| Ransomware | 4 | 0,55 % | 0,250 | 0 | 4 | 0 |
| Infraestructura y Ataques | 3 | 0,41 % | 0,250 | 0 | 2 | 1 |
| Hacktivismo | 2 | 0,28 % | 0,250 | 1 | 0 | 1 |
| **Total** | **724** | **100,00 %** | — | **150** | **146** | **428** |

Los porcentajes se calculan sobre el total del corpus y suman 100,00 %. Las tres últimas columnas distribuyen cada categoría entre las comunidades de origen. La fila **«No relevante» es la salida residual del clasificador** y no una evaluación de ausencia: son las publicaciones que no registraron ninguna coincidencia con el diccionario, y por lo tanto un subconjunto de ellas puede ser material pertinente que el vocabulario no cubrió. La distinción importa y se sostiene en toda la lectura del capítulo: el recuento informa cuántas publicaciones quedaron **sin clasificar**, no cuántas son irrelevantes en los hechos.

Tres observaciones se desprenden de la tabla:

**El 23,48 % del corpus (170 publicaciones) quedó clasificado en ocho categorías de amenaza**; el 76,52 % restante no registra coincidencias con el diccionario. La proporción de material no relevante es alta y consistente con la naturaleza de las comunidades de origen, donde la mayor parte del contenido es discusión técnica, consulta o difusión general.

**La novena categoría del diccionario no registró ninguna coincidencia en todo el corpus.** «Ingeniería Social» (20 términos) no clasificó ni una publicación a lo largo de toda la ventana. Esto no invalida el diccionario, pero sí acota su alcance verificable: de las nueve categorías definidas, ocho tienen al menos una observación y una carece de evidencia empírica en esta ventana. Sobre esa categoría no se afirma nada en este informe.

**La distribución temática difiere fuertemente entre comunidades.** En `r/netsec` domina *Vulnerabilidades* (52 de 66 publicaciones clasificadas, 78,8 %), mientras que en `r/Malware` domina *Malware* (73 de 97, 75,3 %). El hallazgo es coherente con el objeto declarado de cada comunidad y constituye una validación cualitativa de la plausibilidad del clasificador: agrupa cada comunidad en torno a su tema propio.

**Distribución de la puntuación.** La puntuación normalizada se comporta como sigue sobre las 724 publicaciones: 554 con 0,00; 130 con 0,25; 26 con 0,50; 7 con 0,75; y 7 con 1,00. Esto significa que **130 de las 170 publicaciones clasificadas (76,47 %) fueron asignadas a una categoría de amenaza con una sola coincidencia léxica**, el mínimo exigido por el umbral vigente. Este dato es la clave para interpretar la tasa de error de la sección 5.5 y se retoma en la discusión del Capítulo 6.

## 5.3. Latencia extremo a extremo

La latencia se define como la diferencia entre la fecha de creación de la publicación en la plataforma (`created_utc`) y el instante en que el sistema la persistió (`ingested_at`). Ambas columnas están en la tabla `posts`, de modo que la métrica no requiere instrumentación adicional.

**Tabla 5.4. Latencia extremo a extremo de la ingesta (minutos)**

| Subconjunto | n | Media | Desv. est. | P50 | P95 | Máximo | \> 5 min |
|----|---:|---:|---:|---:|---:|---:|---:|
| Corpus completo de la ventana | 724 | 16.483,8 | 38.407,9 | 889,9 | 117.613,1 | 191.368,8 | 685 (94,6 %) |
| Creadas dentro de la ventana (≥ 01/10) | 437 | 400,6 | 602,4 | 126,9 | 1.376,2 | 7.020,2 | 398 (91,1 %) |
| Creadas desde el 02/10 | 409 | 390,9 | 521,9 | 126,1 | 1.392,2 | 3.031,2 | 374 (91,4 %) |
| Creadas con el motor en ejecución | 126 | — | — | 9,0 | 15,7 | 16,9 | 97 (77,0 %) |
| Creadas con el motor detenido | 311 | — | — | 371,1 | 1.557,3 | 7.020,2 | 301 (96,8 %) |

La lectura de esta tabla exige separar dos fenómenos que la cifra agregada mezcla:

**El corpus completo no es una medida operativa.** La media de 16.483,8 minutos (11,4 días) y el P95 de 117.613,1 minutos (81,7 días) están dominados por el arrastre inicial de 287 publicaciones antiguas, que el sistema ingresó correctamente el 01/10 pero cuya antigüedad no depende del pipeline. El máximo de 191.368,8 minutos (132,9 días) corresponde a una publicación creada el 21/05 y persistida el 01/10: es el efecto de recuperar el *feed* vigente, no un retraso del sistema.

**La medida operativa es el subconjunto creado dentro de la ventana.** Sobre las 437 publicaciones creadas desde el 01/10, la mediana es de **126,9 minutos** (2,1 horas), la media de 400,6 minutos (6,7 horas), el **P95 de 1.376,2 minutos (22,9 horas)** y el máximo de 7.020,2 minutos (4,9 días); el desvío estándar es de **602,4 minutos**, más de una vez y media la media, señal de una distribución de cola larga y no de un centro estable.

**Excluir el día de carga inicial no cambia el diagnóstico.** El subconjunto creado desde el 02/10 (n = 409) —que quita el 01/10, el día del arrastre— reproduce el patrón con valores apenas menores: mediana de 126,1 minutos, P95 de 1.392,2, desvío estándar de **521,9** y un máximo que **cae de 7.020,2 a 3.031,2 minutos** (2,1 días). Es decir, aun sin el efecto del arrastre, la serie mantiene una cola de varios días. Que el máximo de este subconjunto sea un 43 % del máximo del subconjunto anterior confirma que **el extremo de la distribución operativa es sensible al día de carga**, pero que ni la mediana ni el P95 dependen de él: el incumplimiento del umbral de 5 minutos no es un artefacto del 01/10.

**El criterio comprometido no se cumple.** El umbral declarado era una latencia extremo a extremo de **5 minutos** y el resultado medido sobre el subconjunto operativo es de **1.376,2 minutos en el percentil 95**: **398 de las 437 publicaciones (91,1 %) superaron los 5 minutos** y ninguna de las medidas de tendencia central se acerca al umbral. Se declara **NO CUMPLIDO**, sin mover el umbral y sin redefinir la métrica con posterioridad a la observación.

**La causa tiene dos componentes y la cifra agregada las confunde.** El registro de ejecuciones del motor conserva 382 corridas, de las cuales 361 caen dentro de la ventana y cubren del 05/10 al 18/10; las anteriores no quedaron retenidas. Sobre ese tramo, el intervalo entre corridas es de **15,0 minutos de mediana y 19,3 en el percentil 95, con el 100 % en estado** `success`: la cadencia declarada se cumple mientras el motor está en ejecución. Lo que no se cumple es la continuidad. Uniendo los intervalos entre corrida y corrida, el motor estuvo en ejecución **4.929 minutos de los 25.920 de la ventana, es decir el 19,0 %**, en jornadas que comienzan alrededor de las 12:00 y terminan entre las 19:00 y las 23:00 (hora local). Los `ingested_at` de la base confirman el patrón de manera independiente del registro del motor: en ninguno de los 17 días hubo ingesta entre las 19:00 y las 12:00.

**Descompuesta por estado del motor, la latencia deja de ser un valor único.** De las 437 publicaciones creadas dentro de la ventana, **126 fueron creadas con el motor en ejecución** y **311 (71,2 %) con el motor detenido**. En el primer grupo la latencia es de **9,0 minutos de mediana, 15,7 en el percentil 95 y 16,9 en el máximo**: la firma de un ciclo de 15 minutos con la espera fija entre comunidades. En el segundo, la mediana es de 371,1 minutos y el máximo de 7.020,2, porque la publicación no esperó un ciclo sino el arranque siguiente del motor.

**Por comunidad, el ciclo se comporta igual en las tres.** Entre las publicaciones creadas con el motor en ejecución, la mediana es de 9,3 minutos en `r/devsarg` (n = 105), 9,4 en `r/Malware` (n = 8) y 7,1 en `r/netsec` (n = 13), con máximos de 16,9, 15,8 y 13,8 minutos respectivamente. Las diferencias son de orden menor y no hay una comunidad sistemáticamente postergada: el ciclo de 15 minutos domina a las tres.

**Las 254 publicaciones con más de una hora de espera se explican por el mismo factor.** Ninguna de las 126 creadas con el motor en ejecución superó los 60 minutos; las 254 pertenecen al grupo creado con el motor detenido, donde representan el 81,7 %. Revisada esa muestra, no aparece un subconjunto con un comportamiento distinto: son publicaciones creadas entre el cierre de una jornada y la apertura de la siguiente. La interrupción de 44 horas del 02/10 al 04/10 queda incluida en el mismo grupo y no se trata como caso aparte, porque su efecto es idéntico en naturaleza —el motor no estaba ejecutándose— y separarla habría sugerido una causa distinta que los datos no muestran.

**Corrección de una afirmación de la V4.** La versión anterior sostenía que el «piso teórico del diseño» era de 15 a 17 minutos. Es incorrecto en los dos sentidos: 15 minutos es el **período** del ciclo y, por lo tanto, una **cota superior de la espera** para una publicación que aparece justo después de una consulta, no un piso; y el piso real es cercano a cero, como muestra el mínimo observado de **0,3 minutos (18 segundos)**, correspondiente a una publicación que ya estaba en el listado cuando el ciclo la consultó. Con un período de 15 minutos y arribos uniformes, la espera esperada es de 7,5 minutos, coherente con la mediana de 9,0 del grupo en ejecución.

**El umbral de 5 minutos era inalcanzable con este diseño, y la operación intermitente lo agravó.** Con tres comunidades consultadas en serie y 60 segundos de espera entre cada una, la tercera se consulta al menos dos minutos después de iniciado el ciclo, de modo que una publicación creada justo después de su turno espera el período completo: ninguna configuración de este diseño podía garantizar 5 minutos extremo a extremo. A eso se sumó que el motor no corrió de manera continua, lo que explica el 71,2 % de las publicaciones y la mayor parte de la mediana agregada. Se declara **NO CUMPLIDO** por ambas razones, sin mover el umbral y sin excluir del cálculo las publicaciones creadas con el motor detenido: el criterio se comprometió sobre el servicio tal como se prestó, y así se informa.

## 5.4. Motor de detección de anomalías

El motor produjo **112 registros de evaluación** (entre 6 y 8 categorías por jornada) en **15 días evaluados**, con **6 disparos** y **6 alertas** registradas. Las 15 jornadas evaluadas son el 01/10 y del 04/10 al 17/10, es decir 15 de las **16 fechas con ingesta** de la ventana: el **02/10 quedó sin evaluar** porque la corrida que debía contarlo era la del 03/10, que no se ejecutó por la interrupción del servicio.

**Tabla 5.5. Disparos del motor de anomalías (6 en total)**

| Día evaluado | Corrida | Categoría                 | Observado | Línea base | Umbral |
|--------------|---------|---------------------------|----------:|-----------:|-------:|
| 01/10        | 02/10   | Malware                   |        55 |        0,0 |      3 |
| 01/10        | 02/10   | Vulnerabilidades          |        41 |        0,0 |      3 |
| 01/10        | 02/10   | Phishing                  |         6 |        0,0 |      3 |
| 01/10        | 02/10   | Ransomware                |         3 |        0,0 |      3 |
| 01/10        | 02/10   | Infraestructura y Ataques |         3 |        0,0 |      3 |
| 12/10        | 13/10   | Vulnerabilidades          |         4 |        0,8 |      3 |

**Los cinco disparos del 02/10 son un artefacto de la carga inicial, no una detección.** Corresponden al día 01/10, cuando el arrastre inicial ingresó 307 publicaciones y, con ellas, 112 de las 170 publicaciones clasificadas como amenaza de toda la ventana. El motor comparó ese volumen contra una línea base de cero —no existían días anteriores con datos— y, con el piso absoluto de tres, disparó en las cinco categorías que superaron ese umbral. La anomalía es del corpus, no del fenómeno: **la carga inicial se comporta como un pico y el motor lo reporta correctamente como tal**. Su tratamiento en un sistema en producción sería una marca de exclusión para los primeros días posteriores a una carga histórica.

**El disparo del 13/10 fue el único que correspondió a actividad real de las comunidades.** Corresponde al día 12/10, con **cuatro publicaciones de Vulnerabilidades** frente a una línea base de 0,8 y un umbral de 3. Como el conteo se hace por fecha de ingesta (3.5), la ventana incluye publicaciones creadas días antes y excluye las creadas el 13/10 aunque ya estuvieran visibles. Las cuatro publicaciones contabilizadas son: *Google paid me \$90,000 for this RCE* (`C-11`, `r/netsec`, puntuación 0,25); *CVE-2026-91768: FastCGI allowed_clients compared only 96 of an IPv6 address* (`C-12`, `r/netsec`, 0,25); *LG webOS sync-demo Preauth RCE* (`C-05`, `r/netsec`, 0,50); y *How do you vet browser-based WASM game ports (GTA V, BO1 Zombies) for malicious content* (`C-13`, `r/Malware`, 0,25), creada el 10/10 e ingresada el 12/10. Las cuatro describen vulnerabilidades reales y dos de ellas remiten a divulgaciones concretas con identificador o recompensa asociada, de modo que el aviso apuntó a contenido verificable y no a ruido. Si esa jornada fue además **inusual** para la comunidad es una pregunta distinta, que se responde en 5.4.1 y cuya respuesta es negativa.

Los agregados por categoría —evaluaciones emitidas, publicaciones observadas, disparos y umbrales— se presentan en la Tabla 5.6.

**Tabla 5.6. Evaluaciones del motor por categoría**

| Categoría | Evaluaciones | Observados | Disparos | Línea base media | Umbral medio |
|----|---:|---:|---:|---:|---:|
| Vulnerabilidades | 15 | 59 | 2 | 2,95 | 6,87 |
| Malware | 15 | 79 | 1 | 4,00 | 8,33 |
| Filtración de Datos | 15 | 4 | 0 | 0,19 | 3,00 |
| Phishing | 15 | 11 | 1 | 0,57 | 3,00 |
| Robo de Credenciales | 15 | 5 | 0 | 0,25 | 3,00 |
| Hacktivismo | 14 | 2 | 0 | 0,11 | 3,00 |
| Ransomware | 14 | 4 | 1 | 0,24 | 3,00 |
| Infraestructura y Ataques | 9 | 3 | 1 | 0,27 | 3,00 |
| **Total** | **112** | **167** | **6** | — | — |

**El número de evaluaciones por categoría no es constante y la causa está identificada.** El motor no emite fila cuando la categoría no registra publicaciones en la ventana móvil de once días: por eso *Hacktivismo* y *Ransomware* tienen 14 evaluaciones y *Infraestructura y Ataques* solo 9. Tampoco evaluó «Ingeniería Social», que no registró ninguna publicación en el corpus, coherente con el hallazgo de 5.2.

**Los observados acumulados (167) no coinciden con las 170 publicaciones clasificadas.** La diferencia son las **tres publicaciones ingeridas el 02/10**: la corrida que debía contarlas es la del **03/10**, que no se ejecutó por la interrupción del servicio. El 03/10 no registró ingesta alguna, de modo que el hueco de datos y la ausencia de corrida son el mismo hecho, y por eso el faltante es de tres y no de ocho. La verificación cruzada confirma el diagnóstico de 5.1: **el corte de la ingesta y la ausencia de evaluaciones del motor coinciden en causa y en intervalo**.

**Los umbrales altos de las categorías con línea base alta confirman que la corrección de la fórmula opera.** *Malware* y *Vulnerabilidades* presentan umbrales promedio de 8,33 y 6,87 respectivamente, resultado del cuantil 95 de sus líneas base. Con la fórmula defectuosa descrita en 4.5 esas dos categorías tenían un umbral inalcanzable. Es decir, **el mecanismo de umbralización opera como fue especificado**: exige un volumen elevado en las categorías frecuentes y un piso de tres en las esporádicas. Que el umbral, cuando se alcanza, corresponda a una anomalía real es una cuestión distinta, que el recálculo de 5.4.1 responde de forma negativa.

**Alertas registradas.** Las **6 alertas** fueron persistidas con canal `telegram` y estado `PENDIENTE`, lo que confirma que el registro funciona y que **no hubo entrega efectiva** a ningún destinatario. Este resultado determina la evaluación del objetivo OE6 (5.8): la alerta se genera y se registra; la notificación externa, no.

**Contenido de una alerta (payload enmascarado).** Se publica el contenido real de una de las seis alertas registradas, con el destinatario enmascarado, para que pueda auditarse qué se habría enviado y verificarse que **no contiene datos personales**:

    {
      "umbral": 3,
      "categoria": "Infraestructura y Ataques",
      "base_media": 0,
      "n_observado": 3,
      "ventana_inicio": "2026-10-01T03:00:00+00:00"
    }

El `payload` es un objeto `jsonb` construido por el propio motor con cinco campos —categoría, conteo observado, línea base media, umbral aplicado y ventana—, **sin identificador de publicación, de autor ni de subreddit**: el mensaje describe una anomalía estadística agregada, no un incidente concreto, de modo que la alerta no reintroduce por la vía de la notificación los datos que la seudonimización protege en la ingesta (4.3 y 6.4). El destinatario, enmascarado aquí como `canal_tfi`, se resuelve en la variable de entorno `TELEGRAM_CHAT_ID` del contenedor, y el token del bot en `TELEGRAM_BOT_TOKEN`; ninguno de los dos aparece en el artefacto versionado ni en la base (4.6 y Anexo B). El canal se codifica como `telegram` en las seis filas, y el estado `PENDIENTE` confirma la ausencia de entrega.

### 5.4.1. Recalculo retrospectivo sobre `created_utc`

**Por qué se recalcula.** El motor cuenta por `ingested_at`, de modo que su serie mide la operación del sistema —la carga inicial del 01/10, la interrupción del 02 al 04/10— tanto como la actividad de las comunidades. Una medición de eficacia exige separar ambas cosas. El motor es determinista sobre la base, así que puede recalcularse sobre el corpus ya persistido, sin tocar la tabla de producción, con tres criterios: **(i)** conteo por `created_utc` de las publicaciones creadas dentro de la ventana; **(ii)** exclusión de la carga inicial y de los días sin operación de la línea base; **(iii)** línea base dividida por los días efectivamente operados.

**Línea base recalculada.** Sobre los quince días con ingesta comprendidos entre el 02/10 y el 17/10 (el 03/10 no hubo recolección), la media diaria de publicaciones creadas es de **1,40** para *Malware* (21 en total), **1,27** para *Vulnerabilidades* (19), **0,40** para *Phishing* (6) y de 0,20 o menos en las cuatro categorías restantes (Filtración de Datos 2, Robo de Credenciales 3, Hacktivismo 1, Ransomware 1). Aplicando la regla del motor —cuantil 95 más uno, con piso de tres— los umbrales resultantes son **5, 4, 3, 3, 3, 3 y 3** respectivamente.

**Resultado.** Sobre **105 evaluaciones** (15 días por 7 categorías con actividad), el número esperado de disparos bajo la hipótesis nula es **0,95** y los disparos observados son **0**. Ninguna jornada alcanza su umbral: el máximo de *Malware* es de 4 publicaciones (03/10 y 05/10) frente a un umbral de 5, y el máximo de *Vulnerabilidades* es de 3 (12/10 y 16/10) frente a un umbral de 4.

**El disparo de producción no sobrevive al recálculo.** Con la serie por `created_utc`, la jornada del 12/10 registra **3** publicaciones de *Vulnerabilidades* frente a un umbral de **4**: no dispara. Disparó en producción porque el 13/10 la ventana móvil de diez días perdió el 01/10 y la línea base cayó de **4,9 a 0,8**, con el umbral bajando de 10 a 3. Es una discontinuidad que produce el calendario de la ventana, no la actividad de la comunidad: el mismo corpus, evaluado un día antes y un día después, cambia de régimen.

**Falsas alarmas esperadas frente a disparos observados.** El techo nominal de la regla es del 5 % por evaluación —unos cinco disparos esperados en 105 evaluaciones—, y el valor efectivo con los umbrales calculados es de 0,95. Los seis disparos registrados superan ambos valores, pero cinco de ellos provienen de la corrida del 02/10 con línea base nula y el sexto de la discontinuidad descrita. Es decir: **el motor no produjo en quince días ni una detección que el recálculo sostenga**, y el único aviso sobre contenido real no distingue una jornada inusual de una ordinaria.

**Referencia externa para juzgar el disparo.** Las tres publicaciones de *Vulnerabilidades* creadas el 12/10 remiten a divulgaciones verificables y contemporáneas: la cadena de RCE preautenticación en LG webOS, CVE-2026-91768 (comparación parcial de direcciones IPv6 en FastCGI) y un RCE premiado por Google con 90.000 dólares. Son hechos reales, pero no constituyen una jornada inusual: en `r/netsec`, **52 de las 66** publicaciones clasificadas (78,8 %) son de esa categoría, de modo que tres en un día es el comportamiento ordinario de la comunidad y no un desvío.

**Conclusión.** El motor está implementado, es determinista, registra sus decisiones negativas y su regla es estadísticamente defendible; lo que no está demostrado es su **eficacia**. Sobre la serie correcta no emite avisos, y el único disparo sobre contenido real se explica por una discontinuidad de la línea base inducida por el calendario de la carga inicial. OE5 se declara por lo tanto **implementado; eficacia no demostrada** (Tabla 7.2).

## 5.5. Desempeño del clasificador sobre el corpus B5

**Alcance de esta medición.** A diferencia de la evaluación previa, esta validación se hizo sobre el **corte exacto del corpus de 5.1**: las 724 publicaciones de la ventana B5, sin comunidades desactivadas y sin material de otro período. Se etiquetaron **352 casos** —el censo de las 170 que el clasificador marcó como amenaza y una muestra sorteada de 182 entre las 554 que marcó como «No relevante»—, con tres anotadores y consenso registrado (3.3.2). Las cifras que siguen describen, por lo tanto, el desempeño del clasificador **sobre el corpus de este informe**, no sobre un corpus distinto. La Tabla 5.7 presenta la matriz estratificada y la Tabla 5.8 los estimadores con sus intervalos exactos.

**5.5.2. Diseño de validación: tres anotadores con kappa de Fleiss**

A diferencia del antecedente (dos anotadores con kappa de Cohen), la validación V5 se realizó con **tres anotadores internos con adjudicación por consenso**. Se optó por este diseño por su mayor robustez ante las fronteras difusas del dominio bilingüe (español rioplatense e inglés técnico) y para disponer de un tercer criterio en caso de desacuerdo. El acuerdo se cuantificó con **kappa de Fleiss** sobre una submuestra común de 50 casos (ver 3.3.2). Los resultados se desagregan por comunidad (Tabla 5.9) y por idioma (Tabla 5.9.b).

**Tabla 5.7. Matriz de confusión estratificada de la validación V5 (352 casos etiquetados)**

|  | Clasificador: amenaza | Clasificador: no relevante | Total |
|----|---:|---:|---:|
| **Estrato 1 (censo, N = 170)** — referencia: amenaza | **TP = 144** | — | 144 |
| **Estrato 1 (censo, N = 170)** — referencia: no relevante | **FP = 26** | — | 26 |
| **Estrato 2 (muestra, n₀ = 182)** — referencia: amenaza | — | **FN = 30** | 30 |
| **Estrato 2 (muestra, n₀ = 182)** — referencia: no relevante | — | **TN = 152** | 152 |
| **Total etiquetado** | 170 | 182 | **352** |

Los guiones no son celdas vacías: cada estrato existe por definición en una sola columna del clasificador, de modo que la matriz es de dos bloques y no un cuadrado de cuatro celdas. El estrato 1 es el censo completo de las predicciones positivas; el estrato 2 es una muestra de las predicciones negativas, y por eso sus conteos se expanden con el peso de muestreo.

**Tabla 5.8. Métricas de clasificación e intervalos de confianza exactos (validación V5)**

| Métrica | Fórmula | Valor | IC 95 % (exacto) | Alcance |  |
|----|----|----|---:|----|----|
| Precisión | `TP / (TP + FP)` = 144/170 | **0,847** | \[0,784; 0,898\] | Censada, sin error de muestreo |  |
| Sensibilidad (*recall*) | `TP / (TP + w·k)` = 144/(144 + 3,044·30) | **0,612** | \[0,534; 0,695\] | Ponderada por el muestreo del estrato 2 |  |
| F1-score | media armónica de P y S | **0,711** | \[0,635; 0,783\] | Derivada; intervalo conservador |  |
| Tasa de falsos descubrimientos | `FP / (TP + FP)` = 26/170 | **0,153** | — | Complemento de la precisión |  |
| Omisión en el estrato 2 | 30 de 182 | **0,165** | \[0,114; 0,227\] | Fuente de la incertidumbre de la sensibilidad |  |
| Exactitud de categoría | 116 de 144 amenazas detectadas | **0,806** | — | Solo entre las que ambos marcan como amenaza |  |

El peso de muestreo es **w = N₀/n₀ = 554/182 = 3,044**: cada omisión encontrada en las 182 sorteadas representa a tres omisiones del estrato completo. La estimación puntual de amenazas en el corpus es, por lo tanto, de **235 publicaciones** (144 censadas más 30 × 3,044 = 91,3 expandidas), es decir el **32,5 %** de las 724, frente a las 170 que marcó el clasificador.

**Contraste con los criterios comprometidos.** Este es el punto donde la V5 se separa de la V4 y conviene decirlo sin rodeos: **solo uno de los tres criterios de clasificación se cumple**.

**Precisión (0,847 ≥ 0,80): cumplida.** El intervalo exacto íntegro queda por encima del umbral.

**Sensibilidad (0,612 ≥ 0,80): NO cumplida.** El intervalo completo queda por debajo. El clasificador omite aproximadamente un tercio de las publicaciones que la referencia considera amenaza.

**F1 (0,711 ≥ 0,80): NO cumplido.** Es la consecuencia aritmética de la sensibilidad.

La diferencia con la cifra de 0,931 que informaba la versión anterior no proviene de un cambio en el clasificador sino del **estimador**. La V4 calculaba la sensibilidad como `TP / (TP + FN)` dentro de una muestra de 50 casos, sin ponderar por el tamaño del estrato negativo: eso equivale a suponer que las 22 publicaciones sorteadas como «No relevante» representaban al conjunto de las 554, cuando en realidad representaban una de cada veinticinco. El estimador correcto, con el peso declarado, arroja el valor de la Tabla 5.8. La corrección estaba prevista en el diseño de la validación (3.3.2) y es el motivo por el cual se rehizo la muestra. El protocolo actual emplea **tres anotadores con kappa de Fleiss** (frente a los dos anotadores con kappa de Cohen del antecedente), con adjudicación por consenso, y reporta el acuerdo obtenido (κ = 0,509) tal como fue medido.

**Desempeño por comunidad.** La desagregación muestra que el comportamiento no es homogéneo y que el agregado lo esconde (Tabla 5.9):

**Tabla 5.9. Desempeño del clasificador por comunidad (validación V5, 352 casos)**

| Comunidad | Predicciones positivas (censo) | TP | FP | Precisión | Muestra del estrato negativo | Omitidas | Omisión |
|----|---:|---:|---:|---:|---:|---:|---:|
| `r/netsec` | 66 | 60 | 6 | **90,9 %** | 29 | 15 | **51,7 %** |
| `r/Malware` | 97 | 81 | 16 | **83,5 %** | 18 | 13 | **72,2 %** |
| `r/devsarg` | 7 | 3 | 4 | **42,9 %** | 135 | 2 | **1,5 %** |

Dos lecturas se imponen. Primera: **el clasificador es preciso en las comunidades técnicas en inglés** y falla en la local, donde 4 de sus 7 detecciones son falsos positivos —un resultado que confirma, con etiquetado ciego y tres anotadores, la estimación que la V4 había adelantado para esa comunidad—. Segunda: **la omisión se concentra en** `r/Malware` **(72,2 %) y** `r/netsec` **(51,7 %)**, es decir en las comunidades que producen el material que el sistema debe detectar. La causa es la misma que documenta la Tabla 5.12: el diccionario no cubre el vocabulario técnico de esas comunidades (`edr`, `red team`, nombres de familias, siglas de herramientas). Los denominadores por comunidad son chicos —18 y 29 casos en la muestra— de modo que las tasas de omisión por comunidad deben leerse como orientación y no como estimaciones de precisión comparable a la del agregado.

**Tabla 5.9.b. Desempeño por idioma (español/inglés), validación V5**

| Idioma | Comunidades | Censo estrato 1 (n) | TP | FP | Precisión | Muestra estrato 2 (n) | Omitidos | Omisión |
|----|----|---:|---:|---:|---:|---:|---:|---:|
| **Español rioplatense** | `r/devsarg` | 7 | 3 | 4 | **42,9 %** | 135 | 2 | **1,5 %** |
| **Inglés** | `r/netsec` + `r/Malware` | 163 | 141 | 22 | **86,5 %** | 47 | 28 | **59,6 %** |
| **Total** | Las tres comunidades | 170 | 144 | 26 | **84,7 % \[78,4; 89,8\]** | 182 | 30 | **16,5 % ponderado \[11,4; 22,7\]** |

El desglose por idioma confirma lo observado: en **inglés** el clasificador es preciso (86,5 %) pero presenta una omisión elevada (59,6 %) en las comunidades técnicas que concentran la mayor parte de las publicaciones relevantes. En **español rioplatense** (`r/devsarg`) la omisión es baja (1,5 %) aunque la precisión es reducida (42,9 %), con un censo muy reducido (n=7) que obliga a leer esa cifra con extrema cautela. El estimador ponderado global es el que corresponde al corpus completo.

**Tabla 5.10. Matriz de confusión por categoría (referencia × clasificador, 352 casos)**

| Referencia ↓ / Clasificador → | Malware | Vulnerabilidades | Phishing | Ransomware | Robo de Credenciales | Filtración de Datos | Infraestructura y Ataques | Hacktivismo | No relevante |
|----|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Malware** | **59** | 7 | 5 | 2 | 2 | 0 | 1 | 0 | 14 |
| **Vulnerabilidades** | 2 | **49** | 2 | 0 | 1 | 1 | 0 | 0 | 12 |
| **Phishing** | 1 | 0 | **5** | 0 | 0 | 0 | 0 | 0 | 3 |
| **Ransomware** | 0 | 0 | 0 | **2** | 0 | 0 | 0 | 0 | 0 |
| **Robo de Credenciales** | 0 | 0 | 0 | 0 | **0** | 1 | 0 | 0 | 0 |
| **Filtración de Datos** | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 1 |
| **Infraestructura y Ataques** | 1 | 0 | 0 | 0 | 1 | 0 | **1** | 1 | 0 |
| **No relevante** | 16 | 5 | 0 | 0 | 1 | 2 | 1 | 1 | **152** |

La diagonal concentra **268 de los 352 casos** (76,1 %), pero esa cifra está dominada por el acuerdo en «No relevante» (152 casos) y por eso no debe leerse como acierto temático. Entre las publicaciones que ambos marcan como amenaza, la categoría coincide en **116 de 144 (80,6 %)**: cuando el clasificador detecta, generalmente acierta la categoría. El error de categoría más frecuente es la confusión **Malware ↔ Vulnerabilidades** (7 y 2 casos) y la asignación de *Malware* a material de *Phishing* (5 casos). Las dos categorías peor resueltas son **Filtración de Datos** y **Robo de Credenciales**, con cero aciertos sobre una base mínima —una y un caso respectivamente—, de modo que no hay evidencia suficiente para afirmar ni negar su funcionamiento. *Ingeniería Social* no registró ninguna coincidencia en todo el corpus, ni como predicción ni como etiqueta de referencia.

### 5.5.1. La medición previa de la V4 y por qué se reemplaza

La evaluación anterior se hizo el **30/09/2026** sobre 50 publicaciones del corpus vigente en esa fecha, con **un solo anotador** y sin medida de acuerdo. Sus cifras —precisión, sensibilidad y F1 de 0,931— no son comparables con las de la Tabla 5.8 por tres razones acumulativas: el estimador de sensibilidad no estaba ponderado por el tamaño del estrato negativo; la muestra provenía de un corpus anterior que incluía comunidades desactivadas después (10 de sus 50 casos eran de `r/DerechoGenial`, ausente de la ventana B5); y no existía una segunda etiqueta que permitiera medir el error del etiquetado. Se conserva aquí porque sostiene una comparación que sigue siendo válida —el efecto de la corrección del umbral del clasificador sobre el mismo texto— y porque su análisis de errores anticipó los patrones que la validación nueva confirma.

**Tabla 5.11. Efecto de la corrección del clasificador (muestra del 30/09/2026, n = 50, mismo texto)**

| Cantidad o métrica | Clasificador anterior (`MIN_HITS = 2`) | Clasificador vigente (`MIN_HITS = 1`) | Cambio |
|----|---:|---:|---:|
| TP | 24 | **27** | +3 |
| FP | 4 | **2** | −2 |
| FN | 5 | **2** | −3 |
| TN | 17 | **19** | +2 |
| Precisión | 0,857 | **0,931** | +0,074 |
| Sensibilidad (estimador de la V4, no ponderado) | 0,828 | **0,931** | +0,103 |
| F1-score | 0,842 | **0,931** | +0,089 |
| Acierto exacto de categoría | 37/50 = 74,0 % | **42/50 = 84,0 %** | +10,0 pp |

La corrección consistió en bajar el umbral de coincidencias de 2 a 1 y en retirar el término `dni` del diccionario de *Filtración de Datos*, que activaba la categoría ante publicaciones sobre trámites administrativos. El efecto neto es una mejora simultánea de precisión y sensibilidad, lo que se explica porque el umbral anterior descartaba señales válidas: **las publicaciones descritas con un solo término del diccionario no son necesariamente ruido, y exigir dos coincidencias eliminaba detecciones correctas**. La comparación entre ambos umbrales sigue siendo válida porque se hizo sobre el mismo texto y con el mismo anotador; lo que no era válido era extrapolar su sensibilidad al corpus.

**Sobre la diferencia entre lo almacenado y el artefacto.** La medición directa sobre la base arrojaba TP = 24 y FP = 4 (F1 = 0,842). La causa no era el texto ni el diccionario, sino **3 filas que conservaban la clasificación de una versión previa del clasificador**, con una puntuación de 0,2 que no pertenece a la escala vigente (la puntuación mínima actual, con una coincidencia, es 0,25). Esas tres filas explican la diferencia de verdaderos positivos entre la medición sobre la base y la del artefacto (24 frente a 27); la diferencia de falsos positivos (4 frente a 2) se desagrega en la Tabla 5.12 y no altera el sentido de la comparación. La evaluación se realizó ejecutando el nodo de código del artefacto desplegado sobre el texto exacto de las publicaciones, sin reimplementar el diccionario. Se verificó además que **ninguna de las 724 publicaciones de la ventana B5 conserva la puntuación de 0,2**, de modo que el problema es ajeno al corpus analizado en este capítulo. La Tabla 5.12 desagrega las discrepancias que subsisten y las atribuye a una causa declarada.

**Tabla 5.12. Análisis de errores del clasificador vigente (muestra del 30/09/2026, n = 50)**

| Tipo de discrepancia | n | Casos | Causa declarada |
|----|---:|----|----|
| Falsos negativos | 2 | *EDR evasion* y *Red team sobre ServiceNow* (`r/netsec`, puntuación 0,0 en ambos) | Ausencia de vocabulario en el diccionario. No se agregaron términos por decisión metodológica |
| Falsos positivos | 2 | Catálogo open-source de +2.800 familias de malware (`r/Malware`, 0,50); suplantación de identidad en redes sociales (`r/DerechoGenial`, 0,25) | El diccionario marca material de defensa y contenido fuera del ámbito del proyecto |
| Aciertos con categoría distinta | 4 | Cuatro publicaciones de `r/Malware` que el anotador etiquetó como *Infraestructura y Ataques* y el sistema como *Malware* (3) o *Vulnerabilidades* (1) | Ambigüedad de frontera de la taxonomía, no defecto de cobertura |

Los **dos falsos negativos** comparten una misma causa: el diccionario no contiene `edr` ni `red team` en los términos de las categorías correspondientes. La decisión adoptada fue **no incorporarlos**: definirlos sin respaldo técnico habría replicado, dentro del diccionario, la misma falta de criterio que se estaba corrigiendo. La validación nueva confirma que ese diagnóstico era el correcto y lo amplía: la omisión no es de dos casos aislados sino de una proporción estimada del 16,5 % del estrato negativo, concentrada en `r/Malware` y `r/netsec`. Los **cuatro desacuerdos de categoría** no afectan la detección binaria —el sistema detectó correctamente las cuatro publicaciones como amenaza— y anticipan la frontera Malware ↔ Vulnerabilidades que la Tabla 5.10 vuelve a mostrar. Se trata de una frontera de taxonomía discutible en la que no hay una respuesta técnicamente única, y se declara como tal en lugar de presentarla como error resuelto.

## 5.6. Extracción de entidades del corpus

La extracción de entidades es el segundo producto del análisis lingüístico de OE4, posterior e independiente de la clasificación temática. Se aplica a **las 724 publicaciones** del corpus y reconoce cinco familias —direcciones IP, identificadores CVE, correos, dominios y nombres de productos o tecnologías— que se persisten en la columna `entities` (tipo `jsonb`) de `posts`. Se informa aquí su rendimiento real, porque la versión previa describía el mecanismo pero no publicaba ni un solo resultado.

**Tabla 5.13. Extracción de entidades sobre el corpus (n = 724)**

| Familia | Publicaciones con ≥ 1 | Valores distintos extraídos | Valores totales |
|----|---:|---:|---:|
| Productos o tecnologías | 220 | 14 | 242 |
| Dominios | 77 | 55 | 93 |
| Identificadores CVE | 32 | 43 | 47 |
| Correos electrónicos | 9 | 9 | 10 |
| Direcciones IP | 4 | 8 | 8 |
| **Alguna entidad** | **286** | — | **400** |

El 39,5 % del corpus (286 de 724 publicaciones) contiene al menos una entidad reconocida; el resto no registra ninguna. La distribución por comunidad es coherente con la naturaleza de cada subreddit: `r/netsec` concentra la extracción de CVE (27 de las 32 publicaciones con identificador, 84,4 %), mientras que `r/devsarg` aporta el mayor volumen de menciones de productos (150 publicaciones) y `r/Malware` el de dominios (41). Por categoría temática, *Vulnerabilidades* es la que más CVE aporta (28 de sus 61 publicaciones) y *Malware* la que más dominios (31 valores).

**Distribución por comunidad (publicaciones con al menos una entidad)**

| Subreddit   | Publicaciones | Con entidad | CVE |  IP | Correo | Dominio | Producto |
|-------------|--------------:|------------:|----:|----:|-------:|--------:|---------:|
| `r/devsarg` |           428 |         162 |   0 |   1 |      4 |      27 |      150 |
| `r/netsec`  |           150 |          51 |  27 |   1 |      2 |       9 |       23 |
| `r/Malware` |           146 |          73 |   5 |   2 |      3 |      41 |       47 |

**Cómo reconoce el sistema cada familia, y qué falla.** CVE, correos, IP y dominios se detectan con expresiones regulares sobre el texto normalizado: el patrón de CVE (`cve-\d{4}-\d{4,7}`) exige el prefijo y el formato de año y secuencia; el de IP valida la forma de cuatro octetos; el de dominio restringe la terminación a `com|ar|org|net|io|gov|edu`; el de correo exige el arroba y un punto en el dominio. **Los nombres de productos o tecnologías no se detectan con una expresión regular**, y esta es la precisión que faltaba en la versión previa: se reconocen por **coincidencia de subcadena** contra una **lista blanca fija de 18 términos** —`whatsapp`, `telegram`, `mercado pago`, `windows`, `linux`, `android`, `ios`, `chrome`, `firefox`, `bitcoin`, `usdt`, `afi p`, `banco nacion`, `galicia`, `santander`, `uala`, `cvu`, `mercado libre`— aplicada sobre el texto en minúsculas y sin diacríticos (`low.includes(p)`). El diccionario de productos es, por lo tanto, cerrado y enumerable, no un patrón.

Ese mecanismo de subcadena tiene un modo de error concreto y medible que el informe declara: `ios` **coincide con la secuencia de letras de «servicios», «estudios», «comentarios», «propios», «negocios» y palabras semejantes**. De las 128 publicaciones que el sistema marca como «con entidad ios», solo **5 contienen «ios» como palabra aislada**; las **123 restantes (96,1 %)** son coincidencias morfológicas dentro de otra palabra. El efecto sobre los agregados es acotado pero no nulo: 111 publicaciones quedan con `ios` como su única entidad, de modo que la cifra de «220 publicaciones con producto» está sobreestimada por esa vía. La lista blanca también produce dos falsos positivos de otra familia, igualmente declarados: los patrones de correo capturan dos especificaciones de paquetes (`dotenv@1.0.0`, `tensorlake@0.5.144`), que tienen la forma `nombre@versión` sin ser direcciones.

**Corrección diferida, no aplicada.** La corrección de este defecto —anclar la coincidencia de productos a límites de palabra y depurar la lista blanca— **no se aplica en esta versión**, por la misma razón que se congeló el diccionario de categorías (sección 4.4.1): cambiar el extractor ahora invalidaría la correspondencia entre el artefacto versionado y los resultados ya publicados, y obligaría a rehacer toda la extracción. Se documenta como limitación y se incorpora a las recomendaciones (Tabla 8.1). La cifra honesta de publicaciones con producto reconocido es, por lo tanto, un **límite superior**; el número de publicaciones con CVE, dominio, correo o IP no está afectado por este defecto.

## 5.7. Casos representativos del corpus

**Tabla 5.14. Casos representativos del corpus B5**

| Publicación | Categoría | Puntuación | Comunidad | Creada | Ingerida | Qué ilustra |
|----|----|---:|----|----|----|----|
| `C-01` | Malware | 1,00 | `r/Malware` | 14/10 | 14/10 | Advertencia sobre un repositorio falso que distribuye un *infostealer*: detección de máxima confianza sobre un incidente en curso |
| `C-02` | Malware | 1,00 | `r/Malware` | 03/10 | 04/10 | Cargador de mando y control preinstalado en proyectores Android. Creada durante el hueco operativo y recuperada en el ciclo siguiente |
| `C-03` | Malware | 1,00 | `r/Malware` | 10/06 | 01/10 | Ataque *ClickFix* con CAPTCHA falso de Cloudflare. Caso de arrastre inicial: 113 días entre creación e ingesta |
| `C-04` | Vulnerabilidades | 0,50 | `r/netsec` | 09/10 | 09/10 | Cadena de RCE preautenticación en PaperCut; el hilo remite a los avisos WT-2026-0141-0144 y a CVE-2026-82077, CVE-2026-82078 y CVE-2026-81578. Misma jornada de creación e ingesta |
| `C-05` | Vulnerabilidades | 0,50 | `r/netsec` | 12/10 | 12/10 | RCE preautenticación en LG webOS, una de las cuatro publicaciones que provocaron el único disparo del motor sobre actividad de las comunidades |
| `C-06` | Hacktivismo | 0,25 | `r/devsarg` | 12/10 | 12/10 | Ataque al sitio oficial de una fundación local: caso de relevancia local que un diccionario solo en inglés no habría detectado |
| `C-07` | Phishing | 0,25 | `r/devsarg` | 13/10 | 13/10 | Falso reclutador que solicita correo y contraseña de LinkedIn: patrón de ingeniería social en español |
| `C-08` | Robo de Credenciales | 0,25 | `r/devsarg` | 15/10 | 15/10 | **Falso positivo**: discusión sobre ingeniería inversa de videojuegos, sin amenaza |
| `C-09` | Filtración de Datos | 0,25 | `r/devsarg` | 10/10 | 10/10 | **Falso positivo**: consulta sobre cómo almacenar datos personales en una aplicación |
| `C-10` | Infraestructura y Ataques | 0,25 | `r/devsarg` | 26/09 | 01/10 | **Falso positivo**: reflexión sobre aprendizaje e inteligencia artificial, sin relación con ataques |

**Términos que coincidieron en cada caso.** La traza se obtuvo con la misma reimplementación validada de 4.4.1. `C-01`: `malware`, `infostealer`, `loader`, `payload` (4 coincidencias, puntuación 1,00). `C-02`: `malware`, `dropper`, `loader`, `c2 server`, `obfuscated`, `payload` (6, 1,00). `C-03`: `malware`, `infostealer`, `dropper`, `rat`, `obfuscated`, `payload` (6, 1,00). `C-04`: `cve`, `rce` (2, 0,50). `C-05`: `exploit`, `rce` (2, 0,50). `C-06`: `hackearon` (1, 0,25). `C-07`: `phishing` (1, 0,25). `C-08`: `clonar` (1, 0,25). `C-09`: `datos personales` (1, 0,25). `C-10`: `botnet` (1, 0,25). `C-11`: `rce` (1, 0,25). `C-12`: `cve` (1, 0,25). `C-13`: `rce` (1, 0,25). Los cuatro casos del disparo del 12/10 son `C-05`, `C-11`, `C-12` y `C-13`, de modo que el aviso se activó por la repetición de dos términos —`rce` y `cve`— en cuatro publicaciones distintas. La traza hace visible el mecanismo de los falsos positivos: cada uno se activó con **un único término del diccionario**, y en dos de ellos (`clonar`, `datos personales`) ese término es genérico del dominio de desarrollo.

**Códigos de caso en lugar de identificadores.** Las publicaciones se identifican con códigos `C-01` a `C-13` en lugar de su identificador público. La razón es de minimización: esos identificadores permiten abrir el hilo original, donde aparecen nombres de usuario y contenido de terceros, y el informe se distribuye fuera del repositorio del proyecto. La correspondencia entre cada código y su identificador, comunidad, fecha, puntuación y URL se conserva en el archivo `correspondencia_casos_v5.csv`, que se entrega junto con la evidencia y permite verificar cada caso sin publicar los identificadores en el cuerpo del documento. Los códigos `C-11` a `C-13` corresponden a tres de las cuatro publicaciones del disparo del 13/10 descrito en 5.4; la cuarta es `C-05`.

Los tres primeros casos ilustran el funcionamiento del sistema en su mejor registro: publicaciones que describen campañas activas, detectadas con la puntuación máxima. El primero y el segundo, además, fueron creados y detectados durante la ventana, lo que demuestra que el sistema **detecta hechos contemporáneos**, no solo material de archivo. El tercero documenta el extremo opuesto, el arrastre inicial: una publicación de junio ingresada el 01/10 por estar aún visible en el listado.

Los casos cuarto a séptimo muestran detecciones correctas con puntuaciones bajas (una o dos coincidencias). El caso de `C-06` y el de `C-07` son particularmente relevantes para la hipótesis del trabajo: **ambos son incidentes locales descritos en español**, y el segundo coincide con el patrón de fraude laboral que motivó la elección del léxico bilingüe.

**Las siete detecciones de** `r/devsarg`**, clasificadas.** Para que la afirmación de 5.1 sea verificable, se publica la clasificación completa de las siete detecciones de la comunidad local. Son correctas tres: el ataque al sitio de una fundación local (`C-06`, 0,25), el falso reclutador que pide credenciales de LinkedIn (`C-07`, 0,25) y una publicación sobre el compromiso del sitio de un organismo nacional, que quedó fuera de la Tabla 5.14 por no aportar un caso distinto de los ya ilustrados. Son falsos positivos cuatro: la consulta sobre ingeniería inversa de videojuegos (`C-08`), la consulta sobre almacenamiento de datos personales (`C-09`), la reflexión sobre aprendizaje e inteligencia artificial (`C-10`) y una consulta sobre monetización de una aplicación para Android que menciona datos personales. Las cuatro activaron **un único término del diccionario** —en dos de los casos genérico del vocabulario de desarrollo— y pertenecen a conversaciones técnicas o administrativas, no a incidentes. En consecuencia, la tasa de falsos positivos de la comunidad local es de **4 de 7 detecciones (57,1 %)** y su aporte de detecciones correctas es de **3 publicaciones sobre 428 (0,70 %)**.

Los tres últimos casos de la tabla son falsos positivos con la puntuación mínima (0,25) y **comparten los tres un mismo rasgo**: provienen de `r/devsarg`, pertenecen a conversaciones técnicas o administrativas y activaron una única coincidencia léxica. No son errores aleatorios: son el resultado previsible de un clasificador por coincidencia de términos sobre una comunidad cuyo vocabulario técnico roza el de la seguridad informática sin tratar sobre ella. Este hallazgo es central para la discusión del Capítulo 6 y para la interpretación de la Tabla 5.1.

## 5.8. Síntesis de resultados y verificación de los umbrales comprometidos

La Tabla 5.15 concentra el estado de cada criterio comprometido en 1.6, con la evidencia que lo respalda.

**Tabla 5.15. Síntesis del cumplimiento de los criterios de éxito**

| Criterio | Umbral | Resultado | Estado |
|----|----|----|----|
| Precisión | ≥ 80 % | 84,7 % \[78,4; 89,8\] (n = 170, censo) | **CUMPLIDO** |
| Sensibilidad | ≥ 80 % | 61,2 % \[53,4; 69,5\] (muestra de 182, w = 3,044) | **NO CUMPLIDO** |
| F1-score | ≥ 0,80 | 0,711 \[0,635; 0,783\] | **NO CUMPLIDO** ᵃ |
| Latencia extremo a extremo | ≤ 5 minutos | P95 = 1.376,2 min; mediana 126,9 min (n = 437) | **NO CUMPLIDO** |
| Throughput | ≥ 1.000 posts/hora | Capacidad no medida. Demanda observada: 1,8 posts/hora (724 en 17 días); máximo de un día: 307 | **NO EVALUADO** |
| Cobertura | ≥ 80 % | — | **RETIRADO** (1.6) |

ᵃ El F1-score se incorporó en la V4, después del cierre de la ventana (1.6). Su valor queda por debajo del umbral como consecuencia aritmética de la sensibilidad, y así se informa: no se busca un umbral alternativo que lo acomode.

**Acuerdo entre anotadores.** El κ de Fleiss sobre los 50 casos comunes a los tres anotadores fue de **0,509** (0,570 al colapsar las categorías a la decisión binaria amenaza / no amenaza), por debajo del 0,61 comprometido en 3.3.2. Un acuerdo moderado implica que la etiqueta de referencia incorpora criterio personal: las métricas se informan con esa banda de incertidumbre y no como una verdad de referencia exenta de error (3.3.3). Dieciséis de los veinte casos discrepantes discuten si hay amenaza, no qué categoría asignarle.

**Complemento informativo.** La tasa de falsos descubrimientos es de **15,3 % (n = 170; IC 95 % \[10,2 %; 21,6 %\])** frente al valor de referencia de ≤ 20 %. No figura en la tabla como criterio porque es el complemento exacto de la precisión: contarla por separado duplicaría el mismo resultado (1.6).

**Sobre el throughput.** El criterio de 1.000 publicaciones por hora se declara **no evaluado**, no incumplido. La métrica confundía dos magnitudes distintas: **capacidad del artefacto** y **ritmo de la fuente**. La capacidad no se midió: no se ejecutó un banco de pruebas sobre esta instalación ni se caracterizaron los recursos del anfitrión (sección 6.3), de modo que no existe una medición que permita afirmar cuántas publicaciones por hora puede procesar el pipeline desplegado. Lo que sí se conoce es la **demanda observada**: 724 publicaciones en 17 días, un promedio de **42,6 por día, equivalente a 1,8 por hora**, con un máximo diario de 307. El techo de diseño —hasta 300 publicaciones por ciclo, 100 por comunidad, y hasta 1.200 por hora con ciclos de 15 minutos— es una **cota de diseño**, no una medición. Por lo tanto, el criterio no puede declararse cumplido ni incumplido: se declara **NO EVALUADO**, y se explicita qué medición haría falta para evaluarlo: una corrida controlada con lote conocido y recursos caracterizados.

**Sobre los objetivos específicos.** El detalle se presenta en la Tabla 7.2 (Capítulo 7); aquí se adelantan los tres resultados que dependen de las mediciones de este capítulo:

**OE1 (recolección automatizada)**: cumplido. El sistema recolectó 724 publicaciones en 16 días efectivos, con una interrupción de servicio documentada y sin pérdida de registros por duplicación.

**OE6 (alertas)**: **cumplimiento parcial**. El motor generó y registró una alerta sobre contenido verificable; la entrega externa por el canal de mensajería no se produjo porque está deshabilitada por configuración. No se declara cumplido, ni se declara no cumplido: el eslabón de generación y registro funciona y está evidenciado, y el eslabón de notificación no fue puesto a prueba.

**OE4 (categorización)**: cumplido en su dimensión funcional, no en la de rendimiento. El clasificador categorizó el 100 % del corpus en nueve categorías posibles, con 8 de ellas observadas, y su salida es auditable; pero **no alcanza los umbrales comprometidos**: la precisión se cumple (84,7 %), mientras que la sensibilidad (61,2 %) y el F1 (0,711) no, y el acuerdo entre anotadores (κ = 0,509) tampoco llega al 0,61 comprometido. El objetivo se declara cumplido con limitaciones y esas limitaciones se informan en 5.5 y 6.3.

# CAPÍTULO 6: DISCUSIÓN

## 6.1. Interpretación de los resultados

El primer hallazgo de este trabajo no es la detección de una amenaza concreta, sino una caracterización del terreno. Sobre 724 publicaciones recolectadas en tres comunidades, **el 76,52 % resultó no relevante** y el 1,64 % del contenido de la comunidad local fue clasificado como amenaza. El sistema no encontró un flujo constante de incidentes: encontró un volumen mayoritario de conversación técnica y consultas, con apariciones esporádicas de amenazas concretas y **ningún día que el recálculo retrospectivo sostenga como anómalo** (5.4.1).

Ese resultado es coherente con la naturaleza de las fuentes y con el antecedente local disponible. Las comunidades seleccionadas discuten ciberseguridad y desarrollo; eso no las convierte en un registro de incidentes. La consecuencia práctica es que **el valor de un sistema de este tipo no está en la exhaustividad, sino en la capacidad de marcar los pocos casos y las pocas jornadas que merecen atención**. La arquitectura implementada responde a esa lógica: el clasificador filtra el volumen y el motor de anomalías señala las jornadas inusuales. El aviso del 13/10 muestra que la cadena de generación, registro y notificación funciona de punta a punta, pero **no que distinga una jornada inusual**: el recálculo de 5.4.1 muestra que la línea base cayó de 4,9 a 0,8 porque la ventana móvil perdió el 01/10, no porque la actividad del 12/10 fuera excepcional. La distinción entre «el mecanismo funciona» y «el mecanismo acierta» atraviesa este capítulo.

El segundo hallazgo es que **el clasificador es preciso cuando marca y conservador cuando descarta**. La precisión censada sobre las 170 predicciones positivas es alta (84,7 %, IC 95 % \[78,4 %; 89,8 %\]), pero la sensibilidad ponderada es de 61,2 %: sobre el corpus hay **235 amenazas estimadas (32,5 %)** y el sistema detecta 170, de modo que omite alrededor de un tercio. El error no es simétrico —no inventa amenazas con frecuencia, pero deja pasar una proporción relevante de las que existen— y la omisión se concentra en las comunidades en inglés (`r/Malware` 72,2 % y `r/netsec` 51,7 %), no en la local. La lectura operativa cambia respecto de la V4: **lo que el sistema marca es confiable; lo que no marca no está libre de amenaza**, y el analista debe tratar el silencio como una zona de incertidumbre y no como una ausencia verificada.

El tercer hallazgo es de ingeniería y tiene relación directa con la comparabilidad de los resultados: **los dos defectos más serios del sistema no fueron de diseño conceptual, sino de implementación silenciosa**. El error en la recurrencia de la distribución de Poisson dejaba inalcanzable el umbral de toda categoría con línea base superior a 1,05: el motor estaba funcionando, registraba evaluaciones y no podía detectar nada en las categorías más activas. El segundo defecto, la ausencia de un centinela en el lazo de control, hacía que una comunidad perdiera sistemáticamente sus publicaciones ante un bloqueo de la fuente, sin error visible. Ambos fueron detectados por verificación cruzada entre artefactos (el workflow evaluado contra el workflow desplegado, y el conteo de la base contra el registro del motor) y no por inspección del código. La lección metodológica es que **en un pipeline automatizado, la ausencia de resultados no es evidencia de ausencia de hechos**: un sistema que informa cero puede estar operando, o puede estar midiendo su propio defecto.

## 6.2. Discusión frente al estado del arte y al antecedente local

Frente a las herramientas OSINT profesionales relevadas en 2.2, el resultado de este trabajo no es competitivo en volumen ni en diversidad de fuentes, y no pretende serlo: la escala es de cientos de publicaciones y una única plataforma, frente a soluciones que integran decenas de fuentes técnicas. La comparación pertinente es de otra naturaleza. Frente a SpiderFoot o Maltego CE, este artefacto aporta tres cosas que esas herramientas no ofrecen de forma directa: **léxico bilingüe con foco en el español rioplatense**, **monitoreo temporal continuo con detección de anomalías sobre la serie diaria** y **un diccionario auditable**, con la lista completa de términos en el Anexo C, que permite reconstruir por qué una publicación fue clasificada de una manera y no de otra. El primer aporte **se ilustra con los casos documentados**, y esa distinción importa: los casos `C-06` y `C-07` son incidentes locales descritos en español que un diccionario exclusivamente en inglés no habría detectado, pero tres detecciones correctas sobre siete ilustran un mecanismo, no lo verifican como propiedad del sistema sobre el corpus. La validación V5 sí incluye la comunidad local: de sus 7 detecciones, 3 son correctas (`C-06`, `C-07` y el tercer caso documentado en 5.7), de modo que el léxico local **produce detecciones verificadas**; pero con 7 detecciones y 4 falsos positivos la base es demasiado pequeña para estimar un rendimiento por lengua, y así se declara. La afirmación que este trabajo sostiene es la más débil y la más honesta: el léxico bilingüe **incorpora** vocabulario local que las herramientas en inglés no tienen, y ese vocabulario produjo al menos dos detecciones correctas sobre la única comunidad argentina del corpus.

Frente al antecedente de Dengra y Rivas (2026), el contraste introducido en 2.2 puede ahora cuantificarse en la Tabla 6.1.

**Tabla 6.1. Contraste con el antecedente local (Dengra y Rivas, 2026)**

| Dimensión | Dengra y Rivas (2026) | Este trabajo |
|----|----|----|
| Plataforma | Bluesky (AT Protocol), con autenticación | Reddit, fuentes RSS/Atom públicas |
| Escala | 3.908 publicaciones, 847 fechas | 724 publicaciones, 16 fechas con datos |
| Ventana de evaluación | Amplia, multi-país | 17 días, corte declarado, 15 días evaluados por el motor |
| Alcance geográfico | América Latina y el Caribe (5 países) | Una comunidad local y dos internacionales |
| Validación | Muestra de 80, dos anotadores, kappa de Cohen | 352 casos (censo de 170 positivos y muestra de 182 negativos), tres anotadores, kappa de Fleiss |
| Fiabilidad reportada | κ = 0,356 (relevancia) y κ = 0,758 (país) | κ = 0,509; por debajo del 0,61 comprometido |
| Clasificación temática | No categoriza: recupera y valida relevancia | 9 categorías, 201 términos |
| Detección temporal | No reportada | Motor con ventana móvil, 112 evaluaciones y 6 disparos; eficacia no demostrada en el recálculo (5.4.1) |
| Seudonimización | Recomendada como buena práctica | Aplicada en la ingesta, con rotación de clave documentada |

La lectura honesta de esta tabla es mixta. El antecedente supera a este trabajo en escala, en alcance geográfico y **en fiabilidad medida**, aunque la brecha es menor que en la V4: este trabajo ahora reporta acuerdo entre tres anotadores (κ = 0,509), pero el valor queda por debajo del umbral que fijó para sí mismo (0,61) y de los 0,758 que el antecedente alcanza en una de sus dos dimensiones. No se compensa con una cifra ajustada ni se elige una variante del coeficiente que suba el valor: se informa el obtenido y su consecuencia, que es una etiqueta de referencia con una cuota no despreciable de criterio personal (3.3.3). En la dirección opuesta, este trabajo incorpora dos elementos que el antecedente no reporta: una **taxonomía temática** con diccionario auditable, y un **componente de detección temporal** que convierte la serie diaria en avisos. Que el mismo director haya conducido ambos trabajos refuerza la utilidad de la comparación: son dos soluciones al mismo problema, con decisiones distintas en cada eslabón, y sus diferencias permiten aislar qué aporta cada decisión.

Un dato del antecedente merece mención específica porque **es evidencia externa y contemporánea de la principal limitación de este trabajo**. Dengra y Rivas documentan un caso en el que la palabra clave `CERT` resultó ruidosa en aproximadamente el 83 % de los casos por colisión con la raíz «cert-» en portugués y catalán, y optaron por retirarla. Es exactamente el fenómeno que en este trabajo produjo los falsos positivos de la Tabla 5.14: coincidencia léxica sin desambiguación de contexto, sobre comunidades cuyo vocabulario roza el dominio sin tratar sobre él. Dos trabajos independientes, con plataformas distintas y métodos distintos, llegaron al mismo límite del enfoque por términos. Eso convierte la limitación en una propiedad del método y no en una deficiencia particular de esta implementación.

## 6.3. Limitaciones

Las limitaciones se agrupan según su origen, porque no todas se corrigen de la misma manera.

**Limitaciones de la fuente.**

**Profundidad temporal acotada.** El listado de novedades devuelve hasta 100 elementos recientes por comunidad. El corpus queda sesgado hacia lo reciente y el arrastre inicial de 287 publicaciones crea la ilusión de un volumen histórico que el sistema no puede sostener día a día. La latencia bruta del corpus completo (media de 11,4 días) es un artefacto de esa primera consulta.

**Sin comentarios.** La tabla `comments` está vacía porque las fuentes RSS/Atom no exponen el árbol de comentarios. El sistema registra la cantidad declarada de comentarios por publicación, pero no analiza su texto. Toda conclusión de este informe se limita al contenido de las publicaciones.

**Acceso condicionado por política.** El endpoint JSON de la plataforma respondió 403 y la vía elegida quedó sujeta a límites de tasa cuyo umbral exacto no se determinó (se documentó como `no determinado`). La interrupción de 44 horas se declara como ausencia de datos.

**Limitaciones del método de clasificación.**

**Coincidencia léxica sin lematización ni desambiguación.** El clasificador no aplica lematización ni análisis de contexto. Una variante morfológica ausente del diccionario no se reconoce, y un término técnico puede activar una categoría en una conversación que no trata sobre amenazas. **130 de las 170 publicaciones clasificadas (76,47 %) lo fueron con una sola coincidencia léxica**, que es el terreno donde se concentran los falsos positivos observados. La auditoría de 4.4.1 cuantifica dos consecuencias: **once publicaciones (6,5 %) dependen exclusivamente de un término genérico** del dominio de desarrollo, y el diccionario no reconoce compuestos escritos con guion, lo que afecta a cinco publicaciones sin alterar el conjunto clasificado. Ninguna de las dos se corrigió en la corrida para no desplazar el marco muestral; ambas quedan como recomendación.

**Vacío de vocabulario declarado.** El diccionario no cubre términos técnicos frecuentes en las comunidades en inglés (`edr`, `red team`, nombres de familias y siglas de herramientas). Dos falsos negativos de la muestra previa lo anticiparon y la validación V5 lo confirma: 30 omisiones en 182 casos sorteados del estrato negativo, equivalentes a una sensibilidad de 61,2 %. No se corrigió por decisión metodológica, para no incorporar términos sin respaldo técnico ni desplazar el marco muestral. La categoría «Ingeniería Social» no registró ninguna coincidencia en toda la ventana.

**Fronteras de la taxonomía.** Cuatro desacuerdos de categoría en la muestra se atribuyeron a una ambigüedad real entre «Infraestructura y Ataques» y «Malware» o «Vulnerabilidades»: el límite entre la herramienta de ataque y la infraestructura sobre la que se ejecuta no tiene una respuesta única.

**Limitaciones de la validación.**

**Acuerdo moderado y anotadores internos.** El etiquetado lo hicieron tres anotadores del equipo del proyecto con la misma guía, no evaluadores externos e independientes. El κ de Fleiss sobre los 50 casos comunes fue de **0,509**, por debajo del 0,61 comprometido en 3.3.2; 16 de los 20 desacuerdos son sobre la presencia de amenaza y no sobre la categoría. La etiqueta de referencia incorpora, por lo tanto, una cuota de criterio personal, y las métricas de 5.5 deben leerse con esa banda. Es la limitación más importante del capítulo y no se compensa con el tamaño de la muestra: un acuerdo moderado no mejora por etiquetar más casos con el mismo protocolo.

**Muestra condicionada por la predicción.** El estrato positivo está censado y el negativo muestreado (182 de 554), de modo que la precisión se estima mejor que la sensibilidad: el peso corrige el sesgo del estimador, no la incertidumbre del sorteo (IC de la omisión \[11,4 %; 22,7 %\]). La muestra pertenece al corpus analizado —a diferencia de la V4—, pero no es una muestra aleatoria simple del total.

**Reproducibilidad del sorteo.** El sorteo de la V5 se generó con `sorteo_v5.py`, semilla 20261020 y `md5` determinista, y se archivó con la correspondencia entre código interno, `id`, puntuación y estrato; la muestra es reconstruible. La limitación de la V4 —8 de 50 filas reproducidas, por un `ORDER BY` que nunca se ejecutó— quedó cerrada por ese script y se informa como antecedente, no como estado vigente.

**Sin evaluación externa ni revisión por pares.** No hubo validación por un tercero ajeno al equipo: los tres anotadores y la dirección del trabajo pertenecen al mismo proyecto.

**Limitaciones de la operación.**

**Latencia incumplida y throughput no evaluado.** La latencia tiene dos causas descritas en 5.3: el umbral de 5 minutos era incompatible con un ciclo de 15 minutos sobre tres comunidades en serie, y el motor operó solo el 19,0 % del período (jornadas diurnas), de modo que el 71,2 % de las publicaciones se creó con el motor detenido. El throughput no se declara incumplido sino **no evaluado**: su enunciado confundía capacidad de artefacto con ritmo de fuente y no se midió la capacidad (5.8).

**Notificación externa no probada.** Las 6 alertas quedaron en estado `PENDIENTE`: el envío por Telegram está deshabilitado. El objetivo OE6 se declara parcial y no se presenta como cumplido.

**Interrupción de servicio de 44 horas** sin detección automática. La interrupción se debió al **apagado del equipo** el 03/10 (instancia inaccesible, sin ciclos), y su fin fue una **reanudación manual** del operador el 04/10, no una recuperación automática (sección 5.1). El sistema no distingue entre «no hay publicaciones nuevas» y «no estoy funcionando», ni se reanuda por sí solo, lo que motiva la propuesta de un centinela de latidos en el trabajo futuro.

**Medición de rendimiento sobre recursos compartidos.** Las cifras de latencia provienen de una instalación de un solo nodo, en dos contenedores sin aislamiento de CPU ni de memoria y sin hardware dedicado (sección 4.3). No se caracterizaron los recursos del equipo anfitrión, de modo que los valores informados describen el comportamiento observado y no un techo de capacidad: no permiten afirmar cuánto del incumplimiento de latencia se debe al artefacto y cuánto al entorno. Por la misma razón, la capacidad de proceso —y con ella el throughput— se declara **no evaluada**.

## 6.4. Implicaciones y trabajo futuro

**Implicaciones para el usuario del sistema.** El resultado principal es que el artefacto es utilizable en su función de **filtrado y vigilancia**, no en la de **cobertura exhaustiva**. Un analista que consuma sus salidas debe interpretar cada aviso como una señal a verificar, no como un hecho confirmado. Para el caso local, la conclusión operativa es que `r/devsarg` aporta señal muy baja (1,64 % de detecciones, con falsos positivos conocidos) y que las comunidades de seguridad en inglés concentran la utilidad, con la salvedad de que su contenido no es local.

**Implicaciones metodológicas.** Tres de los hallazgos de este trabajo son transferibles a cualquier pipeline OSINT automatizado: (a) la verificación debe comparar el artefacto desplegado con el artefacto documentado, porque los defectos que más afectan los resultados son silenciosos; (b) la latencia y el throughput deben formularse distinguiendo capacidad de artefacto y ritmo de fuente; (c) un etiquetado con anotadores del mismo equipo puede sostener métricas puntuales, pero mientras el acuerdo no supere el umbral declarado **la referencia no es un patrón oro**, y declararlo vale más que maquillarlo.

**Trabajo futuro.** Las seis líneas de trabajo que se desprenden de estos hallazgos —repetir la validación con anotadores externos y una guía más fina, incorporar desambiguación por contexto, instrumentar un centinela de latidos, probar la entrega de alertas, registrar la retroalimentación operativa y reformular los criterios temporales— se desarrollan con su criterio de verificación en el Capítulo 8, junto con la línea de trabajo del proyecto. Se enuncian aquí en orden de prioridad: la fiabilidad del etiquetado es el primer límite que conviene cerrar. La V5 ya resolvió el tamaño de la muestra —182 casos sorteados, con un intervalo de omisión de \[11,4 %; 22,7 %\]—, de modo que lo que resta no es ampliar el `n` sino elevar el acuerdo: con κ = 0,509, el límite está en la definición operativa de amenaza y no en la cantidad de casos etiquetados.

# CAPÍTULO 7: CONCLUSIONES

## 7.1. Trazabilidad de los criterios y de los objetivos específicos

La Tabla 7.1 vincula cada criterio comprometido en 1.6 con su resultado verificado y con la tabla donde consta; la Tabla 7.2 hace lo propio con los ocho objetivos específicos.

**Tabla 7.1. Trazabilidad de los criterios de éxito**

| Criterio de 1.6 | Umbral | Resultado verificado | Evidencia | Estado |
|----|----|----|----|----|
| Precisión | ≥ 80 % | 84,7 % \[78,4; 89,8\] (n = 170, censo) | Tabla 5.8 | **Cumplido** |
| Sensibilidad | ≥ 80 % | 61,2 % \[53,4; 69,5\] (n = 182 muestra, w = 3,044) ᵃ | Tabla 5.8 | **No cumplido** |
| F1-score | ≥ 0,80 | 0,711 \[0,635; 0,783\] ᵇ | Tabla 5.8 | **No cumplido** |
| Latencia extremo a extremo | ≤ 5 min | P95 = 1.376,2 min; mediana 126,9 min (n = 437) | Tabla 5.4 | **No cumplido** |
| Throughput | ≥ 1.000 posts/h | Capacidad no medida; demanda observada de 1,8 posts/h | Sección 5.8 | **No evaluado** |
| Cobertura | ≥ 80 % | — | Sección 1.6 | **Retirado** |

ᵃ Estimación ponderada por el muestreo del estrato negativo (w = 3,044); el intervalo se deriva de la proporción de omisión observada en los 182 casos sorteados (3.3.5).

ᵇ Métrica incorporada en la V4, con posterioridad al cierre de la ventana (1.6). *Complemento informativo no contabilizado como criterio:* tasa de falsos descubrimientos de **15,3 % (n = 170)** frente al valor de referencia de ≤ 20 %, por ser `1 − precisión`.

**Tabla 7.2. Trazabilidad de los objetivos específicos**

| Objetivo específico | Evidencia principal | Estado |
|----|----|----|
| OE1. Recolección automatizada con gestión explícita de restricciones de tasa | 724 publicaciones en 17 jornadas de operación parcial (19,0 % del período); `CARACTERIZACION_RATE_LIMIT.md`; interrupción de 44 h declarada con causa (apagado del equipo el 03/10) | **Cumplido con reparos** |
| OE2. Flujos robustos en n8n con idempotencia y recuperación ante fallos parciales | 17 nodos desplegados; `ON CONFLICT DO UPDATE` verificado en ingesta y `UNIQUE (categoria, ventana_inicio)` en análisis; centinela del lazo corregido (incidente `IN-08`: un 429 de la fuente abortaba el ciclo y la corrida quedaba registrada como exitosa); recuperación tras la caída del 03/10 (apagado del equipo) **manual, no automática** | **Cumplido con reparos** |
| OE3. Modelo relacional en PostgreSQL con integridad referencial e índices analíticos | 5 tablas, 5 índices, `RESTRICT`/`CASCADE` justificados; Anexo A; Tabla 4.2 | **Cumplido** |
| OE4. Componente de NLP en español con categorización y extracción de entidades, y descripción de sus límites | 9 categorías, 201 términos, 170 publicaciones clasificadas; extracción de entidades con resultados en §5.6 (286/724 publicaciones, 400 valores); Anexo C; límites en 6.3 | **Cumplido con limitaciones** |
| OE5. Motor de reglas estadísticas para detección de anomalías | 112 evaluaciones, 6 disparos; recálculo retrospectivo: 0,95 disparos esperados y 0 sostenidos (5.4.1); Tablas 5.5, 5.6 y 5.4.1 | **Implementado; eficacia no demostrada** |
| OE6. Sistema de alertas con estado operativo explícito | 6 alertas registradas, todas `PENDIENTE`; envío externo deshabilitado | **Parcial** |
| OE7. Evaluación cuantitativa contra los umbrales declarados en 1.6, con su momento de fijación | Tablas 5.4 y 5.8; Tabla 1.1 con la fecha de cada umbral; sin modificaciones posteriores a la V4 | **Cumplido** |
| OE8. Análisis legal y seudonimización conforme a la Ley 25.326 | HMAC-SHA-256 con clave por variable de entorno; rotación documentada; riesgo residual declarado (3.4) | **Cumplido** |

## 7.2. Conclusiones por objetivo y aportes del trabajo

**Sobre la recolección (OE1, OE2).** El sistema recolecta, normaliza y persiste de forma autónoma y sostenida. La idempotencia se verificó por ejecución repetida, y el corpus no contiene duplicados; la misma propiedad se extiende al análisis mediante la restricción `UNIQUE (categoria, ventana_inicio)` de la tabla `anomalias` (§4.5). El incidente más relevante de este objetivo no fue una falla de recolección sino una falla de silencio: la pérdida sistemática de publicaciones de la tercera comunidad del ciclo ante un bloqueo de la fuente, que se corrigió con un centinela y con una espera explícita entre solicitudes. La conclusión transferible es que **un pipeline que informa cero elementos debe distinguir «no hay novedades» de «no pude consultar»**, y que esa distinción debe ser parte del diseño y no del diagnóstico posterior.

**Sobre la persistencia (OE3).** El modelo de cinco tablas sostiene las consultas analíticas de este informe sin degradación observable, con índices orientados a las series temporales, a los conteos por categoría y al cálculo de latencia. Las dos decisiones estructurales que se corrigieron respecto de la versión previa —el borrado lógico de comunidades mediante `active_monitoring` y la eliminación de índices de texto completo que no se utilizaban— resultaron consistentes con el uso real del sistema.

**Sobre la clasificación (OE4).** El aporte central del trabajo es un clasificador por diccionario **bilingüe, auditable y con límites declarados**: 201 términos distribuidos en 9 categorías, con **precisión de 84,7 % y sensibilidad de 61,2 %** sobre el corpus (Tabla 5.8), y con una limitación medida y declarada —el 76,47 % de las clasificaciones se sostiene en una única coincidencia léxica—. El criterio de precisión se cumple y el de sensibilidad no; el F1, derivado, tampoco. Ese resultado es menos favorable que el que informaba la V4 y se presenta tal como se obtuvo: la corrección del estimador de sensibilidad, no un cambio del clasificador, es lo que explica la diferencia. El dato de las coincidencias únicas es, paradójicamente, el más útil del capítulo de resultados: indica exactamente dónde está el error y cuánto costaría reducirlo. La categoría «Ingeniería Social» no registró coincidencias en la ventana, y ese vacío se informa en lugar de omitirse.

**Sobre la detección de anomalías (OE5).** El motor está implementado, es determinista y auditable: registra sus decisiones negativas, eleva el umbral en las categorías frecuentes y su tabla permite reconstruir cada decisión. La **eficacia, en cambio, no está demostrada**, y el recálculo retrospectivo de 5.4.1 lo muestra con precisión: sobre la serie correcta —`created_utc`, sin la carga inicial y sin los días sin operación en la línea base— el motor no habría emitido ningún aviso en quince días, frente a 0,95 disparos esperados por azar. El único disparo de producción se explica por la caída de la línea base de 4,9 a 0,8 el día en que la ventana móvil perdió el 01/10. El defecto más grave del sistema se encontró igualmente en este componente y su naturaleza es la lección más importante del trabajo: **un error en la recurrencia de la distribución de probabilidad dejaba inalcanzable el umbral de toda categoría activa**. El motor seguía registrando evaluaciones, los conteos seguían siendo correctos y la única evidencia del problema era la ausencia de disparos. Ningún tablero lo habría mostrado; apareció al cotejar el comportamiento esperado con el observado. OE5 se declara **implementado; eficacia no demostrada**.

**Sobre las alertas (OE6).** El eslabón de detección y registro está verificado; el de notificación, no. Las seis alertas quedaron en estado pendiente porque el envío está deshabilitado por configuración. Se declara parcial y se sostiene esa calificación: **no se afirma que el sistema alerta, se afirma que detecta y registra**.

**Sobre la evaluación (OE7) y el cumplimiento legal (OE8).** La evaluación se realizó contra los umbrales de la Tabla 1.1, cuyo momento de fijación se declara criterio por criterio: los de precisión, sensibilidad, latencia, throughput y cobertura son del diseño; el F1-score y la reformulación de los umbrales de clasificación se incorporaron en la V4 y así se informan (1.6). De los seis criterios listados, **solo uno de los tres de clasificación se alcanza** (precisión), **dos no se cumplen** (sensibilidad y F1), **uno no se cumple** en el plano temporal (latencia), **uno queda sin evaluar** por falta de medición de capacidad (throughput) y **uno se retira** con fundamento (cobertura). A ello se suma que el acuerdo entre anotadores (κ = 0,509) queda por debajo del 0,61 comprometido, de modo que la referencia con la que se midieron esos criterios tiene una fiabilidad limitada y así se declara. La tasa de falsos descubrimientos no se cuenta como criterio: es el complemento exacto de la precisión y se informa como tal. La seudonimización con HMAC-SHA-256 y clave por despliegue, con rotación documentada, cumple el objetivo y, además, dejó visible su límite: seudonimizar no es anonimizar, y el contenido textual puede permitir reidentificación indirecta.

## 7.3. Respuesta a las preguntas de investigación

**PI-1. ¿Puede un sistema de código abierto ofrecer una arquitectura viable y de bajo costo frente a soluciones propietarias?** Sí, con un alcance acotado. n8n y PostgreSQL, sobre un único servidor en contenedores, recolectaron 724 publicaciones en 17 jornadas sin licencias ni servicios pagos, aunque con una operación intermitente que cubrió el 19,0 % del período y que se declara como límite en 5.3 y 6.3. La viabilidad técnica queda demostrada en la dimensión de infraestructura. En la dimensión de rendimiento, la respuesta es matizada: la latencia no se cumplió por causas de operación y el throughput quedó **sin evaluar** porque no se midió la capacidad del artefacto. Ninguno de los dos resultados permite atribuir el límite a una deficiencia demostrada del sistema. En la dimensión de acceso, la restricción determinante tampoco fue económica sino de política de plataforma (PI-3).

**PI-2. ¿Qué patrones temporales y temáticos presentan los incidentes discutidos en comunidades técnicas de Reddit durante el período relevado, y en qué medida el léxico rioplatense aporta detecciones que un léxico solo en inglés no captaría?** El patrón dominante es la **ausencia de un flujo constante**: el 76,52 % del corpus no es material de amenaza, y las detecciones se concentran en casos aislados. Sobre la comunidad local relevada, la evidencia permite tres afirmaciones acotadas: (a) el contenido de temática ciberseguridad es marginal dentro de su propio volumen; (b) los casos locales detectados corresponden a un ataque a un sitio institucional y a un intento de fraude laboral en español, ambos verificados como publicaciones reales y contemporáneas; y (c) el **57,1 % de las detecciones de esa comunidad (4 de 7) correspondió a falsos positivos** —conversaciones técnicas o administrativas que activaron un único término genérico—, mientras que las tres restantes describen incidentes locales reales. El patrón temporal, en cambio, **no sostiene una jornada anómala**: el aviso del 13/10 se explica por la discontinuidad de la línea base y no por una concentración excepcional de divulgaciones, y el recálculo sobre la fecha de creación no habría emitido ningún aviso en quince días (5.4.1). La respuesta a esta pregunta es deliberadamente acotada: el aporte del léxico rioplatense se limita a dos detecciones locales verificadas, insuficientes para sostener una ventaja cuantitativa, y el corpus —tres comunidades técnicas de Reddit— no permite caracterizar el ecosistema argentino en su conjunto.

**PI-3. ¿Cómo afectan las restricciones de acceso programático a la cobertura y a la profundidad temporal de un pipeline automatizado?** De manera determinante, y con cuatro efectos medidos: (a) el endpoint JSON de la plataforma quedó inaccesible por política (respuesta 403), lo que forzó la vía de sindicación; (b) esa vía limita cada consulta a los elementos más recientes del listado y **no expone comentarios**, lo que dejó la tabla correspondiente sin poblar y hace que el arrastre inicial de 287 publicaciones antiguas sea un artefacto de la primera consulta, no una capacidad real de profundidad histórica; (c) los límites de tasa impusieron una espera deliberada entre solicitudes y su umbral exacto quedó **no determinado** por decisión metodológica, para no generar más bloqueos al intentar medirlo; y (d) el efecto residual de esos límites es un sesgo por comunidad: una comunidad puede quedar sin datos en un ciclo y el corpus no lo refleja, como se documentó con una corrida incompleta en el 53,6 % de los ciclos medidos. La conclusión es que **en OSINT la restricción de acceso es una variable de diseño de primer orden**, y que un sistema de este tipo debe declarar su cobertura como contingente en lugar de suponerla.

**PI-4. ¿De qué manera puede protegerse la privacidad de los usuarios en un sistema de monitoreo público persistente, conforme a la normativa argentina?** Mediante cuatro medidas implementadas y verificables: (a) seudonimización en el momento de la ingesta con HMAC-SHA-256 y clave por despliegue, de modo que el identificador original nunca se persiste; (b) gestión de la clave fuera del artefacto versionado, con rotación documentada que impide la vinculación de un mismo autor entre períodos; (c) minimización: solo publicaciones públicas, sin comentarios, sin perfiles, sin datos de contacto, y sin perfilado de personas; y (d) declaración explícita del riesgo residual, porque la seudonimización no impide la reidentificación indirecta a partir del contenido. La respuesta honesta incluye su límite: **la única forma de eliminar ese riesgo residual sería no recolectar contenido textual**, y eso suprimiría el objeto del sistema.

## 7.4. Conclusión general

El supuesto de trabajo planteado en 1.6 sostenía que un sistema OSINT de código abierto basado en n8n y PostgreSQL, con clasificación heurística especializada en español, podía automatizar la detección de incidentes con precisión y sensibilidad operativamente útiles. La evidencia reunida respalda ese supuesto **solo parcialmente en la dimensión de clasificación** —la precisión supera el umbral, pero la sensibilidad y el F1 no, y el acuerdo entre anotadores tampoco— y lo acota en las demás:

**La detección funciona, la cobertura no se puede afirmar.** No hay base empírica para sostener que el sistema ve todo lo relevante, y ese criterio se retiró en lugar de maquillarse.

**El ritmo de la fuente manda sobre la capacidad del artefacto.** La latencia incumplida y el throughput no evaluado muestran que los umbrales se formularon sin distinguir lo que el artefacto puede procesar de lo que la fuente produce.

**La validación acota la fuerza de las métricas, aunque ya no por tamaño.** El diseño corrigió el estimador y la muestra —352 casos, tres anotadores, sensibilidad ponderada—, pero el acuerdo entre anotadores (κ = 0,509) no alcanza el umbral comprometido y la muestra sigue condicionada por la predicción del propio sistema. Ambas condiciones se declaran y no se compensan.

El aporte concreto de este trabajo es un artefacto funcional y auditable, un diccionario bilingüe con doscientos un términos verificables, un motor de anomalías con umbral estadístico explícito y un cuerpo documental que permite reconstruir cada cifra. Su principal valor metodológico no está en las cifras que alcanza, sino en el conjunto de defectos que detectó, documentó y no ocultó: un lazo de control que perdía publicaciones en silencio, una distribución de probabilidad mal implementada que impedía toda detección en las categorías activas, una carga inicial que el motor reportó como anomalía, una interrupción de servicio de cuarenta y cuatro horas y una validación cuyo acuerdo entre anotadores no alcanza el umbral que el propio trabajo fijó. **Un sistema de monitoreo que no documenta sus propios límites produce una falsa sensación de cobertura**, y ese es el resultado que este trabajo busca dejar en claro.

# CAPÍTULO 8: RECOMENDACIONES Y TRABAJOS FUTUROS

Las recomendaciones se ordenan según quién debe ejecutarlas, y cada una se acompaña de su criterio de verificación, para que puedan comprobarse en lugar de quedar como declaraciones de intención.

## 8.1. Recomendaciones para el sistema en producción

Las recomendaciones se presentan priorizadas por **impacto sobre la validez de los resultados y el uso operativo del sistema**, y en orden decreciente de relación entre ese impacto y el esfuerzo de implementación. Las tres primeras —probar la entrega, instrumentar el centinela y recalcular el motor sobre la fecha de creación— son de **bajo esfuerzo y alto impacto**: se resuelven con configuración, con registro y con una consulta, y atacan los tres defectos que este informe no pudo cerrar por observación (entrega no probada, silencio no detectado y una serie de anomalías que mide la operación del sistema). Las tres siguientes —retroalimentación de alertas, revisión del peso de `r/devsarg` y revisión del diccionario— son de **esfuerzo medio** y afectan la calibración del motor y del clasificador. La última es de **bajo impacto inmediato y alto esfuerzo potencial**, porque toca datos ya cargados, y por eso se ubica al final. La Tabla 8.1 las enumera con su criterio de verificación.

**Tabla 8.1. Recomendaciones para el sistema en producción y criterios de verificación**

| \# | Recomendación | Criterio de verificación |
|----|----|----|
| 1 | **Habilitar y probar la entrega de alertas** por el canal de mensajería en un entorno controlado, con un destinatario de prueba y un disparo provocado | La tabla `alertas` registra estado de entrega efectiva y el mensaje llega al destinatario |
| 2 | **Incorporar un centinela de latidos**: registrar cada ciclo ejecutado, con marca de tiempo y resultado, y avisar cuando transcurran más de N ciclos sin actividad registrada | Los huecos operativos dejan de detectarse por inspección retrospectiva y quedan asentados en la base |
| 3 | **Recalcular el motor sobre** `created_utc` y excluir de la línea base la carga inicial y los días sin operación, dividiendo por los días efectivamente operados; fijar la ventana en días operados y no en días calendario | La serie deja de reflejar la operación del sistema; desaparecen los 5 disparos espurios del 02/10 y el del 13/10 (5.4.1) |
| 4 | **Registrar el resultado del ciclo de retroalimentación de las alertas** (útil / falso positivo / pendiente) | El umbral del motor puede calibrarse con evidencia operativa y no solo con la distribución histórica |
| 5 | **Revisar el peso de** `r/devsarg` en la estrategia de monitoreo: conservarla como control negativo con frecuencia reducida, no como fuente principal de detecciones | Documento de decisión con la proporción de detecciones y falsos positivos de la comunidad |
| 6 | **Revisar el diccionario del clasificador**: reemplazar los términos genéricos del dominio de desarrollo por variantes específicas y normalizar los guiones a espacio en el texto previo a la coincidencia (4.4.1) | Ninguna publicación clasificada depende exclusivamente de un término genérico; el corpus se reclasifica con el marco muestral recalculado y el porcentaje de detecciones de `r/devsarg` se informa junto al nuevo censo |
| 7 | **Depurar las filas heredadas** con clasificaciones de versiones anteriores del clasificador, para que la puntuación almacenada sea homogénea | Consulta de verificación: ninguna fila con valores fuera de la escala vigente (hoy, en la ventana B5, ya se cumple) |

## 8.2. Recomendaciones metodológicas

**Repetir la validación con anotadores externos y una definición operativa de amenaza más fina.** La V5 ya resolvió el tamaño de la muestra —182 casos sorteados, con un intervalo de omisión de \[11,4 %; 22,7 %\]— y el cálculo de acuerdo entre tres anotadores; el límite que persiste es el **κ de 0,509**, por debajo del 0,61 comprometido y atribuido a la frontera de la definición de amenaza. Es la acción de mayor impacto sobre la validez de los resultados: sin acuerdo suficiente, las métricas describen una referencia con criterio personal y no un patrón oro.

**Fijar el orden del sorteo antes de extraer la muestra** (`ORDER BY` estable en la consulta), y archivar el conjunto con semilla y hash del archivo de origen, para que la muestra sea reconstruible. La V5 lo cumple con `sorteo_v5.py` y semilla 20261020; la recomendación es conservar la práctica en cada revalidación.

**Formular los criterios de latencia y throughput distinguiendo capacidad del artefacto y ritmo de la fuente**, con umbrales derivados de la cadencia elegida. Un umbral de cinco minutos es incompatible con un ciclo de quince minutos, y un umbral de mil publicaciones por hora no es alcanzable desde fuentes que producen decenas de publicaciones por día.

**Fijar la convención de fechas** (creación frente a ingesta) antes de calcular cualquier métrica temporal, y reportar ambas: la latencia bruta del corpus completo y la del subconjunto creado dentro de la ventana introducen conclusiones opuestas sobre el mismo sistema.

**Validar técnicamente el vocabulario del diccionario** antes de incorporar términos nuevos, en lugar de agregarlos por analogía léxica: los dos falsos negativos conocidos (*EDR evasion*, *red team*) quedaron sin corregir precisamente por esta razón.

## 8.3. Línea de trabajo dentro del proyecto

Los resultados de este informe fijan las condiciones de las etapas siguientes del proyecto:

**La latencia es un prerrequisito.** Cualquier etapa que dependa de la oportunidad del dato debe resolverse antes de ampliar el alcance: el P95 operativo de 22,9 horas es incompatible con un uso que requiera reacción temprana.

**La profundidad histórica no se resuelve con más ciclos.** El listado de novedades no puede recuperar el pasado; para análisis retrospectivos hace falta una estrategia de acumulación diaria sostenida o una fuente alternativa de archivo, con la salvedad de que buena parte de las fuentes históricas de esta plataforma fue discontinuada.

**Los comentarios quedan fuera del alcance** mientras la vía de acceso no los exponga. Cualquier objetivo que requiera analizar la conversación y no solo la publicación exige revisar la fuente.

**La recolección posterior al corte constituye un track separado** y sus 31 publicaciones iniciales no se mezclan con el corpus analizado, para preservar la reproducibilidad de las cifras de este informe.

## 8.4. Recomendaciones para terceros

Para organizaciones que evalúen implementar un sistema semejante, la experiencia de este trabajo sugiere cuatro precauciones: no comprometer un criterio de cobertura sin un diseño de captura-recaptura que lo sustente; instrumentar los silencios del pipeline antes que sus resultados; separar en la evaluación el desempeño del clasificador de la composición del corpus, porque un buen clasificador sobre un corpus mayoritariamente no relevante produce pocas detecciones y eso no es un defecto; y documentar los límites de acceso de la fuente como parte del producto, ya que determinan qué afirmaciones son sostenibles.

# REFERENCIAS BIBLIOGRÁFICAS

Dengra, E., y Rivas, M. (2026). *Observatorio OSINT: Diseño e implementación de un sistema de recolección y análisis del discurso público sobre ciberseguridad en Bluesky en América Latina y el Caribe* (Trabajo Final de Carrera inédito, versión consultada de octubre de 2026). Universidad Tecnológica Nacional, Facultad Regional Mendoza. Cifras citadas según la versión consultada el 15/10/2026; por tratarse de un trabajo inédito, pueden variar en versiones posteriores.

Glassman, M., y Kang, M. J. (2012). Intelligence in the internet age: The emergence and evolution of Open Source Intelligence (OSINT). *Computers in Human Behavior, 28*(2), 673-682. https://doi.org/10.1016/j.chb.2011.11.014

Han, J., Kamber, M., y Pei, J. (2012). *Data mining: Concepts and techniques* (3.ª ed.). Morgan Kaufmann.

Hevner, A. R., March, S. T., Park, J., y Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75-105. https://doi.org/10.2307/25148625

ISO/IEC. (2022). *ISO/IEC 27001:2022. Seguridad, ciberseguridad y protección de la privacidad. Sistemas de gestión de la seguridad de la información. Requisitos*. International Organization for Standardization.

Jurafsky, D., y Martin, J. H. (2009). *Speech and language processing: An introduction to natural language processing, computational linguistics, and speech recognition* (2.ª ed.). Pearson Prentice Hall.

Landis, J. R., y Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics, 33*(1), 159-174. https://doi.org/10.2307/2529310

Ley 25.326 de Protección de Datos Personales. (2000, 4 de octubre). Honorable Congreso de la Nación Argentina. Boletín Oficial de la República Argentina.

Liao, X., Yuan, K., Wang, X., Li, Z., Xing, L., y Beyah, R. (2016). Acing the IOC game: Toward automatic discovery and analysis of open-source cyber threat intelligence. En *Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security (CCS ’16)* (pp. 755-766). ACM. https://doi.org/10.1145/2976749.2978315

n8n GmbH. (2026). *n8n documentation (v2.40.6): Workflow automation, rate limits and database nodes*. https://docs.n8n.io/

Pastor-Galindo, J., Nespoli, P., Gómez Mármol, F., y Martínez Pérez, G. (2020). The not yet exploited goldmine of OSINT: Opportunities, open challenges and future trends. *IEEE Access, 8*, 10282-10304. https://doi.org/10.1109/ACCESS.2020.2965257

Peffers, K., Tuunanen, T., Rothenberger, M. A., y Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45-77. https://doi.org/10.2753/MIS0742-1222240302

Poder Ejecutivo Nacional. (2001). *Decreto 1558/2001: Reglamentación de la Ley 25.326 de Protección de Datos Personales*. Boletín Oficial de la República Argentina.

PostgreSQL Global Development Group. (2026). *PostgreSQL 18 documentation*. https://www.postgresql.org/docs/18/

Reddit Inc. (2026). *Reddit API terms of service and developer documentation: OAuth2 authentication, rate limiting and endpoint guidelines*. https://www.reddit.com/dev/api/

Russell, M. A., y Klassen, M. (2019). *Mining the social web: Data mining Facebook, Twitter, LinkedIn, Instagram, GitHub, and more* (3.ª ed.). O’Reilly Media.

Zong, S., Ritter, A., Mueller, G., y Wright, E. (2019). Analyzing the perceived severity of cybersecurity threats reported on social media. En *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT 2019)* (pp. 1380-1390). Association for Computational Linguistics. https://doi.org/10.18653/v1/N19-1140

# ANEXOS

## Anexo A: DDL completo de PostgreSQL

Esquema físico real del sistema, residente en la base `tesi_osint` del clúster PostgreSQL 18 del proyecto. El encabezado del archivo enumera las correcciones aplicadas respecto de la versión anterior del modelo, de modo que la evolución del diseño es auditable. El archivo se conserva sin modificaciones en `V4/anexos/A_DDL.sql`.

    -- =====================================================================
    --  Anexo A (V5) — DDL REAL del sistema
    --  Motor: PostgreSQL (cluster propio del proyecto, puerto 5433)
    --  Base: tesi_osint  |  Rol: tesi_app
    --
    --  CORRECCIONES APLICADAS vs. Anexo A de la V2 (auditor):
    --   [N-06]  + columna nlp_score (puntuación normalizada [0,1])
    --   [N-06]  + columna entities (entidades tecnológicas extraídas, JSONB)
    --   [N-06]  + tablas anomalias y alertas (el modelo no las tenía)
    --   [m-20]  posts.subreddit_id pasa de ON DELETE CASCADE a RESTRICT
    --           (desactivar monitoreo con active_monitoring, no borrando)
    --   [H-16]  se ELIMINA pg_trgm y el índice GIN sobre to_tsvector:
    --           la clasificación ocurre en n8n (diccionario), no en la DB
    --           vía búsqueda de texto completo (no justificado)
    --   [H-01]  author_hash CHAR(64) con HMAC-SHA-256 (la V2 decía
    --           "SHA-256 + Salt" — se corrige terminología y mecanismo en la V4)
    --   [m-21]  alertas.estado DEFAULT 'PENDIENTE' (era 'ENVIADA': una inserción
    --           sin estado explícito quedaba registrada como enviada aunque el
    --           envío estuviera deshabilitado). Renombrados los comentarios.
    --          + anomalias: UNIQUE (categoria, ventana_inicio) para extender la
    --           idempotencia del nodo de análisis a la base (reejecutar el motor
    --           no duplica evaluaciones).
    --
    --  La latencia publicación→ingesta se obtiene de:
    --      ingested_at - created_utc  (no hace falta columna adicional)
    -- =====================================================================

    BEGIN;

    -- 1. Subreddits monitoreados
    CREATE TABLE IF NOT EXISTS subreddits (
        id                VARCHAR(50)  PRIMARY KEY,
        display_name      VARCHAR(100) UNIQUE NOT NULL,
        subscribers       INTEGER      DEFAULT 0,
        active_monitoring BOOLEAN      DEFAULT TRUE,
        created_at        TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP
    );

    -- 2. Publicaciones principales
    CREATE TABLE IF NOT EXISTS posts (
        id            VARCHAR(50)  PRIMARY KEY,
        subreddit_id  VARCHAR(50)  NOT NULL REFERENCES subreddits(id) ON DELETE RESTRICT,
        title         TEXT         NOT NULL,
        selftext      TEXT,
        url           TEXT,
        author_hash   CHAR(64)     NOT NULL,          -- usuario seudonimizado (HMAC-SHA-256)
        score         INTEGER      DEFAULT 0,
        num_comments  INTEGER      DEFAULT 0,
        created_utc   TIMESTAMPTZ  NOT NULL,          -- fecha real de publicación en Reddit
        nlp_category  VARCHAR(100),                   -- salida del clasificador por diccionario
        nlp_score     REAL         CHECK (nlp_score BETWEEN 0 AND 1),  -- [N-06] puntuación [0,1]
        entities      JSONB,                          -- [N-06] entidades extraídas (OE4)
        nlp_processed BOOLEAN      DEFAULT FALSE,
        ingested_at   TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP  -- cuándo lo ingirió el sistema (latencia)
    );

    -- 3. Comentarios asociados
    CREATE TABLE IF NOT EXISTS comments (
        id            VARCHAR(50)  PRIMARY KEY,
        post_id       VARCHAR(50)  NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
        body          TEXT         NOT NULL,
        author_hash   CHAR(64)     NOT NULL,
        score         INTEGER      DEFAULT 0,
        created_utc   TIMESTAMPTZ  NOT NULL,
        nlp_category  VARCHAR(100),
        nlp_score     REAL         CHECK (nlp_score BETWEEN 0 AND 1),
        nlp_processed BOOLEAN      DEFAULT FALSE,
        ingested_at   TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP
    );

    -- 4. Registro de disparos del motor de anomalías  [N-06]
    CREATE TABLE IF NOT EXISTS anomalias (
        id            BIGSERIAL   PRIMARY KEY,
        ventana_inicio TIMESTAMPTZ NOT NULL,          -- inicio de la ventana analizada
        ventana_fin    TIMESTAMPTZ NOT NULL,          -- fin de la ventana analizada
        categoria      VARCHAR(100) NOT NULL,
        n_observado    INTEGER     NOT NULL,          -- posts contados en la ventana
        base_media     REAL        NOT NULL,          -- promedio histórico de la categoría
        umbral         REAL        NOT NULL,          -- umbral disparado (justificado en 4.5)
        disparo        BOOLEAN     NOT NULL DEFAULT FALSE,
        created_at     TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
        -- [m-21] una evaluación por (categoría, ventana): reejecutar el motor no duplica
        CONSTRAINT anomalias_categoria_ventana_uniq UNIQUE (categoria, ventana_inicio)
    );

    -- 5. Alertas registradas  [N-06]  [m-21]
    CREATE TABLE IF NOT EXISTS alertas (
        id           BIGSERIAL    PRIMARY KEY,
        anomalia_id  BIGINT       REFERENCES anomalias(id) ON DELETE CASCADE,
        canal        VARCHAR(50)  NOT NULL,           -- ej.: 'telegram'
        destinatario VARCHAR(200),
        payload      JSONB,                           -- carga útil del aviso (sin datos personales)
        estado       VARCHAR(20)  DEFAULT 'PENDIENTE', -- [m-21] 'PENDIENTE' hasta confirmar el envío
        created_at   TIMESTAMPTZ  DEFAULT CURRENT_TIMESTAMP
    );

    -- 6. Índices para análisis
    CREATE INDEX IF NOT EXISTS idx_posts_created_utc    ON posts (created_utc DESC);
    CREATE INDEX IF NOT EXISTS idx_posts_nlp_category   ON posts (nlp_category);
    CREATE INDEX IF NOT EXISTS idx_posts_ingested_at    ON posts (ingested_at);
    CREATE INDEX IF NOT EXISTS idx_comments_post_id     ON comments (post_id);
    CREATE INDEX IF NOT EXISTS idx_anomalias_created_at ON anomalias (created_at);

    COMMIT;

## Anexo B: Inventario de nodos del workflow

La Tabla B.1 reproduce el inventario de nodos con el tipo técnico y la responsabilidad de cada uno, en el mismo orden en que se ejecutan.

**Tabla B.1. Inventario de nodos y responsabilidades**

| \# | Nodo | Tipo | Flujo | Responsabilidad |
|----|----|----|----|----|
| 1 | `Schedule Ingesta` | `scheduleTrigger` | Ingesta | Dispara el ciclo cada 15 minutos |
| 2 | `Prepare Subreddits` | `code` | Ingesta | Construye la lista de comunidades activas |
| 3 | `Upsert Subreddits` | `postgres` | Ingesta | Alta y actualización de comunidades |
| 4 | `Loop Over Items` | `splitInBatches` | Ingesta | Itera comunidades, lote de tamaño 1 |
| 5 | `Espera Rate Limit` | `wait` | Ingesta | Espera fija de 60 s entre comunidades |
| 6 | `Fetch Posts RSS` | `rssFeedRead` | Ingesta | Descarga el listado público de novedades |
| 7 | `Parse Reddit Posts` | `code` | Ingesta | Normaliza campos y limpia el marcado |
| 8 | `HMAC Anonymize` | `code` | Ingesta | Seudonimiza el autor con HMAC-SHA-256 |
| 9 | `Classify Dictionary` | `code` | Ingesta | Categoría y puntuación por diccionario |
| 10 | `Extract Entities` | `code` | Ingesta | Extrae entidades a `JSONB` |
| 11 | `Prepare Upsert` | `code` | Ingesta | Arma el registro final |
| 12 | `Upsert Posts` | `postgres` | Ingesta | `INSERT … ON CONFLICT DO UPDATE` (idempotente) |
| 13 | `Schedule Anomalias` | `scheduleTrigger` | Análisis | Dispara el análisis a las 12:05 |
| 14 | `Query Daily Counts` | `postgres` | Análisis | Conteos por categoría y día local |
| 15 | `Anomaly Engine` | `code` | Análisis | Línea base, umbral de Poisson y decisión |
| 16 | `Registrar Anomalias y Alertas` | `postgres` | Análisis | Persiste la evaluación y la alerta |
| 17 | `Send Telegram Alert` | `httpRequest` | Análisis | Envío al canal (deshabilitado por defecto) |

**Composición del workflow.** 17 nodos en total, distribuidos en 11 nodos de ingesta, 5 nodos de análisis y 1 disparador por flujo. La representación gráfica de nodos y conexiones se presenta en la Figura 3, generada a partir del propio archivo exportado. Además del inventario, este anexo transcribe el **código de los cuatro nodos de código** (B.2), el **SQL de los tres nodos de base de datos** (B.3) y las **quince consultas de evidencia del Capítulo 5** (B.4). El archivo `V4/anexos/B_workflow.json` (32.843 bytes) contiene el flujo desplegado, incluyendo la corrección del control de tasa (nodo de espera de 60 segundos y centinela del lazo) descrita en 4.1 y 4.3; se regenera mediante `V4/scripts/generar_workflow.py` y **no se edita manualmente**. El mecanismo de notificación está presente; el envío permanece **deshabilitado** por configuración del nodo (ver 4.5 y 5.4). El destino y el token del canal no viven en el artefacto sino en **variables de entorno** del contenedor (`TELEGRAM_CHAT_ID`, `TELEGRAM_BOT_TOKEN`). Cuando el envío se habilita, el valor del token **se carga en la credencial de n8n desde la interfaz de administración**, y esa operación es compatible con la regla de 4.6: la regla prohíbe **editar el flujo** —el grafo de nodos y su lógica— desde la interfaz, no **vincular una credencial** a un nodo, que es precisamente el mecanismo previsto para no incorporar secretos al artefacto versionado.

### Anexo B.2. Código de los nodos de transformación

Los cuatro nodos de código del flujo se transcriben a continuación tal como están definidos en el artefacto desplegado. El código es el que efectivamente corrió durante la ventana B5 y es la fuente de la lógica descrita en el Capítulo 4: la seudonimización (4.3, nodo `HMAC Anonymize`), la clasificación y su puntuación (4.4, nodo `Classify Dictionary`), la extracción de entidades (5.6, nodo `Extract Entities`) y el motor de anomalías (4.5, nodo `Anomaly Engine`). El mismo contenido se conserva como archivos independientes dentro del paquete de evidencia (`anexo_b/*.js`).

**Código B.1. Nodo** `HMAC Anonymize` **— seudonimización del autor (HMAC-SHA-256).**

    const crypto = require('crypto');
    const key = $env.OSINT_HMAC_KEY;
    if (!key) {
      throw new Error('Falta la variable de entorno OSINT_HMAC_KEY. Seteala antes de arrancar n8n (ver GUIA_EJECUCION.md).');
    }
    const out = [];
    for (const item of $input.all()) {
      if (item.json._skip) { out.push(item); continue; }   // centinela de 429: pasa intacto
      out.push({
        json: {
          ...item.json,
          author_hash: crypto.createHmac('sha256', key).update(String(item.json.author)).digest('hex'),
          created_utc_iso: new Date((item.json.created_utc || 0) * 1000).toISOString()
        }
      });
      delete out[out.length - 1].json.author;
    }
    return out;

**Código B.2. Nodo** `Classify Dictionary` **— clasificación por diccionario y puntuación saturante.**

    // Clasificador por diccionario bilingue (ES+EN), 9 categorias. Texto normalizado sin acentos.
    // Match: terminos de UNA palabra por token EXACTO (words.has); de VARIAS por substring (text.includes).
    // Restricciones que el diccionario respeta (si se rompen, el termino nunca encontraria el texto):
    //   - sin tildes: la normalizacion NFD las saca del texto, no del termino ('bufer' nunca encontraria el texto);
    //   - sin guiones: el tokenizado parte en /[^a-z0-9]+/, o sea 'zero-day' se parte en 'zero'+'day'
    //     y la cadena con guion nunca aparece como token -> escribi 'zero day';
    //   - con las formas conjugadas reales: 'filtraron' no matchea con 'filtrar'.
    // Se sacaron los cuasisinonimos demasiado genericos (mp, cuenta, enlace, correo, bug, falla,
    // transferencia, banco, filtrar, cangrejo, pescar, actualizacion) por falsos positivos.
    // 2026-09-30: se SACO 'dni' de 'Filtración de Datos' por el mismo motivo. Matcheaba con un post
    // sobre "dar de baja apoderado de jubilacion anses", que es tramite administrativo y no una
    // filtracion. Con MIN_HITS=2 el falso positivo no se notaba porque el post tenia un solo hit; al
    // bajar el umbral a 1 se hizo visible. Un termino que matchea con paperwork es demasiado generico.
    // Fórmula de puntuación (4.4), AHORA SATURANTE: score = min(1, hits(c) / SATURATION), hits >= MIN_HITS.
    // Por qué el cambio: antes era score = hits(c) / |keywords(c)|, y el denominador depende del tamaño
    // del diccionario. Al ampliarlo de 5 a 9 categorías (y de ~10 a ~22 términos cada una), el MISMO
    // post con los mismos 2 hits pasaba de 0.22 a 0.07: la escala se comprime y nlp_score deja de ser
    // comparable entre corridas y entre categorías. SATURATION fija la escala (2 hits=0.5, 3=0.75,
    // 4+=1.0), independiente del tamaño del diccionario, y sigue dentro de [0,1] (CHECK en la DB).
    //
    // MIN_HITS BAJADO DE 2 A 1 (2026-09-30, evaluacion de la muestra de control de 50 posts):
    // con MIN_HITS=2 el clasificador descartaba amenazas obvias. "Fake Interpol Investigation Emails
    // Are Dropping Ransomware on Small Businesses" tiene la palabra 'ransomware' en el TITULO, el
    // termino existe en el diccionario y matchea perfecto, y aun asi el post se fue a 'No relevante'
    // por no alcanzar el segundo hit. Medido sobre los 50 posts etiquetados a mano:
    //   MIN_HITS=2 -> detecta 25/29 amenazas (86,2 %)
    //   MIN_HITS=1 -> detecta 27/29 amenazas (93,1 %)
    // Costo medido del cambio: los falsos positivos pasan de 1/21 a 3/21 en el grupo de control.
    // Los 2 nuevos son terminos demasiado genericos del diccionario, no un efecto del umbral:
    // 'dni' matcheaba con un post sobre dar de baja un apoderado de jubilacion y se saco en el
    // mismo commit (ver 'Filtración de Datos'). MIN_HITS=1 tambien absorbe el ruido de fondo que
    // antes salia: 'suplantacion de identidad' matchea con consultas legales laborales, que quedan
    // fuera del ambito del proyecto (amenazas a infraestructura).
    // Quedan 2 falsos negativos por vocabulario ausente ('edr evasion', 'red team'). NO se
    // agregaron esos terminos: definirlos sin conocimiento tecnico de ciberseguridad meteria el
    // mismo error conceptual adentro del diccionario. Documentado como limitacion abierta en
    // V4/evidencias/evaluacion_muestra_control_2026-09-30.md.
    const DICT = {
      'Phishing': ['phishing', 'phisher', 'smishing', 'vishing', 'spear phishing', 'correo fraudulento', 'correo suplantado', 'remitente falso', 'enlace fraudulento', 'enlace sospechoso', 'pagina falsa', 'sitio falso', 'portal falso', 'ingreso falso', 'verificar identidad', 'verificacion de identidad', 'captura de datos', 'suplantacion de correo', 'business email compromise', 'fake login', 'credential harvest', 'harvesting'],
      'Robo de Credenciales': ['clonacion de tarjeta', 'tarjeta clonada', 'clonar', 'robo de contrasena', 'robaron mi contrasena', 'cambio de contrasena', 'cambiar mi contrasena', 'acceso no autorizado', 'acceso remoto', 'tomaron control de la cuenta', 'tomo control de mi cuenta', 'sesion robada', 'robo de token', 'segundo factor', 'factor de autenticacion', 'credential stuffing', 'account takeover', 'session hijacking', 'session hijack', 'token theft', 'password theft', 'password dumping', '2fa bypass', 'mfa fatigue', 'sim swap', 'sim swapping', 'otp bypass', 'push bombing', 'adversary in the middle'],
      'Malware': ['malware', 'virus troyano', 'troyano', 'gusano', 'keylogger', 'rootkit', 'infostealer', 'stealer', 'dropper', 'loader', 'criptominer', 'miner', 'carga util', 'ejecucion remota', 'command and control', 'c2 server', 'rat', 'packed', 'obfuscated', 'ofuscado', 'payload', 'reverse shell', 'bind shell', 'webshell'],
      'Ransomware': ['ransomware', 'nota de rescate', 'pedir rescate', 'piden rescate', 'bloquearon mis archivos', 'mis archivos estan cifrados', 'secuestro de datos', 'extorsion', 'wannacry', 'lockbit', 'revil', 'blackcat', 'locker', 'decryptor', 'desencriptador'],
      'Vulnerabilidades': ['cve', 'exploit', 'exploits', 'parche', 'parchear', 'patch tuesday', 'actualizacion de seguridad', 'backdoor', 'puerta trasera', 'zero day', 'prueba de concepto', 'proof of concept', 'inyeccion sql', 'sql injection', 'xss', 'rce', 'ejecucion remota de codigo', 'escalamiento de privilegios', 'buffer overflow', 'desbordamiento de buffer', 'bypass de autenticacion', 'authentication bypass', 'kerberoasting', 'movimiento lateral', 'lateral movement', 'privilege escalation', 'nvd', 'cisa', 'zero day vulnerability', 'poc'],
      'Filtración de Datos': ['filtracion', 'filtraron', 'filtrado', 'filtran', 'fuga de datos', 'fuga de informacion', 'base filtrada', 'base de datos expuesta', 'bases expuestas', 'base expuesta', 'datos personales', 'venta de datos', 'venden datos', 'vazamiento', 'exfiltracion', 'exfiltrated', 'leak', 'leaked', 'leaks', 'breach', 'breached', 'exposed database', 'exposed credentials', 'credentials dump', 'combo list', 'dark web', 'pastebin', 'data dump', 'breach notification'],
      'Infraestructura y Ataques': ['botnet', 'ddos', 'denegacion de servicio', 'denial of service', 'caida de servicio', 'sitio caido', 'tiraron el sitio', 'tiraron abajo el sitio', 'ataque de red', 'amplificacion', 'reflection attack', 'volumetric', 'ip flood', 'takedown', 'cayeron los servidores', 'caida de servidores'],
      'Hacktivismo': ['hacktivismo', 'hacktivista', 'hackeo', 'hackearon', 'hackear', 'deface', 'defacement', 'defaced', 'dox', 'doxeado', 'doxing', 'anonymous', 'filtracion publicada', 'publicacion de datos filtrados', 'protesta hacker', 'hactivist'],
      'Ingenieria Social': ['ingenieria social', 'social engineering', 'mecanismo de engano', 'se hacen pasar', 'suplantar identidad', 'suplantacion de identidad', 'baiting', 'confianza ganada', 'falsa llamada', 'llamada del banco', 'falso empleado', 'falsa policia', 'falso soporte', 'pretexting', 'impersonation', 'pretexto', 'scam call', 'fake support', 'vishing script', 'ayuda de escritorio falsa']
    };
    const MIN_HITS = 1;
    const SATURATION = 4; // hits a partir de los cuales el score vale 1.0 (escala fija, ver cabecera)
    const norm = (s) => String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    const out = [];
    for (const item of $input.all()) {
      if (item.json._skip) { out.push(item); continue; }   // centinela de 429: no se clasifica
      const text = norm(item.json.title + ' ' + (item.json.selftext || ''));
      const words = new Set(text.split(/[^a-z0-9]+/));
      let best = null;
      let bestHits = 0;
      for (const cat of Object.keys(DICT)) {
        let hits = 0;
        for (const kw of DICT[cat]) {
          const k = kw.includes(' ') ? (text.includes(kw) ? 1 : 0) : (words.has(kw) ? 1 : 0);
          hits += k;
        }
        if (hits > bestHits) {
          bestHits = hits;
          best = cat;
        }
      }
      if (best && bestHits >= MIN_HITS) {
        item.json.nlp_category = best;
        item.json.nlp_score = Math.min(1, Math.round((bestHits / SATURATION) * 10000) / 10000); // normalizado [0,1]
      } else {
        item.json.nlp_category = 'No relevante';
        item.json.nlp_score = 0;
      }
      out.push({ json: item.json });
    }
    return out;

**Código B.3. Nodo** `Extract Entities` **— extracción de entidades tecnológicas a** `JSONB`**.**

    // Extracción de entidades (OE4, [N-06]): CVE, emails, IPs, dominios y productos.
    const PRODUCTS = ['whatsapp', 'telegram', 'mercado pago', 'windows', 'linux', 'android', 'ios', 'chrome', 'firefox', 'bitcoin', 'usdt', 'afi p', 'banco nacion', 'galicia', 'santander', 'uala', 'cvu', 'mercado libre'];
    const norm = (s) => String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    const uniq = (a) => Array.from(new Set(a));
    const out = [];
    for (const item of $input.all()) {
      if (item.json._skip) { out.push(item); continue; }   // centinela de 429: sin entidades
      const raw = item.json.title + ' ' + (item.json.selftext || '');
      const low = norm(raw);
      const entities = {
        cves: uniq((low.match(/\bcve-\d{4}-\d{4,7}\b/g) || []).map((x) => x.toUpperCase())).slice(0, 20),
        emails: uniq((raw.match(/\b[\w.+-]+@[\w-]+\.[\w.]+\b/g) || [])).slice(0, 20),
        ips: uniq((low.match(/\b(?:\d{1,3}\.){3}\d{1,3}\b/g) || [])).slice(0, 20),
        domains: uniq((low.match(/\b(?:[a-z0-9-]+\.)+(?:com|ar|org|net|io|gov|edu)\b/g) || []).filter((d) => !d.startsWith('reddit.com'))).slice(0, 20),
        products: uniq(PRODUCTS.filter((p) => low.includes(p))).slice(0, 20)
      };
      item.json.entities = entities;
      item.json.entities_json = JSON.stringify(entities);
      out.push({ json: item.json });
    }
    return out;

**Código B.4. Nodo** `Anomaly Engine` **— línea base, umbral de Poisson y decisión de disparo.**

    // Motor de anomalías (4.5): ventana diaria, base = media diaria de los 10 días previos,
    // umbral = max(cuantil 95 de Poisson + 1, mínimo absoluto 3). Disparo si n_observado >= umbral.
    // Poisson real por recurrencia: P(i) = P(i-1) * l / i, arrancando en P(0) = e^-l.
    //
    // 2026-10-05: la version anterior aritmetizaba las masas con
    //   for (let j = 2; j <= i; j++) logP += Math.log(l / j)
    // lo que produce l^(i-1)/i! * e^-l en vez de l^i/i! * e^-l: le falta un factor l
    // a TODAS las masas menos la de i = 0. Comprobado con l = 5,5:
    //   P(1) exacta 0,022477 | la que computaba el nodo 0,004087  (factor 0,18)
    // La CDF rota satura en 1/l, asi que para l > 1,05 nunca alcanza 0,95, el while
    // de busqueda del umbral corre hasta el tope de 500 y devuelve umbral = 501.
    // Con umbral 501 ninguna categoria con base > 1,05 puede disparar nunca: se
    // comprobo en produccion con Malware (base 5,5) y Vulnerabilidades (base 4,3),
    // ambos con umbral 501. La unica categoria que sobrevivia era Phishing
    // (base 0,7), por accidente, no por diseno.
    function poissonCdf(k, l) {
      if (!(l > 0)) return 1;
      let term = Math.exp(-l);
      let s = term;
      for (let i = 1; i <= k; i++) {
        term = term * l / i;
        s += term;
      }
      return Math.min(1, s);
    }
    const MIN_ABS = 3;
    const out = [];
    for (const item of $input.all()) {
      const lambda = Math.max(0, Number(item.json.base_media) || 0);
      const n = Math.max(0, Math.round(Number(item.json.n_observado) || 0));
      let t = 0;
      if (lambda > 0) {
        while (t < 500 && (1 - poissonCdf(t, lambda)) > 0.05) {
          t += 1;
        }
      }
      const umbralPoisson = lambda > 0 ? t + 1 : 1;
      const umbral = Math.max(umbralPoisson, MIN_ABS);
      out.push({
        json: {
          ventana_inicio: item.json.ventana_inicio,
          ventana_fin: item.json.ventana_fin,
          categoria: item.json.categoria,
          n_observado: n,
          base_media: Math.round(lambda * 1000) / 1000,
          umbral: umbral,
          disparo: n >= umbral
        }
      });
    }
    return out;

### Anexo B.3. SQL de persistencia y análisis

Los tres nodos de base de datos se transcriben con su sentencia completa. El uso de parámetros posicionales (`$1`…`$13`) corresponde al mecanismo de sustitución del nodo Postgres de n8n; el SQL se ejecuta una vez por elemento de entrada.

**SQL B.5. Nodo** `Upsert Posts` **— carga idempotente de publicaciones.**

La lista `SET` de esta sentencia enumera **nueve** campos; `created_utc` e `ingested_at` no integran la lista y por lo tanto no se sobrescriben al reprocesar el mismo elemento (ver 4.3 y la corrección del hallazgo m-29). La cláusula `WHERE COALESCE($13, FALSE) = FALSE` implementa el centinela del lazo descrito en 4.3.

    -- Guardia anti-centinela (IN-08). El item de error que genera 'Parse Reddit Posts'
    -- cuando Reddit responde 429 viaja por toda la cadena para que el loop no se
    -- corte, pero NO debe terminar en la tabla: el sub que fallo vale como 0 posts.
    -- El sentinel llega con $13 = TRUE, asi que este SELECT no devuelve filas.
    -- Se hace con SELECT ... WHERE y no con un IF antes del nodo porque el nodo
    -- corre una query por item de entrada: el IF solo no alcanza si el item llega
    -- mezclado con posts reales, que es justo el caso de un 429 en el 2o subreddit.
    INSERT INTO posts (id, subreddit_id, title, selftext, url, author_hash, score, num_comments, created_utc, nlp_category, nlp_score, entities, nlp_processed)
    SELECT $1, $2, $3, $4, $5, $6, $7, $8, $9::timestamptz, $10, $11, $12::jsonb, TRUE
    WHERE COALESCE($13, FALSE) = FALSE
    ON CONFLICT (id) DO UPDATE SET
      title = EXCLUDED.title,
      selftext = EXCLUDED.selftext,
      url = EXCLUDED.url,
      score = EXCLUDED.score,
      num_comments = EXCLUDED.num_comments,
      nlp_category = EXCLUDED.nlp_category,
      nlp_score = EXCLUDED.nlp_score,
      entities = EXCLUDED.entities,
      nlp_processed = TRUE

**SQL B.6. Nodo** `Query Daily Counts` **— conteos por categoría y día local.**

La ventana observada es el día anterior completo en hora local (`America/Argentina/Buenos_Aires`) y la línea base es la media diaria de los diez días previos (4.5).

    -- Ventana: ayer [00:00, 00:00) hora de Buenos Aires. Base: media diaria de los 10 días previos.
    SELECT
      p.nlp_category AS categoria,
      COUNT(*) FILTER (WHERE p.ingested_at >= date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '1 day'
                       AND p.ingested_at <  date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires')) AS n_observado,
      COUNT(*) FILTER (WHERE p.ingested_at >= date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '11 day'
                       AND p.ingested_at <  date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '1 day') / 10.0 AS base_media,
      (date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '1 day') AT TIME ZONE 'America/Argentina/Buenos_Aires' AS ventana_inicio,
      date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') AT TIME ZONE 'America/Argentina/Buenos_Aires' AS ventana_fin
    FROM posts p
    WHERE p.nlp_category IS NOT NULL
      AND p.nlp_category <> 'No relevante'
      AND p.ingested_at >= date_trunc('day', now() AT TIME ZONE 'America/Argentina/Buenos_Aires') - interval '11 day'
    GROUP BY p.nlp_category
    ORDER BY p.nlp_category

**SQL B.7. Nodo** `Registrar Anomalias y Alertas` **— persistencia de la evaluación y de la alerta.**

La inserción en `anomalias` es idempotente sobre `(ventana_inicio, ventana_fin, categoria)`; la alerta se genera únicamente cuando la evaluación registra un disparo (4.5).

    -- Inserta TODA la evaluación en anomalias; genera alerta solo si hubo disparo.
    -- OJO 1: la función que acepta jsonb se llama jsonb_to_recordset. json_to_recordset
    -- solo tiene la firma (json); invocarla con un jsonb da
    -- 'no existe la función json_to_recordset(jsonb)' y la evaluación no se registra.
    -- OJO 2: *to_recordset exige un ARRAY json en el nivel superior. El nodo manda
    -- JSON.stringify($json), que es un objeto suelto, y eso da
    -- 'no se puede invocar jsonb_to_recordset en un no-array'. Por eso el
    -- jsonb_build_array: envuelve el objeto en un array de un elemento.
    -- El nodo corre la query una vez por item de entrada, asi que aqui llega
    -- una sola categoria por vez y se inserta una fila por evaluacion.
    -- OJO 3: la insercion es IDEMPOTENTE sobre (ventana_inicio, ventana_fin,
    -- categoria). Sin este WHERE NOT EXISTS, ejecutar el workflow dos veces el
    -- mismo dia inserta la misma evaluacion dos veces y el conteo de
    -- suficiencia (que cuenta filas por dia) queda inflado. Con el guardia,
    -- relanzar el nodo a mano para recuperar un dia perdido no duplica nada,
    -- y tampoco se generan alertas repetidas porque el INSERT de alertas sale
    -- de 'ins', que queda vacio si la evaluacion ya existia.
    WITH reg AS (
      SELECT * FROM jsonb_to_recordset(jsonb_build_array($1::jsonb))
        AS x(ventana_inicio timestamptz, ventana_fin timestamptz, categoria varchar, n_observado int, base_media real, umbral real, disparo boolean)
    ),
    ins AS (
      INSERT INTO anomalias (ventana_inicio, ventana_fin, categoria, n_observado, base_media, umbral, disparo)
      SELECT * FROM reg
      WHERE NOT EXISTS (
        SELECT 1 FROM anomalias a
        WHERE a.ventana_inicio = reg.ventana_inicio
          AND a.ventana_fin    = reg.ventana_fin
          AND a.categoria      = reg.categoria
      )
      RETURNING id, categoria, n_observado, base_media, umbral, disparo, ventana_inicio
    )
    INSERT INTO alertas (anomalia_id, canal, destinatario, payload, estado)
    SELECT id, 'telegram', 'canal_tfi',
           jsonb_build_object('categoria', categoria, 'n_observado', n_observado, 'base_media', base_media, 'umbral', umbral, 'ventana_inicio', ventana_inicio),
           'PENDIENTE'
    FROM ins
    WHERE disparo
    RETURNING id, anomalia_id, canal, payload, estado

### Anexo B.4. Consultas SQL de la evidencia del Capítulo 5

Se transcriben las quince consultas de solo lectura que producen las Tablas 5.1 a 5.6 y las Figuras 1 a 4, ejecutadas el 19/10/2026 sobre la base `tesi_osint`. Cada consulta fija por medio de literales de fecha el estado congelado del corte, de modo que su salida no cambia aunque la base crezca después; la salida literal archivada es la del Anexo D (`consultas_corpus_b5.txt`). Las consultas no modifican datos: todas son `SELECT`.

    -- Consultas Q1..Q15 del capítulo de resultados (ventana B5, corte 2026-10-17).
    -- Todas son de solo lectura. Los literales de fecha fijan el estado congelado
    -- del 2026-10-19, de modo que la base pueda haber crecido sin alterar la salida.
    -- Track secundario congelado: 31 filas persistidas hasta 2026-10-19 18:00 UTC.

    -- === Q1 TOTALES ===
    SELECT
      count(*) FILTER (WHERE ingested_at < '2026-10-19 18:00:00+00') AS total,
      count(*) FILTER (WHERE created_utc < '2026-10-18 03:00:00+00'
                         AND ingested_at < '2026-10-19 00:00:00+00') AS ventana,
      count(*) FILTER (WHERE created_utc < '2026-10-01 03:00:00+00'
                         AND ingested_at < '2026-10-01 03:00:00+00') AS previos,
      count(*) FILTER (WHERE ingested_at >= '2026-10-19 00:00:00+00'
                         AND ingested_at <  '2026-10-19 18:00:00+00') AS track,
      (SELECT count(*) FROM comments) AS comentarios,
      count(*) FILTER (WHERE ingested_at < '2026-10-19 00:00:00+00'
                         AND nlp_category IS NULL) AS sin_categoria
    FROM posts;

    -- === Q2 RANGO DE INGESTA VENTANA ===
    SELECT
      min(ingested_at) AS min_ingesta,
      max(ingested_at) AS max_ingesta,
      min(created_utc) AS min_creado,
      max(created_utc) AS max_creado
    FROM posts
    WHERE created_utc < '2026-10-18 03:00:00+00'
      AND ingested_at < '2026-10-19 00:00:00+00';

    -- === Q3 POR SUBREDDIT ===
    SELECT
      subreddit_id,
      count(*) AS n,
      round(100.0 * count(*) / sum(count(*)) OVER (), 2) AS pct,
      count(*) FILTER (WHERE nlp_category = 'No relevante') AS no_relevante,
      round(100.0 * count(*) FILTER (WHERE nlp_category = 'No relevante')
            / count(*), 2) AS pct_no_rel
    FROM posts
    WHERE created_utc < '2026-10-18 03:00:00+00'
      AND ingested_at < '2026-10-19 00:00:00+00'
    GROUP BY subreddit_id
    ORDER BY n DESC;

    -- === Q4 POR DIA (hora local) ===
    SELECT
      (ingested_at AT TIME ZONE 'America/Argentina/Buenos_Aires')::date AS dia,
      count(*) AS n
    FROM posts
    WHERE created_utc < '2026-10-18 03:00:00+00'
      AND ingested_at < '2026-10-19 00:00:00+00'
    GROUP BY 1
    ORDER BY 1;

    -- === Q5 TABLA 3 CATEGORIAS ===
    SELECT
      nlp_category AS categoria,
      count(*) AS n,
      round(100.0 * count(*) / sum(count(*)) OVER (), 2) AS pct,
      round(avg(nlp_score)::numeric, 3) AS score_medio
    FROM posts
    WHERE created_utc < '2026-10-18 03:00:00+00'
      AND ingested_at < '2026-10-19 00:00:00+00'
    GROUP BY nlp_category
    ORDER BY n DESC;

    -- === Q6 LATENCIA ===
    SELECT
      count(*) AS n,
      round(avg(extract(epoch FROM ingested_at - created_utc) / 60.0)::numeric, 2) AS media,
      round(stddev_samp(extract(epoch FROM ingested_at - created_utc) / 60.0)::numeric, 2) AS ds,
      round(percentile_cont(0.5) WITHIN GROUP (
              ORDER BY extract(epoch FROM ingested_at - created_utc) / 60.0)::numeric, 2) AS p50,
      round(percentile_cont(0.95) WITHIN GROUP (
              ORDER BY extract(epoch FROM ingested_at - created_utc) / 60.0)::numeric, 2) AS p95,
      round(min(extract(epoch FROM ingested_at - created_utc) / 60.0)::numeric, 2) AS minimo,
      round(max(extract(epoch FROM ingested_at - created_utc) / 60.0)::numeric, 2) AS maximo,
      count(*) FILTER (WHERE extract(epoch FROM ingested_at - created_utc) / 60.0 > 5) AS gt5,
      count(*) FILTER (WHERE extract(epoch FROM ingested_at - created_utc) / 60.0 > 15) AS gt15,
      count(*) FILTER (WHERE extract(epoch FROM ingested_at - created_utc) / 60.0 > 60) AS gt60,
      count(*) FILTER (WHERE extract(epoch FROM ingested_at - created_utc) / 60.0 > 1440) AS gt24h,
      count(*) FILTER (WHERE extract(epoch FROM ingested_at - created_utc) < 0) AS negativos
    FROM posts
    WHERE created_utc < '2026-10-18 03:00:00+00'
      AND ingested_at < '2026-10-19 00:00:00+00';

    -- === Q7 ANOMALIAS RESUMEN ===
    SELECT
      count(*) AS filas,
      count(DISTINCT ventana_inicio) AS dias,
      count(*) FILTER (WHERE disparo) AS disparos,
      min(ventana_fin) AS desde,
      max(ventana_fin) AS hasta
    FROM anomalias;

    -- === Q8 ANOMALIAS POR CATEGORIA ===
    SELECT
      categoria,
      count(*) AS evals,
      sum(n_observado) AS observados,
      count(*) FILTER (WHERE disparo) AS disparos,
      round(avg(base_media)::numeric, 2) AS base_media_prom,
      round(avg(umbral)::numeric, 2) AS umbral_prom
    FROM anomalias
    GROUP BY categoria
    ORDER BY evals DESC, categoria;

    -- === Q9 DISPAROS DETALLE ===
    SELECT
      ventana_fin::date AS dia,
      categoria,
      n_observado,
      base_media,
      umbral
    FROM anomalias
    WHERE disparo
    ORDER BY dia, categoria;

    -- === Q10 CATEGORIAS EVALUADAS POR DIA ===
    SELECT
      ventana_fin::date AS dia,
      count(*) AS filas,
      string_agg(DISTINCT categoria, ' | ' ORDER BY categoria) AS cats
    FROM anomalias
    GROUP BY 1
    ORDER BY 1;

    -- === Q11 ALERTAS ===
    SELECT
      canal,
      estado,
      count(*) AS n
    FROM alertas
    GROUP BY canal, estado
    ORDER BY canal, estado;

    -- === Q12 TOP POSTS POR CATEGORIA ===
    WITH ranked AS (
      SELECT
        nlp_category,
        id,
        title AS titulo,
        nlp_score AS score,
        created_utc,
        url,
        row_number() OVER (
          PARTITION BY nlp_category
          ORDER BY nlp_score DESC, created_utc DESC
        ) AS rn
      FROM posts
      WHERE created_utc < '2026-10-18 03:00:00+00'
        AND ingested_at < '2026-10-19 00:00:00+00'
        AND nlp_category IS NOT NULL
        AND nlp_category <> 'No relevante'
    )
    SELECT
      nlp_category,
      id,
      titulo,
      round(score::numeric, 3) AS score,
      created_utc::date AS fecha,
      url
    FROM ranked
    WHERE rn <= 2
    ORDER BY nlp_category, rn;

    -- === Q13 DISTRIBUCION DE SCORE ===
    SELECT
      round(nlp_score::numeric, 2) AS score,
      count(*) AS n
    FROM posts
    WHERE created_utc < '2026-10-18 03:00:00+00'
      AND ingested_at < '2026-10-19 00:00:00+00'
    GROUP BY 1
    ORDER BY 1;

    -- === Q14 CATEGORIAS DISTINTAS EN VENTANA ===
    SELECT
      nlp_category AS categoria,
      count(*) AS n
    FROM posts
    WHERE created_utc < '2026-10-18 03:00:00+00'
      AND ingested_at < '2026-10-19 00:00:00+00'
    GROUP BY nlp_category
    ORDER BY n DESC;

    -- === Q15 TRACK SECUNDARIO ===
    SELECT
      count(*) AS n,
      min(ingested_at) AS desde,
      max(ingested_at) AS hasta
    FROM posts
    WHERE ingested_at >= '2026-10-19 00:00:00+00'
      AND ingested_at <  '2026-10-19 18:00:00+00';

## Anexo C: Diccionario de categorías y términos

**Tabla C.1. Diccionario de categorías y términos (9 categorías, 201 términos)**

Los términos se transcriben tal como están definidos en el código, **sin diacríticos**: la normalización del texto remueve las tildes antes de la comparación, y los términos que las contuvieran no coincidirían nunca.

| Categoría | Términos | Listado |
|----|---:|----|
| Phishing | 22 | `phishing`, `phisher`, `smishing`, `vishing`, `spear phishing`, `correo fraudulento`, `correo suplantado`, `remitente falso`, `enlace fraudulento`, `enlace sospechoso`, `pagina falsa`, `sitio falso`, `portal falso`, `ingreso falso`, `verificar identidad`, `verificacion de identidad`, `captura de datos`, `suplantacion de correo`, `business email compromise`, `fake login`, `credential harvest`, `harvesting` |
| Robo de Credenciales | 29 | `clonacion de tarjeta`, `tarjeta clonada`, `clonar`, `robo de contrasena`, `robaron mi contrasena`, `cambio de contrasena`, `cambiar mi contrasena`, `acceso no autorizado`, `acceso remoto`, `tomaron control de la cuenta`, `tomo control de mi cuenta`, `sesion robada`, `robo de token`, `segundo factor`, `factor de autenticacion`, `credential stuffing`, `account takeover`, `session hijacking`, `session hijack`, `token theft`, `password theft`, `password dumping`, `2fa bypass`, `mfa fatigue`, `sim swap`, `sim swapping`, `otp bypass`, `push bombing`, `adversary in the middle` |
| Malware | 24 | `malware`, `virus troyano`, `troyano`, `gusano`, `keylogger`, `rootkit`, `infostealer`, `stealer`, `dropper`, `loader`, `criptominer`, `miner`, `carga util`, `ejecucion remota`, `command and control`, `c2 server`, `rat`, `packed`, `obfuscated`, `ofuscado`, `payload`, `reverse shell`, `bind shell`, `webshell` |
| Ransomware | 15 | `ransomware`, `nota de rescate`, `pedir rescate`, `piden rescate`, `bloquearon mis archivos`, `mis archivos estan cifrados`, `secuestro de datos`, `extorsion`, `wannacry`, `lockbit`, `revil`, `blackcat`, `locker`, `decryptor`, `desencriptador` |
| Vulnerabilidades | 30 | `cve`, `exploit`, `exploits`, `parche`, `parchear`, `patch tuesday`, `actualizacion de seguridad`, `backdoor`, `puerta trasera`, `zero day`, `prueba de concepto`, `proof of concept`, `inyeccion sql`, `sql injection`, `xss`, `rce`, `ejecucion remota de codigo`, `escalamiento de privilegios`, `buffer overflow`, `desbordamiento de buffer`, `bypass de autenticacion`, `authentication bypass`, `kerberoasting`, `movimiento lateral`, `lateral movement`, `privilege escalation`, `nvd`, `cisa`, `zero day vulnerability`, `poc` |
| Filtración de Datos | 29 | `filtracion`, `filtraron`, `filtrado`, `filtran`, `fuga de datos`, `fuga de informacion`, `base filtrada`, `base de datos expuesta`, `bases expuestas`, `base expuesta`, `datos personales`, `venta de datos`, `venden datos`, `vazamiento`, `exfiltracion`, `exfiltrated`, `leak`, `leaked`, `leaks`, `breach`, `breached`, `exposed database`, `exposed credentials`, `credentials dump`, `combo list`, `dark web`, `pastebin`, `data dump`, `breach notification` |
| Infraestructura y Ataques | 16 | `botnet`, `ddos`, `denegacion de servicio`, `denial of service`, `caida de servicio`, `sitio caido`, `tiraron el sitio`, `tiraron abajo el sitio`, `ataque de red`, `amplificacion`, `reflection attack`, `volumetric`, `ip flood`, `takedown`, `cayeron los servidores`, `caida de servidores` |
| Hacktivismo | 16 | `hacktivismo`, `hacktivista`, `hackeo`, `hackearon`, `hackear`, `deface`, `defacement`, `defaced`, `dox`, `doxeado`, `doxing`, `anonymous`, `filtracion publicada`, `publicacion de datos filtrados`, `protesta hacker`, `hactivist` |
| Ingeniería Social | 20 | `ingenieria social`, `social engineering`, `mecanismo de engano`, `se hacen pasar`, `suplantar identidad`, `suplantacion de identidad`, `baiting`, `confianza ganada`, `falsa llamada`, `llamada del banco`, `falso empleado`, `falsa policia`, `falso soporte`, `pretexting`, `impersonation`, `pretexto`, `scam call`, `fake support`, `vishing script`, `ayuda de escritorio falsa` |
| **Total** | **201** | — |

El diccionario completo, con su extracción programática desde el artefacto y su fecha, se conserva en `V4/evidencias/informe_v4_2026-10-19/DICCIONARIO_REAL.md` junto con su versión en formato JSON. Las categorías se evalúan con una escala saturante de cuatro coincidencias (`nlp_score = min(1, coincidencias / 4)`) y un mínimo de una coincidencia para asignar categoría distinta de «No relevante».

## Anexo D: Repositorio, copia congelada y reproducibilidad

### D.1. Medio de acceso

La evidencia del trabajo se pone a disposición del tribunal por **dos vías complementarias**, de modo que la verificación no dependa de una sola:

**Repositorio Git versionado.** El proyecto se aloja en `https://github.com/Valentino-24/tfi-osint-n8n` (rama `main`). El repositorio contiene el informe, los anexos, los scripts de generación y las evidencias enumeradas en D.2; el tribunal puede clonarlo, inspeccionar el historial de cambios y ejecutar los scripts. El acceso se concede al tribunal mediante la invitación a la organización o el otorgamiento de permiso de lectura al repositorio, según lo acordado con la cátedra.

**Copia congelada con hash.** Para que la verificación sea independiente del estado del repositorio en el momento de la lectura, se entrega un archivo comprimido inmutable:

`V4/evidencias/informe_v5_2026-10-20/evidencia_v5.zip` — 722.230 bytes (37 archivos).

**SHA-256:** `09cdab8aaa3b41c23a6048de0ef5bfbffd4b17622807157a600ad4bea85a327f`.

El comprimido congela el código de los cuatro nodos de código, el SQL de los tres nodos de base de datos, las quince consultas de evidencia (Q1 a Q15), el artefacto del workflow, el DDL, la salida literal archivada del Capítulo 5, el paquete completo de la validación del clasificador (sorteo, hojas ciegas, adjudicación, scripts y salida) y la declaración jurada de trazabilidad entre versiones (Anexo E). Su contenido se detalla en el índice del propio archivo (`INDICE.md`). Verificación del hash:

    certutil -hashfile evidencia_v5.zip SHA256       (Windows)
    sha256sum evidencia_v5.zip                        (Linux/macOS)

El comprimido **no contiene credenciales, tokens ni la clave HMAC**; su contenido se limita a código, esquema y consultas de solo lectura.

### D.2. Inventario de la evidencia entregada

| Archivo o directorio | Contenido | Cómo se verifica |
|----|----|----|
| `evidencia_v5.zip` | Copia congelada de código, SQL, workflow, DDL y salidas | SHA-256 y tamaño en D.1; índice interno `INDICE.md` |
| `anexo_b/` | Código de los cuatro nodos, SQL de los tres nodos y Q1–Q15 en texto plano | Ejecutable sobre `tesi_osint`; validación en `consultas_q1_q15_validacion.md` |
| `Declaracion_trazabilidad_versiones.md` | Declaración jurada de trazabilidad entre versiones (Anexo E), con el inventario de resultados de V2/V3 y su origen | Original firmado en la evidencia fechada; texto transcripto en el Anexo E |
| `evidencia-muestreo/` | Sorteo (`sorteo_v5.py`), guía, hojas ciegas, adjudicación, correspondencia y salida de `analizar_v5.py` (`resultados_v5.json` / `.md`) | Recalculable con los scripts y la semilla 20261020 |
| `recalculo_cifras_v5.sql` y `recalculo_cifras_v5_resultados.txt` | Recálculo independiente de las cifras clave del informe | Consulta y salida literal |
| `correspondencia_casos_v5.csv` | Código interno ↔ `id`, URL, fecha y puntuación de los trece casos | Permite abrir cada caso citado |
| `auditoria_diccionario.md` | Auditoría completa de los 201 términos y efecto medido | Traza por término y publicación |
| `latencia_descomposicion.md` | Descomposición de la latencia y percentiles | `n`, mediana y P95 por subconjunto |
| `motor_anomalias_recalculo.md` | Recálculo del motor sobre `created_utc` | Serie diaria y disparos esperados |

Todos los archivos están fechados y ninguno contiene credenciales, tokens ni la clave HMAC. La validación del clasificador se construyó entre el 20/10/2026 y el 22/10/2026 y su salida (`resultados_v5.json`) es la fuente de la Tabla 5.8; el resto de las cifras del Capítulo 5 proviene de la salida archivada de Q1–Q15 del 19/10/2026 (5.1).

### D.3. Declaración de trazabilidad entre versiones (Anexo E)

El texto completo de la declaración se transcribe en el Anexo E; el archivo firmado es la *Declaración de trazabilidad entre versiones* (`V4/evidencias/informe_v5_2026-10-20/Declaracion_trazabilidad_versiones.md`) documenta (a) las cifras de V2/V3 no presentes en V4/V5 con su origen, (b) el ciclo de vida de los datos (B4, muestra preliminar 25–30/09, depuración, B5) y el destino de lo eliminado, y (c) que ninguna cifra del corpus B5 deriva de mediciones de V2/V3. Se conserva en la evidencia fechada con las firmas de los autores y el visado de la dirección.

    V4/   (el directorio conserva el nombre V4; V5 es la versión del documento)
    ├── anexos/
    │   ├── A_DDL.sql              — esquema físico real (Anexo A)
    │   └── B_workflow.json        — workflow desplegado (Anexo B; 17 nodos)
    ├── scripts/
    │   ├── generar_workflow.py    — genera el artefacto del workflow
    │   ├── generar_figuras_v4.py  — genera las Figuras 1 a 4
    │   └── evaluar_muestra_reproducible.py — ejecuta el nodo real sobre la muestra
    ├── figuras/                   — Figura_1 … Figura_4 (PNG)
    ├── evidencias/
    │   ├── informe_v4_2026-10-19/
    │   │   └── consultas_corpus_b5.txt     — salida de las consultas Q1 a Q15
    │   └── informe_v5_2026-10-20/
    │       ├── evidencia_v5.zip    — copia congelada (hash en D.1)
    │       ├── anexo_b/            — código de los nodos y consultas Q1 a Q15
    │       ├── evidencia-muestreo/ — sorteo, guía, hojas ciegas, adjudicación y resultados
    │       ├── Declaracion_trazabilidad_versiones.md
    │       ├── recalculo_cifras_v5.sql
    │       ├── recalculo_cifras_v5_resultados.txt
    │       ├── auditoria_diccionario.md
    │       ├── latencia_descomposicion.md
    │       ├── motor_anomalias_recalculo.md
    │       └── correspondencia_casos_v5.csv
    └── devoluciones/
        ├── tesis_v4.md            — versión previa
        ├── tesis_v5.md            — este documento
        └── tesis_v5.pdf           — versión entregable

**Reproducibilidad de las cifras.** Todas las cifras del Capítulo 5 provienen de consultas de solo lectura sobre la base `tesi_osint`, cuyo SQL se transcribe en el Anexo B.4 y cuya salida literal se conserva en `consultas_corpus_b5.txt` con fecha 19/10/2026 y corte del corpus en el inicio del 18/10/2026. Las quince consultas fijan por literales de fecha ese estado congelado, de modo que su salida es estable aunque la base crezca; esa reproducción se validó una por una contra la salida archivada (`anexo_b/consultas_q1_q15_validacion.md`). Las métricas del clasificador provienen del etiquetado consensuado de los 352 casos (3.3.2) y del cálculo reproducible de `analizar_v5.py` sobre la salida real del nodo de código del artefacto desplegado, no de una reimplementación del diccionario; su salida literal se conserva en `evidencia-muestreo/resultados_v5.json`. Las tres reglas que sostienen esa reproducibilidad: no editar a mano el workflow, regenerarlo desde su script y no escribir en la base fuera del pipeline.

## Anexo E: Declaración de trazabilidad entre versiones

### E.1. Alcance y carácter de la declaración

Esta declaración responde al requerimiento del tribunal sobre las versiones anteriores del informe y tiene carácter de **declaración jurada de los autores**. Su objeto es identificar el origen de cada resultado cuantitativo que la V2 y la V3 publicaron y que la V4 y la V5 no conservan, documentar el ciclo de vida de los datos con sus fechas y declarar si alguna cifra del informe vigente deriva de material de esas versiones.

Las versiones V1 y V2 se redactaron con asistencia de herramientas generativas de lenguaje. En ese proceso se produjeron valores numéricos que **no derivaban de una medición**: se generaron como parte del texto y no de una corrida del sistema. La V4 los retiró al reemplazar el objeto de estudio y al reconstruir el informe sobre el sistema implementado, pero no declaró su procedencia; la V5 lo hace en este anexo.

Los autores declaran, con carácter de declaración jurada:

que **ninguno** de los valores enumerados en E.2 proviene de una medición sobre el sistema entregado, sobre un corpus recolectado ni sobre un banco de pruebas;

que **no existe** base de datos, archivo de salida, registro de ejecución, respaldo ni artefacto alguno que los respalde, y que la búsqueda de ese respaldo se realizó sobre el repositorio completo y sobre la base `tesi_osint` antes de suscribir esta declaración;

que esos valores deben considerarse **sin validez empírica** y no pueden citarse como resultados del trabajo;

que **ninguna cifra de la V4 ni de la V5 deriva** de ellos, según se detalla en E.4;

que los autores asumen la responsabilidad por haber presentado esos valores sin declarar su origen en las versiones V1 a V3.

El registro de las sesiones de generación no se conservó, de modo que no es posible reconstruir qué valor provino de qué instrucción. Por esa razón el origen se declara **por bloque** —corpus, clasificación, rendimiento, operación, acuerdo y casos— y en todos los casos la declaración es la misma: valor generado, sin medición y sin respaldo. Si el tribunal identificara algún otro resultado de la V2 o de la V3 que no figure en la enumeración de E.2, queda alcanzado por esta declaración.

### E.2. Inventario de resultados y su origen

**Tabla E.1. Resultados de V2/V3 retirados y su origen**

| Bloque | Elemento | Valor declarado en la V2/V3 | Origen y respaldo |
|----|----|----|----|
| Corpus | Volumen total | 8.240 publicaciones y 42.150 comentarios recolectados entre enero y junio de 2026 (181 días) | Generado con asistencia generativa en la V1/V2. No hubo recolección en ese período: el primer registro del pipeline es del 24/09/2026 (corrida B4) y la ventana analizada comienza el 01/10/2026. Sin respaldo. |
| Corpus | Tabla 1, publicaciones por mes | 1.120 / 980 / 1.740 / 1.250 / 1.850 / 1.300 | Generado. La serie suma exactamente el total declarado, lo que indica un conjunto construido de una vez y no una agregación sobre registros. Sin respaldo. |
| Corpus | Tabla 1, comentarios por mes | 5.450 / 4.820 / 9.210 / 6.120 / 10.150 / 6.400 | Generado. Además es incompatible con la fuente: los listados RSS/Atom no exponen el árbol de comentarios (5.1). Sin respaldo. |
| Corpus | Tabla 2, aporte por subreddit | r/argentina 4.860 publicaciones y 22.350 comentarios; r/devsarg 1.540 y 11.120; r/derechogenial 1.840 y 8.680; ratios 4,60 / 7,22 / 4,71 / 5,11 | Generado. Las comunidades corresponden al alcance Plan B, abandonado el 25/09/2026 (IN-07). Sin respaldo. |
| Clasificación | Tabla 3, categorías temáticas | Estafas 2.840 (34,5 %); phishing 1.980 (24,0 %); no relevante 1.483 (18,0 %); filtración de datos 1.045 (12,7 %); vulnerabilidades 620 (7,5 %); ransomware 272 (3,3 %), sobre n = 8.240 | Generado. No existe etiquetado de 8.240 publicaciones en ninguna versión del proyecto: la única referencia etiquetada es de 352 casos (5.3). Sin respaldo. |
| Rendimiento | Tabla 4, cobertura de recolección | 84,0 % (umbral ≥ 80 %) | Generado. La cobertura se evalúa sobre la ventana real y no alcanza ese valor (Tabla 7.1). Sin respaldo. |
| Rendimiento | Tabla 4, precisión NLP | 82,0 % (umbral ≥ 80 %) | Generado. La precisión medida es 84,7 % en la validación de la V5 (Tabla 5.8) y 93,1 % en la evaluación del 30/09/2026 (5.5.1); el 82,0 % no proviene de ninguna de las dos. Sin respaldo. |
| Rendimiento | Tabla 4, recall temático | 81,0 % (umbral ≥ 80 %) | Generado. La sensibilidad medida es 61,2 % (Tabla 5.8). Sin respaldo. |
| Rendimiento | Tabla 4, F1-score | 0,815 (umbral ≥ 0,800) | Generado. El F1 medido es 0,711 (Tabla 5.8). Sin respaldo. |
| Rendimiento | Tabla 4, tasa de falsos positivos | 18,0 % (umbral ≤ 18 %) | Generado. La tasa medida es 15,3 % (Tabla 5.8). Sin respaldo. |
| Operación | Tabla 4, latencia extremo a extremo | Media 4,2 min (DE 0,5; P95 4,9) | Estimación del diseño inicial, no medida. La latencia medida tiene mediana 126,9 min y P95 1.376,2 min (Tabla 5.4). Sin respaldo. |
| Operación | Tabla 5, throughput | 1.450 publicaciones/hora en banco de pruebas (umbral ≥ 1.000) | Estimación de capacidad del diseño inicial. No existió banco de pruebas: en la V5 la capacidad se declara NO EVALUADA (Tabla 7.1). Sin respaldo. |
| Acuerdo | Kappa de Fleiss (3.3) | 0,78 con tres anotadores | Generado. No hubo etiquetado con tres anotadores antes de la validación de la V5, cuyo valor es 0,509 (Tabla 5.8). Sin respaldo. |
| Casos | Sección 5.3, caso 1 | Phishing masivo contra Mercado Pago, 14/03/2026, 42 publicaciones clasificadas | Ilustración generada. No corresponde a publicaciones registradas en la base ni a un incidente verificado por el equipo. |
| Casos | Sección 5.3, caso 2 | Ransomware a un hospital mendocino, 05/05/2026, entidad enmascarada | Ilustración generada. Ídem. |
| Casos | Sección 5.3, caso 3 | Filtración de un e-commerce nacional, 22/06/2026, score 0,94 | Ilustración generada. Ídem. |

Los valores de las Tablas 1 a 3 de la V3 son aritméticamente consistentes entre sí: las columnas suman los totales declarados y los porcentajes suman 100,0 %. Esa consistencia es propia de un conjunto construido de una sola vez y **no constituye respaldo de medición**; se deja constancia para que no se la interprete como indicio de que hubo un corpus detrás.

### E.3. Ciclo de vida de los datos

**Tabla E.2. Ciclo de vida del corpus, con fechas y destino**

| Fecha | Hecho | Destino y evidencia |
|----|----|----|
| 24/09/2026 17:42 | Corrida de prueba B4: 201 publicaciones verificadas (r/argentina 101, r/devsarg 100, r/derechogenial 0 por límite de tasa) | Prueba técnica del prototipo, fuera de la ventana. `CARACTERIZACION_RATE_LIMIT.md`; `psql_2026-09-25_caso_429_b4_derechogenial.txt` |
| 25/09/2026 | Inicio de la ventana en curso: 36 publicaciones adicionales, 237 en total | Conservadas hasta el reinicio del corpus. `ROTACION_HMAC_2026-09-26.md` |
| 25/09/2026 | Pérdida de la clave HMAC al reiniciar el motor sin la variable de entorno | Las 237 publicaciones conservan el hash de la clave anterior y no se rehashearon. `ROTACION_HMAC_2026-09-26.md` |
| 25/09/2026 | Rediseño del alcance: baja de r/argentina y r/DerechoGenial, alta de r/netsec y r/Malware | Cambio de objeto, registrado como IN-07. `VENTANA_B5.md`, sección 6 |
| 25–30/09/2026 | Muestra preliminar de 50 publicaciones etiquetada por un anotador; calibración del clasificador (MIN_HITS 2→1, retiro del término `dni`) | Conservada como evidencia y usada solo para la calibración; no es el corpus de resultados. `evaluacion_muestra_control_2026-09-30.md` y archivos asociados |
| 01/10/2026 13:05:59 | Reinicio del corpus: `TRUNCATE` de `posts`, `comments`, `anomalias` y `alertas` | Elimina las 237 publicaciones anteriores. No se generó respaldo: la base no registra publicaciones previas a esa fecha (`COUNT(*) = 0`, verificado) y el repositorio no contiene ningún volcado. `VENTANA_B5.md`, secciones 4 a 6 |
| 01/10/2026 13:15:12 – 17/10/2026 | Ventana B5: 724 publicaciones en 16 fechas (el 03/10/2026 no hubo recolección) | Corpus del informe. `ventana_b5` y Q1–Q15 del 19/10/2026 |
| 18/10/2026 | Corte del corpus al inicio del día | Estado congelado por literales de fecha en las consultas. `consultas_corpus_b5.txt` |
| Desde el 19/10/2026 | Recolección secundaria (C-25), posterior al corte | Fuera del análisis de este informe. `openspec/changes/recoleccion-secundaria/` |

### E.4. Derivación de las cifras de la V4 y de la V5

**Ninguna cifra del informe vigente deriva de material de la V2 o de la V3.** La declaración se sostiene en cuatro puntos verificables:

El corpus del Capítulo 5 son las 724 publicaciones de la ventana B5, contadas por las consultas Q1–Q15 del 19/10/2026 sobre la base `tesi_osint` y archivadas con su salida literal (5.1).

Las métricas del clasificador provienen de 352 casos etiquetados entre el 20/10/2026 y el 22/10/2026 con tres anotadores y adjudicación por consenso, y de su recálculo reproducible con `analizar_v5.py` sobre la salida real del nodo de código (5.3.2, Tabla 5.8).

La evaluación del 30/09/2026 (50 casos, un anotador) que sostiene la comparación de 5.5.1 es una medición real, conservada en `V4/evidencias/evaluacion_muestra_control_2026-09-30.md`, y no proviene de la V2 ni de la V3: su corpus es el de la muestra preliminar descrita en E.3.

Las únicas referencias a la V2 y a la V3 que subsisten en este informe son las comparaciones narrativas de 5.5.1 y de este anexo, que citan los valores para retirarlos.

### E.5. Afirmaciones de diseño de la V2 y la V3 que no se implementaron

La V2 y la V3 describieron componentes que el sistema entregado no tiene. Se declaran retirados, y su descripción no respalda ninguna cifra:

**Microservicio Python con SpaCy (**`es_core_news_lg`**)** para lematización y clasificación. La clasificación se implementa en un nodo de código JavaScript con diccionario taxonómico propio (Anexo B.2), sin dependencias de NLP externas.

**Extensión** `pg_trgm` en el modelo relacional. El esquema físico no la utiliza (Anexo A); la coincidencia es por subcadena en el nodo de código y su límite se declara en la Tabla 8.1 (IN-06).

**Motor de anomalías con ventana móvil de 7 días y umbral μ + 2σ sobre ventanas de 60 minutos.** El motor implementado aplica un umbral de Poisson sobre una ventana móvil de 11 días con piso absoluto de 3 eventos (4.5).

**«Salt dinámico»** en el hash de seudonimización. El mecanismo es HMAC-SHA-256 con clave por despliegue, sin salt (3.4).

**Cadencia de recolección cada 15 minutos.** Es la única de estas descripciones que se sostiene: está implementada y verificada sobre el artefacto desplegado (`Schedule Ingesta`, Tabla 4.1).

### E.6. Ratificación

Los autores ratifican el contenido de este anexo como declaración jurada, toman conocimiento de que el tribunal valorará su contenido conforme al reglamento vigente y dejan constancia de que la entrega de la V5 no habría sido posible sin esta rectificación expresa.

La dirección de la carrera toma conocimiento de la presente declaración.

Autores:

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Valentino Lorca

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Jerónimo Zúñiga

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Enzo Severino

Dirección:

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Prof. Alberto Cortez

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ Prof. Ariel Enferrel Mendoza, Argentina — octubre de 2026
