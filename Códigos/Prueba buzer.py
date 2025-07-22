from machine import Pin, PWM
import time

# Configurar buzzer
buzzer = PWM(Pin(4))

def tocar_tono(frecuencia, duracion):
    buzzer.freq(frecuencia)
    buzzer.duty_u16(32768)  # 50% duty cycle
    time.sleep(duracion)
    buzzer.duty_u16(0)      # Apagar

print("=== BUZZER PASIVO ===")
print("Tocando tonos de prueba...")

# Tocar 3 tonos diferentes
tonos = [500, 1000, 1500]  # Hz

for i, freq in enumerate(tonos):
    print(f"Tono {i+1}: {freq} Hz")
    tocar_tono(freq, 1)
    time.sleep(0.5)

print("Prueba completada")
buzzer.deinit()

"""
INTERPRETACIÓN DE RESULTADOS:

Buzzer:
✓ Funciona: Escuchas 3 tonos diferentes
✗ No funciona: Silencio total

