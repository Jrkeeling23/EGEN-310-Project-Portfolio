#! /usr/bin/python3

"""
------------------------------------------------------------------------------------------------------------------------
Justin Keeling
EGEN-310R: Multidisciplinary Engineering Design
Montana State University
6 December, 2019
------------------------------------------------------------------------------------------------------------------------
Note:
- Uses Bluetooth wireless protocol.
- Made to be used with Movement class from movement file.
- COMMENT AT TOP: This comment signifies what language to use when ran; it is converted into .sh to run from start up.

Overview:
- Server creates a channel in which a client can join.
- Server reads client data and performs accordingly from the input.

Unique Design:
- Dictionaries to control velocity specific updates as well as movement instructions.
- Threading for acceleration while also waiting for user input, which stops a thread.
- Key commands can be used in combination and instantiate different movements.
------------------------------------------------------------------------------------------------------------------------
"""
from bluetooth import *
import threading
from movement import Movement


class ServerBT:
    """
    ServerBT: is a server that is designed to run on a raspberry pi using Bluetooth wireless protocol.
    """

    def __init__(self):
        self.size = 1024  # max size within buffer
        self.server_mac = 'DC:A6:32:37:E6:48'  # raspberry pi MAC/server
        self.server = None  # socket that can send and receive data
        self.port = None  # port to be used

        self.client = None  # client that will connect
        self.clientInfo = None  # info of the client

        self.move = Movement()  # instance variable to control movements

        # Dictionary to control movements. The key:value is "possible client input":"corresponding function"
        self.action_dict = {"w": self.move.move_forward, "s": self.move.move_reverse, "a": self.move.skidsteer_left,
                            "d": self.move.skidsteer_right, "x": self.move.stop, "wa": self.move.moving_left,
                            "aw": self.move.moving_left, "wd": self.move.moving_right, "dw": self.move.moving_right,
                            "sa": self.move.move_reverse, "as": self.move.move_reverse, "sd": self.move.move_reverse,
                            "ds": self.move.move_reverse}
        self.update_dict = {"up": self.move.increment_target_velocity, "down": self.move.decrement_target_velocity,
                            "left": self.move.decrement_start_velocity, "right": self.move.increment_start_velocity}

        self.thread = threading.Thread(target=self.move.thread_accelerate_handler)  # initialize thread

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
        :return: None
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
        :return: None
        """
        while True:  # continue waiting for client data until given instruction to terminate
            try:  # waits for data
                data = self.client.recv(self.size)  # try and get data
                if data:  # if there is data...
                    data = data.decode("ascii")  # ... decode it
                    if data is "q":  # command is 'quit'
                        self.move.stop()  # stop the motors from continuously running
                        self.client.close()  # close the client connection
                        self.server.close()  # close the server
                        quit()  # terminate the program
                    else:
                        self.process_input(data)  # process the input
            except IOError:
                ### Close connections ####
                self.client.close()
                self.server.close()
                self.client.close()

    def process_input(self, data):
        """
        Process data sent from a client.
        :param data: data from client.
        :return: None
        """
        if self.thread.is_alive():  # is the thread is running and the server receives data...
            self.move.thread_stopper = True  # kill thread
            self.thread.join()  # join (May not need)
        if data in self.action_dict:  # Since no thread is running, check if input is in possible commands
            self.move.current_act = data  # if so, set the current action to it
            if self.move.current_act is not 'x':  # if not telling the motors to stop...
                self.set_thread(self.action_dict[data])  # create the thread
                self.move.set_to_initial_speed()  # set the current speed to initial
                self.thread.start()  # start the thread
            self.action_dict[data]()  # perform the action
        elif data in self.update_dict:  # if its not in the actions...
            self.update_dict[data]()  # then check the update dictionary

    def set_thread(self, act):
        """
        initializes the thread with the args as the current instruction.
        :param act: function of Movement
        :return: None
        """
        self.thread = threading.Thread(target=self.move.thread_accelerate_handler, args=(act,))


### Controls the python file when ran ###
if __name__ == "__main__":
    host = ServerBT()  # create instance variables
    host.create_server()  # create the server
    host.client_connection()  # look for a client request
    host.receive_instruction()  # receive data from client
