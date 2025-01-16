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

def keep_until_close_to_obstacle(left_motor, right_motor, ultrasonic_sensor, distance_to_obstacle):
    """
    Función que hace que el robot avance hasta que se encuentre a una distancia menor o igual a la indicada
    """
    threshold = 15
    while distance_to_obstacle > threshold:
        avanzar_cm(2, left_motor, right_motor)
        sleep(0.3)
        # Si deja de detectar el obstáculo es porque se ha desviado, hace un barrido.
        if ultrasonic_sensor.distance_centimeters > distance_to_obstacle:
            sweep(left_motor, right_motor, ultrasonic_sensor, -15, 15)
        # Pilla la distancia actual al obstáculo
        distance_to_obstacle = ultrasonic_sensor.distance_centimeters
    left_motor.off()
    right_motor.off()
    return distance_to_obstacle

def go_around_obstacle(left_motor, right_motor, ultrasonic_sensor, color_sensor, distance_to_obstacle):
    """
    Función que hace que el robot rodee un obstáculo
    """
    # Girar 90 grados a la derecha
    girar_grados(90, left_motor, right_motor)
    # Avanzar 20 cm
    avanzar_cm(30, left_motor, right_motor)
    # Girar 90 grados a la derecha
    girar_grados(-90, left_motor, right_motor)
    # Avanzar 20+10(diametro aproximado de la lata)+distance_to_obstacle cm
    avanzar_cm(40+distance_to_obstacle, left_motor, right_motor)
    # Girar y avanzar hasta llegar a la línea
    go_to_line(left_motor, right_motor, color_sensor, -90)
    return distance_to_obstacle