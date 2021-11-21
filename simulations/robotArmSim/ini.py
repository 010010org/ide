import configparser
import os

_robotOutputiniFile = "lib/robotArm/robotOutput.ini"
BaseWorkingDirectory = os.path.dirname(os.path.dirname(os.getcwd()))
path = os.path.join(BaseWorkingDirectory , _robotOutputiniFile)

#TODO automatisch een parts list aanmaken
#TODO bool / string types toevoegen

#parts is a list of lists so expanding is easier, dict can only have 2 items, 1 value and 1 key. Whereas a list can have infinite items  
#First item in each sub-list MUST be the name of the part
#each part NEEDS to have: name, degrees
parts = [
    ["base", 0],
    ["shoulder", 0],
    ["elbow", 0],
    ["wrist", 0]
]
config = configparser.ConfigParser()
config.read(path)

#TODO try except?
def getAngles(list):
    for i in range(len(list)):
        #loop through dict of parts searching for the name of the part in the ini file and adding the degree of that part into the dict
        partName =  list[i][0]
        parts[i][1] = int(config[partName]['DEGREES'])
    return parts

print(parts)
getAngles(parts)
print(parts)

