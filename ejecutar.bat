@echo off
rem Python IDE v4.0 - Lanzador para Windows (equivalente a ejecutar.sh)
set "DIR=%~dp0"
if not exist "%DIR%venv\Scripts\pythonw.exe" (
    echo No se encontro el entorno virtual de Python.
    echo Ejecuta primero el instalador: install.ps1
    pause
    exit /b 1
)
start "" "%DIR%venv\Scripts\pythonw.exe" "%DIR%python_Ide.py" %*
