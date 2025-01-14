#!/usr/bin/env python3
from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_A
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from time import sleep
from math import pi
from basic_functions import *

# Definición de motores y sensores
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)
spkr = Sound()
ultrasonic = UltrasonicSensor(INPUT_2)

# Inicio del programa
spkr.beep()
while True:
    # Detectar objetos con el sensor de ultrasonido
    distancia = ultrasonic.distance_centimeters
    if distancia < 20:  # Si la distancia al objeto es menor a 20 cm
        avanzar_cm(distancia - 5, left_motor, right_motor, velocidad=20)  # Acércate hasta 5 cm de la lata
        rodear_lata(left_motor, right_motor)
        break
    else:
        avanzar_cm(5, left_motor, right_motor, velocidad=20)  # Avanza mientras no detecta un objeto
spkr.beep()