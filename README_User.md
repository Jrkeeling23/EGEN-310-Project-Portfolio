# EGEN-310-Project-Portfolio
For users, this document gives instructions on how to use the Cat's Conundrum project.  
NOTE: device must be laptop or computer.

## Getting Started
Assuming that the user has all of the components of the car, the following is a guide to set up bluetooth and use the control app with the car.

### Bluetooth Configuration
If this is the first time using the Raspberry Pi with the control app, depending on your make, either connect the Pi to the internet over ethernet/wifi or use the HDMI port.

#### WIFI or Ethernet

* If the Pi has been connected WIFI before and SSH is enabled, ensure that your device to configure the pi is connected to the same WIFI. NOTE: this does not have to be the same device to control it with. 
##### Using a phone 'terminal' app, or using a computer terminal, type the following:
```
ping raspberrypi.local 
# returns the ip of the device

ssh pi@IP_address_of_pi
``` 
* For Windows, open the control panel => Network and Sharing Center => View Network connections => Find Pi and Right click to 'View status of this connection'.

#### WIFI, Ethernet, or HDMI
In the Pi terminal type the following.
```
bluetoothctl 
power on
agent on
discoverable on
scan on 
pair <ip of control app device>
connect <ip of control app device>
# type yes when prompted
trust <ip of device>
exit

sudo nano crontab -e
# at the bottom of the file type the following
@reboot echo -e 'power on\n discoverable on\nscan on\nquit | sudo bluetoothctl  && sudo ./server.sh
# ctrl-o to save  and ctrl-x to exit
sudo reboot
```
* This will automatically connect the pi to your device and start the server for the car to run.
## Running Control App
* On your control app device, locate the file via command line or in the file manager. 
* If command line:
```
python3 client.py
```
* If file manager, right click and 'execute', or 'run on' and find python3.
* A new window will appear showing the app.
* Swiping/clicking and pulling left will take you to a instructions as well as a bluetooth connection/discovery page. 
