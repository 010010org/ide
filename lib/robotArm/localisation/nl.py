baseMovements = ["met de klok mee", "tegen de klok in"]
gripMovements = ["open", "dicht"]
ledMovement = "aan"
normalMovements = ["omhoog", "omlaag"]
offMovement = "uit"

partList = ["basis", "schouder", "elleboog", "pols", "grijper", "lampje"]

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
