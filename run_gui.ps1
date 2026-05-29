$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonPath = Join-Path $projectRoot "venv\Scripts\python.exe"
$guiPath = Join-Path $projectRoot "gui.py"

if (-not (Test-Path -LiteralPath $pythonPath)) {
    Write-Host "Nie znaleziono interpretera w venv."
    Write-Host "Najpierw uruchom: .\setup_venv.ps1"
    exit 1
}

if (-not (Test-Path -LiteralPath $guiPath)) {
    throw "Nie znaleziono pliku gui.py."
}

Write-Host "Uruchamiam GUI przez lokalne środowisko venv..."
& $pythonPath $guiPath
