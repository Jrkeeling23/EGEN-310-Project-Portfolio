"""Simple test for using adafruit_motorkit with a DC motor"""
import time


# from adafruit_motorkit import MotorKit

# kit = MotorKit()


class Movement:

    def __init__(self):
        print("_______________Initializing Motors_______________")
        self.target_velocity = 0.9
        self.start_velocity = 0.55
        self.current_velocity = self.start_velocity
        self.speed_increment = 0.025
        self.time_increment = 0.05
        self.thread_stopper = False
        self.current_act = None

    def move_forward(self):
        print("----------Movement: FORWARD:----------")
        print(self.current_velocity)

    def move_reverse(self):
        print("----------Movement: REVERSE----------")
        print(self.current_velocity)

    def stop(self):
        print("----------Movement: STOP----------")
        self.current_velocity = 0
        print(self.current_velocity)

    def moving_left(self):
        print("----------Movement: TURNING-LEFT----------")
        print(self.current_velocity)

    def skidsteer_left(self):
        print("----------Movement: SKID-STEER-LEFT----------")
        print(self.current_velocity)

    def moving_right(self):
        print("----------Movement: TURNING-RIGHT----------")
        print(self.current_velocity)

    def skidsteer_right(self):
        print("----------Movement: SKID-STEER-RIGHT----------")
        print(self.current_velocity)

    def increment_target_velocity(self):
        print("----------Increment Speed ----------")
        added = self.target_velocity + 0.05
        if added > 1:
            self.target_velocity = 1
            print("\tSPEED AT MAX")
        else:
            self.target_velocity = added
            print("\tSPEED AT %s" % self.target_velocity)

    def decrement_target_velocity(self):
        print("----------Decrement Speed ----------")
        added = self.target_velocity - 0.03
        if added < self.start_velocity:
            self.target_velocity = self.start_velocity
            print("\tTARGET AT MIN")
        else:
            self.target_velocity = added
            print("\tTARGET AT %s" % self.target_velocity)

    def increment_start_velocity(self):
        print("----------Increment Speed ----------")
        added = self.start_velocity + 0.03
        if added >= self.target_velocity:
            self.start_velocity = self.target_velocity
            print("\tSTART AT MAX")
        else:
            self.start_velocity = added
            print("\tSTART AT %s" % self.start_velocity)

    def decrement_start_velocity(self):
        print("----------Decrement Speed ----------")
        subbed = self.start_velocity - 0.05
        if subbed < 0.5:
            self.start_velocity = 0.5
            print("\tSTART AT MIN")
        else:
            self.start_velocity = subbed
            print("\tSTART AT %s" % self.start_velocity)

    def reset_current_velocity(self):
        self.current_velocity = self.start_velocity

    def accel(self, act):
        print("ACCELERATING")
        if self.current_velocity >= self.target_velocity:
            self.current_velocity = self.target_velocity
            act()
            return True
        else:
            self.current_velocity += self.speed_increment
            act()
            return False

    def set_to_initial_speed(self):
        self.current_velocity = self.start_velocity
        self.thread_stopper = False

    def thread_accelerate_handler(self, act):
        while self.thread_stopper is False:
            maxed = self.accel(act)
            if maxed:
                self.thread_stopper = True
                break
            time.sleep(.2)
        self.thread_stopper = True
        print("-----END OF THREAD-----")
