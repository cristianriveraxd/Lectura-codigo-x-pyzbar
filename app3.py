import cv2
from pyzbar.pyzbar import decode
import RPi.GPIO as GPIO
import time
import threading

# Configuración del GPIO
ALARM_PIN = 18  # Pin de la alarma
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALARM_PIN, GPIO.OUT)
GPIO.output(ALARM_PIN, GPIO.LOW)  # Iniciar apagado

# Inicializa la cámara
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def detect_product(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total_area = sum(cv2.contourArea(c) for c in contours)
    return total_area > 5000  # Umbral para determinar si hay un producto

def process_frame(frame):
    has_product = detect_product(frame)
    barcodes = decode(frame)
    
    if has_product:
        barcode_detected = False
        for barcode in barcodes:
            if barcode.type == "CODE128":
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                barcode_value = barcode.data.decode("utf-8")
                cv2.putText(frame, barcode_value, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                print(f'Código CODE128 detectado: {barcode_value}')
                barcode_detected = True
                break
        
        if not barcode_detected:
            print("⚠️ Producto sin código de barras CODE128 ⚠️")
            GPIO.output(ALARM_PIN, GPIO.HIGH)  # Activar alarma

def capture_loop():
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Error en la captura de video.")
            break
        
        thread = threading.Thread(target=process_frame, args=(frame,))
        thread.start()
        
        cv2.imshow("Lector", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):  # Reset de la alarma con ESPACIO
            GPIO.output(ALARM_PIN, GPIO.LOW)
            print("Alarma reseteada")

    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()

# Iniciar el bucle de captura en un hilo
capture_thread = threading.Thread(target=capture_loop)
capture_thread.start()

