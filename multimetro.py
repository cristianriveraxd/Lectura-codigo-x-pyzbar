import pigpio

pi = pigpio.pi()
pin = 18

estado = pi.read(pin)
print(f"El estado del pin {pin} es: {'HIGH (5V)' if estado else 'LOW (0V)'}")
