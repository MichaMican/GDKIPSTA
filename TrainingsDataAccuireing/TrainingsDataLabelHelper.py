from pathlib import Path
from darknetpy.detector import Detector
import os
import keyboard
from matplotlib import image, patches, pyplot as plt
from PIL import Image
from enum import Enum

class ImageClass(Enum):
    CORRECT = 1
    WRONG = 2
    EXCLUDE = 3
    NONE = 4

detector = Detector('/home/gott/Desktop/GIT/GDKIPSTA/TrainingsDataAccuireing/ampelnRYG.data',
                    '/home/gott/Desktop/GIT/GDKIPSTA/TrainingsDataAccuireing/ampelnRYG.cfg',
                    '/home/gott/Desktop/GIT/GDKIPSTA/TrainingsDataAccuireing/ampelnRYG.weights')

scriptPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/"
imgFolderPath = scriptPath + "imgFolder/"
correctlyLabledFolderPath = scriptPath + "correctLabled/"
wronglyLabledFolderPath = scriptPath + "wrongLabled/"
excludedImagesFolderPath = scriptPath + "excludedImages/"
labelsFolderPath = scriptPath + "labels/"

def main():
    createDir(imgFolderPath)
    createDir(correctlyLabledFolderPath)
    createDir(wronglyLabledFolderPath)
    createDir(excludedImagesFolderPath)
    createDir(labelsFolderPath)
    for fileName in os.listdir(imgFolderPath):
        filePath = imgFolderPath + fileName
        classifingResult = evaluateImage(filePath)

        if classifingResult == ImageClass.CORRECT:
            os.rename(filePath, correctlyLabledFolderPath + fileName)
        elif classifingResult == ImageClass.WRONG:
            os.rename(filePath, wronglyLabledFolderPath + fileName)
        elif classifingResult == ImageClass.EXCLUDE:
            os.rename(filePath, excludedImagesFolderPath + fileName)



def createDir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def getBoundingBoxes(imgPath):
    return detector.detect(imgPath)



def evaluateImage(imgPath):
    bboxes = getBoundingBoxes(imgPath)
    yoloFileStringContent = []
    fig, ax = plt.subplots(1)
    ax.imshow(image.imread(imgPath))


    for i, bbox in enumerate(bboxes):
        color = 'b'
        classId = -1
        if bbox['class'] == "TL_R":
            color = 'r'
            classId = 0
        if bbox['class'] == "TL_Y":
            color = 'y'
            classId = 1
        if bbox['class'] == "TL_G":
            color = 'g'
            classId = 2


        if classId >= 0:

            widthOfImage, heightOfImage = Image.open(imgPath).size

            width = int(int(bbox['right']) - int(bbox['left']))
            height = int(int(bbox['bottom']) - int(bbox['top']))

            relXMiddle = float((0.5 * width + int(bbox['left'])) / widthOfImage)
            relYMiddle = float((0.5 * height + int(bbox['top'])) / heightOfImage)
            relWidth = float(width / widthOfImage)
            relHeight = float(height / heightOfImage)

            yoloFileStringContent.append("{} {} {} {} {}".format(str(classId), relXMiddle, relYMiddle, relWidth, relHeight))

        rect = patches.Rectangle(
            (bbox['left'], bbox['top']),
            bbox['right'] - bbox['left'],
            bbox['bottom'] - bbox['top'],
            linewidth=1,
            edgecolor=color,
            facecolor='none'
        )

        ax.text(bbox['left'], bbox['top'], bbox['class'] + str(bbox['prob']), fontsize=12, bbox={
                'facecolor': color, 'pad': 2, 'ec': color})

        ax.add_patch(rect)

    plt.ion()
    plt.show()
    plt.draw()
    plt.pause(0.001)
    
    print("Press 'Y' if the boxes are CORRECT. Press 'N' if there are WRONG detections. If there is nothing to lable in the image press 'E'")
    imgClass = ImageClass.NONE
    while imgClass == ImageClass.NONE:
        if keyboard.is_pressed('y'):
            imgClass = ImageClass.CORRECT
            print("Perfect - Here's the next one!")
            break
        elif keyboard.is_pressed('n'):
            imgClass = ImageClass.WRONG
            print("Damnit - I'll try better next time")
            break
        elif keyboard.is_pressed('e'):
            imgClass = ImageClass.EXCLUDE
            print("Whats that doing here? - Take a look on this instead")
            break

    if imgClass == ImageClass.CORRECT:
        imgName = (imgPath.split(".")[-2]).split("/")[-1] + ".txt"

        with open(labelsFolderPath + imgName, "w+") as f:
            f.writelines(yoloFileStringContent)

    plt.clf()
    plt.close()

    return imgClass


main()
