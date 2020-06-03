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

    if ".jpg" in fileName or ".png" in fileName or ".jpeg" in fileName:
        im = Image.open(scriptPath + fileName, "r")
        exifData = None
        try:
            exifData = im._getexif()
        except:
            #This happens when the image is an Exif free format (e.g. jpg or png)
            print("Unable to get exif of " + fileName)

        if exifData != None:
            if exifData[274] == 6:
                print("Rotating Img left")
                im = im.rotate(-90, expand=True)
            elif exifData[274] == 8:
                print("Rotating Img right")
                im = im.rotate(90, expand=True)
            elif exifData[274] == 3:
                print("Rotating Img arround")
                im = im.rotate(180, expand=True)

        #save jpeg as jpg and non jpeg as their type
        if ".jpeg" in fileName:
            im.save(convertedImagesPath + fileName.split(".")[-2] + ".jpg")
            print("Images converted !")
        else:
            im.save(convertedImagesPath + fileName)
            print("Image not converted!")


main()
