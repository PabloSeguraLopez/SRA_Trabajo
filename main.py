#!/usr/bin/env python3
from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_A
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from time import sleep
from math import pi

# Definición de motores y sensores
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)
spkr = Sound()
ultrasonic = UltrasonicSensor(INPUT_2)
# Parámetros físicos
diametro_rueda = float(5.6) 
ancho_robot = float(12.3192)      # Ancho del robot corregido
circunferencia_rueda = float(pi) * diametro_rueda  # Circunferencia de la rueda

# Función para avanzar
def avanzar_cm(distancia, velocidad=20):
    # Cálculos
    grados = (distancia / circunferencia_rueda) * 360  # grados para cada rueda
    # Movimiento
    left_motor.on_for_degrees(speed=velocidad, degrees=grados, brake=True, block=False)
    right_motor.on_for_degrees(speed=velocidad, degrees=grados, brake=True, block=True)
    evade_correcting_angle()

# Función para girar a la derecha 90º
def girar_grados(angulo_giro, velocidad=20):
    # Cálculos
    distancia_giro_90 = (pi * ancho_robot) / (360/angulo_giro)
    grados = ((distancia_giro_90 / circunferencia_rueda) * 360)  # grados para cada rueda
    # Movimiento
    left_motor.on_for_degrees(speed=velocidad, degrees=grados, brake=True, block=False)
    right_motor.on_for_degrees(speed=velocidad, degrees=-grados, brake=True, block=True)
    evade_correcting_angle()

def evade_correcting_angle():
    left_motor.reset()
    right_motor.reset()
    return


# Función para rodear una lata
def rodear_lata():
    # Supongamos que la lata tiene un diámetro aproximado de 7 cm
    diametro_lata = 7.0
    distancia_alrededor = pi * (ancho_robot + diametro_lata)  # Circunferencia del rodeo
    avanzar_cm(distancia_alrededor / 4, velocidad=20)  # Avanza un cuarto del círculo
    girar_grados(90, velocidad=20)  # Gira 90 grados
    avanzar_cm(distancia_alrededor / 4, velocidad=20)  # Avanza otro cuarto
    girar_grados(90, velocidad=20)  # Gira 90 grados
    avanzar_cm(distancia_alrededor / 4, velocidad=20)  # Avanza otro cuarto
    girar_grados(90, velocidad=20)  # Gira 90 grados
    avanzar_cm(distancia_alrededor / 4, velocidad=20)  # Completa el rodeo

## Inicio del programa
#spkr.beep()
#while True:
    ## Detectar objetos con el sensor de ultrasonido
    #distancia = ultrasonic.distance_centimeters
    #if distancia < 20:  # Si la distancia al objeto es menor a 20 cm
        #avanzar_cm(distancia - 5, velocidad=20)  # Acércate hasta 5 cm de la lata
        #rodear_lata()
        #break
    #else:
        #avanzar_cm(5, velocidad=20)  # Avanza mientras no detecta un objeto
#spkr.beep()
while True:
    print(ultrasonic.distance_centimeters)