import os
from PIL import Image

for file in os.listdir(os.getcwd() + "/Dataset_test"):
    if file.endswith(".txt"):
        img = file.split('.')[0] + ".jpg"
        im = Image.open("Dataset/" + img)
        width, height = im.size 
        linecount = len(open("Dataset/" + file).readlines())
        for line in range(0,linecount):
            f = open("Dataset/"+file)
            content = f.readlines()[line]
            content = content.split(" ")
            x_min,y_min,x_max,y_max =float(content[1]),float(content[2]),float(content[3]),float(content[4])
            area = (x_min,y_min,x_min+width,y_min+height)
            left = width * x_min
            top = width * x_min
            right = width * x_max
            bottom = height * y_max

            testarea = (left,top,right,bottom)
            im1 = im.crop(testarea)
            im1.show()