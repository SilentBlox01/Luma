# ==============================================================================
# Luma / Lumart Universal Installer for Windows (PowerShell)
# Compatible: Windows 10, Windows 11, Windows Server, PowerShell 5.1+ / 7+
# ==============================================================================

[CmdletBinding()]
param (
    [string]$Lang = "auto"
)

$ErrorActionPreference = "Stop"
$VERSION = "2.5.0"

# Autodetección de idioma
if ($Lang -eq "auto") {
    $culture = [System.Globalization.CultureInfo]::CurrentUICulture.TwoLetterISOLanguageName
    if ($culture -eq "es") { $Lang = "es" } else { $Lang = "en" }
}

if ($Lang -eq "es") {
    $MSG_TITLE = "Instalador Universal de Lumart v$VERSION para Windows"
    $MSG_NO_PY = "❌ Error: Python 3 no está instalado o no se encuentra en tu PATH."
    $MSG_INSTALL_PY = "Por favor instala Python 3 desde https://www.python.org/ o la Microsoft Store."
    $MSG_CHECK_PILLOW = "🔍 Verificando dependencias necesarias (Pillow)..."
    $MSG_INSTALL_PILLOW = "⚙️  Instalando Pillow con pip..."
    $MSG_COPY_ENGINE = "📦 Configurando motor Lumart en"
    $MSG_CREATE_WRAPPERS = "🔗 Creando lanzadores ejecutables (luma y lumart)..."
    $MSG_PATH_ADDED = "🔗 Directorio agregado al PATH de usuario:"
    $MSG_SUCCESS = "✅ ¡Luma v$VERSION instalado exitosamente!"
    $MSG_HINT = "Abre una nueva ventana de PowerShell o Terminal y prueba:"
} else {
    $MSG_TITLE = "Lumart v$VERSION Universal Installer for Windows"
    $MSG_NO_PY = "❌ Error: Python 3 is not installed or not in your PATH."
    $MSG_INSTALL_PY = "Please install Python 3 from https://www.python.org/ or Microsoft Store."
    $MSG_CHECK_PILLOW = "🔍 Checking required dependencies (Pillow)..."
    $MSG_INSTALL_PILLOW = "⚙️  Installing Pillow with pip..."
    $MSG_COPY_ENGINE = "📦 Setting up Lumart engine in"
    $MSG_CREATE_WRAPPERS = "🔗 Creating executable wrappers (luma and lumart)..."
    $MSG_PATH_ADDED = "🔗 Directory added to User PATH:"
    $MSG_SUCCESS = "✅ Luma v$VERSION installed successfully!"
    $MSG_HINT = "Open a new PowerShell or Terminal window and run:"
}

Write-Host ""
Write-Host " █    █ █ █▄ ▄█ ▄▀▄ █▀▄ ▀█▀" -ForegroundColor Cyan
Write-Host " █▄▄▄ ▀▄█ █ ▀ █ █▀█ █▀▄  █" -ForegroundColor Cyan
Write-Host " v$VERSION - $MSG_TITLE`n" -ForegroundColor DarkCyan

# 1. Verificar Python 3
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} else {
    Write-Host $MSG_NO_PY -ForegroundColor Red
    Write-Host $MSG_INSTALL_PY -ForegroundColor Yellow
    exit 1
}

# 2. Verificar o instalar Pillow
Write-Host $MSG_CHECK_PILLOW -ForegroundColor Cyan
$pillowCheck = & $pythonCmd -c "import PIL" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host $MSG_INSTALL_PILLOW -ForegroundColor Yellow
    & $pythonCmd -m pip install --user Pillow --quiet
}

# 3. Directorios de instalación
$shareDir = "$env:LOCALAPPDATA\Programs\Luma\share"
$binDir = "$env:LOCALAPPDATA\Programs\Luma\bin"

if (!(Test-Path $shareDir)) { New-Item -ItemType Directory -Force -Path $shareDir | Out-Null }
if (!(Test-Path $binDir)) { New-Item -ItemType Directory -Force -Path $binDir | Out-Null }

Write-Host "$MSG_COPY_ENGINE $shareDir..." -ForegroundColor Cyan

# Copiar archivos locales o descargar de GitHub
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($scriptDir -and (Test-Path "$scriptDir\lumart.py")) {
    Copy-Item "$scriptDir\lumart.py" -Destination "$shareDir\lumart.py" -Force
    if (Test-Path "$scriptDir\mary.py") {
        Copy-Item "$scriptDir\mary.py" -Destination "$shareDir\mary.py" -Force
    }
} else {
    $repoUrl = "https://raw.githubusercontent.com/SilentBlox01/Luma/main"
    Invoke-WebRequest -Uri "$repoUrl/lumart.py" -OutFile "$shareDir\lumart.py" -UseBasicParsing
    try {
        Invoke-WebRequest -Uri "$repoUrl/mary.py" -OutFile "$shareDir\mary.py" -UseBasicParsing
    } catch {}
}

# 4. Crear archivos .cmd para ejecución global
Write-Host $MSG_CREATE_WRAPPERS -ForegroundColor Cyan

$wrapperContent = @"
@echo off
"$pythonCmd" "$shareDir\lumart.py" %*
"@

Set-Content -Path "$binDir\lumart.cmd" -Value $wrapperContent -Encoding ASCII
Set-Content -Path "$binDir\luma.cmd" -Value $wrapperContent -Encoding ASCII

# 5. Agregar $binDir al PATH de usuario
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$binDir*") {
    $newPath = "$userPath;$binDir"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    $env:Path = "$env:Path;$binDir"
    Write-Host "$MSG_PATH_ADDED $binDir" -ForegroundColor Green
}

Write-Host "`n$MSG_SUCCESS" -ForegroundColor Green
Write-Host "$MSG_HINT" -ForegroundColor White
Write-Host "  luma --help" -ForegroundColor Cyan
Write-Host "  luma -v" -ForegroundColor Cyan
Write-Host "  luma /path/to/image.png" -ForegroundColor Cyan
Write-Host ""
