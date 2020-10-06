import tkinter as tk
import ast
import time
import GPIOArm
import tkTooltip


class Interface(object):
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400
    buttonWidth = 8
    maxButtons = SCREEN_WIDTH//(15*buttonWidth)
    buttonNumber = iter(range(0xEFFFFFFF))
    arm = GPIOArm.Arm()
    window = tk.Tk()
    commandList = ["if", "elif", "else", "for", "while", "break", "continue"]
    armList = []
    expressionList = ["+", "-", "*", "/", "//", "%", "**", "<<", ">>", "|", "^", "&", "~", "@"]
    expressionExplanationList = ["optellen", "aftrekken",
                                 "vermenigvuldigen", "delen", "delen zonder rest", "rest van deling",
                                 "machtsverheffen", "Bitwise shift naar links", "Bitwise shift naar rechts",
                                 "Bitwise OR", "Bitwise XOR", "Bitwise AND", "Bitwise NOT",
                                 "Matrix vermenigvuldiging"]
    equationList = ["==", "!=", "<", "<=", ">", ">=", "is", "is not", "in", "not in"]
    logicGateList = ["AND", "OR", "XOR", "NOT"]
    logicGateList2 = ["NAND", "NOR", "XNOR"]
    variableList = ["i", "j", "k", "l"]
    options = tk.StringVar(window)
    expressionOptions = tk.StringVar(window)
    armOptions = tk.StringVar(window)
    moveOptions = tk.StringVar(window)
    logicGateOptions = tk.StringVar(window)
    logicGateOptions2 = tk.StringVar(window)

    def __init__(self):
        self.window.geometry(str(self.SCREEN_WIDTH)+"x"+str(self.SCREEN_HEIGHT))
        self.window.title = "robotarm"
        self.options.set("command")
        optionMenu = tk.OptionMenu(self.window, self.options, *self.commandList)
        optionMenu.config(width=self.buttonWidth)
        optionMenu.grid(row=self.buttonRow(), column=self.buttonColumn())
        self.options.trace('w', self.getOption)
        self.expressionOptions.set("expressions")
        self.expressionMenu = tk.OptionMenu(self.window, self.expressionOptions, *self.expressionList)
        self.expressionMenu.config(width=self.buttonWidth)
        self.expressionMenu['menu'].bind("<Enter>", self.on_enter)
        self.expressionMenu['menu'].bind("<Leave>", self.on_leave)
        #for i in range(self.expressionMenu['menu'].index("end")+1):
            #print(self.expressionMenu['menu'].entrycget(i, "state"))
            #tkTooltip.Tooltip(self.expressionMenu['menu'].entrycget(i, "label"), text=self.expressionExplanationList[i])
        self.expressionMenu.grid(row=self.buttonRow(), column=self.buttonColumn())
        self.expressionOptions.trace('w', self.getExpressionOption)
        for attr in dir(self.arm):
            if not callable(getattr(self.arm, attr)) and not attr.startswith("_"):
                self.armList.append(attr)
        self.armOptions.set("part")
        armMenu = tk.OptionMenu(self.window, self.armOptions, *self.armList)
        armMenu.config(width=self.buttonWidth)
        armMenu.grid(row=self.buttonRow(), column=self.buttonColumn())
        self.moveOptions.set("direction")
        self.armOptions.trace('w', self.getArmOption)
        self.moveOptions.trace('w', self.getMoveOption)
        self.window.mainloop()

    def buttonRow(self):
        return (self.buttonNumber.__next__()//2) // self.maxButtons + 2

    def buttonColumn(self):
        return (self.buttonNumber.__next__()//2) % self.maxButtons + 1

    def on_enter(self, event):
        time.sleep(0.025)
        for i in range(self.expressionMenu['menu'].index("end")+1):
            if self.expressionMenu['menu'].entrycget(i, "state") == "active":
                print(self.expressionMenu['menu'].entrycget(i, "label"))
        print(event)

    def on_leave(self, event):
        return

    def getOption(self, *_args):
        print(self.options.get())

    def getExpressionOption(self, *_args):
        print(self.expressionOptions.get())

    def getArmOption(self, *_args):
        moveList = []
        self.moveOptions.set("Select one")
        if hasattr(getattr(self.arm, self.armOptions.get()).part, "clock"):
            moveList = ["clock", "counter"]
        elif hasattr(getattr(self.arm, self.armOptions.get()).part, "open"):
            moveList = ["open", "close"]
        elif hasattr(getattr(self.arm, self.armOptions.get()).part, "on"):
            moveList.append("on")
        else:
            moveList = ["up", "down"]
        moveList.append("off")

        moveMenu = tk.OptionMenu(self.window, self.moveOptions, *moveList)
        moveMenu.config(width=self.buttonWidth)
        moveMenu.grid(row=self.buttonRow(), column=self.buttonColumn())

    def getMoveOption(self, *_args):
        print(self.armOptions.get()+" moving "+self.moveOptions.get())


interface = Interface()
