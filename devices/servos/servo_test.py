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
import servo

servo1 = servo.Servo(11,200)
steps = 100
sine = [round(270*math.sin(math.pi*n/steps)) for n in range(steps)]

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
        time.sleep(0.005)

except KeyboardInterrupt:
    servo1.set_angle(0)
    servo1.stop_servo()