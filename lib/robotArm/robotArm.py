import time  # library used to wait for a specified time
import ctypes.util  # library used to detect if we're running on a raspberry pi or a different os
import configparser  # library used to read ini file


class Arm(object):
	_iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
	_iniWriter.optionxform = str
	_iniFile = "lib/robotArm/pinout.ini"

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
		if ctypes.util.find_library("RPi.GPIO"):
			import RPi.GPIO as GPIO
			GPIO.setmode(GPIO.BCM)
			for i in _channel_list:
				GPIO.setup(i, GPIO.OUT)
				GPIO.output(i, GPIO.LOW)

		# create the different parts of the arm
		self.base = self.Base(_M5)
		self.shoulder = self.GenericPart(_M4)
		self.elbow = self.GenericPart(_M3)
		self.wrist = self.GenericPart(_M2)
		self.grip = self.Grip(_M1)
		self.light = self.Light(_M_LIGHT)

	# This is the parent class of all parts. This contains the functions that actually move the part.
	class Part(object):
		_pins = []

		def __init__(self, pins):
			self._pins = pins

		# This is the only real function to move one the motors, all the other functions just give this function a different name for ease of use.
		# Do NOT attempt to call this function directly, it's only meant for internal use.
		def _move(self, pin, power=0, timer=0):
			# This code actually powers the motors. It only runs if the program is running on a pi
			if ctypes.util.find_library("RPi.GPIO"):
				import RPi.GPIO as GPIO
				self.tempPWM = GPIO.PWM(pin, 50)  # turns on PWM at the specified pin at 50 Hz (no real reason for 50 Hz specifically)
				# if a PWM percentage is given, the motor will use that. Otherwise, use full power
				if power > 0 & power < 100:
					self.tempPWM.start(power)
				else:
					self.tempPWM.start(100)
				# if a timer is specified, turn off after that time. Otherwise, don't turn off.
				if timer <= 0:
					return
				time.sleep(timer)
				self.tempPWM.stop()
				return
			# "Simulation code" for when the code is run on a different device. Prints to the console.
			print("robotArm powering pin", pin, "of part", self.__class__.__name__, end=" ")
			if timer > 0:
				print("for", timer, "seconds", end=" ")
			if power > 0 & power < 100:
				print("at " + str(power) + "% power", end=" ")
			print("")  # creates a new line (yes, really) to keep the console log readable
			return

		# Turns off a part if running on a pi. Only prints to the console otherwise.
		def off(self):
			if ctypes.util.find_library("RPi.GPIO"):
				self.tempPWM.stop()
				return
			print("power off pins:", self._pins[0], self._pins[1])
			pass

	# shoulder, elbow and wrist don't have any special functions. They're just the same part, but with different names.
	class GenericPart(Part):
		def __init__(self, pins):
			super().__init__(pins)

		# up() and down() only specify the pin they want to move to the _move function.
		def up(self, power=0, timer=0):
			self._move(self._pins[0], power, timer)

		def down(self, power=0, timer=0):
			self._move(self._pins[1], power, timer)

	# Because the base moves horizontally instead of vertically, it has clock and counter functions instead of up and down.
	class Base(Part):
		def __init__(self, pins):
			super().__init__(pins)

		def counter(self, power=0, timer=0):
			self._move(self._pins[0], power, timer)

		def clock(self, power=0, timer=0):
			self._move(self._pins[1], power, timer)

	# Just like the Base, the Grip moves differently. As such, it has different functions.
	class Grip(Part):
		def __init__(self, pins):
			super().__init__(pins)

		def close(self, power=0, timer=0):
			self._move(self._pins[0], power, timer)

		def open(self, power=0, timer=0):
			self._move(self._pins[1], power, timer)

	# Because the light can only go on or off, it only has one "movement" function.
	class Light(Part):
		def __init__(self, pins):
			super().__init__(pins)

		def on(self, power=0, timer=0):
			self._move(self._pins[0], power, timer)
