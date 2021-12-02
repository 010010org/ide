from abc import abstractstaticmethod


class IsimulationMaker():
    '''simulationMaker interface'''

    @abstractstaticmethod
    def setAmountParts(value):
        '''give list of all part names'''

    @abstractstaticmethod
    def setRectangle(name, color, size):
        '''set size and color of rectangle'''

    @abstractstaticmethod
    def setName(value):
        '''ja toch'''

    def getResult():
        '''return final product'''





