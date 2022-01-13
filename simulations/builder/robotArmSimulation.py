from createSimulation import CreateSimulation
class RobotArmSimulation():
    def __init__(self):
        self.outputInifile = "lib/robotArm/robotOutput.ini"
        self.name = "robotArm"
        self.parts =    [['stand',   'cylinder',    (1, 1, 0.2),     (0.5, 0.5, 0.8),   (0, 0, 0.2),      (0, 0, 1)               ],
                        [ 'base',     'beam',      (0.5, 0.5 ,0.5), (0.4, 0.4, 0.6),   (0, 0, 0.5),      (0, 0, 1)                ],
                        ['shoulder', 'ellipsoid', (1, 0.4, 0.4),   (1, 0.2, 0.2),     (0.4, -0.3, 0.1), (0, 1, 0), (-0.4, 0, 0)  ], 
                        [ 'elbow',    'beam',      (1, 0.4, 0.4),   (0.7, 0.15, 0.15), (0.65, 0.175, 0), (0, 1, 0), (-0.25, 0, 0) ],
                        [ 'grip',    'cone',      (1, 0.4, 0.4),   (0.3, 0.1, 0.1),   (0.4, -0.125, 0),  (0, 1, 0),  (-0.05, 0, 0)],
                        ['light',      'beam',      (1,0.1,0.1),     (0.1,0.09,0.09),   (0.15,0,0),        (1,0,0)]]
                        #name, part, colour, size, center , pivot, optional joint, by default 0,0,0

    def createSimulation(self):
        self.simulation = CreateSimulation(self.name, self.outputInifile, self.parts).getSimulation()
        return self.simulation



