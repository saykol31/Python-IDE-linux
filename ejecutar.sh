#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_BIN=""

if [[ -x "$SCRIPT_DIR/.venv/bin/python" ]]; then
    PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"
else
    command -v python3 >/dev/null 2>&1 || {
        echo "Error: no se encontró python3."
        exit 1
    }

    python3 -c 'import tkinter' 2>/dev/null || {
        echo "Error: Tkinter no está disponible."
        echo "Instala el paquete del sistema: sudo apt install python3-tk"
        exit 1
    }

    python3 -m venv --system-site-packages "$SCRIPT_DIR/.venv" || {
        echo "No se pudo crear el entorno virtual."
        echo "En Debian/MX Linux puedes instalarlo con:"
        echo "sudo apt install python3-venv"
        exit 1
    }

    PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"

    "$PYTHON_BIN" -m pip install -r "$SCRIPT_DIR/requirements-ide.txt"
fi

"$PYTHON_BIN" "$SCRIPT_DIR/python_Ide.py" "$@"
