# Proximity manager for Webex devices

## Description

When you have more than one Webex device in the same room, ultrasound signals (used for Proximity pairing) from all devices can conflict. This script will allow you to define a master device and pick which device should emit ultrasound in the room (while turning off the other devices) from the master device Touch 10.

Here below is the representation of the master device Touch 10.

![](./touch10.png)

In the above example, clicking on *Board 55* would set the ultrasound volume of the Board 55 to its maximum level while turning down the ultrasound volume of all other devices to zero.


## Prerequisites

- ADMIN or INTEGRATOR credentials of Webex devices
- A VM running Python 3 (with modules *flask* and *requests*) on the same local network as the Webex devices


## Touch 10 Panel Setup

1. Access the local web interface of the Cisco Webex device ([procedure](https://help.webex.com/en-us/n5pqqcm/Advanced-Settings-for-Room-and-Desk-Devices))
2. Enable the HTTP client (be aware of security implications of enabling insecure HTTPS):
     > Setup > Configuration > HttpClient > AllowInsecureHTTPS > True

     and

     > Setup > Configuration > HttpClient > Mode > On
3. Navigate to:
     > Integration > In-Room Control > Launch Editor

4. Open the menu in the upper-right corner, select *Import from file* and find [roomcontrolconfig.xml](./roomcontrolconfig.xml)
5. Add/remove/replace buttons to fit with the devices in your room

## VM Setup




