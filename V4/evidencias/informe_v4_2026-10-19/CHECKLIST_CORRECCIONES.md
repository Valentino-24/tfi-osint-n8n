# Checklist de correcciones — trazabilidad hallazgo → sección (V4)

**Qué es este documento.** Registra, ítem por ítem, los **45 hallazgos** de las dos instancias de evaluación (identificados como `H-01…H-17`, `M-01…M-12`, `N-01…N-06`, `m-13…m-20` en `PLAN_V4.md`) y el lugar exacto del informe donde cada uno se resuelve. Cierra las tareas **1.2** y **5.2** del change `reconstruccion-informe-v4`.

**Insumos.** `PLAN_V4.md` (lista de hallazgos y fases), `CHANGES.md`, las dos devoluciones del tribunal, y el informe `V4/devoluciones/tesis_v4.md`.

**Convención de estados.**

| Estado | Significado |
|---|---|
| **RESUELTO** | El pedido se cumple con contenido verificable en la sección indicada. |
| **RESUELTO (reformulado)** | El pedido se cumple cambiando la forma pedida, y la reformulación se declara en el informe. |
| **RESUELTO por retiro** | El pedido se resuelve retirando la afirmación o la métrica que lo motivaba, con fundamento explícito. |
| **DECLARADO** | No se ejecuta, se declara como límite o como no aplicable, según lo admitía el propio auditor. |
| **RETIRADO** | El objeto del pedido no se publica en la V4 (dato o fuente de una versión anterior). |
| **VERIFICADO** | Hallazgo ya resuelto en una instancia previa; se revisó que la corrección sobreviva a la reescritura. |

**Regla aplicada en todos los casos.** Ninguna corrección se resolvió modificando un número para que cuadrara. Donde el dato no existía, la salida fue **medirlo** o **retirar la afirmación** (regla de honestidad de `PLAN_V4.md`, línea 29).

---

## 1. Hallazgos de la primera instancia (H-01 … H-17)

