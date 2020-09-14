import pygame, os, sys
from pygame.locals import *


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class Sprite(object):

	def __init__(self, x, y, speed, imageLoc):
		self.x = x
		self.y = y
		self.speed = speed
		self.image = pygame.image.load(imageLoc)

	def update(self):
		self.x+=self.speed[0]
		self.y+=self.speed[1]
		if self.x+self.image.get_width()>SCREEN_WIDTH:
			self.x=SCREEN_WIDTH-self.image.get_width()
			self.speed[0]*=-1
		if self.x<0:
			self.x=0
			self.speed[0]*=-1
		if self.y+self.image.get_height()>SCREEN_HEIGHT:
			self.y=SCREEN_HEIGHT-self.image.get_height()
			self.speed[1]*=-1
		if self.y<0:
			self.y=0
			self.speed[1]*=-1


class Smiley(Sprite):
	def __init__(self, x, y, speed):
		super().__init__(x, y, speed, "img/smiley.bmp")

class Font(object):
	width = 8
	height = 8
	def __init__(self):
		self.image = pygame.image.load("img/font.bmp")

	def drawChar(self, letter, x, y):
		self.char = ord(letter[0])
		self.row = self.char // 32
		self.column = self.char % 32
		print("%d   %d",self.row, self.column)
		self.width = 8
		self.height = 8
		surface.blit(self.image, (x, y), (self.width*self.column, self.height*self.row, self.width, self.height))

	def drawString(self, letters, x, y):
		for i in range(len(letters)):
			self.drawChar(letters[i], x+self.width*i, y)

pygame.init()
fpsClock = pygame.time.Clock()
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.Color(255, 0, 0)
#smiley = Smiley(100, 100, [5, 5])
font = Font()
iter = 0
while True:
	surface.fill(background)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEMOTION:
			mouseX, mouseY = event.pos
	font.drawString('Hello World', 100, 100)
	#surface.blit(smiley.image, (smiley.x, smiley.y))
	#smiley.update()
	pygame.display.update()
	fpsClock.tick(30)
