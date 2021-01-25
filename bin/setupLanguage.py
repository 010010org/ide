import tkinter as tk  # Used to create interface
import localisationdata as ld  # Contains translated strings for selected language
import os  # Used to get library folders
import os.path  # Used to check if required files exist
import configparser  # Used to read/write ini file


class Interface (object):
    def __init__(self, parent):
        # Open ini file to get list of libraries
        self._iniWriter = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self._iniWriter.optionxform = str
        self._iniFile = "config.ini"
        self._iniWriter.read(self._iniFile)
        self._parent = parent
        self._window = tk.Frame(parent)
        self._window.title = ld.setupOption
        self._languageList = self._updateLangs()
        self._selectedLanguage = self._iniWriter["OPTIONS"]["LANGUAGE"]
        self._languageNumber = 0

        for i in range(len(self._languageList)):
            if self._languageList[i] == self._selectedLanguage:
                self._languageNumber = i

        # Create interface items
        self._infoText = tk.Label(self._window, text=ld.langSelectBox)
        self._infoText.grid(row=0, column=1, sticky='w')
        rownumber = 0
        self._selectedLanguageVar = tk.StringVar(value=self._selectedLanguage)
        for i in range(len(self._languageList)):
            rownumber += 1
            tk.Radiobutton(self._window, text=self._languageList[i], variable=self._selectedLanguageVar, value=self._languageList[i], command=self._updateRadiobuttons).grid(row=rownumber, column=1, sticky='w')
        self._saveButton = tk.Button(self._window, text=ld.saveButton, command=self._saveData)
        rownumber += 1
        self._saveButton.grid(row=rownumber, column=1, sticky='w')

        # Start program.
        self._window.grid(row=0, column=0)

    # Get available languages.
    @staticmethod
    def _updateLangs():
        langList = []

        # Look for available languages.
        for i in os.listdir(path="localisation"):
            if os.path.isfile("localisation/"+i):
                langList.append(str(i).split('.')[0])
        return langList

    # Updates selected language.
    def _updateRadiobuttons(self, *_args):
        self._selectedLanguage = str(self._selectedLanguageVar.get())

    # Saves updated data to ini file. Closes this program and launches setupUsedIO.
    def _saveData(self):
        self._iniWriter["OPTIONS"]["LANGUAGE"] = self._selectedLanguage
        with open(self._iniFile, 'w') as configFile:
            self._iniWriter.write(configFile, space_around_delimiters=False)
        self._window.destroy()
        import setupUsedIO
        setupUsedIO.Interface(self._parent)
        return "break"  # tkinter sometimes seems to require this to function properly.
