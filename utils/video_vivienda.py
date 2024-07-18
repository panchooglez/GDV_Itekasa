import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap

def wrap_text(text, font, max_width):
    """
    Inserta saltos de línea en el texto para que se ajuste al ancho máximo especificado.

    Parameters:
    - text: Texto original sin saltos de línea.
    - font: Objeto de fuente PIL utilizado para medir el texto.
    - max_width: Ancho máximo en píxeles para cada línea de texto.

    Returns:
    - Texto con saltos de línea insertados.
    """
    if not isinstance(text, str):
        text = str(text)

    wrapped_text = ""
    lines = textwrap.wrap(text, width=40)  # Ajusta este valor según sea necesario

    for line in lines:
        line_width = font.getbbox(line)[2] - font.getbbox(line)[0]
        if line_width > max_width:
            words = line.split()
            line = ""
            for word in words:
                test_line = f"{line} {word}".strip()
                test_line_width = font.getbbox(test_line)[2] - font.getbbox(test_line)[0]
                if test_line_width <= max_width:
                    line = test_line
                else:
                    wrapped_text += f"{line}\n"
                    line = word
            wrapped_text += f"{line}\n"
        else:
            wrapped_text += f"{line}\n"
    
    return wrapped_text.strip()

def calculate_text_height(text, font):
    """
    Calcula la altura total del texto envuelto en múltiples líneas.

    Parameters:
    - text: Texto con saltos de línea.
    - font: Objeto de fuente PIL utilizado para medir el texto.

    Returns:
    - Altura total del texto en píxeles.
    """
    lines = text.split('\n')
    height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)
    return height

def draw_multicolor_text(draw, text, position, font, default_fill, color_ranges):
    """
    Dibuja texto con múltiples colores.

    Parameters:
    - draw: Objeto ImageDraw.
    - text: Texto a dibujar.
    - position: Posición (x, y) para el texto.
    - font: Objeto de fuente PIL.
    - default_fill: Color por defecto para el texto.
    - color_ranges: Lista de tuplas (start, end, color) para colorear rangos específicos.
    """
    x, y = position
    for i, char in enumerate(text):
        char_fill = default_fill
        for start, end, color in color_ranges:
            if start <= i < end:
                char_fill = color
                break
        draw.text((x, y), char, font=font, fill=char_fill)
        x += font.getbbox(char)[2] - font.getbbox(char)[0]

def format_price(price):
    """
    Formatea el precio para incluir puntos como delimitadores de miles.

    Parameters:
    - price: Precio como string o número.

    Returns:
    - Precio formateado como string con delimitadores de miles.
    """
    if isinstance(price, str):
        price = float(price.replace(',', '').replace('€', '').strip())
    return "{:,.0f}".format(price).replace(',', '.')

