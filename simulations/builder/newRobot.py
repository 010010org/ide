from simulation import Simulation
class newRobot():

    def __init__(self):
        self.file = " "
        self.partsList = [['stand', 'rectangle', (0.3,0.5,0.2), (1,1.4,1.8), (0,0,0.4), (0,0.8, 0)]]
        self.name = 'testing'
        self.sim = Simulation(self.name, self.partsList, self.file)
        
    def getSimulation(self):
        self.sim.createPartsList()
        return self.sim