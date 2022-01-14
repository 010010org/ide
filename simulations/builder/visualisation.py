import simpylc as sp
import os
import configparser
import copy
import sys
from visualisationLoader import VisualisationLoader

#check for raspbery pi, raspberry pi 400 and laptop have different versions of python installed
if os.path.exists("/sys/firmware/devicetree/base/model"):
    with open("/sys/firmware/devicetree/base/model") as file:
        if "Raspberry Pi" in file.read():
            #!/usr/bin/python3.7
            pass

#call from robotarm gives inifile, debugmode etc

class Visualisation (sp.Scene):
    def __init__ (self):
        sp.Scene.__init__ (self)
        #grab the library and get corresponding object
        #library is given as an extra variabel in the command line
        self.library = sys.argv[1]
        self.sim = VisualisationLoader(self.library).getSimulation()
        #grab the relevant variables
        self.receivedPartsList = self.sim.parts
        self.robotOutputIniFile = self.sim.robotOutputIniFile
        self.baseWorkingDirectory = os.getcwd()
        #create the path to the correct ini file
        self.path = os.path.join(self.baseWorkingDirectory , self.robotOutputIniFile)
        #create lists that will contain the information needed to update the visuals
        self.parts = []
        self.finalAngles = []
      
        #call function once, otherwise append will create a very long duplicate list
        self.createPartsList()

    def _configureIniFile(self):
        iniWriter = configparser.ConfigParser(strict = False)
        iniWriter.optionxform = str
        iniWriter.read(self.robotOutputIniFile)
        for i in range(self.parts):
            iniWriter[self.parts[i][0]]
        pass

    def createPartsList(self):
        #creates the list for the angles so the simulation can move, also updates the ini file for all the parts it has
        if os.path.exists(self.robotOutputIniFile):
            config = configparser.ConfigParser(strict = False, )
            config.optionxform = str
            config.read(self.robotOutputIniFile)
            for i in range(len(self.receivedPartsList)):
                name = self.receivedPartsList[i][0]
                #create empty list with the names of all the parts
                self.parts.append([name, 0])
                #looks if the part already exists, if so resets the degrees to 0. if it doesn't exist creates the part with 0 degrees
                try:
                    config[name]["DEGREES"] = '0'
                except (KeyError, configparser.NoSectionError) as e:
                    config[name] = {"DEGREES": '0'}
                
            #use deepcopy so original list is copied instead of a pointer to original object
            self.finalAngles = copy.deepcopy(self.parts)
            with open(self.robotOutputIniFile, "w") as configFile:
                config.write(configFile, space_around_delimiters=False)
            
    def updateFinalAngleList(self):
        if os.path.exists(self.path):
            config = configparser.ConfigParser()
            config.read(self.path)
            for i in range(len(self.parts)):
            #loop through dict of parts searching for the name of the part in the ini file and adding the degree of that part into the dict
                partName =  self.parts[i][0]
                #sometimes the program cannot handle all the input and throughs an keyError
                try:
                    self.finalAngles[i][1] = int(config[partName]['DEGREES'])
                except KeyError as k:
                    #both simpylc and ide want to access ini file at the same time
                    #waiting for a short amoun of time does not resolve error 
                    pass 
                    print(f'er is iets fout gegaan: {k} maar dat maakt niet uit')
        else:   
            print(f'{self.path} bestaat niet')
    
    def updateCurrentAngles(self):
        #function that checks if the part is on its destination point, else moves that part closer
        for i in range(len(self.parts)):
            finalAngle = self.finalAngles[i][1]
            currentAngle = self.parts[i][1]
            angledifference = finalAngle - currentAngle
            if angledifference > 0:
                self.parts[i][1] += 1           
            elif angledifference < 0:
                self.parts[i][1] -= 1

    def createNextPart(self, i):
        #checks for last part, lambda needed because of simpylc. TODO documentation for more information
        if i != len(self.receivedPartsList)-1:
            return lambda :self.receivedPartsList[i][1](rotation = self.parts[i][1], parts = self.createNextPart(i+1))
        else:
            return lambda: self.receivedPartsList[i][1](rotation = self.parts[i][1])

    #basically the main, everything in this function happens every few milliseconds
    def display (self):
        self.updateFinalAngleList()
        self.updateCurrentAngles()
        self.receivedPartsList[0][1](parts = self.createNextPart(1))

#actually activates the code            
sp.World(Visualisation)

