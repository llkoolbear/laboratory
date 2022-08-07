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

from devices import device
from devices.servos import servo
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

class Gimbal(device.Device):

    def __init__(self, pan_pin, tilt_pin, max_pan=30, max_tilt=15, model='DS3225'):
        
        self.pan_pin = pan_pin # GPIO pin on the Raspberry Pi refer to Board (#) not BCM GPIO#
        self.tilt_pin = tilt_pin
        self.pan = servo.Servo(pan_pin)
        self.tilt = servo.Servo(tilt_pin)
        self.model = model
        self.attributes = GIMBAL_ATTRIBUTES[self.model]

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
        if x < self.min_x:
            x = self.min_x
        elif x > self.max_x:
            x = self.max_x
        
        if y < self.min_y:
            y = self.min_y
        elif y > self.max_y:
            y = self.max_y

        self.pan.set_angle(x + self.pan.attributes.mid_angle)
        self.tilt.set_angle(y + self.tilt.attributes.mid_angle)

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
        while self.x != x or self.y != y:
            if abs(self.x-x) < speed*self.pan.delay:
                set_x = x
            elif self.x < x:
                set_x = self.x+speed*self.pan.delay*x_retard
            elif self.x > x:
                set_x = self.x-speed*self.pan.delay*x_retard

            if abs(self.y-y) < speed*self.tilt.delay:
                set_y = y
            elif self.y < y:
                set_y = self.y+speed*self.tilt.delay*y_retard
            elif self.y > y:
                set_y = self.y-speed*self.tilt.delay*y_retard
            print(set_x, set_y)
            self.pan_goto(set_x, set_y)
            print(self.x,self.y)    

    def pan_search(self, move_x, move_y, speed):
        pan_dx = self.x + move_x
        if pan_dx > self.max_x:
            pan_dx = self.min_x
        #pan_dy = self.y + move_y
        #if pan_dy > self.max_y:
        #    pan_dy = self.min_y
        self.guide_to_position(pan_dx, 5, speed)

    def sine_search(self, speed):
        steps = round(self.max_x*2/5)
        sleep = self.max_x*2/speed/steps
        
        sine = [round(self.max_x*math.cos(2*math.pi*n/(steps-1)+math.pi)) for n in range(steps)]

        try:
            while True:
                for n in sine:
                    self.pan_goto(n,0)
                    if sleep > self.pan.delay:
                        time.sleep(sleep - self.pan.delay)

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