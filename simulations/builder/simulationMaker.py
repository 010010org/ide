from IsimulationMaker import IsimulationMaker
from simulation import Simulation


class SimulationMaker(IsimulationMaker):
    def __init__(self):
        self.simulation = Simulation()
        self.beamNames = ['beam', 'balk', 'rectangle', 'vierkant', 'square']
        self.cylinderNames = ['cylinder', 'barrel']
        self.coneNames = ['cone']
        self.ellipsoidNames = ['ellipsoid']
        self.functionDict = {
            **dict.fromkeys(self.beamNames, self.createBeam),
            **dict.fromkeys(self.coneNames, self.createCone),
            **dict.fromkeys(self.ellipsoidNames, self.createEllipsoid),
            **dict.fromkeys(self.cylinderNames, self.createCylinder)
            }
    
    
    def createStand(self, stand, partsList):
        self.simulation.parts= partsList
        self.simulation.stand = stand
        self.receivedParts = partsList
        self.simulation.partsAmount = len(partsList)
        
        
        for i in range(self.simulation.partsAmount):
            try:
                name = self.receivedParts[i][0]
                partObject = self.receivedParts[i][1]
                colour = self.receivedParts[i][2]
                size = self.receivedParts[i][3]
                center = self.receivedParts[i][4]
                #check for error
                #temp = self.simulation.parts[i][6]
                #print(temp)
            except IndexError as e:
                print(f'Lijst error nog veranderen in LD {e}')
                #shuts down the program so no indexErrors can occur. List is not complete
                exit()
            #creates all the parts
            if partObject.lower() in self.functionDict:
                self.functionDict[partObject](name, colour, size) 
            else:
                print(f'{partObject} could not be found, please make sure you spelled it correctly or if it exists')
        return self

    #parts builder implementeren


    def setSimulationName(self, name):
        self.simulation.simulationName = name
        return self

    
    def getResult(self):
        return self.simulation

