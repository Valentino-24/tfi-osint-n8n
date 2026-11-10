# Panel OSINT — prototipo

Prototipo de **capa de lectura** sobre `tesi_osint`. Muestra en el navegador
lo que la ingesta de n8n ya escribió: volumen por comunidad, distribución por
categoría, ritmo de recolección, anomalías detectadas y entidades extraídas.
La v4 agrega alertas, régimen de operación, latencia de ingesta y export CSV.

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

Python 3.11+ con `fastapi`, `pydantic`, `uvicorn` y `psycopg2-binary`. Para
correr los tests, además, `pytest`. En esta máquina ya están instalados. El
contenedor `tfi-postgres` debe estar arriba: sin él la API responde 503 en
`/api/salud` y las consultas fallan.

## Uso

```powershell
Copy-Item .env.example .env      # una sola vez; completar la contraseña
.\run.ps1                        # opcional: .\run.ps1 8100 para otro puerto
```

Si falta `.env`, `run.ps1` lo crea solo a partir de `.env.example` y avisa que
hay que completar `TFI_DB_PASSWORD` antes de que la primera consulta funcione.

Abrir <http://127.0.0.1:8000>. La documentación de la API, autogenerada por
FastAPI, queda en <http://127.0.0.1:8000/docs>.

Las cuatro versiones conviven; cada una suma endpoints, no toca los que usan
las otras:

| Ruta | Versión | Qué es |
|---|---|---|
| <http://127.0.0.1:8000/> | **v1** | Panel clásico, en un solo HTML. |
| <http://127.0.0.1:8000/v2> | **v2** | Landing por secciones, con hero, alcance activo y Metodología. |
| <http://127.0.0.1:8000/v3> | **v3** | Diseño Canva, mismo contenido con datos en vivo. Agrega suficiencia de la ventana. |
| <http://127.0.0.1:8000/v4> | **v4** | v3 + alertas de Telegram, régimen de operación, latencia y export CSV. |

La **v3** y la **v4** tienen dos temas (claro y oscuro) con un botón de sol/luna
en la barra de navegación. **Arrancan en modo claro** por defecto; el tema
elegido se guarda en `localStorage` y se aplica antes de pintar (script mínimo
en el `<head>`) para que no haya destello. Las secciones se agrupan en
**franjas** (`.band`: Resumen, Entidades y Posts) que solo cambian el *tono* de
fondo según el tema —un tinte suave en claro, el mismo tono oscuro de la página
en oscuro—, no la paleta. La franja declara `color:var(--ink)` además de
heredarlo: sin eso, los `h2`/`h3` y los números heredan el color calculado en
`body` y quedan claros sobre una franja clara (texto invisible). El color del
texto y de los paneles sale de variables CSS (`--bg`, `--surface`, `--ink`,
`--muted`, `--line`, `--accent`, `--warn`, `--band-tone`): no hay colores fijos
en el markup, así que cambiar el tema no requiere tocar los datos ni el HTML de
las secciones.

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
| `config.py` | Configuración centralizada: lee `.env` y variables de entorno (las env vars ganan) y define la zona horaria. Única fuente de host, puerto, base, usuario y contraseña. |
| `db.py` | Conexión de solo lectura, armada desde `config.py`. Una conexión por consulta, sin pool. |
| `models.py` | Schemas Pydantic de cada respuesta; son los `response_model` de la API. |
| `queries.py` | Las consultas, cada una con su SQL a la vista. |
| `app.py` | Endpoints de solo lectura y montaje de `static/` en `/static`. |
| `static/v1/index.html` | Panel v1, servido en `/`. Sin dependencias externas: los gráficos son SVG y CSS. |
| `static/v2/index.html` | Landing v2, secciones con alcance activo. |
| `static/v3/index.html` | Landing v3, diseño Canva + datos en vivo. |
| `static/v4/index.html` + `static/v4/css/styles.css` + `static/v4/js/app.js` | Landing v4 (v3 + alertas Telegram, régimen de operación, latencia y export CSV). Es la única versión con HTML, CSS y JS separados. |
| `tests/test_queries.py` | 15 tests de las consultas. Necesitan la base arriba y datos cargados. |
| `.env.example` | Plantilla de credenciales. `TFI_DB_PASSWORD` va vacía a propósito. |
| `run.ps1` | Levanta uvicorn y crea `.env` desde `.env.example` si falta. |

## Endpoints

