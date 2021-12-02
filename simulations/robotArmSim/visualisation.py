from logging import error
from time import sleep
import simpylc as sp
import os
import configparser
import copy

class Visualisation (sp.Scene):
    def __init__ (self):
        sp.Scene.__init__ (self)
        self._robotOutputIniFile = "lib/robotArm/robotOutput.ini"
        self._baseWorkingDirectory = os.getcwd()
        self._path = os.path.join(self._baseWorkingDirectory , self._robotOutputIniFile)

        self._parts = [["base", 0], ["shoulder", 0], ["elbow", 0], ["wrist", 0],]
        self._finalAngles = copy.deepcopy(self._parts)

        self.stand = sp.Cylinder (size = (0.3, 0.3, 0.4), center = (0, 0, 0.2), pivot = (0, 0, 1), color = (1, 1, 0.2))
        self.base = sp.Beam (size = (0.4, 0.4, 0.6), center = (0, 0, 0.5), pivot = (0, 0, 1), color = (0.5, 0.5, 0.5))
        
        armColor = (1, 0.4, 0.4)
        self.shoulder = sp.Beam (size = (1, 0.2, 0.2), center = (0.4, -0.3, 0.1), joint = (-0.4, 0, 0), pivot = (0, 1, 0), color = armColor)
        self.elbow = sp.Beam (size = (0.7, 0.15, 0.15), center = (0.65, 0.175, 0), joint = (-0.25, 0, 0), pivot = (0, 1, 0), color = armColor)
        self.wrist = sp.Beam (size = (0.3, 0.1, 0.1), center = (0.40, -0.125, 0), joint = (-0.05, 0, 0), pivot = (0, 1, 0), color = armColor)
        
        handColor = (1, 0.01, 0.01)
        handSideSize = (0.1, 0.1, 0.1)
        self.handCenter = sp.Beam (size = (0.1, 0.09, 0.09), center = (0.15, 0, 0), pivot = (1, 0, 0), color = handColor)
        self.handSide0 = sp.Beam (size = handSideSize, center = (0, -0.075, -0.075), color = handColor)
        self.handSide1 = sp.Beam (size = handSideSize, center = (0, 0.075, -0.075), color = handColor)
        self.handSide2 = sp.Beam (size = handSideSize, center = (0, 0.075, 0.075), color = handColor)
        self.handSide3 = sp.Beam (size = handSideSize, center = (0, -0.075, 0.075), color = handColor)
        
        fingerColor = (0.01, 1, 0.01)
        fingerSize = (0.3, 0.05, 0.05)
        fingerJoint = (-0.125, 0, 0)
        self.finger0 = sp.Beam (size = fingerSize, center = (0.15, 0, -0.1), joint = fingerJoint, pivot = (0, -1, 0), color = fingerColor)
        self.finger1 = sp.Beam (size = fingerSize, center = (0.15, 0, 0.1), joint = fingerJoint, pivot = (0, 1, 0), color = fingerColor)
        self.finger2 = sp.Beam (size = fingerSize, center = (0.15, -0.1, 0), joint = fingerJoint, pivot = (0, 0, 1), color = fingerColor)
        self.finger3 = sp.Beam (size = fingerSize, center = (0.15, 0.1, 0), joint = fingerJoint, pivot = (0, 0, -1), color = fingerColor)
    
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
            #TODO keypress toevoegen aan ini zodat je weet of het een grote of kleine bewerking is
            #TODO gaat nu van 350 - 8 de andere kant op met modulo 360
            #Maandag meeting brainstorm
            if angledifference > 0:
                self._parts[i][1] += 1           
            elif angledifference < 0:
                self._parts[i][1] -= 1


    def display (self):
        #print(f'{self._parts}')
        self.updateFinalAngleList()
        self.updateCurrentAngles()
        self.stand (parts = lambda:
        #for loop met [i]
            self.base (rotation = self._parts[0][1], parts = lambda:
                self.shoulder (rotation = self._parts[1][1], parts = lambda:
                    self.elbow (rotation = self._parts[2][1], parts = lambda:
                        self.wrist (rotation = self._parts[3][1], parts = lambda:
                            self.handCenter (rotation = self._parts[3][1]))))))
                    
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
        
