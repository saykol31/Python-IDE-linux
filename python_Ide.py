# Importaciones estándar
import sys
import os
import re
import shlex
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import glob
import time
import queue
import tkinter.font as tkfont
import sqlite3
import shutil
import io
import json
# Importaciones de terceros
from PIL import Image, ImageTk
import importlib.metadata



# Rutas
#venv_python = sys.executable  # Siempre apunta al Python que ejecuta la IDE
DB_PATH = "pip_packages.db"
REQUIREMENTS_FILE = "requirements.txt"
VENV_DIR = "venv"  # nombre de tu entorno virtual
venv_python = "/home/saykol/PYTHON/venv/bin/python3"
RUTA = "/home/saykol/PYTHON"
pip_path = os.path.join(RUTA, "venv/bin/pip")

RUTA_BASE = "/home/saykol/PYTHON/mantenimiento/"
PYTHONPATH_GRAPH = "/home/saykol/PYTHON/dibujo/Graph_lib"
# Ruta al intérprete del entorno virtual



ultimo_archivo = None

# --- COLORES ---
COLOR_ROSA       = "#FF69B4"
COLOR_DORADO_OSC = "#DAA520"
COLOR_NARANJA    = "#FFA500"
COLOR_VERDE_LIMA = "#32CD32"
COLOR_AZUL_DODGE = "#1E90FF"
COLOR_PURPURA    = "#8A2BE2"
COLOR_TURQUESA   = "#00CED1"
COLOR_DORADO     = "#FFD700"
COLOR_ROJO       = "#FF0000"

# --- COLORES EXTENDIDOS ---
COLORES = {
    "NEGRO": "#000000",
    "BLANCO": "#FFFFFF",
    "GRIS": "#808080",
    "GRIS_CLARO": "#D3D3D3",
    "GRIS_OSCURO": "#A9A9A9",
    "GRIS_PIZARRA": "#708090",
    "GRIS_PIZARRA_OSCURO": "#2F4F4F",
    "ROJO": "#FF0000",
    "ROJO_OSCURO": "#8B0000",
    "ROJO_INDIO": "#CD5C5C",
    "ROSA": "#FF69B4",
    "ROSA_CLARO": "#FFB6C1",
    "ROSA_PROFUNDO": "#FF1493",
    "NARANJA": "#FFA500",
    "NARANJA_ROJO": "#FF4500",
    "DORADO": "#FFD700",
    "DORADO_OSCURO": "#DAA520",
    "AMARILLO": "#FFFF00",
    "AMARILLO_VERDE": "#9ACD32",
    "VERDE_LIMA": "#32CD32",
    "VERDE": "#008000",
    "VERDE_OSCURO": "#006400",
    "VERDE_MAR": "#2E8B57",
    "VERDE_MAR_CLARO": "#20B2AA",
    "VERDE_MAR_MEDIO": "#3CB371",
    "VERDE_OLIVA": "#6B8E23",
    "CIAN": "#00FFFF",
    "TURQUESA": "#40E0D0",
    "TURQUESA_OSCURO": "#00CED1",
    "TURQUESA_MEDIO": "#48D1CC",
    "AZUL": "#0000FF",
    "AZUL_OSCURO": "#00008B",
    "AZUL_MEDIO": "#0000CD",
    "AZUL_ACERO": "#4682B4",
    "AZUL_ACERO_CLARO": "#B0C4DE",
    "AZUL_CIELO": "#87CEEB",
    "AZUL_CIELO_CLARO": "#87CEFA",
    "AZUL_CIELO_PROFUNDO": "#00BFFF",
    "AZUL_DODGER": "#1E90FF",
    "AZUL_REYAL": "#4169E1",
    "AZUL_NAVAL": "#000080",
    "AZUL_MEDIANOCHE": "#191970",
    "PURPURA": "#800080",
    "PURPURA_OSCURO": "#4B0082",
    "PURPURA_MEDIO": "#9370DB",
    "PURPURA_ORQUIDEA": "#DA70D6",
    "PURPURA_VIOLETA": "#8A2BE2",
    "MARRON": "#A52A2A",
    "MARRON_SILLA": "#A0522D",
    "MARRON_CHOCOLATE": "#D2691E",
    "MARRON_SUELO": "#8B4513",
    "MARRON_CANELA": "#F4A460",
    "MARRON_TRIGO": "#F5DEB3",
    "BEIGE": "#F5F5DC",
    "MARFIL": "#FFFFF0",
    "CAFE": "#FFE4B5",
    "CORAL": "#FF7F50",
    "CORAL_CLARO": "#F08080",
    "SALMON": "#FA8072",
    "SALMON_CLARO": "#FFA07A",
    "SALMON_OSCURO": "#E9967A",
    "LAVANDA": "#E6E6FA",
    "LAVANDA_ROSADA": "#FFF0F5",
    "AZUL_VIOLETA": "#8A2BE2",
    "CHARTREUSE": "#7FFF00",
    "AGUAMARINA": "#7FFFD4",
    "AGUAMARINA_MEDIO": "#66CDAA",
    "CAQUI": "#F0E68C",
    "CAQUI_OSCURO": "#BDB76B",
    "MIEL": "#FFDAB9",
    "PERLA": "#EAE0C8",
    "PLATA": "#C0C0C0",
    "ORO_VIEJO": "#CFB53B"
}




# -------Definir Variables

