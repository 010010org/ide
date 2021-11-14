import tkinter as tk  # Used to create interface
import localisationdata as ld  # Contains translated strings for selected language
import os.path  # Used to check if pinout inis still exist
import configparser  # Used to read pinout inis
import string  # Only used for string.digits, which is "0123456789"


class Interface(object):
    _libraryList = []
    _pinoutList = []
    _entryList = []
    _entryCounter = 0

    def __init__(self, parent, libraryList):
        # Create configparser
        self._iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self._iniWriter.optionxform = str
        self._iniFile = None
        # Creating interface
        self._parent = parent
        self._window = tk.Frame(parent)
        self._libraryList = libraryList
        self._getPinouts()
        tk.Label(self._window, text=ld.pinoutTextbox).grid(row=0, column=1, columnspan=4, sticky='w')
        tk.Label(self._window, text=ld.pinoutTextbox2).grid(row=1, column=1, columnspan=4, sticky='w')
        rowNumber = 0
        self._entryList = []
        for i in range(len(self._pinoutList)):
            tk.Label(self._window, text=self._pinoutList[i][0]+': '+self._pinoutList[i][1]).grid(row=2+i, column=1, columnspan=1, sticky='w')
            for j in range(len(self._pinoutList[i][2].split(','))):
                self._entryList.append([j, tk.StringVar(self._window)])
                self._entryList[self._entryCounter][1].set(self._pinoutList[i][2].split(',')[j])
                self._entryList[self._entryCounter][1].trace_add('write', self._updateEntries)
                tk.Entry(self._window, textvariable=self._entryList[self._entryCounter][1]).grid(row=2+i, column=2+j, columnspan=1, sticky='w')
                self._entryCounter += 1
            rowNumber = i
        tk.Button(self._window, text=ld.pinoutButton, command=self._saveSettings).grid(row=3+rowNumber, column=1, columnspan=1, sticky='w')
        tk.Button(self._window, text=ld.resetButton, command=self._resetClick).grid(row=3+rowNumber, column=2, columnspan=1, sticky='w')
        self._warningLabel = tk.Label(self._window, text="")
        self._warningLabel.grid(row=3+rowNumber, column=3, columnspan=3, sticky='w')
        self._window.grid(row=0, column=0)

    # Runs through al libraries and collects the pinouts each of them require.
    def _getPinouts(self):
        self._iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self._iniWriter.optionxform = str
        self._pinoutList = []
        for i in self._libraryList:
            self._iniFile = "lib/" + i + "/pinout.ini"
            if os.path.isfile(self._iniFile):
                self._iniWriter.read(self._iniFile)
            else:
                print("pinout.ini for " + i + " library somehow disappeared while the program was running.")  # Freak error, should never happen unless user deletes the file on purpose while the program is running.
        for j in self._iniWriter:
            for k in self._iniWriter[j]:
                self._pinoutList.append([j, k, self._iniWriter[j][k]])

    # This code runs when one of the entries is changed.
    # If a number over 27, a character that isn't a number, or the number 0 is entered, the last character gets removed.
    # 27 is the number of GPIO pins the pi has, starting with 1, so it wouldn't make sense for something else to be entered.
    # If a duplicate number gets entered, a warning is shown.
    def _updateEntries(self, *_args):
        previousEntry = ""
        tempList = []
        entryStringArray = []
        for i in self._entryList:
            entryStringArray.append(i[1].get())
            if len(i[1].get()) > 0:
                if i[1].get()[-1] not in string.digits:
                    i[1].set(i[1].get()[:-1])
                if int(i[1].get()) > 27:
                    i[1].set(i[1].get()[:-1])
                if int(i[1].get()) == 0:
                    i[1].set(i[1].get()[:-1])
            if i[0] == 0:
                if previousEntry != "":
                    tempList.append(previousEntry)
                previousEntry = i[1].get()
            if i[0] >= 1:
                previousEntry += ',' + i[1].get()
        tempList.append(previousEntry)
        for i in range(len(tempList)):
            self._pinoutList[i][2] = tempList[i]
        if len(self._entryList) > len(set(entryStringArray)):
            self._warningLabel.config(text=ld.duplicatesWarning)
        else:
            self._warningLabel.config(text="")

    # Saves changed pinout to ini files.
    def _saveSettings(self):
        folder = ""
        for i in self._pinoutList:
            if i[0] != folder:
                if folder == "":
                    self._iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
                    self._iniWriter.optionxform = str
                    self._iniWriter.read("lib/" + i[0] + "/pinout.ini")
                if folder != "":
                    self._iniFile = "lib/" + folder + "/pinout.ini"
                    with open(self._iniFile, 'w') as configFile:
                        self._iniWriter.write(configFile, space_around_delimiters=False)
                    self._iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
                    self._iniWriter.optionxform = str
                    self._iniWriter.read("lib/" + i[0] + "/pinout.ini")
                folder = i[0]
            self._iniWriter[folder][i[1]] = i[2]
        self._iniFile = "lib/" + self._pinoutList[-1][0] + "/pinout.ini"
        with open(self._iniFile, 'w') as configFile:
            self._iniWriter.write(configFile, space_around_delimiters=False)
        self._window.destroy()
        import setupSimulation
        setupSimulation.Interface(self._parent, self._libraryList)

    # Reads pinouts from default file and restores them, closes window.
    def _resetClick(self):
        for i in self._libraryList:
            self._iniFile = "lib/" + i + "/defaultPinout.ini"
            self._iniWriter.read(self._iniFile)
            self._iniFile = "lib/" + i + "/pinout.ini"
            with open(self._iniFile, 'w') as configFile:
                self._iniWriter.write(configFile, space_around_delimiters=False)
        self._getPinouts()
        self._window.destroy()
        #TO-DO make changes visible? instead of going straight to the next window
        import setupSimulation
        setupSimulation.Interface(self._parent, self._libraryList)
