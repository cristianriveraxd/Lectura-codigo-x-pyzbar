import cv2
import RPi.GPIO as GPIO
from pyzbar.pyzbar import decode
from datetime import datetime
import threading
from controller import obtener_codigo_barras

# Configuración del GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ALERTA_PIN = 18  # PIN SALIDA
GPIO.setup(ALERTA_PIN, GPIO.OUT)
GPIO.output(ALERTA_PIN, GPIO.LOW)  # Inicialmente apagado

# Inicializa la captura de video
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se puede abrir la cámara")
    exit()

# Aumentamos la resolución para mejorar la detección
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)



# Proceso de frame
def process_frame(frame):
    
    # Código de barras esperado
    codigo_bd = obtener_codigo_barras()
    codigo_programado = str(codigo_bd[0])
    
    barcodes = decode(frame)
    i = 0
    for barcode in barcodes:
        if barcode.type == "CODE128":
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            lectura=barcode_value = barcode.data.decode("utf-8")
            leido=str(lectura)
            cv2.putText(frame, barcode_value, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            print('Código de barras leído:', barcode_value)
            print('Código de barras obtenido:', codigo_programado)
            
            
            if leido.strip() != codigo_programado.strip():
                print('¡Producto incorrecto detectado!')
                tomar_foto(frame)
                activar_alerta()
            else:
                print(f'Producto correcto #{i}')
                
            i += 1
                
                

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
    
#Eliminar espacios en blanco de codigo
def tratar_codigo(codigo: str) -> str:
    return codigo.replace(" ","")
    

while cap.isOpened():
    success, frame = cap.read()
    
    if not success:
        print("Error: No se puede recibir el frame (stream end?). Exiting ...")
        break

    thread = threading.Thread(target=process_frame, args=(frame,))
    thread.start()
    
    cv2.imshow("Lector", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):  # Reset de la alarma con la tecla espacio
        print("🔇 Alarma desactivada")
        desactivar_alerta() # Apaga la alarma

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
