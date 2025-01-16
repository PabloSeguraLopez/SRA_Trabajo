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


# Función para avanzar
def avanzar_cm(distancia, left_motor, right_motor, velocidad=20):
    # Cálculos
    grados = (distancia / circunferencia_rueda) * 360  # grados para cada rueda
    # Movimiento
    left_motor.on_for_degrees(speed=velocidad, degrees=grados, brake=True, block=False)
    right_motor.on_for_degrees(speed=velocidad, degrees=grados, brake=True, block=True)
    evade_correcting_angle(left_motor, right_motor)

# Función para girar a la derecha 90º
def girar_grados(angulo_giro, left_motor, right_motor, velocidad=20):
    # Cálculos
    distancia_giro_90 = (pi * ancho_robot) / (360/angulo_giro)
    grados = ((distancia_giro_90 / circunferencia_rueda) * 360)  # grados para cada rueda
    # Movimiento
    left_motor.on_for_degrees(speed=velocidad, degrees=grados, brake=True, block=False)
    right_motor.on_for_degrees(speed=velocidad, degrees=-grados, brake=True, block=True)
    evade_correcting_angle(left_motor, right_motor)

def evade_correcting_angle(left_motor, right_motor):
    left_motor.reset()
    right_motor.reset()
    return

def start_program(leds,spkr):
    spkr.beep()
    leds.set_color('LEFT', 'AMBER')
    leds.set_color('RIGHT', 'AMBER')
def end_program(leds,spkr):
    spkr.beep()
    leds.set_color('LEFT', 'GREEN')
    leds.set_color('RIGHT', 'GREEN')
    while True:
        continue
