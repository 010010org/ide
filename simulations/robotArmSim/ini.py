import configparser
import os
import copy

_robotOutputiniFile = "lib/robotArm/robotOutput.ini"
BaseWorkingDirectory = os.path.dirname(os.path.dirname(os.getcwd()))
path = os.path.join(BaseWorkingDirectory , _robotOutputiniFile)
#print(f"path exists {os.path.exists(path)}")
#print(path)

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
#config = configparser.ConfigParser()
#config.read(path)

#TODO try except?
def getAngles(list):
    for i in range(len(list)):
        #loop through dict of parts searching for the name of the part in the ini file and adding the degree of that part into the dict
        partName =  list[i][0]
        parts[i][1] = int(config[partName]['DEGREES'])
    return parts

def foo():
    list = [[0],[1],[2]]

    list2 = copy.deepcopy(list)
    list3 = copy.deepcopy(list)

    list2[0].append(1)
    list2[1].append(3)
    list2[2].append(0)

    list3[0].append(4)
    list3[1].append(1)
    list3[2].append(0)

    print(f'list2: {list2}')
    print(f'list3: {list3}')
    for i in range(len(list)):
        FinalAngle = list3[i][1]
        currentAngle = list2[i][1]
        angledifference = FinalAngle- currentAngle
        print(f"{angledifference}")
        if angledifference > 0:
            print(f'go up')
        elif angledifference < 0:
            print(f'go down')


foo()