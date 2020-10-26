import GPIOArm
import pygame
import configparser


class ArmControl(object):
	_arm = GPIOArm.Arm()
	_iniReader = configparser.ConfigParser()
	_iniFile = 'bin/armControls.ini'
	_partArray = []

	def __init__(self):
		self._iniReader.read(self._iniFile)
		for i in self._iniReader:
			if i != "DEFAULT":
				for j in self._iniReader[i]:
					self._partArray.append([i, j, self._iniReader[i][j]])
		pygame.init()
		pygame.display.set_mode()

	# Deze functie is bedoeld om gerunt te worden in de event-loop van een stuk pygame-code.
	# De eerste if kijkt of een van de toetsen ingedrukt is, en stuurt het desbetreffende onderdeel aan als dat zo is.
	# De elif zet een onderdeel uit als de aansturingstoets losgelaten wordt.
	def armInput(self, event):
		if event.type == pygame.QUIT:
			self._arm.close()
			pygame.quit()
		if event.type == pygame.KEYDOWN:
			for i in self._partArray:
				if event.key == getattr(pygame, "K_"+i[2]):
					getattr(getattr(self._arm, i[0]), i[1])()
		elif event.type == pygame.KEYUP:
			for i in self._partArray:
				if event.key == getattr(pygame, "K_"+i[2]):
					getattr(getattr(self._arm, i[0]), "off")()
