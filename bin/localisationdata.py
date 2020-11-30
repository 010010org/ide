# startMenu
startMenuName = "start menu"
startMenuMessage = "choose a program to start"
setupOption = "Setup"
controlArmOption = "control robot arm with keyboard"
advancedControlArmOption = "advanced robot arm control"
programOption = "start programming interface"
AdvancedProgramOption = "advanced programming interface"

# setupUsedIO
infoTextBox = "select the devices you want to use"
saveButton = "Save"

# setupPinout
pinoutTextbox = "Please enter the pins you used to connect the selected devices."
pinoutTextbox2 = "In the case of multiple cables the coloured cable is the one on the left, the other one is the one on the right."
pinoutButton = "Save and exit"

# tkinterTest
advanced = "Advanced mode"
fileMenuList = ["New...", "Open", "Save", "Save as..."]
expressionExplanationList = ["addition", "subtraction", "multiplication", "division",
                             "floor division (division rounded down)", "modulo (rest number of division)",
                             "exponentiation", "Bitwise shift left", "Bitwise shift right", "Bitwise OR", "Bitwise XOR",
                             "Bitwise AND", "Bitwise NOT", "Matrix multiplication"]
equationExplanationList = ["equal to", "not equal to", "smaller than", "smaller than or equal to", "bigger than",
                           "bigger than or equal to", "is the same variable", "not the same variable", "is a part of",
                           "not a part of"]
functionExplanationList = ["prints text to the console", "takes input from console until the return key is pressed", "turns data into text",
                           "turns data into whole number (rounded down)", "turns data into a float (a number with a decimal point)",
                           "rounds a float to the nearest whole number",
                           "gives a range of numbers between two entered numbers. If only one number is entered the other one is set to 0. used in for loops",
                           "returns the length of a list or string. Useful in for loops", "returns the lowest number in a list",
                           "returns the highest number in a list"]
functionExplanationList2 = ["waits for a specified amount of time (in seconds)", "returns the number of seconds since jan 1st 1970. Useful for comparisons",
                            "returns a random number between 0.0 and 1.0", "returns a random number between two specified values. If you only use one value, the other one is set to 0"]


windowName = "robotarm"
fileWindowName = "File"
commandWindowName = "command"
expressionWindowName = "expression"
equationWindowName = "equation"
functionWindowName = "standard functions"
functionWindow2Name = "external functions"
armWindowName = "part"
movementWindowName = "direction"
saveAsWindowText = "File name:"

helpInfo = "command explanation: "
helpInfoDefault = "right click a command to get an explanation of it"

baseMovements = ["clockwise", "counterclockwise"]
gripMovements = ["open", "close"]
ledMovement = "on"
normalMovements = ["up", "down"]
offMovement = "off"

partList = ["base", "shoulder", "elbow", "wrist", "grip", "light"]

# tkControlInterface
duplicatesWarning = "You used the same key multiple times!"
timerButtonText = "Timer"
powerButtonText = "Power"
saveButtonText = "Save and start"
editButtonText = "Stop and edit"
stopButtonText = "Emergency stop"
timerInfo = "enter a number of seconds"
powerInfo = "enter a percentage (0-100)"

partDictionary = {
    "base": partList[0],
    "shoulder": partList[1],
    "elbow": partList[2],
    "wrist": partList[3],
    "grip": partList[4],
    "light": partList[5],
    "clock": baseMovements[0],
    "counter": baseMovements[1],
    "up": normalMovements[0],
    "down": normalMovements[1],
    "open": gripMovements[0],
    "close": gripMovements[1],
    "on": ledMovement,
    "off": offMovement
}
