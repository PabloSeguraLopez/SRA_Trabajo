#!/usr/bin/env python3
from ev3dev2.motor import SpeedPercent


def turn_in_goal(left_motor, right_motor,color_sensor):
    # Gira hasta que detecta la línea
    left_motor.on(SpeedPercent(-20), block=False)
    right_motor.on(SpeedPercent(20), block=False)
    while color_sensor.color != 1:
        continue
    left_motor.off()
    right_motor.off()