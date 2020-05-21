import os
from sys import argv

FolderToChange = "\DataAugmentation\\DataAugmentation_TL_G\\"
NewId = "2"
for file in os.listdir(os.getcwd() + FolderToChange):
    if file.endswith(".txt"):
        filePath = os.getcwd() + FolderToChange + file
        f = open(filePath)
        lines = f.readlines()
        f.close()
        f = open(filePath, 'w')
        for line in lines:
            f.write(NewId + line[1:])
        f.close()
