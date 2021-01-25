import random
import time
import robotArm
arm = robotArm.Arm()
arm.base.clock()
time.sleep(0.5)
arm.shoulder.down(power=50)
time.sleep(0.5)
arm.base.off()
arm.shoulder.off()
dice = random.randint(1, 6)
if dice == 6:
	arm.light.on()
	time.sleep(1)
	arm.light.off()
else:
	print("rolled", dice)

