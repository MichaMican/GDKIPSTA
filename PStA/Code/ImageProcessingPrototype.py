import cv2
import itertools as it
import time
import numpy as np
import time


def cropImageY(imgArr):
    res = imgArr.shape

    sumTopBot = [[],[]] #sumTop, sumBot, numberOfPixels in Top/Bot

    #calculate start threshholds
    for y, x in it.product(range(0, round(res[0]/3)), range(0, res[1])):
        yfromBot = res[0] - y - 1
        xfromBot = res[1] - x - 1

        if imgArr[y][x] < 128:
            sumTopBot[0].append(imgArr[y][x])
        if imgArr[yfromBot][xfromBot] < 128:
            sumTopBot[1].append(imgArr[yfromBot][xfromBot])

    blackThresholdTop = np.median(sumTopBot[0])
    blackThresholdBot = np.median(sumTopBot[1])

    detectedTopBorder=-1
    detectedBotBorder=-1
    #check upper third if the top of the traffic light is detected
    while (detectedBotBorder < 0 or detectedBotBorder < 0):
        for y, x in it.product(range(0, round(res[0]/3)), range(0, res[1])):
            yfromBot = res[0] - y - 1
            xfromBot = res[1] - x - 1

            if(detectedTopBorder < 0):
                if imgArr[y][x] <= blackThresholdTop:
                    colorUnderneath = (imgArr[y+1][x] +imgArr[y+2][x]) / 2
                    if colorUnderneath <= blackThresholdTop:
                        detectedTopBorder = y
                        break

            if(detectedBotBorder < 0):                
                if imgArr[yfromBot][xfromBot] <= blackThresholdBot:
                    colorAbove = (imgArr[yfromBot-1][xfromBot] + imgArr[yfromBot-2][xfromBot]) / 2
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

    for x in range(0,imgArr.shape[1]):
        imgArr[detectedTopBorder][x] = 255
        imgArr[detectedBotBorder][x] = 255

    return imgArr
    

def evaluate(arr):
    arrayToReturn = [-1, 1] #detectedColor, certanty
    arrayToReturn[0] = arr.index(max(arr))

    if arrayToReturn[0] == 0 or arrayToReturn[0] == 2:
        #this is if the first and the last box reports a high value
        if abs(arr[0] - arr[2]) < abs(arr[arrayToReturn[0]] - arr[1]):
            arrayToReturn[1] = abs(arr[0] - arr[2])/abs(arr[arrayToReturn[0]] - arr[1])

    return arrayToReturn



def main(pathToImage, saveImageAfterProcessing=True):

    imgGrey = cv2.imread(pathToImage, 0)
    cropedGreyImg = imgGrey[0:imgGrey.shape[0], round(imgGrey.shape[1]/2)-5: round(imgGrey.shape[1]/2)+5]
    resolution = cropedGreyImg.shape
    ythird = round(resolution[0] / 3)
    ytwothirds = round(2 * resolution[0] / 3)

    sumPixels = [0, 0, 0]
    averageGrey = [0, 0, 0]


    for y, x in it.product(range(0, resolution[0]), range(0, resolution[1])):
        # First third
        if y < ythird:
            sumPixels[0] += cropedGreyImg[y][x]
            # imgGrey[y][x] = 255

        # second third
        elif y < ytwothirds and y > ythird:
            sumPixels[1] += cropedGreyImg[y][x]
            # imgGrey[y][x] = 100

        # third third
        else:
            sumPixels[2] += cropedGreyImg[y][x]
            # imgGrey[y][x] = 0

        if y == ythird or y == ytwothirds:
            pass
            # imgGrey[y][x] = 255

    for i, sumPixel in enumerate(sumPixels):
        #resolution/3 => only thirds of image
        averageGrey[i] = sumPixel/(resolution[0] / 3 * resolution[1])

    evaluationIndexGreyScale = evaluate(averageGrey)[0]

    imgGrayYCropped = cropImageY(cropedGreyImg)

    result = -1
    result = evaluationIndexGreyScale

    if saveImageAfterProcessing:
        cv2.imwrite("./out/" + pathToImage.split("/")[-1], imgGrayYCropped)
    return result

# main("C:/Users/dasch/Downloads/AmpelTest1.jpg")
