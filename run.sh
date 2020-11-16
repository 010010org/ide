#!/bin/bash
. config.ini

cp  ./localisation/${LANGUAGE}.py ./bin/localisationdata.py
if !(test -f "./lib/robotArm/armControls.ini"); then
	cp ./lib/robotArm/defaultArmControls.ini ./lib/robotArm/armControls.ini
fi

python3 ./bin/startMenu.py
