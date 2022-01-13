import simpylc as sp

class Simulation():

    def __init__(self, name, List, iniFile):
        self.name = name
        self.receivedList = List
        self.partsAmount = len(self.receivedList)
        self.parts = []
        self.robotOutputIniFile = iniFile
        #creates list of names that can be used to create certain objects
        self.beamNames = ['beam', 'balk', 'rectangle', 'vierkant', 'square']
        self.cylinderNames = ['cylinder', 'barrel']
        self.coneNames = ['cone']
        self.ellipsoidNames = ['ellipsoid']
        self.circleNames = ['circle']
        #create a dictionary that has a list as key and a function as value
        self.functionDict = {
            **dict.fromkeys(self.beamNames, sp.Beam),
            **dict.fromkeys(self.coneNames, sp.Cone),
            **dict.fromkeys(self.ellipsoidNames, sp.Ellipsoid),
            **dict.fromkeys(self.cylinderNames, sp.Cylinder),
            **dict.fromkeys(self.circleNames, sp.Circle)
            }

    def createPartsList(self):
        for i in range(self.partsAmount):
            #strip the receivedlist of all its parts to create the needed objects for the visualisation
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
            except IndexError as e:
                print(f'lijst mist ergens een waarde / Lijst error nog veranderen in LD {e}')
                #shuts down the program so no indexErrors can occur. List is not complete
                exit()
            #creates all the parts
            if partObject.lower() in self.functionDict:
                #calls the value of functiondict and passes all the values to the simpylc object
                self.createPart(self.functionDict[partObject], name, colour, size, center, pivot, joint) 
            else:
                print(f'{partObject} could not be found, please make sure you spelled it correctly or if it exists')#TODO Ld
        return self.parts

    def createPart(self, partName, name, colour, size, center, pivot, joint):
        #add all the parts to a list so it can be passed to visualisation
        part = partName(color  = colour, size = size, center = center, pivot = pivot, joint = joint)
        self.parts.append([name, part])
