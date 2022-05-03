# ===============================================================================
#
# Name:       servo.py 
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

import RPi.GPIO as GPIO
import time
from collections import namedtuple

ServoAttributes = namedtuple('ServoAttributes',
                            'min_angle mid_angle max_angle\
                            min_freq max_freq\
                            min_pulse_width max_pulse_width\
                            min_step max_step\
                            min_speed max_speed')

SERVO_ATTRIBUTES = {
    'DS3225': ServoAttributes( 0, 135, 270,         # Angle in Degrees
                                50, 330,            # Frequency in Hz
                                500e-6, 2500e-6,    # Pulse Width in Seconds
                                1, 270,             # Degrees
                                1, 400)             # Degrees per Second
}

class Servo():

    def __init__(self, pin, freq = 50, delay = 0.02, model = 'DS3225'):
        
        self.pin = pin # GPIO pin on the Raspberry Pi refer to Board (#) not BCM GPIO#
        self.freq = freq
        self.delay = delay
        self.model = model
        self.attributes = SERVO_ATTRIBUTES[self.model]

        if not isinstance(freq, (int,float)):
            err_str = f'"{freq}" not a valid frequency! (usage:int|float)'
            raise RuntimeError(err_str) 

        if freq < self.attributes.min_freq or freq > self.attributes.max_freq:
            err_str = f"{freq} degrees out of range! ({self.attributes.min_freq} to {self.attributes.max_freq} degrees)"
            raise RuntimeError(err_str)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.freq)
        self.min_duty_cycle = self.freq*self.attributes.min_pulse_width*100
        self.max_duty_cycle = self.freq*self.attributes.max_pulse_width*100
        self.duty_cycle = self.min_duty_cycle
        self.angle = 0
        self.pwm.start(self.min_duty_cycle)

    def set_angle(self, angle):

        if not isinstance(angle, (int,float)):
            err_str = f'"{angle}" not a valid angle! (usage:int|float)'
            raise RuntimeError(err_str) 

        if angle < self.attributes.min_angle or angle > self.attributes.max_angle:
            err_str = f"{angle} degrees out of range! ({self.attributes.min_angle} to {self.attributes.max_angle} degrees)"
            raise RuntimeError(err_str)

        self.angle = angle
        self.duty_cycle = self.angle/self.attributes.max_angle*(self.max_duty_cycle-self.min_duty_cycle)+self.min_duty_cycle
        self.pwm.ChangeDutyCycle(self.duty_cycle)
        time.sleep(self.delay)

    def guide_to_angle(self, angle, speed):
        
        if not isinstance(angle, (int,float)):
            err_str = f'"{angle}" not a valid angle! (usage:int|float)'
            raise RuntimeError(err_str) 

        if angle < self.attributes.min_angle or angle > self.attributes.max_angle:
            err_str = f"{angle} degrees out of range! ({self.attributes.min_angle} to {self.attributes.max_angle} degrees)"
            raise RuntimeError(err_str)

        if not isinstance(speed, (int,float)):
            err_str = f'"{speed}" not a valid angle! (usage:int|float)'
            raise RuntimeError(err_str) 

        if speed < self.attributes.min_speed or speed > self.attributes.max_speed:
            err_str = f"{speed} degrees per second out of range! ({self.attributes.min_speed} to {self.attributes.max_speed} degrees per second)"
            raise RuntimeError(err_str)

        while self.angle != angle:
            if abs(self.angle-angle) < speed*self.delay:
                self.set_angle(angle)
            elif self.angle < angle:
                self.set_angle(self.angle+speed*self.delay)
            elif self.angle > angle:
                self.set_angle(self.angle-speed*self.delay)

    def stop_servo(self):
        self.pwm.stop()
        time.sleep(self.delay)
        GPIO.cleanup()
        time.sleep(self.delay)
