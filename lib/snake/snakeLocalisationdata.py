from random import normalvariate


normalMovements = ["up", "down"]
partList = ["head", "body1", "body2", "body3", "body4", "body5", "body6", "body7", "tail"]

partDictionary = {
    "head":partList[0],
    "body1":partList[1],
    "body2":partList[2],
    "body3":partList[3],
    "body4":partList[4],
    "body5":partList[5],
    "body6":partList[6],
    "body7":partList[7],
    "tail":partList[8],
    "up":normalMovements[1],
    "down":normalMovements[0]
}

fileError = "is not correct, file cannot be found. please make sure the file exists"
writeToIniFile = "something went wrong writing to ini file"