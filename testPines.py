import RPi.GPIO as GPIO
import time

# Lista de pines GPIO disponibles en Raspberry Pi (sin contar alimentación y tierra)
GPIO_PINS = [18,18,18,18,18]

# Configura el modo de numeración de pines
GPIO.setmode(GPIO.BCM)

# Configura todos los pines como salidas
for pin in GPIO_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

print("Iniciando prueba de pines GPIO...")

try:
    while True:
        for pin in GPIO_PINS:
            print(f"Encendiendo GPIO {pin}")
            GPIO.output(pin, GPIO.HIGH)  # Enciende el pin
            time.sleep(5)  # Espera medio segundo
            print(f"Apagando GPIO {pin}")
            GPIO.output(pin, GPIO.LOW)  # Apaga el pin
            time.sleep(5)  # Espera medio segundo
            
except KeyboardInterrupt:
    print("\nPrueba interrumpida por el usuario. Limpiando GPIO...")
    GPIO.cleanup()  # Limpia los GPIO al finalizar
    print("GPIO restaurados. Saliendo.")

