from abc import abstractstaticmethod


class IsimulationMaker():
    '''simulationMaker interface'''

    @abstractstaticmethod
    def setAmountParts(value):
        '''give list of all part names'''

    @abstractstaticmethod
    def createStand(stand, partsList):
        '''create the stand / platform for the simulation'''

    @abstractstaticmethod
    def createBeam(name, colour, size):
        '''set size and color of rectangle'''

    @abstractstaticmethod
    def createCylinder(name, colour, size):
        '''set size and colour of cylinder'''
    
    @abstractstaticmethod
    def createEllipsoid(name):
        '''set size and name of ellipsoid'''

    @abstractstaticmethod
    def createCone(name):
        '''set size and name of Cone'''

    @abstractstaticmethod
    def setSimulationName(value):
        '''ja toch'''

    def getResult():
        '''return final product'''





