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
        self._simulationOption = 0 # iniwriter

        # Create interface items
        self._infoText = tk.Label(self._window, text="Do you want to run the simulation for " + self._libraryList[0] + " ?")#ld
        self._infoText.grid(row=0, column=1, sticky='w')
        rownumber = 1
        self._simulationOptionVar = tk.StringVar(value = self._simulationOption)

        #done in a round about way, meant for moday morning meetings for feedback
        tk.Radiobutton(self._window, text = "yes", variable = self._simulationOptionVar, value = self._simulationOption ,command = self._updateRadiobuttons).grid(row = rownumber, column = 1, sticky = "w")
        rownumber += 1
        tk.Radiobutton(self._window, text = "no", variable =  self._simulationOptionVar, value = not self._simulationOption, command = self._updateRadiobuttons).grid(row = rownumber, column = 1, sticky = "w")
        
        self._saveButton = tk.Button(self._window, text=ld.saveButton, command=self._saveData)
        rownumber += 1
        self._saveButton.grid(row=rownumber, column=1, sticky='w')

        # Start program.
        self._window.grid(row=0, column=0)


    # Updates selected language.
    def _updateRadiobuttons(self):
        self._simulationOption = str(self._simulationOptionVar.get())

    # Saves updated data to ini file. Closes this program and launches setupUsedIO.
    def _saveData(self):
        #self._iniWriter["OPTIONS"]["LANGUAGE"] = self._selectedLanguage
        #with open(self._iniFile, 'w') as configFile:
        #    self._iniWriter.write(configFile, space_around_delimiters=False)
        self._window.master.destroy()
    
