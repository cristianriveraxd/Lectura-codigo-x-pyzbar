from gpiozero import LED
from time import sleep

pin = LED(18)  # Asegúrate de que este es el pin que usas

print("Encendiendo el pin por 3 segundos...")
pin.on()
sleep(3)

print("Apagando el pin...")
pin.off()
