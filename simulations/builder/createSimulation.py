from simulation import Simulation

class CreateSimulation():
    def __init__(self, name, outputfile, parts):
        self.name = name
        self.outputIniFile = outputfile
        self.parts = parts
        self.sim = Simulation(self.name, self.parts, self.outputIniFile)

    def getSimulation(self):
        self.sim.createPartsList()
        return self.sim
