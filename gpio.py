import cv2
import RPi.GPIO as GPIO
from pyzbar.pyzbar import decode
from datetime import datetime
import threading

# Configuración del GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ALERTA_PIN = 18  # Cambia al pin que estés usando
GPIO.setup(ALERTA_PIN, GPIO.OUT)
GPIO.output(ALERTA_PIN, GPIO.LOW)  # Inicialmente apagado

# Inicializa la captura de video
cap = cv2.VideoCapture("p1.mp4")

if not cap.isOpened():
    print("Error: No se puede abrir la cámara")
    exit()

# Aumentamos la resolución para mejorar la detección
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Código de barras esperado
codigo_correcto = "5094"

def process_frame(frame):
    barcodes = decode(frame)
    
    for barcode in barcodes:
        if barcode.type == "CODE128":
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            barcode_value = barcode.data.decode("utf-8")
            cv2.putText(frame, barcode_value, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            print('Código de barras leído:', barcode_value)
            
            if barcode_value != codigo_correcto:
                print('¡Producto incorrecto detectado!')
                tomar_foto(frame)
                activar_alerta()
            else:
                print('Producto correcto')
                desactivar_alerta()

def tomar_foto(frame):
    """Guarda una imagen cuando se detecta un código incorrecto."""
    time = datetime.now()
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"productos_truncados/producto_truncado_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Foto guardada: {filename}")

def activar_alerta():
    """Activa la salida digital en el GPIO (5V)."""
    GPIO.output(ALERTA_PIN, GPIO.HIGH)

def desactivar_alerta():
    """Desactiva la salida digital en el GPIO (0V)."""
    GPIO.output(ALERTA_PIN, GPIO.LOW)

while cap.isOpened():
    success, frame = cap.read()
    
    if not success:
        print("Error: No se puede recibir el frame (stream end?). Exiting ...")
        break

    thread = threading.Thread(target=process_frame, args=(frame,))
    thread.start()
    
    cv2.imshow("Lector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
