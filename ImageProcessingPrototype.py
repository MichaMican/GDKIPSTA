import cv2
import itertools as it
import time
import numpy as np
import time


def detectUpperLowerStart(imgArr):
    res = imgArr.shape
    blackThresholdTop = 0 # this has to be calculated
    blackThresholdBot = 0 # this has to be calculated

    sumTopBot = [[],[]] #sumTop, sumBot, numberOfPixels in Top/Bot

    #calculate start threshholds
    for y, x in it.product(range(0, round(res[0]/3)), range(0, res[1])):
        yfromBot = res[0] - y - 1
        xfromBot = res[1] - x - 1

        sumTopBot
        sumTopBot


    detectedTopBorder=-1
    detectedBotBorder=-1
    #check upper third if the top of the traffic light is detected
    while (detectedBotBorder < 0 or detectedBotBorder < 0):
        for y, x in it.product(range(0, round(res[0]/3)), range(0, res[1])):
            yfromBot = res[0] - y - 1
            xfromBot = res[1] - x - 1

            if(detectedTopBorder < 0):
                if imgArr[y][x] <= blackThresholdTop:
                    colorUnderneath = (imgArr[y+1][x] +imgArr[y+2][x] +imgArr[y+3][x] +imgArr[y+4][x] +imgArr[y+5][x]) / 5
                    if colorUnderneath <= blackThresholdTop:
                        detectedTopBorder = y
                        break

            if(detectedBotBorder < 0):                
                if imgArr[yfromBot][xfromBot] <= blackThresholdBot:
                    colorAbove = (imgArr[yfromBot-1][xfromBot] + imgArr[yfromBot-2][xfromBot] + imgArr[yfromBot-3][xfromBot] + imgArr[yfromBot-4][xfromBot] + imgArr[yfromBot-5][xfromBot]) / 5
                    if colorAbove <= blackThresholdBot:
                        detectedBotBorder = yfromBot
                        break
            
        if detectedBotBorder < 0 or detectedTopBorder < 0:
            blackThresholdTop += 10
            blackThresholdBot += 10

    if detectedTopBorder < 0:
        detectedTopBorder = 0
    if detectedBotBorder < 0:
        detectedBotBorder = res[1]-1

    return [detectedTopBorder, detectedBotBorder]
    


def evaluate(arr):
    return arr.index(max(arr))


def indexToColor(index):
    if index == 0:
        return "RED"
    elif index == 1:
        return "YELLOW"
    elif index == 2:
        return "GREEN"
    else:
        return "Unknown result - " + str(index)


def main(pathToImage, showImageAfterProcessing=True):

    imgColor = cv2.imread(pathToImage, -1)
    imgColorPreProcessed = cv2.imread(pathToImage, -1)

    resolution = imgColor.shape

    ythird = round(resolution[0] / 3)
    ytwothirds = round(2 * resolution[0] / 3)

    sumPixels = [0, 0, 0]
    averageColor = [0, 0, 0]
    for y, x in it.product(range(0, resolution[0]), range(0, resolution[1])):
        # First third
        if y < ythird:
            sumPixels[0] += imgColor[y][x][2]
            imgColorPreProcessed[y][x][0] = 0
            imgColorPreProcessed[y][x][1] = 0
        # second third
        elif y < ytwothirds and y > ythird:
            sumPixels[1] += (3 * imgColor[y][x][1] + 2 * imgColor[y][x][2])/5
            imgColorPreProcessed[y][x][1] = 0

        # third third
        else:
            sumPixels[2] += imgColor[y][x][1]
            imgColorPreProcessed[y][x][0] = 0
            imgColorPreProcessed[y][x][2] = 0

        if y == ythird or y == ytwothirds:
            imgColor[y][x][0] = 255
            imgColor[y][x][1] = 255
            imgColor[y][x][2] = 255

    for i, sumPixel in enumerate(sumPixels):
        averageColor[i] = sumPixel/(resolution[0] / 3 * resolution[1])

    evaluationIndexColor = evaluate(averageColor)
    imgGrey = cv2.imread(pathToImage, 0)

    cropedGreyImg = imgGrey[0:resolution[0], round(resolution[1]/2)-5: round(resolution[1]/2)+5]

    resolution = cropedGreyImg.shape
    ythird = round(resolution[0] / 3)
    ytwothirds = round(2 * resolution[0] / 3)

    sumPixels = [0, 0, 0]
    averageGrey = [0, 0, 0]
    imgGrey = cropedGreyImg


    for y, x in it.product(range(0, resolution[0]), range(0, resolution[1])):
        # First third
        if y < ythird:
            sumPixels[0] += imgGrey[y][x]
            # imgGrey[y][x] = 255

        # second third
        elif y < ytwothirds and y > ythird:
            sumPixels[1] += imgGrey[y][x]
            # imgGrey[y][x] = 100

        # third third
        else:
            sumPixels[2] += imgGrey[y][x]
            # imgGrey[y][x] = 0

        if y == ythird or y == ytwothirds:
            pass
            # imgGrey[y][x] = 255

    for i, sumPixel in enumerate(sumPixels):
        #resolution/3 => only thirds of image
        averageGrey[i] = sumPixel/(resolution[0] / 3 * resolution[1])

    evaluationIndexGreyScale = evaluate(averageGrey)

    resultText = -1
    resultText = evaluationIndexGreyScale

    imgGrayYCropped = cropedGreyImg.copy()
    
    borders = detectUpperLowerStart(imgGrayYCropped)

    for x in range(0, imgGrayYCropped.shape[1]):
        imgGrayYCropped[borders[0]][x] = 255
        imgGrayYCropped[borders[1]][x] = 255


    if showImageAfterProcessing:
        if imgColor.shape[2] == 4:
            imgGrey3Chanel = cv2.cvtColor(cropedGreyImg, cv2.COLOR_GRAY2BGRA)
        elif imgColor.shape[2] == 3:
            imgGrey3Chanel = cv2.cvtColor(cropedGreyImg, cv2.COLOR_GRAY2BGR)

        img = np.hstack((imgGrey, imgGrayYCropped))
        cv2.imshow(pathToImage.split("/")[-1], img)

        output = imgGrey.copy()

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return resultText

# main("C:/Users/dasch/Downloads/AmpelTest1.jpg")
