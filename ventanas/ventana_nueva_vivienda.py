import tkinter as tk
from tkinter import simpledialog, filedialog
from ttkbootstrap import Style
import utils.manejo_archivos as manejo_archivos

class VentanaNuevaVivienda(simpledialog.Dialog):
    def __init__(self, parent):
        self.imagen_path = ""
        super().__init__(parent, "Añadir Nueva Vivienda")

    def body(self, master):
        self.style = Style(theme="superhero")
        tk.Label(master, text="Descripción:").grid(row=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(master, text="Precio:").grid(row=1, sticky=tk.W, padx=10, pady=5)
        tk.Label(master, text="Ubicación:").grid(row=2, sticky=tk.W, padx=10, pady=5)
        tk.Label(master, text="Imagen:").grid(row=3, sticky=tk.W, padx=10, pady=5)

        self.descripcion = tk.Entry(master)
        self.descripcion.grid(row=0, column=1, padx=10, pady=5)

        self.precio = tk.Entry(master)
        self.precio.grid(row=1, column=1, padx=10, pady=5)

        self.ubicacion = tk.Entry(master)
        self.ubicacion.grid(row=2, column=1, padx=10, pady=5)

        self.imagen_label = tk.Label(master, text="No seleccionada")
        self.imagen_label.grid(row=3, column=1, padx=10, pady=5)

        boton_seleccionar_imagen = tk.Button(master, text="Seleccionar Imagen", command=self.seleccionar_imagen)
        boton_seleccionar_imagen.grid(row=3, column=2, padx=10, pady=5)

        return self.descripcion

    def seleccionar_imagen(self):
        self.imagen_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        self.imagen_label.config(text=self.imagen_path.split("/")[-1])

    def apply(self):
        descripcion = self.descripcion.get()
        precio = self.precio.get()
        ubicacion = self.ubicacion.get()
        manejo_archivos.guardar_vivienda(descripcion, precio, ubicacion, self.imagen_path)
        self.parent.cargar_viviendas()
