import tkinter as tk
from tkinter.constants import END  # Used to create interface
import localisationdata as ld  # Contains translated strings for selected language
import os  # Used to get library folders
import os.path  # Used to check if required files exist
import time



class Interface (object):
    def __init__(self, parent, libraryList):
        self._parent = parent
        self._window = tk.Frame(parent)
        self._window.title = ld.windowTitle #ld
        self._libraryList = libraryList
        self._library = 0
        self._simulationOption = False
        self._pathToSimulation = "/simulations/robotArmSim"
        self._testPath = "/bin/test.py"

        #call function
        self._askSimulationOption()
        
    def _askSimulationOption(self):
        #schrijft eroverheen, buffer leegmaken
        self._infoText = tk.Label(self._window, text = ld.simulationInfoText + self._libraryList[self._library] + " ?")
        self._infoText.grid(row=0, column=1, sticky='w')
        rownumber = 1
        self._simulationOptionVar = tk.BooleanVar(value = self._simulationOption)

        #update option to default 0
        #done in a round about way, meant for moday morning meetings for feedback.
        tk.Radiobutton(self._window, text = ld.yes , variable = self._simulationOptionVar, value = not self._simulationOption ,command = self._updateRadiobuttons).grid(row = rownumber, column = 1, sticky = "w")
        rownumber += 1
        tk.Radiobutton(self._window, text = ld.no , variable =  self._simulationOptionVar, value = self._simulationOption, command = self._updateRadiobuttons).grid(row = rownumber, column = 1, sticky = "w")
        #self._saveButton = tk.Button(self._window, text=ld.saveButton, command=self._saveData)
        rownumber += 1
        #lambda functies moeten in een list, het eerste gedeelte zorgt ervoor dat de text van _infotext verwijderd wordt ander overschrijft het de text die er al staat
        self._saveButton = tk.Button(self._window, text=ld.saveButton, command=lambda:[self._infoText.config(text = "") , self._saveData()])
        self._saveButton.grid(row=rownumber, column=1, sticky='w')

        # Start program.
        self._window.grid(row=0, column=0)


    # Updates selected option.
    def _updateRadiobuttons(self):
        self._simulationOption = self._simulationOptionVar.get()

    def startSimulation(self, library):
        #works with one call, need 2 or more calls.
        #double clicking .py file
        #wherispython , pythonfile , path to simulation
        x = os.system(str(os.getcwd() + self._pathToSimulation + '/' + library + '.py'))
        print(x)
        x
        

    def _saveData(self):
        if self._simulationOption:
            #call actual simulation or function to call simulation
            print("calling: " + self._libraryList[self._library])

        #reset simulationOption so the next option will not be chosen. #better explanation needed
        
        #loop through libraries selected until none are left

        if self._simulationOption:
            import threading
            #deamon closes thread once the program is killed
            x = threading.Thread(target = self.startSimulation, args = (self._libraryList[self._library],), daemon = True)
            print("Thread started")
            x.start()
            self._window.master.destroy()

        self._library += 1
        self._simulationOption = False

        if self._library != len(self._libraryList):
            self._askSimulationOption()
        

            
            
    