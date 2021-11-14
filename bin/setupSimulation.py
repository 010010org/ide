import tkinter as tk  # Used to create interface
import localisationdata as ld  # Contains translated strings for selected language
import os  # Used to get library folders
import os.path  # Used to check if required files exist



class Interface (object):
    def __init__(self, parent, libraryList):
        self._parent = parent
        self._window = tk.Frame(parent)
        self._window.title = "Simulation" #ld
        self._libraryList = libraryList
        self._library = 0
        self._simulationOption = False
        #call function
        self._askSimulationOption()

    def _askSimulationOption(self):
        #add ld
        
        self._infoText = tk.Label(self._window, text="Do you want to run the simulation for " + self._libraryList[self._library] + " ?")#ld
        self._infoText.grid(row=0, column=1, sticky='w')
        rownumber = 1
        self._simulationOptionVar = tk.BooleanVar(value = self._simulationOption)

        #update option to default 0
        #done in a round about way, meant for moday morning meetings for feedback. ld for yes and no
        tk.Radiobutton(self._window, text = "yes", variable = self._simulationOptionVar, value = not self._simulationOption ,command = self._updateRadiobuttons).grid(row = rownumber, column = 1, sticky = "w")
        rownumber += 1
        tk.Radiobutton(self._window, text = "no", variable =  self._simulationOptionVar, value = self._simulationOption, command = self._updateRadiobuttons).grid(row = rownumber, column = 1, sticky = "w")
        
        self._saveButton = tk.Button(self._window, text=ld.saveButton, command=self._saveData)
        rownumber += 1
        self._saveButton.grid(row=rownumber, column=1, sticky='w')

        # Start program.
        self._window.grid(row=0, column=0)


    # Updates selected option.
    def _updateRadiobuttons(self):
        self._simulationOption = self._simulationOptionVar.get()


    def _saveData(self):
        #write to ini file which simulation has to be run, or call simulation here
        if self._simulationOption:
            print("calling: " + self._libraryList[self._library])

        #update library number after all calls have been made for that library
        self._library += 1

        #reset simulationOption so the next option will not be chosen. #better explanation needed
        self._simulationOption = False

        #all libraries asked
        if self._library == len(self._libraryList):
            self._window.master.destroy()
        else:
            self._askSimulationOption()
    
