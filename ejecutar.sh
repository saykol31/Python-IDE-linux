#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
PYTHON_BIN="$VENV_DIR/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
    echo "No se encontró el entorno virtual de Python."
    echo "Ejecuta primero: $SCRIPT_DIR/install.sh"
    exit 1
fi

exec "$PYTHON_BIN" "$SCRIPT_DIR/python_Ide.py" "$@"
