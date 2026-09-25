# Descripción General

## Stack tecnológico

| Capa | Tecnología | Versión / detalle |
|---|---|---|
| Orquestación | n8n | 2.22.6 |
| Persistencia | PostgreSQL | 18, cluster local en puerto 5433 |
| Base de datos | `tesi_osint` | Esquema definido en `V4/anexos/A_DDL.sql` |
| Fuente de datos | Reddit RSS/Atom público | Feeds `/r/{subreddit}/new/.rss` |
| Clasificación | Nodos Code de n8n | Diccionario taxonómico y score `[0,1]` |
| Seudonimización | Node `crypto` | HMAC-SHA-256 |
| Entidades | Nodos Code / JSONB | CVE, emails, IPs, dominios y productos |
| Alertas | Telegram opcional | Nodo deshabilitado por defecto |
| Versionado | Git | Repositorio local con remoto configurado |
| Configuración de workflow | JSON importable | `V4/anexos/B_workflow.json` |

## Arquitectura general

```text
Feeds RSS públicos de Reddit
            |
            v
  n8n Schedule (cada 15 min)
            |
            v
  RSS Read -> Parse -> HMAC -> Clasificar
            |                    |
            |                    +-> Extraer entidades
            v
  Upsert idempotente en PostgreSQL (subreddits, posts)

  n8n Schedule diario (00:05)
            |
            v
  Conteos por categoría + base histórica
            |
            v
  Umbral Poisson + mínimo absoluto -> anomalias -> alertas
            |
            v
       Telegram (opcional)
```

El sistema es un pipeline por lotes, no una aplicación web con API propia. La fuente de verdad de la clasificación y de la persistencia es el workflow exportable junto con el DDL.

## Integraciones externas

| Servicio | Propósito | Tipo | Estado |
|---|---|---|---|
| Reddit RSS/Atom | Obtener publicaciones públicas | Feed HTTP público | Operativo con rate limit |
| Reddit OAuth/API | Obtener campos adicionales | REST | No disponible; requiere developer account |
| PostgreSQL | Persistencia y consultas de evidencia | SQL | Operativo en puerto 5433 |
| Telegram | Notificación de alertas | Bot API | Opcional, no habilitado |

## API REST

No existe una API REST propia. Las consultas de evidencia se realizan directamente con `psql` o clientes SQL sobre `tesi_osint`. El acceso operativo a n8n es su interfaz web local.

## Estado de implementación

- B1: entorno instalado y verificado.
- B2: DDL ejecutado; las cinco tablas existen.
- B3: workflow generado e importado; las credenciales deben reasignarse después de cada importación.
- B4: verificado con ingesta RSS real; en la última corrida registrada había 201 posts (`r/argentina`: 101, `r/devsarg`: 100, `r/derechogenial`: 0 por rate limit) y un post clasificado como phishing.
- B5: la ventana de recolección real quedó **definida y abierta**: inicio **2026-09-25**, corte **`no fijada`** (decisión pendiente de los autores con sus directores, tarea 6.1 de C-05). El corpus se define sobre `posts.ingested_at`; los 201 posts de B4 (2026-09-24) quedan fuera del corpus salvo decisión de los autores. Bitácora diaria en `V4/evidencias/bitacora_b5/` generada por `V4/scripts/bitacora_b5.py` (solo lectura). El cierre sigue pendiente con los autores.
- B6: las evidencias E1–E15 se producirán a partir de la base y de las corridas reales.
