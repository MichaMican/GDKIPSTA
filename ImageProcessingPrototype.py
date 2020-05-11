import cv2
import itertools as it

pathToImage = "C:/Users/dasch/Downloads/AmpelTest2.jpg"

img = cv2.imread(pathToImage, -1)

resolution = img.shape

ythird = round(resolution[0] / 3)
ytwothirds = round(2 * resolution[0] / 3)

sumPixels = [0,0,0]
averageColor = [0,0,0]
for y, x in it.product(range(0, resolution[0]), range(0, resolution[1])):
    #First third
    if y < ythird:
        sumPixels[0] += img[y][x][2]
    #second third
    elif y < ytwothirds and y > ythird:
        sumPixels[1] += (3 * img[y][x][1] + 2 * img[y][x][2])/5
        #img[y][x] = 100

    #third third    
    else:
        sumPixels[2] += img[y][x][1]
        #img[y][x] = 0

for i, sumPixel in enumerate(sumPixels):
    averageColor[i] = sumPixel/(resolution[0] / 3 * resolution[1])

print(str(averageColor) + " by Color")

img = cv2.imread(pathToImage, 0)

ythird = round(resolution[0] / 3)
ytwothirds = round(2 * resolution[0] / 3)

sumPixels = [0,0,0]
averageColor = [0,0,0]

for y, x in it.product(range(0, resolution[0]), range(0, resolution[1])):
    #First third
    if y < ythird:
        sumPixels[0] += img[y][x]
        #img[y][x] = 255

    #second third
    elif y < ytwothirds and y > ythird:
        sumPixels[1] += img[y][x]
        #img[y][x] = 100

    #third third    
    else:
        sumPixels[2] += img[y][x]
        #img[y][x] = 0

for i, sumPixel in enumerate(sumPixels):
    averageColor[i] = sumPixel/(resolution[0] / 3 * resolution[1])

print(str(averageColor) + " by Greyscale")

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()