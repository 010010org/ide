import tkinter as tk
import tkinter.ttk as ttk
import GPIOArm
import localisationdata as ld
import configparser


class Interface(object):
    iniReader = configparser.ConfigParser()
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    buttonWidth = 9
    maxButtons = SCREEN_WIDTH//(14*buttonWidth)
    buttonNumber = iter(range(0xEFFFFFFF))
    arm = GPIOArm.Arm()
    window = tk.Tk()
    commandList = ["if", "elif", "else", "for", "while"]
    advancedCommandList = ["break", "continue"]
    expressionList = ["+", "-", "*", "/", "//", "%", "**"]
    advancedExpressionList = ["<<", ">>", "|", "^", "&", "~", "@"]
    equationList = ["==", "!=", "<", "<=", ">", ">="]
    advancedEquationList = ["is", "is not", "in", "not in"]
    logicGateList = ["AND", "OR", "XOR", "NOT"]
    advancedLogicGateList = ["NAND", "NOR", "XNOR"]
    variableList = ["i", "j", "k", "l"]
    moveList = [None]
    fileOptions = tk.StringVar(window)
    commandOptions = tk.StringVar(window)
    expressionOptions = tk.StringVar(window)
    equationOptions = tk.StringVar(window)
    armOptions = tk.StringVar(window)
    moveOptions = tk.StringVar(window)
    logicGateOptions = tk.StringVar(window)
    tipWindow = None

    def __init__(self):
        # read state of advanced mode and implement if needed
        self.iniReader.read('config.ini')
        self.advancedMode = int(self.iniReader['options']['ADVANCED_MODE'])
        if self.advancedMode:
            self.expressionList += self.advancedExpressionList
            self.commandList += self.advancedCommandList
            self.equationList += self.advancedEquationList
            self.logicGateList += self.advancedLogicGateList

        # setup window
        self.window.geometry(str(self.SCREEN_WIDTH)+"x"+str(self.SCREEN_HEIGHT))
        self.window.title = ld.windowName

        # setup menu bar
        self.menuBar = tk.Menu(self.window)

        # setup file menu (only decorative except for advanced mode for now)
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        for i in ld.fileMenuList:
            self.fileMenu.add_command(label=i)
        self.fileMenu.add_checkbutton(label=ld.advanced, variable=self.advancedMode, onvalue=1, offvalue=0, command=self.setAdvancedMode)
        self.menuBar.add_cascade(label=ld.fileWindowName, menu=self.fileMenu)

        # setup command menu
        self.commandMenu = tk.Menu(self.menuBar, tearoff=0)
        for i in self.commandList:
            self.commandMenu.add_command(label=i)
        self.commandMenu.bind("<Button-1>", self.commandClick)
        self.menuBar.add_cascade(label=ld.commandWindowName, menu=self.commandMenu)

        # setup expression menu
        self.expressionMenu = tk.Menu(self.menuBar, tearoff=0)
        for i in self.expressionList:
            self.expressionMenu.add_command(label=i)
        self.expressionMenu.bind("<Button-1>", self.expressionClick)
        self.expressionMenu.bind("<Button-3>", self.expressionRightClick)
        self.menuBar.add_cascade(label=ld.expressionWindowName, menu=self.expressionMenu)

        # setup equation menu
        self.equationMenu = tk.Menu(self.menuBar, tearoff=0)
        for i in self.equationList:
            self.equationMenu.add_command(label=i)
        self.equationMenu.bind("<Button-1>", self.equationClick)
        self.equationMenu.bind("<Button-3>", self.equationRightClick)
        self.menuBar.add_cascade(label=ld.equationWindowName, menu=self.equationMenu)

        # setup arm menu
        self.armMenu = tk.Menu(self.menuBar, tearoff=0)
        for i in ld.partList:
            self.armMenu.add_command(label=i)
        self.armMenu.bind("<Button-1>", self.armClick)
        self.menuBar.add_cascade(label=ld.armWindowName, menu=self.armMenu)

        # setup move menu; actual values get added once a part has been selected in the arm menu.
        self.moveMenu = tk.Menu(self.menuBar, tearoff=0)
        self.moveMenu.bind("<Button-1>", self.moveClick)
        self.menuBar.add_cascade(label=ld.movementWindowName, menu=self.moveMenu)

        # setup textbox
        self.textBox = tk.Text(self.window, width=79)
        self.textBox.grid(row=5, columnspan=6)

        # start program loop
        self.window.config(menu=self.menuBar)
        self.window.mainloop()

    def buttonRow(self):
        return (self.buttonNumber.__next__()//2) // self.maxButtons + 2

    def buttonColumn(self):
        return (self.buttonNumber.__next__()//2) % self.maxButtons + 1

    def commandClick(self, event):
        self.commandOptions.set(ld.commandWindowName)
        print("(left)clicked option " + self.commandList[event.y // 22])

    def expressionClick(self, event):
        self.expressionOptions.set(ld.expressionWindowName)
        print("(left)clicked option " + self.expressionList[event.y // 22])

    def expressionRightClick(self, event):
        self.expressionOptions.set(ld.expressionWindowName)
        print(ld.expressionExplanationList[event.y // 22])

    def equationClick(self, event):
        self.equationOptions.set(ld.equationWindowName)
        print("(left)clicked option " + self.equationList[event.y // 22])

    def equationRightClick(self, event):
        self.equationOptions.set(ld.equationWindowName)
        print(ld.equationExplanationList[event.y // 22])

    def setAdvancedMode(self):
        self.commandMenu.delete(0, 'end')
        self.expressionMenu.delete(0, 'end')
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
            self.commandMenu.add_command(label=i)
        for i in self.expressionList:
            self.expressionMenu.add_command(label=i)

    def armClick(self, event):
        self.moveList = []
        self.moveMenu.delete(0, 'end')
        if hasattr(getattr(self.arm, self.arm.partList[event.y//22]).part, "clock"):
            self.moveList = ld.baseMovements
        elif hasattr(getattr(self.arm, self.arm.partList[event.y//22]).part, "open"):
            self.moveList = ld.gripMovements
        elif hasattr(getattr(self.arm, self.arm.partList[event.y//22]).part, "on"):
            self.moveList.append(ld.ledMovement)
        else:
            self.moveList = ld.normalMovements
        self.moveList.append(ld.offMovement)

        for i in self.moveList:
            self.moveMenu.add_command(label=i)

    def moveClick(self, event):
        print("moving " + self.moveList[event.y//22])


interface = Interface()
