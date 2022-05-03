# ===============================================================================
#
# Name:       servo_test.py 
#
# Purpose:    Tests Servo Driver functionality
#
# Author:     Bear Bissen
#
# Created:    April 23, 2022
# Last Rev:   
# Edited by:  
#
# License: MIT Open License
#
# ===============================================================================

import math
import time
from servo import Servo

SERVO_PIN = 13
SERVO_FREQUENCY = 50
STEPS = 100

servo1 = Servo(SERVO_PIN,SERVO_FREQUENCY)
sine = [round(servo1.attributes.max_angle*(math.cos(2*math.pi*n/(STEPS-1)+math.pi)+1)/2) for n in range(STEPS)]

try:
  while True:
    for n in sine:
        servo1.set_angle(n)
        time.sleep(0.02)
    for n in sine:
        servo1.set_angle(n)
        time.sleep(0.01)
    for n in sine:
        servo1.set_angle(n)
    servo1.guide_to_angle(270, 200)
    servo1.guide_to_angle(0, 200)
    servo1.guide_to_angle(270, 250)
    servo1.guide_to_angle(0, 250)
    servo1.guide_to_angle(270, 300)
    servo1.guide_to_angle(0, 300)
    servo1.guide_to_angle(270, 350)
    servo1.guide_to_angle(0, 350)
    servo1.guide_to_angle(270, 400)
    servo1.guide_to_angle(0, 400)
    servo1.set_angle(270)
    time.sleep(1)
    servo1.set_angle(0)
    time.sleep(1)

    servo1.set_angle(0)


except KeyboardInterrupt:
    pass

finally:
    servo1.set_angle(servo1.attributes.max_angle/2)
    time.sleep(servo1.delay)
    servo1.stop_servo()

    print('shutdown properly')