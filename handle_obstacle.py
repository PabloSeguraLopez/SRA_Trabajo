from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_A
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from time import sleep
import math
from basic_functions import *
from reconnaissance import *
from navigation_to_line import *

def keep_until_close_to_obstacle(left_motor, right_motor, ultrasonic_sensor, color_sensor):
    """
    Función que hace que el robot avance hasta que se encuentre a una distancia menor o igual a la indicada
    """
    while ultrasonic_sensor.distance_centimeters > 10:
        avanzar_cm(1, left_motor, right_motor)
        grados = 0
        while color_sensor.color != 1:
            grados += 5
            girar_grados(grados, left_motor, right_motor)
            girar_grados(-2*grados, left_motor, right_motor)
    return ultrasonic_sensor.distance_centimeters

def go_around_obstacle(left_motor, right_motor, ultrasonic_sensor, color_sensor, distance_to_obstacle):
    """
    Función que hace que el robot rodee un obstáculo
    """
    # Girar 90 grados a la derecha
    girar_grados(90, left_motor, right_motor)
    # Avanzar 20 cm
    avanzar_cm(10, left_motor, right_motor)
    # Girar 90 grados a la derecha
    girar_grados(-90, left_motor, right_motor)
    # Avanzar 20+10(diametro aproximado de la lata) cm
    avanzar_cm(30+ distance_to_obstacle, left_motor, right_motor)
    # Girar y avanzar hasta llegar a la línea
    alfa, h1, h2 = sweep(left_motor, right_motor, ultrasonic_sensor, -150, -30)
    go_to_gap(alfa, left_motor, right_motor, color_sensor)
    return distance_to_obstacle