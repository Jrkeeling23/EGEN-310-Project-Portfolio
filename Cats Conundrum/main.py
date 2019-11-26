"""
------------------------------------------------------------------------------------------------------------------------
Justin Keeling
EGEN-310R: Multidisciplinary Engineering Design
Montana State University
6 December, 2019
------------------------------------------------------------------------------------------------------------------------
Note:
- This application is made to run on a Bluetooth compatible laptop/desktop.

Overview:
- Creates some of the structure and all the functionality of the application.
- Can discover and connect to nearby devices (if paired and trusted already).

Unique Design:
- App uses Client class in client.py to create a connection to the server as well as send data.
- Uses .kv file to add more structure to the application.

Reference:
- https://kivy.org/doc/stable/api-kivy.uix.vkeyboard.html
    - Used for listener... The event handlers are mine.
- https://kivy.org/doc/stable/
    - Used to only learn about the classes and class methods, the application of the classes/methods are mine.
------------------------------------------------------------------------------------------------------------------------
"""

import kivy
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import *
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from client import Client

kivy.require('1.11.1')  # version of kivy used
test = Builder.load_file('launch_me.kv')  # kv file; this one contains the structure of the app
test2 = Builder.load_file('connect.kv')  # contains the structure of the discovered devices.


class AppStruct(PageLayout):
    """
    Enables a swipe feel; left or right.
    """

    def __init__(self):
        super(AppStruct, self).__init__()
        self.client = Client()  # client object

    def discover(self):
        """
        Discovers nearby devices using the client object.
        :return: None
        """
        my_box = DropDown()  # drop down for discovered devices
        my_box.btns = []  # contains the buttons in the drop down child
        devices = self.client.discover()  # discover and retrieve nearby devices

        my_box.btns = []
        for device in devices:  # create buttons for each discovered device in a drop down view
            print(device)
            button = Button(text=device[0], padding_x=25, padding_y=25, font_size=20, height=100, width=100)
            button.bind(on_press=lambda button: my_box.select(button.text))
            my_box.btns.append(button)  # keep tab on buttons
            my_box.add_widget(button)  # add it to screen
        mainbutton = Button(text='Show devices', size_hint=(None, None))
        mainbutton.bind(on_release=my_box.open)
        my_box.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        self.ids.d2.clear_widgets()  # remove current widgets to add new one
        self.ids.d2.add_widget(my_box)  # add the discovered devices

    def connect(self, mac):
        """
        Connect to the device that is clicked in the drop down (Used as an event).
        :return: None
        """
        self.client.connect_to_server(mac)
        kb = MyKeyboardListener(client=self.client)  # listen to user data from keyboard
        self.clear_widgets()  # remove the current widgets on screen
        self.add_widget(Label(text='Connected to...%s' % self.client.serverMACAddress))  # show connected device

    def close_user(self):
        """
        Close the connections.
        :return:
        """
        self.client.server_socket.send('q')  # client sends 'q' to close the connection
        self.clear_widgets()  # close the remaining widgets
        exit()  # terminate program


class MyKeyboardListener(Widget):
    """
    Listens to the keyboard data from the user. Uses Client object to access its functions.
    https://kivy.org/doc/stable/api-kivy.uix.vkeyboard.html

    - Event functions, and event handling as well as user are mine
    """

    def __init__(self, **kwargs):
        """
        pass in the client object as an argument since it is used earlier in AppStruct.
        :param kwargs:
        """
        self.client = kwargs["client"]
        kwargs = {}  # pass into super
        super(MyKeyboardListener, self).__init__(**kwargs)  # parent shout out
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')  # https://kivy.org/doc/stable/api-kivy.uix.vkeyboard.html
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_key_up)  # set up keyboard events

    def _keyboard_closed(self):
        """
        Stops listening to keyboard.
        :return: None
        """
        self._keyboard.unbind(on_key_down=self._on_keyboard_down, on_key_up=self._on_key_up)  # stop events
        self._keyboard = None  # set keyboard variable to None so it is not used anymore.

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """
        Event when a key is pressed and listener is listening.
        :param keyboard: keyboard object to enable listening
        :param keycode: data pressed
        :param text: Not Used
        :param modifiers: Not Used
        :return: Boolean to continue listener
        """
        if keycode[1] == 'escape' or keycode[1] == 'q':
            self.client._pressed('q')  # NOTE: Uses client methods
        else:
            self.client._pressed(keycode[1])  # NOTE: Uses client methods
        return True  # just for formality of events

    def _on_key_up(self, kb, keycode):
        self.client._released(keycode[1])  # NOTE: Uses client methods
        return True  # just for formality of events


class MyApp(App):
    """
    The main class that instantiates the remaining application functions.
    """

    def build(self):
        """
        build function is used to construct the application.
        :return:
        """
        return AppStruct()  # returns the app structure... Not necessarily used but more for functionality when called.


if __name__ == '__main__':  # main method call to instantiate MyApp
    MyApp().run()
