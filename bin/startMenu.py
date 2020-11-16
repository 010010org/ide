import tkinter as tk
import localisationdata as ld
import configparser

window = tk.Tk()
window.title = ld.startMenuName
iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
iniFile = "config.ini"
iniWriter.read(iniFile)
progress = int(iniWriter["OPTIONS"]["PROGRESS"])


def runProgrammer(advancedMode):
    global progress
    import tkinterTest

    if advancedMode:
        progress = max(progress, 4)
    else:
        progress = max(progress, 3)
    iniWriter["OPTIONS"]["PROGRESS"] = str(progress)
    with open(iniFile, 'w') as configFile:
        iniWriter.write(configFile)

    window.destroy()
    tkinterTest.Interface(advancedMode)


def runControlProgram(advancedMode):
    global progress
    import tkArmInterface

    if advancedMode:
        progress = max(progress, 2)
    else:
        progress = max(progress, 1)
    iniWriter["OPTIONS"]["PROGRESS"] = str(progress)
    with open(iniFile, 'w') as configFile:
        iniWriter.write(configFile)

    window.destroy()
    tkArmInterface.Interface(advancedMode)


welcomeMessage = tk.Label(window, text=ld.startMenuMessage)
welcomeMessage.grid(row=0, columnspan=2)
controlButton = tk.Button(window, text=ld.controlArmOption, command=lambda: runControlProgram(0))
controlButton.grid(row=1, column=1)
AdvancedControlButton = tk.Button(window, text=ld.advancedControlArmOption, command=lambda: runControlProgram(1))
AdvancedControlButton.grid(row=1, column=2)
AdvancedControlButton['state'] = tk.DISABLED
programmingButton = tk.Button(window, text=ld.programOption, command=lambda: runProgrammer(0))
programmingButton.grid(row=1, column=3)
programmingButton['state'] = tk.DISABLED
AdvancedProgrammingButton = tk.Button(window, text=ld.AdvancedProgramOption, command=lambda: runProgrammer(1))
AdvancedProgrammingButton.grid(row=1, column=4)
AdvancedProgrammingButton['state'] = tk.DISABLED

if progress >= 1:
    AdvancedControlButton['state'] = tk.NORMAL
    if progress >= 2:
        programmingButton['state'] = tk.NORMAL
        if progress >= 3:
            AdvancedProgrammingButton['state'] = tk.NORMAL

window.mainloop()

