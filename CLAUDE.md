# TFI OSINT/n8n — Instrucciones para Agentes

> Este archivo y su copia `AGENTS.md` son la guía de entrada al repositorio.
> Se generan desde `knowledge-base/` y `CHANGES.md`. Si cambia la KB o el roadmap, regenerarlos.

## Stack tecnológico

| Capa | Tecnología | Versión / detalle |
|------|------------|-------------------|
| Orquestación | n8n | 2.22.6 |
| Persistencia | PostgreSQL | 18, cluster local en puerto 5433 |
| Base de datos | `tesi_osint` | `V4/anexos/A_DDL.sql` |
| Fuente de datos | Reddit RSS/Atom público | Feeds `new/.rss` |
| Transformación | Code nodes de n8n | Node.js, JavaScript |
| Seudonimización | Node `crypto` | HMAC-SHA-256 |
| Alertas | Telegram, opcional | Deshabilitado por defecto |
| Versionado | Git | Commits atómicos, sin atribución de IA |

Detalle completo: [knowledge-base/02_descripcion_general.md](knowledge-base/02_descripcion_general.md).

## Base de Conocimiento

La fuente de verdad del dominio vive en `knowledge-base/`. Leer el archivo relevante antes de implementar o modificar evidencia.

| Archivo | Cuándo leerlo |
|---------|---------------|
| [01_vision_y_objetivos.md](knowledge-base/01_vision_y_objetivos.md) | Propósito, alcance y límites |
| [02_descripcion_general.md](knowledge-base/02_descripcion_general.md) | Stack, arquitectura e integraciones |
| [03_actores_y_roles.md](knowledge-base/03_actores_y_roles.md) | Responsabilidades y permisos operativos |
| [04_modelo_de_datos.md](knowledge-base/04_modelo_de_datos.md) | Tablas, relaciones, constraints e índices |
| [05_reglas_de_negocio.md](knowledge-base/05_reglas_de_negocio.md) | Reglas RN del pipeline |
| [06_funcionalidades.md](knowledge-base/06_funcionalidades.md) | Historias de usuario y estado |
| [07_flujos_principales.md](knowledge-base/07_flujos_principales.md) | Flujos extremo a extremo y errores |
| [08_arquitectura_propuesta.md](knowledge-base/08_arquitectura_propuesta.md) | Patrones, estructura y seguridad |
| [09_decisiones_y_supuestos.md](knowledge-base/09_decisiones_y_supuestos.md) | Decisiones, alternativas y trade-offs |
| [10_preguntas_abiertas.md](knowledge-base/10_preguntas_abiertas.md) | Inconsistencias y decisiones pendientes |

> Resolver las preguntas de prioridad **Alta** antes de cambiar el pipeline o producir resultados.

## Skills disponibles

| Agente / rol | Skills que carga |
|--------------|-----------------|
| **Pipeline n8n** | `n8n-workflow-patterns`, `n8n-code-javascript`, `n8n-validation-expert` |
| **Infraestructura y seguridad** | `n8n-self-hosting`, `n8n-credentials-and-security-official` |
| **Ciclo de vida del workflow** | `n8n-workflow-lifecycle-official` |
| **Datos** | `postgresql-table-design` |
| **Evidencia y versionado** | `git-workflow-and-versioning` |

Cargar la skill correspondiente al contexto antes de escribir código o modificar un workflow.

> Los compact rules de cada skill los resuelve el orquestador desde `.atl/skill-registry.md` (generado por `skill-registry`; no versionado). Esta tabla solo mapea skill → rol.

## Roadmap de Changes

El plan completo está en [CHANGES.md](CHANGES.md).

- **Total**: 23 changes en 6 fases.
- **Fundación verificada**: C-01 a C-04 (B1–B4, ingesta RSS/Plan C).
- **Camino crítico pendiente**: `C-05 → C-08 → C-09 → C-20 → C-21 → C-23`.
- **Primer change**: C-05 `ventana-recoleccion-b5`.
- **Prerrequisito de latencia**: C-07 debe cerrarse antes de C-08.

Antes de cualquier `/opsx:propose`, leer `CHANGES.md`, respetar las dependencias y revisar los archivos de "Leer antes".

## Reglas duras (específicas del proyecto)

- **NUNCA** hardcodear credenciales, tokens o la clave HMAC en el workflow, el código o las evidencias → usar credenciales de n8n y variables de entorno.
- **NUNCA** editar `V4/anexos/B_workflow.json` manualmente → regenerarlo desde `V4/scripts/generar_workflow.py`.
- **NUNCA** asumir que una importación conserva credenciales → reasignar la credencial Postgres después de importar.
- **NUNCA** modificar la base ni ejecutar pruebas destructivas sin una corrida controlada → validar el workflow y verificar que el upsert siga siendo idempotente.
- **NUNCA** derivar métricas de resultados de V2/V3 o de tasas supuestas → reconstruirlas con consultas SQL sobre datos reales.
- **NUNCA** eliminar un subreddit que tenga posts → desactivarlo con `active_monitoring`.
- **NUNCA** versionar datos secretos, claves o valores de producción.
- **NUNCA** presentar una métrica de resultados sin su consulta, fecha, ventana y número de observaciones.

## Flujo de trabajo

```text
1. Leer la KB relevante y las preguntas abiertas.
2. Identificar el change y sus dependencias en CHANGES.md.
3. Crear el change con /opsx:propose.
4. Implementar las tasks con las skills correspondientes.
5. Validar el artefacto y ejecutar consultas de evidencia.
6. Archivar con /opsx:archive y marcar el change como cerrado.
```

Aplicar las reglas duras en cada paso. Ante conflicto entre la KB y este archivo, prevalecen las reglas duras.
