import cv2

def save_last_frame(video_path, output_image_path):
    """
    Guarda el último fotograma de un video como una imagen.

    Parameters:
    - video_path: Ruta al archivo de video.
    - output_image_path: Ruta para guardar la imagen extraída.
    """
    # Abrir el video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error al abrir el video: {video_path}")
        return
    
    # Obtener el número total de fotogramas
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Número total de fotogramas en el video: {total_frames}")

    # Establecer el último fotograma
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)

    # Leer el último fotograma
    ret, frame = cap.read()
    if not ret:
        print(f"Error al leer el último fotograma.")
        cap.release()
        return

    # Guardar el último fotograma como una imagen
    cv2.imwrite(output_image_path, frame)
    print(f"Último fotograma guardado como {output_image_path}")

    # Liberar el video
    cap.release()

# Ruta del archivo de video
video_path = 'assets/inicio.mp4'

# Ruta para guardar la imagen del último fotograma
output_image_path = 'assets/bg.png'

# Guardar el último fotograma
save_last_frame(video_path, output_image_path)
