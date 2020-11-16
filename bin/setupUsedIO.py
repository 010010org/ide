import tkinter as tk
import localisationdata as ld
import os
import configparser


class Interface (object):
    _window = tk.Tk()

    # Open ini file to get list of libraries
    _iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
    _iniWriter.optionxform = str
    _iniFile = "config.ini"

    _infoText = tk.Label(_window, text=ld.infoTextBox)
    _libraryList = []
    _checkBoxList = []

    def __init__(self):
        self._window.title = ld.setupOption
        self._infoText.grid(row=0, column=1)
        self._libraryList = self._updateINI()

        i = 0  # Not needed, but PyCharm complains if removed.
        for i in range(len(self._libraryList)):
            self._checkBoxList.append(tk.IntVar(self._window, value=int(self._iniWriter["LIBRARIES"][self._libraryList[i]])))
            tk.Checkbutton(self._window, text=self._libraryList[i], variable=self._checkBoxList[i], onvalue=1, offvalue=0, command=self._updateCheckbox).grid(row=i+1, column=1, sticky='w')
        self._saveButton = tk.Button(self._window, text=ld.saveButton, command=self._saveData)
        self._saveButton.grid(row=i+2, column=1, sticky='w')

        # Start program.
        self._window.mainloop()

    # Update ini file and return list of installed libraries.
    def _updateINI(self):
        realLibraryList = []
        iniLibraryList = []

        # Look for installed libraries. TODO: test for existence of required files
        for i in os.listdir(path="lib"):
            realLibraryList.append(i)

        # Look for list of libraries in ini file.
        self._iniWriter.read(self._iniFile)
        for i in self._iniWriter["LIBRARIES"]:
            iniLibraryList.append(i)

        # Add new libraries to ini.
        for i in realLibraryList:
            if i not in iniLibraryList:
                iniLibraryList.append(i)
                self._iniWriter["LIBRARIES"][i] = "0"

        # Remove libraries from ini that no longer exist.
        for i in iniLibraryList:
            if i not in realLibraryList:
                self._iniWriter.remove_option("LIBRARIES", i)
                iniLibraryList.remove(i)

        # Save ini file.
        with open(self._iniFile, 'w') as configFile:
            self._iniWriter.write(configFile, space_around_delimiters=False)
        return iniLibraryList

    def _updateCheckbox(self):
        for i in range(len(self._checkBoxList)):
            self._iniWriter["LIBRARIES"][self._libraryList[i]] = str(self._checkBoxList[i].get())

    def _saveData(self):
        with open(self._iniFile, 'w') as configFile:
            self._iniWriter.write(configFile, space_around_delimiters=False)
