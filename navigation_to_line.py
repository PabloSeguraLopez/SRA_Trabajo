#!/usr/bin/env python3
from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_A
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from time import sleep
import math
from basic_functions import *

def angle_to_line(first_obstacle_distance, second_obstacle_distance, distance_between_obstacles=50):
    numerador = (second_obstacle_distance**2 - first_obstacle_distance**2 - distance_between_obstacles**2) / (distance_between_obstacles*2)
    
    denominador = math.sqrt(first_obstacle_distance**2 - (numerador)**2)
    
    # Calcula el arcotangente y convierte a grados
    alfa = math.atan(numerador / denominador) * (180 / math.pi)
    
    return alfa

def go_to_line(left_motor, right_motor, color_sensor, angle_to_line):
    # Gira hacia la línea
    girar_grados(angle_to_line, left_motor, right_motor, velocidad=20)
    # Avanza hasta la línea hasta que la detecte con el sensor de color
    left_motor.on(SpeedPercent(20), block=False)
    right_motor.on(SpeedPercent(20), block=False)
    while color_sensor.color != 1:
        continue
    left_motor.off()
    right_motor.off()
    # Tras detectar la línea, avanza para que ésta esté en el centro de gravedad del robot
    avanzar_cm(5, left_motor, right_motor, velocidad=20)

def go_to_gap(first_obstacle_distance, second_obstacle_distance, angle_between_obstacles, left_motor, right_motor, color_sensor):
    go_to_line(left_motor, right_motor, color_sensor, angle_between_obstacles/2)


