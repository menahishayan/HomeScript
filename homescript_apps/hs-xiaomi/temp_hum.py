#!/usr/bin/python3

""" Read the temperature and humidity from a Xiaomi Aqara Temperature and Humidity Sensor
    through a Aqara Air Conditioning Companion Gateway.
"""
import sys

# Import homescript that is 3 folders before.
sys.path.append('..\..\..\homescript')
import homescript

# import xiaomi
from xiaomi import *

__HOSTNAME__='192.168.0.106'
__PORT__='51826'
__AUTH__='043-14-615'

# Name of the acessories to access - CHANGE WITH YOUR ACESSORY NAME.
# Name of the temperature sensor.
temp_sensor_name = "TemperatureAndHumiditySensor2_TemperatureSensor_7aaf"
# Name of the humidity sensor.
hum_sensor_name = "TemperatureAndHumiditySensor2_HumiditySensor_7aaf"

list_of_accessories = [temp_sensor_name, hum_sensor_name]

start = False

# To wait to Homebridge to start
while False == start:
    try:
        # Initialize with hostname, port and auth code. Debug and sys.argv are optional
        hs = homescript.HomeScript(__HOSTNAME__, __PORT__, __AUTH__)
        start = True
    except Exception as e:
        print("An exception occurred!")
        print(e)

# Select all accessories
for accessory in list_of_accessories:
    hs.selectAccessory(accessory.lower())

# Get data
temp = get_temperature(hs)
print(temp)

hum = get_humidity(hs)
print(hum)
