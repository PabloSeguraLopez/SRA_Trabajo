from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_A
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from time import sleep
import math
from basic_functions import *

def sweep(left_motor, right_motor, ultrasonic_sensor, max_degrees_left, max_degrees_right):
    """
    Función que devuelve el ángulo y distancia del robot a la primera y segunda lata, haciendo un barrido de
    N grados en N grados, de izquierda a derecha
    """

    # Creamos un diccionario para almacenar las detecciones: clave = ángulo, valor = distancia
    detections = {}
    # Definimos n_degrees como el incremento de giro que haremos en cada paso del barrido
    n_degrees = 10
    # Giramos primero hasta el ángulo más a la izquierda antes de iniciar el barrido
    girar_grados(max_degrees_left, left_motor, right_motor)
    # Recorremos con saltos de n_degrees desde max_degrees_left hasta max_degrees_right
    for i in range(max_degrees_left, max_degrees_right, n_degrees):
        # Tiempo necesario para que el sensor de ultrasonidos pueda de forma precisa tomar los datos y también evitar errores de giro
        sleep(0.5)
        # Medimos la distancia con el sensor ultrasónico
        distance_to_obstacle = ultrasonic_sensor.distance_centimeters           
        # Clave -> grados del barrido, valor -> distancia de la detección
        detections[i] = distance_to_obstacle
        # Giramos n_degrees para el siguiente punto de medición
        girar_grados(n_degrees, left_motor, right_motor)

    # Calculamos el ángulo donde la distancia es mínima (suponemos que ahí está la primera lata)
    min_distance_angle_first_can = min(detections, key=detections.get)
    # Obtenemos esa distancia mínima
    min_distance_first_can = detections[min_distance_angle_first_can]

    # Creamos una lista para almacenar las claves que excedan un rango de 70 cm con respecto a la primera lata
    keys_to_delete = []
    for angle, distance in detections.items():
        # Si la distancia está 70 cm por encima de la mínima, la consideramos ruido o irrelevante
        if distance > min_distance_first_can + 70:
            keys_to_delete.append(angle)

    # Borramos las entradas del diccionario que cumplan la condición de estar muy lejos
    for key in keys_to_delete:
        del detections[key]
    
    # Definimos un umbral para considerar una segunda lata (10 cm de diferencia)
    threshold = 10
    # Creamos un nuevo dict con los ángulos cuyas distancias difieren en al menos 10 cm de la primera lata
    to_detect_second_can = {angle: distance for angle, distance in detections.items() if abs(min_distance_first_can - distance) >= threshold}

    # Si hay algo en ese diccionario, calculamos la segunda lata
    if to_detect_second_can:
        # Calculamos la distancia mínima de las detecciones que corresponden con la detección de la segunda lata
        min_distance_angle_second_can = min(to_detect_second_can, key=to_detect_second_can.get)
        min_distance_second_can = to_detect_second_can[min_distance_angle_second_can]
    else:
        # No hay detección de una segunda lata
        min_distance_angle_second_can = 0
        min_distance_second_can = None

    # Ahora giramos de vuelta al punto que consideramos la primera lata
    girar_grados(-(max_degrees_right-min_distance_angle_first_can), left_motor, right_motor)
    
    # Si la segunda lata no existe, alfa = 0
    if min_distance_second_can is None:
        alfa = 0
    else:
        # alfa es la diferencia angular entre la primera y segunda lata
        alfa = min_distance_angle_second_can - min_distance_angle_first_can
    
    # Devolvemos: alfa (diferencia angular), distancia primera lata, distancia segunda lata
    return alfa, min_distance_first_can, min_distance_second_can