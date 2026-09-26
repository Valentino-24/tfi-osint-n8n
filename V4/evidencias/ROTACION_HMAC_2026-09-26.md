# Rotación de la clave HMAC — 2026-09-26

> **Estado:** ejecutado. Clave nueva generada, guardada fuera del repositorio y
> `V4/scripts/arrancar_n8n.bat` creado para que no dependa de la memoria de nadie.
> Los 237 posts existentes **no se tocaron**: conservan el hash de la clave anterior.

## Qué pasó

La clave HMAC se generó con un comando interactivo el 2026-09-25
(`GUIA_EJECUCION.md` §1, hoy reescrito) y quedó solo en la variable `$hmac` de
aquella ventana de PowerShell. Al reiniciar n8n con `n8n start` pelado el día
2026-09-25 23:26, la variable no existió más.

Consecuencia práctica: **el pipeline llevaba ~8 horas sin poder recolectar**. La
ejecución 26 (trigger de las 00:00:01) murió con `Module 'crypto' is disallowed`
— ni siquiera llegaba a pedir la clave, moría en el `require('crypto')` de la
línea 1 del Code node.

## Por qué no se recuperó

Se buscó en todos los lugares razonables y no aparece:

| Lugar | Resultado |
|---|---|
| Historial de PowerShell (`ConsoleHost_history.txt`) | no está: la línea corre de un piped `python -c` |
| Variable de entorno Usuario / Máquina | nunca se persistió con `setx` |
| Repositorio (working tree + historial git) | nunca estuvo |
| Escritorio / Documentos / `%TEMP%` | no aparece |
| `opencode.db` (memoria de agentes) | no aparece |
| Transcripts de Claude Code | no aparece |

Quedan dos vías:

1. **Probar candidatas.** Se extrajeron **72 pares de control** `(author, author_hash)`
   de la ejecución 14 (la última con la clave original) y se armó un verificador:
   ```powershell
   python "$env:LOCALAPPDATA\Temp\opencode\verifica_clave.py" <clave_de_64_hex>
   ```
   Salida `72/72` ⇒ es la clave original. Cualquier otra ⇒ `0/72`. Son 72 pares
   con autor real: **no versionarlos**.
2. **Rotar.** Es lo que se hizo.

## Qué se hizo

| | |
|---|---|
| Clave nueva | `secrets.token_hex(32)` — 64 hex, generada 2026-09-26 |
| Dónde vive | `%USERPROFILE%\.n8n-hmac-key.txt` — **fuera del repositorio** |
| Por qué ahí | el repo se pushea a GitHub; una clave en el árbol es una clave publicada |
| Cómo la lee | `V4/scripts/arrancar_n8n.bat` la carga en `OSINT_HMAC_KEY` al arrancar |
| Validación del arranque | `findstr /r "^[0-9a-fA-F]\{64\}$"` |

## Épocas de hash

La decisión de diseño (KB `09_decisiones_y_supuestos.md`) es *"HMAC-SHA-256 con
clave secreta **por despliegue**"*. Esta rotación es exactamente eso: un despliegue
nuevo. `author_hash` solo es comparable **dentro de una misma época**.

| Época | Clave | Posts | Período |
|---|---|---|---|
| 1 | la original, perdida | 237 | `2026-09-24 17:42` → `2026-09-25 16:00:05` (-03) |
| 2 | la nueva | 0 al momento de rotar | desde el primer ciclo posterior a la importación |

`posts.author_hash` **no se actualiza** en el `ON CONFLICT DO UPDATE`, así que los
237 posts de la época 1 conservan su hash original. No hubo ni habrá rehasheo.

## Qué queda afectado y qué no

**No afectado** — y es lo importante, porque son todas las métricas que usa la
evidencia de B5:

- El motor de anomalías: cuenta por `nlp_category` y ventana, nunca por autor.
- La bitácora diaria, la ventana B5, los conteos por categoría y hora.
- `RN-PS-02` (64 hex, HMAC-SHA-256): la clave nueva también la cumple.

**Afectado** — cualquier métrica que agrupe por autor cruzando la frontera:

- `count(DISTINCT author_hash)` mezcla dos dominios de hash y **empieza a
  sobreestimar autores**. Hoy hay 237 posts de **195 autores distintos**: 42 posts
  (17,7%) pertenecen a autores que ya aparecieron más de una vez. Cada uno de
  esos 42 que vuelva a publicar después de la rotación se cuenta como autor
  nuevo.