def crear_video_vivienda(output_video, text_strings, sliding_image_path, background_path, width=848, height=480, fps=30, duration=18, font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size=35):
    """
    Crea un video con textos deslizantes y una imagen deslizante sobre un fondo fijo.

    Parameters:
    - output_video: Ruta del archivo de video de salida.
    - text_strings: Lista de strings con los textos que aparecerán en pantalla.
    - sliding_image_path: Ruta de la imagen que se desliza.
    - background_path: Ruta de la imagen de fondo.
    - width: Ancho del video (por defecto 1920).
    - height: Alto del video (por defecto 1080).
    - fps: Frames por segundo (por defecto 30).
    - duration: Duración del video en segundos (por defecto 10).
    - font_path: Ruta de la fuente (por defecto DejaVuSans-Bold.ttf).
    - font_size: Tamaño de la fuente (por defecto 70).
    """
    
    # Cargar la imagen de fondo y redimensionarla
    background_image = Image.open(background_path).resize((width, height)).convert("RGBA")

    # Cargar y redimensionar la imagen que se desliza
    sliding_image = Image.open(sliding_image_path).convert("RGBA")
    image_width, image_height = sliding_image.size
    max_image_width = width * 2 // 5  # Tamaño máximo de la imagen, ahora la mitad del ancho del video
    max_image_height = height * 3 // 4  # Tamaño máximo de la imagen, ahora dos tercios de la altura del video

    # Redimensionar manteniendo la relación de aspecto
    aspect_ratio = image_width / image_height
    if image_width > max_image_width:
        image_width = max_image_width
        image_height = int(image_width / aspect_ratio)
    if image_height > max_image_height:
        image_height = max_image_height
        image_width = int(image_height * aspect_ratio)
    
    sliding_image = sliding_image.resize((image_width, image_height))

    # Calcular la cantidad de frames totales y la duración del desvanecimiento en frames
    total_frames = int(fps * duration)
    fade_frames = int(2 * fps)  # Duración del desvanecimiento en segundos
    fade_start_frame = total_frames - fade_frames

    # Crear el video usando OpenCV
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    def interpolate(start_pos, end_pos, progress):
        """Interpolar entre dos posiciones según el progreso."""
        return (int(start_pos[0] + (end_pos[0] - start_pos[0]) * progress),
                int(start_pos[1] + (end_pos[1] - start_pos[1]) * progress))

    def draw_multiline_text(draw, text, position, font, fill="black"):
        """Dibuja texto en múltiples líneas."""
        lines = text.split('\n')
        x, y = position
        for line in lines:
            draw.text((x, y), line, font=font, fill=fill)
            y += font.getbbox(line)[3]  # Incrementa y según la altura de la línea

    # Cargar la fuente para calcular el tamaño del texto
    font = ImageFont.truetype(font_path, font_size)
    
    # Ajustar textos con prefijos y colores
    text_descripcion = text_strings[0]
    text_ubicacion = f"Dirección: {text_strings[1]}"
    text_precio_num = format_price(text_strings[2])
    text_precio = f"Precio: {text_precio_num} €"

    text_strings = [text_descripcion, text_precio, text_ubicacion]
    
    # Envuelve el texto y calcula la altura
    num_texts = len(text_strings)
    wrapped_texts = [wrap_text(text, font, width // 2) for text in text_strings]
    heights = [calculate_text_height(text, font) for text in wrapped_texts]

    total_height = sum(heights)
    initial_y = (height - total_height) // (num_texts + 1)  # Espacio inicial y entre textos

    texts = []
    current_y = initial_y + 100  # Ajustar para más distancia del margen superior
    for i, wrapped_text in enumerate(wrapped_texts):
        texts.append({
            "text": wrapped_text,
            "start_pos": (width // 4, height + 100),  # Posición inicial para deslizamiento desde abajo
            "end_pos": (width // 18, current_y - 40),  # Mucho más cerca del margen izquierdo
            "start_time": 0.5 + 0.5 * i,
            "slide_duration": 3,
            "is_price": i == 1
        })
        current_y += heights[i] + initial_y // 2  # Menor espacio entre textos

    # Generar cada frame del video
    for frame_count in range(total_frames):
        # Crear una imagen PIL desde el fondo para agregar textos
        img_pil = background_image.copy()
        draw = ImageDraw.Draw(img_pil)

        # Agregar cada texto según la interpolación de su posición
        for text_info in texts:
            start_frame = int(text_info["start_time"] * fps)
            slide_frames = int(text_info["slide_duration"] * fps)
            end_frame = start_frame + slide_frames

            if start_frame <= frame_count < end_frame:
                progress = (frame_count - start_frame) / slide_frames
                pos = interpolate(text_info["start_pos"], text_info["end_pos"], progress)
                if text_info["is_price"]:
                    # Dibujar texto con colores múltiples
                    draw_multicolor_text(draw, text_info["text"], pos, font, "black", [(7, len(text_info["text"]) - 2, "red")])
                else:
                    draw_multiline_text(draw, text_info["text"], pos, font)
            elif frame_count >= end_frame and frame_count < fade_start_frame:
                pos = text_info["end_pos"]
                if text_info["is_price"]:
                    draw_multicolor_text(draw, text_info["text"], pos, font, "black", [(7, len(text_info["text"]) - 2, "red")])
                else:
                    draw_multiline_text(draw, text_info["text"], pos, font)

        # Agregar la imagen deslizante según la interpolación de su posición
        image_start_frame = int(0.5 * fps)  # Tiempo de inicio de la imagen
        image_slide_duration = 3  # Duración del deslizamiento de la imagen en segundos
        image_slide_frames = int(image_slide_duration * fps)
        image_end_frame = image_start_frame + image_slide_frames

        image_final_x = width - image_width - 20  # Ajustar margen derecho
        image_final_y = (height - image_height) // 2  # Centrar verticalmente

        if image_start_frame <= frame_count < image_end_frame:
            progress = (frame_count - image_start_frame) / image_slide_frames
            image_pos = interpolate((width, height // 2), (image_final_x, image_final_y), progress)
            img_pil.paste(sliding_image, image_pos, sliding_image)
        elif frame_count >= image_end_frame and frame_count < fade_start_frame:
            img_pil.paste(sliding_image, (image_final_x, image_final_y), sliding_image)

        # Aplicar desvanecimiento al final
        if frame_count >= fade_start_frame:
            alpha = int(255 * (1 - (frame_count - fade_start_frame) / fade_frames))
            overlay = Image.new('RGBA', img_pil.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            # Desvanecer textos
            for text_info in texts:
                pos = text_info["end_pos"]
                if text_info["is_price"]:
                    draw_multicolor_text(overlay_draw, text_info["text"], pos, font, (0, 0, 0, alpha), [(7, len(text_info["text"]) - 2, (255, 0, 0, alpha))])
                else:
                    draw_multiline_text(overlay_draw, text_info["text"], pos, font, fill=(0, 0, 0, alpha))
            
            # Desvanecer imagen
            sliding_image_with_alpha = sliding_image.copy()
            sliding_image_with_alpha.putalpha(alpha)
            overlay.paste(sliding_image_with_alpha, (image_final_x, image_final_y), sliding_image_with_alpha)
            
            img_pil = Image.alpha_composite(img_pil, overlay)

        # Convertir la imagen PIL de vuelta a un frame OpenCV
        frame = cv2.cvtColor(np.array(img_pil.convert("RGB")), cv2.COLOR_RGB2BGR)
        out.write(frame)

    # Liberar el video
    out.release()
    cv2.destroyAllWindows()
