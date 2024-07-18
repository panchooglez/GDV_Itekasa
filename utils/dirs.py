import os

def obtener_directorio_escritorio():
    home_dir = os.path.expanduser("~")
    escritorio_dir = os.path.join(home_dir, "Desktop")
    return escritorio_dir

def obtener_ruta(ruta):
    home = os.path.expanduser("~")
    return os.path.join(home, ruta)