- Cualquier "autores recurrentes" o "posts por autor" sobre la ventana completa.

**Mitigación para el momento:** si alguna vez hace falta una métrica de autores,
restringirla a una sola época filtrando por `ingested_at`:

```sql
-- autores de la epoca 2 (post-rotacion)
SELECT count(DISTINCT author_hash) FROM posts
 WHERE ingested_at >= timestamptz '2026-09-26 00:00:00-03';
```

**Decisión pendiente (no implementada):** agregar una columna `hash_epoch` (o
`key_version`) a `posts` para poder separar épocas sin depender de `ingested_at`.
Es un cambio de modelo de datos → requiere pasar por el flujo de change de
OpenSpec, no se metió a mano acá.

## Pendiente operativo

- [x] Reimportar `V4/anexos/B_workflow.json` (el motor de anomalías tenía SQL roto) y **reasignar la credencial Postgres** después del import.
      → Import OK el 2026-09-26 (1 workflow, sin duplicados, `active = 0`).
      El `--userId` falla en n8n 2.22.6; importar sin ese flag.
- [ ] **Cerrar todas las ventanas de n8n y relanzar con `V4/scripts/arrancar_n8n.bat`.**
      Ver abajo: la instancia que estaba corriendo no tenía las variables.
- [ ] Reasignar la credencial Postgres en los **4** nodos (el import las borra) y activar el workflow.
- [ ] Verificar un ciclo de ingesta de 15 min con `author_hash` nuevo.
- [x] Las cuatro variables no secretas, persistidas en `HKCU\Environment` con `setx`
      (no solo en el `.bat`). La clave HMAC **no** va al registro.
- [ ] Cargar en el Anexo E9 (entorno) que la clave vive en `%USERPROFILE%\.n8n-hmac-key.txt` y **no** en el repositorio.

## Incidente: `Module 'crypto' is disallowed` (2026-09-26)

La ejecución manual `id 30` (01:02:46) falló en `HMAC Anonymize`. No era un
problema del workflow:

- El `jsCode` del nodo es **idéntico** al de la versión commiteada (`require('crypto')`),
  así que no es una regresión del arreglo del motor de anomalías.
- n8n 2.22.6 **sí** incluye `NODE_FUNCTION_ALLOW_BUILTIN` en el whitelist que le
  pasa al task runner (`dist/task-runners/task-runner-process-js.js:92`), y el runner
  lo parsea bien (`'crypto'` → `Set{'crypto'}`).

La causa real: **el proceso de n8n no tenía las variables en su entorno.** Se verificó
leyendo el bloque de entorno real del proceso (PEB → `RTL_USER_PROCESS_PARAMETERS`;
55 variables, con `SystemRoot`/`USERNAME`/`Path` presentes como control):

| Proceso | `NODE_FUNCTION_ALLOW_BUILTIN` | `N8N_BLOCK_ENV_ACCESS_IN_NODE` | `OSINT_HMAC_KEY` |
|---|---|---|---|
| n8n (PID 13500) | ausente | ausente | ausente |
| task runner (PID 4644) | ausente | ausente | ausente |

El `.bat` sí las define bien: con una copia donde se sustituyó `n8n start` por un
`node -e`, el proceso hijo leyó `ALLOW="crypto"`, `BLOCK="false"` y la clave de
64 caracteres. O sea, el script funciona; lo que no las tenía era la instancia viva.
**Un proceso no puede recibir variables después de arrancar**, así que re-ejecutar
el workflow no alcanza: hay que cerrar n8n y relanzarlo.

**Corrección de diseño:** que el pipeline dependa de que el operador se acuerde de
usar un `.bat` es frágil. Las cuatro variables no secretas se persistieron en el
entorno de Usuario con `setx`, de modo que n8n las herede por cualquier vía de
arranque. La clave HMAC quedó fuera del registro, en el archivo. Detalle en
`GUIA_EJECUCION.md` §1.

## Nota sobre el 25/9 (hueco de la ventana)

Entre las 19:15 (último ciclo con éxito) y la importación del workflow corregido,
el pipeline estuvo caído. Ese día queda como **ventana parcial** y su bitácora
daily no se puede comparar con un día completo. Está documentado en
`VENTANA_B5.md`.
