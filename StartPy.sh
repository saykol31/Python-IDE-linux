#!/usr/bin/env bash

# Obtener la carpeta del proyecto, incluso al usar source.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

# Crear el entorno local si todavía no existe.
if [[ ! -f "$VENV_DIR/bin/activate" ]]; then
    command -v python3 >/dev/null 2>&1 || {
        echo "Error: no se encontró python3."
        return 1 2>/dev/null || exit 1
    }

    python3 -m venv "$VENV_DIR" || {
        echo "No se pudo crear el entorno virtual."
        echo "En Debian/MX Linux puedes instalarlo con:"
        echo "sudo apt install python3-venv"
        return 1 2>/dev/null || exit 1
    }
fi

# Activar el entorno en la terminal actual.
source "$VENV_DIR/bin/activate"

# Banner original.
echo -e "\033[1;92m"
echo " ==============================================="
echo "        PYTHON VIRTUAL ENVIROMENT v3.1"
echo " =============================================== "
echo -e "\033[0m"



#export PS1="(venv) $PS1"

echo -e "\033[1;95m      ******************ENTORNO VIRTUAL ACTIVADO******************  \033[0m"
echo -e "\033[1;94m      VERSION: $(python --version)    UBICACION: $SCRIPT_DIR\033[0m"
echo -e "\033[1;95m      -----------------------------------------------------------------\033[0m"
