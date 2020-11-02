import tkinter as tk
import localisationdata as ld
import configparser
import GPIOArm
import string


class Interface(object):
    _arm = GPIOArm.Arm()
    iniWriter = configparser.ConfigParser()
    iniFile = 'bin/armControls.ini'
    window = tk.Tk()
    partArray = []
    keyArray = []
    entryArray = []
    rowNumber = 0
    maxEntryLength = 1
    warningLabel = tk.Label(window, text="")
    timerMode = tk.IntVar(window, value=0)
    timerVar = tk.StringVar(window, value="0")
    timerValue = 0
    powerMode = tk.IntVar(window, value=0)
    powerVar = tk.StringVar(window, value="0")
    powerValue = 0

    def __init__(self):
        # Read controls from ini
        self.iniWriter.read(self.iniFile)
        for i in self.iniWriter:
            if i != "DEFAULT":
                for j in self.iniWriter[i]:
                    self.partArray.append([i, j, self.iniWriter[i][j]])

        # Setup controls
        for i in range(len(self.partArray)):
            self.keyArray.append(tk.StringVar(self.window))
            self.keyArray[i].set(self.partArray[i][2])
            self.keyArray[i].trace_add('write', self.updateEntries)
            tk.Label(self.window, text=self.partArray[i][0]+" "+self.partArray[i][1]).grid(row=i, column=1)
            tk.Entry(self.window, textvariable=self.keyArray[i]).grid(row=i, column=2)
            self.rowNumber = i

        # Setup timer options
        self.timerCheckButton = tk.Checkbutton(self.window, text=ld.timerButtonText, variable=self.timerMode, onvalue=1, offvalue=0, command=self.setTimerMode)
        self.timerCheckButton.grid(sticky='w', row=0, column=3)
        self.timerEntry = tk.Entry(self.window, textvariable=self.timerVar, state='disabled')
        self.timerEntry.grid(row=0, column=4)
        self.timerEntry.bind("<FocusIn>", self.onTimerFocus)
        self.timerEntry.bind("<FocusOut>", self.onFocusLoss)
        self.timerVar.trace('w', self.setTimerValue)

        # Setup power options
        self.powerCheckButton = tk.Checkbutton(self.window, text=ld.powerButtonText, variable=self.powerMode, onvalue=1, offvalue=0, command=self.setPowerMode)
        self.powerCheckButton.grid(sticky='w', row=1, column=3)
        self.powerEntry = tk.Entry(self.window, textvariable=self.powerVar, state='disabled')
        self.powerEntry.grid(row=1, column=4)
        self.powerEntry.bind("<FocusIn>", self.onPowerFocus)
        self.powerEntry.bind("<FocusOut>", self.onFocusLoss)
        self.powerVar.trace('w', self.setPowerValue)

        self.startButton = tk.Button(self.window, text=ld.startButtonText, command=self.startProgram).grid(sticky='w', row=self.rowNumber+2, column=1, columnspan=2)
        self.warningLabel.grid(sticky='w', row=self.rowNumber+3, column=1, columnspan=2)
        self.updateEntries()
        self.window.mainloop()

    def setTimerMode(self):
        if self.timerMode.get():
            self.timerEntry.configure(state='normal')
        else:
            self.timerEntry.configure(state='disabled')

    def setTimerValue(self, *_args):
        try:
            self.timerValue = float(self.timerVar.get())
        except ValueError:
            if len(self.timerVar.get()) < 1:
                return
            else:
                self.timerVar.set(self.timerVar.get()[:-1])

    def onTimerFocus(self, *_args):
        self.warningLabel.config(text=ld.timerInfo)

    def setPowerMode(self):
        if self.powerMode.get():
            self.powerEntry.configure(state='normal')
        else:
            self.powerEntry.configure(state='disabled')

    def setPowerValue(self, *_args):
        try:
            self.powerValue = int(self.powerVar.get())//25
        except ValueError:
            if len(self.powerVar.get()) < 1:
                return
            else:
                self.powerVar.set(self.powerVar.get()[:-1])

    def onPowerFocus(self, *_args):
        self.warningLabel.config(text=ld.powerInfo)

    def onFocusLoss(self, *_args):
        self.warningLabel.config(text="")

    def updateEntries(self, *_args):
        stringKeyArray = []
        for i in self.keyArray:
            stringKeyArray.append(i.get())
            if len(i.get()) > self.maxEntryLength:
                i.set(i.get()[0])
        if len(self.keyArray) != len(set(stringKeyArray)):
            self.warningLabel.config(text=ld.duplicatesWarning)
        else:
            self.warningLabel.config(text="")

    def startProgram(self):
        for i in string.ascii_letters+string.digits:
            self.window.unbind('<'+i[0]+'>')
            self.window.unbind('<KeyRelease-'+i[0]+'>')
        for i in range(len(self.keyArray)):
            self.partArray[i][2] = self.keyArray[i].get()
        for i in self.partArray:
            self.iniWriter[i[0]][i[1]] = i[2]
        with open(self.iniFile, 'w') as configFile:
            self.iniWriter.write(configFile)
        for i in self.partArray:
            self.window.bind('<'+i[2]+'>', lambda event=None, part=i[0], direction=i[1]: (getattr(getattr(self._arm, part), direction)(self.powerMode.get()*self.powerValue, self.timerMode.get()*self.timerValue)))
            self.window.bind('<KeyRelease-'+i[2]+'>', lambda event=None, part=i[0]: (getattr(getattr(self._arm, part), 'off')()))
