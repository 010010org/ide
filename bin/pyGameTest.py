import pygame
import os
import sys
import random
from pygame.locals import *
from pygame import PixelArray

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)


class Sprite(object):

    def __init__(self, x, y, speed, imageLoc):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(imageLoc)

    def update(self):
        self.x += self.speed[0]
        self.y += self.speed[1]
        if self.x + self.image.get_width() > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.image.get_width()
            self.speed[0] *= -1
        if self.x < 0:
            self.x = 0
            self.speed[0] *= -1
        if self.y + self.image.get_height() > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.image.get_height()
            self.speed[1] *= -1
        if self.y < 0:
            self.y = 0
            self.speed[1] *= -1


class Smiley(Sprite):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed, "img/smiley.bmp")


class Font(object):
    width = 8
    height = 8

    def __init__(self, fontName="font"):
        self.image = pygame.image.load("img/" + fontName + ".bmp")
        self.image.set_colorkey(MAGENTA)

    def drawChar(self, letter, x=0, y=0, color=BLACK, fancy=False, bold=False, underline=False):
        char = ord(letter[0])
        row = char // 32
        column = char % 32
        surface.blit(self.image, (x, y), (self.width * column, self.height * row, self.width, self.height))
        if bold:
            surface.blit(self.image, (x + 1, y), (self.width * column, self.height * row, self.width, self.height))
        if underline:
            surface.blit(self.image, (x, y + 1),
                         (self.width * (ord('_') % 32), self.height * (ord('_') // 32), self.width, self.height))
        if fancy:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if color != BLACK:
            pixels = PixelArray(surface)
            pixels.replace(Color(0, 0, 0), color)
            del pixels

    def drawString(self, letters, x=0, y=0, color=BLACK, fancy=False, bold=False, underline=False):
        lineList = letters.splitlines(keepends=False)
        for i in range(len(lineList)):
            for j in range(len(lineList[i])):
                self.drawChar(lineList[i][j], x + (self.width - 1) * j, y + self.height * i, color, fancy, bold,
                              underline)


pygame.init()
fpsClock = pygame.time.Clock()
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.Color(255, 0, 0)
# smiley = Smiley(100, 100, [5, 5])
font = Font()

loremIpsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa
qui officia deserunt mollit anim id est laborum."""

while True:
    surface.fill(background)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouseX, mouseY = event.pos
    font.drawString(loremIpsum, color=WHITE, underline=True)
    # surface.blit(smiley.image, (smiley.x, smiley.y))
    # smiley.update()
    pygame.display.update()
    fpsClock.tick(30)
