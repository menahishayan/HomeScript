#!/bin/bash

# Example script to toggle lights based on the status of fan
# Created by Menahi Shayan. 2019.

FAN=$(../homeScript.py -g fan | cut -d ' ' -f 2 | head -1)

if [ "$FAN" == "False" ]; then
    ../homeScript.py -s fan 1
    ../homeScript.py -s all lights 0
else
    ../homeScript.py -s fan 0
    ../homeScript.py -s all lights 1
fi
