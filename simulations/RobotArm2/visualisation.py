import simpylc as sp

class Visualisation (sp.Scene):
    def __init__ (self):
        sp.Scene.__init__ (self)
        self.stand = sp.Cylinder (size = (0.3, 0.3, 0.4), center = (0, 0, 0.2), pivot = (0, 0, 1), color = (1, 1, 0.2))
        self.base = sp.Beam (size = (0.4, 0.4, 0.6), center = (0, 0, 0.5), pivot = (0, 0, 1), color = (0.5, 0.5, 0.5))
        
        armColor = (0.9, 0.6, 0.9)
        self.shoulder = sp.Beam (size = (1, 0.2, 0.2), center = (0.4, -0.3, 0.1), joint = (-0.4, 0, 0), pivot = (0, 1, 0), color = armColor)
        self.elbow = sp.Beam (size = (0.7, 0.15, 0.15), center = (0.65, 0.175, 0), joint = (-0.25, 0, 0), pivot = (0, 1, 0), color = armColor)
        self.wrist = sp.Beam (size = (0.3, 0.1, 0.1), center = (0.40, -0.125, 0), joint = (-0.05, 0, 0), pivot = (0, 1, 0), color = armColor)
        
        handColor = (1, 0.01, 0.01)
        handSideSize = (0.1, 0.1, 0.1)
        self.handCenter = sp.Beam (size = (0.1, 0.09, 0.09), center = (0.15, 0, 0), pivot = (1, 0, 0), color = handColor)
        self.handSide0 = sp.Beam (size = handSideSize, center = (0, -0.075, -0.075), color = handColor)
        self.handSide1 = sp.Beam (size = handSideSize, center = (0, 0.075, -0.075), color = handColor)
        self.handSide2 = sp.Beam (size = handSideSize, center = (0, 0.075, 0.075), color = handColor)
        self.handSide3 = sp.Beam (size = handSideSize, center = (0, -0.075, 0.075), color = handColor)
        
        fingerColor = (0.01, 1, 0.01)
        fingerSize = (0.3, 0.05, 0.05)
        fingerJoint = (-0.125, 0, 0)
        self.finger0 = sp.Beam (size = fingerSize, center = (0.15, 0, -0.1), joint = fingerJoint, pivot = (0, -1, 0), color = fingerColor)
        self.finger1 = sp.Beam (size = fingerSize, center = (0.15, 0, 0.1), joint = fingerJoint, pivot = (0, 1, 0), color = fingerColor)
        self.finger2 = sp.Beam (size = fingerSize, center = (0.15, -0.1, 0), joint = fingerJoint, pivot = (0, 0, 1), color = fingerColor)
        self.finger3 = sp.Beam (size = fingerSize, center = (0.15, 0.1, 0), joint = fingerJoint, pivot = (0, 0, -1), color = fingerColor)
        
    def display (self):
        self.stand (parts = lambda:
            self.base (rotation = sp.world.control.baseAngle, parts = lambda:
                self.shoulder (rotation = sp.world.control.shoulderAngle, parts = lambda:
                    self.elbow (rotation = sp.world.control.elbowAngle, parts = lambda:
                        self.wrist (rotation = sp.world.control.wristAngle, parts = lambda:
                            self.handCenter (rotation = sp.world.control.wristAngle))))))
'''

, parts = lambda:
    self.handSide0 () +
    self.handSide1 () +
    self.handSide2 () +
    self.handSide3 () +
    self.finger0 (rotation = sp.world.robot.finAng) +
    self.finger1 (rotation = sp.world.robot.finAng) +
    self.finger2 (rotation = sp.world.robot.finAng) +
    self.finger3 (rotation = sp.world.robot.finAng)
    '''
        
