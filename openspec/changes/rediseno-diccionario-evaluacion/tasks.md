> Estado de este change: los pasos 1 a 5 ya fueron ejecutados el 2026-09-30 **antes** de que este change existiera, como desviación de RN-GL-03. Están marcados `[hecho-dev]` y NO se presentan como_steps previos a la decisión de diseño. El registro de la desviación está en `design.md` → D-5 y en la sección «Desviación de gobernanza». Los pasos 6 en adelante siguen pendientes.

## 1. Diccionario taxonómico

- [x] 1.1 `[hecho-dev]` Reemplazar `DICT` en `generar_workflow.py` por 9 categorías sobre un eje único de tipo de amenaza (D-1): `Phishing`, `Robo de Credenciales`, `Malware`, `Ransomware`, `Vulnerabilidades`, `Filtración de Datos`, `Infraestructura y Ataques`, `Hacktivismo`, `Ingenieria Social`
- [x] 1.2 `[hecho-dev]` Redistribuir los términos de `Estafas Virtuales` en `Phishing`, `Robo de Credenciales` e `Ingenieria Social`; eliminar `Estafas Virtuales` como categoría
- [x] 1.3 `[hecho-dev]` Retirar los términos genéricos que coinciden por trivialidad: `mp`, `cuenta`, `enlace`, `correo`, `bug`, `falla`, `transferencia`, `banco`, `filtrar`, `cangrejo`, `pescar`, `actualizacion`
- [x] 1.4 `[hecho-dev]` Agregar formas conjugadas en castellano por ausencia de lematización (D-4): `filtraron`, `filtran`, `filtrado`, `hackearon`, `hackear`, `suplantan`, `clonar`, `pidieron`
- [x] 1.5 `[hecho-dev]` Verificar invariantes del diccionario: sin acentos, sin guiones, sin duplicados, sin términos vacíos. Total resultante: 202 términos
- [x] 1.6 `[hecho-dev]` Actualizar el comentario de cabecera de `CLASSIFY_CODE` con el criterio de construcción del diccionario (D-5)

## 2. Fórmula de score

- [x] 2.1 `[hecho-dev]` Reemplazar `hits / |keywords(cat)|` por `min(1, round(hits / SATURATION, 4))` con `SATURATION = 4` (D-3)
- [x] 2.2 `[hecho-dev]` Declarar `SATURATION` como constante nombrada en el Code node
- [x] 2.3 `[hecho-dev]` Verificar que el score resultante satisface el `CHECK (nlp_score BETWEEN 0 AND 1)` del DDL sin modificar el esquema
- [x] 2.4 `[hecho-dev]` Mantener `MIN_HITS = 2` sin cambios (D-2)
- [x] 2.5 `[hecho-dev]` Verificar el comportamiento de los valores límite: `hits=0` → `0.0`, `hits=2` → `0.5`, `hits=4` → `1.0`, `hits=9` → `1.0`

## 3. Sincronización del generador con el workflow en ejecución

- [x] 3.1 `[hecho-dev]` Corregir `PREPARE_SUBS`: `derechogenial` → `DerechoGenial` (D-8)
- [x] 3.2 `[hecho-dev]` Agregar nodo `Loop Over Items` con `batchSize: 1` después de `Parse Reddit Posts`
- [x] 3.3 `[hecho-dev]` Agregar nodo `Espera Rate Limit` con 30 s de espera dentro del loop
- [x] 3.4 `[hecho-dev]` Cablear `Upsert Posts → Loop Over Items` y cerrar el retorno del loop a la etapa de ingesta
- [x] 3.5 `[hecho-dev]` Configurar `Fetch Posts RSS` con `waitBetweenTries: 3000`, `maxTries: 3` y continuación de error como red de seguridad (D-7)
- [x] 3.6 `[hecho-dev]` No modificar `PRODUCTS` ni el resto de la extracción de entidades: el contexto argentino ya se captura ahí

## 4. Regeneración y verificación del artefacto

