# GUÍA DE INSTALACIÓN — B1 (ENTORNO RESUELTO el 2026-09-23)

> ✅ **YA ESTÁ INSTALADO Y FUNCIONANDO.** Esto fue resuelto desde el entorno:
>
> | Componente | Estado |
> |---|---|
> | **PostgreSQL 18** (cluster PROPIO del proyecto, puerto **5433**) | ✅ Corriendo |
> | **n8n v2.22.6** (vía npm) | ✅ Instalado (falta arrancarlo y crear la cuenta) |
> | Base `tesi_osint` + rol `tesi_app` | ✅ Creados y verificados |
>
> **¿Por qué cluster propio y no el PostgreSQL del sistema?** La instalación del sistema (puerto 5432) tiene contraseña de superusuario desconocida y modificarla requiere permisos de administrador. Creé un cluster **nuevo del proyecto** (en `V4\pgdata`) que arranca como usuario normal, no toca tu instalación y queda documentado como parte del TFI. Es incluso más prolijo para la tesis.

---

## Credenciales (todas locales, para anotar)

| Dato | Valor |
|---|---|
| Host / Puerto PostgreSQL | `localhost:5433` |
| Superusuario `postgres` | password `tesi_super_2026` |
| Rol aplicación `tesi_app` | password `tesi_app_2026` |
| Base de datos | `tesi_osint` |
| n8n | http://localhost:5678 (creás cuenta local vos) |

> ⚠️ Estos passwords son de desarrollo local, se documentan en el Anexo E9 (entorno de pruebas). No son secretos de producción.

---

## Cómo arrancar y parar cada cosa

**PostgreSQL (después de reiniciar la PC):** doble clic en
`V4\scripts\arrancar_postgres.bat` — o el silencioso: `arrancar_postgres_silencioso.bat`.
Para parar: `parar_postgres.bat`.

**n8n:** abrí PowerShell y corré:
```powershell
n8n start
```
Se abre el navegador en **http://localhost:5678** → creá la cuenta de administrador local (usuario y contraseña que quieras, solo para entrar a n8n).

> 💡 Si n8n da error de `N8N_SECURE_COOKIE` o de puertos, avisame: se arregla con una variable de entorno.

---

## Verificación rápida (opcional)

```powershell
# ¿Está el cluster del proyecto? (debe decir: running, port 5433)
& "C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe" -D "C:\Users\valen\Desktop\Tesis\V4\pgdata" status

# ¿Anda la conexión con el rol de la app?
$env:PGPASSWORD = "tesi_app_2026"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -w -U tesi_app -h localhost -p 5433 -d tesi_osint -c "SELECT 1;"
```

---

## Próximos pasos (los entrego yo)

| Paso | Qué | Estado |
|---|---|---|
| **B2** | DDL real (`A_DDL.sql`) para crear tablas `posts`, `comments`, `anomalias`, `alertas` | ⏳ siguiente entrega |
| **B3** | Workflow n8n importable (`B_workflow.json`) | ⏳ siguiente entrega |
| **B4** | Correr el flujo + verificar que la base se llena | vos ejecutás, yo guío |
| **B5** | Dejarlo recolectando semanas | el sistema corre solo |
| **B6** | Evidencias E1–E15 (consultas SQL listas en PLAN_V4.md §7) | con la base poblada |

---

## Checklist de esta fase

| | Ítem |
|---|---|
| ✅ | PostgreSQL 5433 corriendo (cluster propio) |
| ✅ | n8n instalado (v2.22.6) |
| ✅ | rol `tesi_app` + base `tesi_osint` creados y verificados |
| ⏳ | n8n arrancado por vos + cuenta local creada en localhost:5678 |
| ⏳ | (B2) tablas creadas con el DDL |