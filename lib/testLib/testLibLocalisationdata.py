ledMovement = "aan"
normalMovements = ["vooruit", "achteruit"]
planeMovements = ["omhoog", "omlaag"]
offMovement = "uit"

partList = ["fiets", "auto", "boot", "vliegtuig", "skateboard", "zaklamp"]

partDictionary = {
    "bike": partList[0],
    "car": partList[1],
    "boat": partList[2],
    "plane": partList[3],
    "skateboard": partList[4],
    "flashlight": partList[5],
    "forward": normalMovements[0],
    "backwards": normalMovements[1],
    "up": planeMovements[0],
    "down": planeMovements[1],
    "on": ledMovement,
    "off": offMovement
}