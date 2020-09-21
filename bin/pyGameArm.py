from GPIOArm import Arm
import pygame
#code om deze library direct te testen. Wordt niet uitgevoegd als de library geimporteerd wordt.
arm = Arm()
pygame.init()
pygame.display.set_mode()

#Dit is een vrij lelijk stuk code om herhaald schrijfwerk te voorkomen.
#De eerste regel kijkt of de ingevulde letter degene is die is ingedrukt.
#Als key bijvoorbeeld 'a' is wordt de regel vertaald naar "if event.key == pygame.K_a:".
#De tweede regel zoekt eerst het genoemde onderdeel van de robot op en daarna de genoemde beweegrichting.
#voor part = "base" en state = "counter" wordt deze regel vertaald naar "arm.base.counter()".
def _ArmControl(key, part, state):
	if event.key == getattr(pygame, "K_"+key):
		getattr(getattr(arm, part), state)()

#Deze functie is bedoeld om gerunt te worden in de event-loop van een stuk pygame-code.
#De eerste if kijkt of een van de toetsen ingedrukt is, en stuurt het desbetreffende onderdeel aan als dat zo is.
#De elif zet een onderdeel uit als de aansturingstoets losgelaten wordt.
def ArmInput(event):
	if event.type == pygame.KEYDOWN:
		_ArmControl("a", "base", "counter")
		_ArmControl("d", "base", "clock")
		_ArmControl("w", "shoulder", "up")
		_ArmControl("s", "shoulder", "down")
		_ArmControl("r", "elbow", "up")
		_ArmControl("f", "elbow", "down")
		_ArmControl("t", "wrist", "up")
		_ArmControl("g", "wrist", "down")
		_ArmControl("y", "grip", "close")
		_ArmControl("h", "grip", "open")
		_ArmControl("u", "light", "on")
	elif event.type == pygame.KEYUP:
		_ArmControl("a", "base", "off")
		_ArmControl("d", "base", "off")
		_ArmControl("w", "shoulder", "off")
		_ArmControl("s", "shoulder", "off")
		_ArmControl("r", "elbow", "off")
		_ArmControl("f", "elbow", "off")
		_ArmControl("t", "wrist", "off")
		_ArmControl("g", "wrist", "off")
		_ArmControl("y", "grip", "off")
		_ArmControl("h", "grip", "off")
		_ArmControl("u", "light", "off")
