# ===============================================================================
#
# Name:       gimbal.py 
#
# Purpose:    Driver for servos when controlled by the raspberry pi
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

import servo
from .. import device
import time
import math
from collections import namedtuple

GimbalAttributes = namedtuple('GimbalAttributes',
                            'min_x max_x\
                            min_y max_y\
                            min_pulse_width max_pulse_width')

GIMBAL_ATTRIBUTES = {
    'DS3225': GimbalAttributes( 0, 270,             # Angle in Degrees
                                50, 330,            # Frequency in Hz
                                500e-6, 2500e-6)    # Pulse Width in Seconds
}

STEPS = 100

class Gimbal(device.Device):

    def __init__(self, pan_pin, tilt_pin, max_pan=45, max_tilt=45):
        
        self.pan_pin = pan_pin # GPIO pin on the Raspberry Pi refer to Board (#) not BCM GPIO#
        self.tilt_pin = tilt_pin
        self.pan = servo.Servo(pan_pin)
        self.tilt = servo.Servo(tilt_pin)
        #self.attributes = GIMBAL_ATTRIBUTES[self.model]

        if max_pan > self.pan.attributes.mid_angle:
            max_pan = self.pan.attributes.mid_angle
        if max_tilt > self.tilt.attributes.mid_angle:
            max_tilt = self.tilt.attributes.mid_angle

        self.max_pan = max_pan
        self.max_tilt = max_tilt

        self.min_x = 0 - self.max_pan
        self.max_x = 0 + self.max_pan
        self.min_y = 0 - self.max_tilt
        self.max_y = 0 + self.max_tilt

        self.pan_goto(0,0)

    def pan_goto(self, x, y):    
        ''' Move the pan/tilt to a specific location.
            Convert cartesian x and y to servo angle
        '''
        # check maximum servo limits and change if exceeded
        if x < self.min_x:
            x = self.min_x
        elif x > self.max_x:
            x = self.max_x

        if y < self.min_y:
            y = self.min_y
        elif y > self.max_y:
            y = self.max_y

        # convert and move pan servo
        self.pan.set_angle(x + self.pan.attributes.mid_angle)
        self.tilt.set_angle(y + self.tilt.attributes.mid_angle)

        #if verbose:
        #    print(f"pan_goto - Moved Camera to pan_cx={x} pan_cy={y}")
        
        self.x = x
        self.y = y

    def guide_to_position(self, x, y, speed):

        # check maximum server limits and change if exceeded
        if x < self.min_x:
            x = self.min_x
        elif x > self.max_x:
            x = self.max_x

        if y < self.min_y:
            y = self.min_y
        elif y > self.max_y:
            y = self.max_y

        if abs(self.x-x) > abs(self.y-y):
            x_retard = 1
            y_retard = abs((self.y-y)/(self.x-x))
        elif abs(self.x-x) < abs(self.y-y):
            x_retard = abs((self.x-x)/(self.y-y))
            y_retard = 1
        else:
            x_retard = 1
            y_retard = 1
        print(x_retard,y_retard)
        print(self.x,self.y)    
        print(x, y)
        while self.x != x and self.y != y:
            if abs(self.x-x) < speed*self.pan.delay*x_retard:
                set_x = x
            elif self.x < x:
                set_x = self.x+speed*self.pan.delay*x_retard
            elif self.x > x:
                set_x = self.x-speed*self.pan.delay*x_retard

            if abs(self.y-y) < speed*self.tilt.delay*y_retard:
                set_y = y
            elif self.y < y:
                set_y = self.y+speed*self.tilt.delay*y_retard
            elif self.y > y:
                set_y = self.y-speed*self.tilt.delay*y_retard
            print(set_x, set_y)
            self.pan_goto(set_x, set_y)
            print(self.x,self.y)    


    '''
    def pan_search(pan_cx, pan_cy):
        pan_cx = pan_cx + pan_move_x
        if pan_cx > pan_max_right:
            pan_cx = pan_max_left
            pan_cy = pan_cy + pan_move_y
            if pan_cy > pan_max_bottom:
                pan_cy = pan_max_top
        if debug:
            print(f"pan_search - at pan_cx={pan_cx} pan_cy={pan_cy}")
        return pan_cx, pan_cy
    '''

    def sine_search(self, speed):
        
        sine = [round(self.max_x*math.cos(2*math.pi*n/(STEPS-1)+math.pi)) for n in range(STEPS)]

        try:
            while True:
                for n in sine:
                    self.pan_goto(n,0)
                    time.sleep(0.01*(5-speed))

        except KeyboardInterrupt:
            pass

    def box_search(self, speed):

        try:
            while True:
                print(self.min_x,self.max_x,self.min_y,self.max_y)
                self.guide_to_position(self.min_x,self.max_y,speed)
                time.sleep(1)
                self.guide_to_position(self.max_x,self.max_y,speed)
                time.sleep(1)
                self.guide_to_position(self.max_x,self.min_y,speed)
                time.sleep(1)
                self.guide_to_position(self.min_x,self.min_y,speed)
                time.sleep(1)

        except KeyboardInterrupt:
            pass


    def stop_gimbal(self):
        self.pan.stop_servo
        self.tilt.stop_servo