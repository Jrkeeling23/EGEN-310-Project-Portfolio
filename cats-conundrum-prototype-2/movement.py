#! /usr/bin/python3
"""Simple test for using adafruit_motorkit with a DC motor"""
import time
from adafruit_motorkit import MotorKit

kit = MotorKit()


class Movement:

    def __init__(self):
        self.m1 = kit.motor1  # back left
        self.m2 = kit.motor2 # back right
        self.m3 = kit.motor3  # front left
        self.m4 = kit.motor4  # front right

    def move_forward(self, speed):
        x = 1
        self.m1.throttle = -x
        self.m3.throttle = x
        self.m2.throttle = x
        self.m4.throttle = -x

    def move_reverse(self, speed):
        x = 1
        self.m1.throttle = x
        self.m3.throttle = -x
        self.m2.throttle = -x
        self.m4.throttle = x
        time.sleep(0.1)

    def stop(self, speed):
        self.m1.throttle = 0
        self.m2.throttle = 0
        self.m3.throttle = 0
        self.m4.throttle = 0
        time.sleep(0.1)

    def moving_left(self, speed):
        self.m1.throttle = 0
        self.m2.throttle = 0
        self.m3.throttle = 0
        self.m4.throttle = 0
        time.sleep(0.1)

    def skidsteer_left(self, speed):
        x = .7
        self.m1.throttle = x
        self.m3.throttle = x
        self.m2.throttle = x
        self.m4.throttle = 0
        time.sleep(0.1)

    def moving_right(self, speed):
        x = .65
        y = .85
        self.m1.throttle = -x
        self.m2.throttle = y
        self.m3.throttle = -x
        self.m4.throttle = 0  # y
        time.sleep(0.1)

    def skidsteer_right(self, speed):
        x = .7
        self.m1.throttle = -x
        self.m3.throttle = -x
        self.m2.throttle = -x
        self.m4.throttle = 0
        time.sleep(0.1)

