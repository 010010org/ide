import tkinter as tk
from tkinter import Button

import localisationdata as ld
import configparser


class Interface(object):
    _root = tk.Tk()
    _iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
    _iniFile = "config.ini"
    _controlButton = None
    _AdvancedControlButton = None
    _programmingButton = None
    _AdvancedProgrammingButton = None
    _progress = 0

    def __init__(self):
        self._window = tk.Frame(self._root)
        self._window.title = ld.startMenuName
        self.drawWindow()
        self.getProgress()
        self._window.grid(row=0, column=0)
        self._root.mainloop()

    def runSetup(self):
        self.getProgress()
        self._progress = max(self._progress, 1)
        self._iniWriter["OPTIONS"]["PROGRESS"] = str(self._progress)
        with open(self._iniFile, 'w') as configFile:
            self._iniWriter.write(configFile, space_around_delimiters=False)
        import setupUsedIO
        setupUsedIO.Interface(tk.Toplevel(self._root))
        self.getProgress()

    def runProgrammer(self, advancedMode):
        self.getProgress()
        if advancedMode:
            self._progress = max(self._progress, 5)
        else:
            self._progress = max(self._progress, 4)
        self._iniWriter["OPTIONS"]["PROGRESS"] = str(self._progress)
        with open(self._iniFile, 'w') as configFile:
            self._iniWriter.write(configFile, space_around_delimiters=False)

        self._window.grid_remove()
        import tkProgrammerInterface
        tkProgrammerInterface.Interface(self._root, advancedMode)
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
        welcomeMessage = tk.Label(self._window, text=ld.startMenuMessage)
        welcomeMessage.grid(row=0, columnspan=3, sticky='w')
        setupButton = tk.Button(self._window, text=ld.setupOption, command=self.runSetup)
        setupButton.grid(row=1, column=1)
        self._controlButton = tk.Button(self._window, text=ld.controlArmOption, command=lambda: self.runControlProgram(0))
        self._controlButton.grid(row=1, column=2)
        self._controlButton['state'] = tk.DISABLED
        self._AdvancedControlButton = tk.Button(self._window, text=ld.advancedControlArmOption, command=lambda: self.runControlProgram(1))
        self._AdvancedControlButton.grid(row=1, column=3)
        self._AdvancedControlButton['state'] = tk.DISABLED
        self._programmingButton = tk.Button(self._window, text=ld.programOption, command=lambda: self.runProgrammer(0))
        self._programmingButton.grid(row=1, column=4)
        self._programmingButton['state'] = tk.DISABLED
        self._AdvancedProgrammingButton = tk.Button(self._window, text=ld.AdvancedProgramOption, command=lambda: self.runProgrammer(1))
        self._AdvancedProgrammingButton.grid(row=1, column=5)
        self._AdvancedProgrammingButton['state'] = tk.DISABLED

    def getProgress(self):
        self._iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self._iniWriter.optionxform = str
        self._iniWriter.read(self._iniFile)
        self._progress = int(self._iniWriter["OPTIONS"]["PROGRESS"])
        if self._progress >= 1:
            self._controlButton['state'] = tk.NORMAL
            if self._progress >= 2:
                self._AdvancedControlButton['state'] = tk.NORMAL
                if self._progress >= 3:
                    self._programmingButton['state'] = tk.NORMAL
                    if self._progress >= 4:
                        self._AdvancedProgrammingButton['state'] = tk.NORMAL


Interface()