| ID | Hallazgo / pedido | Dónde se resuelve en `tesis_v4.md` | Estado |
|---|---|---|---|
| H-01 | Terminología de la seudonimización: «SHA-256 con *salt* dinámico» → HMAC-SHA-256 con clave secreta por despliegue | §3.4 medidas 1–3; nota de correcciones del Anexo A (`author_hash CHAR(64)`) | **RESUELTO** |
| H-01c | Verificar en la configuración de n8n el uso de `crypto` y de `$env` (`NODE_FUNCTION_ALLOW_BUILTIN`, `N8N_BLOCK_ENV_ACCESS_IN_NODE`) | §3.4 medida 2 (condiciones de configuración, agregado en la V4) | **RESUELTO** |
| H-01d | Gestión de clave (generación, custodia, rotación) y riesgo residual bajo la Ley 25.326 | §3.4 medidas 3 y 5; `ROTACION_HMAC_2026-09-26.md` | **RESUELTO** |
| H-02 | Alcance real de OE6 y coherencia del título y del Resumen con lo implementado | §1.4; §7.1 (OE6 **Parcial**); §7.2; Tabla 7.2; Resumen y Abstract | **RESUELTO** |
| H-03 | Validar los casos de 5.x contra el motor real y reportar los disparos efectivos | §5.4 (112 evaluaciones, 6 disparos, 1 legítimo); Tablas 5.5 y 5.6; §5.6 | **RESUELTO** |
| H-04 | Fórmula explícita de la tasa de falsos positivos y matriz de confusión de la muestra | §3.3.5 (`FP/(TP+FP)`, precisión, sensibilidad, F1, exactitud); §5.5 Tabla 5.7 (matriz binaria) y Tabla 5.10 (errores y desacuerdos) | **RESUELTO (reformulado)** — ver desviaciones |
| H-05 | Cobertura: protocolo de captura–recaptura o retiro de la métrica | §1.6 nota metodológica (**retirada**); §5.7; Resumen | **RESUELTO por retiro** |
| H-06 | Separar throughput operativo del techo del banco de pruebas; restituir la especificación del entorno | §4.3 «Entorno de ejecución» (agregado en la V4); §5.7; Tabla 7.1; §6.3 ítem 14 | **RESUELTO (declarado)** |
| H-07 | Tabla de recuentos reconstruida desde SQL con residual rotulado; anexos reales | §5.2 Tabla 5.3 (recuento contado, fila residual explicitada); Anexos A–D; §7.3 | **RESUELTO** |
| H-08 | CABASE y Fortinet: cita con URL y fecha, o retiro de la comparación | §6.2 reescrita sobre literatura citada y sobre el antecedente local; **ninguna de las dos se cita** en la V4 | **RESUELTO por retiro** |
| H-09 | Restituir los ejemplos de modismos que sostienen la brecha de léxico local | §2.2 (agregado: «tiraron el sitio», «caeron los servidores», «robaron mi contrasena», «tomaron control de la cuenta», «piden rescate») contrastados con el Anexo C | **RESUELTO** |
| H-10 | Contraste explícito con Dengra y Rivas (2026) y citas del marco conceptual | §2.2 (contraste en seis ejes); §2.1.3 y §2.1.4; Referencias | **RESUELTO** — spaCy: ver desviaciones |
| H-11 | Figuras reales e índices de tablas y figuras | Figuras 1–4 (§4.1, §4.2, §4.6, §5.1); índice de tablas y índice de figuras | **RESUELTO** |
| H-12 | n y medidas descriptivas por métrica (n, media, DS, P50, P95) | §3.3.5; §5.3 Tabla 5.4; §5.5; §5.7 | **RESUELTO** |
| H-13 | Regla de desempate del etiquetado y evaluador externo | §3.3.1–3.3.3; §6.3 ítems 7–10; §8.2 recomendación 1 | **DECLARADO** — un solo anotador: no hay desacuerdo que desempatar ni acuerdo calculable |
| H-14 | Índice regenerado y paginación verificada | Índice general, índice de tablas e índice de figuras (encabezado) | **RESUELTO** — la paginación se resuelve en la conversión a PDF |
| H-15 | Export real e importable del workflow (Anexo B) | Anexo B (inventario de 17 nodos); `V4/anexos/B_workflow.json` | **RESUELTO** |
| H-16 | Tabla de atributos como espejo del DDL; resolver `pg_trgm` | §4.2 Tabla 4.2 y Anexo A (5 índices; índice de texto completo retirado, `pg_trgm` justificado) | **RESUELTO** |
| H-17 | Función de puntuación y su normalización a [0,1]; diccionario completo | §4.4 (`min(1, hits/4)`); §4.4.1 (escala saturante y su justificación); Anexo C (201 términos) | **RESUELTO** |

## 2. Hallazgos de la segunda instancia (M-01 … M-12)

