#!/usr/bin/env python3
from ev3dev2.motor import SpeedPercent

# Función para girar en la línea final: el robot gira en su propio eje hasta detectar color negro, de forma que cada rueda quede a un lado de la linea.
def turn_in_goal(left_motor, right_motor,color_sensor):
    left_motor.on(SpeedPercent(-20), block=False)
    right_motor.on(SpeedPercent(20), block=False)
    
    # Mientras el sensor de color no detecte el color negro (línea), sigue girando
    while color_sensor.color != 1:
        continue

    # Cuando detectamos la linea en el centro, paramos ambos motores
    left_motor.off()
    right_motor.off()