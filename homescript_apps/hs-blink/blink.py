#!/usr/bin/python3

""" Automation Rule to Blink an accessory for example a light or smart plug
    The script is executed on an infinite loop to exit, CTRL + C.
"""

import argparse
import time
import os
import sys
import inspect

# Import homescript that is 2 folders before.
sys.path.append('..\..\..\homescript')
import homescript

__HOSTNAME__='192.168.0.106'
__PORT__='51826'
__AUTH__='043-14-615'

# Name of the acessory to control - CHANGE WITH YOUR ACESSORY NAME.
accessory="Smart_Plug_"

def blink_accessory(name, time_sec):
    """ Blinks an accessory for example a light or a Smart Plug. 

    Parameters
    ----------
    name : string
        Acessory name.
    time_sec : integer
        Seconds between change the state. ON->OFF->ON.
    """

    try:
        # Select an accessory or group of accessories. Any get/set/print operation requires accessories to be selected first.
        hs.selectAccessory(name.lower())

        while True:
            hs.setStates("1")
            time.sleep(time_sec)
            hs.setStates("0")
            time.sleep(time_sec)

    except KeyboardInterrupt:
        print("Exiting...")

parser = argparse.ArgumentParser(description='Command line blink accessory', add_help=True)
parser.add_argument('-t', '--time', type=int, required=True, help='Time in seconds between state ON and OFF')
args = parser.parse_args()

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

blink_accessory(accessory, args.time)