| ID | Hallazgo / pedido | Dónde se resuelve | Estado |
|---|---|---|---|
| M-01 | No afirmar «se superaron todos los umbrales»; Resumen y Abstract espejo | Resumen, Abstract y §5.7 (2 criterios incumplidos, 1 retirado); Tabla 7.1 | **RESUELTO** |
| M-02 | *(resuelto en V3)* revisar que la corrección sobreviva a la reescritura | Revisión cruzada del texto final | **VERIFICADO** |
| M-03 | Tamaños por estrato corregidos (no 94/111) | §5.5: muestra de 50 = censo de 28 casos marcados + 22 sorteos del estrato no relevante | **RESUELTO (reformulado)** |
| M-04 | Tablas y figuras como elementos formales con rótulo numerado | 22 tablas (1.1 … C.1) y 4 figuras, todas numeradas y citadas en el texto | **RESUELTO** |
| M-05 | Numeración de subsecciones coherente con el índice | Índice general sin entradas que no existan en el cuerpo | **RESUELTO** |
| M-06 | *(resuelto en V3)* | Revisión cruzada del texto final | **VERIFICADO** |
| M-07 | Fecha de consulta de los límites de la API de Reddit | §4.3 (espera de 60 s y valor de referencia observado); `CARACTERIZACION_RATE_LIMIT.md` (caracterización del 24 al 30/09/2026) | **RESUELTO** |
| M-08 | Suscriptores por comunidad con fecha de relevamiento | Tabla 4.2 (campo `subscribers` del esquema) | **RETIRADO** — no hay relevamiento fechado que los respalde: no se informan |
| M-09 | Numeración de Referencias y Anexos conforme al reglamento | Referencias (15 entradas, APA 7) y Anexos A–D | **RESUELTO** |
| M-10 | *(resuelto en V3)* | Revisión cruzada del texto final | **VERIFICADO** |
| M-11 | *(resuelto en V3)* | Revisión cruzada del texto final | **VERIFICADO** |
| M-12 | Declaración de autoría visible desde el índice | Bloque inicial «Declaración de autoría y de uso de herramientas de asistencia», referenciado en el índice general | **RESUELTO** |

## 3. Hallazgos menores (m-13 … m-20)

| ID | Hallazgo / pedido | Dónde se resuelve | Estado |
|---|---|---|---|
| m-13 | Redondeos de las cifras de la versión previa (4,72 y 5,12, no 4,71 y 5,11) | — | **RETIRADO** — las cifras de la V2 (8.680 / 1.840 / 42.150 / 8.240) no se publican en la V4 |
| m-14 | Uso correcto de Liao et al. (2016): extracción de IoC, no reconocimiento activo | §2.2 (antecedente directo de normalización y filtrado de IoC) | **RESUELTO** |
| m-15 | Separador decimal consistente | Verificación automatizada sobre el documento completo (76,52 %; 6,9 %; 0,931) | **RESUELTO** |
| m-16 | Justificar `r/derechogenial` y su efecto sobre el corpus | §6.3 ítem 8 (comunidad desactivada; efecto sobre la muestra declarado) | **RESUELTO por retiro** |
| m-17 | Declaración de autoría precisa: herramientas generativas y usos | Bloque inicial, línea 14 del informe | **RESUELTO** |
| m-18 | Mostrar la sentencia de persistencia que garantiza la idempotencia | §4.3 punto 7 (`INSERT … ON CONFLICT (id) DO UPDATE`, con los campos que sobreescribe) | **RESUELTO** |
| m-19 | Política de enmascaramiento extendida a atributos indirectos | §3.4 medida 5 (reidentificación indirecta por contenido) | **RESUELTO** |
| m-20 | `ON DELETE CASCADE` → `RESTRICT` en `posts → subreddits`, con `active_monitoring` | §4.2 y Anexo A | **RESUELTO** |

## 4. Hallazgos transversales (N-01 … N-06)

| ID | Hallazgo / pedido | Dónde se resuelve | Estado |
|---|---|---|---|
| N-01 | Latencia y cadencia: revisar el criterio contra el *scheduler* y medir | §3.2 y §4.3 (ciclo de 15 min); §5.3 (medición real, n = 724 y n = 437); §1.6 y Tabla 7.1 (**no cumplido**, sin mover el umbral) | **RESUELTO** |
| N-02 | Recuentos contados y no derivados; comparación con la literatura sobre amenazas reales | §5.2 Tabla 5.3 (recuento contado y residual explicitado); §5.1 (composición del corpus); §6.1–6.2 (interpretación sobre tasas corregidas) | **RESUELTO** |
| N-03 | Construir sobre la base textual de la V2, restituir extensión y contenido valorado | Estructura completa del informe; arquitectura en §4.1; tabla de atributos en §4.2; priorización de recomendaciones en §8.1 | **RESUELTO** |
| N-04 | Formalizar el motor de anomalías (variable, ventana, base, umbral) y justificar el umbral | §4.5 (base por media de 10 días, ventana móvil de 11, cuantil 95 de Poisson + 1, mínimo absoluto 3); §4.5 corrección de la fórmula; §5.4 | **RESUELTO** |
| N-05 | Umbrales a priori, F1 propio, fin de la redundancia precisión/FP, intervalos de confianza | §1.6 y Tabla 1.1, con las tres notas metodológicas (cobertura retirada, F1 incorporado, cambio de umbral 82/18 → 80/20 declarado y justificado); IC exactos en §5.5 y Tabla 5.8 | **RESUELTO** |
| N-06 | DDL completo (`score`, entidades, anomalías, alertas, latencias) y descripción de la extracción de entidades | §4.2 y Anexo A (5 tablas, 5 índices, restricciones); §4.4 (extracción de CVE, correos, IPv4, dominios y productos, tope de 20 por publicación) | **RESUELTO** |

