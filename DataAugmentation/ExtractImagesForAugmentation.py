import os
from PIL import Image
import cv2

def cropImage(img, height, width, content):
    mittewidth = int(width * float(content[1]))
    mittheight = int(height * float(content[2]))
    widthOfBbox =int( width * float(content[3]))
    heightOfBbox = int(height * float(content[4]))
    min_x = int(mittewidth - (0.5 * widthOfBbox))
    min_y = int(mittheight - (0.5 * heightOfBbox))
    crop_img = img[min_y:min_y+heightOfBbox, min_x:min_x+widthOfBbox]
    return crop_img

def saveImageToFolder(indicator, img, name):
    folderToSave = "wait what"
    if indicator == 0:
        folderToSave = "TL_R"
    elif indicator == 1:
        folderToSave = "TL_Y"
    elif indicator == 2:
        folderToSave = "TL_G"
    elif indicator == 3:
        folderToSave = "TS"
    elif indicator == 4:
        folderToSave = "TL_RY"
    path = folderToSave + "\\" + name
    if img.shape[0] is not 0 and img.shape[1] is not 0 and img.shape[2] is not 0:
        cv2.imwrite(path, img)

    
def checkForAllFolders():
    if not os.path.exists("TL_R"):
        os.makedirs("TL_R")
    if not os.path.exists("TL_Y"):
        os.makedirs("TL_Y")
    if not os.path.exists("TL_G"):
        os.makedirs("TL_G")
    if not os.path.exists("TL_RY"):
        os.makedirs("TL_RY")
    if not os.path.exists("TS"):
        os.makedirs("TS")
def main():
    checkForAllFolders()
    path = os.getcwd() + "/Dataset"
    num_files = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))]) / 2
    counter = 1
    for file in os.listdir(path):
        print("Working on {} / {} Image".format(counter, num_files))
        if file.endswith(".txt"):
            imgPath = file.split('.')[0] + ".jpg"
            if os.path.isfile("Dataset/" + imgPath) == False:
                continue
                counter += 1
            img = cv2.imread("Dataset/" + imgPath)
            if img is None:
                continue
                counter += 1
            height, width, channels = img.shape
            linecount = len(open("Dataset/" + file).readlines())
            for line in range(0,linecount):
                f = open("Dataset/"+file)
                content = f.readlines()[line]
                content = content.split(" ")
                croppedImage = cropImage(img, height, width, content)
                saveImageToFolder(int(content[0]), croppedImage, imgPath)
            counter += 1

main()