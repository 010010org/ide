#!/bin/bash
. config.ini

for folder in `find ./lib -maxdepth 1 -mindepth 1 -type d -not -name .svn`; do
	if !(test -f ${folder}/controls.ini); then
		cp ${folder}/defaultControls.ini ${folder}/controls.ini
	fi
	if !(test -f ${folder}/pinout.ini); then
		cp ${folder}/defaultPinout.ini ${folder}/pinout.ini
	fi
	if test -f ${folder}/localisation/${LANGUAGE}.py; then
		cp ${folder}/localisation/${LANGUAGE}.py ${folder}/${folder#"./lib/"}Localisationdata.py
	else
		cp ${folder}/localisation/en.py ${folder}/${folder#"./lib/"}Localisationdata.py
	fi
done
if test -f ./localisation/${LANGUAGE}.py; then
	cp  ./localisation/${LANGUAGE}.py ./bin/localisationdata.py
else
	cp ./localisation/en.py ./bin/localisationdata.py
fi

if [[ ! $(pip3 list|grep "pygments") ]]; then
    pip3 install pygments
fi

#change this line to the python variable you want to use
python3.7 ./bin/startMenu.py

