from simulationMaker import SimulationMaker

class RobotArmSimulation:
    @staticmethod
    def construct():
        return SimulationMaker()\
            .setName("hahahaha")\
            .getResult()
        
sim = RobotArmSimulation.construct()
print(sim.construction())
            
