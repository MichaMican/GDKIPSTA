import os
import ImageProcessingPrototype as imProc
import sys

path = "C:/Users/dasch/Documents/Git/Schule/GDKIPSTA/TestImages/"

for filename in os.listdir(path):

    displayImages = False

    if len(sys.argv) >= 2:
        displayImages = sys.argv[1] == "True"

    res = imProc.main(path + filename, displayImages)
    with open("results.txt", "a+") as f:
        f.write(filename + ": " + res + "\n")

