# Levanta el panel de lectura. No escribe nada.
# Uso:  .\run.ps1   (opcional:  .\run.ps1 8100)

$ErrorActionPreference = "Stop"
$puerto = if ($args.Count -ge 1) { $args[0] } else { "8000" }
$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Path -LiteralPath "$raiz\.env")) {
  Write-Host "Falta .env. Creando desde .env.example..." -ForegroundColor Yellow
  Copy-Item -LiteralPath "$raiz\.env.example" -Destination "$raiz\.env"
  Write-Host "Completá TFI_DB_PASSWORD en $raiz\.env" -ForegroundColor Yellow
  Write-Host "El rol de solo lectura se crea en el README." -ForegroundColor Yellow
  Write-Host ""
}

Push-Location $raiz
Write-Host "Panel en http://127.0.0.1:$puerto" -ForegroundColor Green
Write-Host "API docs en http://127.0.0.1:$puerto/docs" -ForegroundColor Green
Write-Host "Ctrl+C para detener" -ForegroundColor DarkGray
Write-Host ""
try {
  python -m uvicorn app:app --host 127.0.0.1 --port $puerto
} finally {
  Pop-Location
}
