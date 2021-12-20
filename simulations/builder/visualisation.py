from time import sleep
import simpylc as sp
import os
import configparser
import copy
from robotArmSimulation import RobotArmSimulation

class Visualisation (sp.Scene):
    def __init__ (self):
        sp.Scene.__init__ (self)
        #make an object from robotarm
        #TODO roep andere sims aan
        #parameter meegeven met aanroepen vanuit ide, + dict hier
        #grote if statement of een dict statement voor de verschillende mogelijkheden
        self.temp = jaToch().getSimulation()
        self.sim = RobotArmSimulation().getSimulation()
        #print(self.temp.print())
        self.test = test()

        #self._receivedPartsList = self.test.partList
        self._receivedPartsList = self.sim.parts
        #self._receivedPartsList = self.temp.parts
        

        #self._stand = self._receivedPartsList[0][1]

        self._robotOutputIniFile = self.sim._robotOutputIniFile
        #"lib/robotArm/robotOutput.ini"
        self._baseWorkingDirectory = os.getcwd()
        self._path = os.path.join(self._baseWorkingDirectory , self._robotOutputIniFile)

        self._parts = []
        self._finalAngles = []
      
        #call function once, otherwise append will create a very long duplicate list
        self.createPartsList()
    
    def createPartsList(self):
        for i in range(len(self._receivedPartsList)):
            name = self._receivedPartsList[i][0]
            #create empty list with the names of all the parts
            self._parts.append([name, 45])
        #use deepcopy so original list is copied instead of a pointer to original object
        self._finalAngles = copy.deepcopy(self._parts)
          
    def updateFinalAngleList(self):
        if os.path.exists(self._path):
            config = configparser.ConfigParser()
            config.read(self._path)
            for i in range(len(self._parts)):
            #loop through dict of parts searching for the name of the part in the ini file and adding the degree of that part into the dict
                partName =  self._parts[i][0]
                #sometimes the program cannot handle all the input and throughs an keyError
                try:
                    self._finalAngles[i][1] = int(config[partName]['DEGREES'])
                except KeyError as k:
                    print(f'er is iets fout gegaan: {k}')
        else:   
            print(f'{self._path} bestaat niet')
    
    def updateCurrentAngles(self):
        for i in range(len(self._parts)):
            finalAngle = self._finalAngles[i][1]
            currentAngle = self._parts[i][1]
            angledifference = finalAngle - currentAngle
            #print(f'{self._parts[0][0]}: finalangle: {finalAngle}. currentangle: {currentAngle}. angledifference: {angledifference}')
            if angledifference > 0:
                self._parts[i][1] += 1           
            elif angledifference < 0:
                self._parts[i][1] -= 1

    #basically the main, everything in this function happens every few milliseconds
    def display (self):
        self._receivedPartsList[0][1](parts = self.createNextPart(0))   


    def createNextPart(self, i):
        #checks for last part, see documentation why lambda:
        if i != len(self._receivedPartsList)-1:
            return lambda :self._receivedPartsList[i][1](rotation = self._parts[i][1], parts = self.createNextPart(i+1))
        else:
            return lambda: self._receivedPartsList[i][1](rotation = self._parts[i][1])

                           

#ja toch
from simulation import Simulation
class jaToch():
    def __init__(self):
        self.name = "ja toch"

        self.partList =[['stand',   'cylinder',    (1, 1, 0.2),     (0.5, 0.5, 0.8),   (0, 0, 0.2),      (0, 0, 1)                    ],
                    [ 'base',     'beam',      (0.5, 0.5, 0.5), (0.4, 0.4, 0.6),   (0, 0, 0.5),      (0, 0, 1)                ],
                    [ 'shoulder', 'ellipsoid', (1, 0.4, 0.4),   (1, 0.2, 0.2),     (0.4, -0.3, 0.1), (0, 1, 0), (-0.4, 0, 0)  ], 
                    [ 'elbow',    'beam',      (1, 0.4, 0.4),   (0.7, 0.15, 0.15), (0.65, 0.175, 0), (0, 1, 0), (-0.25, 0, 0) ],
                    [ 'wrist',    'cone',      (1, 0.4, 0.4),   (0.3, 0.1, 0.1),   (0.4, -0.125, 0),  (0, 1, 0),  (-0.05, 0, 0)]]
        self.file = " "

        self.sim =Simulation(self.name, self.partList, self.file)
    
    def getSimulation(self):
        self.sim.createPartsList()
        return self.sim

        
        # self.handSide0 = sp.Beam (size = handSideSize, center = (0, -0.075, -0.075), color = handColor)
        # self.handSide1 = sp.Beam (size = handSideSize, center = (0, 0.075, -0.075), color = handColor)
        # self.handSide2 = sp.Beam (size = handSideSize, center = (0, 0.075, 0.075), color = handColor)
        # self.handSide3 = sp.Beam (size = handSideSize, center = (0, -0.075, 0.075), color = handColor)
class test():
    def __init__(self): 
        self.stand = sp.Cylinder (size = (0.5, 0.5, 0.8), center = (0, 0, 0.2), pivot = (0, 0, 1), color = (1, 1, 0.2), joint = (0,0,0))
        self.base = sp.Beam (size = (0.4, 0.4, 0.6), center = (0, 0, 0.5), pivot = (0, 0, 1), color = (0.5, 0.5, 0.5),joint = (0,0,0))

        armColor = (1, 0.4, 0.4)
        self.shoulder = sp.Ellipsoid (size = (1, 0.2, 0.2), center = (0.4, -0.3, 0.1), joint = (-0.4, 0, 0), pivot = (0, 1, 0), color = armColor)
        self.elbow = sp.Beam (size = (0.7, 0.15, 0.15), center = (0.65, 0.175, 0), joint = (-0.25, 0, 0), pivot = (0, 1, 0), color = armColor)
        self.wrist = sp.Cone (size = (0.3, 0.1, 0.1), center = (0.40, -0.125, 0), joint = (-0.05, 0, 0), pivot = (0, 1, 0), color = armColor)
        
        handColor = (1, 0.01, 0.01)
        handSideSize = (0.1, 0.1, 0.1)
        self.handCenter = sp.Beam (size = (0.1, 0.09, 0.09), center = (0.15, 0, 0), pivot = (1, 0, 0), color = handColor, joint = (0,0,0))   
        self.partList = [['stand',self.stand],['base', self.base],['shoulder', self.shoulder], ['elbow',self.elbow], ['wrist', self.wrist], ['hand' , self.handCenter]]
    
'''

, parts = lambda:
    self.handSide0 () +
    self.handSide1 () +
    self.handSide2 () +
    self.handSide3 () +
    self.finger0 (rotation = sp.world.robot.finAng) +
    self.finger1 (rotation = sp.world.robot.finAng) +
    self.finger2 (rotation = sp.world.robot.finAng) +
    self.finger3 (rotation = sp.world.robot.finAng)
    '''


sp.World(Visualisation)
#simulation = RobotArmSimulation().getSimulation()
#print(simulation._parts)
