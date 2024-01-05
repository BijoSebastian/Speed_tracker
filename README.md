# Speed_tracker

# Components:
1] K-LD7-RFB-00H-01 RFbeam Microwave GmbH  
2] Raspberry Pi  
3] ArduCam Hawk-eye

# Setup:
## 1]Radar sensor(for raspberry pi 4 and below):

Install the python driver(kld7) for the radar sensor from https://github.com/nickovs/kld7

The Raspberry Pi (except Raspberry Pi 5) has 2 in-built types of UART:(all UARTS on the Pi ar 3.3V)  
	->PL011  
	->mini UART(has reduced feature set)  
  	
The default state of the `enable_uart` flag depends on which UART is the primary UART in the `/boot/config.txt `file of the Pi.   
Refer to https://www.raspberrypi.com/documentation/computers/configuration.html#uarts-and-device-tree:~:text=contain%20this%20controller.-,Primary%20and%20Secondary%20UART,-The%20following%20table to find the primary UART of your particular pi model.  
On the Raspberry Pi 3B+ model, the mini UART is the default and hence needs to be changed, this can also be seen by observing which linux device is being used in the folder `/dev/`.  
Note that `/dev/serial0` and `/dev/serial1` are symbolic links which point to either `/dev/ttyS0` or `/dev/ttyAMA0` where the latter indicates that PL011 is beng used.  
By default, the primary UART is assigned to the Linux console. If you wish to use the primary UART for other purposes, you must reconfigure Raspberry Pi OS. This can be done by using raspi-config.   
Follow the steps in https://www.raspberrypi.com/documentation/computers/configuration.html#uarts-and-device-tree:~:text=Linux%20Serial%20Console-,By%20default,-%2C%20the%20primary%20UART to do this.
Now disable bluetooth in `/boot/config.txt` under #Disable  Bluetooth  
```
# Disable Bluetooth
dtoverlay=disable-bt
```

Also disable the service hciuart with
```
sudo systemctl disable hciuart.service
```
Now reboot to apply the changes:
```
sudo reboot
```
Check to see if the `/dev/ttyAMA0` is being used in `/dev/`  
Now run the basictest1.py program under /code/radar/ in this repository to see if the radar is working.  
  

## 2]Camera:
Follow instrucions from https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/Quick-Start-Guide/#arducam-pi-hawk-eye-64mp-cameras:~:text=support%20PDAF%20function.-,Step%201.%20Download%20the%20bash%20scripts,-wget%20%2DO%20install_pivariety_pkgs to install necessary packages and drivers.

Add the following under `[all]` in the /boot/config.txt
``` 
dtoverlay=arducam-64mp
 ```  
 Now test if `libcamera-hello` works properly. If yes then your camera is good to go.  