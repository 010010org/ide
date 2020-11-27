#!/bin/bash
. config.ini

cp  ./localisation/${LANGUAGE}.py ./bin/localisationdata.py
if !(test -f "./lib/robotArm/controls.ini"); then
	cp ./lib/robotArm/defaultControls.ini ./lib/robotArm/controls.ini
fi
if !(test -f "./lib/robotArm/pinout.ini"); then
	cp ./lib/robotArm/defaultPinout.ini ./lib/robotArm/pinout.ini
fi

python3 ./bin/startMenu.py
