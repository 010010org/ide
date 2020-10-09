#!/bin/bash
. config.ini

cp  ./localisation/${LANGUAGE}.py ./bin/localisationData.py
python3 ./bin/tkinterTest.py
