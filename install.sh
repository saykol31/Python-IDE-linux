#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

echo "==============================================="
echo "          INSTALADOR DE PYTHON IDE"
echo "==============================================="

# Comprobar Python 3.
command -v python3 >/dev/null 2>&1 || {
    echo "Error: no se encontró Python 3."
    exit 1
}

# Comprobar las dependencias del sistema y, si falta alguna,
# instalarla aquí mismo (solo pedirá la contraseña de sudo).
faltan=()
python3 -c 'import tkinter' 2>/dev/null || faltan+=("python3-tk")
python3 -c 'import ensurepip' 2>/dev/null || faltan+=("python3-venv")

if (( ${#faltan[@]} > 0 )); then
    echo "Faltan paquetes del sistema: ${faltan[*]}"
    echo "Instalándolos ahora (puede pedir tu contraseña)..."
    sudo apt-get install -y "${faltan[@]}" || {
        sudo apt-get update && sudo apt-get install -y "${faltan[@]}"
    } || {
        echo "Error: no se pudieron instalar: ${faltan[*]}"
        exit 1
    }
fi

# Reverificar: sin Tkinter o sin ensurepip no se puede seguir.
python3 -c 'import tkinter' 2>/dev/null || {
    echo "Error: sigue faltando Tkinter (python3-tk)."
    exit 1
}
python3 -c 'import ensurepip' 2>/dev/null || {
    echo "Error: sigue faltando el soporte de entornos virtuales (python3-venv)."
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
chmod +x "$SCRIPT_DIR/activar_venv.sh" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/StartPy.sh" 2>/dev/null || true

# El entorno solo es válido si tiene activate y un pip que responde.
# Una creación interrumpida deja un venv a medias (python sin pip):
# ese se borra y se recrea, nunca se reutiliza.
venv_sano() {
    [[ -x "$VENV_DIR/bin/python" && -f "$VENV_DIR/bin/activate" ]] \
        && "$VENV_DIR/bin/python" -m pip --version >/dev/null 2>&1
}

if [[ -e "$VENV_DIR" ]] && ! venv_sano; then
    echo "Entorno virtual incompleto detectado: se recrea desde cero."
    rm -rf "$VENV_DIR"
fi

# Crear el entorno propio del proyecto si no existe.
if [[ ! -e "$VENV_DIR" ]]; then
    python3 -m venv "$VENV_DIR"
fi

venv_sano || {
    echo "Error: el entorno virtual quedó sin pip utilizable."
    exit 1
}

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
