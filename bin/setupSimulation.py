import tkinter as tk # Used to create interface
import localisationdata as ld  # Contains translated strings for selected language
import os  # Used to get library folders
import os.path  # Used to check if required files exist



class Interface (object):
    def __init__(self, parent, libraryList):
        self._parent = parent
        self._window = tk.Frame(parent)
        self._window.title = ld.windowTitle #ld
        self._libraryList = libraryList
        self._library = 0
        self._simulationOption = False #turns to true when simulation is called
        self._pathToSimulationFolder = "/simulations/builder"

        #call function
        self._askSimulationOption()
        
    def _askSimulationOption(self):
        #clears text, then writes over it
        self._infoText = tk.Label(self._window, text = ld.simulationInfoText + self._libraryList[self._library] + " ?")
        self._infoText.grid(row=0, column=1, sticky='w')
        rownumber = 1
        self._simulationOptionVar = tk.BooleanVar(value = self._simulationOption)

        tk.Radiobutton(self._window, text = ld.yes , variable = self._simulationOptionVar, value = not self._simulationOption ,command = self._updateRadiobuttons).grid(row = rownumber, column = 1, sticky = "w")
        rownumber += 1
        tk.Radiobutton(self._window, text = ld.no , variable =  self._simulationOptionVar, value = self._simulationOption, command = self._updateRadiobuttons).grid(row = rownumber, column = 1, sticky = "w")
        rownumber += 1
        #lambda function must be in a list, otherwise it only calls the first or causes an error
        self._saveButton = tk.Button(self._window, text=ld.saveButton, command=lambda:[self._infoText.config(text = "") , self._saveData()])
        self._saveButton.grid(row=rownumber, column=1, sticky='w')

        # Start program.
        self._window.grid(row=0, column=0)


    # Updates selected option.
    def _updateRadiobuttons(self):
        self._simulationOption = self._simulationOptionVar.get()

    def startSimulation(self, library):
        #double clicking .py file
        #TODO wherispython , pythonfile , path to simulation
        #x = os.system(str(os.getcwd() + self._pathToSimulationFolder + '/' + library + 'Simulation.py'))
        x = os.system(str(os.getcwd())+ "/simulations/builder/visualisation.py")

        

    def _saveData(self):
        if self._simulationOption:
            #start a new thread that runs the simulation
            import threading
            #deamon closes thread once the program is killed
            x = threading.Thread(target = self.startSimulation, args = (self._libraryList[self._library],), daemon = True)
            print("simulation starting...")
            x.start()
            #destroys window asking to run simulation
            self._window.master.destroy()

        self._library += 1
        #keep asking to run simulation until all libraries are asked or 1 is chosen
        if self._library == len(self._libraryList):
            self._window.master.destroy()
        else:
            self._askSimulationOption()