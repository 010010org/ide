from roboarm import Arm
arm = Arm()
arm.base.rotate_clock(1)
arm.shoulder.up(1)
arm.elbow.down(1)
#arm.wrist.up(1)
#arm.grips.close(1)
arm.led.on(2)

