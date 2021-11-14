import simpylc as sp
#alleen register gebruiken anders private variabelen, dus _name. wordt op gechecked in simpylc
class Control(sp.Module):
    def __init__(self):
        sp.Module.__init__(self)

        self.page('movement')

        self.group('base', True)
        
        self.baseAngle = sp.Register()
        
        self._clockwise = 1 #communicatie optie met ide
        
        self.group('start')
        self.start = sp.Marker(1)

        self.group('shoulder', True)
        self.shoulderAngle = sp.Register(0)

        self.group('wrist')
        self.wristAngle = sp.Register(0)

        self.group('elbow')
        self.elbowAngle = sp.Register(0)

        self.group('grip', True)
        self.closedGrip = sp.Register(0)
        self.gripAngle = sp.Register(0)

        self.group('light')
        self.light = sp.Register(0)
    
    
    def input(self):
        #hie kan de communicatie komen vanuit robot_output.txt
        self.part('angles')
        '''
        self.baseAngle.set(sp.world.robot.baseAngle)
        self.shoulderAngle.set(sp.world.robot.shoulderAngle)
        self.elbowAngle.set(sp.world.robot.elbowAngle)
        self.wristAngle.set(sp.world.robot.wristAngle)
        self.gripAngle.set(sp.world.robot.gripAngle)
        '''

    def sweep(self):
        self.part('base')
        self.baseAngle.set(self.baseAngle)

        self.part('shoulder')
        self.shoulderAngle.set(self.shoulderAngle)
        
        self.part('elbow')
        self.elbowAngle.set(self.elbowAngle)

        self.part('wrist')
        self.gripAngle.set(self.gripAngle)

        self.part('grip')
        self.gripAngle.set(self.gripAngle)
        self.closedGrip.set(self.closedGrip)

        self.part('light')
        self.light.set(self.light)


