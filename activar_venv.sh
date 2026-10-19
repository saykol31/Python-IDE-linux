#!/bin/bash
#activar_venv.sh

PROYECTO_DIR="$HOME/PYTHON"
VENV_DIR="venv"

cd "$PROYECTO_DIR" || { echo "No se pudo acceder a $PROYECTO_DIR"; exit 1; }

clear

# Banner en verde lima
echo -e "\033[1;92m"
echo               " ==============================================="
echo               "        PYTHON VIRTUAL ENVIROMENT v3.1"
echo               " =============================================== "
echo -e "\033[0m"

# Activar entorno virtual
source "$VENV_DIR/bin/activate"

# Mostrar (venv) en el prompt aunque la shell no lo haga por defecto
export PS1="(venv) $PS1"

# Mensaje en cyan
echo -e "\033[1;95m      ********************ENTORNO VIRTUAL ACTIVADO********************  \033[0m"
echo -e "\033[1;94m      VERSION: $(python3 --version)     UBICACION: $(pwd)\033[0m"
echo -e "\033[1;95m      -----------------------------------------------------------------\033[0m"

# Verificar si tkinter está instalado
echo -e "\033[1;93mVerificando Python en el entorno virtual...\033[0m"



# Mantener la shell abierta con el entorno activado
exec $SHELL
