# ===============================================================================
#
# Name:       gimbal_test.py 
#
# Purpose:    Tests Gimbal Driver functionality
#
# Author:     Bear Bissen
#
# Created:    April 30, 2022
# Last Rev:   
# Edited by:  
#
# License: MIT Open License
#
# ===============================================================================

import math
import time
from devices.servos import gimbal

PAN_PIN = 17 #11
TILT_PIN = 27 #13

gimbal = gimbal.Gimbal(PAN_PIN,TILT_PIN)

try:
    gimbal.sine_search(50)

except KeyboardInterrupt:
    pass

finally:
    gimbal.pan_goto(0,0)
    time.sleep(gimbal.pan.delay)
    gimbal.stop_gimbal()

    print('shutdown properly')