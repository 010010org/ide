import tkinter as tk
import localisationdata as ld
import configparser


class Interface(object):
    iniReader = configparser.ConfigParser()
    window = tk.Tk()
    partArray = []
    keyArray = []
    entryArray = []

    def __init__(self):
        self.iniReader.read('bin/armControls.ini')
        for i in self.iniReader:
            if i != "DEFAULT":
                for j in self.iniReader[i]:
                    self.partArray.append([i, j, self.iniReader[i][j]])
        print(self.partArray)
        for i in range(len(self.partArray)):
            self.keyArray.append(tk.StringVar(self.window))
            self.keyArray[i].set(self.partArray[i][2])
            tk.Label(self.window, text=self.partArray[i][0]+" "+self.partArray[i][1]).grid(row=i, column=1)
            tk.Entry(self.window, textvariable=self.keyArray[i]).grid(row=i, column=2)
        startButton = tk.Button(self.window, text=ld.startButtonText, command=self.startProgram).grid(row=i+1, column=1)
        self.window.mainloop()

    def startProgram(self):
        import pyGameArm
        self.window.destroy()
