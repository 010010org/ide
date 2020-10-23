import tkinter as tk
import localisationdata as ld

window = tk.Tk()
window.title = ld.startMenuName


def runProgrammer():
    import tkinterTest
    window.destroy()
    tkinterTest.Interface()


def runControlProgram():
    import tkArmInterface
    window.destroy()
    tkArmInterface.Interface()


welcomeMessage = tk.Label(window, text=ld.startMenuMessage)
welcomeMessage.grid(row=0, columnspan=2)
controlButton = tk.Button(window, text=ld.controlArmOption, command=runControlProgram)
controlButton.grid(row=1, column=1)
programmingButton = tk.Button(window, text=ld.programOption, command=runProgrammer)
programmingButton.grid(row=1, column=2)
window.mainloop()

