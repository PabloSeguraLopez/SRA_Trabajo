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
    beta = math.degrees(math.atan(numerador / denominador))
    
    return beta

def angle_to_obstacle_after_movement(obstacle_distance, distance_moved, angle_moved):
    other_angle = math.degrees(math.asin(distance_moved * math.sin(math.radians(angle_moved)/math.sqrt(obstacle_distance**2 + distance_moved**2 - 2*obstacle_distance*distance_moved*math.cos(math.radians(angle_moved))))))
    return abs(180 - (180 - abs(angle_moved) - abs(other_angle)))

def is_between_obstacles(angle_between_obstacles, distance_from_second_obstacle, distance_between_obstacles=40):
    first_obstacle_angle = math.degrees(math.asin(distance_from_second_obstacle * math.sin(math.radians(abs(angle_between_obstacles)))/distance_between_obstacles))
    return abs(first_obstacle_angle) < 90

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

def go_to_gap(angle_between_obstacles, left_motor, right_motor, color_sensor):
    go_to_line(left_motor, right_motor, color_sensor, angle_between_obstacles/2)


