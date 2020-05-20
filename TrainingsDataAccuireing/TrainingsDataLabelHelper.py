from pathlib import Path
from darknetpy.detector import Detector
import os
import keyboard
from matplotlib import image, patches, pyplot as plt
from enum import Enum

class ImageClass(Enum):
    CORRECT = 1
    WRONG = 2
    EXCLUDE = 3
    NONE = 4

detector = Detector('<absolute-path-to>/darknet/cfg/coco.data',
                    '<absolute-path-to>/darknet/cfg/yolo.cfg',
                    '<absolute-path-to>/darknet/yolo.weights')

scriptPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/"
imgFolderPath = scriptPath + "imgFolder/"
correctlyLabledFolderPath = scriptPath + "correctLabled/"
wronglyLabledFolderPath = scriptPath + "wrongLabled/"
excludedImagesFolderPath = scriptPath + "excludedImages/"

def main():
    createDir(imgFolderPath)
    createDir(correctlyLabledFolderPath)
    createDir(wronglyLabledFolderPath)
    createDir(excludedImagesFolderPath)
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
    return detector.detect('<absolute-path-to>/darknet/data/dog.jpg')



def evaluateImage(imgPath):
    bboxes = getBoundingBoxes(imgPath)
    fig, ax = plt.subplots(1)
    ax.imshow(image.imread(imgPath))

    for i, bbox in enumerate(bboxes):
        color = 'b'
        if bbox['class'] == "TL_R":
            color = 'r'
        if bbox['class'] == "TL_Y":
            color = 'y'
        if bbox['class'] == "TL_G":
            color = 'g'

        rect = patches.Rectangle(
            (bbox['left'], bbox['top']),
            bbox['right'] - bbox['left'],
            bbox['bottom'] - bbox['top'],
            linewidth=1,
            edgecolor=color,
            facecolor='none'
        )

        ax.text(bbox['left'], bbox['top'], bbox['class'], fontsize=12, bbox={
                'facecolor': color, 'pad': 2, 'ec': color})

        ax.add_patch(rect)

    plt.ion()
    plt.show()
    plt.draw()
    plt.pause(0.001)
    
    print("Press 'Y' if the boxes are CORRECT. Press 'N' if there are WRONG detections. If there is nothing to lable in the image press 'e'")
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

    plt.clf()
    plt.close()

    return imgClass


main()
