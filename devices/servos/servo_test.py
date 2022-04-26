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

servo1 = Servo(11,50)
steps = 100
sine = [round(270*(math.cos(2*math.pi*n/(steps-1)+math.pi)+1)/2) for n in range(steps)]

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
    servo1.set_angle(0)
    servo1.stop_servo()

    print('shutdown properly')