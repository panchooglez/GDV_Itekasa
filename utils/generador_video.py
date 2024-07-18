import os
import cv2
from moviepy.editor import *
from moviepy.config import change_settings
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from utils.video_vivienda import crear_video_vivienda
from utils.dirs import obtener_directorio_escritorio, obtener_ruta

def concatenar_videos(videos, output):
    # Abrir el primer video para obtener las propiedades (ancho, alto, fps)
    cap = cv2.VideoCapture(videos[0])
    if not cap.isOpened():
        print(f"Error al abrir el video {videos[0]}")
        return
    
    # Obtener propiedades del video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    
    # Crear un VideoWriter para el video de salida
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output, fourcc, fps, (width, height))
    
    # Leer y escribir los frames de cada video
    for video in videos:
        cap = cv2.VideoCapture(video)
        if not cap.isOpened():
            print(f"Error al abrir el video {video}")
            continue
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        
        cap.release()
    
    out.release()

def generar_video(ventana):

    # Configurar la barra de progreso
    ventana.progress["value"] = 0
    ventana.progress["maximum"] = 100  # Ajusta esto según el número de pasos

    # Ruta del archivo de inicio y del CSV con los datos de las viviendas
    #inicio_video_path = "assets/inicio.mp4"
    #logo_path = "assets/logo.png"
    viviendas_csv_path = obtener_ruta(".LED/datos/viviendas.csv")
    
    # Leer el archivo CSV
    df = pd.read_csv(viviendas_csv_path)

    clips = [obtener_ruta('.LED/assets/inicio.mp4')]

    ventana.progress['value'] += 10
    ventana.update_idletasks()

    n_viviendas = df.shape[0]
    
    # Crear un clip para cada vivienda
    for index, row in df.iterrows():
        descripcion = row["Descripcion"]
        precio = row["Precio"]
        ubicacion = row["Ubicacion"]
        ruta_imagen = row["Foto"]

        nombre_video = obtener_ruta(f".LED/assets/output_video_{index}.mp4")

        crear_video_vivienda(nombre_video, [descripcion, ubicacion, str(precio)], obtener_ruta(ruta_imagen), obtener_ruta('.LED/assets/bg.png'))

        clips.append(nombre_video)
        ventana.progress['value'] += 80 / n_viviendas
        ventana.update_idletasks()

    clips.append(obtener_ruta('.LED/assets/final.mp4'))

    #concatenar_videos(clips, os.path.join(obtener_directorio_escritorio(), 'output_video.mp4'))
    concatenar_videos(clips, '../output_video.mp4')

    for i in range(0, len(clips)-2):
        os.remove(obtener_ruta(f".LED/assets/output_video_{i}.mp4"))

    ventana.progress['value'] = 100
    ventana.update_idletasks()