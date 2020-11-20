# startMenu
startMenuName = "startmenu"
startMenuMessage = "kies een programma om te starten"
setupOption = "Instellingen"
controlArmOption = "robotarm besturen met toetsenbord"
advancedControlArmOption = "geävanceerde besturing robotarm"
programOption = "programmeerinterface starten"
AdvancedProgramOption = "geävanceerde programmeerinterface"

# setupUsedIO
infoTextBox = "Vink de apparaten aan die je wil aansturen"
saveButton = "Opslaan"

# setupPinout
pinoutTextbox = "Vul de pins in waarop je de apparaten hebt aangesloten."
pinoutTextbox2 = "In het geval van meerdere kabels vul je de gekleurde kabel links in en de andere rechts."
pinoutButton = "Opslaan en terug naar startmenu"

# tkinterTest
advanced = "Geavanceerde modus"
fileMenuList = ["Nieuw...", "Openen", "Opslaan", "Opslaan als..."]
expressionExplanationList = ["optellen", "aftrekken", "vermenigvuldigen", "delen", "delen zonder rest",
                             "modulo (rest van deling)", "machtsverheffen", "Bitwise shift naar links",
                             "Bitwise shift naar rechts", "Bitwise OR", "Bitwise XOR", "Bitwise AND", "Bitwise NOT",
                             "Matrix vermenigvuldiging"]
equationExplanationList = ["is gelijk aan", "niet gelijk aan", "kleiner dan", "kleiner dan of gelijk aan", "groter dan",
                           "groter dan of gelijk aan", "is dezelfde variabele", "niet dezelfde variabele",
                           "is een onderdeel van", "geen onderdeel van"]
functionExplanationList = ["schrijft tekst naar de console", "leest tekst uit de console tot de enter-toets ingedrukt wordt", "zet data om in tekst",
                           "zet data om in een geheel getal (rondt omlaag af)", "zet data om in een kommagetal",
                           "rondt een kommagetal af naar het dichtstbijzijnde gehele getal",
                           "geeft een \"range\" van getallen tussen de twee ingevoerde getallen. Als je maar één getal invult wordt als ander getal 0 gebruikt. Wordt gebruikt in for loops",
                           "geeft de lengte van een lijst of string. Handig voor for loops", "geeft het laagste getal in een lijst",
                           "geeft het hoogste getal in een lijst"]
functionExplanationList2 = ["wacht voor de ingevoerde tijd (in seconden)", "geeft het aantal seconden sinds 1 januari 1970. Handig voor vergelijkingen",
                            "geeft een willekeurig kommagetal tussen 0.0 en 1.0",
                            "geeft een willekeurig geheel getal tussen de twee getallen die je ingevoerd hebt. Als je maar één getal invult wordt als ander getal 0 gebruikt"]


windowName = "robotarm"
fileWindowName = "Bestand"
commandWindowName = "commando"
expressionWindowName = "berekening"
equationWindowName = "vergelijking"
functionWindowName = "standaard functies"
functionWindow2Name = "externe functies"
armWindowName = "onderdeel"
movementWindowName = "beweegrichting"
saveAsWindowText = "Bestandsnaam:"

helpInfo = "commando-uitleg: "
helpInfoDefault = "klik met je rechtermuisknop op een commando voor uitleg"

baseMovements = ["met de klok mee", "tegen de klok in"]
gripMovements = ["open", "dicht"]
ledMovement = "aan"
normalMovements = ["omhoog", "omlaag"]
offMovement = "uit"

partList = ["basis", "schouder", "elleboog", "pols", "grijper", "lampje"]

# tkArmInterface
duplicatesWarning = "Dezelfde toets wordt voor meerdere dingen gebruikt."
timerButtonText = "Timer"
powerButtonText = "Kracht"
startButtonText = "opslaan en besturen"
timerInfo = "vul een aantal seconden in"
powerInfo = "vul een percentage (0-100) in"

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

# Unused
upDownErrorMessage = "kan niet omhoog of omlaag!"
leftRightErrorMessage = "kan niet naar links of rechts!"
openCloseErrorMessage = "kan niet open of dicht!"
turnOnErrorMessage = "kan niet gewoon aan!"
