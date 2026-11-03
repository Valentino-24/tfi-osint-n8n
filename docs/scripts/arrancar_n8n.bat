@echo off
REM ============================================================
REM  Arranque de n8n del TFI. Doble clic cuando reinicies la PC.
REM  Dejalo abierto: la ventana es el proceso n8n. Ctrl+C para
REM  detener.
REM
REM  Por que existe: la clave HMAC vive en un archivo y hay que
REM  cargarla en el entorno del proceso. Las otras cuatro variables
REM  ya estan en HKCU\Environment (setx, 2026-09-26) asi que n8n las
REM  herede por cualquier via de arranque, pero las seteamos igual
REM  para que este script no dependa del registro.
REM
REM  Si arrancás n8n por otra via, n8n tiene que tener la clave en su
REM  entorno: sin ella el nodo HMAC Anonymize muere con "Falta la
REM  variable de entorno OSINT_HMAC_KEY". Y sin
REM  NODE_FUNCTION_ALLOW_BUILTIN, con "Module 'crypto' is disallowed".
REM  Ver V4\evidencias\ROTACION_HMAC_2026-09-26.md
REM ============================================================
setlocal

REM --- La clave HMAC vive FUERA del repositorio ----------------
REM     (V4\pgdata\ esta en .gitignore; el repo se pushea a GitHub)
set "KEYFILE=%USERPROFILE%\.n8n-hmac-key.txt"
if not exist "%KEYFILE%" goto :sin_clave

REM     Valida 64 hex. NO se puede hacer con findstr: su regex trata
REM     \{64\} como escapes literales y nunca matchea. Se delega a
REM     PowerShell. El -replace quita CR/LF y espacios de los extremos
REM     y es null-safe: Get-Content -Raw devuelve $null en un archivo
REM     vacio y un .Trim() ahi revienta con error.
powershell -NoProfile -Command "if ((Get-Content -LiteralPath $env:KEYFILE -Raw) -replace '^\s+|\s+$','' -match '^[0-9a-fA-F]{64}$') { exit 0 } else { exit 1 }"
if errorlevel 1 goto :clave_mal

REM     Lee la clave ya validada
for /f "usebackq delims=" %%K in (`powershell -NoProfile -Command "(Get-Content -LiteralPath $env:KEYFILE -Raw) -replace '^\s+|\s+$',''"`) do set "OSINT_HMAC_KEY=%%K"
if not defined OSINT_HMAC_KEY goto :clave_mal
goto :clave_ok

:sin_clave
echo.
echo  No encontre la clave HMAC en:
echo    %KEYFILE%
echo.
echo  Genera una con:
echo    python -c "import secrets; print(secrets.token_hex(32))"
echo.
echo  y guardala en ese archivo como una sola linea de 64 hex,
echo  sin texto alrededor. No la guardes en el repositorio.
echo.
pause
exit /b 1

:clave_mal
echo.
echo  La clave en %KEYFILE% no son 64 hex. Corregila y volve a correr.
echo.
pause
exit /b 1

:clave_ok
REM --- PostgreSQL del TFI tiene que estar arriba ----------------
"C:\Program Files\PostgreSQL\18\bin\pg_isready.exe" -h localhost -p 5433 -q || goto :sin_pg

REM --- Variables que el pipeline necesita ----------------------
REM     crypto        : habilita require('crypto') en los Code nodes
REM     env access    : deja leer $env.OSINT_HMAC_KEY desde el Code node
REM     retencion     : 30 dias de log para las consultas de evidencia
set "NODE_FUNCTION_ALLOW_BUILTIN=crypto"
set "N8N_BLOCK_ENV_ACCESS_IN_NODE=false"
set "EXECUTIONS_DATA_MAX_AGE=720"
set "EXECUTIONS_DATA_PRUNE_MAX_COUNT=5000"

where n8n >nul 2>&1 || goto :sin_n8n
echo.
echo  Iniciando n8n con la clave HMAC cargada. Dejalo abierto.
echo.
n8n start
goto :fin

:sin_pg
echo.
echo  PostgreSQL no responde en localhost:5433.
echo  Abri V4\scripts\arrancar_postgres.bat primero.
echo.
pause
exit /b 1

:sin_n8n
echo.
echo  No encuentro 'n8n' en el PATH de esta terminal.
echo  Instalalo con:  npm install -g n8n
echo.
pause
exit /b 1

:fin
endlocal
pause
