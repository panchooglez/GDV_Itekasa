import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from ventanas.ventana_nueva_vivienda import VentanaNuevaVivienda
import utils.manejo_archivos as manejo_archivos
import utils.generador_video as generador_video

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        # Estilo de ttkbootstrap
        self.style = Style(theme="superhero")
        self.title("Gestión de Viviendas")
        self.geometry("800x600")

        # Crear un frame principal
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Treeview con estilo ttk
        self.lista_viviendas = ttk.Treeview(main_frame, columns=("ID", "Descripción", "Precio", "Ubicación"), show='headings', height=15)
        self.lista_viviendas.heading("ID", text="ID")
        self.lista_viviendas.heading("Descripción", text="Descripción")
        self.lista_viviendas.heading("Precio", text="Precio")
        self.lista_viviendas.heading("Ubicación", text="Ubicación")
        self.lista_viviendas.pack(expand=True, fill=tk.BOTH)

        # Configurar el Treeview para ajustar las columnas al contenido
        self.lista_viviendas.column("ID", width=50, anchor='center')
        self.lista_viviendas.column("Descripción", width=300, anchor='w')
        self.lista_viviendas.column("Precio", width=100, anchor='center')
        self.lista_viviendas.column("Ubicación", width=200, anchor='w')

        # Añadir un scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.lista_viviendas.yview)
        self.lista_viviendas.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # Frame para los botones
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.pack(fill=tk.X, pady=10)

        # Botones con estilo ttkbootstrap
        boton_añadir = ttk.Button(button_frame, text="Añadir Vivienda", command=self.abrir_ventana_nueva_vivienda, bootstyle="success")
        boton_añadir.pack(side=tk.LEFT, padx=5)

        boton_eliminar = ttk.Button(button_frame, text="Eliminar Vivienda", command=self.eliminar_vivienda, bootstyle="danger")
        boton_eliminar.pack(side=tk.LEFT, padx=5)

        boton_generar = ttk.Button(button_frame, text="Generar Video", command=self.generar_video, bootstyle="info")
        boton_generar.pack(side=tk.LEFT, padx=5)

        boton_salir = ttk.Button(button_frame, text="Salir", command=self.quit, bootstyle="secondary")
        boton_salir.pack(side=tk.LEFT, padx=5)

        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.X, pady=10)

        # Cargar las viviendas
        self.cargar_viviendas()

    def cargar_viviendas(self):
        self.limpiar_treeview()
        viviendas = manejo_archivos.leer_viviendas()
        for index, vivienda in enumerate(viviendas):
            item_id = self.lista_viviendas.insert("", tk.END, values=vivienda, tags=('evenrow',) if index % 2 == 0 else ('oddrow',))

        # Alternar colores de las filas
        self.lista_viviendas.tag_configure('evenrow', background='#DDEEFF', foreground='#000000')
        self.lista_viviendas.tag_configure('oddrow', background='#BBDDFF', foreground='#000000')

    def limpiar_treeview(self):
        for item in self.lista_viviendas.get_children():
            self.lista_viviendas.delete(item)

    def abrir_ventana_nueva_vivienda(self):
        VentanaNuevaVivienda(self)

    def eliminar_vivienda(self):
        selected_item = self.lista_viviendas.selection()[0]
        vivienda_id = self.lista_viviendas.item(selected_item, "values")[0]
        manejo_archivos.eliminar_vivienda(vivienda_id)
        self.lista_viviendas.delete(selected_item)

    def generar_video(self):
        generador_video.generar_video(self)