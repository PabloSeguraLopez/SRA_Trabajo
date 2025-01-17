from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_A
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from time import sleep
from math import pi

# Parámetros físicos
diametro_rueda = float(5.6) 
ancho_robot = float(12.3192)      # Ancho del robot corregido
circunferencia_rueda = float(pi) * diametro_rueda  # Circunferencia de la rueda


# Función para avanzar en línea recta una distancia dada en centímetros
def avanzar_cm(distancia, left_motor, right_motor, velocidad=20):
    # Convertimos la distancia que se desea recorrer a grados que deben girar las ruedas
    grados = (distancia / circunferencia_rueda) * 360  # grados para cada rueda
    left_motor.on_for_degrees(speed=velocidad, degrees=grados, brake=True, block=False)
    right_motor.on_for_degrees(speed=velocidad, degrees=grados, brake=True, block=True)
    
    # Llamamos a la función para corregir ángulos tras el movimiento (resetea los motores)
    evade_correcting_angle(left_motor, right_motor)

# Función para girar un número de grados dado (positivo = giro a la derecha, negativo = giro a la izquierda)
def girar_grados(angulo_giro, left_motor, right_motor, velocidad=10):
    # Calculamos la distancia de la trayectoria de giro basándonos en el ancho del robot
    distancia_giro = (pi * ancho_robot) / (360/angulo_giro)
    # Calculamos los grados que deben girar las ruedas para producir el ángulo de giro deseado
    grados = ((distancia_giro / circunferencia_rueda) * 360)  # grados para cada rueda

    left_motor.on_for_degrees(speed=velocidad, degrees=grados, brake=True, block=False)
    right_motor.on_for_degrees(speed=velocidad, degrees=-grados, brake=True, block=True)
    
    evade_correcting_angle(left_motor, right_motor)

# Función para “evitar” que el robot acumule error de giro, resetea los contadores de los motores
def evade_correcting_angle(left_motor, right_motor):
    left_motor.reset()
    right_motor.reset()
    return

# Función para indicar el inicio del programa
def start_program(leds,spkr):
    spkr.beep()
    leds.set_color('LEFT', 'AMBER')
    leds.set_color('RIGHT', 'AMBER')
    print("Programa iniciado")

# Función para indicar el fin del programa
def end_program(leds,spkr):
    spkr.beep()
    leds.set_color('LEFT', 'GREEN')
    leds.set_color('RIGHT', 'GREEN')
    print("Programa terminado")