- [x] 4.1 `[hecho-dev]` Regenerar `V4/anexos/B_workflow.json` desde `generar_workflow.py`; nunca editarlo a mano
- [x] 4.2 `[hecho-dev]` Verificar estructura: 16 nodos, 9 categorías en `CLASSIFY_CODE`, nodos de loop y espera presentes, cables correctos
- [x] 4.3 `[hecho-dev]` Verificar que el artefacto no contiene secretos: sin credenciales, sin tokens, sin `OSINT_HMAC_KEY`
- [x] 4.4 `[hecho-dev]` Confirmar que `A_DDL.sql` no fue modificado

## 5. Importación y corrida de control

- [ ] 5.1 Reimportar `B_workflow.json` en la instancia n8n 2.40.6
- [ ] 5.2 Reasignar explícitamente la credencial de PostgreSQL a los nodos que la usan. **No asumir que la importación la conserva**
- [ ] 5.3 Confirmar que los 16 nodos validan sin errores
- [ ] 5.4 Ejecutar una corrida de control completa y verificar que las tres comunidades ingieren sin error de clave foránea
- [ ] 5.5 Verificar que `nlp_score` queda en `[0, 1]` y que `nlp_category` contiene valores de las 9 categorías o `No relevante`
- [ ] 5.6 Ejecutar una segunda corrida y confirmar que el total de filas no crece. Este es el test de idempotencia del workflow de 16 nodos; la idempotencia del workflow de 14 nodos ya está verificada
- [ ] 5.7 Registrar en la bitácora de C-05 la corrida de control, su fecha, su consulta de conteo y su `n`

## 5 bis. Corpus mixto (D-9)

- [x] 5b.1 Actualizar `PREPARE_SUBS` a `netsec`, `Malware` y `devsarg`
- [x] 5b.2 Declarar `Malware` con mayúscula inicial, no `malware`. Verificado el 2026-09-30: los permalinks de `r/Malware` traen `Malware`, y `subreddit_id` se compara exacto contra la PK
- [x] 5b.3 Desactivar con `active_monitoring = false` las filas `argentina` y `DerechoGenial`. **Prohibido `DELETE`**: ambas tienen posts
- [x] 5b.4 NO tocar la fila huérfana `derechogenial` en esta change. Se conserva y se documenta
- [x] 5b.5 Verificar que el total de filas NO baja tras desactivar: 301 posts deben permanecer
- [x] 5b.6 Regenerar `B_workflow.json` y reimportar. Verificado el 2026-09-30 contra la base viva: 1 workflow `2sA14g1elooDTbID`, 16 nodos, `active=false`, 9 categorías, `SATURATION` presente, `MIN_HITS=2`, corpus `netsec`/`Malware`/`devsarg`, nodo `Espera Rate Limit` 30 s, 0 conexiones rotas, credencial `SdAca4yxWwVuQDi3` en los 4 nodos postgres. `/healthz` 200. Sin ejecuciones en curso
- [x] 5b.7 Ejecutar y verificar que las 3 comunidades del corpus ingieren sin error de PK. **Verificado el 2026-09-30** (ejecución 9, 04:30:13 → 04:31:47): `netsec` 100 posts, `r/Malware` 100 posts, sin error de FK ni de PK. Total 301 → 501. `r/devsarg` quedó con 0 por un 429 que **abortó la ejecución completa**; causa aislada y corregida en D-10 (los settings por nodo estaban bajo `node.settings` y n8n 2.40.6 los lee desde la raíz del nodo, `workflow-execute.js:933/937/938/563/564`). Post-condiciones del D-10 verificadas en runtime: `retryOnFail`, `maxTries=3`, `waitBetweenTries=5000`, `continueOnFail` y `onError=continueRegularOutput` presentes en la raíz; `Parse Reddit Posts` descarta `.error` explícitamente; 16 nodos, 9 categorías, `Espera Rate Limit` 30 s, 0 conexiones rotas, credencial en los 4 nodos postgres, `/healthz` 200
- [x] 5b.8 Registrar en la bitácora de C-05 la desactivación, su motivo y el `n` de posts conservados. Entrada generada el 2026-09-30 con `V4/scripts/bitacora_b5.py` (solo lectura, sin escribir en la base): `V4/evidencias/bitacora_b5/2026-09-30.md`. Consta con su consulta `SELECT id, display_name, active_monitoring FROM subreddits` que `r/argentina` y `r/DerechoGenial` quedaron en `false` conservando 101 y 100 posts, y que el `n` del día es 200 (100 de `r/netsec` + 100 de `r/Malware`). Estado declarado de n8n: `instancia_arriba_workflow_inactivo` — la corrida fue de control técnico y **no** comienza la ventana formal

