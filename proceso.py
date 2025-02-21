import cv2

# Ruta del video cargado
video_path = "/mnt/data/Video de WhatsApp 2025-02-21 a las 07.31.51_6cfe3e49.mp4"

# Abrir el video
cap = cv2.VideoCapture(video_path)

# Obtener información del video
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
duration = frame_count / fps

# Obtener resolución
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Información del video
video_info = {
    "Total de Frames": frame_count,
    "FPS": fps,
    "Duración (segundos)": duration,
    "Resolución": f"{width}x{height}"
}

# Liberar recursos
cap.release()

# Mostrar la información
video_info



