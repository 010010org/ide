from createSimulation import CreateSimulation

class Snake():
    def __init__(self):
        self.name = "car"
        self.outputIniFile = "lib/snake/robotOutput.ini"
        self.parts = [['head',   'cylinder',    (0.7, 1, 0.2),     (0.2, 0.2, 0.2),   (0, 0, 0.1),      (0, 0, 1)               ],
                    [ 'body1',     'beam',      (0.7, 0.5 ,0.5), (0.1, 0.1, 0.2),   (0, 0, 0.2),      (0, 1, 1)                ],
                    [ 'body2',     'beam',      (0.5, 0.7 ,0.5), (0.1, 0.1, 0.2),   (0, 0, 0.2),      (1, 0, 1)                ],
                    [ 'body3',     'beam',      (0.5, 0.5 ,0.7), (0.1, 0.1, 0.2),   (0, 0, 0.2),      (1, 1, 1)                ],
                    [ 'body4',     'beam',      (0.5, 0.7 ,0.5), (0.1, 0.1, 0.2),   (0, 0, 0.2),      (0, 0, 1)                ],
                    [ 'body5',     'beam',      (0.7, 0.5 ,0.5), (0.1, 0.1, 0.2),   (0, 0, 0.2),      (1, 0, 0)                ],
                    [ 'body6',     'beam',      (0.5, 0.7 ,0.5), (0.1, 0.1, 0.2),   (0, 0, 0.2),      (0, 1, 0)                ],
                    [ 'body7',     'beam',      (0.5, 0.5 ,0.7), (0.1, 0.1, 0.2),   (0, 0, 0.2),      (0, 0, 1)                ],
                    [ 'tail',     'cylinder',      (0.5, 0.7 ,0.5), (0.1, 0.1, 0.2),   (0, 0, 0.2),      (0, 0, 1)                ]]
        
        
    def createSimulation(self):
        self.simulation = CreateSimulation(self.name, self.outputIniFile, self.parts).getSimulation()
        return self.simulation