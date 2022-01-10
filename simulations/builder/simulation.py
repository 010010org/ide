import simpylc as sp

class Simulation():

    def __init__(self, name, List, iniFile):
        self.name = name
        self.receivedList = List
        self.partsAmount = len(self.receivedList)
        self.parts = []
        self._robotOutputIniFile = iniFile

        self.beamNames = ['beam', 'balk', 'rectangle', 'vierkant', 'square']
        self.cylinderNames = ['cylinder', 'barrel']
        self.coneNames = ['cone']
        self.ellipsoidNames = ['ellipsoid']
        self.functionDict = {
            **dict.fromkeys(self.beamNames, sp.Beam),
            **dict.fromkeys(self.coneNames, sp.Cone),
            **dict.fromkeys(self.ellipsoidNames, sp.Ellipsoid),
            **dict.fromkeys(self.cylinderNames, sp.Cylinder)
            }

    def createPartsList(self):
        for i in range(self.partsAmount):
            try:
                name = self.receivedList[i][0]
                partObject = self.receivedList[i][1]
                colour = self.receivedList[i][2]
                size = self.receivedList[i][3]
                center = self.receivedList[i][4]
                pivot = self.receivedList[i][5]
                #check last
                if len(self.receivedList[i]) == 7:
                    joint = self.receivedList[i][6]
                else:
                    joint = (0,0,0)
                #check for error
                #temp = self.simulation.parts[i][6]
                #print(temp)
            except IndexError as e:
                print(f'Lijst error nog veranderen in LD {e}')
                #shuts down the program so no indexErrors can occur. List is not complete
                exit()
            #creates all the parts
            if partObject.lower() in self.functionDict:
                #calls the value of functiondict and passes all the values to the simpylc object
                self.createPart(self.functionDict[partObject], name, colour, size, center, pivot, joint) 
            else:
                print(f'{partObject} could not be found, please make sure you spelled it correctly or if it exists')#TODO Ld
        #print(self._parts)
        return self.parts

    def createPart(self, partName, name, colour, size, center, pivot, joint):
        part = partName(color  = colour, size = size, center = center, pivot = pivot, joint = joint)
        self.parts.append([name, part])
    
    def print(self):
        print(f'Hello, my name is {self.name}\nI have {self.partsAmount} parts\nmy part list looks like this: {self.parts}')
