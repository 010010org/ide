import RPi.GPIO as GPIO
import time
import threading


class PartThread(threading.Thread):
	isRunning = True

	def __init__(self, part, name):
		self.part = part
		self.name = name
		threading.Thread.__init__(self)
		self.daemon = True
		self.start()

	def run(self):
		while self.isRunning:
			pass

	def up(self, timer=0):
		if hasattr(self.part, "up"):
			self.part.up(timer)
		else:
			print(self.name + "can't move up or down!")

	def down(self, timer=0):
		if hasattr(self.part, "down"):
			self.part.down(timer)
		else:
			print(self.name + "can't move up or down!")

	def left(self, timer=0):
		if hasattr(self.part, "left"):
			self.part.left(timer)
		else:
			print(self.name + "can't move left or right!")

	def right(self, timer=0):
		if hasattr(self.part, "right"):
			self.part.right(timer)
		else:
			print(self.name + "can't move left or right!")

	def open(self, timer=0):
		if hasattr(self.part, "open"):
			self.part.open(timer)
		else:
			print(self.name + "can't open or close!")

	def close(self, timer=0):
		if hasattr(self.part, "close"):
			self.part.close(timer)
		else:
			print(self.name + "can't open or close!")

	def on(self, timer=0):
		if hasattr(self.part, "on"):
			self.part.on(timer)
		else:
			print(self.name + "can't just turn on!")

	def off(self):
		self.part.off()


class Arm(object):
	# Dit zijn de GPIO pins waar de verschillende onderdelen van de robotarm mee aangestuurd worden.
	# De eerste pin is voor omhoog, de tweede voor omlaag.
	M1 = (2, 3)
	M2 = (14, 15)
	M3 = (17, 18)
	M4 = (27, 22)
	M5 = (23, 24)
	M_LIGHT = 25,
	channel_list = list(M1) + list(M2) + list(M3) + list(M4) + list(M5) + list(M_LIGHT)
	threads = []

	# Wanneer de arm geinitialiseerd wordt zet deze alle pins op output en haalt ie overal de stroom af, voor het geval
	# dat de pins hiervoor ergens anders voor gebruikt zijn en er nog stroom op staat.
	# Ook maakt de Arm threads aan voor alle verschillende onderdelen, zodat deze tegelijk (met naam) aangestuurd
	# kunnen worden.
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		for i in self.channel_list:
			GPIO.setup(i, GPIO.OUT)
			GPIO.output(i, GPIO.LOW)

		self.base = PartThread(self.Base(self.M5), "base")
		self.shoulder = PartThread(self.Shoulder(self.M4), "shoulder")
		self.elbow = PartThread(self.Elbow(self.M3), "elbow")
		self.wrist = PartThread(self.Wrist(self.M2), "wrist")
		self.grip = PartThread(self.Grip(self.M1), "grip")
		self.light = PartThread(self.Light(self.M_LIGHT), "light")

		self.threads.append(self.base)
		self.threads.append(self.shoulder)
		self.threads.append(self.elbow)
		self.threads.append(self.wrist)
		self.threads.append(self.grip)
		self.threads.append(self.light)

	def close(self):
		for i in self.threads:
			i.isRunning = False

	# Dit is de parent class van alle motoren. Hierin staan de functies voor het aansturen.
	class Part(object):
		pins = (0, 0)

		def __init__(self, pins):
			self.pins = pins

		# Dit is eigenlijk de enige bewegingsfunctie.
		# up() en down() vullen gewoon de pin in die aangestuurd moet worden.
		# De functie kan met of zonder timer aangestuurd worden. als er een timer meegegeven wordt gaat de motor uit
		# zodra de timer afgelopen is. Zo niet, dan blijft de motor aan staan tot hij weer uitgezet wordt.
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

		# Deze functie zet de motor weer uit.
		def off(self):
			GPIO.output(self.pins, GPIO.LOW)

	# Omdat de base-motor niet naar boven en beneden maar naar links en rechts gaat
	# heeft deze een andere naam voor up en down. Dit is gedaan voor gebruiksgemak.
	# Indien gewenst kan de base ook met up en down aangestuurd worden.
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

	# Net als bij de base gaat de grijper niet naar boven en beneden en zijn de functies dus hernoemd.
	class Grip(Part):
		def __init__(self, pins):
			super().__init__(pins)

		def close(self, timer=0):
			self.up(timer)

		def open(self, timer=0):
			self.down(timer)

	# Omdat het lampje alleen aan of uit kan in plaats van omhoog en omlaag (en dus ook maar 1 pin in plaats van 2)
	# gebruikt deze alleen een hernoemde versie van up(). down() zet het lampje ook aan. off() staat al in Part().
	class Light(Part):
		def __init__(self, pin):
			super().__init__((pin, pin))

		def on(self, timer=0):
			self.up(timer)
