#!/usr/bin/python3

import sys
import socket
from pythonping import ping

users = {
    'shayan': {
        'phone': '192.168.0.90',
        'pc': '192.168.0.10'
    }
}

argumentLength = len(sys.argv)

def present(person,device=''):
    if len(device) < 2:
        for dev in users[person.lower()]:
            try:
                if ping(users[person.lower()][dev], count=1).success():
                    print (1)
                    return
            except:
                print (0)
        print (0)
    else:
        try:
            if ping(users[person.lower()][device], count=1).success():
                print (1)
                return
        except:
            print (0)
        print (0)

def printHelp():
    print('hs-pih.py user <device>')

if argumentLength==1:
    printHelp()
elif argumentLength==2:
    present(sys.argv[1])
else:
    present(sys.argv[1], sys.argv[2])
