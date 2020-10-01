import tkinter as tk
from GPIOArm import Arm

arm = Arm()
window = tk.Tk()
window.geometry("300x200")
window.title = "test"

commandList = ["if", "for", "while", "goto"]

options = tk.StringVar(window)
options.set("Select one") # default value

om1 =tk.OptionMenu(window, options, *commandList)
om1.grid(row=2,column=1)

def get_option(*args):
    print(options.get())

options.trace('w',get_option)

armList=[]
for attr in dir(arm):
    if not callable(getattr(arm, attr)) and not attr.startswith("_"):
            armList.append(attr)

armOptions = tk.StringVar(window)
armOptions.set("Select one") # default value

armMenu =tk.OptionMenu(window, armOptions, *armList)
armMenu.grid(row=2,column=2)

moveList = []
moveOptions = tk.StringVar(window)
moveOptions.set("Select one") # default value

def getArmOption(*args):
    if(hasattr(getattr(arm, armOptions.get()).part, "clock")):
        moveList=["clock", "counter", "off"]
    elif(hasattr(getattr(arm, armOptions.get()).part, "open")):
        moveList=["open", "close", "off"]
    elif(hasattr(getattr(arm, armOptions.get()).part, "on")):
        moveList=["on", "off"]
    else:
        moveList=["up", "down", "off"]

    moveMenu=tk.OptionMenu(window, moveOptions, *moveList)
    moveMenu.grid(row=2, column=3)

def getMoveOption(*args):
    print(armOptions.get()+" moving "+moveOptions.get())

armOptions.trace('w',getArmOption)
moveOptions.trace('w',getMoveOption)
window.mainloop()  # Keep the window open