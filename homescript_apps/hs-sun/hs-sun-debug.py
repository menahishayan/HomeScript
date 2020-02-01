#!/usr/bin/python

from suntime import Sun, SunTimeException
import sys

sun = Sun(12.8888509, 77.6102861)

def sunrise():
    try:
        print sun.get_local_sunrise_time().strftime('%M %H %d %m')
    except SunTimeException as e:
        print "0 0 0 0"

def sunset():
    try:
        print sun.get_local_sunset_time().strftime('%M %H %d %m')
    except SunTimeException as e:
        print "0 0 0 0"

if len(sys.argv)==2:
    if str(sys.argv[1]) == "sunrise":
        sunrise()
    elif str(sys.argv[1]) == "sunset":
        sunset()
    else: print "0 0 0 0"
else:
    sunrise()
    sunset()
