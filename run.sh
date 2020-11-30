#!/bin/bash
. config.ini

for folder in `find ./lib -type d -maxdepth 1 -mindepth 1 -not -name .svn`
	if !(test -f ./lib/${folder}/controls.ini); then
		cp ./lib/${folder}/defaultControls.ini ./lib/${folder}/controls.ini
	fi
	if !(test -f ./lib/${folder}/pinout.ini); then
		cp ./lib/${folder}/defaultPinout.ini ./lib/${folder}/pinout.ini
	fi
	if test -f ./lib/${folder}/localisation/${LANGUAGE}.py; then
		cp ./lib/${folder}/localisation/${LANGUAGE}.py ./lib/${folder}/${folder}Localisationdata.py
	else
		cp ./lib/${folder}/localisation/en.py ./lib/${folder}/${folder}Localisationdata.py
	fi
if test -f ./localisation/${LANGUAGE}.py; then
	cp  ./localisation/${LANGUAGE}.py ./bin/localisationdata.py
else
	cp ./localisation/en.py ./bin/localisationdata.py
fi

python3 ./bin/startMenu.py