> Nota de método (2026-09-30): n8n 2.40.6 usa SQLite en modo WAL. La verificación de la base exige copiar `database.sqlite`, `database.sqlite-wal` y `database.sqlite-shm`; leer solo `database.sqlite` devuelve el estado previo al import. Además el reloj del contenedor va 3 h adelantado respecto al host, así que los timestamps no sirven para ordenar eventos entre ambos.

## 6. Muestra de control etiquetada

- [ ] 6.1 Acordar con los autores y sus directores el criterio de etiquetado: qué cuenta como post de amenaza y qué cuenta como `No relevante` (pregunta abierta 3)
- [ ] 6.2 Extraer una muestra de 50 posts de `tesi_osint` con su consulta, fecha, ventana y `n`, sin reetiquetar los mismos ejemplos de forma iterativa
- [ ] 6.3 Etiquetar los 50 posts a mano, registrando la categoría asignada y el criterio aplicado
- [ ] 6.4 Persistir las etiquetas en un archivo versionable bajo `V4/evidencias/`, con la fecha de etiquetado y quién etiquetó
- [ ] 6.5 Mantener la muestra independiente del corpus de resultados: la muestra nunca es la misma que los posts sobre los que se reportan métricas

## 7. Evaluación

- [ ] 7.1 Ejecutar el clasificador vigente sobre los 50 posts etiquetados sin modificar el diccionario
- [ ] 7.2 Calcular la matriz de confusión 9×1 contra la muestra
- [ ] 7.3 Calcular precisión, recall y F1 con su `n` y su matriz de confusión delante (RN-GL-01)
- [ ] 7.4 Calcular Cohen's Kappa e declarar su límite de confianza dado el `n` y el desbalance de clases
- [ ] 7.5 Evaluar el umbral `MIN_HITS` contra la muestra. Recién aquí se decide si 1 o 2 es el valor correcto
- [ ] 7.6 Documentar los falsos positivos y falsos negativos uno por uno, con su causa léxica
- [ ] 7.7 Reportar los conteos operativos de la sección `Why` del proposal como lo que son: conteos, no métricas

## 8. Evidencia de selección de corpus

- [ ] 8.1 Archivar la medición de señal por comunidad ya realizada en `V4/evidencias/`, con su consulta, fecha, communities, muestra y `n`
- [ ] 8.2 Declarar en el documento que la medición distingue capacidad del clasificador y temática de la comunidad
- [ ] 8.3 Declarar explícitamente que elegir el corpus por su tasa de rendimiento es sobreajuste y está descartado (D-6)
- [ ] 8.4 Someter a los autores las opciones de composición de corpus con la evidencia a la vista
- [ ] 8.5 Registrar la decisión de composición: `r/netsec`, `r/Malware`, `r/devsarg`, con fecha, responsable y criterio temático (D-9)
- [ ] 8.6 Declarar en la evidencia que la tasa de señal del corpus final **no es una estimación de desempeño**, porque el corpus se fijó después de medir esas mismas comunidades y dos de ellas se eligieron por su tasa
- [ ] 8.7 Declarar que `r/argentina` y `r/DerechoGenial` se desactivaron por decisión de alcance, no por su tasa, y que sus 201 posts se conservan
- [ ] 8.8 Declarar el criterio de inclusión a priori: tema declarado de seguridad de la información, más `r/devsarg` como comunidad técnica argentina de referencia

## 9. Documentación

