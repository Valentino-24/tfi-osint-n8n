@echo off
REM ============================================================
REM  Arranque de PostgreSQL del TFI (cluster propio, puerto 5433)
REM  Doble clic cuando reinicies la PC. Cierra con parar_postgres.bat
REM ============================================================
"C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe" -D "C:\Users\valen\Desktop\Tesis\V4\pgdata" -o "-p 5433" -l "C:\Users\valen\Desktop\Tesis\V4\pgdata\server.log" start
pause