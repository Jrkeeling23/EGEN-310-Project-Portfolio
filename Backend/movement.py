"""
------------------------------------------------------------------------------------------------------------------------
Justin Keeling
EGEN-310R: Multidisciplinary Engineering Design
Montana State University
6 December, 2019
------------------------------------------------------------------------------------------------------------------------
Note:
- This python file can only be run on a raspberry pi with an adafruit motor driver.
- Made for the use of FOUR motors.

Overview:
- Movement class controls the 4 separate motors by using adafruit_motorkit library (control pins and pwm).
- Movements include: forward, reverse, skid steer left/right, and a left/right veering.

Unique Design:
- Acceleration function that uses threading. This allows the car to accelerate, while also overriding the function when
  the client sends more data.
    - The entails client controlled start velocity as well as "target" velocity in which it will accelerate too.

Reference:
- https://circuitpython.readthedocs.io/projects/motorkit/en/latest/api.html
    - Only used documentation for provided functions; Code below is mine
------------------------------------------------------------------------------------------------------------------------
"""
from adafruit_motorkit import MotorKit  # https://circuitpython.readthedocs.io/projects/motorkit/en/latest/api.html
import time

kit = MotorKit()


class Movement:
    """
    Controlled within the Server class of the server file, Movement contains functions to control motors.
    """

    def __init__(self):
        # initialize 4 motors (Using adafruit library)
        self.m1 = kit.motor1  # back left
        self.m2 = kit.motor2  # back right
        self.m3 = kit.motor3  # front left
        self.m4 = kit.motor4  # front right

        # initialize velocity variables within a range of [-1,1] where 0 is stopped
        self.target_velocity = 0.9
        self.start_velocity = 0.55
        self.current_velocity = self.start_velocity

        # initialize acceleration variables
        self.speed_increment = 0.025
        self.time_increment = 0.05

        self.thread_stopper = False  # controlled in Server class, stops acceleration function

    """
    BELOW (until next comment): movement functions
    """

    def move_forward(self):
        # NOTICE, '-x'. This determines the the direction of the motor rotation
        x = self.current_velocity  # speed to start at (server calls the acceleration function so thread can be cut).
        self.m1.throttle = -x
        self.m3.throttle = -x
        self.m2.throttle = -x
        self.m4.throttle = -x
        # does not stop motors until instructed to from server

    def move_reverse(self):
        x = self.current_velocity
        self.m1.throttle = x
        self.m3.throttle = x
        self.m2.throttle = x
        self.m4.throttle = x

    def stop(self):
        self.m1.throttle = 0
        self.m2.throttle = 0
        self.m3.throttle = 0
        self.m4.throttle = 0

    def moving_left(self):
        x = self.current_velocity
        z = x - 0.12  # veering requires some change in the the motors throttle, although rotating in same direction.
        self.m1.throttle = -x
        self.m2.throttle = -z
        self.m3.throttle = -z
        self.m4.throttle = -x

    def skidsteer_left(self):
        x = self.current_velocity
        self.m1.throttle = -x
        self.m3.throttle = 0
        self.m2.throttle = 0
        self.m4.throttle = -x

    def moving_right(self):
        x = self.current_velocity
        z = x - 0.12
        self.m1.throttle = -z
        self.m2.throttle = -x
        self.m3.throttle = -x
        self.m4.throttle = -z

    def skidsteer_right(self):
        x = self.current_velocity
        self.m4.throttle = 0
        self.m1.throttle = 0
        self.m3.throttle = -x
        self.m2.throttle = -x

    """
    END of movement control functions
    
    BELOW: Thread/acceleration and dynamic velocity functions 
    """

    def increment_target_velocity(self):
        """
        Controls the target velocity. This is controlled by the client and instantiated in Server.
        :return: None
        """
        added = self.target_velocity + self.speed_increment  # increment
        if added > 1:  # thresholds
            self.target_velocity = 1  # set to upper bound
        else:
            self.target_velocity = added  # set to incremented value

    def decrement_target_velocity(self):
        """
        Controls the target velocity. This is controlled by the client and instantiated in Server.
        :return: None
        """
        subbed = self.target_velocity - self.speed_increment  # decrement
        if subbed < self.start_velocity:  # thresholds
            self.target_velocity = self.start_velocity  # set to lower bound
        else:
            self.target_velocity = subbed  # set to decremented value

    def increment_start_velocity(self):
        """
        Controls the starting velocity. This is controlled by the client and instantiated in Server.
        :return: None
        """
        added = self.start_velocity + self.speed_increment  # increment
        if added >= self.target_velocity:  # thresholds
            self.start_velocity = self.target_velocity  # set to upper bound
        else:
            self.start_velocity = added  # set to incremented value

    def decrement_start_velocity(self):
        """
        Controls the starting velocity. This is controlled by the client and instantiated in Server.
        :return: None
        """
        subbed = self.start_velocity - self.speed_increment  # decrement
        if subbed < 0.5:  # thresholds
            self.start_velocity = 0.5  # set to lower bound
        else:
            self.start_velocity = subbed  # set to decremented value

    def accel(self, act):
        """
        Controls the acceleration of the motors.
        :param act: the action in which to continue performing.
        :return: Boolean; ends or continues accel call from Server.
        """
        if self.current_velocity >= self.target_velocity:
            self.current_velocity = self.target_velocity  # lower current velocity to user defined max of [0,1]
            act()  # performs movement
            return True  # return to thread handler
        else:
            self.current_velocity += self.speed_increment  # increment speed
            act()  # performs movement
            return False  # return to thread handler

    def set_to_initial_speed(self):
        """
        Resets the current velocity variable to initial user defined value.
        :return: None
        """
        self.current_velocity = self.start_velocity
        self.thread_stopper = False  # reopen thread

    def thread_accelerate_handler(self, act):
        """
        Given an action from server, controls the thread until...
        1) Override from client input processe in server,
        2) Acceleration is maxed.
        :param act: movement call to continuously run until while loop break.
        :return: None
        """
        while self.thread_stopper is False:
            maxed = self.accel(act)  # boolean that represents convergence of current and target velocity.
            if maxed:
                self.thread_stopper = True  # cut thread (from server)
                break
            time.sleep(self.time_increment)  # timer to pause between velocity increments. (controls acceleration)
        self.thread_stopper = True  # if current velocity and target converge, thread closes.
