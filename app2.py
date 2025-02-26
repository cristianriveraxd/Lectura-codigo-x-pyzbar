import cv2
import time
import os
import threading
import RPi.GPIO as GPIO
from pyzbar.pyzbar import decode
from controller import obtener_codigo_barras

# Configuración del GPIO para la alarma
ALARM_PIN = 18  # Cambia esto si usas otro pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALARM_PIN, GPIO.OUT)
GPIO.output(ALARM_PIN, GPIO.LOW)  # Inicia apagada la alarma

# Configuración de la cámara
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Mayor resolución para mejor lectura
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Verificar si la cámara abrió correctamente
if not cap.isOpened():
    print("Error: No se puede abrir la cámara")
    exit()

# Código de barras correcto esperado
EXPECTED_BARCODE = "5183"

def save_photo(frame):
    """ Guarda una foto en una carpeta con la fecha y hora en el nombre """
    folder = "capturas"
    if not os.path.exists(folder):
        os.makedirs(folder)  # Crea la carpeta si no existe
    filename = time.strftime("%Y%m%d-%H%M%S") + ".jpg"
    filepath = os.path.join(folder, filename)
    cv2.imwrite(filepath, frame)
    print(f"Foto guardada: {filepath}")

def process_frame(frame):
    """ Procesa el frame para detectar códigos de barras """
    codigo_correcto = obtener_codigo_barras()
    barcodes = decode(frame)
    for barcode in barcodes:
        if barcode.type == "CODE128":
            x, y, w, h = barcode.rect
            barcode_value = barcode.data.decode("utf-8")

            # Dibujar rectángulo alrededor del código de barras
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, barcode_value, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            print(f"Código detectado: {barcode_value}")

            if barcode_value != EXPECTED_BARCODE:
                print("⚠ Producto incorrecto - Activando alarma y capturando imagen")
                GPIO.output(ALARM_PIN, GPIO.HIGH)  # Activa la alarma
                save_photo(frame)  # Guarda la imagen del producto incorrecto
            else:
                print("✅ Producto correcto")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Error: No se puede recibir el frame. Saliendo...")
        break

    # Procesar el frame en un hilo separado para no bloquear la cámara
    thread = threading.Thread(target=process_frame, args=(frame,))
    thread.start()

    cv2.imshow("Lector de Código de Barras", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Salir con la tecla 'q'
        break
    elif key == ord(' '):  # Reset de la alarma con la tecla espacio
        print("🔇 Alarma desactivada")
        GPIO.output(ALARM_PIN, GPIO.LOW)  # Apaga la alarma

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