---

## 5. Desviaciones declaradas

1. **Matriz de confusión (H-04).** Se solicitaba una matriz 6×6 —o una matriz completa por categoría— de la muestra de control. La V4 informa una **matriz binaria** (Tabla 5.7) más dos medidas que el diseño de 50 filas sí sostiene: la **exactitud de categoría** (42/50 = 84,0 %, definida en §3.3.5 como coincidencia exacta de la categoría asignada, incluida «No relevante») y el **detalle ítem por ítem de errores y desacuerdos** (Tabla 5.10). Motivo: con 50 observaciones repartidas en 9 categorías, las celdas de una matriz completa quedarían en 0 o 1 y no estimarían ninguna proporción; presentarlas como una matriz sugeriría una precisión que el dato no tiene. El detalle por ítem que respalda esas dos medidas —las listas de falsos positivos, falsos negativos y aciertos con categoría distinta— está archivado en `V4/evidencias/evaluacion_muestra_control_2026-09-30.md` (§2, §5.b y §6) y en la hoja de etiquetas `muestra_control_50_2026-09-30_ETIQUETAS.csv`, con `categoria_humana`, anotador y criterio aplicado por fila.
2. **Lista de referencias (H-10).** El plan pedía «17 o más» fuentes. La V4 cierra con **15 entradas, todas citadas** en el texto. Se descartaron Honnibal et al. (spaCy) y Stallings por haber quedado sin cita tras reescribir las secciones que los invocaban: el criterio aplicado fue que ninguna referencia huérfana permaneciera, y ninguna cita quedara sin referencia.
3. **Extensión (N-03).** El cuerpo del informe quedó en **20.364 palabras de prosa** (21.042 contando portada, índices y siglas), equivalentes a **≈ 51 páginas** a 400 palabras por página. El diseño del change fijaba 16.000–19.000 palabras (42–48 páginas), de modo que la entrega queda **≈ 7 % por encima del techo autoimpuesto**. **El exceso es relativo al presupuesto que nos fijamos, no al requisito del tribunal**: la V2 tenía 34 páginas y lo que se exigió fue "recuperar al menos la extensión y el nivel de detalle" de esa versión, de modo que la V4 lo supera con margen —que es el lado seguro del error—. La causa no es relleno: son las correcciones que las dos evaluaciones exigieron y que se agregaron después del control de presupuesto —el entorno de ejecución de H-06, los ejemplos de modismos de H-09, las condiciones de configuración de H-01c, la nota de cambio de umbrales de N-05, la priorización por esfuerzo e impacto de N-03 en el Capítulo 8 y la explicación del residual en el Capítulo 5—. **Decisión tomada: no recortar.** El tribunal reprobó la versión anterior precisamente por resolver las correcciones **borrando contenido** (24 páginas frente a las 34 de la V2), y el riesgo de tres páginas de más es menor que el de repetir ese error. Si el reglamento impusiera un máximo, los recortes candidatos —sin tocar el Capítulo 4, que es el núcleo de la evaluación— son el Capítulo 5 (repetición de cifras ya tabuladas) y el Capítulo 2 (listado de herramientas OSINT).
4. **Título (H-02).** El título se mantiene en «detección de tendencias y alertas» porque el sistema **detecta y registra** alertas, y el Informe declara explícitamente que la notificación externa no está probada (OE6 **Parcial**). No se afirma que el sistema alerte a un destinatario.
5. **Entorno de pruebas (H-06).** Se documenta el entorno real (dos contenedores sobre un solo equipo, sin aislamiento de recursos ni hardware dedicado) pero **no** se caracterizaron CPU, memoria ni entrada/salida: se declara como limitación en §6.3 ítem 14 en lugar de estimarla.
6. **Suscriptores (M-08).** No se informan suscriptores por comunidad: no existe un relevamiento con fecha que los respalde. El campo permanece en el esquema como columna de la tabla `subreddits`.

