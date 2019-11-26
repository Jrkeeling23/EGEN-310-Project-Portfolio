import kivy
from kivy.properties import NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.layout import Layout
from kivy.uix.relativelayout import RelativeLayout

kivy.require('1.11.1')

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import *
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.pagelayout import PageLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from client import Client
from kivy.uix.dropdown import DropDown

test = Builder.load_file('launch_me.kv')
test2 = Builder.load_file('connect.kv')


class AppStruct(PageLayout):
    def __init__(self):
        super(AppStruct, self).__init__()
        self.client = Client()

    def discover(self):
        print("working")
        my_box = DropDown()
        my_box.btns = []
        devices = self.client.discover()

        my_box.btns = []
        for device in devices:
            print(device)
            button = Button(text=device[0],padding_x=25, padding_y=25, font_size=20, height=100, width=100)
            button.bind(on_press=lambda button: my_box.select(button.text))
            my_box.btns.append(button)
            my_box.add_widget(button)
        mainbutton = Button(text='Show devices', size_hint=(None, None))
        mainbutton.bind(on_release=my_box.open)
        my_box.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        self.ids.d2.clear_widgets()
        self.ids.d2.add_widget(my_box)

    def connect(self):
        self.client.connect_to_server()
        kb = MyKeyboardListener(client=self.client)
        self.clear_widgets()
        self.add_widget(Label(text='Connected to...%s' % self.client.serverMACAddress))

    def close_user(self):  # TODO check
        self.client.server_socket.send('q')
        self.clear_widgets()
        exit()


# class Devices(GridLayout):
#     def __init__(self):
#         super(Devices, self).__init__()
#         self.cols=1
#         print("hererere")
#     #     self.btns = []
    #
    # def create_button(self, device):
    #     button = Button(text=device, on_press=self.connect)
    #     self.add_widget(button)
    #     self.btns.append(button)


# class BluetoothConnect(GridLayout):
#     def __init__(self, **kwargs):
#         super(BluetoothConnect, self).__init__(**kwargs)
#         self.cols = 2
#         self.spacing = 10
#         self.padding = 10
#         self.add_widget(Button(text="Discover Nearby Devices!", font_size=24, on_press=self.show_devices))
#         self.add_widget(Button(text=""))
#         self.add_widget(Label(text='Manually connect a device?'))
#
#         self.username = TextInput(multiline=False)
#         self.add_widget(self.username)
#         self.password = TextInput(password=True, multiline=False)


# class DiscoverButton(Button):
#     def __init__(self, ):
#         super(DiscoverButton, self).__init__()
#         self.discover()
#
#     def discover(self):
#         client = Client()
#         devices = client.discover()
#         mybox = BoxLayout()
#         mybox.my_buttons = []
#         if devices is not None:
#             for d in devices:
#                 button = Button(text=d[1])
#                 mybox.my_buttons.append(button)
#                 mybox.add_widget(button)
#             return mybox


class MyKeyboardListener(Widget):

    def __init__(self, **kwargs):
        self.client = kwargs["client"]
        kwargs = {}
        super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_key_up)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down, on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape' or keycode[1] == 'q':
            self.client._pressed('q')
            keyboard.release()
        else:
            self.client._pressed(keycode[1])

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def _on_key_up(self, kb, keycode):
        self.client._released(keycode[1])
        return True


class MyApp(App):
    client = Client()

    def build(self):
        return AppStruct()


if __name__ == '__main__':
    from kivy.base import runTouchApp
    from client import Client

    MyApp().run()
