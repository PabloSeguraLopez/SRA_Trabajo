from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_A
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from time import sleep
from math
from basic_functions import *

def sweep(right_motor, left_motor, ultrasonic_sensor, max_degrees_right, max_degrees_left):
    """
    Función que devuelve el ángulo y distancia del robot a la primera y segunda lata, haciendo un barrido de
    5 grados en 5 grados, de izquierda a derecha
    """
    detections = {}
    # Ir hacia el punto angular más a la izq para barrer hacia el punto angular más a la der
    girar_grados(max_degrees_left, left_motor, right_motor)
    # Hacer movimientos de 5 grados en 5 grados para barrer, del punto más a la izq al más a la der
    for i in range(max_degrees_left, max_degrees_right, 5):
        distance_to_obstacle = ultrasonic_sensor.distance_centimeters()           
        # Clave -> grados del barrido, valor -> distancia de la detección
        detections[i] = distance_to_obstacle
        # Girar 5 grados
        girar_grados(i, left_motor, right_motor)

    # Calculamos la distancia mínima de las detecciones que corresponden con la detección de la primera lata
    min_distance_angle_first_can = min(detections, key=detections.get)
    min_distance_first_can = detections[min_distance_angle_first_can]


    keys_to_delete = []
    for angle, distance in detections.items():
        if distance > min_distance_first_can + 70:
            # Añadir la clave a la lista de claves a borrar
            keys_to_delete.append(angle)

    # Borrar las entradas del diccionario que cumplan la condicion anterior
    for key in keys_to_delete:
        del detections[key]
    
    # Filtrar valores que estén fuera del rango restringido (min_distance + 10)
    threshold = min_distance_first_can + 10
    to_detect_second_can = {angle: distance for angle, distance in detections.items() if distance >= threshold}

    if to_detect_second_can:
        # Calculamos la distancia mínima de las detecciones que corresponden con la detección de la segunda lata
        min_distance_angle_second_can = min(to_detect_second_can, key=to_detect_second_can.get)
        min_distance_second_can = to_detect_second_can[min_distance_angle_second_can]
    else:
        # No hay detección de una segunda lata
        min_distance_angle_second_can = None
        min_distance_second_can = None

    # Calculamos alpha, que se corresponde con el ángulo que hay entre la línea perpendicular 
    # a la línea negra de las latas y el robot
    numerador = (min_distance_first_can^2 - min_distance_first_can - 16)/8
    denominador = math.sqrt(min_distance_first_can^2 - numerador^2)
    alpha = math.degrees(math.atan(numerador/denominador))

    # Giramos hacia el angulo de la detección de la primera lata
    girar_grados(min_distance_angle_first_can, left_motor, right_motor)
    
    return min_distance_angle_first_can, min_distance_first_can, min_distance_angle_second_can, min_distance_second_can

def angle_to_line(distance_to_first_can):
    # Calculamos el ángulo de giro que se necesita para caminar perpendicularmente a la línea negra
    numerador = (distance_to_first_can^2 - distance_to_first_can - 16)/8
    denominador = math.sqrt(distance_to_first_can^2 - numerador^2)

    # Calculamos el ángulo con el arcotangente y pasamos a ángulos
    alpha = math.degrees(math.atan(numerador/denominador))

    return alpha