# Panel OSINT — prototipo

Prototipo de **capa de lectura** sobre `tesi_osint`. Muestra en el navegador
lo que la ingesta de n8n ya escribió: volumen por comunidad, distribución por
categoría, ritmo de recolección, anomalías detectadas y entidades extraídas.

No es el proyecto final. Este repo (`tfi-osint-n8n`) es de documentación y
coordinación; el panel con su README definitivo va a vivir en otro repo.

## Garantía central: no puede tocar la evidencia

La protección no depende de que el código se porte bien. Depende del rol de
PostgreSQL:

```sql
CREATE ROLE tfi_lectura LOGIN PASSWORD '...';
GRANT CONNECT ON DATABASE tesi_osint TO tfi_lectura;
GRANT USAGE ON SCHEMA public TO tfi_lectura;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO tfi_lectura;
```

`tfi_lectura` no tiene permiso de escritura. Un `INSERT` o `DELETE` escrito
por error **falla en la base**, no en el código. Comprobado:

```
$ psql -U tfi_lectura -c "DELETE FROM posts WHERE id='x';"
ERROR:  permission denied for table posts
```

Además:

- La API solo expone `GET`. No hay `POST`, `PUT` ni `DELETE`.
- No importa nada de n8n, no genera el workflow, no toca `A_DDL.sql`.
- No interviene en la ventana B5 ni altera su log de ejecuciones.

## Requisitos

Python 3.11+ con `fastapi`, `uvicorn` y `psycopg2-binary`. En esta máquina ya
están instalados. El contenedor `tfi-postgres` debe estar arriba.

## Uso

```powershell
Copy-Item .env.example .env      # una sola vez; completar la contraseña
.\run.ps1
```

Abrir <http://127.0.0.1:8000>. La documentación de la API, autogenerada por
FastAPI, queda en <http://127.0.0.1:8000/docs>.

La v1 (panel clásico) vive en `/`, la **v2** (landing por secciones, con hero,
alcance activo y Metodología) en <http://127.0.0.1:8000/v2> y la **v3** (diseño
Canva, mismo contenido con datos en vivo) en <http://127.0.0.1:8000/v3>.
Conviven: cada versión agrega sus endpoints, no toca lo que usan las otras.

La **v3 tiene dos temas** (claro y oscuro) con un botón de sol/luna en la barra
de navegación. **Arranca en modo claro** por defecto; el tema elegido se guarda
en `localStorage` y se aplica antes de pintar (script mínimo en el `<head>`)
para que no haya destello. Las secciones se agrupan en **franjas** (`.band`:
Resumen, Entidades y Posts) que solo cambian el *tono* de fondo según el tema
—un tinte suave en claro, el mismo tono oscuro de la página en oscuro—, no la
paleta. La franja declara `color:var(--ink)` además de heredarlo: sin eso, los
`h2`/`h3` y los números heredan el color calculado en `body` y quedan claros
sobre una franja clara (texto invisible). El color del texto y de los paneles
sale de variables CSS (`--bg`, `--surface`, `--ink`, `--muted`, `--line`,
`--accent`, `--warn`, `--band-tone`): no hay colores fijos en el markup, así
que cambiar el tema no requiere tocar los datos ni el HTML de las secciones.

La ilustración del hero usa los **logos oficiales** de las dos herramientas:
el glifo de **n8n** (`#EA4B71`) junto a "Diseñado con n8n" y el de **Reddit**
(`#FF4500`) en su nodo, sobre una tarjeta blanca para que el trazo de línea se
lea igual que en la marca. Son SVG vectoriales embebidos (sin pedidos de red),
tomados del set abierto Simple Icons.

La contraseña va en `.env`, que está en `.gitignore` y no se versiona. También
funciona como variable de entorno, que tiene prioridad sobre el archivo:

```powershell
$env:TFI_DB_PASSWORD = "..."   # gana sobre .env
```

## Estructura

| Archivo | Qué es |
|---|---|
| `db.py` | Conexión. Lee la config de `.env`. |
| `queries.py` | Las consultas, cada una con su SQL a la vista. |
| `app.py` | Endpoints de solo lectura. |
| `static/index.html` | Panel v1. Sin dependencias externas: los gráficos son SVG y CSS. |
| `static/v2/index.html` | Landing v2, secciones con alcance activo. |
| `static/v3/index.html` | Landing v3, diseño Canva + datos en vivo. |
| `run.ps1` | Levanta uvicorn. |

## Endpoints

| Ruta | Devuelve |
|---|---|
| `/api/resumen` | KPIs de cabecera |
| `/api/por-comunidad` | Volumen por subreddit |
| `/api/comunidades-estado` | Volumen por subreddit + `active_monitoring` (lo usa la v2) |
| `/api/por-categoria` | Las 9 categorías + `No relevante` |
| `/api/serie-diaria` | Posts por día |
| `/api/anomalias` | Anomalías registradas |
| `/api/entidades/{tipo}` | `products`, `cves`, `domains`, `emails`, `ips` |
| `/api/distribucion-score` | Score en tramos |
| `/api/ultimos-posts` | Últimos posts ingeridos |
| `/api/suficiencia` | Días completos evaluados y estado de la ventana B5 (lo usa la v3) |
| `/api/salud` | Comprueba la conexión |

## Decisiones que vale la pena conocer

**La tabla `anomalias` arranca vacía y no es un bug.** La llena el nodo de
anomalías del workflow, una vez por día a las 12:05. El panel muestra un
mensaje explicando eso en vez de un cero pelado.

**Todas las fechas se fijan a `America/Argentina/Buenos_Aires` dentro del
SQL**, no en Python. Así el dato no depende de la máquina desde la que se mira.

**El panel se refresca cada 60 segundos.** Es lectura pura: no genera
evidencia nueva ni altera la que hay.

**Sin CDN ni librerías externas (v1 y v2).** Los gráficos son SVG generado a
mano. Esas versiones funcionan sin internet, cosa que importa si se presenta en
un aula con wifi de facultad. La **v3** carga las tipografías del diseño
(DM Sans y Space Mono) desde Google Fonts: es el único recurso externo, y sin
él degrada a la fuente del sistema sin perder datos ni funciones.

**`score` y `num_comments` están en 0** en todos los posts. El RSS de Reddit
no los trae; es una limitación conocida, documentada como RN-FU-04.

## Qué falta para convertirlo en el proyecto real

- README del proyecto, instalación y decisiones de arquitectura
- Tests de las consultas contra datos con anomalies forzadas
- Filtros por categoría y rango de fechas
- Exportación de evidencia (por ejemplo, CSV de lo que se muestra)
- Migración a otro repo con su propio versionado

## Verificación de no-escritura

Para comprobar que el rol sigue siendo de solo lectura:

```powershell
psql -U tfi_lectura -h localhost -p 5433 -d tesi_osint -c "DELETE FROM posts;"  # debe fallar
```
