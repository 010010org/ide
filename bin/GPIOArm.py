import RPi.GPIO as GPIO
import time

M1 = (2, 3)
M2 = (14, 15)
M3 = (17, 18)
M4 = (27, 22)
M5 = (23, 24)
channel_list = list(M1) + list(M2) + list(M3) + list(M4) + list(M5)

GPIO.setup(channel_list, GPIO.OUT)
GPIO.output(channel_list, GPIO.HIGH)

class Part(object):
	def __init__(self, pin):
		self.pin = pin

	def move(piin, timer):
		GPIO.output(piin, GPIO.LOW)
		if(timer):
			time.sleep(timer)
			GPIO.output(piin, GPIO.HIGH)

	def up(timer=None):
		move(pin[0], timer)

	def down(timer=None):
		move(pin[1], timer)

class Base(Part):
	def __init__(self):
		super().__init__(M1)

	def counter(timer=None):
		self.up(timer)

	def clock(timer=None):
		self.down(timer)


