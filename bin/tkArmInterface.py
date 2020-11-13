import tkinter as tk  # used to create the interface
import localisationdata as ld  # contains all displayed text
import configparser  # used to read and write to ini file
import GPIOArm  # controls the robotic arm
import string  # only used to get a list of letters and numbers


# TODO: fix inconsistent use of private and public variables
# TODO: create advanced mode to hide timer and power settings behind
class Interface(object):
    # Creates instance of robotarm class to control it.
    _arm = GPIOArm.Arm()

    # opens .ini file containing the controls of the robot arm
    iniWriter = configparser.ConfigParser()
    iniFile = 'bin/armControls.ini'

    # opens window to create interface in
    window = tk.Tk()

    # These are used to iterate through the configured keys and text fields
    partArray = []
    keyArray = []

    rowNumber = 0  # Used to put every option on a new line
    # creates info textbox
    warningLabel = tk.Label(window, text="")

    # Trackers for timer checkbox and text field
    timerMode = tk.IntVar(window, value=0)
    timerVar = tk.StringVar(window, value="0")
    timerValue = 0

    # Trackers for power checkbox and text field
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
                    # partArray looks like this:
                    # [part1, direction1, keybind], [part1, direction2, keybind], [part2, ...

        # Creates an "entry" (editable text field) for every move-action. Also fills in the keys read from the ini file.
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

        # Adds the start button and info textbox. Refreshes all entry fields and start the main loop.
        self.startButton = tk.Button(self.window, text=ld.startButtonText, command=self.startProgram).grid(sticky='w', row=self.rowNumber+2, column=1, columnspan=2)
        self.warningLabel.grid(sticky='w', row=self.rowNumber+3, column=1, columnspan=2)
        self.updateEntries()
        self.window.mainloop()

    # Activate the timer entry field if the checkbox is checked, disable when unchecked.
    def setTimerMode(self):
        if self.timerMode.get():
            self.timerEntry.configure(state='normal')
        else:
            self.timerEntry.configure(state='disabled')

    # Activate the power entry field if the checkbox is checked, disable when unchecked.
    def setPowerMode(self):
        if self.powerMode.get():
            self.powerEntry.configure(state='normal')
        else:
            self.powerEntry.configure(state='disabled')

    # Sets the timer value. If a character is added that isn't a number or a decimal point, it is removed.
    def setTimerValue(self, *_args):
        try:
            self.timerValue = float(self.timerVar.get())
        except ValueError:
            if len(self.timerVar.get()) < 1:
                self.timerValue = 0
                return
            else:
                self.timerVar.set(self.timerVar.get()[:-1])

    # Sets the power value. If a character is added that isn't a number or a decimal point, it is removed. Rounds down to whole numbers.
    def setPowerValue(self, *_args):
        try:
            self.powerValue = int(self.powerVar.get())
        except ValueError:
            if len(self.powerVar.get()) < 1:
                return
            else:
                self.powerVar.set(self.powerVar.get()[:-1])

    # Displays help info if the timer entry field is clicked.
    def onTimerFocus(self, *_args):
        self.warningLabel.config(text=ld.timerInfo)

    # Displays help info if the power entry field is clicked.
    def onPowerFocus(self, *_args):
        self.warningLabel.config(text=ld.powerInfo)

    # Removes help info when user clicks away from timer or power entry field.
    def onFocusLoss(self, *_args):
        self.warningLabel.config(text="")

    # Updates the list of assigned keys. If an entry field contains multiple characters, all but the first one are removed.
    # Gives a warning if the same key is used multiple times.
    def updateEntries(self, *_args):
        stringKeyArray = []
        for i in self.keyArray:
            stringKeyArray.append(i.get())
            if len(i.get()) > 1:
                i.set(i.get()[0])
        if len(self.keyArray) != len(set(stringKeyArray)):
            self.warningLabel.config(text=ld.duplicatesWarning)
        else:
            self.warningLabel.config(text="")

    # Starts controlling controlling the robotic arm.
    def startProgram(self):
        # Removes all possible keybinds in case they were changed. #TODO: test non-letter keybinds
        for i in string.ascii_letters+string.digits:
            self.window.unbind('<'+i[0]+'>')
            self.window.unbind('<KeyRelease-'+i[0]+'>')

        # Writes the keys the user selected to the array of configured keys.
        for i in range(len(self.keyArray)):
            self.partArray[i][2] = self.keyArray[i].get()

        # Writes the keys to the ini file to save them for the next time the program is started
        for i in self.partArray:
            self.iniWriter[i[0]][i[1]] = i[2]
        with open(self.iniFile, 'w') as configFile:
            self.iniWriter.write(configFile)

        # Adds events to the specified keys. This is ugly code, see the explanation below.
        for i in self.partArray:
            self.window.bind('<'+i[2]+'>', lambda event=None, part=i[0], direction=i[1]: (getattr(getattr(self._arm, part), direction)(self.powerMode.get()*self.powerValue, self.timerMode.get()*self.timerValue)))
            self.window.bind('<KeyRelease-'+i[2]+'>', lambda event=None, part=i[0]: (getattr(getattr(self._arm, part), 'off')()))
        # i[2] is the key in question. We bind an event to it that runs the code written after "lambda" when the key is pressed.
        # event is used to ignore the useless data tkinter sends us without us asking for it.
        # part and direction are the part and direction the specified key needs to control.
        # getattr() allows us to turn a piece of text into code. For example, if part = "base", getattr(self._arm, part) would return _arm.base
        # doing this twice (with direction = "counter", for example), we get getattr(getattr(self._arm, part), direction), which would return _arm.base.counter
        # the next part adds the power and timer data. Since these function the same, I'll use power to explain:
        # self.powerMode.get() returns the state if our checkbox. if it's checked, it returns a 1. If it's unchecked, it returns a 0.
        # self.powerValue returns the number the user added to the entry field.
        # By multiplying these two, we are only sending the data if the checkbox is checked, and 0 if it's unchecked.
