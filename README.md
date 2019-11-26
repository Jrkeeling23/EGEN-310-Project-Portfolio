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
## Directory Structure
The current structure of the files is redundant only to simplify components for the instructor.

### Backend
The Backend directory contains the files that are used to create a Bluetooth server, Bluetooth client, and contol motor movements over Bluetooth.
* server.py
* client.py
* movements.py
### Frontend
Th Frontend has files that are used for the application using [Kivy](#kivy)
* main.py
* launch_me.kv
* connect.kv
### Cats Conundrum

Contains all the files mentioned above in addition to the python environment that is needed to run the files.
