# Python IDE

Entorno de desarrollo creado con Python 3 y Tkinter.

## Características

- Interfaz gráfica con Tkinter.
- Integración con herramientas del sistema.
- Ejecución de procesos externos.
- Gestión local de paquetes mediante SQLite.
- Uso de Pillow para funciones gráficas.

## Requisitos

- Python 3.
- Tkinter.
- Pillow.

En Debian y MX Linux, si Tkinter no está instalado:

    sudo apt install python3-tk python3-venv

## Instalación

Clona el repositorio y entra en su carpeta:

    git clone URL_DEL_REPOSITORIO
    cd NOMBRE_DEL_REPOSITORIO

Crea el entorno virtual:

    python3 -m venv --system-site-packages .venv
    source .venv/bin/activate

Instala las dependencias:

    python -m pip install -r requirements-ide.txt

## Ejecución

    python python_Ide.py

La aplicación puede crear archivos locales de configuración y una base
de datos SQLite durante su funcionamiento.

## Estado

Proyecto en desarrollo.
