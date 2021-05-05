import os  # Used to get working directory (needed to save/open files)
import tkinter as tk  # Used for interface
import tkinter.filedialog as filedialog  # Used for open/save as... interfaces
import tkinter.scrolledtext as scrolledtext  # Used for the textbox
import tkinter.font as font  # Used for syntax highlighting (specifically for bold and italic text)

import localisationdata as ld  # Contains translated strings for selected language
import configparser  # Used to read ini file (to see which libraries we need to use)
import importlib.util  # Used to import our libraries

from pygments.lexers.python import PythonLexer  # Needed for syntax highlighting
from pygments.styles import get_style_by_name  # idem


class Interface(object):
    SCREEN_WIDTH = 640  # int(window.winfo_screenwidth())
    SCREEN_HEIGHT = 480  # int(window.winfo_screenheight())

    _libraryArray = []
    _ldArray = []
    _deviceArray = []
    advancedMode = 0

    # lists of menu items (not all of these are used)
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

    fileName = ""
    fullScreen = 0

    def __init__(self, parent):
        self.lexer = PythonLexer()  # Used for syntax highlighting
        self._window = tk.Frame(parent)
        self.helpText = tk.StringVar(self._window)

        # setup window
        self._window.master.geometry(str(self.SCREEN_WIDTH) + "x" + str(self.SCREEN_HEIGHT))
        if self.fullScreen:
            self._window.master.attributes("-fullscreen", True)
        self._window.bind("<F11>", self.swapFullScreen)
        self._window.master.title(ld.windowName)

        # setup library imports (and localisation data of those libraries)
        #same as tkControllerface.py __init__
        libReader = configparser.ConfigParser()
        libReader.optionxform = str
        configIni = "config.ini"
        libReader.read(configIni)
        for i in libReader["LIBRARIES"]:
            if libReader["LIBRARIES"][i] == "1":
                self._libraryArray.append(i)
                module_name = i
                file_path = "lib/" + i + "/" + i + ".py"
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                ld_module_name = i + "Localisationdata"
                ld_file_path = "lib/" + i + "/" + ld_module_name + ".py"
                ld_spec = importlib.util.spec_from_file_location(ld_module_name, ld_file_path)
                ld_module = importlib.util.module_from_spec(ld_spec)
                ld_spec.loader.exec_module(ld_module)
                self._ldArray.append(ld_module)
                for objname in dir(module):
                    if type(eval("module." + objname)) is type:
                        self._deviceArray.append(getattr(module, objname)())

        # setup menu bar
        self.menuBar = tk.Menu(self._window)

        # setup file menu
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

        # setup device menu
        # basically, this code imports all selected libraries, checks their code for all public variables (i.e. instances of parts),
        # checks those instance variables for all public methods (i.e. movement directions),
        # translates all names and organises all this data neatly in a cascading menu.
        self.deviceMenu = tk.Menu(self.menuBar, tearoff=0)
        for libraryCounter in range(len(self._libraryArray)):
            library = self._libraryArray[libraryCounter]
            device = self._deviceArray[libraryCounter]
            locData = self._ldArray[libraryCounter]
            specificPartMenu = tk.Menu(self.deviceMenu, tearoff=0)
            for part in vars(device):
                if not part.startswith('_'):
                    specificMoveMenu = tk.Menu(specificPartMenu, tearoff=0)
                    partPointer = getattr(device, part)
                    for movement in dir(partPointer):
                        if callable(getattr(partPointer, movement)) and not movement.startswith("_"):
                            specificMoveMenu.add_command(label=locData.partDictionary[movement], command=lambda lib_=library, device_=device, part_=part, move_=movement: self.moveClick(lib_, device_, part_, move_))
                    specificPartMenu.add_cascade(label=locData.partDictionary[part], menu=specificMoveMenu)
            self.deviceMenu.add_cascade(label=library, menu=specificPartMenu)
        self.menuBar.add_cascade(label=ld.connectedDeviceWindowName, menu=self.deviceMenu)

        # setup textbox
        self.textBox = scrolledtext.ScrolledText(self._window, width=self.SCREEN_WIDTH // 8 - 3, height=self.SCREEN_HEIGHT // 20)
        self.textBox.grid(row=2, columnspan=6)

        # setup run button
        self.runButton = tk.Button(self._window, text=ld.runButtonText, command=self.runCode)
        self.runButton.grid(row=3, sticky='w')

        # setup help text
        self.helpText.set(ld.helpInfo+ld.helpInfoDefault)
        self.helpLabel = tk.Label(self._window, textvar=self.helpText)
        self.helpLabel.grid(sticky=tk.W, row=4, column=0, columnspan=6)

        # start program loop
        self._window.master.config(menu=self.menuBar)
        self._window.grid(row=0, column=0)
        self._window.master.bind("<KeyRelease-Return>", self.recolorize)

    # Toggles fullscreen
    def swapFullScreen(self, *_args):
        self.fullScreen ^= 1
        if self.fullScreen:
            self._window.master.attributes("-fullscreen", True)
        else:
            self._window.master.attributes("-fullscreen", False)

    # Setup what happens when file menu is clicked
    def fileClick(self, item):
        itemId = ld.fileMenuList.index(item)
        if itemId == 0:  # new file
            self.textBox.delete(1.0, tk.END)
            self.fileName = ""
        if itemId == 1:  # open file
            self.openFile()
        if itemId == 2:  # save file
            self.saveFile()
        if itemId == 3:  # save as
            self.saveFile(True)

    # Run the code in the textbox
    def runCode(self):
        exec(self.textBox.get("1.0", tk.END))

    # Open a file
    def openFile(self):
        # Shows file selection popup
        fileOpenPopup = filedialog.askopenfile(parent=self._window, mode="r", initialdir=os.getcwd() + "/saves")
        if fileOpenPopup is None:
            return
        # Opens file to textbox. Old data gets deleted.
        self.fileName = fileOpenPopup.name
        file = open(self.fileName, "r")
        self.textBox.delete(1.0, tk.END)
        self.textBox.insert(1.0, file.read())
        file.close()
        self.recolorize()

    # Saves the file
    def saveFile(self, newName=False):
        # If the file isn't named yet or "Save as..." is clicked, the user gets a popup to choose a filename and location.
        if newName | (self.fileName == ""):
            fileSavePopup = filedialog.asksaveasfile(parent=self._window, mode="w", initialdir=os.getcwd() + "/saves", defaultextension=".py", filetypes=(("python files", "*.py"), ("text files", "*.txt")))
            if fileSavePopup is None:
                return
            self.fileName = fileSavePopup.name
        # Saves textbox to that file
        file = open(self.fileName, "w")
        file.write(self.textBox.get(1.0, tk.END))
        file.close()

    # Setup what happens when command menu is clicked
    def commandClick(self, item):
        startIndex = self.textBox.index(tk.INSERT)
        tabCheckString = self.textBox.get(str(float(startIndex) // 1), startIndex)
        tabCount = tabCheckString.count("\t")
        self.textBox.insert(tk.INSERT, item)
        if item != "else":
            self.textBox.insert(tk.INSERT, "()")
        self.textBox.insert(tk.INSERT, ":\n\t")
        for i in range(tabCount):
            self.textBox.insert(tk.INSERT, "\t")
        if item != "else":
            self.textBox.mark_set(tk.INSERT, startIndex.split(".")[0] + "." + str(int(startIndex.split(".")[1])+len(item)+1))
        return "break"

    # Setup what happens when expression menu is clicked
    def expressionClick(self, item):
        self.textBox.insert(tk.INSERT, item)
        self.helpText.set(ld.helpInfo + ld.expressionExplanationList[self.expressionList.index(item)])
        return "break"

    # Setup what happens when equation menu is clicked
    def equationClick(self, item):
        self.textBox.insert(tk.INSERT, item)
        self.helpText.set(ld.helpInfo + ld.equationExplanationList[self.equationList.index(item)])
        return "break"

    # Setup what happens when regular function menu is clicked
    def functionClick(self, item):
        startIndex = self.textBox.index(tk.INSERT)
        self.textBox.insert(tk.INSERT, item+"\n")
        self.helpText.set(ld.helpInfo + ld.functionExplanationList[self.functionList.index(item)])
        self.recolorize()
        self.textBox.mark_set(tk.INSERT, startIndex.split(".")[0] + "." + str(int(startIndex.split(".")[1])+len(item)-1))
        return "break"

    # Setup what happens when external function menu is clicked
    def function2Click(self, item):
        self.textBox.insert("1.0", "import " + item.split(".")[0]+"\n")
        self.textBox.insert(tk.INSERT, item)
        self.helpText.set(ld.helpInfo + ld.functionExplanationList2[self.functionList2.index(item)])
        return "break"

    # Sets up advanced mode
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

    # Setup what happens when move menu is clicked: prints selected part and direction to textbox as one would use it in code.
    def moveClick(self, library, device, part, movement):
        if "import " + library not in self.textBox.get("1.0", tk.END):
            self.textBox.insert("1.0", "import " + library + "\n")
            self.textBox.insert(tk.INSERT, type(device).__name__.lower() + " = " + library + "." + type(device).__name__ + "()\n")
        self.textBox.insert(tk.INSERT, type(device).__name__.lower() + "." + part + "." + movement + "()\n")
        self.recolorize()

    # Syntax highlighting code. Changes pieces of code to bold/italic according to the style sheet.
    def create_tags(self):
        bold_font = font.Font(self.textBox, self.textBox.cget("font"))
        bold_font.configure(weight=font.BOLD)

        italic_font = font.Font(self.textBox, self.textBox.cget("font"))
        italic_font.configure(slant=font.ITALIC)

        bold_italic_font = font.Font(self.textBox, self.textBox.cget("font"))
        bold_italic_font.configure(weight=font.BOLD, slant=font.ITALIC)

        style = get_style_by_name('colorful')
        for ttype, ndef in style:
            tag_font = None
            if ndef['bold'] and ndef['italic']:
                tag_font = bold_italic_font
            elif ndef['bold']:
                tag_font = bold_font
            elif ndef['italic']:
                tag_font = italic_font

            if ndef['color']:
                foreground = "#%s" % ndef['color']
            else:
                foreground = None

            self.textBox.tag_configure(str(ttype), foreground=foreground, font=tag_font)

    # Syntax highlighting code. Changes color of pieces of code specified in style sheet.
    def recolorize(self, _event=None):
        self.create_tags()
        code = self.textBox.get("1.0", "end-1c")
        tokensource = self.lexer.get_tokens(code)

        start_line = 1
        start_index = 0
        end_line = 1
        end_index = 0
        for ttype, value in tokensource:
            if "\n" in value:
                end_line += value.count("\n")
                end_index = len(value.rsplit("\n", 1)[1])
            else:
                end_index += len(value)

            if value not in (" ", "\n"):
                index1 = "%s.%s" % (start_line, start_index)
                index2 = "%s.%s" % (end_line, end_index)

                for tagname in self.textBox.tag_names(index1):
                    self.textBox.tag_remove(tagname, index1, index2)
                self.textBox.tag_add(str(ttype), index1, index2)

            start_line = end_line
            start_index = end_index
