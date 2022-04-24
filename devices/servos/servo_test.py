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

import time
import servo

servo1 = servo.Servo(11)

try:
  while True:
    servo1.set_angle(45)
    time.sleep(0.5)
    servo1.set_angle(90)
    time.sleep(0.5)
    servo1.set_angle(135)
    time.sleep(0.5)
    servo1.set_angle(180)
    time.sleep(0.5)
    servo1.set_angle(225)
    time.sleep(0.5)
    servo1.set_angle(270)
    time.sleep(0.5)
    servo1.set_angle(225)
    time.sleep(0.5)
    servo1.set_angle(180)
    time.sleep(0.5)
    servo1.set_angle(135)
    time.sleep(0.5)
    servo1.set_angle(90)
    time.sleep(0.5)
    servo1.set_angle(45)
    time.sleep(0.5)
    servo1.set_angle(0)
    time.sleep(0.5)

except KeyboardInterrupt:
  servo1.stop_servo()