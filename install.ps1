# install.ps1 - Instalador de Python IDE v4.0 para Windows
# Equivalente al install.sh de Linux: comprueba Python, lo instala
# con winget si falta, crea el venv (recrea si está incompleto),
# instala las dependencias y crea el acceso directo.

$ErrorActionPreference = "Stop"

$ProjectDir = $PSScriptRoot
$VenvDir = Join-Path $ProjectDir "venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$VenvPythonW = Join-Path $VenvDir "Scripts\pythonw.exe"

Write-Host "==============================================="
Write-Host "          INSTALADOR DE PYTHON IDE v4.0"
Write-Host "                 (Windows)"
Write-Host "==============================================="

# Buscar un Python real. El "python" de la Microsoft Store es un
# atajo falso: se detecta porque vive en WindowsApps y no ejecuta.
function Find-Python {
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) {
        & py -3 -c "import sys" 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            return @{ Exe = "py"; PreArgs = @("-3") }
        }
    }

    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source -notlike "*WindowsApps*") {
        & python -c "import sys" 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            return @{ Exe = $cmd.Source; PreArgs = @() }
        }
    }

    $bases = @(
        (Join-Path $env:LOCALAPPDATA "Programs\Python"),
        $env:ProgramFiles,
        ${env:ProgramFiles(x86)}
    )
    foreach ($base in $bases) {
        if (-not $base) { continue }
        $found = Get-ChildItem -Path $base -Filter "Python3*" -Directory -ErrorAction SilentlyContinue |
            ForEach-Object { Join-Path $_.FullName "python.exe" } |
            Where-Object { Test-Path $_ } |
            Select-Object -First 1
        if ($found) {
            return @{ Exe = $found; PreArgs = @() }
        }
    }
    return $null
}

$python = Find-Python

# Sin Python, instalarlo con winget (el propio instalador, como en Linux).
if (-not $python) {
    Write-Host "No se encontro Python. Instalando con winget..."
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) {
        Write-Host "Error: no hay Python ni winget en este equipo."
        Write-Host "Instala Python desde https://www.python.org/downloads/"
        Write-Host "y vuelve a ejecutar este instalador."
        exit 1
    }
    winget install -e --id Python.Python.3.13 --scope user --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: winget no pudo instalar Python."
        exit 1
    }
    # Refrescar el PATH de esta sesion con el del registro.
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
                [Environment]::GetEnvironmentVariable("Path", "User")
    $python = Find-Python
    if (-not $python) {
        Write-Host "Python quedo instalado, pero esta sesion no lo ve aun."
        Write-Host "Cierra esta ventana de PowerShell, abre otra y repite .\install.ps1"
        exit 1
    }
}

# Tkinter viene con el Python de python.org; comprobarlo.
& $python.Exe @($python.PreArgs) -c "import tkinter" 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: este Python no trae Tkinter."
    Write-Host "Reinstala Python desde https://www.python.org/downloads/"
    exit 1
}

# Comprobar los archivos necesarios.
foreach ($archivo in @("python_Ide.py", "ejecutar.bat", "python.png", "requirements-ide.txt")) {
    if (-not (Test-Path (Join-Path $ProjectDir $archivo))) {
        Write-Host "Error: falta el archivo $archivo"
        exit 1
    }
}

# El entorno solo es valido si tiene Activate y un pip que responde.
# Uno a medias (python sin pip) se borra y se recrea, nunca se reutiliza.
function Test-VenvSano {
    if (-not (Test-Path $VenvPython)) { return $false }
    if (-not (Test-Path (Join-Path $VenvDir "Scripts\Activate.ps1"))) { return $false }
    & $VenvPython -m pip --version 2>$null | Out-Null
    return ($LASTEXITCODE -eq 0)
}

if ((Test-Path $VenvDir) -and -not (Test-VenvSano)) {
    Write-Host "Entorno virtual incompleto detectado: se recrea desde cero."
    Remove-Item $VenvDir -Recurse -Force
}

if (-not (Test-Path $VenvDir)) {
    & $python.Exe @($python.PreArgs) -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: no se pudo crear el entorno virtual."
        exit 1
    }
}

if (-not (Test-VenvSano)) {
    Write-Host "Error: el entorno virtual quedo sin pip utilizable."
    exit 1
}

# Instalar o comprobar las dependencias.
& $VenvPython -m pip install -r (Join-Path $ProjectDir "requirements-ide.txt")
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: no se pudieron instalar las dependencias."
    exit 1
}

# Crear el acceso directo en el Escritorio.
$DesktopDir = [Environment]::GetFolderPath("Desktop")
$lnkPath = Join-Path $DesktopDir "PythonIDE.lnk"
$shell = New-Object -ComObject WScript.Shell
$lnk = $shell.CreateShortcut($lnkPath)
$lnk.TargetPath = $VenvPythonW
$lnk.Arguments = '"' + (Join-Path $ProjectDir "python_Ide.py") + '"'
$lnk.WorkingDirectory = $ProjectDir
$lnk.IconLocation = "$VenvPython,0"
$lnk.Save()

Write-Host ""
Write-Host "Instalacion terminada."
Write-Host "Proyecto: $ProjectDir"
Write-Host "Entorno:  $VenvDir"
Write-Host "Acceso:   $lnkPath"
Write-Host ""
Write-Host "Ahora puedes iniciar la IDE desde el escritorio o con ejecutar.bat."
