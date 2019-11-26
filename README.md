# EGEN-310-Project-Portfolio

The computer science discipline for the Cats Conundrum project involves developing the software to control an RC car wirelessly and using a GUI. 
In this case, Bluetooth is used to connect wirelessly, while Kivy is used to create a GUI to do so.  

## Getting Started
Requirements to setup the programming development environment.
### Prerequisites 
What will be needed in terms of software and hardware. Follow the links for installation instructions or hardware documentation.
#### Software related
* [python3](https://www.python.org/downloads/)
* [pip3](https://pip.pypa.io/en/stable/installing/)
* [adafruit motorkit](https://circuitpython.readthedocs.io/projects/motorkit/en/latest/)
* [kivy](https://pypi.org/project/Kivy/)
* [PyBluez](https://pypi.org/project/PyBluez/)
#### Hardware related
* [Raspberry Pi](https://www.adafruit.com/category/105) (3, 4, or zero). Must have Bluetooth connectivity.
* Adafruit DC and Stepper Motor ([HAT](https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/overview?gclid=CjwKCAiAlO7uBRANEiwA_vXQ-79H7aV8Ql1Dwbz5FU_IP-XY1XgD2iuNmu-fn2I6Fy7RoLhIUEFMxRoCd9IQAvD_BwE) or [Bonnet](https://www.adafruit.com/product/4280?gclid=CjwKCAiAlO7uBRANEiwA_vXQ-8Dt6Pb63q9ybWfFCYqH_QHKKfQPZxtOaQ894nUELJAkP48LXHv2MxoCG0UQAvD_BwE))
* 4 DC Motors

### Raspberry Pi
The raspberry pi operating system used is [Raspbian](https://www.raspberrypi.org/downloads/). This OS comes with python3.

#### Setup Bluetooth from terminal
* First install [pip3](https://pip.pypa.io/en/stable/installing/), [adafruit motorkit](https://circuitpython.readthedocs.io/projects/motorkit/en/latest/) and [PyBluez](https://pypi.org/project/PyBluez/)

* Using bluetoothctl, bluetooth can be setup from the terminal.
```
pi@raspberrypi:~$ bluetoothctl
Agent registered
[bluetooth] power on 
[bluetooth] agent on
[bluetooth] discoverable on
[bluetooth] scan on
[bluetooth] quit
```
* Using 'pair' and 'connect' will allow a device to reconnect without the terminal.
```
[bluetooth] pair XX:XX:XX:XX:XX:XX
[bluetooth] connect XX:XX:XX:XX:XX:XX
```
#### Setup Bluetooth on boot
* To set up bluetooth discoverable and scanning as well as the RFCOMM server on boot, a shell file must be created using your text editor. 
```
pi@raspberrypi:~$ sudo nano filename.sh
```
* Add the following into the new file. Adding 'sudo python3 /PATH/TO/server.py is one way to start the server (not preferred).
```
#! /bin/bash
sudo systemctl bluetooth enable
sudo hciconfig hci0 up
sudo echo -e 'power on\nagent on\ndiscoverable on\nscan on\nquit' | sudo bluetoothctl
```
Additionally, adding the following allows a connection to be made to a specific device.
```
#! /bin/bash
sudo systemctl bluetooth enable
hciconfig hci0 up
sudo echo -e 'power on\nagent on\ndiscoverable on\nscan on\n connect XX:XX:XX:XX\nquit' | sudo bluetoothctl
```

* Save and exit. Then give the new file and the server.py file access permissions.
```
pi@raspberrypi:~$ sudo chmod +X filename.sh
pi@raspberrypi:~$ sudo chmod +X /PATH/TO/server.py

```
* These can then added to the crontab using root.
```
pi@raspberrypi:~$ sudo -i
root@raspberrypi:~# crontab -e
```
* This opens the crontab file. Add the following to the bottom of the crontab.
```
@reboot /PATH/TO/filename.sh
@reboot /PATH/TO/server.py
```
* Save, exit, and reboot. 

## Directory Structure
The current structure of the files is redundant only to simplify components for the instructor.

### Backend
The Backend directory contains the files that are used to create a Bluetooth server, Bluetooth client, and contol motor movements over Bluetooth.
* server.py
* client.py
* movements.py
### Frontend
Th Frontend has files that are used for the application using [Kivy](kivy)
* main.py
* launch_me.kv
* connect.kv
### Cats Conundrum

Contains all the files mentioned above in addition to the python environment that is needed to run the files.

## Running the App
First, turn on the raspberry pi and locate the destination of the application.
Once found, run the program using python3.
Alternativly, you can create a shell file as mentioned earlier and adding...
```sudo python3 /PATH/TO/APPLICATION.py ```
Giving it access permissions as earler, this can be ran by adding it to your desktop, or by using the terminal.
```./PATH/TO/shell_for_application.sh file ```
