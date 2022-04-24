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

servo1 = servo.Servo(11)
sine = [270*math.sin(math.pi*n/100) for n in range(100)]
print(sine)

try:
  while True:
    for n in sine:
        servo1.set_angle(n)
        time.sleep(0.5)

except KeyboardInterrupt:
  servo1.stop_servo()