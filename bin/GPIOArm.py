import RPi.GPIO as GPIO
import time


class Arm(object):
	M1 = (2, 3)
	M2 = (14, 15)
	M3 = (17, 18)
	M4 = (27, 22)
	M5 = (23, 24)
	M_LIGHT = 25,
	channel_list = list(M1) + list(M2) + list(M3) + list(M4) + list(M5) + list(M_LIGHT)

	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		for i in self.channel_list:
				GPIO.setup(i, GPIO.OUT)
				GPIO.output(i, GPIO.LOW)

		self.base = self.Base(self.M5)
		self.shoulder = self.Shoulder(self.M4)
		self.elbow = self.Elbow(self.M3)
		self.wrist = self.Wrist(self.M2)
		self.grip = self.Grip(self.M1)
		self.light = self.Light(self.M_LIGHT)

	class Part(object):
		pins = (0, 0)

		def __init__(self, pins):
			self.pins = pins

		def move(self, pin, timer=0):
			GPIO.output(pin, GPIO.HIGH)
			if timer <= 0:
				return
			time.sleep(timer)
			GPIO.output(pin, GPIO.LOW)

		def up(self, timer=0):
			self.move(self.pins[0], timer)

		def down(self, timer=0):
			self.move(self.pins[1], timer)

		def off(self):
			GPIO.output(self.pins, LOW)

	class Base(Part):
		def __init__(self, pins):
			super().__init__(pins)

		def counter(self, timer=0):
			self.up(timer)

		def clock(self, timer=0):
			self.down(timer)

	class Shoulder(Part):
		def __init__(self, pins):
			super().__init__(pins)

	class Elbow(Part):
		def __init__(self, pins):
			super().__init__(pins)

	class Wrist(Part):
		def __init__(self, pins):
			super().__init__(pins)

	class Grip(Part):
		def __init__(self, pins):
			super().__init__(pins)

		def close(self, timer=0):
			self.up(timer)

		def open(self, timer=0):
			self.down(timer)


	class Light(Part):
		def __init__(self, pin):
			self.pin = pin

		def on(self, timer=0):
			GPIO.output(self.pin, GPIO.HIGH)
			if timer <= 0:
				return
			time.sleep(timer)
			GPIO.output(self.pin, GPIO.LOW)

		def off(self):
			GPIO.output(self.pin, GPIO.LOW)
