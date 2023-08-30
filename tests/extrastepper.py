import time

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

################################
# RPi and Motor Pre-allocations
################################
#
# define GPIO pins
direction = 22  # Direction (DIR) GPIO Pin
step = 23  # Step GPIO Pin
EN_pin = 24  # enable pin (LOW to enable)

# Declare a instance of class pass GPIO pins numbers and the motor type
mymotortest = RpiMotorLib.A4988Nema(direction, step, (21, 21, 21), "DRV8825")
GPIO.setup(EN_pin, GPIO.OUT)  # set enable pin as output

###########################
# Actual motor control
###########################
#
GPIO.output(EN_pin, GPIO.LOW)  # pull enable to low to enable motor
mymotortest.motor_go(
    True,  # True=Clockwise, False=Counter-Clockwise
    "1/8",  # Step type (Full,Half,1/4,1/8,1/16,1/32)
    15000,  # number of steps
    0.000075,  # step delay [sec]
    False,  # True = print verbose output
    0.05,
)  # initial delay [sec]

# GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
# mymotortest.motor_go(False, # True=Clockwise, False=Counter-Clockwise
# "1/8" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
# 1500, # number of steps
# .000075, # step delay [sec]
# False, # True = print verbose output
# .05) # initial delay [sec]
GPIO.cleanup()  # clear GPIO allocations after run
