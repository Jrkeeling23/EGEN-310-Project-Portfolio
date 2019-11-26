from kivy.app import App
from kivy.lang import Builder
from client import Client
from main import Devices
from kivy.uix.button import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown


class DeviceList(BoxLayout):
    def __init__(self, devices):
        super(DeviceList, self).__init__()
        print("working")
        my_box = DropDown()
        my_box.btns = []
        for device in devices:
            print(device)
            button = Button(text=device[1])
            button.bind(on_press=lambda button: my_box.select(button.text))
            my_box.btns.append(button)
            my_box.add_widget(button)


class NearbyDevices(App):
    def build(self, **kwargs):
        client = kwargs["client"]
        devices = client.discover()

        return DeviceList(devices)

    def connect(self, mac):
        pass


if __name__ == "__main__":
    NearbyDevices().run()
