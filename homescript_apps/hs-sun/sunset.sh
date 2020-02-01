#!/bin/bash

HSPATH=/home/shares/public/scripts/HomeScript/
PIH=$HSPATH/homescript_apps/hs-pih/hs-pih.py

if [ "$(python3 $PIH shayan)" == "1" ]
then
	$HSPATH/homeScript.py -s double 1
fi

