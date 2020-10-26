#!/bin/bash
. config.ini

cp  ./localisation/${LANGUAGE}.py ./bin/localisationdata.py
if !(test -f "./bin/armControls.ini"); then
	cp ./bin/defaultArmControls.ini ./bin/armControls.ini
fi

python3 ./bin/startMenu.py
