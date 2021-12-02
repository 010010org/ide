from IsimulationMaker import IsimulationMaker
from simulation import Simulation


class SimulationMaker(IsimulationMaker):
    def __init__(self):
        print(f'init')
        self.simulation = Simulation()
    
    def setAmountParts(self, value):
        self.partsAmount = value
        print(f'amount parts')
        return self
    
    def setRectangle(self, name, color, size):
        print(f'created rectangle')
        return self

    def setName(self, name):
        self.simulation.name = name
        return self
    
    def getResult(self):
        print(f'return simulation')
        return self.simulation

