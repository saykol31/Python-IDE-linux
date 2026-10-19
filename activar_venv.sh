#!/bin/bash
# activar_venv.sh

# Localizar el proyecto a partir de la ubicación de este script.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

# Comprobar que existe el entorno virtual.
if [[ ! -f "$VENV_DIR/bin/activate" ]]; then
    echo "Error: no se encontró el entorno virtual en:"
    echo "$VENV_DIR"
    echo "Ejecuta primero ./install.sh para crearlo."
    exit 1
fi

cd "$SCRIPT_DIR" || {
    echo "No se pudo acceder a $SCRIPT_DIR"
    exit 1
}

clear

# Banner en verde lima.
echo -e "\033[1;92m"
echo " ==============================================="
echo "       PYTHON VIRTUAL ENVIRONMENT v3.1"
echo " ==============================================="
echo -e "\033[0m"

# Activar el entorno virtual local.
source "$VENV_DIR/bin/activate" || {
    echo "No se pudo activar el entorno virtual."
    exit 1
}

# Mostrar el entorno activado en el prompt.
export PS1="(venv) $PS1"

# Información del entorno.
echo -e "\033[1;95m********** ENTORNO VIRTUAL ACTIVADO **********\033[0m"
echo -e "\033[1;94mVERSION: $(python --version)  UBICACION: $(pwd)\033[0m"
echo -e "\033[1;95m---------------------------------------------------------------\033[0m"

echo -e "\033[1;93mVerificando Python en el entorno virtual...\033[0m"
echo "Python utilizado: $(command -v python)"
echo "Entorno virtual: $VIRTUAL_ENV"

# Mantener una shell abierta con el entorno activado.
exec "${SHELL:-/bin/bash}"
