import serial
import string

output = " "
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
while True:
	while output != "":
		output = ser.readline()
		print(output)
		output = " "
