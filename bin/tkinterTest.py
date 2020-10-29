import tkinter as tk
import GPIOArm
import localisationdata as ld
import configparser


class Interface(object):
    iniReader = configparser.ConfigParser()
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    arm = GPIOArm.Arm()
    window = tk.Tk()
    commandList = ["if", "elif", "else", "for", "while"]
    advancedCommandList = ["break", "continue"]
    expressionList = ["+", "-", "*", "/", "//", "%", "**"]
    advancedExpressionList = ["<<", ">>", "|", "^", "&", "~", "@"]
    equationList = ["==", "!=", "<", "<=", ">", ">="]
    advancedEquationList = ["is", "is not", "in", "not in"]
    functionList = ["print()", "input()", "str()", "int()", "float()", "round()", "range()", "len()", "min()", "max()"]
    functionList2 = ["time.sleep()", "time.time()", "random.random()", "random.randint()"]
    logicGateList = ["AND", "OR", "XOR", "NOT"]
    advancedLogicGateList = ["NAND", "NOR", "XNOR"]
    variableList = ["i", "j", "k", "l"]
    selectedPart = None
    moveList = []
    helpText = tk.StringVar(window)
    tipWindow = None

    def __init__(self):
        # read state of advanced mode and implement if needed
        self.iniReader.read('config.ini')
        self.advancedMode = int(self.iniReader['OPTIONS']['ADVANCED_MODE'])
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

        # setup standard function menu
        self.functionMenu = tk.Menu(self.menuBar, tearoff=0)
        for i in self.functionList:
            self.functionMenu.add_command(label=i)
        self.functionMenu.bind("<Button-1>", self.functionClick)
        self.functionMenu.bind("<Button-3>", self.functionRightClick)
        self.menuBar.add_cascade(label=ld.functionWindowName, menu=self.functionMenu)

        # setup standard function menu
        self.functionMenu2 = tk.Menu(self.menuBar, tearoff=0)
        for i in self.functionList2:
            self.functionMenu2.add_command(label=i)
        self.functionMenu2.bind("<Button-1>", self.function2Click)
        self.functionMenu2.bind("<Button-3>", self.function2RightClick)
        self.menuBar.add_cascade(label=ld.functionWindow2Name, menu=self.functionMenu2)

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
        self.textBox.grid(row=2, columnspan=6)

        # setup help text
        self.helpText.set(ld.helpInfo+ld.helpInfoDefault)
        self.helpLabel = tk.Label(self.window, textvar=self.helpText)
        self.helpLabel.grid(sticky=tk.W, row=3, column=0, columnspan=6)

        # start program loop
        self.window.config(menu=self.menuBar)
        self.window.mainloop()

    def commandClick(self, event):
        self.textBox.insert(tk.INSERT, self.commandList[event.y // 22] + "():\n\t")
        self.textBox.mark_set(tk.INSERT, tk.END)
        return "break"

    def expressionClick(self, event):
        self.textBox.insert(tk.INSERT, self.expressionList[event.y // 22])
        self.helpText.set(ld.helpInfo + ld.expressionExplanationList[event.y // 22])
        return "break"

    def expressionRightClick(self, event):
        self.helpText.set(ld.helpInfo + ld.expressionExplanationList[event.y // 22])
        return "break"

    def equationClick(self, event):
        self.textBox.insert(tk.INSERT, self.equationList[event.y // 22])
        self.helpText.set(ld.helpInfo + ld.equationExplanationList[event.y // 22])
        return "break"

    def equationRightClick(self, event):
        self.helpText.set(ld.helpInfo + ld.equationExplanationList[event.y // 22])
        return "break"

    def functionClick(self, event):
        self.textBox.insert(tk.INSERT, self.functionList[event.y // 22])
        self.helpText.set(ld.helpInfo + ld.functionExplanationList[event.y // 22])
        return "break"

    def functionRightClick(self, event):
        self.helpText.set(ld.helpInfo + ld.functionExplanationList[event.y // 22])
        return "break"

    def function2Click(self, event):
        self.textBox.insert(tk.INSERT, self.functionList2[event.y // 22])
        self.helpText.set(ld.helpInfo + ld.functionExplanationList2[event.y // 22])
        return "break"

    def function2RightClick(self, event):
        self.helpText.set(ld.helpInfo + ld.functionExplanationList2[event.y // 22])
        return "break"

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
        self.selectedPart = getattr(self.arm, self.arm.partList[event.y//22])
        self.moveList = []
        self.moveMenu.delete(0, 'end')
        if hasattr(self.selectedPart, "clock"):
            self.moveList = ld.baseMovements
        elif hasattr(self.selectedPart, "open"):
            self.moveList = ld.gripMovements
        elif hasattr(self.selectedPart, "on"):
            self.moveList.append(ld.ledMovement)
        else:
            self.moveList = ld.normalMovements
        self.moveList.append(ld.offMovement)

        for i in self.moveList:
            self.moveMenu.add_command(label=i)
        return "break"

    def moveClick(self, event):
        self.textBox.insert(tk.INSERT, self.selectedPart.name + "." + self.moveList[event.y//22] + "()")


# interface = Interface()
