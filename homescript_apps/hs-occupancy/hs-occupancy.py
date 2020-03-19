#!/usr/bin/python

import os
import sys

sensors = {
    'O01': 'Bedroom'
}

hsappPath = '/home/shares/public/scripts/HomeScript/homescript_apps/'

scripts = {
    'Bedroom-Enter' : hsappPath + 'hs-occupancy/bedroom-enter.sh',
    'Bedroom-Exit' : hsappPath + 'hs-occupancy/bedroom-exit.sh'
}

argumentLength = len(sys.argv)

def printHelp():
    print('hs-occupancy.py <sensor-id>')

if argumentLength==2:
    os.system('bash ' + scripts[sensors[sys.argv[1]] + '-Enter'])
elif argumentLength==3 and sys.argv[2]=="-x":
    os.system('bash ' + scripts[sensors[sys.argv[1]] + '-Exit'])
else:
    printHelp()
