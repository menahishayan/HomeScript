#!/usr/bin/python3

""" Reads the state of the realy from a TP-Link Smart Plug. 
"""
import sys

# Import homescript that is 2 folders before.
sys.path.append('..\..\..\homescript')
import homescript

# import tplink
from tplink import *

__HOSTNAME__='192.168.0.106'
__PORT__='51826'
__AUTH__='043-14-615'

# Name of the acessory to control - CHANGE WITH YOUR ACESSORY NAME.
accessory="Smart_Plug_"

start = False

# To wait to Homebridge to start
while False == start:
    try:
        # Initialize with hostname, port and auth code. Debug and sys.argv are optional
        hs = homescript.HomeScript(__HOSTNAME__, __PORT__, __AUTH__, True)
        start = True
    except Exception as e:
        print("An exception occurred!")
        print(e)

hs.selectAccessory(accessory.lower())

# Get data
relay_state = get_state(hs)
print(relay_state)
