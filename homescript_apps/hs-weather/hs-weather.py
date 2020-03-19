#!/usr/bin/python

import pyowm
import os
import sys
import time

scriptPath='/home/shares/public/scripts/HomeScript/homescript_apps/hs-weather/'

hot=21
cold=19
argumentLength = len(sys.argv)

def getTemp():
    global temp
    w = pyowm.OWM('c7df50e0e8a98cd81fe2c7ba38966bd6').weather_around_coords(12.8888509, 77.6102861, limit=1)[0].get_weather()
    temp = w.get_temperature('celsius')['temp']
    writeCache()

def getCache():
    global temp
    try:
        f = open(scriptPath + "cache.txt")
        cacheTime = f.readline()
        if time.time() - float(cacheTime) < 1800:
            temp = float(f.readline())
            f.close()
        else:
            f.close()
            getTemp()
    except:
        f = open(scriptPath + "cache.txt", "w+")
        f.close()
        getTemp()

def writeCache():
    try:
        f = open(scriptPath + "cache.txt", "w")
        f.write(str(time.time()) + "\n" + str(temp))
        f.close()
    except:
        f = open(scriptPath + "cache.txt", "w")
        f.write("300000\n30")
        f.close()

def printHelp():
    print('hs-weather.py -t|h|a')

if argumentLength==2:
    getCache()
    if sys.argv[1] == '-t':
        print(temp)
    elif sys.argv[1] == '-h':
        if temp >= hot:
            print("HOT")
        elif temp <= cold:
            print("COLD")
        else:
            print("NORMAL")
    elif sys.argv[1] == '-a':
        if temp >= hot:
            os.system("bash " + scriptPath + "hot.sh")
    else:
        printHelp()
else:
    printHelp()
