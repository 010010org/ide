import tkinter as tk  # used to create the interface
import localisationdata as ld  # contains all displayed text
import configparser  # used to read and write to ini file
import string  # only used to get a list of letters and numbers
import importlib.util


class Interface(object):
    _advancedMode = 0
    _iniWriter = configparser.ConfigParser()

    # Used to call the various libraries
    _libraryArray = []
    _deviceArray = []
    _ldArray = []

    # These are used to iterate through the configured keys and text fields
    _partArray = []
    _keyArray = []

    _entryArray = []

    _rowNumber = 0  # Used to put every option on a new line

    # Tracker to see if the user is editing the keybinds or wants to control the devices
    _editMode = 1

    def __init__(self, parent, advancedMode=0):
        self._window = tk.Frame(parent)
        self._window.title = ld.controlArmOption
        self._advancedMode = advancedMode
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

        for i in self._libraryArray:
            self._iniWriter = configparser.ConfigParser()
            _iniFile = 'lib/' + i + '/controls.ini'
            self._iniWriter.read(_iniFile)
            for j in self._iniWriter:
                if j != "DEFAULT":
                    for k in self._iniWriter[j]:
                        self._partArray.append([i, j, k, self._iniWriter[j][k]])
                        # partArray looks like this:
                        # [device1, part1, direction1, keybind], [device1, part1, direction2, keybind], [device1, part2, ...

        # creates info textbox
        self._warningLabel = tk.Label(self._window, text="")

        # Trackers for timer checkbox and text field
        self._timerMode = tk.IntVar(self._window, value=0)
        self._timerVar = tk.StringVar(self._window, value="0")
        self._timerValue = 0

        # Trackers for power checkbox and text field
        self._powerMode = tk.IntVar(self._window, value=0)
        self._powerVar = tk.StringVar(self._window, value="0")
        self._powerValue = 0

        # Creates an "entry" (editable text field) for every move-action. Also fills in the keys read from the ini file.
        for i in range(len(self._partArray)):
            locLib = self._ldArray[self._libraryArray.index(self._partArray[i][0])]
            self._keyArray.append(tk.StringVar(self._window))
            self._keyArray[i].set(self._partArray[i][3])
            self._keyArray[i].trace_add('write', self.updateEntries)
            tk.Label(self._window, text=self._partArray[i][0] + ": " + locLib.partDictionary[self._partArray[i][1]] + " " + locLib.partDictionary[self._partArray[i][2]]).grid(sticky='w', row=i, column=1)
            self._entryArray.append(tk.Entry(self._window, textvariable=self._keyArray[i], width=2))
            self._entryArray[i].grid(sticky='w', row=i, column=2)
            self._rowNumber = i

        # Adds the save button and info textbox. Refreshes all entry fields and start the main loop.
        self._saveButton = tk.Button(self._window, text=ld.saveButtonText, command=self._saveProgram)
        self._saveButton.grid(sticky='w', row=self._rowNumber + 2, column=1)

        if advancedMode:
            self._window.title = ld.advancedControlArmOption

            # Setup timer options
            self._timerCheckButton = tk.Checkbutton(self._window, text=ld.timerButtonText, variable=self._timerMode, onvalue=1, offvalue=0, command=self.setTimerMode)
            self._timerCheckButton.grid(sticky='w', row=0, column=3)
            self._timerSlider = tk.Scale(self._window, from_=0, to=2000, showvalue=False, state='disabled', command=self.setTimerValue, orient=tk.HORIZONTAL)
            self._timerSlider.grid(row=0, column=4)
            self._timerSlider.bind("<FocusIn>", self.onTimerFocus)
            self._timerSlider.bind("<FocusOut>", self.onFocusLoss)

            # Setup power options
            self._powerCheckButton = tk.Checkbutton(self._window, text=ld.powerButtonText, variable=self._powerMode, onvalue=1, offvalue=0, command=self.setPowerMode)
            self._powerCheckButton.grid(sticky='w', row=1, column=3)
            self._powerSlider = tk.Scale(self._window, from_=30, to=100, showvalue=False, state='disabled', command=self.setPowerValue, orient=tk.HORIZONTAL)
            self._powerSlider.grid(row=1, column=4)

            # adds stop button
            self._stopButton = tk.Button(self._window, text=ld.stopButtonText, command=self._stopProgram)
            self._stopButton.grid(sticky='w', row=self._rowNumber + 2, column=2)
            self._stopButton['state'] = tk.DISABLED

            # put warninglabel under power and timer button
            self._warningLabel.grid(sticky='w', row=2, column=3, columnspan=3)
        else:
            self._warningLabel.grid(sticky='w', row=self._rowNumber + 3, column=1, columnspan=3)

        self.updateEntries()
        self._window.grid(row=0, column=0)

    # Activate the timer entry field if the checkbox is checked, disable when unchecked.
    def setTimerMode(self):
        if self._timerMode.get():
            self._timerSlider.configure(state='normal')
        else:
            self._timerSlider.configure(state='disabled')

    # Activate the power entry field if the checkbox is checked, disable when unchecked.
    def setPowerMode(self):
        if self._powerMode.get():
            self._powerSlider.configure(state='normal')
        else:
            self._powerSlider.configure(state='disabled')

    # Sets the timer value. If a character is added that isn't a number or a decimal point, it is removed.
    def setTimerValue(self, value):
        try:
            self._timerValue = int(value)/1000
        except ValueError:
            print("How did you do that?")
            return

    # Sets the power value. If a character is added that isn't a number or a decimal point, it is removed. Rounds down to whole numbers.
    def setPowerValue(self, value):
        try:
            self._powerValue = int(value)
        except ValueError:
            print("How did you do that?")
            return  # Should never happen

    # Displays help info if the timer entry field is clicked.
    def onTimerFocus(self, *_args):
        self._warningLabel.config(text=ld.timerInfo)

    # Removes help info when user clicks away from timer entry field.
    def onFocusLoss(self, *_args):
        self._warningLabel.config(text="")

    # Updates the list of assigned keys. If an entry field contains multiple characters, all but the first one are removed.
    # Gives a warning if the same key is used multiple times.
    def updateEntries(self, *_args):
        _stringKeyArray = []
        for i in self._keyArray:
            _stringKeyArray.append(i.get())
            if len(i.get()) > 1:
                i.set(i.get()[0])
        if len(self._keyArray) != len(set(_stringKeyArray)):
            self._warningLabel.config(text=ld.duplicatesWarning)
        else:
            self._warningLabel.config(text="")

    # Starts controlling controlling the robotic arm.
    def _saveProgram(self):
        # Removes all possible keybinds in case they were changed.
        for i in string.printable:
            self._window.master.unbind('<' + i + '>')
            self._window.master.unbind('<KeyRelease-' + i + '>')
        if self._editMode:
            # Writes the keys the user selected to the array of configured keys.
            for i in range(len(self._keyArray)):
                self._partArray[i][3] = self._keyArray[i].get()

            # Writes the keys to the ini file to save them for the next time the program is started
            _device = ""
            _iniFile = "temp.ini"
            self._iniWriter = configparser.ConfigParser()
            for i in self._partArray:
                if i[0] != _device:
                    if _device == "":
                        self._iniWriter = configparser.ConfigParser()
                        self._iniWriter.read("lib/"+i[0]+"/controls.ini")
                    if _device != "":
                        _iniFile = "lib/"+_device+"/controls.ini"
                        with open(_iniFile, 'w') as configFile:
                            self._iniWriter.write(configFile, space_around_delimiters=False)
                        self._iniWriter = configparser.ConfigParser()
                        self._iniWriter.read("lib/" + i[0] + "/controls.ini")
                    _device = i[0]
                self._iniWriter[i[1]][i[2]] = i[3]
            _iniFile = "lib/"+self._partArray[-1][0]+"/controls.ini"
            with open(_iniFile, 'w') as configFile:
                self._iniWriter.write(configFile)

            # Adds events to the specified keys. This is ugly code, see the explanation below.
            for i in self._partArray:
                self._window.master.bind('<' + i[3] + '>', lambda event=None, device=self._deviceArray[self._libraryArray.index(i[0])], part=i[1], direction=i[2]: self._keyPressed(device, part, direction, power=self._powerMode.get()*self._powerValue, timer=self._timerMode.get()*self._timerValue))
                self._window.master.bind('<KeyRelease-' + i[3] + '>', lambda event=None, device=self._deviceArray[self._libraryArray.index(i[0])], part=i[1]: self._keyPressed(device, part, direction='off'))
            # i[3] is the key in question. We bind an event to it that runs the code written after "lambda" when the key is pressed.
            # event is used to ignore the useless data tkinter sends us without us asking for it.
            # device is the class used for the device that needs to be controlled, robotArm.Arm for example.
            # part and direction are the part and direction the specified key needs to control.
            # getattr() allows us to turn a piece of text into code. For example, if device = robotArm and part = "base", getattr(device, part) would return robotArm.Arm.base
            # doing this twice (with direction = "counter", for example), we get getattr(getattr(device, part), direction), which would return robotArm.Arm.base.counter
            # the next part adds the power and timer data. Since these function the same, I'll use power to explain:
            # self.powerMode.get() returns the state if our checkbox. if it's checked, it returns a 1. If it's unchecked, it returns a 0.
            # self.powerValue returns the number the user added to the entry field.
            # By multiplying these two, we are only sending the data if the checkbox is checked, and 0 if it's unchecked.

            # disables editing the controls after saving
            for i in self._entryArray:
                i['state'] = tk.DISABLED
            if self._advancedMode:
                self._timerCheckButton['state'] = tk.DISABLED
                self._timerSlider['state'] = tk.DISABLED
                self._powerCheckButton['state'] = tk.DISABLED
                self._powerSlider['state'] = tk.DISABLED
            # enables the stop button
                self._stopButton['state'] = tk.NORMAL

            # Changes the Save button to now be an Edit button
            self._saveButton['text'] = ld.editButtonText
        else:
            for i in self._entryArray:
                i['state'] = tk.NORMAL
            if self._advancedMode:
                self._timerCheckButton['state'] = tk.NORMAL
                self._powerCheckButton['state'] = tk.NORMAL
                if self._timerMode:
                    self._timerSlider['state'] = tk.NORMAL
                if self._powerMode:
                    self._powerSlider['state'] = tk.NORMAL
                self._stopButton['state'] = tk.DISABLED

            # Changes the button text back to 'Save'
            self._saveButton['text'] = ld.saveButtonText

        # Switches from save mode to edit mode
        self._editMode ^= 1

    def _keyPressed(self, device, part, direction, power=0, timer=0):
        if direction == 'off':
            (getattr(getattr(device, part), direction))
            return
        (getattr(getattr(device, part), direction)(power=power))
        if timer:
            self._window.after(int(1000*timer), (getattr(getattr(device, part), 'off')))

    def _stopProgram(self):
        # Removes all keybinds
        for i in string.printable:
            self._window.master.unbind('<' + i + '>')
            self._window.master.unbind('<KeyRelease-' + i + '>')

        # Turns every part of every device off.
        for i in self._partArray:
            getattr(getattr(self._deviceArray[self._libraryArray.index(i[0])], i[1]), 'off')()
