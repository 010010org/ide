import configparser  # library used to read ini file
import os.path # library used to test if file exists (to see if we're running on a pi)
import robotArmLocalisationdata as ld  
#from pynput import keyboard
import time

class Arm(object):
	_iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
	_iniWriter.optionxform = str
	#pathfiles to different files so it only needs to be noted once and can easily be changed
	_iniFile = "lib/robotArm/pinout.ini"
	_robotOutputFile = "lib/robotArm/robot_output.txt"
	_raspberryPiPath = "/sys/firmware/devicetree/base/model"
	_runningOnPi = False
	_debugmode = True


	#function that checks if the file exists and returns true or false.
	#also resolves errors that might occur, the open function creates a file if none is found. that can cause communication issues with simpylc or any other program.
	def file_check(self, path_to_file):
		return os.path.exists(path_to_file)

	def __init__(self):
		# read configured pins from ini file
		#each motor has 2 pins, on or off, up or down.
		self._iniWriter.read(self._iniFile)
		_M1 = self._iniWriter["robotArm"]["M1"].split(",")
		_M2 = self._iniWriter["robotArm"]["M2"].split(",")
		_M3 = self._iniWriter["robotArm"]["M3"].split(",")
		_M4 = self._iniWriter["robotArm"]["M4"].split(",")
		_M5 = self._iniWriter["robotArm"]["M5"].split(",")
		_M_LIGHT = self._iniWriter["robotArm"]["M_LIGHT"].split(",")
		# creates a list of all used pins
		_channel_list = _M1 + _M2 + _M3 + _M4 + _M5 + _M_LIGHT  
		
		
		# If running on a pi, set all used pins to output and turn off their power as Raspberry pi sometimes uses these pins on startup.
		if os.path.exists(self._raspberryPiPath):
			with open(self._raspberryPiPath) as file:
				if "Raspberry Pi" in file.read():
					import RPi.GPIO as GPIO
					GPIO.setmode(GPIO.BCM)
					for i in _channel_list:
						GPIO.setup(int(i), GPIO.OUT)
						GPIO.output(int(i), GPIO.LOW)
					self._runningOnPi = True
			file.close()
		
		# create the different parts of the arm, passing the motor number, runnningOnPi and name of the part of the motor.
		self.base = self.Base(_M5, self._runningOnPi, "base" )
		self.shoulder = self.GenericPart(_M4, self._runningOnPi, "shoulder")
		self.elbow = self.GenericPart(_M3, self._runningOnPi, "elbow")
		self.wrist = self.GenericPart(_M2, self._runningOnPi, "wrist")
		self.grip = self.Grip(_M1, self._runningOnPi, "grip")
		self.light = self.Light(_M_LIGHT, self._runningOnPi, "light")

		if self.file_check(self._robotOutputFile):
			file = open(self._robotOutputFile, "w")
			#truncate makes the file empty.
			file.truncate()
			file.close()

	#function that writes the printlines to a separate file.
	def write_to_file(self, path_to_file, message):
		#checks if file exists
		if Arm.file_check(self, path_to_file): 
			file = open (path_to_file, "a")
			file.write(str(message + "\n"))
			file.close()

		else:
			print(path_to_file, ld.fileError )#ld


	# This is the parent class of all parts. This contains the functions that actually move the part.
	class Part(object):
		_pins = []
		_tempPWM = None
		_runningOnPi = False
		_name = ""

		def __init__(self, pins, runningOnPi, name):
			self._pins = pins
			self._runningOnPi = runningOnPi
			self._name = name
			self._debugmode = Arm._debugmode
			self._timeTaken = 0
		
		def time(self):
			import random
			return str(random.randint(10,50))
		
		
		# This is the only real function to move one the motors, all the other functions just give this function a different name for ease of use.
		# Do NOT attempt to call this function directly, it's only meant for internal use.
		def _move(self, pin, power = 0):
			# This code actually powers the motors. It only runs if the program is running on a pi
			if self._runningOnPi:
				import RPi.GPIO as GPIO
				self._tempPWM = GPIO.PWM(int(pin), 50)  # turns on PWM at the specified pin at 50 Hz (no real reason for 50 Hz specifically)
				# if a PWM percentage is given, the motor will use that. Otherwise, use full power
				if power > 0 & power < 100:
					self._tempPWM.start(power)
				else:
					self._tempPWM.start(100)
				if not self._debugmode:
					return
			# "Simulation code" for when the code is run on a different device. Prints to self._robotOutputFile
			
			#TODO time of key pressed instead of random int.
			message = str("robotarm powering pin " + pin + " from part " + self._name + " for " + self.time() + " second(s).")
			#cannot enter the if statement, assuming it works.
			if power > 0 & power < 100:
				message += (" at " + str(power) + "% power")
				print("appended")
			Arm.write_to_file(self, Arm._robotOutputFile, message)
			return

		# Turns off a part if running on a pi. Only prints to the console otherwise.
		def off(self):
			if self._runningOnPi:
				if self._tempPWM is not None:
					self._tempPWM.stop()
				#checks if debugmode is turned off, otherwise prints to file
				if not self._debugmode:
					return
			# Simulation code
			message = "power off pins: " 
			for i in self._pins:
				message += str(i + " ")
			
			#currently not needed
			#Arm.write_to_file(self, Arm._robotOutputFile, message)
			return
		

		
	


	# shoulder, elbow and wrist don't have any special functions. They're just the same part, but with different names.
	class GenericPart(Part):
		def __init__(self, pins, runningOnPi, name):
			super().__init__(pins, runningOnPi, name)

		# up() and down() only specify the pin they want to move to the _move function.
		def up(self, power=0):
			self._move(self._pins[0], power)

		def down(self, power=0):
			self._move(self._pins[1], power)

	# Because the base moves horizontally instead of vertically, it has clock and counter functions instead of up and down.
	class Base(Part):
		def __init__(self, pins, runningOnPi, name):
			super().__init__(pins, runningOnPi, name)

		def counter(self, power=0):
			self._move(self._pins[0], power)

		def clock(self, power=0):
			self._move(self._pins[1], power)

	# Just like the Base, the Grip moves differently. As such, it has different functions.
	class Grip(Part):
		def __init__(self, pins, runningOnPi, name):
			super().__init__(pins, runningOnPi, name)

		def close(self, power=0):
			self._move(self._pins[0], power)

		def open(self, power=0):
			self._move(self._pins[1], power)

	# Because the light can only go on or off, it only has one "movement" function.
	class Light(Part):
		def __init__(self, pins, runningOnPi, name):
			super().__init__(pins, runningOnPi, name)

		def on(self, power=0):
			self._move(self._pins[0], power)
