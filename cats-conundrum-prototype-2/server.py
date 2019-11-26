#! /usr/bin/python3
import time
from bluetooth import *
from adafruit_motorkit import MotorKit
import threading

kit = MotorKit()


class ServerBT:
    def __init__(self):
        self.size = 1024  # max size within buffer
        self.server_mac = 'DC:A6:32:37:E6:48'  # raspberry pi MAC/server
        self.server = None  # socket that can send and receive data
        self.port = None  # port to be used
        self.client = None  # client that will connect
        self.clientInfo = None  # info of the client
        self.move = Movement()
        action = self.move
        self.action_dict = {"w": action.move_forward, "s": action.move_reverse, "a": action.skidsteer_left,
                            "d": action.skidsteer_right, "x": action.stop, "wa": action.moving_left,
                            "aw": action.moving_left, "wd": action.moving_right, "dw": action.moving_right,
                            "sa": action.move_reverse, "as": action.move_reverse, "sd": action.move_reverse,
                            "ds": action.move_reverse}
        self.update_dict = {"up": action.increment_target_velocity, "down": action.decrement_target_velocity,
                            "left": action.decrement_start_velocity, "right": action.increment_start_velocity}
        self.active_buttons = []
        self.thread = threading.Thread(target=self.move.thread_accelerate_handler)

    def create_server(self):
        """
        Create a server using any port and the raspberry pi's mac address
        :return:
        """
        self.server = BluetoothSocket(RFCOMM)  # socket that can send and receive data
        self.server.bind((self.server_mac, PORT_ANY))  # ties the socket with a MAC and port
        self.server.listen(1)  # waits
        self.port = self.server.getsockname()[1]  # port number used
        print("__________Server Initialized__________\n\tWait for connection....")  # prompt for user

    def client_connection(self):
        """
        Waits for a client connection to be made and accepts.
        :return:
        """
        try:
            self.client, self.clientInfo = self.server.accept()  # accept a connection from client
        except BluetoothError:
            print("ERROR: while accepting....\n Trying again...")  # prompt user that a connection failed
            self.client, self.clientInfo = self.server.accept()  # try again
        print("\nACCEPTED CLIENT: ", self.clientInfo, "\n")  # prompt that a connection has been made

    def receive_instruction(self):
        """
        Continuously wait for data until clients ends connection
        :return:
        """
        thread = None
        while True:  # continue waiting for client data until given instruction to terminate
            try:  # waits for data
                data = self.client.recv(self.size)  # try and get data
                if data:  # if there is data...
                    data = data.decode("ascii")  # ... decode it
                    if data is "q":
                        self.move.stop()
                        self.client.close()
                        self.server.close()
                        quit()
                    else:
                        self.process_input(data)
            except IOError:
                ### Close connections ####
                self.client.close()
                self.server.close()
                self.client.close()

    def process_input(self, data):
        if self.thread.is_alive():
            self.move.thread_stopper = True
            self.thread.join()
        if data in self.action_dict:
            self.move.current_act = data
            if self.move.current_act is not 'x':
                self.set_thread(self.action_dict[data])
                self.move.set_to_initial_speed()
                self.thread.start()
            self.action_dict[data]()
        elif data in self.update_dict:
            self.update_dict[data]()

    def send_thread_update(self, data):
        self.action_dict[data]()

    def set_thread(self, act):
        self.thread = threading.Thread(target=self.move.thread_accelerate_handler, args=(act,))


class Movement:
    def __init__(self):
        self.m1 = kit.motor1  # back left
        self.m2 = kit.motor2  # back right
        self.m3 = kit.motor3  # front left
        self.m4 = kit.motor4  # front right
        self.target_velocity = 0.9
        self.start_velocity = 0.55
        self.current_velocity = self.start_velocity
        self.speed_increment = 0.025
        self.time_increment = 0.05
        self.thread_stopper = False
        self.current_act = None

    def move_forward(self):
        x = self.current_velocity
        self.m1.throttle = -x
        self.m3.throttle = -x
        self.m2.throttle = -x
        self.m4.throttle = -x

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
        z = x-0.12
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
        z = x-0.12
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


if __name__ == "__main__":
    host = ServerBT()
    host.create_server()
    host.client_connection()
    host.receive_instruction()
