import tkinter as tk
import localisationdata as ld
import configparser

window = tk.Tk()
window.title = ld.startMenuName
iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
iniWriter.optionxform = str  # Why is this not the default option?!
iniFile = "config.ini"
iniWriter.read(iniFile)
progress = int(iniWriter["OPTIONS"]["PROGRESS"])


def runSetup():
    global progress
    import setupUsedIO
    progress = max(progress, 1)
    iniWriter["OPTIONS"]["PROGRESS"] = str(progress)
    with open(iniFile, 'w') as configFile:
        iniWriter.write(configFile, space_around_delimiters=False)  # Again, why is this not the default option?!

    window.destroy()
    setupUsedIO.Interface()


def runProgrammer(advancedMode):
    global progress
    import tkinterTest

    if advancedMode:
        progress = max(progress, 5)
    else:
        progress = max(progress, 4)
    iniWriter["OPTIONS"]["PROGRESS"] = str(progress)
    with open(iniFile, 'w') as configFile:
        iniWriter.write(configFile, space_around_delimiters=False)

    window.destroy()
    tkinterTest.Interface(advancedMode)


def runControlProgram(advancedMode):
    global progress
    import tkArmInterface

    if advancedMode:
        progress = max(progress, 3)
    else:
        progress = max(progress, 2)
    iniWriter["OPTIONS"]["PROGRESS"] = str(progress)
    with open(iniFile, 'w') as configFile:
        iniWriter.write(configFile, space_around_delimiters=False)

    window.destroy()
    tkArmInterface.Interface(advancedMode)


welcomeMessage = tk.Label(window, text=ld.startMenuMessage)
welcomeMessage.grid(row=0, columnspan=3, sticky='w')
controlButton = tk.Button(window, text=ld.setupOption, command=runSetup)
controlButton.grid(row=1, column=1)
controlButton = tk.Button(window, text=ld.controlArmOption, command=lambda: runControlProgram(0))
controlButton.grid(row=1, column=2)
controlButton['state'] = tk.DISABLED
AdvancedControlButton = tk.Button(window, text=ld.advancedControlArmOption, command=lambda: runControlProgram(1))
AdvancedControlButton.grid(row=1, column=3)
AdvancedControlButton['state'] = tk.DISABLED
programmingButton = tk.Button(window, text=ld.programOption, command=lambda: runProgrammer(0))
programmingButton.grid(row=1, column=4)
programmingButton['state'] = tk.DISABLED
AdvancedProgrammingButton = tk.Button(window, text=ld.AdvancedProgramOption, command=lambda: runProgrammer(1))
AdvancedProgrammingButton.grid(row=1, column=5)
AdvancedProgrammingButton['state'] = tk.DISABLED

if progress >= 1:
    controlButton['state'] = tk.NORMAL
    if progress >= 2:
        AdvancedControlButton['state'] = tk.NORMAL
        if progress >= 3:
            programmingButton['state'] = tk.NORMAL
            if progress >= 4:
                AdvancedProgrammingButton['state'] = tk.NORMAL

window.mainloop()

