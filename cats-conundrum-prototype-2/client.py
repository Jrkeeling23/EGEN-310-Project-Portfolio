#! /usr/bin/python3
from bluetooth import *
from pynput.keyboard import Key, Listener
import time


class Client:

    def __init__(self):
        self.server_socket = None
        self.serverMACAddress = "DC:A6:32:37:E6:48"
        self.port = 1
        self.current_action = ""
        self.possible_data = ['w', 'a', 's', 'd', 'q']
        self.possible_combos = ['wa', 'aw', 'wd', 'dw', 'sd', 'ds', 'sa', 'as']
        self.speed_accel_data = ['up', 'down', 'left', 'right']

    def discover(self):
        """
        Scan for nearby bluetooth devices.
        :return: List of nearby devices
        """
        nearby_devices = discover_devices(lookup_names=True)
        return nearby_devices

    def connect_to_server(self, server_mac="DC:A6:32:37:E6:48"):
        """
        Given a mac address of a nearby device, try and make a connection to a server.
        :param server_mac: Mac address of the desired server.
        :return: None
        """
        self.server_socket = BluetoothSocket(RFCOMM)
        self.serverMACAddress = server_mac
        self.server_socket.connect((self.serverMACAddress, self.port))
        # if self.server_socket.connected:
        print("Connection made! ---- Server Mac Address: %s ---- Port in use: %s" % (
            self.serverMACAddress, self.port))

    def handle_keyboard_data(self):
        """
        This function handles the data from the client end. A listener is used to listen to the keyboard and use the
        appropriate functions when pressed/released.
        :return: None
        """
        with Listener(on_press=self._pressed, on_release=self._released)as listener:
            listener.join()
            time.sleep(0.2)
        self.server_socket.close()

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
                    self.current_action += key
                    self.server_socket.send(self.current_action)
                    print("sending: %s" % self.current_action)
                elif len(self.current_action) is 1:  # size of 1
                    potential = key + self.current_action
                    if potential in self.possible_combos:
                        self.current_action += key
                        self.server_socket.send(self.current_action)
                        print("sending: %s" % self.current_action)
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
                if len(self.current_action) is 1:
                    self.server_socket.send('x')
                    print("released: %s" % self.current_action)
                    # print("current_action x")
                    self.current_action = ''
                else:
                    self.current_action = self.current_action.replace(key, "")
                    # print("current_action ", self.current_action)
                    self.server_socket.send(self.current_action)
                    print("released: %s" % self.current_action)
            else:
                pass
        except AttributeError:
            pass


DEBUGGER = False
if DEBUGGER:
    client = Client()
    devices = client.discover()
    for d in devices:
        print(d)
    client.connect_to_server('DC:A6:32:37:E6:48')
