import RPi.GPIO as GPIO
import time

class Arm(object):
	M1 = (2, 3)
	M2 = (14, 15)
	M3 = (17, 18)
	M4 = (27, 22)
	M5 = (23, 24)
	M_LIGHT = ()
	channel_list = list(M1) + list(M2) + list(M3) + list(M4) + list(M5) + list(M_LIGHT)

	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		for i in channel_list:
        		GPIO.setup(i, GPIO.OUT)
	        	GPIO.output(i, GPIO.HIGH)

		base=Base(M5)
		shoulder=Shoulder(M4)
		elbow=Elbow(M3)
		wrist=Wrist(M2)
		grip=Grip(M1)

	class Part(object):
		pins=(0,0)

		def __init__(self, pins):
			self.pins=pins

		def move(self, pin, timer=0):
       	        	GPIO.output(pin, GPIO.LOW)
        	        if(timer>0):
       	        	        time.sleep(timer)
               	        	GPIO.output(pin, GPIO.HIGH)

		def up(self, timer=0):
			self.move(pins[0], timer)

        	def down(self, timer=0):
       	        	self.move(pins[1], timer)

	class Base(Part):
		def __init__(self, pins):
			super.__init__(pins)

		def counter(self, timer=0):
			self.up(timer)

		def clock(self, timer=0):
			self.down(timer)

	class Shoulder(Part):
		def __init__(self, pins):
			super.__init__(pins)

	class Elbow(Part):
		def __init__(self, pins):
			super.__init__(pins)

	class Wrist(Part):
		def __init__(self, pins):
			super.__init__(pins)

	class Grip(Part):
		def __init__(self, pins):
			super.__init__(pins)

		def close(timer=0):
			self.up(timer)

		def open(timer=0):
			self.down(timer)

arm = Arm()
input("Press Enter when ready...")

arm.base.counter(1)
