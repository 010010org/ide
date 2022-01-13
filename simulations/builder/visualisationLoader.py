class VisualisationLoader():
    def __init__(self,library):
        self.library = library
        self.libraryDict = {'robotArm': self.robotArm,
                            'snake' : self.snake}
        #automatically call function that updates self.simulation
        self.selectLibrary()
    
    def selectLibrary(self):
        #checks for the library given by setupsimulation and calls the correct function
        if self.library in self.libraryDict:
            self.libraryDict[self.library]()
        else:
            print(f"library niet gevonden, bekijk de spelling nog eens")
            exit()
    
    def robotArm(self):
        from robotArmSimulation import RobotArmSimulation
        self.simulation = RobotArmSimulation().createSimulation()
    
    def snake(self):
        from snake import Snake
        self.simulation = Snake().createSimulation()

    def getSimulation(self):
        #function that gets called directly, returns the updated simulation to visualisation
        return self.simulation