# Python IDE

Entorno de desarrollo creado con Python 3 y Tkinter.

Versión 4.0: instaladores de un solo paso para Linux y Windows.

## Características

- Interfaz gráfica con Tkinter.
- Integración con herramientas del sistema.
- Ejecución de procesos externos.
- Gestión local de paquetes mediante SQLite.
- Uso de Pillow para funciones gráficas.

## Requisitos

- Python 3.

Nada más. Cada instalador comprueba lo que necesita su sistema y pone
lo que falte: en Linux instala los paquetes del sistema con sudo; en
Windows instala Python con winget si no lo hay. Pillow se instala
automáticamente dentro del entorno virtual del proyecto.

## Instalación

Clona el repositorio y entra en su carpeta:

    git clone https://github.com/saykol31/Python-IDE-linux.git
    cd Python-IDE-linux

### Linux (Debian y MX Linux)

Dale permisos al instalador y ejecútalo:

    chmod +x install.sh
    ./install.sh

Con esos dos comandos queda listo. El instalador:

- Instala los paquetes del sistema que falten (`python3-tk`,
  `python3-venv`).
- Crea el entorno virtual en `venv/` (si encuentra uno incompleto,
  lo borra y lo recrea).
- Instala las dependencias de `requirements-ide.txt` en el entorno.
- Crea un acceso directo en el Escritorio.

### Windows

En PowerShell, permite ejecutar el instalador solo en esa ventana
y ejecútalo:

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\install.ps1

Con eso queda listo. El instalador:

- Busca un Python real (ignora el atajo falso de la Microsoft Store)
  y, si no hay ninguno, lo instala con winget.
- Comprueba que el Python trae Tkinter.
- Crea el entorno virtual en `venv\` (si encuentra uno incompleto,
  lo borra y lo recrea).
- Instala las dependencias de `requirements-ide.txt` en el entorno.
- Crea un acceso directo en el Escritorio.

## Ejecución

### Linux

Desde el acceso directo del Escritorio, o con el lanzador del proyecto:

    ./ejecutar.sh

El lanzador usa el Python del entorno virtual. Para trabajar en una
terminal con el entorno ya activado están `activar_venv.sh` y
`StartPy.sh`.

### Windows

Desde el acceso directo del Escritorio, o con doble clic en:

    ejecutar.bat

La aplicación puede crear archivos locales de configuración y una base
de datos SQLite durante su funcionamiento.

## Estado

Proyecto en desarrollo.
