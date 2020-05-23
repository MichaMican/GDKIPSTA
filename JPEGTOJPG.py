import os
from pathlib import Path
from PIL import Image

scriptPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/"
convertedImagesPath = scriptPath + "converted/"


def main():

    createDir(convertedImagesPath)

    for fileName in os.listdir(scriptPath):
        resize(fileName)


def createDir(path):
    Path(path).mkdir(parents=True, exist_ok=True)



def resize(fileName):

    if ".jpg" in fileName or ".png" in fileName:
        im = Image.open(scriptPath + fileName, "r")
        exifData = im._getexif()

        if exifData != None:
            if exifData[274] == 6:
                im.rotate(-90, expand=True)
            elif exifData[274] == 8:
                im.rotate(90, expand=True)
            elif exifData[274] == 3:
                im.rotate(180, expand=True)

        imageSize = im.size
        width = imageSize[0]
        height = imageSize[1]


        if ".jpeg" in fileName:
            im.save(convertedImagesPath + fileName.split(".")[-2] + ".jpg")
            print("Images converted !")

        else:
            im.save(convertedImagesPath + fileName)
            print("Image not converted!")


main()