## 6. Cierre y pendientes

- **Tarea 5.8 — cumplida el 2026-10-19.** Los autores ratificaron que latencia y throughput **no se cumplieron** y que eso queda publicado así (§1.6, §5.7, Tabla 7.1 y Resumen). Con esa confirmación se registró el change en `CHANGES.md` como **`[C-26] reconstruccion-informe-v4`** (`[~]` parcial), que **absorbe** `C-16`, `C-17` y `C-18`…`C-23` — los ocho compartían entregable y se ejecutaron en una sola sesión. Queda un único paso administrativo: archivarlo con `/opsx:archive`.
- **Efecto sobre el roadmap que conviene revisar antes de retomar los changes de evidencia.** Las evidencias consolidadas que `C-08`, `C-09`, `C-10` y `C-13` iban a producir ya existen dentro de `V4/devoluciones/tesis_v4.md` (Capítulo 5) y de esta carpeta de evidencias. Antes de ejecutarlos hay que comprobar qué falta realmente: es posible que queden sin objeto o reducidos a formalizar lo ya hecho.
- **Decisiones que no dependen del equipo:** ninguna. Las tres decisiones abiertas del informe quedaron resueltas (cobertura retirada, OE6 parcial declarado, incumplimiento de latencia y throughput publicado).

## 7. Conversión a PDF y verificación de los índices

El PDF de entrega (`V4/devoluciones/tesis_v4.pdf`, **74 páginas A4**) se generó el **2026-10-19** con `V4/scripts/convertir_pdf.py` a partir de `V4/devoluciones/tesis_v4.md` (pandoc 3.8 → DOCX intermedio → Word 16.0 por COM → PDF). **El Markdown entregable no se modificó**: los ajustes se aplican sobre una copia de trabajo en `V4/devoluciones/build/`.

- **Índices:** **36 entradas** (10 del índice general, 22 de tablas, 4 de figuras) con número de página. Cada número se verificó de forma independiente contra el PDF (`valida_indices_final2.py`): **36 correctas, 0 desfases**. La numeración converge en **dos pasadas** (la segunda no introdujo cambios).
- **Rótulos:** **0 rótulos ausentes** del PDF (22 tablas y 4 figuras declaradas en el Markdown), **4 imágenes embebidas** y **0 páginas en blanco**.
- **Diseño de portada e índices (ajuste del 2026-10-19).**
  - **Portada:** queda en la página 1 **solo** con los datos del trabajo (título, institución, carrera, tipo de trabajo, autores, directores y «Mendoza, Argentina — 2026»), centrados y con aire repartido entre bloques (título 16 pt con 36 pt después, «Trabajo Final…» con 24 pt antes, autores/directores con 36 pt antes, lugar con 48 pt antes). Las dos notas —«Versión del documento (V4)» y «Declaración de autoría y de uso de herramientas de asistencia»— se movieron a la **página 2** con un salto de página. La declaración de autoría **no se elimina**: sigue presente en el documento, en la página siguiente.
  - **Índices:** rediseñados con el estilo de `tesis_v2`. Cada entrada es un renglón compacto (11 pt, interlineado simple, 3 pt después) con **puntos guía hasta el margen derecho** y la **página alineada a la derecha** (tabulación derecha en 453,6 pt con relleno de puntos). Los capítulos van en **MAYÚSCULAS y negrita** con el número reescrito como texto (`1. Introducción`, … `10. Anexos`); las entradas de tablas y figuras llevan sangría de 12 pt. Los encabezados de los tres índices van en mayúsculas.
  - **Defecto corregido:** pandoc numeraba las entradas del índice general como lista; en el DOCX el glifo vive en `numbering.xml` colgado del estilo `Compact`, y Word lo escribía **antes** del texto y lo empujaba al margen con la tabulación, produciendo `1…… I` + `ntroducción …… 10`. Se corrigió en la copia de trabajo: `preparar_markdown` convierte las entradas del índice general en párrafos planos y `normalizar_indices` quita el `<w:numPr>` del DOCX; el número se reescribe con `_numerar_texto_parrafo` sin fusionar párrafos vecinos.
