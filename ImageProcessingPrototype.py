import cv2
import itertools as it
import time
import numpy as np
import time


def detectUpperLowerStart(imgArr):
    res = imgArr.shape
    blackThreshold = 125
    detectedTopBorder=[]
    detectedBotBorder=[]
    bottomBorderDetected = False
    topBorderDetected = False
    #check upper third if the top of the traffic light is detected
    while (not topBorderDetected or not bottomBorderDetected) and blackThreshold >= 0:
        for y, x in it.product(range(0, round(res[0]/3)), range(0, res[1])):
            yfromBot = res[0] - y - 1
            xfromBot = res[1] - x - 1

            if not topBorderDetected:
                if imgArr[y][x] <= blackThreshold:
                    colorUnderneath = (imgArr[y+1][x] +imgArr[y+2][x] +imgArr[y+3][x] +imgArr[y+4][x] +imgArr[y+5][x]) / 5
                    if colorUnderneath >= blackThreshold:
                        detectedTopBorder.append(y)
                        break
                elif len(detectedTopBorder) >= 1:
                    topBorderDetected = True

            if not bottomBorderDetected:
                if imgArr[yfromBot][xfromBot] <= blackThreshold:
                    colorAbove = (imgArr[yfromBot-1][xfromBot] + imgArr[yfromBot-2][xfromBot] + imgArr[yfromBot-3][xfromBot] + imgArr[yfromBot-4][xfromBot] + imgArr[yfromBot-5][xfromBot]) / 5
                    if colorAbove >= blackThreshold:
                        detectedBotBorder.append(yfromBot)
                        break
                elif len(detectedBotBorder) >= 1:
                    bottomBorderDetected = True
            
        if not topBorderDetected or not bottomBorderDetected:
            blackThreshold -= 10

    if len(detectedTopBorder) <= 0:
        detectedTopBorder = [0]
    if len(detectedBotBorder) <= 0:
        detectedBotBorder = [res[0]-1]

    return [int(round(np.mean(detectedTopBorder))), int(round(np.mean(detectedBotBorder)))]
    


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

    print("Processing " + pathToImage)

    start = time.time()
    imgColor = cv2.imread(pathToImage, -1)
    imgColorPreProcessed = cv2.imread(pathToImage, -1)
    end = time.time()
    print("Time to read image (colored) : " + str(end - start))

    start = time.time()
    resolution = imgColor.shape

    #cropedColorImg = imgColor[0:resolution[0], round(resolution[1]/2)+5: round(resolution[1]/2)+5]

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

    end = time.time()
    print("Time to calculate Average (colored): " + str(end - start))

    print(str(averageColor) + " by Color")
    evaluationIndexColor = evaluate(averageColor)

    start = time.time()
    imgGrey = cv2.imread(pathToImage, 0)

    cropedGreyImg = imgGrey[0:resolution[0], round(resolution[1]/2)-5: round(resolution[1]/2)+5]

    resolution = cropedGreyImg.shape


    # if imgColor.shape[2] == 4:
    #     imgGrey = cv2.cvtColor(imgColorPreProcessed, cv2.COLOR_BGRA2GRAY)
    # elif imgColor.shape[2] == 3:
    #     imgGrey = cv2.cvtColor(imgColorPreProcessed, cv2.COLOR_BGR2GRAY)
    # else:
    #     imgGrey = cv2.imread(pathToImage, 0)

    end = time.time()
    print("Time to read image (greyscaled) : " + str(end - start))

    start = time.time()
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
        #resolution0/3 => only thirds of image
        averageGrey[i] = sumPixel/(resolution[0] / 3 * resolution[1])

    end = time.time()
    print("Time to calculate Average (greyscale): " + str(end - start))

    print(str(averageGrey) + " by Greyscale")
    evaluationIndexGreyScale = evaluate(averageGrey)

    resultText = ""
    # if evaluationIndexColor != evaluationIndexGreyScale:
    #     resultText = "Color & greyscale deliver different results - Color: " + \
    #         indexToColor(evaluationIndexColor) + " Greyscale: " + indexToColor(
    #             evaluationIndexGreyScale) + " C: " + str(averageColor) + " G: " + str(averageGrey)
    # else:
    #     resultText = indexToColor(
    #         evaluationIndexColor) + " C: " + str(averageColor) + " G: " + str(averageGrey)

    resultText = "color|greyscale: {} | {} ({} | {})".format(indexToColor(evaluationIndexColor), indexToColor(evaluationIndexGreyScale), str(averageColor), str(averageGrey))


    imgGrayYCropped = cropedGreyImg.copy()
    borders = detectUpperLowerStart(imgGrayYCropped)

    for x in range(0, imgGrayYCropped.shape[1]):
        imgGrayYCropped[borders[0]][x] = 255
        imgGrayYCropped[borders[1]][x] = 255


    print(resultText)
    if showImageAfterProcessing:
        if imgColor.shape[2] == 4:
            imgGrey3Chanel = cv2.cvtColor(cropedGreyImg, cv2.COLOR_GRAY2BGRA)
        elif imgColor.shape[2] == 3:
            imgGrey3Chanel = cv2.cvtColor(cropedGreyImg, cv2.COLOR_GRAY2BGR)

        img = np.hstack((cropedGreyImg, imgGrayYCropped))
        cv2.imshow(pathToImage.split("/")[-1], img)

        output = imgGrey.copy()

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return resultText

# main("C:/Users/dasch/Downloads/AmpelTest1.jpg")
