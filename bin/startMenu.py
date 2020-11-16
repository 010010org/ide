import tkinter as tk
import localisationdata as ld

window = tk.Tk()
window.title = ld.startMenuName


def runProgrammer():
    import tkinterTest
    window.destroy()
    tkinterTest.Interface()


def runControlProgram(advancedMode):
    import tkArmInterface
    window.destroy()
    tkArmInterface.Interface(advancedMode)


welcomeMessage = tk.Label(window, text=ld.startMenuMessage)
welcomeMessage.grid(row=0, columnspan=2)
controlButton = tk.Button(window, text=ld.controlArmOption, command=lambda: runControlProgram(0))
controlButton.grid(row=1, column=1)
AdvancedControlButton = tk.Button(window, text=ld.advancedControlArmOption, command=lambda: runControlProgram(1))
AdvancedControlButton.grid(row=1, column=2)
programmingButton = tk.Button(window, text=ld.programOption, command=runProgrammer)
programmingButton.grid(row=1, column=3)
window.mainloop()

