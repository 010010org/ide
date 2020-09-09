import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup((2,3), GPIO.OUT)
input("start test...")
while(1):
	try:
		GPIO.output(2, GPIO.HIGH)
		GPIO.output(3, GPIO.LOW)
		time.sleep(0.5)
		GPIO.output(2, GPIO.LOW)
		GPIO.output(3, GPIO.HIGH)
		time.sleep(0.5)
	except KeyboardInterrupt:
		GPIO.cleanup()
		raise
