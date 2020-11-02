import os
import tkinter as tk
import tkinter.filedialog as filedialog
import GPIOArm
import localisationdata as ld
import configparser


class Interface(object):
    iniReader = configparser.ConfigParser()
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    arm = GPIOArm.Arm()
    window = tk.Tk()

    # lists of menu items
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
    fileName = ""

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
        self.window.title(ld.windowName)

        # setup menu bar
        self.menuBar = tk.Menu(self.window)

        # setup file menu (only decorative except for advanced mode for now)
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        for i in ld.fileMenuList:
            self.fileMenu.add_command(label=i, command=lambda item=i: self.fileClick(item))
        self.fileMenu.add_checkbutton(label=ld.advanced, variable=self.advancedMode, onvalue=1, offvalue=0, command=self.setAdvancedMode)
        self.menuBar.add_cascade(label=ld.fileWindowName, menu=self.fileMenu)

        # setup command menu
        self.commandMenu = tk.Menu(self.menuBar, tearoff=0)
        for i in self.commandList:
            self.commandMenu.add_command(label=i, command=lambda item=i: self.commandClick(item))
        self.menuBar.add_cascade(label=ld.commandWindowName, menu=self.commandMenu)

        # setup expression menu
        self.expressionMenu = tk.Menu(self.menuBar, tearoff=0)
        for i in self.expressionList:
            self.expressionMenu.add_command(label=i, command=lambda item=i: self.expressionClick(item))
        self.menuBar.add_cascade(label=ld.expressionWindowName, menu=self.expressionMenu)

        # setup equation menu
        self.equationMenu = tk.Menu(self.menuBar, tearoff=0)
        for i in self.equationList:
            self.equationMenu.add_command(label=i, command=lambda item=i: self.equationClick(item))
        self.menuBar.add_cascade(label=ld.equationWindowName, menu=self.equationMenu)

        # setup standard function menu
        self.functionMenu = tk.Menu(self.menuBar, tearoff=0)
        for i in self.functionList:
            self.functionMenu.add_command(label=i, command=lambda item=i: self.functionClick(item))
        self.menuBar.add_cascade(label=ld.functionWindowName, menu=self.functionMenu)

        # setup standard function menu
        self.functionMenu2 = tk.Menu(self.menuBar, tearoff=0)
        for i in self.functionList2:
            self.functionMenu2.add_command(label=i, command=lambda item=i: self.function2Click(item))
        self.menuBar.add_cascade(label=ld.functionWindow2Name, menu=self.functionMenu2)

        # setup arm menu
        self.armMenu = tk.Menu(self.menuBar, tearoff=0)
        for i in ld.partList:
            self.armMenu.add_command(label=i, command=lambda item=i: self.armClick(item))
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

    def fileClick(self, item):
        itemId = ld.fileMenuList.index(item)
        if itemId == 0:  # new file
            self.textBox.delete(1.0, tk.END)
        if itemId == 1:  # open file
            self.openFile()
        if itemId == 2:  # save file
            self.saveFile()
        if itemId == 3:  # save as
            self.saveFile(True)

    def openFile(self):
        fileOpenPopup = filedialog.askopenfile(mode="r", initialdir=os.getcwd()+"/saves", initialfile=self.fileName)
        if fileOpenPopup is None:
            return
        self.fileName = fileOpenPopup.name
        file = open(self.fileName, "r")
        self.textBox.delete(1.0, tk.END)
        self.textBox.insert(1.0, file.read())
        file.close()

    def saveFile(self, newName=False):
        if newName | (self.fileName == ""):
            fileSavePopup = filedialog.asksaveasfile(mode="w", initialdir=os.getcwd()+"/saves", initialfile=self.fileName, defaultextension=".py", filetypes=(("python files", "*.py"), ("text files", "*.txt")))
            if fileSavePopup is None:
                return
            self.fileName = fileSavePopup.name
        file = open(self.fileName, "w")
        file.write(self.textBox.get(1.0, tk.END))
        file.close()

    def commandClick(self, item):
        self.textBox.insert(tk.INSERT, item + "():\n\t")
        self.textBox.mark_set(tk.INSERT, tk.END)
        return "break"

    def expressionClick(self, item):
        self.textBox.insert(tk.INSERT, item)
        self.helpText.set(ld.helpInfo + ld.expressionExplanationList[self.expressionList.index(item)])
        return "break"

    def equationClick(self, item):
        self.textBox.insert(tk.INSERT, item)
        self.helpText.set(ld.helpInfo + ld.equationExplanationList[self.equationList.index(item)])
        return "break"

    def functionClick(self, item):
        self.textBox.insert(tk.INSERT, item)
        self.helpText.set(ld.helpInfo + ld.functionExplanationList[self.functionList.index(item)])
        return "break"

    def function2Click(self, item):
        self.textBox.insert(tk.INSERT, item)
        self.helpText.set(ld.helpInfo + ld.functionExplanationList2[self.functionList2.index(item)])
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

    def armClick(self, item):
        self.selectedPart = getattr(self.arm, item)
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
            self.moveMenu.add_command(label=i, command=lambda moveItem=i: self.moveClick(moveItem))
        return "break"

    def moveClick(self, item):
        self.textBox.insert(tk.INSERT, self.selectedPart.name + "." + item + "()")


# interface = Interface()
