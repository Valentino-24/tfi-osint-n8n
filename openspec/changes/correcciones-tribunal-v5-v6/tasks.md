# Tasks

## 1. Preparación y trazabilidad
- [x] 1.1 Crear checklist item-por-item desde comparación V5 vs tesis_v5.md (basado en análisis previo) y verificar en V6. **Verificación:** checklist guardado en cambio con referencias sección/página/lógica.
- [x] 1.2 Copiar `docs/devoluciones/tesis_v5.md` a `docs/informe/tesis_v6.md` como base. **Verificación:** archivo existe en `docs/informe/tesis_v6.md`.

## 2. Correcciones mayores N-15, N-16, N-17, N-18, N-19
- [x] 2.1 N-15: Agregar sensibilidad por comunidad/idioma con pesos e IC, renombrar columna, reescribir 5.5/6.1/6.2/6.4/PI-2. **Verificación:** Tablas 5.9/5.9.b actualizadas, texto corregido.
- [x] 2.2 N-16: Declarar composición referencia, identificar anotador, coincidencia 50 casos, rango por anotador, unificar uso herramientas. **Verificación:** Resumen/Abstract/3.3.2/5.5/E.4 actualizados.
- [x] 2.3 N-17: Tabla régimen por día, recalcular fracción mismo intervalo, explicar evaluaciones 16/10-17/10, usar "instancia de n8n", reescribir secciones, unificar OE1. **Verificación:** Tabla 5.1.1 en 5.1 (reconstruida desde `execution_entity`), cobertura 27,9 % del tramo con registro (20,1 % de la ventana como cota inferior), descomposición de latencia en ejecución/detenida/sin registro, OE1 "cumplido con reparos" unificado en 5.8 y Tabla 7.2, propagado a Resumen, Abstract, 2.2, 6.2, 6.3, 7.3 y 7.4. Evidencia: `docs/evidencias/informe_v6_2026-11-02/regimen_operacion.py` + `regimen_operacion_salida.txt`. Pendiente derivado (a N-19): el conteo «31 al 19/10/2026» debe pasar a 41.
- [x] 2.4 N-18: Versionado código transcripto, conciliar comentarios, Anexo A aclarado/migración, cuantificar extractor/solapamientos, transcribir Parse Reddit Posts. **Verificación:** Anexo B.2 abre con identificación de versión (commit 86a1b21, 24/10/2026) y erratas de efecto nulo; Código B.0 transcribe Parse Reddit Posts; nota de conciliación 25/29 vs 24/29 y 1/21→3/21 vs 4→2; Anexo A declarado como pg_dump --schema-only del 02/11/2026 con verificación contra pg_constraint; errata `afi p` declarada con cuantificación (1 mención, 0 reconocidas); top-10 dominios publicados; auditoría de solapamientos completada (10 pares, 0 con ambos miembros). Evidencia: `docs/evidencias/informe_v6_2026-11-02/` (consultas de dominios y solapamientos).
- [x] 2.5 N-19: Atender los 16 ítems (Fig4/texto, días operación, FP, notificación, OE1, detecciones locales, modismos, índices, columnas SET, Tabla 5.14, categorías peor resueltas, registro ejecuciones, publicaciones previas rotación, cronología umbrales, Anexo E, numeración/rótulos). **Verificación:** Fig4 texto corregido; modismo «caeron»→«cayeron» en 2.2; índices (4.2) y columnas SET (4.3) corregidos; precisión por categoría añadida (5.5); Figura 3 nota 360 corridas en ventana; 3.4 corregido (237 eliminadas el 01/10, vinculables con misma clave); cronología de umbrales precisada (previo a validación V5); Anexo E: referencias IN-07/C-25 definidas, remisión 5.5.2 corregida; numeración 5.5.1/5.5.2 ordenada; 4.7 «base tesi_osint» corregido; 1.4 califica la versión del clasificador. Pendiente derivado (a N-19 menores): m-31 a m-38.

## 3. Anexo E y trazabilidad N-07
- [x] 3.1 Corregir (b) quién toma conocimiento, (c) ciclo de vida, (d) alcance V3, (e) latencia/throughput como mediciones sin serlo, (f) errores puntuales. **Verificación:** Anexo E actualizado.
- [x] 3.2 Documentar (a) firmas y entrega copia/repositorio con hash como pendientes institucionales (sin inventar). **Verificación:** Nota clara en Anexo E/Hoja de firmas.
- [x] 3.3 Verificar Tablas E.1/E.2 consistentes. **Verificación:** Sin contradicciones con cuerpo.

## 4. Correcciones V4 restantes y formales
- [x] 4.1 Atender H-01 (3.4 publicaciones previas/rotación), H-07 (reproducibilidad), H-09 (modismos 2.2), H-11 (Fig4/texto), H-12 (latencia consulta analítica), H-13/H-14/H-15 según corresponda. **Verificación:** Items cerrados o con observación justificada.
- [x] 4.2 Formales: índice multinivel (m-28), denominación trabajo (m-30), figuras (m-34), hoja firmas ubicación (m-35), tabla 5.1 suscriptores (m-36), HMAC undefined (m-37), patrón CVE (m-38), m-31-m-33. **Verificación:** Revisados.

## 5. Consistencia numérica y pasadas finales
- [x] 5.1 Verificación cruzada tablas/figuras/referencias (mismas cifras). **Verificación:** Sin contradicciones nuevas.
- [x] 5.2 Pasada N-19 completa. **Verificación:** Todos los 16 ítems marcados.
- [x] 5.3 Revisar Resumen/Abstract/Conclusiones coherentes con correcciones. **Verificación:** Coherentes.

## 6. Generación de PDF V6
- [x] 6.1 Ejecutar `python docs/scripts/convertir_pdf.py` para generar `docs/devoluciones/tesis_v6.pdf`. **Verificación:** Archivo generado.
- [x] 6.2 Ejecutar/verificar con `docs/scripts/verificar_pdf.py`. **Verificación:** Revisar resultado (10 compuertas).
- [x] 6.3 Commit atómico de cambios. **Verificación:** Commit con mensaje descriptivo.

## Workflow follow-up
- Archivar cambio con `/opsx:archive` tras revisión.
- Verificar entregable final V6.