# ---------------- VENTANA ---------------- #
root = tk.Tk()
frame_consola = tk.Frame(root)
root.title("IDE Python v.4.1")
root.geometry("900x850")
root.config(bg="#E6E6FA")



# --- FUNCIONES ---

###################  LISTAR  #######################

def listar():
    global ultimo_archivo
    archivo = filedialog.askopenfilename(
        initialdir=RUTA,
        filetypes=[("Archivos Python", "*.py"), ("Todos los archivos", "*.*")],
        title="Abrir archivo"
    )
    if archivo:
        with open(archivo, "r") as f:
            contenido = f.read()
        editor.delete("1.0", tk.END)
        editor.insert(tk.END, contenido)
        editor.edit_modified(False)
        ultimo_archivo = archivo
        messagebox.showinfo("Archivo abierto", f"Se abrió correctamente:\n{archivo}")

###################  GUARDAR  #######################

def guardar():
    global ultimo_archivo
    contenido = editor.get("1.0", tk.END)

    if ultimo_archivo:
        # Guardar directamente en el archivo ya existente
        with open(ultimo_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)

        editor.edit_modified(False)
        messagebox.showinfo("Guardado", f"Archivo guardado: {ultimo_archivo}")

        ruta_carpeta = os.path.dirname(ultimo_archivo)

    else:
        # Primera vez: pedir al usuario un nombre
        archivo = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),   # carpeta actual
            defaultextension=".py",
            filetypes=[("Archivos Python", "*.py"), ("Todos los archivos", "*.*")],
            title="Guardar como..."
        )
        if archivo:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(contenido)

            ultimo_archivo = archivo
            editor.edit_modified(False)
            messagebox.showinfo("Guardado", f"Archivo guardado: {ultimo_archivo}")

            ruta_carpeta = os.path.dirname(archivo)
        else:
            return  # canceló el diálogo

    # Limpiar consola
    consola.config(state="normal")
    consola.delete("1.0", tk.END)
    consola.config(state="disabled")

    # Mostrar en consola integrada
    if 'print_consola' in globals():
        print_consola(f"✅ Guardado en carpeta: {ruta_carpeta}")

###################  SELECCIONAR  #######################

def seleccionar_todo():
    """Selecciona todo el contenido del editor."""
    editor.tag_add("sel", "1.0", "end")
    editor.mark_set("insert", "1.0")  # opcional: colocar cursor al inicio
    editor.see("1.0")


###################  COPIAR  #######################

def copiar():
    editor.event_generate("<<Copy>>")

# Limpiar consola
    consola.config(state="normal")
    consola.delete("1.0", tk.END)
    consola.config(state="disabled")


###################  PEGAR  #######################

def pegar():
    editor.event_generate("<<Paste>>")
    editor.after_idle(resaltar)

# Limpiar consola
    consola.config(state="normal")
    consola.delete("1.0", tk.END)
    consola.config(state="disabled")


###################  LIMPIAR  #######################

def limpiar_area():
    global ultimo_archivo
    if editor.edit_modified():
        if not messagebox.askyesno("Confirmar", "Tienes cambios sin guardar. ¿Deseas continuar?"):
            return

         # Limpiar editor
    editor.delete("1.0", tk.END)
    editor.edit_modified(False)

     # Limpiar consola integrada
    consola.config(state="normal")
    consola.delete("1.0", tk.END)
    consola.config(state="disabled")

    # Limpiar barra de números de línea
    lineas.config(state="normal")
    lineas.delete("1.0", tk.END)
    lineas.config(state="disabled")

    ultimo_archivo = None
    messagebox.showinfo("Limpiar", "Área de edición vacía.")



###################  actualizar  #######################

#####################
# --- Configuración ---
#####################

DB_PATH = "pip_packages.db"
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
consola = None  # Se asigna desde el IDE

# Categorías de paquetes
CATEGORIAS = {
    "Herramientas de desarrollo": ["black", "mypy", "pytest"],
    "CLI y web": ["httpie", "rich"],
    "Frameworks web": ["flask", "django"],
    "Ciencia de datos": ["pandas", "matplotlib"],
    "Deep Learning": ["tensorflow", "torch"],
    "Scraping y testing": ["requests", "beautifulsoup4", "selenium"]
}

