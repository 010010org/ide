from simulation import Simulation

class CreateSimulation():
    def __init__(self):
        self.outputIniFile = "lib/robotArm/robotOutput.ini"
        # order is    name,     kind of part,     colour,            size,            center       pivot
        self.parts =[['stand',   'cylinder',    (1, 1, 0.2),     (0.5, 0.5, 0.8),   (0, 0, 0.2),      (0, 0, 1)               ],
                    [ 'base',     'beam',      (0.5, 0.5 ,0.5), (0.4, 0.4, 0.6),   (0, 0, 0.5),      (0, 0, 1)                ],
                    [ 'shoulder', 'ellipsoid', (1, 0.4, 0.4),   (1, 0.2, 0.2),     (0.4, -0.3, 0.1), (0, 1, 0), (-0.4, 0, 0)  ], 
                    [ 'elbow',    'beam',      (1, 0.4, 0.4),   (0.7, 0.15, 0.15), (0.65, 0.175, 0), (0, 1, 0), (-0.25, 0, 0) ],
                    [ 'wrist',    'cone',      (1, 0.4, 0.4),   (0.3, 0.1, 0.1),   (0.4, -0.125, 0),  (0, 1, 0),  (-0.05, 0, 0)],
                    ['hand',      'beam',      (1,0.1,0.1),     (0.1,0.09,0.09),   (0.15,0,0),        (1,0,0)]]


        self.sim = Simulation('test', self.parts, self.outputIniFile)

    def getSimulation(self):
        self.sim.createPartsList()
        return self.sim





#sim = RobotArmSimulation()
#sim.getSimulation()







#simulation = RobotArmSimulation.construct('test' , stand, parts)
#TODO hoe gaat de ide de simulatie aanroepen met de goede settings?, getter
#print alles wat hij heeft
#print(simulation.construction())

#sim = Simulation('test', parts)
#print(sim.createOrder())
#sim.print()

#def getSimulation():
#    return simulation

#sim = getSimulation()
#print(sim.construction())
            
