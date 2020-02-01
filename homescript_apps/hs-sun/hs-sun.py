#!/usr/bin/python

from suntime import Sun, SunTimeException
from datetime import timedelta
import sys

sun = Sun(12.8888509, 77.6102861)

sunriseOffset=25
sunsetOffset=-7

def sunrise():
    try:
        return (sun.get_local_sunrise_time() + timedelta(minutes=sunriseOffset)).strftime('%M %H %d %m')
    except SunTimeException as e:
        return "0 0 0 0"

def sunset():
    try:
        return (sun.get_local_sunset_time() + timedelta(minutes=sunsetOffset)).strftime('%M %H %d %m')
    except SunTimeException as e:
        return "0 0 0 0"

scriptPath='/home/shares/public/scripts/HomeScript/homescript_apps/hs-sun/'

riseScript='sunrise.sh'
setScript='sunset.sh'

crontab = open("/etc/crontab", "r")
ct2 = open("/tmp/ct2", "w")

foundRise=False
foundSet=False

for l in crontab:
    if riseScript in l:
        ct2.write(sunrise() + ' *\troot\tbash ' + scriptPath + riseScript + '\n')
        foundRise=True
    elif setScript in l:
        ct2.write(sunset() + ' *\troot\tbash '  + scriptPath + setScript + '\n')
        foundSet=True
    else:
        ct2.write(l)

if foundRise==False:
    ct2.write(sunrise() + ' *\troot\tpython ' + scriptPath + riseScript + '\n')

if foundSet==False:
    ct2.write(sunset() + ' *\troot\tpython '  + scriptPath + setScript + '\n')

ct2.close()
