import tkinter as tk  # used to create the interface
import localisationdata as ld  # contains all displayed text
import configparser  # used to read and write to ini file
import GPIOArm  # controls the robotic arm
import string  # only used to get a list of letters and numbers


# TODO: create advanced mode to hide timer and power settings behind
class Interface(object):
    # Creates instance of robotarm class to control it.
    _arm = GPIOArm.Arm()

    # opens .ini file containing the controls of the robot arm
    _iniWriter = configparser.ConfigParser()
    _iniFile = 'bin/armControls.ini'

    # opens window to create interface in
    _window = tk.Tk()

    # These are used to iterate through the configured keys and text fields
    _partArray = []
    _keyArray = []

    _rowNumber = 0  # Used to put every option on a new line
    # creates info textbox
    _warningLabel = tk.Label(_window, text="")

    # Trackers for timer checkbox and text field
    _timerMode = tk.IntVar(_window, value=0)
    _timerVar = tk.StringVar(_window, value="0")
    _timerValue = 0

    # Trackers for power checkbox and text field
    _powerMode = tk.IntVar(_window, value=0)
    _powerVar = tk.StringVar(_window, value="0")
    _powerValue = 0

    def __init__(self):
        # Read controls from ini
        self._iniWriter.read(self._iniFile)
        for i in self._iniWriter:
            if i != "DEFAULT":
                for j in self._iniWriter[i]:
                    self._partArray.append([i, j, self._iniWriter[i][j]])
                    # partArray looks like this:
                    # [part1, direction1, keybind], [part1, direction2, keybind], [part2, ...

        # Creates an "entry" (editable text field) for every move-action. Also fills in the keys read from the ini file.
        for i in range(len(self._partArray)):
            self._keyArray.append(tk.StringVar(self._window))
            self._keyArray[i].set(self._partArray[i][2])
            self._keyArray[i].trace_add('write', self.updateEntries)
            tk.Label(self._window, text=ld.partDictionary[self._partArray[i][0]] + " " + ld.partDictionary[self._partArray[i][1]]).grid(row=i, column=1)
            tk.Entry(self._window, textvariable=self._keyArray[i]).grid(row=i, column=2)
            self._rowNumber = i

        # Setup timer options
        self._timerCheckButton = tk.Checkbutton(self._window, text=ld.timerButtonText, variable=self._timerMode, onvalue=1, offvalue=0, command=self.setTimerMode)
        self._timerCheckButton.grid(sticky='w', row=0, column=3)
        self._timerEntry = tk.Entry(self._window, textvariable=self._timerVar, state='disabled')
        self._timerEntry.grid(row=0, column=4)
        self._timerEntry.bind("<FocusIn>", self.onTimerFocus)
        self._timerEntry.bind("<FocusOut>", self.onFocusLoss)
        self._timerVar.trace('w', self.setTimerValue)

        # Setup power options
        self._powerCheckButton = tk.Checkbutton(self._window, text=ld.powerButtonText, variable=self._powerMode, onvalue=1, offvalue=0, command=self.setPowerMode)
        self._powerCheckButton.grid(sticky='w', row=1, column=3)
        self._powerEntry = tk.Entry(self._window, textvariable=self._powerVar, state='disabled')
        self._powerEntry.grid(row=1, column=4)
        self._powerEntry.bind("<FocusIn>", self.onPowerFocus)
        self._powerEntry.bind("<FocusOut>", self.onFocusLoss)
        self._powerVar.trace('w', self.setPowerValue)

        # Adds the start button and info textbox. Refreshes all entry fields and start the main loop.
        self._startButton = tk.Button(self._window, text=ld.startButtonText, command=self.startProgram).grid(sticky='w', row=self._rowNumber + 2, column=1, columnspan=2)
        self._warningLabel.grid(sticky='w', row=self._rowNumber + 3, column=1, columnspan=2)
        self.updateEntries()
        self._window.mainloop()

    # Activate the timer entry field if the checkbox is checked, disable when unchecked.
    def setTimerMode(self):
        if self._timerMode.get():
            self._timerEntry.configure(state='normal')
        else:
            self._timerEntry.configure(state='disabled')

    # Activate the power entry field if the checkbox is checked, disable when unchecked.
    def setPowerMode(self):
        if self._powerMode.get():
            self._powerEntry.configure(state='normal')
        else:
            self._powerEntry.configure(state='disabled')

    # Sets the timer value. If a character is added that isn't a number or a decimal point, it is removed.
    def setTimerValue(self, *_args):
        try:
            self._timerValue = float(self._timerVar.get())
        except ValueError:
            if len(self._timerVar.get()) < 1:
                self._timerValue = 0
                return
            else:
                self._timerVar.set(self._timerVar.get()[:-1])

    # Sets the power value. If a character is added that isn't a number or a decimal point, it is removed. Rounds down to whole numbers.
    def setPowerValue(self, *_args):
        try:
            self._powerValue = int(self._powerVar.get())
        except ValueError:
            if len(self._powerVar.get()) < 1:
                return
            else:
                self._powerVar.set(self._powerVar.get()[:-1])

    # Displays help info if the timer entry field is clicked.
    def onTimerFocus(self, *_args):
        self._warningLabel.config(text=ld.timerInfo)

    # Displays help info if the power entry field is clicked.
    def onPowerFocus(self, *_args):
        self._warningLabel.config(text=ld.powerInfo)

    # Removes help info when user clicks away from timer or power entry field.
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
    def startProgram(self):
        # Removes all possible keybinds in case they were changed.
        for i in string.printable:
            self._window.unbind('<' + i[0] + '>')
            self._window.unbind('<KeyRelease-' + i[0] + '>')

        # Writes the keys the user selected to the array of configured keys.
        for i in range(len(self._keyArray)):
            self._partArray[i][2] = self._keyArray[i].get()

        # Writes the keys to the ini file to save them for the next time the program is started
        for i in self._partArray:
            self._iniWriter[i[0]][i[1]] = i[2]
        with open(self._iniFile, 'w') as _configFile:
            self._iniWriter.write(_configFile)

        # Adds events to the specified keys. This is ugly code, see the explanation below.
        for i in self._partArray:
            self._window.bind('<' + i[2] + '>', lambda event=None, part=i[0], direction=i[1]: (getattr(getattr(self._arm, part), direction)(self._powerMode.get() * self._powerValue, self._timerMode.get() * self._timerValue)))
            self._window.bind('<KeyRelease-' + i[2] + '>', lambda event=None, part=i[0]: (getattr(getattr(self._arm, part), 'off')()))
        # i[2] is the key in question. We bind an event to it that runs the code written after "lambda" when the key is pressed.
        # event is used to ignore the useless data tkinter sends us without us asking for it.
        # part and direction are the part and direction the specified key needs to control.
        # getattr() allows us to turn a piece of text into code. For example, if part = "base", getattr(self._arm, part) would return _arm.base
        # doing this twice (with direction = "counter", for example), we get getattr(getattr(self._arm, part), direction), which would return _arm.base.counter
        # the next part adds the power and timer data. Since these function the same, I'll use power to explain:
        # self.powerMode.get() returns the state if our checkbox. if it's checked, it returns a 1. If it's unchecked, it returns a 0.
        # self.powerValue returns the number the user added to the entry field.
        # By multiplying these two, we are only sending the data if the checkbox is checked, and 0 if it's unchecked.
