#!/usr/bin/env python3
from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_A
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from time import sleep
import math
from basic_functions import *

# Función para calcular el ángulo al que se encuentra la línea, dados dos obstáculos
def angle_to_line(first_obstacle_distance, second_obstacle_distance, distance_between_obstacles=50):
    # Usamos la fórmula (descrita en la memoria) para determinar la posición relativa (beta) en base a las distancias h1 y h2
    numerador = (second_obstacle_distance**2 - first_obstacle_distance**2 - distance_between_obstacles**2) / (distance_between_obstacles*2)
    
    # Calculamos la parte del denominador para la fórmula
    denominador = math.sqrt(first_obstacle_distance**2 - (numerador)**2)
    
     # Calcula el arcotangente y lo convierte a grados
    beta = math.degrees(math.atan(numerador / denominador))
    
    return beta

# Función para calcular el ángulo de corrección tras un pequeño movimiento hacia la lata
def angle_to_obstacle_after_movement(obstacle_distance, distance_moved, angle_moved):
    # Calcula el ángulo adicional usando la ley del seno inverso (asin) y la ley de cosenos 
    other_angle = math.degrees(math.asin(distance_moved * math.sin(math.radians(angle_moved)/math.sqrt(obstacle_distance**2 + distance_moved**2 - 2*obstacle_distance*distance_moved*math.cos(math.radians(angle_moved))))))

    return abs(180 - (180 - abs(angle_moved) - abs(other_angle)))

# Función para comprobar si el ángulo detectado indica que estamos entre dos obstáculos
def is_between_obstacles(angle_between_obstacles, distance_from_second_obstacle, distance_between_obstacles=40):
    # Calculamos un ángulo usando la ley del seno, asumiendo que distance_between_obstacles es la distancia entre las dos latas
    first_obstacle_angle = math.degrees(math.asin(distance_from_second_obstacle * math.sin(math.radians(abs(angle_between_obstacles)))/distance_between_obstacles))
    # Devolvemos True si ese ángulo es menor de 90 (significa que estamos en el hueco entre latas)
    return abs(first_obstacle_angle) < 90

# Función para ir a la línea, girando el ángulo calculado y avanzando hasta detectar color = 1
def go_to_line(left_motor, right_motor, color_sensor, angle_to_line):
    # Giramos hacia la línea
    girar_grados(angle_to_line, left_motor, right_motor, velocidad=20)

    # Avanzamos hasta que el sensor de color detecte la línea
    left_motor.on(SpeedPercent(20), block=False)
    right_motor.on(SpeedPercent(20), block=False)
    while color_sensor.color != 1:
        continue

    left_motor.off()
    right_motor.off()
    # Tras detectar la línea, avanza para que ésta esté en el centro de gravedad del robot
    avanzar_cm(5, left_motor, right_motor, velocidad=20)

# Función para cuando detectamos un hueco entre dos latas y queremos dirigirnos a la línea
def go_to_gap(angle_between_obstacles, left_motor, right_motor, color_sensor):
    # Dividimos el ángulo entre obstáculos entre 2, para apuntar al medio
    go_to_line(left_motor, right_motor, color_sensor, angle_between_obstacles/2)


