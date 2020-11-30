For a library to be properly recognized by the program, it needs the following format:

\---[library name]
    |   defaultControls.ini		# Contains the default keybinds to be used, see format below.
    |   defaultPinout.ini		# Contains the pins used to connect the device to the Pi, see format below.
    |   [library name].py		# Contains the actual code used to run the device. Name MUST be identical to folder name or the file won't be able to be found.
    |
    \---localisation			# Contains the translation dictionary, see format below.
            en.py			# English files are required as a fallback if the chosen language isn't supported.
            [other language].py		# All other languages are optional. You can add as many languages as you want.
            ...

When the code is first ran after you install your library, it will generate 3 files:
pinout.ini
controls.ini
[library name]Localisationdata.py

These files are copies of the defaults and the selected language file and are what is actually used by the code.



---------------------
|defaultControls.ini|
---------------------
[part]					# This is the name you use for the object of the part in your code. every part needs their own object, and every object needs to be described here.
fuction1 = keybind1			# Everything you want a part of your device to do needs it's own function, and every function needs a unique keybind.
function2 = keybind2			# The keybinds are case-sensitive, 'A' is a different keybind from 'a'.

[part2]					# You can add as many objects as you want, and as many functions as you want to each object.
function1 = keybind3			# Just keep in mind that everything here need to have the exact same name as it has in your code.
...



-------------------
|defaultPinout.ini|
-------------------
[library name]				# This name needs to be identical to your folder and code file.
device1=pin1,pin2,pin3			# All individual i/o devices need to have unique pins. Only GPIO pins need to be put here, ground/5v etc can be ignored.
device2=pin4,pin5			# Pins need to be seperated by a comma, without spaces. Your code needs to read and implement the pins from the pinouts.ini file.
...



-------
|en.py|						# Please use ISO 639-1 for language names (en, nl, de). If you want to add regional variants, use a dash followed by the ISO 3166-1 alpha-2 code (en-US, nl-BE, de-AT). If you for some reason want to implement a language without an ISO code (LOLCAT or Pirate English for example), you are free to choose your own abbreviation.
-------
partDictionary = {				# The dictionary NEEDS to have this exact name for it to be found by the code.
	"[object1]" = "[translation1]"		# All objects need to have their name translated into the specified language. For English this would probably be the actual name you used.
	"[object2]" = "[translation2]"		# Both the names of objects/functions and their translations should be strings.
	...
	"[function1]" = "[translation3]"	# All functions need to have their name translated as well.
	"[function2]" = "[translation4]"
	...
}
