
#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

echo "==============================================="
echo "          INSTALADOR DE PYTHON IDE"
echo "==============================================="

# Comprobar los requisitos del sistema.
command -v python3 >/dev/null 2>&1 || {
    echo "Error: no se encontró Python 3."
    exit 1
}

python3 -c 'import tkinter' 2>/dev/null || {
    echo "Falta Tkinter. En Debian/MX Linux ejecuta:"
    echo "sudo apt install python3-tk"
    exit 1
}

python3 -m venv --help >/dev/null 2>&1 || {
    echo "Falta el soporte para entornos virtuales."
    echo "En Debian/MX Linux ejecuta:"
    echo "sudo apt install python3-venv"
    exit 1
}

# Comprobar los archivos necesarios.
for archivo in python_Ide.py ejecutar.sh python.png requirements-ide.txt; do
    if [[ ! -f "$SCRIPT_DIR/$archivo" ]]; then
        echo "Error: falta el archivo $archivo"
        exit 1
    fi
done

chmod +x "$SCRIPT_DIR/ejecutar.sh"

# Crear el entorno propio del proyecto si no existe.
if [[ ! -x "$VENV_DIR/bin/python" ]]; then
    python3 -m venv "$VENV_DIR"
fi

# Instalar o comprobar las dependencias.
"$VENV_DIR/bin/python" -m pip install \
    -r "$SCRIPT_DIR/requirements-ide.txt"

# Detectar la carpeta Escritorio del usuario.
if command -v xdg-user-dir >/dev/null 2>&1; then
    DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
else
    DESKTOP_DIR=""
fi

if [[ -z "$DESKTOP_DIR" ]]; then
    DESKTOP_DIR="$HOME/Desktop"
fi

mkdir -p "$DESKTOP_DIR"

# Crear el acceso directo con rutas de esta instalación.
cat > "$DESKTOP_DIR/PythonIDE.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Python IDE
Comment=Iniciar Python IDE
Exec="$SCRIPT_DIR/ejecutar.sh"
Icon=$SCRIPT_DIR/python.png
Terminal=false
Categories=Development;IDE;
StartupNotify=true
EOF

chmod +x "$DESKTOP_DIR/PythonIDE.desktop"

echo
echo "Instalación terminada."
echo "Proyecto: $SCRIPT_DIR"
echo "Entorno:  $VENV_DIR"
echo "Acceso:   $DESKTOP_DIR/PythonIDE.desktop"
echo
echo "Ahora puedes iniciar la IDE desde el escritorio."
