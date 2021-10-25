import configparser  # library used to read ini file
import os.path  # library used to test if file exists (to see if we're running on a pi)


class Arm(object):
	_iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
	_iniWriter.optionxform = str
	_iniFile = "lib/robotArm/pinout.ini"
	_runningOnPi = 0
	_debugmode = 1
	print("debugmode is", _debugmode)

	def __init__(self):
		# read configured pins from ini file
		self._iniWriter.read(self._iniFile)
		_M1 = self._iniWriter["robotArm"]["M1"].split(",")
		_M2 = self._iniWriter["robotArm"]["M2"].split(",")
		_M3 = self._iniWriter["robotArm"]["M3"].split(",")
		_M4 = self._iniWriter["robotArm"]["M4"].split(",")
		_M5 = self._iniWriter["robotArm"]["M5"].split(",")
		_M_LIGHT = self._iniWriter["robotArm"]["M_LIGHT"].split(",")
		_channel_list = _M1 + _M2 + _M3 + _M4 + _M5 + _M_LIGHT  # creates a list of all used pins so you can run through them with a for loop.
		# If running on a pi, set all used pins to output and turn off their power
		if os.path.exists("/sys/firmware/devicetree/base/model"):
			with open("/sys/firmware/devicetree/base/model") as file:
				if "Raspberry Pi" in file.read():
					import RPi.GPIO as GPIO
					GPIO.setmode(GPIO.BCM)
					for i in _channel_list:
						GPIO.setup(int(i), GPIO.OUT)
						GPIO.output(int(i), GPIO.LOW)
					self._runningOnPi = 1
			file.close()

		# create the different parts of the arm
		self.base = self.Base(_M5, self._runningOnPi, "base" )
		self.shoulder = self.GenericPart(_M4, self._runningOnPi, "shoulder")
		self.elbow = self.GenericPart(_M3, self._runningOnPi, "elbow")
		self.wrist = self.GenericPart(_M2, self._runningOnPi, "wrist")
		self.grip = self.Grip(_M1, self._runningOnPi, "grip")
		self.light = self.Light(_M_LIGHT, self._runningOnPi, "light")

	#function that writes the printlines to a separate file.
	def write_to_file():
		print("off")



	# This is the parent class of all parts. This contains the functions that actually move the part.
	class Part(object):
		_pins = []
		_tempPWM = None
		_runningOnPi = 0
		_name = ""

		def __init__(self, pins, runningOnPi, name):
			self._pins = pins
			self._runningOnPi = runningOnPi
			self._name = name


		
		

		# This is the only real function to move one the motors, all the other functions just give this function a different name for ease of use.
		# Do NOT attempt to call this function directly, it's only meant for internal use.
		def _move(self, pin, power=0):
			# This code actually powers the motors. It only runs if the program is running on a pi
			if self._runningOnPi:
				import RPi.GPIO as GPIO
				self._tempPWM = GPIO.PWM(int(pin), 50)  # turns on PWM at the specified pin at 50 Hz (no real reason for 50 Hz specifically)
				# if a PWM percentage is given, the motor will use that. Otherwise, use full power
				if power > 0 & power < 100:
					self._tempPWM.start(power)
				else:
					self._tempPWM.start(100)
				if not Arm._debugmode:
					return
			# "Simulation code" for when the code is run on a different device. Prints to the console for now.
			print("robotArm powering pin", pin, "of part", self._name, end=" ")
			if power > 0 & power < 100:
				print("at " + str(power) + "% power", end=" ")
			print("")  # creates a new line to keep the console log readable
			return

		# Turns off a part if running on a pi. Only prints to the console otherwise.
		def off(self):
			if self._runningOnPi:
				if self._tempPWM is not None:
					self._tempPWM.stop()
				if not Arm._debugmode:
					return
			# Simulation code
			#print("power off pins:", end=" "), [print(i, end=" ") for i in self._pins], print("")
			Arm.write_to_file()
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
