from machine import Pin, PWM, time_pulse_us
import time
from time import sleep  

# Pines
TRIG = Pin(32, Pin.OUT)
ECHO = Pin(33, Pin.IN)
BUZZER = PWM(Pin(13), freq=1000, duty=0)
MOTOR = PWM(Pin(27), freq=1000, duty=0)
BUTTON = Pin(5, Pin.IN, Pin.PULL_UP)

# Estado del sistema
sistema_encendido = False 

# Función para medir la distancia
def medir_distancia():
    """Mide la distancia en cm"""
    # Pulso de trigger
    TRIG.off()
    time.sleep_us(2)
    TRIG.on()
    time.sleep_us(10)
    TRIG.off()
    
    # Medir tiempo de respuesta
    try:
        duration = time_pulse_us(ECHO, 1, 30000)
        if duration < 0:
            return None  # Timeout
        
        # Calcular distancia (velocidad sonido = 343 m/s)
        distance = (duration * 0.034) / 2
        return distance
    except:
        return None

# Función para leer el botón con debounce
def leer_boton():
    """Lee el estado del botón y cambia el estado del sistema"""
    global sistema_encendido
    
    # Si el botón está presionado (valor 0 porque usa PULL_UP)
    if BUTTON.value() == 0:
        if not sistema_encendido:
            sistema_encendido = True
            print("=== Sistema ACTIVADO ===")
        sleep(0.05)  # Debounce simple
    else:
        if sistema_encendido:
            sistema_encendido = False
            print("=== Sistema DESACTIVADO ===")
            # Apagar salidas cuando se desactiva
            BUZZER.duty(0)
            MOTOR.duty(0)
def actualizar_salida(distancia):
    # ← AGREGADO: Validación para evitar el error
    if distancia is None:
        print("Error: Lectura de sensor inválida")
        BUZZER.duty(0)
        MOTOR.duty(0)
        return
    
    if distancia < 50:  # Cerquita
        BUZZER.duty(512)
        BUZZER.freq(2000)  # Frecuencia alta
        MOTOR.duty(800)    # Vibración fuerte
    elif distancia < 130:  # Medio- medio
        BUZZER.duty(256)
        BUZZER.freq(1000)  # Frecuencia media
        MOTOR.duty(400)    # Vibración media
    else:  # Muy lejos
        BUZZER.duty(0)
        MOTOR.duty(0)    # Vibración suave

# Bucle principal
while True:
    # Leer el estado del botón
    leer_boton()
    
    if sistema_encendido:
        distancia = medir_distancia()
        print("Distancia: ", distancia)
        actualizar_salida(distancia)
    else:
        # Asegurar que las salidas estén apagadas cuando el sistema está inactivo
        BUZZER.duty(0)
        MOTOR.duty(0)
    
    sleep(0.1)