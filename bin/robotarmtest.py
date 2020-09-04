from roboarm import Arm
import pygame
arm = Arm()
pygame.init()
pygame.display.set_mode()
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_l:
				arm.led.on()
			if event.key == pygame.K_o:
				arm.led.off()
#arm.base.rotate_clock(1)
#arm.shoulder.up(1)
#arm.elbow.down(1)
#arm.wrist.up(1)
#arm.grips.close(1)
#arm.led.on(2)


