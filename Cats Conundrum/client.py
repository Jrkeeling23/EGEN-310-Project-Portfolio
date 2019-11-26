"""
------------------------------------------------------------------------------------------------------------------------
Justin Keeling
EGEN-310R: Multidisciplinary Engineering Design
Montana State University
6 December, 2019
------------------------------------------------------------------------------------------------------------------------
Note:
- Uses Bluetooth wireless protocol.

Overview:
- Client class is a client connection to a server over Bluetooth
- Client object sends data to the server.

Unique Design:
- Eliminate weight sent to server.
    - Results in faster data sending, no buffer overload, server does not process redundant data
- 'current_action' variable stops redundant data from being sent.
- since only sent once, the server can act accordingly to combination commands when a released or pressed.
- Can be run WITH or WITHOUT the application.

Reference:
- https://pynput.readthedocs.io/en/latest/keyboard.html
------------------------------------------------------------------------------------------------------------------------
"""
from bluetooth import *
from pynput.keyboard import Listener
import time


class Client:
    """
    Client reaches out to a discoverable Bluetooth connection; Sends data (does not receive data)
    """
    def __init__(self):
        self.server_socket = None
        self.serverMACAddress = None  # "DC:A6:32:37:E6:48" initially hardcoded to enable a faster connection
        self.port = 1  # port to use for connection in wireless protocol Bluetooth

        self.current_action = ""  # controls what is sent to the user and to keep the state of an action when ONE ...
        # ... key in a combination is released.

        # possible velocity updates, commands for motors (both singular and combination)
        self.possible_data = ['w', 'a', 's', 'd', 'q']  # single
        self.possible_combos = ['wa', 'aw', 'wd', 'dw', 'sd', 'ds', 'sa', 'as']  # combos
        self.speed_accel_data = ['up', 'down', 'left', 'right']  # arrow keys

    def discover(self):
        """
        Scan for nearby bluetooth devices.
        :return: List of nearby devices
        """
        nearby_devices = discover_devices(lookup_names=True)
        return nearby_devices

    def connect_to_server(self, server_mac):
        """
        Given a mac address of a nearby device, try and make a connection to a server.
        :param server_mac: Mac address of the desired server.
        :return: None
        """
        self.server_socket = BluetoothSocket(RFCOMM)  # uses RFCOMM Bluetooth protocol
        self.serverMACAddress = server_mac  # server mac address to establish a connection to
        self.server_socket.connect((self.serverMACAddress, self.port))  # connect
        print("Connection made! ---- Server Mac Address: %s ---- Port in use: %s" % (
            self.serverMACAddress, self.port))  # prompt

    def handle_keyboard_data(self):
        """
        This function handles the data from the client end. A listener is used to listen to the keyboard and use the
        appropriate functions when pressed/released.
        :return: None
        """
        with Listener(on_press=self._pressed,
                      on_release=self._released)as listener:  # https://pynput.readthedocs.io/en/latest/keyboard.html
            listener.join()
            time.sleep(0.1)  # time buffer before closing
        self.server_socket.close()  # close the connection to server

    def _pressed(self, key):
        """
        Listener function when a key is pressed.
        :param key: The 'key' pressed on keyboard
        :return: None
        """
        if key is 'q':
            self.server_socket.send('q')
            time.sleep(0.2)
            quit()
        try:
            if key in self.possible_data and len(self.current_action) <= 2:
                # its possible, a combo can be added, and is not the last redundant data
                if len(self.current_action) is 0:
                    self.current_action += key  # current action "" can be concatenated
                    self.server_socket.send(self.current_action)  # single command
                    print("sending: %s" % self.current_action)
                elif len(self.current_action) is 1:  # size of 1
                    potential = key + self.current_action  # potential temp variable
                    if potential in self.possible_combos:  # must be a possible combo
                        self.current_action += key  # update the current action
                        self.server_socket.send(self.current_action)  # send the data
                        print("sending: %s" % self.current_action)  # prompt (NOT needed)
                    else:
                        return None
                else:
                    return None
            elif key in self.speed_accel_data:
                self.server_socket.send(key)
        except AttributeError:
            pass

    def _released(self, key):
        """
        Listener Function When a 'key' is released.
        :param key: The ket that is released.
        :return: None
        """
        try:
            if key in self.current_action:
                if len(self.current_action) is 1:  # if there will be no current action
                    self.server_socket.send('x')  # send data to stop motors
                    self.current_action = ''  # reset the current action
                else:  # combo command
                    self.current_action = self.current_action.replace(key, "")  # replace the command released with ''
                    self.server_socket.send(self.current_action)  # send update to server
            else:
                pass
        except AttributeError:
            pass
