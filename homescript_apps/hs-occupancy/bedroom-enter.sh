#!/bin/bash

HSPATH='/home/shares/public/scripts/HomeScript'
HSW=$HSPATH'/homescript_apps/hs-weather/hs-weather.py'
HSSD=$HSPATH'/homescript_apps/hs-sun/hs-sun-debug.py'

SUNSETTIME=$($HSSD sunset)
SUNRISETIME=$($HSSD sunrise)

if [ $(echo $SUNSETTIME | cut -d ' ' -f 2) -ge $(date +%H) ] && [ $(echo $SUNSETTIME | cut -d ' ' -f 1) -ge $(date +%M) ]
then
	NIGHT=1
elif [ $(echo $SUNRISETIME | cut -d ' ' -f 2) -le $(date +%H) ] && [ $(echo $SUNRISETIME | cut -d ' ' -f 1) -le $(date +%M) ]
then
	NIGHT=1
else
	NIGHT=0
fi

if [ "$NIGHT" == "1" ]
then
	if [ "$($HSPATH/homeScript.py -g double | cut -d ' ' -f 2)" == "False" ]
	then
		$HSPATH/homeScript.py -s double 1
		if [ "$(python3 $HSW -h)" == "HOT" ]
		then
			$HSPATH/homeScript.py -s fan 1
		else
			$HSPATH/homeScript.py -s fan 0
		fi
	fi
elif [ "$(python3 $HSW -h)" == "HOT" ]
then
	$HSPATH/homeScript.py -s fan 1
fi
