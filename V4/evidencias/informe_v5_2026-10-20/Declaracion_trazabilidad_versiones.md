# Declaración de trazabilidad entre versiones

Fecha: 2026-10-20 (revisada el 2026-10-26)

Autores: Valentino Lorca, Jerónimo Zúñiga, Enzo Severino

Directores / Profesores: Prof. Alberto Cortez, Prof. Ariel Enferrel

Este documento es el original firmado de la declaración que el informe transcribe como **Anexo E**. Su contenido es idéntico al del anexo y tiene carácter de declaración jurada de los autores.

## E.1. Alcance y carácter de la declaración

La declaración identifica el origen de cada resultado cuantitativo que la V2 y la V3 publicaron y que la V4 y la V5 no conservan, documenta el ciclo de vida de los datos con sus fechas y declara si alguna cifra del informe vigente deriva de material de esas versiones.

Las versiones V1 y V2 se redactaron con asistencia de herramientas generativas de lenguaje. En ese proceso se produjeron valores numéricos que **no derivaban de una medición**: se generaron como parte del texto y no de una corrida del sistema. La V4 los retiró al reemplazar el objeto de estudio y al reconstruir el informe sobre el sistema implementado, pero no declaró su procedencia; la V5 lo hace.

Los autores declaran, con carácter de declaración jurada:

1. que **ninguno** de los valores enumerados en E.2 proviene de una medición sobre el sistema entregado, sobre un corpus recolectado ni sobre un banco de pruebas;
2. que **no existe** base de datos, archivo de salida, registro de ejecución, respaldo ni artefacto alguno que los respalde, y que la búsqueda de ese respaldo se realizó sobre el repositorio completo y sobre la base `tesi_osint` antes de suscribir esta declaración;
3. que esos valores deben considerarse **sin validez empírica** y no pueden citarse como resultados del trabajo;
4. que **ninguna cifra de la V4 ni de la V5 deriva** de ellos, según se detalla en E.4;
5. que los autores asumen la responsabilidad por haber presentado esos valores sin declarar su origen en las versiones V1 a V3.

El registro de las sesiones de generación no se conservó, de modo que no es posible reconstruir qué valor provino de qué instrucción. Por esa razón el origen se declara **por bloque** —corpus, clasificación, rendimiento, operación, acuerdo y casos— y en todos los casos la declaración es la misma: valor generado, sin medición y sin respaldo. Si el tribunal identificara algún otro resultado de la V2 o de la V3 que no figure en la enumeración de E.2, queda alcanzado por esta declaración.

## E.2. Inventario de resultados y su origen

### Tabla E.1. Resultados de V2/V3 retirados y su origen

| Bloque | Elemento | Valor declarado en la V2/V3 | Origen y respaldo |
|---|---|---|---|
| Corpus | Volumen total | 8.240 publicaciones y 42.150 comentarios recolectados entre enero y junio de 2026 (181 días) | Generado con asistencia generativa en la V1/V2. No hubo recolección en ese período: el primer registro del pipeline es del 24/09/2026 (corrida B4) y la ventana analizada comienza el 01/10/2026. Sin respaldo. |
| Corpus | Tabla 1, publicaciones por mes | 1.120 / 980 / 1.740 / 1.250 / 1.850 / 1.300 | Generado. La serie suma exactamente el total declarado, lo que indica un conjunto construido de una vez y no una agregación sobre registros. Sin respaldo. |
| Corpus | Tabla 1, comentarios por mes | 5.450 / 4.820 / 9.210 / 6.120 / 10.150 / 6.400 | Generado. Además es incompatible con la fuente: los listados RSS/Atom no exponen el árbol de comentarios (5.1 del informe). Sin respaldo. |
| Corpus | Tabla 2, aporte por subreddit | r/argentina 4.860 publicaciones y 22.350 comentarios; r/devsarg 1.540 y 11.120; r/derechogenial 1.840 y 8.680; ratios 4,60 / 7,22 / 4,71 / 5,11 | Generado. Las comunidades corresponden al alcance Plan B, abandonado el 25/09/2026 (IN-07). Sin respaldo. |
| Clasificación | Tabla 3, categorías temáticas | Estafas 2.840 (34,5 %); phishing 1.980 (24,0 %); no relevante 1.483 (18,0 %); filtración de datos 1.045 (12,7 %); vulnerabilidades 620 (7,5 %); ransomware 272 (3,3 %), sobre n = 8.240 | Generado. No existe etiquetado de 8.240 publicaciones en ninguna versión del proyecto: la única referencia etiquetada es de 352 casos (5.3 del informe). Sin respaldo. |
| Rendimiento | Tabla 4, cobertura de recolección | 84,0 % (umbral ≥ 80 %) | Generado. La cobertura se evalúa sobre la ventana real y no alcanza ese valor (Tabla 7.1 del informe). Sin respaldo. |
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

## E.3. Ciclo de vida de los datos

### Tabla E.2. Ciclo de vida del corpus, con fechas y destino

