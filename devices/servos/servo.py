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
from collections import namedtuple

ServoAttributes = namedtuple('ServoAttributes',
                            'min_angle max_angle\
                            min_freq max_freq\
                            min_pulse_width max_pulse_width')

SERVO_ATTRIBUTES = {
    'DS3225': ServoAttributes( 0, 270,              # Angle in Degrees
                                50, 330,            # Frequency in Hz
                                500e-6, 2500e-6)    # Pulse Width in Seconds
}

class Servo():

    def __init__(self, pin, freq = 50, model = 'DS3225'):
        
        self.pin = pin # GPIO pin on the Raspberry Pi refer to Board (#) not BCM GPIO#
        self.freq = freq
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
        print(self.duty_cycle)
        self.pwm.ChangeDutyCycle(self.duty_cycle)

    def stop_servo(self):
        self.pwm.stop()
        GPIO.cleanup()