import os

scriptPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/"

for fileName in os.listdir(scriptPath):
    if fileName.__contains__(".jpeg"):
        os.rename(scriptPath + fileName, scriptPath + fileName.split(".")[-2] + ".jpg")