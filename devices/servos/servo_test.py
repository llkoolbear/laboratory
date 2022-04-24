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

servo1 = servo.Servo(11,50)
steps = 100
sine = [round(270*(math.cos(2*math.pi*n/(steps-1)+math.pi)+1)/2) for n in range(steps)]
print(sine)
try:
  while True:
    for n in sine:
        servo1.set_angle(n)
        time.sleep(0.04)
    for n in sine:
        servo1.set_angle(n)
        time.sleep(0.03)
    for n in sine:
        servo1.set_angle(n)
        time.sleep(0.02)

except KeyboardInterrupt:
    servo1.set_angle(0)
    servo1.stop_servo()