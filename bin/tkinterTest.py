import tkinter as tk
import math
import ast

import GPIOArm


class Interface(object):
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400
    buttonWidth = 8
    maxButtons = SCREEN_WIDTH/(15*buttonWidth)
    buttonNumber = iter(range(0xEFFFFFFF))
    buttonColumn = buttonNumber.__next__() % maxButtons
    buttonRow = 2
    arm = GPIOArm.Arm()
    window = tk.Tk()
    commandList = ["if", "for", "while", "break", "continue"]
    armList = []
    expressionList = ["+", "-", "*", "/", "//", "%", "**", "<<", ">>", "|", "^", "&", "~", "@"]
    expressionExplanationList = ["optellen", "aftrekken",
                                 "vermenigvuldigen", "delen", "delen zonder rest", "rest van deling",
                                 "machtsverheffen", "Bitwise shift naar links", "Bitwise shift naar rechts",
                                 "Bitwise OR", "Bitwise XOR", "Bitwise AND", "Bitwise NOT",
                                 "Matrix vermenigvuldiging"]
    equationList = ["==", "!=", "<", "<=", ">", ">=", "is", "isNot"]
    logicGateList = ["AND", "OR", "XOR", "NOT"]
    logicGateList2 = ["NAND", "NOR", "XNOR"]
    variableList = ["i", "j", "k", "l"]
    options = tk.StringVar(window)
    armOptions = tk.StringVar(window)
    moveOptions = tk.StringVar(window)
    logicGateOptions = tk.StringVar(window)
    logicGateOptions2 = tk.StringVar(window)

    def __init__(self):
        self.window.geometry(str(self.SCREEN_WIDTH)+"x"+str(self.SCREEN_HEIGHT))
        self.window.title = "robotarm"
        self.options.set("Select one")
        optionMenu = tk.OptionMenu(self.window, self.options, *self.commandList)
        optionMenu.config(width=self.buttonWidth)
        optionMenu.grid(row=self.buttonRow, column=self.buttonColumn)
        print(self.buttonNumber)
        self.options.trace('w', self.getOption)
        for attr in dir(self.arm):
            if not callable(getattr(self.arm, attr)) and not attr.startswith("_"):
                self.armList.append(attr)
        self.armOptions.set("Select one")
        armMenu = tk.OptionMenu(self.window, self.armOptions, *self.armList)
        armMenu.config(width=self.buttonWidth)
        armMenu.grid(row=self.buttonRow, column=self.buttonColumn)
        self.moveOptions.set("Select one")
        self.armOptions.trace('w', self.getArmOption)
        self.moveOptions.trace('w', self.getMoveOption)
        self.window.mainloop()

    def getOption(self, *_args):
        print(self.options.get())

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
        moveMenu.grid(row=self.buttonRow, column=self.buttonColumn)

    def getMoveOption(self, *_args):
        print(self.armOptions.get()+" moving "+self.moveOptions.get())


interface = Interface()
