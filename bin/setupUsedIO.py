import tkinter as tk
import os
import configparser


class Interface (object):
    _window = tk.Tk()

    _iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
    _iniWriter.optionxform = str
    _iniFile = "config.ini"

    def __init__(self):
        libraryList = self._updateINI()
        self._window.mainloop()

    def _updateINI(self):

        realLibraryList = []
        iniLibraryList = []
        for i in os.listdir(path="lib"):
            realLibraryList.append(i)
        self._iniWriter.read(self._iniFile)
        for i in self._iniWriter["LIBRARIES"]:
            iniLibraryList.append(i)
        for i in realLibraryList:
            if i not in iniLibraryList:
                iniLibraryList.append(i)
                self._iniWriter["LIBRARIES"][i] = 0
        for i in iniLibraryList:
            if i not in realLibraryList:
                self._iniWriter.remove_option("LIBRARIES", i)
        with open(self._iniFile, 'w') as configFile:
            self._iniWriter.write(configFile, space_around_delimiters=False)
        return iniLibraryList
