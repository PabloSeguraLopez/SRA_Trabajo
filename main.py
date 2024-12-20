#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_A
from ev3dev2.motor import SpeedPercent
from time import sleep
from math import pi

# Definición de los motores
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)

# Parámetros físicos
diametro_rueda = float(5.6) 
ancho_robot = float(11.8)      # De mitad de rueda a mitad de rueda
lado_cuadrado = float(50) 

# Cálculos
circunferencia_rueda = float(pi) * diametro_rueda  
grados_para_50cm = (lado_cuadrado / circunferencia_rueda) * 360  # grados

# Distancia a recorrer para un giro de 90º en el sitio
distancia_giro_90 = (pi * ancho_robot) / 4  
grados_giro_90 = ((distancia_giro_90 / circunferencia_rueda) * 360)  # grados para cada rueda. Dividimos entre dos porque se mueven ambas ruedas

# Función para avanzar una distancia (cm)
def avanzar_distancia(grados, velocidad=20):
    left_motor.on_for_degrees(speed=velocidad, degrees=grados, brake=True, block=False)
    right_motor.on_for_degrees(speed=velocidad, degrees=grados, brake=True, block=True)
    evade_correcting_angle()

# Función para girar a la izquierda 90º
def girar_izquierda_90(grados, velocidad=20):
    # El motor derecho avanza y el izquierdo retrocede para girar en el lugar
    left_motor.on_for_degrees(speed=velocidad, degrees=-grados, brake=True, block=False)    # Grados negativos para girar a la izquierda
    right_motor.on_for_degrees(speed=velocidad, degrees=grados, brake=True, block=True)     # Grados positivos para girar a la izquierda
    evade_correcting_angle()

def evade_correcting_angle():
    left_motor.reset()
    right_motor.reset()
    return

# Hacerlo 4 veces
for _ in range(4):
    avanzar_distancia(grados_para_50cm, velocidad=20)  # Avanzar 50 cm
    girar_izquierda_90(grados_giro_90, velocidad=20)  # Girar a la izquierda 90º