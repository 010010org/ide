import simpylc as sp
import os
import configparser
import copy
from createSimulation import CreateSimulation

#call from robotarm gives inifile, debugmode etc

class Visualisation (sp.Scene):
    def __init__ (self):
        sp.Scene.__init__ (self)
        #make an object from robotarm
        #TODO roep andere sims aan
        #parameter meegeven met aanroepen vanuit ide, + dict hier
        #grote if statement of een dict statement voor de verschillende mogelijkheden
        self.sim = CreateSimulation().getSimulation()
        self._receivedPartsList = self.sim.parts
        self._robotOutputIniFile = self.sim._robotOutputIniFile
        #"lib/robotArm/robotOutput.ini"
        self._baseWorkingDirectory = os.getcwd()
        self._path = os.path.join(self._baseWorkingDirectory , self._robotOutputIniFile)

        self._parts = []
        self._finalAngles = []
      
        #call function once, otherwise append will create a very long duplicate list
        self.createPartsList()

    def configureIniFile(self):
        iniWriter = configparser.ConfigParser(strict = False)
        iniWriter.optionxform = str
        iniWriter.read(self._robotOutputIniFile)
        for i in range(self._parts):
            iniWriter[self.parts[i][0]]
        pass

    def createPartsList(self):
        #creates the list for the angles so the simulation can move, also updates the ini file for all the parts it has
        if os.path.exists(self._robotOutputIniFile):
            config = configparser.ConfigParser(strict = False, )
            config.optionxform = str
            config.read(self._robotOutputIniFile)
            for i in range(len(self._receivedPartsList)):
                name = self._receivedPartsList[i][0]
                #create empty list with the names of all the parts
                self._parts.append([name, 0])
                #looks if the part already exists, if so resets the degrees to 0. if it doesn't exist creates the part with 0 degrees
                try:
                    config[name]["DEGREES"] = '0'
                except (KeyError, configparser.NoSectionError) as e:
                    config[name] = {"DEGREES": '0'}
                
            #use deepcopy so original list is copied instead of a pointer to original object
            self._finalAngles = copy.deepcopy(self._parts)
            with open(self._robotOutputIniFile, "w") as configFile:
                config.write(configFile, space_around_delimiters=False)
            
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
                    #waiting does not resolve error 
                    print(f'er is iets fout gegaan: {k} maar dat maakt niet uit')
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

    def createNextPart(self, i):
        #checks for last part, see documentation why lambda:
        if i != len(self._receivedPartsList)-1:
            return lambda :self._receivedPartsList[i][1](rotation = self._parts[i][1], parts = self.createNextPart(i+1))
        else:
            return lambda: self._receivedPartsList[i][1](rotation = self._parts[i][1])

    #basically the main, everything in this function happens every few milliseconds
    def display (self):
        self.updateCurrentAngles()
        self.updateFinalAngleList()
        self._receivedPartsList[0][1](parts = self.createNextPart(1))
               
sp.World(Visualisation)