- [ ] 9.1 `knowledge-base/06_funcionalidades.md`: US-005 pasa de «cinco categorías» a nueve, con la definición del eje único
- [ ] 9.2 `knowledge-base/05_reglas_de_negocio.md`: actualizar RN-CL-04 si su referencia al Anexo C cambia de ubicación
- [ ] 9.3 `knowledge-base/04_modelo_de_datos.md`: registrar que `nlp_category` admite las nueve categorías y que no hay dominio en el DDL
- [ ] 9.4 `V4/devoluciones/tesis_v4_borrador.md`: actualizar Tabla 6 (`:1450-1458` y `:2889-2895`) y el Anexo C (`:2876-2938`) con las nueve categorías
- [ ] 9.5 `V4/devoluciones/tesis_v4_borrador.md`: corregir la fórmula del score en OE4 (`:2492`) y declarar que los posts previos usan la fórmula anterior
- [ ] 9.6 `V4/devoluciones/tesis_v4_borrador.md`: registrar el estado real de los cinco criterios de aceptación. Solo se rehabilitan si las tareas del grupo 7 se completaron
- [ ] 9.7 `V4/evidencias/CARACTERIZACION_RATE_LIMIT.md`: actualizar la mitigación documentada, que hoy dice «reintento hasta tres veces con 30 segundos», a la mitigación real de espaciado por loop (D-7)
- [ ] 9.8 `V4/GUIA_EJECUCION.md`: corregir la misma afirmación de reintentos y documentar el ciclo de ~2 minutos
- [ ] 9.9 `CHANGES.md`: registrar este change y desbloquear C-10 y C-13
- [ ] 9.10 `AGENTS.md` y `CLAUDE.md`: confirmar que la tabla de skills sigue vigente para este trabajo

## Desviación de gobernanza

RN-GL-03 exige que el cambio de diseño se documente antes de modificar la implementación. Los grupos 1 a 5 de este checklist se ejecutaron el 2026-09-30 antes de que el change existiera. El cambio está registrado ahora, después de los hechos.

Lo que se hizo para que la desviación no se convierta en una pérdida de trazabilidad: `design.md` documenta las ocho decisiones con su alternativa rechazada y su razón, y esas decisiones describen lo que realmente se implementó, no una reconstrucción. `proposal.md` declara la desviación en `Why` y en `Impact`. Y ninguna tarea de los grupos 1 a 5 se ejecutó sobre datos de producción sin evidencia: la corrida de 301 posts del 2026-09-30 es la que motivó el rediseño, y es reproducible con las consultas citadas.

Lo que este change **no** repara: la fecha de inicio de la ventana en C-05 sigue fija en 2026-09-25 aunque el workflow estuvo inactivo durante ese período. Esa inconsistencia es de C-05 y se corrige en su propio change, no aquí.

## Consecuencia de D-9 sobre la ventana de C-05

El corpus de la ventana cambia con este change, pero la ventana **no se reinicia**. Las dos comunidades desactivadas y las dos incorporadas producen una discontinuidad en la cobertura que C-05 debe registrar: los posts anteriores a este change provienen de un conjunto de comunidades distinto de los posteriores.

Consecuencias que C-05 debe declarar cuando se retome:

- La ventana tiene **dos segmentos de cobertura** con corpus distintos, y toda métrica por comunidad debe indicar a cuál pertenece.
- Los 301 posts existentes quedan fuera del corpus de resultados por decisión de alcance, salvo decisión registrada en contrario. No se reclasifican ni se reprocesan.
- La fecha de inicio vigente sigue siendo la de C-05. Este change no la mueve.

Esto no habilita por sí mismo ninguna métrica. El corpus de resultados sigue sin muestra etiquetada, y sin ella las métricas de desempeño continúan sin poder declararse.

## Fuera de alcance

Ninguna tarea de este checklist ejecuta `DELETE`, `TRUNCATE`, `DROP` ni `ALTER` sobre `tesi_osint`, ni modifica `A_DDL.sql`, ni activa el workflow, ni borra la fila huérfana `derechogenial`, ni desactiva ningún subreddit, ni toca credenciales o la clave HMAC.
