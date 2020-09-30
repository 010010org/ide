from bin.GPIOArm import Arm
import pygame
# code om deze library direct te testen. Wordt niet uitgevoegd als de library geimporteerd wordt.
arm = Arm()
pygame.init()
pygame.display.set_mode()


# Dit is een vrij lelijk stuk code om herhaald schrijfwerk te voorkomen.
# De eerste regel kijkt of de ingevulde letter degene is die is ingedrukt.
# Als key bijvoorbeeld 'a' is wordt de regel vertaald naar "if event.key == pygame.K_a:".
# De tweede regel zoekt eerst het genoemde onderdeel van de robot op en daarna de genoemde beweegrichting.
# voor part = "base" en state = "counter" wordt deze regel vertaald naar "arm.base.counter()".
def _ArmControl(event, key, part, state):
	if event.key == getattr(pygame, "K_"+key):
		getattr(getattr(arm, part), state)()


# Deze functie is bedoeld om gerunt te worden in de event-loop van een stuk pygame-code.
# De eerste if kijkt of een van de toetsen ingedrukt is, en stuurt het desbetreffende onderdeel aan als dat zo is.
# De elif zet een onderdeel uit als de aansturingstoets losgelaten wordt.
def ArmInput(event):
	if event.type == pygame.QUIT:
		arm.close()
		pygame.quit()
	if event.type == pygame.KEYDOWN:
		_ArmControl(event, "a", "base", "counter")
		_ArmControl(event, "d", "base", "clock")
		_ArmControl(event, "w", "shoulder", "up")
		_ArmControl(event, "s", "shoulder", "down")
		_ArmControl(event, "r", "elbow", "up")
		_ArmControl(event, "f", "elbow", "down")
		_ArmControl(event, "t", "wrist", "up")
		_ArmControl(event, "g", "wrist", "down")
		_ArmControl(event, "y", "grip", "close")
		_ArmControl(event, "h", "grip", "open")
		_ArmControl(event, "u", "light", "on")
	elif event.type == pygame.KEYUP:
		_ArmControl(event, "a", "base", "off")
		_ArmControl(event, "d", "base", "off")
		_ArmControl(event, "w", "shoulder", "off")
		_ArmControl(event, "s", "shoulder", "off")
		_ArmControl(event, "r", "elbow", "off")
		_ArmControl(event, "f", "elbow", "off")
		_ArmControl(event, "t", "wrist", "off")
		_ArmControl(event, "g", "wrist", "off")
		_ArmControl(event, "y", "grip", "off")
		_ArmControl(event, "h", "grip", "off")
		_ArmControl(event, "u", "light", "off")
