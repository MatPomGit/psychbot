param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $projectRoot "venv"
$pythonPath = Join-Path $venvPath "Scripts\python.exe"
$requirementsPath = Join-Path $projectRoot "requirements.txt"

if ((Test-Path -LiteralPath $venvPath) -and -not $Force) {
    Write-Host "Katalog venv już istnieje. Użyj parametru -Force, aby utworzyć go ponownie."
    Write-Host "Aktywacja środowiska: .\venv\Scripts\Activate.ps1"
    exit 0
}

if ((Test-Path -LiteralPath $venvPath) -and $Force) {
    Write-Host "Usuwam istniejący katalog venv..."
    Remove-Item -LiteralPath $venvPath -Recurse -Force
}

if (-not (Test-Path -LiteralPath $requirementsPath)) {
    throw "Nie znaleziono pliku requirements.txt w katalogu projektu."
}

Write-Host "Tworzę środowisko wirtualne w katalogu venv..."
python -m venv $venvPath

Write-Host "Aktualizuję pip..."
& $pythonPath -m pip install --upgrade pip

Write-Host "Instaluję zależności z requirements.txt..."
& $pythonPath -m pip install -r $requirementsPath

Write-Host ""
Write-Host "Gotowe. Aktywuj środowisko poleceniem:"
Write-Host ".\venv\Scripts\Activate.ps1"
