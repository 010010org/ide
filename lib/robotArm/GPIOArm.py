import time  # library used to wait for a specified time
import localisationdata as ld  # library that contains all displayed text
import ctypes.util  # library used to detect if we're running on a raspberry pi or a different os


class Arm(object):
	# These are the GPIO pins the parts of the arm are connected to.
	# TODO: read and save from/to an .ini file
	_M1 = (2, 3)
	_M2 = (14, 15)
	_M3 = (17, 18)
	_M4 = (27, 22)
	_M5 = (23, 24)
	_M_LIGHT = (25, 25)  # written twice because the Part class expects a tuple with two integers.
	_channel_list = list(_M1) + list(_M2) + list(_M3) + list(_M4) + list(_M5) + list(_M_LIGHT)  # creates a list of all used pins so you can run through them with a for loop.
	_partList = ["base", "shoulder", "elbow", "wrist", "grip", "light"]  # not used internally, so should not be private (or even exist). TODO: fix

	def __init__(self):
		# If running on a pi, set all used pins to output and turn off their power
		if ctypes.util.find_library("RPi.GPIO"):
			import RPi.GPIO as GPIO
			GPIO.setmode(GPIO.BCM)
			for i in self._channel_list:
				GPIO.setup(i, GPIO.OUT)
				GPIO.output(i, GPIO.LOW)

		# create the different parts of the arm
		self.base = self.Base(self._M5, ld.partList[0])
		self.shoulder = self.Shoulder(self._M4, ld.partList[1])
		self.elbow = self.Elbow(self._M3, ld.partList[2])
		self.wrist = self.Wrist(self._M2, ld.partList[3])
		self.grip = self.Grip(self._M1, ld.partList[4])
		self.light = self.Light(self._M_LIGHT, ld.partList[5])

	# This is the parent class of all parts. This contains the functions that actually move the part.
	class Part(object):
		tempPWM = None
		pins = (0, 0)

		def __init__(self, pins):
			self.pins = pins

		# This is the only real function to move one the motors, all the other functions just give this function a different name for ease of use.
		def move(self, pin, power=0, timer=0):
			# This code actually powers the motors. It only runs of the program is running on a pi
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
			print("Powering pin", pin, end=" ")
			if timer > 0:
				print("for", timer, "seconds", end=" ")
			if power > 0 & power < 100:
				print("at " + str(power) + "% power", end=" ")
			print("")  # creates a new line (yes, really) to keep the console log readable
			return

		# up() and down() only specify the pin they want to move to the move function.
		# these are mapped to the keyboard in tkArmInterface.
		def up(self, power=0, timer=0):
			self.move(self.pins[0], power, timer)

		def down(self, power=0, timer=0):
			self.move(self.pins[1], power, timer)

		# Turns off a part if running on a pi. Only prints to the console otherwise.
		def off(self):
			if ctypes.util.find_library("RPi.GPIO"):
				self.tempPWM.stop()
				return
			print("power off pins:", self.pins[0], self.pins[1])
			pass

	# Because the base moves horizontally instead of vertically, up and down have been renamed to counter and clock.
	# You can still use up and down if you'd want to for whatever reason.
	class Base(Part):
		def __init__(self, pins, name):
			self.name = name
			super().__init__(pins)

		def counter(self, power=0, timer=0):
			self.up(power, timer)

		def clock(self, power=0, timer=0):
			self.down(power, timer)

	# Shoulder, Elbow and Wrist don't have any special functions. They're only individual classes to make the code easier to read.
	class Shoulder(Part):
		def __init__(self, pins, name):
			self.name = name
			super().__init__(pins)

	class Elbow(Part):
		def __init__(self, pins, name):
			self.name = name
			super().__init__(pins)

	class Wrist(Part):
		def __init__(self, pins, name):
			self.name = name
			super().__init__(pins)

	# Just like the Base, the Grip moves differently. As such, the functions have been renamed.
	class Grip(Part):
		def __init__(self, pins, name):
			self.name = name
			super().__init__(pins)

		def close(self, power=0, timer=0):
			self.up(power, timer)

		def open(self, power=0, timer=0):
			self.down(power, timer)

	# Because the light can only go on or off, directions don't matter. Calling either up() or down() will turn it on.
	# I chose to use up because it was shorter.
	class Light(Part):
		def __init__(self, pins, name):
			self.name = name
			super().__init__(pins)

		def on(self, power=0, timer=0):
			self.up(power, timer)
