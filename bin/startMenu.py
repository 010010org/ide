import tkinter as tk
import localisationdata as ld
import configparser


class Interface(object):
    _window = tk.Tk()
    _iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
    _iniFile = "config.ini"

    def __init__(self):
        self._window.title = ld.startMenuName
        self._iniWriter.optionxform = str
        self._iniWriter.read(self._iniFile)
        self._progress = int(self._iniWriter["OPTIONS"]["PROGRESS"])
        self.drawWindow()
        self._window.mainloop()

    def runSetup(self):
        self._progress = max(self._progress, 1)
        self._iniWriter["OPTIONS"]["PROGRESS"] = str(self._progress)
        with open(self._iniFile, 'w') as configFile:
            self._iniWriter.write(configFile, space_around_delimiters=False)

        self._window.destroy()
        import setupUsedIO
        setupUsedIO.Interface()

    def runProgrammer(self, advancedMode):
        if advancedMode:
            self._progress = max(self._progress, 5)
        else:
            self._progress = max(self._progress, 4)
        self._iniWriter["OPTIONS"]["PROGRESS"] = str(self._progress)
        with open(self._iniFile, 'w') as configFile:
            self._iniWriter.write(configFile, space_around_delimiters=False)

        self._window.withdraw()
        import tkinterTest
        tkinterTest.Interface(advancedMode)
        self._window.deiconify()

    def runControlProgram(self, advancedMode):
        if advancedMode:
            self._progress = max(self._progress, 3)
        else:
            self._progress = max(self._progress, 2)
        self._iniWriter["OPTIONS"]["PROGRESS"] = str(self._progress)
        with open(self._iniFile, 'w') as configFile:
            self._iniWriter.write(configFile, space_around_delimiters=False)

        self._window.destroy()
        import tkControlInterface
        tkControlInterface.Interface(advancedMode)

    def drawWindow(self):
        welcomeMessage = tk.Label(self._window, text=ld.startMenuMessage)
        welcomeMessage.grid(row=0, columnspan=3, sticky='w')
        setupButton = tk.Button(self._window, text=ld.setupOption, command=self.runSetup)
        setupButton.grid(row=1, column=1)
        controlButton = tk.Button(self._window, text=ld.controlArmOption, command=lambda: self.runControlProgram(0))
        controlButton.grid(row=1, column=2)
        controlButton['state'] = tk.DISABLED
        AdvancedControlButton = tk.Button(self._window, text=ld.advancedControlArmOption, command=lambda: self.runControlProgram(1))
        AdvancedControlButton.grid(row=1, column=3)
        AdvancedControlButton['state'] = tk.DISABLED
        programmingButton = tk.Button(self._window, text=ld.programOption, command=lambda: self.runProgrammer(0))
        programmingButton.grid(row=1, column=4)
        programmingButton['state'] = tk.DISABLED
        AdvancedProgrammingButton = tk.Button(self._window, text=ld.AdvancedProgramOption, command=lambda: self.runProgrammer(1))
        AdvancedProgrammingButton.grid(row=1, column=5)
        AdvancedProgrammingButton['state'] = tk.DISABLED

        if self._progress >= 1:
            controlButton['state'] = tk.NORMAL
            if self._progress >= 2:
                AdvancedControlButton['state'] = tk.NORMAL
                if self._progress >= 3:
                    programmingButton['state'] = tk.NORMAL
                    if self._progress >= 4:
                        AdvancedProgrammingButton['state'] = tk.NORMAL

Interface()