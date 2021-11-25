
import os
#alleen register gebruiken anders private variabelen, dus _name. wordt op gechecked in simpylc
class Waardes():

        #TODO make it compatible with debugmode, debugmode shows control page
    def __init__(self):
        self._robotOutputiniFile = "lib/robotArm/robotOutput.ini"
        self._baseWorkingDirectory = os.path.dirname(os.path.dirname(os.getcwd()))
        self._iniPath = os.path.join(self._baseWorkingDirectory , self._robotOutputiniFile)

        #base
        self._baseAngle = 0
        self._clockwise = 1 

        #shoulder
        self._shoulderAngle = 0

        #wrist
        self._wristAngle = 0

        #elbow
        self._elbowAngle = 0

        #grip
        self._closedGrip = 0
        self._gripAngle = 0

        #light
        self._light = 0

        #start
        self._start = 1
    
    
    def input(self):
        #hier kan de communicatie komen vanuit robot_output.txt
        '''
        self.baseAngle.set(sp.world.robot.baseAngle)
        self.shoulderAngle.set(sp.world.robot.shoulderAngle)
        self.elbowAngle.set(sp.world.robot.elbowAngle)
        self.wristAngle.set(sp.world.robot.wristAngle)
        self.gripAngle.set(sp.world.robot.gripAngle)
        '''
    def getBaseAngle(self):
        Angle = self._baseAngle
        return Angle
    

    def sweep(self):
        #base
        self._baseAngle.set(self._baseAngle)

        #shoulder
        self._shoulderAngle.set(self._shoulderAngle)
        
        #elbow
        self._elbowAngle.set(self._elbowAngle)

        #wrist
        self._gripAngle.set(self._gripAngle)

        #grip
        self._gripAngle.set(self._gripAngle)
        self._closedGrip.set(self._closedGrip)

        #light
        self._light.set(self._light)


