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

    def __init__(self):
        self.iniWriter.read(self.iniFile)
        for i in self.iniWriter:
            if i != "DEFAULT":
                for j in self.iniWriter[i]:
                    self.partArray.append([i, j, self.iniWriter[i][j]])
        for i in range(len(self.partArray)):
            self.keyArray.append(tk.StringVar(self.window))
            self.keyArray[i].set(self.partArray[i][2])
            self.keyArray[i].trace_add('write', self.testDuplicates)
            tk.Label(self.window, text=self.partArray[i][0]+" "+self.partArray[i][1]).grid(row=i, column=1)
            tk.Entry(self.window, textvariable=self.keyArray[i]).grid(row=i, column=2)
            self.rowNumber = i
        startButton = tk.Button(self.window, text=ld.startButtonText, command=self.startProgram).grid(sticky='w', row=self.rowNumber+1, column=1, columnspan=2)
        self.warningLabel.grid(sticky='w', row=self.rowNumber+2, column=1, columnspan=2)
        self.testDuplicates()
        self.window.mainloop()

    def testDuplicates(self, *_args):
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
            self.window.bind('<'+i[2]+'>', lambda x: getattr(getattr(self._arm, i[0]), i[1])())
            self.window.bind('<KeyRelease-'+i[2]+'>', lambda y: getattr(getattr(self._arm, i[0]), 'off')())
