import cv2
from pyzbar.pyzbar import decode
import threading

# Inicializa la captura de video desde la cámara (índice 1)
cap = cv2.VideoCapture(0)

# Verifica si la cámara se abrió correctamente
if not cap.isOpened():
    print("Error: No se puede abrir la cámara")
    exit()

# Reduce la resolución del frame para acelerar el procesamiento
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def process_frame(frame):
    
    barcodes = decode(frame)
    
    for barcode in barcodes:
        if barcode.type == "CODE128":
            # Extrae las coordenadas para dibujar el rectángulo
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Decodifica el valor del código de barras
            barcode_value = barcode.data.decode("utf-8")
            cv2.putText(frame, barcode_value, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            print('Código de barras leído: ' + barcode_value)
            
            value = '5703'  
            
            if value != barcode_value:
                print('Producto truncado')
            else:
                print('Producto correcto')

while cap.isOpened():
    success, frame = cap.read()
    
    if not success:
        print("Error: No se puede recibir el frame (stream end?). Exiting ...")
        break
    
    # Crea y lanza un thread para procesar el frame
    thread = threading.Thread(target=process_frame, args=(frame,))
    thread.start()
    
    cv2.imshow("Lector", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