| Fecha | Hecho | Destino y evidencia |
|---|---|---|
| 24/09/2026 17:42 | Corrida de prueba B4: 201 publicaciones verificadas (r/argentina 101, r/devsarg 100, r/derechogenial 0 por límite de tasa) | Prueba técnica del prototipo, fuera de la ventana. `CARACTERIZACION_RATE_LIMIT.md`; `psql_2026-09-25_caso_429_b4_derechogenial.txt` |
| 25/09/2026 | Inicio de la ventana en curso: 36 publicaciones adicionales, 237 en total | Conservadas hasta el reinicio del corpus. `ROTACION_HMAC_2026-09-26.md` |
| 25/09/2026 | Pérdida de la clave HMAC al reiniciar el motor sin la variable de entorno | Las 237 publicaciones conservan el hash de la clave anterior y no se rehashearon. `ROTACION_HMAC_2026-09-26.md` |
| 25/09/2026 | Rediseño del alcance: baja de r/argentina y r/DerechoGenial, alta de r/netsec y r/Malware | Cambio de objeto, registrado como IN-07. `VENTANA_B5.md`, sección 6 |
| 25–30/09/2026 | Muestra preliminar de 50 publicaciones etiquetada por un anotador; calibración del clasificador (MIN_HITS 2→1, retiro del término `dni`) | Conservada como evidencia y usada solo para la calibración; no es el corpus de resultados. `evaluacion_muestra_control_2026-09-30.md` y archivos asociados |
| 01/10/2026 13:05:59 | Reinicio del corpus: `TRUNCATE` de `posts`, `comments`, `anomalias` y `alertas` | Elimina las 237 publicaciones anteriores. No se generó respaldo: la base no registra publicaciones previas a esa fecha (`COUNT(*) = 0`, verificado) y el repositorio no contiene ningún volcado. `VENTANA_B5.md`, secciones 4 a 6 |
| 01/10/2026 13:15:12 – 17/10/2026 | Ventana B5: 724 publicaciones en 16 fechas (el 03/10/2026 no hubo recolección) | Corpus del informe. `ventana_b5` y Q1–Q15 del 19/10/2026 |
| 18/10/2026 | Corte del corpus al inicio del día | Estado congelado por literales de fecha en las consultas. `consultas_corpus_b5.txt` |
| Desde el 19/10/2026 | Recolección secundaria (C-25), posterior al corte | Fuera del análisis de este informe. `openspec/changes/recoleccion-secundaria/` |

## E.4. Derivación de las cifras de la V4 y de la V5

**Ninguna cifra del informe vigente deriva de material de la V2 o de la V3.** La declaración se sostiene en cuatro puntos verificables:

1. El corpus del Capítulo 5 son las 724 publicaciones de la ventana B5, contadas por las consultas Q1–Q15 del 19/10/2026 sobre la base `tesi_osint` y archivadas con su salida literal (5.1).
2. Las métricas del clasificador provienen de 352 casos etiquetados entre el 20/10/2026 y el 22/10/2026 con tres anotadores y adjudicación por consenso, y de su recálculo reproducible con `analizar_v5.py` sobre la salida real del nodo de código (5.3.2, Tabla 5.8).
3. La evaluación del 30/09/2026 (50 casos, un anotador) que sostiene la comparación de 5.5.1 es una medición real, conservada en `V4/evidencias/evaluacion_muestra_control_2026-09-30.md`, y no proviene de la V2 ni de la V3: su corpus es el de la muestra preliminar descrita en E.3.
4. Las únicas referencias a la V2 y a la V3 que subsisten en el informe son las comparaciones narrativas de 5.5.1 y del Anexo E, que citan los valores para retirarlos.

## E.5. Afirmaciones de diseño de la V2 y la V3 que no se implementaron

La V2 y la V3 describieron componentes que el sistema entregado no tiene. Se declaran retirados, y su descripción no respalda ninguna cifra:

- **Microservicio Python con SpaCy (`es_core_news_lg`)** para lematización y clasificación. La clasificación se implementa en un nodo de código JavaScript con diccionario taxonómico propio (Anexo B.2 del informe), sin dependencias de NLP externas.
- **Extensión `pg_trgm`** en el modelo relacional. El esquema físico no la utiliza (Anexo A); la coincidencia es por subcadena en el nodo de código y su límite se declara en la Tabla 8.1 (IN-06).
- **Motor de anomalías con ventana móvil de 7 días y umbral μ + 2σ sobre ventanas de 60 minutos.** El motor implementado aplica un umbral de Poisson sobre una ventana móvil de 11 días con piso absoluto de 3 eventos (4.5).
- **«Salt dinámico»** en el hash de seudonimización. El mecanismo es HMAC-SHA-256 con clave por despliegue, sin salt (3.4).
- **Cadencia de recolección cada 15 minutos.** Es la única de estas descripciones que se sostiene: está implementada y verificada sobre el artefacto desplegado (`Schedule Ingesta`, Tabla 4.1).

## E.6. Ratificación

Los autores ratifican el contenido de este documento como declaración jurada, toman conocimiento de que el tribunal valorará su contenido conforme al reglamento vigente y dejan constancia de que la entrega de la V5 no habría sido posible sin esta rectificación expresa.

La dirección de la carrera toma conocimiento de la presente declaración.

Autores:

_________________________  **Valentino Lorca**

_________________________  **Jerónimo Zúñiga**

_________________________  **Enzo Severino**

Dirección:

_________________________  **Prof. Alberto Cortez**

_________________________  **Prof. Ariel Enferrel**

Mendoza, Argentina — octubre de 2026
