#!/bin/bash
. config.ini

cp  ./localisation/${LANGUAGE}.py ./bin/localisationdata.py
python3 ./bin/tkinterTest.py
