#!/usr/bin/env python3
from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_A
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import UltrasonicSensor, ColorSensor
from ev3dev2.sensor import INPUT_2, INPUT_1
from ev3dev2.led import Leds
from time import sleep
from math import pi
from basic_functions import *
from navigation_to_line import *
from reconnaissance import *
from final_steps import *
from handle_obstacle import *

# Definimos los motores izquierdo y derecho usando las salidas definidas
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)
# Definimos el objeto de sonido
spkr = Sound()
# Definimos los LEDs
leds = Leds()
# Definimos el sensor ultrasónico en el puerto 2
ultrasonic = UltrasonicSensor(INPUT_2)
# Definimos el sensor de color en el puerto 1
color_sensor = ColorSensor(INPUT_1)

# Iniciamos el programa
start_program(leds,spkr)

# Rango inicial de barrido: de -30 a 30 grados
sweep_left_range = -30
sweep_right_range = 30

# Variable para saber si se ha detectado la línea y si se está entre los obstáculos
line_detected = False
between_obstacles = False

# Barrido para detectar la primera y segunda lata
alfa, h1, h2 = (0,0,0)

# Bucle para llegar a la línea mientras no se haya detectado
while not line_detected:
    # Barrido para detectar las latas
    alfa, h1, h2 = sweep(left_motor, right_motor, ultrasonic, sweep_left_range, sweep_right_range)
    print(str(alfa), str(h1), str(h2))

    # Ajustamos el rango de barrido para la siguiente iteración
    sweep_left_range = -40
    sweep_right_range = 40
    print(str(h2))

    # Verificamos si no hay segunda lata (h2 is None) o si el ángulo entre latas es muy pequeño (abs(alfa) <= 31)
    if h2 is None or abs(alfa) <= 31:
        alfa = -1
        # Gira 25 grados a la derecha
        girar_grados(25, left_motor, right_motor)

        # Avanza 10 cm en total, repartido en 5 tramos de 2 cm
        for i in range(0, 5):
            avanzar_cm(2, left_motor, right_motor)
            if color_sensor.color == 1:
                # Si el color detectado es 1 (la línea), se marca que la línea ha sido detectada
                line_detected = True
                # Tras detectar la línea, avanza para que ésta esté en el centro de gravedad del robot
                avanzar_cm(5, left_motor, right_motor, velocidad=20)
                break

        # Si no se detectó la línea en ese avance, se corrige el giro para volver a apuntar a la lata
        if not line_detected:
            girar_grados(-angle_to_obstacle_after_movement(h1, 10, 25), left_motor, right_motor)
        continue

    # Si is_between_obstacles evalúa a True, significa que estamos entre las latas
    elif is_between_obstacles(alfa, h2):
        print("GAP", str(alfa))
        # Llamamos a la función go_to_gap para dirigirnos a la línea a través del hueco
        go_to_gap(alfa, left_motor, right_motor, color_sensor)
        between_obstacles = True
        line_detected = True
    else:
        try:
            # Si alfa < 0, significa que esta por la parte superior de la pizarra, por lo que intentamos girar a la derecha para llegar a la linea.
            # Beta es el angulo para ir perpendicular a la linea
            if alfa < 0:
                beta = angle_to_line(h1, h2)
            else:
                # En caso contrario, estamos en la parte inferior por lo que debemos girar hacia la izquierda buscando la linea.
                beta = -angle_to_line(h1, h2)
            print("BETA", str(beta))
            # Si el ángulo calculado es mayor que 20, estamos lejos de las latas por lo que buscamos llegar a la linea.
            if abs(beta) > 20:
                print("LINE", str(beta))
                go_to_line(left_motor, right_motor, color_sensor, beta)
            else:
                # Si beta es muy pequeño, significa que estamos cerca de la primera lata por lo que buscamos ir al hueco.
                print("GAP", str(alfa))
                go_to_gap(alfa, left_motor, right_motor, color_sensor)
                between_obstacles = True
            line_detected = True
            
        except Exception as e:
            print(str(e))
# Linea detectada
# Si no está entre las latas, acercarse a la primera lata, rodearla y volver a la línea
if not between_obstacles:
    obstacle = 0
    print("ALFA", str(alfa))
    if alfa > 0:
        # Si empezó en la zona inferior del mapa, giramos a la derecha.
        print("derecha")
        while(color_sensor.color != 1):
            left_motor.on(SpeedPercent(20), block=False)
            right_motor.on(SpeedPercent(-20), block=False)
    else:
        #En caso contrario, giramos a la izquierda.
        print("izquierda")
        while(color_sensor.color != 1):
            left_motor.on(SpeedPercent(-20), block=False)
            right_motor.on(SpeedPercent(20), block=False)
        
    #Añadimos un pequeño retardo para que el robot termine de alinearse correctamente.
    sleep(0.2)
    left_motor.off()
    right_motor.off()

    obstacle = keep_until_close_to_obstacle(left_motor, right_motor, ultrasonic, color_sensor)
    # Rodeamos el obstáculo con la distancia obtenida
    go_around_obstacle(left_motor, right_motor, ultrasonic, color_sensor, obstacle)

# Si estamos entre las dos latas, giramos hasta que cada rueda esté a un lado de la línea
turn_in_goal(left_motor, right_motor, color_sensor)

# Fin del programa
end_program(leds,spkr)