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

# Definición de motores y sensores
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)
spkr = Sound()
leds = Leds()
ultrasonic = UltrasonicSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_1)

# Empieza el programa
start_program(leds,spkr)
# El primer barrido es de -30 a 30 grados
sweep_left_range = -30
sweep_right_range = 30
# Variable para saber si se ha detectado la linea y si está entre las latas
line_detected = False
between_obstacles = False
# Barrido para detectar la primera y segunda lata
alfa, h1, h2 = (0,0,0)
# Bucle para llegar a la línea
while not line_detected:
    # Barrido para detectar la primera y segunda lata
    alfa, h1, h2 = sweep(left_motor, right_motor, ultrasonic, sweep_left_range, sweep_right_range)
    print(str(alfa), str(h1), str(h2))
    sweep_left_range = -40
    sweep_right_range = 40
    print(str(h2))
    if h2 is None or abs(alfa) <= 31:
        # Gira 25 grados a la derecha y avanza 10 cm
        girar_grados(25, left_motor, right_motor)
        for i in range(0, 5):
            avanzar_cm(2, left_motor, right_motor)
            if color_sensor.color == 1:
                line_detected = True
                # Tras detectar la línea, avanza para que ésta esté en el centro de gravedad del robot
                avanzar_cm(5, left_motor, right_motor, velocidad=20)
                break
        # Vuelve a mirar hacia la lata (teniendo en cuenta la rotación y avance)
        if not line_detected:
            girar_grados(-angle_to_obstacle_after_movement(h1, 10, 25), left_motor, right_motor)
        continue
    elif is_between_obstacles(alfa, h2):
        print("GAP", str(alfa))
        go_to_gap(alfa, left_motor, right_motor, color_sensor)
        between_obstacles = True
        line_detected = True
    else:
        try:
            if alfa < 0:
                beta = angle_to_line(h1, h2)
            else:
                beta = -angle_to_line(h1, h2)
            print("BETA", str(beta))
            if abs(beta) > 20:
                print("LINE", str(beta))
                go_to_line(left_motor, right_motor, color_sensor, beta)
            else:
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
        # Si empezó en la zona inferior del mapa
        print("derecha")
        while(color_sensor.color != 1):
            left_motor.on(SpeedPercent(20), block=False)
            right_motor.on(SpeedPercent(-20), block=False)
    else:
        print("izquierda")
        while(color_sensor.color != 1):
            left_motor.on(SpeedPercent(-20), block=False)
            right_motor.on(SpeedPercent(20), block=False)
    sleep(0.2)
    left_motor.off()
    right_motor.off()
    obstacle = keep_until_close_to_obstacle(left_motor, right_motor, ultrasonic, color_sensor)
    go_around_obstacle(left_motor, right_motor, ultrasonic, color_sensor, obstacle)

# Entre las dos latas, girar hasta que cada rueda esté a un lado de la línea
turn_in_goal(left_motor, right_motor, color_sensor)


# Fin del programa
end_program(leds,spkr)