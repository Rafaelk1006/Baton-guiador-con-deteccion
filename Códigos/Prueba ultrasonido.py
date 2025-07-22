from machine import Pin, time_pulse_us
import time

# Configurar pines
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)

def medir_distancia():
    # Pulso trigger
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()
    
    # Medir tiempo echo
    try:
        duration = time_pulse_us(echo, 1, 30000)
        if duration > 0:
            distance = (duration * 0.034) / 2
            return distance
        else:
            return None
    except:
        return None

print("=== SENSOR ULTRASONICO HC-SR04 ===")
print("Midiendo distancia continuamente...")
print("Presiona Ctrl+C para salir\n")

try:
    while True:
        distancia = medir_distancia()
        
        if distancia is not None:
            print(f"Distancia: {distancia:.1f} cm")
        else:
            print("ERROR: Sin lectura")
        
        time.sleep(0.5)
        
except KeyboardInterrupt:
    print("\nMedición terminada")