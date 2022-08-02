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
from ..devices.servos import servo

SERVO_PIN = 13
SERVO_FREQUENCY = 50
STEPS = 100

servo1 = servo.Servo(SERVO_PIN,SERVO_FREQUENCY)
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

except KeyboardInterrupt:
    pass

finally:
    servo1.set_angle(servo1.attributes.max_angle/2)
    time.sleep(servo1.delay)
    servo1.stop_servo()

    print('shutdown properly')