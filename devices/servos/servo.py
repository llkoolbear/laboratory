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
import pigpio
from devices import device
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

class Servo(device.Device):

    def __init__(self, pin, freq = 50, delay = 0.02, model = 'DS3225'):
        
        self.pin = pin # GPIO pin on the Raspberry Pi refer to Board (#) not BCM GPIO#
        self.freq = freq
        self.delay = delay
        self.model = model
        self.attributes = SERVO_ATTRIBUTES[self.model]

        self.check_num(freq, "Hz", self.attributes.min_freq, self.attributes.max_freq)

        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(self.pin, GPIO.OUT)
        #self.pwm = GPIO.PWM(self.pin, self.freq)
        self.pwm = pigpio.pi()
        self.pwm.set_mode(self.pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(self.pin, self.freq)
        self.pwm.set_PWM_range(self.pin, 10000)
        self.min_duty_cycle = self.freq*self.attributes.min_pulse_width*100
        self.max_duty_cycle = self.freq*self.attributes.max_pulse_width*100
        self.duty_cycle = self.min_duty_cycle
        self.angle = 0
        self.pwm.set_PWM_dutycycle(self.pin, self.min_duty_cycle*100)

    def set_angle(self, angle):
        self.check_num(angle, "degrees", self.attributes.min_angle, self.attributes.max_angle)

        self.angle = angle
        self.duty_cycle = self.angle/self.attributes.max_angle*(self.max_duty_cycle-self.min_duty_cycle)+self.min_duty_cycle
        self.pwm.set_PWM_dutycycle(self.pin, self.duty_cycle*100)
        time.sleep(self.delay)

    def guide_to_angle(self, angle, speed):
        
        self.check_num(angle, "degrees", self.attributes.min_angle, self.attributes.max_angle)
        self.check_num(speed, "degrees/second", self.attributes.min_speed, self.attributes.max_speed)

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
        #GPIO.cleanup()
        time.sleep(self.delay)
