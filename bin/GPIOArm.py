import pigpio
import time
import localisationdata as ld


class Arm(object):
	# Dit zijn de GPIO pins waar de verschillende onderdelen van de robotarm mee aangestuurd worden.
	# De eerste pin is voor omhoog, de tweede voor omlaag.
	_M1 = (2, 3)
	_M2 = (14, 15)
	_M3 = (17, 18)
	_M4 = (27, 22)
	_M5 = (23, 24)
	_M_LIGHT = 25,
	_channel_list = list(_M1) + list(_M2) + list(_M3) + list(_M4) + list(_M5) + list(_M_LIGHT)
	_threads = []
	_partList = ["base", "shoulder", "elbow", "wrist", "grip", "light"]
	_pwmPins = pigpio.pi()

	# Wanneer de arm geinitialiseerd wordt zet deze alle pins op output en haalt ie overal de stroom af, voor het geval
	# dat de pins hiervoor ergens anders voor gebruikt zijn en er nog stroom op staat.
	# Ook maakt de Arm threads aan voor alle verschillende onderdelen, zodat deze tegelijk (met naam) aangestuurd
	# kunnen worden.
	def __init__(self):
		for i in self._channel_list:
			self._pwmPins.set_mode(i, pigpio.OUTPUT)

		self.base = self.Base(self._M5, ld.partList[0])
		self.shoulder = self.Shoulder(self._M4, ld.partList[1])
		self.elbow = self.Elbow(self._M3, ld.partList[2])
		self.wrist = self.Wrist(self._M2, ld.partList[3])
		self.grip = self.Grip(self._M1, ld.partList[4])
		self.light = self.Light(self._M_LIGHT, ld.partList[5])

	def close(self):
		for i in self._threads:
			i.isRunning = False

	# Dit is de parent class van alle motoren. Hierin staan de functies voor het aansturen.
	class Part(object):
		_pwmPins = pigpio.pi()
		pins = (0, 0)

		def __init__(self, pins):
			self.pins = pins

		# Dit is eigenlijk de enige bewegingsfunctie.
		# up() en down() vullen gewoon de pin in die aangestuurd moet worden.
		# De functie kan met of zonder timer aangestuurd worden. als er een timer meegegeven wordt gaat de motor uit
		# zodra de timer afgelopen is. Zo niet, dan blijft de motor aan staan tot hij weer uitgezet wordt.
		def move(self, pin, power=0, timer=0):
			if power > 0:
				if power < 4:
					self._pwmPins.set_PWM_dutycycle(pin, round(256*(power/4.0)))
			else:
				self._pwmPins.set_PWM_dutycycle(pin, 255)
			if timer <= 0:
				return
			time.sleep(timer)
			self._pwmPins.set_PWM_dutycycle(pin, 0)

		def up(self, power=0, timer=0):
			self.move(self.pins[0], power, timer)

		def down(self, power=0, timer=0):
			self.move(self.pins[1], power, timer)

		# Deze functie zet de motor weer uit.
		def off(self):
			self._pwmPins.set_PWM_dutycycle(self.pins, 0)
			pass

	# Omdat de base-motor niet naar boven en beneden maar naar links en rechts gaat
	# heeft deze een andere naam voor up en down. Dit is gedaan voor gebruiksgemak.
	# Indien gewenst kan de base ook met up en down aangestuurd worden.
	class Base(Part):
		def __init__(self, pins, name):
			self.name = name
			super().__init__(pins)

		def counter(self, power=0, timer=0):
			self.up(power, timer)

		def clock(self, power=0, timer=0):
			self.down(power, timer)

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

	# Net als bij de base gaat de grijper niet naar boven en beneden en zijn de functies dus hernoemd.
	class Grip(Part):
		def __init__(self, pins, name):
			self.name = name
			super().__init__(pins)

		def close(self, power=0, timer=0):
			self.up(power, timer)

		def open(self, power=0, timer=0):
			self.down(power, timer)

	# Omdat het lampje alleen aan of uit kan in plaats van omhoog en omlaag (en dus ook maar 1 pin in plaats van 2)
	# gebruikt deze alleen een hernoemde versie van up(). down() zet het lampje ook aan. off() staat al in Part().
	class Light(Part):
		def __init__(self, pin, name):
			self.name = name
			super().__init__((pin, pin))

		def on(self, power=0, timer=0):
			self.up(power, timer)

