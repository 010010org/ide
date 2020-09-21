from roboarm import Arm
import mcpi.minecraft as minecraft
import mcpi.block as block
import time


class Poss(object):
	x = 0
	y = 0
	z = 0
	
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z


mc = minecraft.Minecraft.create()
arm = Arm()

BaseLPos = Poss(-3, -1, -50)
BaseRPos = Poss(-5, -1, -50)


def checkHit():
	events = mc.events.pollBlockHits()
	for e in events:
		pos = e.pos
		print(pos)
		if pos.x == BaseLPos.x and pos.y == BaseLPos.y and pos.z == BaseLPos.z:
			arm.base.rotate_counter(1)
		if pos.x == BaseRPos.x and pos.y == BaseRPos.y and pos.z == BaseRPos.z:
			arm.base.rotate_clock(1)


while True:
	time.sleep(1)
	checkHit()	
