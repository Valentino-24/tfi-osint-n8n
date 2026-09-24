@echo off
REM Detiene PostgreSQL del TFI (cluster propio, puerto 5433)
"C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe" -D "C:\Users\valen\Desktop\Tesis\V4\pgdata" stop
pause