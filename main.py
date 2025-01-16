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

# Definición de motores y sensores
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)
spkr = Sound()
leds = Leds()
ultrasonic = UltrasonicSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_1)

# Empieza el programa
spkr.beep()
leds.set_color('LEFT', 'AMBER')
leds.set_color('RIGHT', 'AMBER')
# El primer barrido es de -30 a 30 grados
sweep_left_range = -30
sweep_right_range = 30
# Variable para saber si se ha detectado la linea y si está entre las latas
line_detected = False
between_obstacles = False
# Barrido para detectar la primera y segunda lata
alfa, h1, h2 = sweep(left_motor, right_motor, ultrasonic, sweep_left_range, sweep_right_range)
print(str(alfa), str(h1), str(h2))
# Bucle para llegar a la línea
while True:
    if line_detected:
        break
    # Los siguientes barridos son de -180 a 0 grados
    sweep_left_range = -90
    sweep_right_range = 0
    if h2 is None:
        girar_grados(25, left_motor, right_motor)
        for i in range(0, 5):
            avanzar_cm(2, left_motor, right_motor)
            if color_sensor.color != 1:
                line_detected = True
                break
        continue
    if alfa < 0:
        beta = angle_to_line(h1, h2)
    else:
        beta = -angle_to_line(h1, h2)
    print("BETA", str(beta))
    if abs(h1-h2)>20:
        print("LINE", str(beta))
        go_to_line(left_motor, right_motor, color_sensor, beta)
    else:
        print("GAP", str(alfa))
        go_to_gap(alfa, left_motor, right_motor, color_sensor)
        between_obstacles = True
    line_detected = True

# Linea detectada
if alfa > 0:
    # Si empezó en la zona inferior del mapa
    girar_grados(90, left_motor, right_motor)
else:
    girar_grados(-90, left_motor, right_motor)
# Si no está entre las latas, acercarse a la primera lata, rodearla y volver a la línea
if not between_obstacles:
    sweep(left_motor, right_motor, ultrasonic, -20, 20)
    h1 = keep_until_close_to_obstacle(left_motor, right_motor, ultrasonic, h1)
    go_around_obstacle(left_motor, right_motor, ultrasonic, color_sensor, h1)
turn_in_goal(left_motor, right_motor, color_sensor)


# Fin del programa
spkr.beep()
leds.set_color('LEFT', 'GREEN')
leds.set_color('RIGHT', 'GREEN')
while True:
    continue