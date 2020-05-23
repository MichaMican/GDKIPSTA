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
        imageSize = im.size
        width = imageSize[0]
        height = imageSize[1]
        backgroundwidth = 1600
        backgroundHeight = 900

        if(width < height):
            if height > width:
                backgroundwidth = round((height * (16/9)))

            background = Image.new('RGB', (backgroundwidth, height), (255, 255, 255))
            offset = (round(backgroundwidth / 2 - width/2), 0)

            background.paste(im, offset)
            background.save(convertedImagesPath + fileName.split(".")[-2] + ".jpg")
            print("Images resized !")

        else:
            im.save(convertedImagesPath + fileName)
            print("Image not resized !")


main()