- **Ajustes de formato necesarios para la conversión:** i) las reglas horizontales del Markdown (`---`, 7 en total) se descartan en la copia de trabajo porque pandoc las convierte en marcos VML que Word reporta como párrafos y generan una página en blanco; ii) el guionado automático se desactiva en la portada y en los títulos (el título se cortaba en «ME- / DIANTE»); el cuerpo justificado conserva el guionado; iii) las notas de portada que pandoc inserta como *footnotes* se reducen a la nota del bloque inicial (`separar_notas`), porque el texto completo ya figura como cuerpo en la página 2.
- **Observación (sin acción):** en varias tablas la entrada del índice es una versión abreviada del rótulo real (p. ej. `Tabla 5.9` en el índice frente al rótulo «Efecto de la corrección del clasificador (misma muestra, mismo texto)»). Es una característica del documento de origen y **no** un defecto de la conversión; por eso no se tocó el Markdown. La única diferencia de texto entre índice y cuerpo es `A_DDL.sql`, marca de código en la tabla de atributos.
- **Espaciado entre bloques (ajuste del 2026-10-19, posterior a la primera verificación).** En el primer PDF el primer renglón posterior a cada tabla arrancaba a **1–3 pt** del borde inferior, medido con el perfil de tinta del PDF renderizado a 1 px = 1 pt (`diag_tabla_texto.py`, método reproducible: una regla de tabla es una fila con ≥ 350 px oscuros). Word **no admite** espacio después de una tabla, así que el aire se aplica en el párrafo siguiente (`SpaceBefore = 12`) y en el anterior (`SpaceAfter = 4` si es rótulo, `10` si es texto): función `espaciado_bloques`, **22 tablas**, borde final ahora a **14–15 pt**. Se normalizaron además las brechas entre bloques: cuerpo **8 pt** (antes 6), listas e índices **6 pt**, rótulo→tabla **4 pt**, títulos 18/14/12 pt antes y 12/8/6 después (antes 18/12/10 y 12/6/4), lo que elimina la mezcla de 6/16/18/24 pt de la versión previa.
- **Figura 2 (ajuste del 2026-10-19).** El layout del diagrama entidad-relación se recalculó (`V4/scripts/generar_figuras_v4.py`, `figura_2`): con `ylim=(0,112)` y geometría fija (`ALTO_CABECERA=6.0`, `ALTO_FILA=4.4`), columnas A (`subreddits`/`comments`), B (`posts`/`anomalias`) y C (`alertas`), 3 flechas 1:N y notas al pie. Se verificó con las cajas reales del renderer de matplotlib (`verif_fig2.py`): **5 tablas, 76 textos, 0 solapamientos**. El título interno se conserva porque duplica el epígrafe del PDF (característica del documento).

*Documento generado el 2026-10-19 para el change `reconstruccion-informe-v4`. Las referencias `§` corresponden a `V4/devoluciones/tesis_v4.md`.*