| Ruta | Devuelve |
|---|---|
| `/api/resumen` | KPIs de cabecera |
| `/api/por-comunidad` | Volumen por subreddit |
| `/api/comunidades-estado` | Volumen por subreddit + `active_monitoring` (lo usan la v2, la v3 y la v4) |
| `/api/por-categoria` | Las 9 categorías + `No relevante` |
| `/api/serie-diaria` | Posts por día. Acepta `?categoria=` |
| `/api/anomalias` | Anomalías registradas (máximo 200, las más recientes primero) |
| `/api/alertas` | Alertas generadas por el motor de anomalías (lo usa la v4) |
| `/api/regimen` | Régimen de operación por día: publicaciones y primera/última ingesta (lo usa la v4) |
| `/api/latencia` | Latencia de ingesta en minutos, agrupada en `en_ventana` y `arrastre_inicial` (lo usa la v4) |
| `/api/entidades/{tipo}` | `products`, `cves`, `domains`, `emails`, `ips`. Un tipo inválido responde 400 |
| `/api/distribucion-score` | Score en tramos, incluida la bolsa `sin clasificar` |
| `/api/ultimos-posts` | Últimos posts ingeridos. Acepta `?limite=` (1–100), `?categoria=`, `?desde=`, `?hasta=` |
| `/api/export/csv` | Los últimos posts como CSV (`?limite=` hasta 1000, `?categoria=`). Se arma en memoria: no escribe archivos |
| `/api/suficiencia` | Días completos evaluados y estado de la ventana B5, mínimo 10 y objetivo 15 (lo usan la v3 y la v4) |
| `/api/salud` | Comprueba la conexión; 503 si la base no responde |

## Decisiones que vale la pena conocer

**La tabla `anomalias` arranca vacía y no es un bug.** La llena el nodo de
anomalías del workflow, una vez por día a las 12:05. El panel muestra un
mensaje explicando eso en vez de un cero pelado.

**Todas las fechas se fijan a `America/Argentina/Buenos_Aires` dentro del
SQL**, no en Python. Así el dato no depende de la máquina desde la que se mira.

**El panel se refresca cada 60 segundos.** Es lectura pura: no genera
evidencia nueva ni altera la que hay.

**Sin CDN ni librerías externas en la v1 y la v2.** Los gráficos son SVG
generado a mano. Esas versiones funcionan sin internet, cosa que importa si se
presenta en un aula con wifi de facultad. La **v3** y la **v4** cargan las
tipografías del diseño (DM Sans y Space Mono) desde Google Fonts: es el único
recurso externo, y sin él degradan a la fuente del sistema sin perder datos ni
funciones. La v4 además separa HTML, CSS y JS, pero sigue siendo un único
`index.html` servido por FastAPI: no hay build ni bundler.

**`score` y `num_comments` están en 0** en todos los posts. El RSS de Reddit
no los trae; es una limitación conocida, documentada como RN-FU-04.

**El ~27,9 % de instancia activa que muestra la v4 no sale de la API.** Es un
dato del informe y vive en una constante (`REGIMEN_INSTANCIA_PCT` en
`static/v4/js/app.js`): no hay tabla en `tesi_osint` que registre corridas ni
tiempo activo, y `/api/regimen` solo devuelve fecha, publicaciones y
primera/última ingesta. Está marcado así para que no se lea como dato en vivo.

## Tests

```powershell
pytest tests/ -v        # desde prototipo-landing-page/
```

Son 15 tests que golpean la base real (no hay mocks): verifican forma y
coherencia de cada consulta —que `total_posts` sea igual a `con_senal +
sin_senal`, que `por_comunidad` devuelva las tres comunidades del piloto, que
`suficiencia` devuelva un estado válido y que `distribucion_score` incluya el
tramo `0.00`. **Requieren `tfi-postgres` arriba y datos cargados**; si la base
está caída fallan los 14 que consultan y pasa solo el de validación de tipo de
entidad.

## Qué falta para convertirlo en el proyecto real

- README del proyecto, instalación y decisiones de arquitectura
- Tests contra datos con anomalías forzadas (los actuales dependen del estado real de la base)
- Paginado real en `ultimos-posts` (hoy es tope + `LIMIT`)
- Migración a otro repo con su propio versionado

## Verificación de no-escritura

Para comprobar que el rol sigue siendo de solo lectura:

```powershell
psql -U tfi_lectura -h localhost -p 5433 -d tesi_osint -c "DELETE FROM posts;"  # debe fallar
```
