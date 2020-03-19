#!/bin/bash

HSPATH='/home/shares/public/scripts/HomeScript'
HSW=$HSPATH'/homescript_apps/hs-weather/hs-weather.py'

$HSPATH/homeScript.py -s all lights 0
if [ "$(python3 $HSW -h)" == "HOT" ]
then
	$HSPATH/homeScript.py -s fan 1
else
	$HSPATH/homeScript.py -s fan 0
fi
