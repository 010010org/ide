import tkinter as tk  # Used to create interface
import sys  # Used to add folders to the path
import os  # Used to get current directory

import localisationdata as ld  # Contains translated strings for selected language
import configparser  # Used to read/write ini files


# This program creates a simple start menu, allowing the user to choose which sub-program they want to start
# It allows the user to unlock new sub-programs based on the programs they've already used.
# This progress is stored in an ini file, so users can keep going from where they left off last time when they start a new session.
class Interface(object):
    # _ signifies private field
    _root = tk.Tk()
    #coonfigparse library coverts ini files to PEP8 format
    _iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
    _iniFile = "config.ini"
    #forward declaration, used in drawWindow, otherwise a warning / error appears that variables are initiated in the function
    _controlButton = None
    _AdvancedControlButton = None
    _programmingButton = None
    _AdvancedProgrammingButton = None
    _progress = 0
    _pathToDirectoryAbove = os.path.dirname(os.getcwd())
    _pathToSimulation = '/GUI-simpylc/RobotArm/world.py'
    

    # __init__ is called when the object is made
    def __init__(self):
        self._window = tk.Frame(self._root)
        self._window.title = ld.startMenuName
        self.drawWindow()
        self.getProgress()
        self._window.grid(row=0, column=0)
        self._root.mainloop()

    def runSetup(self):
        #unlocks different menus
        #TODO can remove some getProgress

        self.getProgress()
        self._progress = max(self._progress, 1)
        #_iniWriter[header][field]
        self._iniWriter["OPTIONS"]["PROGRESS"] = str(self._progress)
        with open(self._iniFile, 'w') as configFile:
            self._iniWriter.write(configFile, space_around_delimiters=False)
        #import not above because of load times on raspberryPi 3
        import setupLanguage
        setupLanguage.Interface(tk.Toplevel(self._root))
        self.getProgress()

    #below functions work the same as runSetup

    def runProgrammer(self):
        self.getProgress()
        self._progress = max(self._progress, 4)
        self._iniWriter["OPTIONS"]["PROGRESS"] = str(self._progress)
        with open(self._iniFile, 'w') as configFile:
            self._iniWriter.write(configFile, space_around_delimiters=False)

        self._window.grid_remove()
        import tkProgrammerInterface
        tkProgrammerInterface.Interface(self._root)
        self.getProgress()

    def runControlProgram(self, advancedMode):
        self.getProgress()
        if advancedMode:
            self._progress = max(self._progress, 3)
        else:
            self._progress = max(self._progress, 2)
        self._iniWriter["OPTIONS"]["PROGRESS"] = str(self._progress)
        with open(self._iniFile, 'w') as configFile:
            self._iniWriter.write(configFile, space_around_delimiters=False)

        self._window.grid_remove()
        import tkControlInterface
        tkControlInterface.Interface(self._root, advancedMode)
        self.getProgress()      

    def drawWindow(self):
        #copies everything from localisation\en.py or nl.py to localisationData in the bat file
        welcomeMessage = tk.Label(self._window, text=ld.startMenuMessage)
        welcomeMessage.grid(row=0, columnspan=3, sticky='w')
        setupButton = tk.Button(self._window, text=ld.setupOption, command=self.runSetup)
        setupButton.grid(row=1, column=1)
        #give very button its function with the command=lambda:
        #can be used without lambda but tkinter likes to give data with every button press.
        self._controlButton = tk.Button(self._window, text=ld.controlArmOption, command=lambda: self.runControlProgram(0))
        self._controlButton.grid(row=1, column=2)
        self._controlButton['state'] = tk.DISABLED
        self._AdvancedControlButton = tk.Button(self._window, text=ld.advancedControlArmOption, command=lambda: self.runControlProgram(1))
        self._AdvancedControlButton.grid(row=1, column=3)
        self._AdvancedControlButton['state'] = tk.DISABLED
        self._programmingButton = tk.Button(self._window, text=ld.programOption, command=lambda: self.runProgrammer())
        self._programmingButton.grid(row=1, column=4)
        self._programmingButton['state'] = tk.DISABLED

    def getProgress(self):
        self._iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self._iniWriter.optionxform = str
        self._iniWriter.read(self._iniFile)
        self._progress = int(self._iniWriter["OPTIONS"]["PROGRESS"])
        #attributes start as disabled, can configure this in config.ini with the PROGRESS = X, used with the idea of unlocking features in mind. 
        if self._progress >= 1:
            self._controlButton['state'] = tk.NORMAL
            if self._progress >= 2:
                self._AdvancedControlButton['state'] = tk.NORMAL
                if self._progress >= 3:
                    self._programmingButton['state'] = tk.NORMAL
        self.fixImports()

    # Adds folders of libraries selected in setupUsedIO to the path, so they can be imported by the user in tkProgrammerInterface
    # without this kind of added code.
    def fixImports(self):
        for i in self._iniWriter["LIBRARIES"]:
            if self._iniWriter["LIBRARIES"][i] == "1":
                if os.getcwd()+"/lib/"+i not in sys.path:
                    #puts the field i into the path
                    sys.path.append(os.getcwd()+"/lib/"+i)


Interface()
