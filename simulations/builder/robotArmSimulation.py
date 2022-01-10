import visualisation as vs
import simpylc as sp
import createSimulation

outputfile = " "
debugmode = 0
name = "robotArm"
partsList = [['stand',   'cylinder',    (1, 1, 0.2),     (0.5, 0.5, 0.8),   (0, 0, 0.2),      (0, 0, 1)               ],
            [ 'base',     'beam',      (0.5, 0.5 ,0.5), (0.4, 0.4, 0.6),   (0, 0, 0.5),      (0, 0, 1)                ],
            [ 'shoulder', 'ellipsoid', (1, 0.4, 0.4),   (1, 0.2, 0.2),     (0.4, -0.3, 0.1), (0, 1, 0), (-0.4, 0, 0)  ], 
            [ 'elbow',    'beam',      (1, 0.4, 0.4),   (0.7, 0.15, 0.15), (0.65, 0.175, 0), (0, 1, 0), (-0.25, 0, 0) ],
            [ 'grip',    'cone',      (1, 0.4, 0.4),   (0.3, 0.1, 0.1),   (0.4, -0.125, 0),  (0, 1, 0),  (-0.05, 0, 0)],
            ['light',      'beam',      (1,0.1,0.1),     (0.1,0.09,0.09),   (0.15,0,0),        (1,0,0)]]

simulation = createSimulation(outputfile, debugmode, name, partsList)