#########################
# --- Funciones de DB ---
#########################

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS packages (
            name TEXT PRIMARY KEY,
            version TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_packages_to_db(packages):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for pkg in packages:
        if "==" in pkg:
            name, version = pkg.strip().split("==")
        else:
            name, version = pkg.strip(), ""
        name = name.lower().strip()  # 🔑 normalizamos
        cursor.execute(
            "INSERT OR REPLACE INTO packages (name, version) VALUES (?, ?)",
            (name, version)
        )
    conn.commit()
    conn.close()


# -------------------------
# LEER DB CORRECTAMENTE
# -------------------------

def load_packages_from_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name, version FROM packages")
    rows = cursor.fetchall()
    conn.close()

    paquetes = {}
    for name, version in rows:
        if version:
             paquetes[name.lower()] = version
        else:
             paquetes[name.lower()] = ""
        return [f"{n}=={v}" if v else n for n, v in paquetes.items()]

        # Si hay duplicados con distintas versiones, quedarse con la última
        paquetes[name.lower()] = version
    return [f"{name}=={version}" for name, version in paquetes.items()]


# -------------------------
# SINCRONIZAR VENV -> DB
# -------------------------

def sync_installed_pip_to_db(pip_path):
    result = subprocess.run([pip_path, "freeze"], capture_output=True, text=True)
    if result.stdout:
        paquetes = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        add_packages_to_db(paquetes)
        log_consola("✅ Paquetes actuales del venv sincronizados con la DB.", "green")

#########################
# --- Funciones PyPI ---
#########################

def get_paquetes_instalados():
    import importlib.metadata
    return {dist.metadata['Name'].lower(): dist.version for dist in importlib.metadata.distributions()}

def get_paquetes_desactualizados(pip_path):
    result = subprocess.run([pip_path, "list", "--outdated", "--format=json"],
                            stdout=subprocess.PIPE, text=True)
    desactualizados = {}
    try:
        data = json.loads(result.stdout)
        for pkg in data:
            desactualizados[pkg["name"].lower()] = pkg["latest_version"]
    except json.JSONDecodeError:
        log_consola("⚠️ No se pudo leer la lista de paquetes desactualizados.", "red")
    return desactualizados

def generar_requirements(pip_path):
    result = subprocess.run([pip_path, "freeze"], capture_output=True, text=True)
    if result.stdout:
        with open(REQUIREMENTS_FILE, "w") as f:
            f.write(result.stdout)
        log_consola(f"✅ {REQUIREMENTS_FILE} generado.", "green")

#########################
# --- Consola IDE ---
#########################

def log_consola(linea, color="white"):
    global consola
    if consola is None:
        print(linea)  # fallback si no hay consola
    else:
        consola.config(state="normal")
        consola.insert(tk.END, linea + "\n", color)
        consola.see(tk.END)
        consola.config(state="disabled")

def ejecutar_comando(comando):
    try:
        proceso = subprocess.Popen(
            comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1
        )

        def leer_salida(fuente, color):
            for linea in fuente:
                log_consola(linea.strip(), color)
            fuente.close()

        threading.Thread(target=leer_salida, args=(proceso.stdout, "green"), daemon=True).start()
        threading.Thread(target=leer_salida, args=(proceso.stderr, "red"), daemon=True).start()

        proceso.wait()
        if proceso.returncode != 0:
            log_consola(f"⚠️ El comando falló con código {proceso.returncode}", "red")
    except Exception as e:
        log_consola(f"Error al ejecutar comando: {e}", "red")

#########################
# --- Función principal ---
#########################

def _actualizar_venv_completo():
    log_consola("♻ Iniciando actualización del venv...", "cyan")

    # Validar venv
    pip_path_local = os.path.join(VENV_DIR, "Scripts", "pip.exe") if sys.platform == "win32" else os.path.join(VENV_DIR, "bin", "pip")
    if not os.path.isfile(pip_path_local):
        log_consola(f"No se encontró pip en el venv: {pip_path_local}", "red")
        return

    # Inicializar DB
    init_db()
    log_consola("📂 Base de datos de paquetes inicializada.", "cyan")

    # Sincronizar pip actual con DB
    sync_installed_pip_to_db(pip_path_local)

    # Actualizar paquetes por categorías
    instalados = get_paquetes_instalados()
    desactualizados = get_paquetes_desactualizados(pip_path_local)

    for nombre_categoria, paquetes in CATEGORIAS.items():
        para_instalar = [p for p in paquetes if p.lower() not in instalados]
        para_actualizar = [p for p in paquetes if p.lower() in desactualizados]

        if para_instalar:
            log_consola(f"Paquetes de {nombre_categoria} para instalar: {para_instalar}", "yellow")
            ejecutar_comando([pip_path_local, "install"] + para_instalar)

        if para_actualizar:
            log_consola(f"Paquetes de {nombre_categoria} para actualizar: {para_actualizar}", "cyan")
            ejecutar_comando([pip_path_local, "install", "--upgrade"] + para_actualizar)

    # Procesar requirements.txt
    if os.path.isfile(REQUIREMENTS_FILE):
        log_consola(f"📄 Procesando {REQUIREMENTS_FILE}...", "yellow")
        with open(REQUIREMENTS_FILE, "r") as f:
            nuevos_paquetes = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        add_packages_to_db(nuevos_paquetes)
        ejecutar_comando([pip_path_local, "install", "--upgrade"] + load_packages_from_db())
        log_consola("✅ Todos los paquetes actualizados.", "green")
    else:
        log_consola(f"No se encontró {REQUIREMENTS_FILE}. Se omite esta parte.", "yellow")

    # Re-sincronizar DB con el estado final del venv
    sync_installed_pip_to_db(pip_path_local)

    # Regenerar requirements.txt actualizado
    generar_requirements(pip_path_local)
    log_consola("♻ Actualización del venv completada.", "cyan")

def actualizar_venv_completo():
    threading.Thread(target=_actualizar_venv_completo, daemon=True).start()

###################  EJECUTAR  #######################

def ejecutar_archivo():
    global ultimo_archivo
    try:
        if not ultimo_archivo:
            messagebox.showwarning("Ejecutar", "⚠️ No has abierto ningún archivo aún.")
            return

        # Ejecutar dentro de IDE, sin abrir Konsole
        comando = [venv_python, ultimo_archivo]

        proceso = subprocess.Popen(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        def leer_salida(fuente, color="white"):
            for linea in fuente:
                consola.config(state="normal")
                consola.insert(tk.END, linea, color)
                consola.see(tk.END)
                consola.config(state="disabled")
            fuente.close()

        # Capturar stdout (verde) y stderr (rojo)
        threading.Thread(target=leer_salida, args=(proceso.stdout, "green"), daemon=True).start()
        threading.Thread(target=leer_salida, args=(proceso.stderr, "red"), daemon=True).start()

        messagebox.showinfo("Ejecución", f"Ejecutando en consola integrada:\n{ultimo_archivo}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo ejecutar el archivo.\n{e}")



###################  CREAR  #######################



def crear_externo():
    # Abrir VS Code
    try:
        subprocess.Popen(["code"])
        # Limpiar consola integrada
        consola.config(state="normal")
        consola.delete("1.0", tk.END)
        consola.config(state="disabled")
        print_consola(f"✅ abriendo VS Code....\n", "verde")
    except Exception as e:
        print_consola(f"❌ Error al abrir VS Code: {e}", "rojo")




###################  PyCharm  #######################

# --- Función para abrir PyCharm ---
def pycharm():
    try:
        # Intentar ejecutar PyCharm
        subprocess.Popen(["/opt/pycharm/bin/pycharm.sh"])
        # Limpiar consola integrada
        consola.config(state="normal")
        consola.delete("1.0", tk.END)
        consola.insert(tk.END, "✅ PyCharm se ha abierto correctamente.\n", "verde")
        consola.config(state="disabled")
    except Exception as e:
        consola.config(state="normal")
        consola.insert(tk.END, f"❌ Error al abrir PyCharm: {e}\n")
        consola.config(state="disabled")




###################  DATA BASE  #######################


def listar_db():
    """
    Lista todo el contenido de la base de datos de paquetes.
    Muestra nombre y versión (si existe), ordenados alfabéticamente.
    """
    try:
        if not os.path.isfile(DB_PATH):
            print_consola("⚠️ La base de datos no existe aún.", "amarillo")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name, version FROM packages ORDER BY name COLLATE NOCASE")
        paquetes = cursor.fetchall()
        conn.close()

        if paquetes:
            print_consola("📦 Paquetes en la DB:", "cyan")
            for name, version in paquetes:
                if version and version.strip():
                    print_consola(f"{name}=={version}", "green")
                else:
                    print_consola(f"{name}", "green")
            print_consola(f"🔍 Total: {len(paquetes)} paquetes registrados.", "cyan")
        else:
            print_consola("ℹ️ La base de datos está vacía.", "yellow")

    except Exception as e:
        print_consola(f"❌ Error al acceder a la DB: {e}", "red")


# --- FUNCIONES ESPECIALES---

def ejecutar_script(script):
    ruta_completa = os.path.join(RUTA_BASE, script)
    if script == "repotest.sh":
        if not messagebox.askyesno("Confirmación",
                                   "⚠️ Este script moverá y restaurará repositorios.\n¿Seguro que quieres continuar?"):
            return
    try:
        if script.endswith(".py"):
            subprocess.Popen([venv_python, ruta_completa])
        elif script.endswith(".sh"):
            subprocess.Popen(['konsole', '--noclose', '-e', ruta_completa])

        else:
            messagebox.showerror("Error", f"Tipo de archivo no soportado: {script}")
            return
        messagebox.showinfo("Ejecutando", f"Se abrió konsole para {script}.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo ejecutar {script}.\n{e}")

def exportar_pythonpath():
    comando = f'export PYTHONPATH=$PYTHONPATH:{PYTHONPATH_GRAPH}; echo "PYTHONPATH exportado correctamente"; exec bash'
    subprocess.Popen(['konsole', '--noclose', '-e', 'bash', '-c', comando])
    messagebox.showinfo("PYTHONPATH", "Variable PYTHONPATH exportada en Konsole.")

def compilar_cpp():
    comando = (
        f'export PYTHONPATH=$PYTHONPATH:{PYTHONPATH_GRAPH} && '
        f'cd {PYTHONPATH_GRAPH} && '
        'c++ main.cpp -o main -O2 -std=c++17 $(python3 -m pybind11 --includes) -lpython3.11 && '
        'echo "✅ Compilación completada"; exec bash'
    )
    subprocess.Popen(['konsole', '--noclose', '-e', 'bash', '-c', comando])
    messagebox.showinfo("Compilación", f"Se abrió Konsole para compilar main.cpp en {PYTHONPATH_GRAPH}.")


# Fuente global para botones
FUENTE_BOTONES = ("Segoe UI", 10, "bold")
FUENTE_BOTONES1 = ("Courier", 10, "bold")
FUENTE_BOTONES2 = ("Courier", 10, "bold")



# --- FRAME SUPERIOR ---

frame_superior = tk.Frame(root, bg="#E6E6FA")
frame_superior.pack(side="top", fill="x", pady=5)

btn_abrir = tk.Button(frame_superior, text="OPEN", command=listar, bg="#4682B4", fg="white", font=FUENTE_BOTONES)
btn_abrir.pack(side="left", padx=5)

btn_guardar = tk.Button(frame_superior, text="SAVE", command=guardar, bg="#4682B4", fg="white", font=FUENTE_BOTONES)
btn_guardar.pack(side="left", padx=5)

btn_selectall = tk.Button(frame_superior, text="SELECT ALL", command=seleccionar_todo, bg="#4682B4", fg="white", font=FUENTE_BOTONES)
btn_selectall.pack(side="left", padx=5)

btn_copiar = tk.Button(frame_superior, text="COPY", command=copiar, bg="#4682B4", fg="white", font=FUENTE_BOTONES)
btn_copiar.pack(side="left", padx=5)

btn_pegar = tk.Button(frame_superior, text="PASTE", command=pegar, bg="#4682B4", fg="white", font=FUENTE_BOTONES)
btn_pegar.pack(side="left", padx=5)

btn_clear = tk.Button(frame_superior, text="CLEAR", command=limpiar_area, bg="#4682B4", fg="white", font=FUENTE_BOTONES)
btn_clear.pack(side="left", padx=5)

btn_update = tk.Button(frame_superior, text="UPDATE", command=actualizar_venv_completo, bg="#4682B4", fg="white", font=FUENTE_BOTONES)
btn_update.pack(side="left", padx=5)

btn_ejecutar = tk.Button(frame_superior, text="PLAY", command=ejecutar_archivo,  bg=COLORES["VERDE"], fg="white", font=FUENTE_BOTONES)
btn_ejecutar.pack(side="left", padx=5)

btn_exit = tk.Button(frame_superior, text="EXIT", command=root.destroy, bg=COLOR_ROJO, fg="white", font=FUENTE_BOTONES)
btn_exit.pack(side="left", padx=5)




###################   EDITOR  #######################


# --- identado   ---
def auto_indent_python(event):
    line = editor.get("insert linestart", "insert")
    indent = ""
    for c in line:
        if c in (" ", "\t"):
            indent += c
        else:
            break

    # Revisar si la línea termina en ':' → añadir un nivel extra
    line_text = editor.get("insert linestart", "insert lineend").strip()
    if line_text.endswith(":"):
        # Considerar tabsize de 4 espacios
        indent += " " * 4

    editor.insert("insert", "\n" + indent)
    return "break"

# --- Area de EDITOR  ---

# Contenedor para barra de línea + editor
frame_editor = tk.Frame(root)
frame_editor.pack(fill="both", expand=True, padx=5, pady=5)

# --- Barra de números de línea ---
lineas = tk.Text(frame_editor, width=4, padx=3, takefocus=0, border=0,
                 background="#DDDDDD", state="disabled", wrap="none")
lineas.pack(side="left", fill="y")

# --- Editor PRINCIPAL  ---

# Scrollbar vertical del editor
scroll_vert = tk.Scrollbar(frame_editor, orient="vertical", command=lambda *args: [editor.yview(*args), lineas.yview(*args)])
scroll_vert.pack(side="right", fill="y")

# Scrollbar horizontal del editor
scroll_hor = tk.Scrollbar(frame_editor, orient="horizontal", command=lambda *args: [editor.xview(*args), lineas.xview(*args)])
scroll_hor.pack(side="bottom", fill="x")

#------AREA DE TRABAJO-----

editor = tk.Text(frame_editor, wrap="none", background="#FFFFFF",yscrollcommand=scroll_vert.set, xscrollcommand=scroll_hor.set, font=("Courier", 10), undo=True)
editor.pack(side="left", fill="both", expand=True)

# --- Scroll sincronizado entre editor y números de línea ---
def sync_scroll(*args):
    editor.yview(*args)
    lineas.yview(*args)
    scroll_vert.set(*args)  # actualiza scrollbar vertical

# Conectar scrollbars con editor y línea
editor.config(yscrollcommand=scroll_vert.set, xscrollcommand=scroll_hor.set)
lineas.config(yscrollcommand=scroll_vert.set)

# --- Función de sincronización para scrollbar vertical ---
scroll_vert.config(command=sync_scroll)
scroll_hor.config(command=editor.xview)

# Función para sincronizar la rueda del ratón
def on_mouse_wheel(event):
    # Windows/Mac usan event.delta, Linux usa Button-4/5
    if event.num == 4:   # Linux scroll up
        editor.yview_scroll(-1, "units")
        lineas.yview_scroll(-1, "units")
    elif event.num == 5: # Linux scroll down
        editor.yview_scroll(1, "units")
        lineas.yview_scroll(1, "units")
    else:
        editor.yview_scroll(int(-1*(event.delta/120)), "units")
        lineas.yview_scroll(int(-1*(event.delta/120)), "units")
    return "break"

# Vincular rueda del ratón
editor.bind("<MouseWheel>", on_mouse_wheel)  # Windows/Mac
editor.bind("<Button-4>", on_mouse_wheel)    # Linux scroll up
editor.bind("<Button-5>", on_mouse_wheel)    # Linux scroll down




# --- Auto-indent + actualizar líneas correctamente ---
def on_return(event):
    auto_indent_python(event)
    root.after(10, actualizar_lineas)  # esperar que el Enter se procese
    root.after(15, resaltar)           # llamar al resaltado después de actualizar líneas
    return "break"

editor.bind("<Return>", on_return)


# Llamar resaltar + actualizar líneas en eventos de edición
editor.bind("<Any-KeyRelease>", lambda e: [actualizar_lineas(), resaltar()])
editor.bind("<Button-1>", lambda e: [actualizar_lineas(), resaltar()])
editor.bind("<MouseWheel>", lambda e: [actualizar_lineas(), resaltar()])

# ---------------- RESALTADO AVANZADO ---------------- #
def resaltar(event=None):
    contenido = editor.get("1.0", tk.END)

    # Borrar formatos previos
    for tag in editor.tag_names():
        editor.tag_remove(tag, "1.0", tk.END)

    # --- Palabras clave de Python ---
    palabras_clave = r'\b(' + '|'.join([
        # Tipos básicos
        'None', 'True', 'False', 'int', 'float', 'complex', 'bool', 'str', 'bytes', 'bytearray', 'list', 'tuple', 'set', 'frozenset', 'dict',

        # Control de flujo
        'if', 'elif', 'else', 'for', 'while', 'break', 'continue', 'return', 'yield', 'try', 'except', 'finally', 'raise', 'with', 'as', 'assert', 'del', 'pass',

        # Definición y clases
        'def', 'class', 'lambda', 'nonlocal', 'global', 'import', 'from', 'return', 'async', 'await',

        # Operadores especiales y palabras mágicas
        'in', 'is', 'not', 'and', 'or', 'assert', 'async', 'await',

        # Decoradores y tipos de contexto
        'self', '__init__', '__name__', '__main__',

        # Literales especiales
        'Ellipsis',

        # Excepciones comunes (para resaltado)
        'Exception', 'BaseException', 'KeyboardInterrupt', 'SystemExit', 'StopIteration', 'GeneratorExit',

        # Palabras de manejo de módulos
        'import', 'from', 'as', 'global', 'nonlocal',

        # Otros
        'del', 'pass'
    ]) + r')\b'


    # Preprocesadores
    preprocesador = r'^\s*#\s*\w+'

    # Strings (simples y dobles)
    string = r'(\".*?\"|\'.*?\')'

    # Comentarios (// y /* */)
    comentario_linea = r'//.*$'        # termina al final de la línea
    comentario_bloque = r'/\*.*?\*/'   # multilinea

    # Funciones (identificadores seguidos de paréntesis)
    funcion = r'\b([a-zA-Z_]\w*)(?=\s*\()'

    # Números
    numeros = r'\b\d+(\.\d+)?\b'

    # Aplicar resaltado
    patrones = [
        ("comment", comentario_bloque),  # primero los bloques
        ("comment", comentario_linea),   # luego los comentarios de línea
        ("string", string),
        ("keyword", palabras_clave),
        ("preprocessor", preprocesador),
        ("function", funcion),
        ("number", numeros)
    ]


    for tag, pattern in patrones:
        flags = re.MULTILINE
        if tag == "comment" and pattern == comentario_bloque:
            flags |= re.DOTALL  # permite multilinea en /* */
        for match in re.finditer(pattern, contenido, flags):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            editor.tag_add(tag, start, end)

# --- Configuración de colores y estilos neón ---
editor.tag_config("keyword", foreground="#0000FF", font=("Consolas", 10, ))        # azul intenso
editor.tag_config("preprocessor", foreground="#BF00FF", font=("Consolas", 10, ))   # púrpura neón
editor.tag_config("string", foreground="#C833FF", font=("Consolas", 10, "italic"))       # lila neón
editor.tag_config("comment", foreground="#008000", font=("Consolas", 10, "italic"))      # verde intenso
editor.tag_config("function", foreground="#C833FF", font=("Consolas", 10, "underline"))  #  rosado
editor.tag_config("number", foreground="#FF3131", font=("Consolas", 10, ))         # rojo neón

# --- Opcionales adicionales para resaltado avanzado ---
editor.tag_config("type", foreground="#00FF9F", font=("Consolas", 10, ))           # tipos de datos
editor.tag_config("operator", foreground="#FFFF00", font=("Consolas", 10, ))       # operadores
editor.tag_config("constant", foreground="#FF00FF", font=("Consolas", 10, ))       # constantes
editor.tag_config("boolean", foreground="#00FFFF", font=("Consolas", 10, ))        # true / false
editor.tag_config("namespace", foreground="#FFA500", font=("Consolas", 10, "italic"))    # nombres de espacio
editor.tag_config("macro", foreground="#BF00FF", font=("Consolas", 10, ))          # macros #define
editor.tag_config("todo", foreground="#FF1493", font=("Consolas", 10, ))           # comentarios

# --- Actualizar números de línea ---
def actualizar_lineas(event=None):
    lineas.config(state="normal")
    lineas.delete("1.0", tk.END)
    # obtener número de líneas reales, ignorando línea final extra
    num_lineas = int(editor.index('end-1c').split('.')[0])
    numeros = "\n".join(str(i) for i in range(1, num_lineas+1))
    lineas.insert("1.0", numeros)
    lineas.config(state="disabled")

# Inicializar línea 1 al inicio
actualizar_lineas()
resaltar()



# --- Barra inferior ---
frame_inferior = tk.Frame(root, bg="#E6E6FA")
frame_inferior.pack(side="bottom", fill="x", pady=5)

#  - -  -tupla-  -  -("Nombre del boton", enlace a la funcion , color del boton , "nombre del icono"),
botones_inferior = [
    ("Crear (F1)", crear_externo, COLOR_NARANJA, "crear"),
    ("PyCharm (F2)",pycharm, COLOR_NARANJA, "pycharm"),
    ("DATA BASE (F3)",listar_db, COLOR_NARANJA, "linker"),
    ("Build (F5)",listar_db, COLOR_NARANJA, "build"),
    ("Compile (F6)",listar_db, COLOR_NARANJA, "compilar"),
    ("Debug (F7)",listar_db, COLOR_NARANJA, "debug"),
    ("Run (F8)",listar_db, COLOR_NARANJA, "ejecutar"),
]

for texto,comando, color, icono_nombre in botones_inferior:
    #img = iconos.get()
    btn = tk.Button(
        frame_inferior,
        text=texto,
        command=comando,
        #image=img,
        compound="top",
        bg=color,
        fg="black",
        activebackground="#FFD700",  # fondo al presionar
        activeforeground="black",    # texto al presionar
        relief="raised",              # efecto elevado
        bd=4,                         # grosor del borde
        padx=4,
        pady=4,
        highlightthickness=0,
        font=("Arial", 10, "bold"),  # <-- aquí asignas la fuente
    )
    # Ajuste seguro: solo si img existe
    #if img is not None:
        #btn.config(width=img.width(), height=img.height())
        #refs_imgs.append(img)  # mantener referencia para que no se elimine

    btn.pack(side="left", padx=3)



# --- POPUP MENU ---
popup_menu = tk.Menu(root, tearoff=0, bg="white", fg="black",
                     font=("Arial", 10))

# Lista de opciones
opciones_menu = [
    ("Actualizar entorno", "actualizarentorno.py"),
    ("Temperatura", "temperatura.py"),
    ("Monitores", "pantallas.py"),
    ("Bateria", "bateria.py"),
    ("Perifericos", "perifericos.py"),
    ("HARDWARE", "hardware.py"),
    ("BUSES Y PUERTOS", "busesypuertos.py"),
    ("Actualizar sistema", "my_updater.py"),
    ("Paquetes Rotos", "paquetesrotos.py"),
    ("Probar Repositorios Rotos", "repotest.sh"),
    ("Limpiar temporales", "limpiar_temporales.py"),
    ("Vaciar papelera", "vaciar_papelera.py"),
    ("Limpiar caché DNS", "limpiar_dns.py"),
    ("Reiniciar red", "reiniciar_red.py"),
    ("Restaurar DNS", "restaurar_dns.py"),
]

# Añadir opciones al popup
for texto, script in opciones_menu:
    popup_menu.add_command(label=texto,
                           command=lambda s=script: ejecutar_script(s))

# --- BOTÓN MENU ---
def mostrar_menu(event=None):
    # Obtener posición del botón
    x = menu_boton.winfo_rootx()
    y = menu_boton.winfo_rooty()
    # Mostrar el menú justo encima del botón (desplegable hacia arriba)
    popup_menu.tk_popup(x, y - popup_menu.winfo_reqheight())

menu_boton = tk.Button(frame_inferior, text="MENU",
                       bg="#DAA520", fg="black",
                       font=("Arial", 10, "bold"),
                       relief="raised", bd=3,
                       activebackground="#FFD700",
                       command=mostrar_menu)
menu_boton.pack(side="left", padx=5, pady=5)




# --- BOTONES EXTRA ---

btn_export = tk.Button(frame_inferior, text="Exportar PYTHONPATH", command=exportar_pythonpath)
btn_export.pack(side="left", padx=5)

btn_compilar = tk.Button(frame_inferior, text="Compilar main.cpp", command=compilar_cpp)
btn_compilar.pack(side="left", padx=5)


#----------------------------------
# --- Area de consola integrada ---
#-----------------------------------

# Contenedor principal de la consola
frame_consola = tk.Frame(root, bg="black")
frame_consola.pack(fill="both", side="bottom", padx=5, pady=5, expand=True)

# Frame para la salida
frame_salida = tk.Frame(frame_consola)
frame_salida.pack(fill="both", expand=True)

# Text de salida dentro de frame_salida
consola = tk.Text(frame_salida, height=12, bg="black", fg="white",
                  font=("Courier", 10), state="disabled", wrap="none")
consola.pack(side="left", fill="both", expand=True)

# Scroll vertical dentro de frame_salida
scroll_consola = tk.Scrollbar(frame_salida, command=consola.yview)
scroll_consola.pack(side="right", fill="y")
consola.config(yscrollcommand=scroll_consola.set)

# Frame para la entrada
frame_entrada = tk.Frame(frame_consola)
frame_entrada.pack(fill="x")  # ocupa todo el ancho inferior

# Entrada de comandos dentro de frame_entrada
entrada_consola = tk.Entry(frame_entrada, bg="black", fg="white",
                           insertbackground="white", font=("Courier", 10))
entrada_consola.pack(fill="x", padx=0, pady=2)

# --- Variables globales ---
proceso_activo = None
cola_salida = queue.Queue()
historial = []
indice_historial = -1
stdin_queue = queue.Queue()
ultimo_archivo = None  # Aquí se guarda el archivo actual a ejecutar
venv_python = sys.executable  # Ajusta a tu venv si es otro

# --- Función para imprimir en consola ---
def print_consola(mensaje, color=None):
    consola.config(state="normal")
    if color:
        consola.insert(tk.END, mensaje + "\n", color)
    else:
        consola.insert(tk.END, mensaje + "\n")
    consola.see(tk.END)
    consola.config(state="disabled")

# Colores para diferenciar
consola.tag_config("verde", foreground="#00FF00")
consola.tag_config("rojo", foreground="#FF0000")
consola.tag_config("amarillo", foreground="#FFFF00")
consola.tag_config("cyan", foreground="#00FFFF")
consola.tag_config("lila", foreground="#FF00FF")

# --- Lectura de procesos en hilos ---
def leer_salida(proceso):
    for linea in iter(proceso.stdout.readline, ''):
        if linea:
            cola_salida.put(("stdout", linea.rstrip()))
    proceso.stdout.close()

def leer_error(proceso):
    for linea in iter(proceso.stderr.readline, ''):
        if linea:
            cola_salida.put(("stderr", linea.rstrip()))
    proceso.stderr.close()

def actualizar_consola():
    try:
        while True:
            tipo, mensaje = cola_salida.get_nowait()
            if tipo == "stdout":
                print_consola(mensaje, "verde")
            else:
                print_consola(mensaje, "rojo")
    except queue.Empty:
        pass
    root.after(100, actualizar_consola)

# --- Hilo que envía input() del usuario al proceso ---
def hilo_entrada_proceso():
    global proceso_activo
    while proceso_activo and proceso_activo.poll() is None:
        linea = stdin_queue.get()  # Bloquea hasta que el usuario escriba
        proceso_activo.stdin.write(linea + "\n")
        proceso_activo.stdin.flush()

# --- Función para enviar comandos desde Entry ---
def enviar_comando(event=None):
    global proceso_activo, indice_historial

    entrada = entrada_consola.get().strip()
    if not entrada:
        return
    entrada_consola.delete(0, tk.END)

    # Guardar en historial
    historial.append(entrada)
    indice_historial = len(historial)

    # --- Comandos internos ---
    if entrada == "clear":
        consola.config(state="normal")
        consola.delete("1.0", tk.END)
        consola.config(state="disabled")
        return
    elif entrada == "exit":
        if proceso_activo and proceso_activo.poll() is None:
            proceso_activo.terminate()
            print_consola("🔴 Proceso terminado.", "rojo")
            proceso_activo = None
        else:
            root.destroy()
        return
    elif entrada == "help":
        print_consola("Comandos internos:", "amarillo")
        print_consola("  clear  -> limpia la consola", "amarillo")
        print_consola("  exit   -> termina proceso activo o sale del IDE", "amarillo")
        print_consola("  help   -> muestra esta ayuda", "amarillo")
        print_consola("  python -> abre intérprete Python en venv", "amarillo")
        return

    # --- Python en venv ---
    if entrada in ("python", "startpy"):
        if proceso_activo and proceso_activo.poll() is None:
            print_consola("🔵 Ya hay un proceso Python activo.", "amarillo")
            return
        try:
            proceso_activo = subprocess.Popen(
                [venv_python],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            threading.Thread(target=leer_salida, args=(proceso_activo,), daemon=True).start()
            threading.Thread(target=leer_error, args=(proceso_activo,), daemon=True).start()
            threading.Thread(target=hilo_entrada_proceso, daemon=True).start()
            print_consola(f"✅ Intérprete Python del venv lanzado: {venv_python}", "amarillo")
        except Exception as e:
            print_consola(f"Error al iniciar Python: {e}", "rojo")
        return

    # --- Si hay proceso activo, enviar al stdin ---
    if proceso_activo and proceso_activo.poll() is None:
        stdin_queue.put(entrada)
        print_consola("> " + entrada, "cyan")
        return

    # --- Comando externo ---
    try:
        proceso_activo = subprocess.Popen(
            entrada,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        threading.Thread(target=leer_salida, args=(proceso_activo,), daemon=True).start()
        threading.Thread(target=leer_error, args=(proceso_activo,), daemon=True).start()
        print_consola(f"✅ Comando externo ejecutado: {entrada}", "amarillo")
    except Exception as e:
        print_consola(f"Error al ejecutar: {e}", "rojo")

# --- Historial con flechas ---
def navegar_historial(event):
    global indice_historial
    if historial:
        if event.keysym == "Up":
            indice_historial = max(0, indice_historial - 1)
        elif event.keysym == "Down":
            indice_historial = min(len(historial), indice_historial + 1)
        if 0 <= indice_historial < len(historial):
            entrada_consola.delete(0, tk.END)
            entrada_consola.insert(0, historial[indice_historial])

# --- Bind de eventos ---
entrada_consola.bind("<Return>", enviar_comando)
entrada_consola.bind("<Up>", navegar_historial)
entrada_consola.bind("<Down>", navegar_historial)

# --- Arranque ---
# --- Banner de inicio ---
actualizar_consola()

# Banner principal (verde lima)
banner_lines = [
                   "                   ===============================================",
                   "                           PYTHON VIRTUAL ENVIRONMENT v4.1",
                   "                   =============================================== "
]
for line in banner_lines:
    # Centrar el texto según ancho de consola (aprox)
    print_consola(line.center(60), "verde")

# Obtener la carpeta del venv (normalmente la carpeta padre de bin/python)
ubicacion_venv = os.path.dirname(os.path.dirname(sys.executable))

# Mensaje de activación (cyan / lila)
mensaje_lines = [
    "********************************ENTORNO VIRTUAL ACTIVADO*****************************",
    f"VERSION: {sys.version.split()[0]}   VENV: {ubicacion_venv}   ACTUAL: {os.getcwd()}",
    "-------------------------------------------------------------------------------------"
]

# Alternar colores para resaltar
colores = ["cyan", "lila", "cyan"]
for line, color in zip(mensaje_lines, colores):
    print_consola(line.center(60), color)


root.mainloop()




