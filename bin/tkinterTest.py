import tkinter as tk
import ast
import time
import GPIOArm
import tkTooltip
import localisationdata as ld
import configparser


class Interface(object):
    iniReader = configparser.ConfigParser()
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    buttonWidth = 8
    maxButtons = SCREEN_WIDTH//(16*buttonWidth)
    buttonNumber = iter(range(0xEFFFFFFF))
    arm = GPIOArm.Arm()
    window = tk.Tk()
    commandList = ["if", "elif", "else", "for", "while"]
    advancedCommandList = ["break", "continue"]
    armList = []
    expressionList = ["+", "-", "*", "/", "//", "%", "**"]
    advancedExpressionList = ["<<", ">>", "|", "^", "&", "~", "@"]
    equationList = ["==", "!=", "<", "<=", ">", ">="]
    advancedEquationList = ["is", "is not", "in", "not in"]
    logicGateList = ["AND", "OR", "XOR", "NOT"]
    advancedLogicGateList = ["NAND", "NOR", "XNOR"]
    variableList = ["i", "j", "k", "l"]
    fileOptions = tk.StringVar(window)
    commandOptions = tk.StringVar(window)
    expressionOptions = tk.StringVar(window)
    armOptions = tk.StringVar(window)
    moveOptions = tk.StringVar(window)
    logicGateOptions = tk.StringVar(window)

    def __init__(self):
        self.iniReader.read('config.ini')
        self.advancedMode = int(self.iniReader['options']['ADVANCED_MODE'])
        if self.advancedMode:
            self.expressionList += self.advancedExpressionList
            self.commandList += self.advancedCommandList
            self.equationList += self.advancedEquationList
            self.logicGateList += self.advancedLogicGateList
        self.window.geometry(str(self.SCREEN_WIDTH)+"x"+str(self.SCREEN_HEIGHT))
        self.window.title = ld.windowName
        self.commandOptions.set(ld.commandWindowName)
        fileMenu = tk.OptionMenu(self.window, self.fileOptions, *ld.fileMenuList)
        fileMenu.config(width=self.buttonWidth)
        fileMenu.grid(row=self.buttonRow(), column=self.buttonColumn())
        fileMenu['menu'].add_checkbutton(label=ld.advanced, variable=self.advancedMode, onvalue=1, offvalue=0, command=self.setAdvancedMode)
        self.fileOptions.set(ld.fileWindowName)
        self.commandMenu = tk.OptionMenu(self.window, self.commandOptions, *self.commandList)
        self.commandMenu.config(width=self.buttonWidth)
        self.commandMenu.grid(row=self.buttonRow(), column=self.buttonColumn())
        self.commandOptions.trace('w', self.getCommandOption)
        self.expressionOptions.set(ld.expressionWindowName)
        self.expressionMenu = tk.OptionMenu(self.window, self.expressionOptions, *self.expressionList)
        self.expressionMenu.config(width=self.buttonWidth)
        self.expressionMenu['menu'].bind("<Enter>", self.on_enter)
        self.expressionMenu['menu'].bind("<Leave>", self.on_leave)
        # for i in range(self.expressionMenu['menu'].index("end")+1):
        # print(self.expressionMenu['menu'].entrycget(i, "state"))
        # tkTooltip.Tooltip(self.expressionMenu['menu'].entrycget(i, "label"), text=ld.expressionExplanationList[i])
        self.expressionMenu.grid(row=self.buttonRow(), column=self.buttonColumn())
        self.expressionOptions.trace('w', self.getExpressionOption)
        for attr in dir(self.arm):
            if not callable(getattr(self.arm, attr)) and not attr.startswith("_"):
                self.armList.append(getattr(self.arm, attr).name)
        self.armOptions.set(ld.armWindowName)
        armMenu = tk.OptionMenu(self.window, self.armOptions, *self.armList)
        armMenu.config(width=self.buttonWidth)
        armMenu.grid(row=self.buttonRow(), column=self.buttonColumn())
        self.moveOptions.set(ld.movementWindowName)
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

    def setAdvancedMode(self):
        self.commandMenu['menu'].delete(0, 'end')
        self.expressionMenu['menu'].delete(0, 'end')
        self.advancedMode ^= 1
        if self.advancedMode:
            for i in self.advancedCommandList:
                self.commandList.append(i)
            for i in self.advancedExpressionList:
                self.expressionList.append(i)
        else:
            for i in self.advancedCommandList:
                while i in self.commandList:
                    self.commandList.remove(i)
            for i in self.advancedExpressionList:
                while i in self.expressionList:
                    self.expressionList.remove(i)
        for i in self.commandList:
            self.commandMenu['menu'].add_command(label=i)
        for i in self.expressionList:
            self.expressionMenu['menu'].add_command(label=i)

    def on_leave(self, event):
        return

    def getCommandOption(self, *_args):
        print(self.commandOptions.get())

    def getExpressionOption(self, *_args):
        print(self.expressionOptions.get())

    def getArmOption(self, *_args):
        moveList = []
        self.moveOptions.set(ld.movementWindowName)
        if hasattr(getattr(self.arm, self.arm.partList(ld.partList.index(self.armOptions.get()))).part, "clock"):
            moveList = ld.baseMovements
        elif hasattr(getattr(self.arm, self.arm.partList(ld.partList.index(self.armOptions.get()))).part, "open"):
            moveList = ld.gripMovements
        elif hasattr(getattr(self.arm, self.arm.partList(ld.partList.index(self.armOptions.get()))).part, "on"):
            moveList.append(ld.ledMovement)
        else:
            moveList = ld.normalMovements
        moveList.append(ld.offMovement)

        moveMenu = tk.OptionMenu(self.window, self.moveOptions, *moveList)
        moveMenu.config(width=self.buttonWidth)
        moveMenu.grid(row=self.buttonRow(), column=self.buttonColumn())

    def getMoveOption(self, *_args):
        print(self.armOptions.get()+" moving "+self.moveOptions.get())


interface = Interface()
