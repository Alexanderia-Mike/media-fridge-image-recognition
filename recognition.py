import cv2
import numpy as np
# from datetime import datetime
# from datetime import date
import time

from .QuickCommands.crop_resize import crop_resize
from .QuickCommands.crop_resize import fruit_position
from .QuickCommands.image_show import image_show
from .parameters import parameters
from .QuickCommands.mostOftenClrPtn import most_often_color_pattern
from .image_recognition import image_recognition

# img1 = cv2.imread("Images/templates/banana.jpg")
# img2 = cv2.imread("Images/bananas/banana2.jpeg")
# img3 = cv2.imread("Images/bananas/banana3.jpeg")
# img4 = cv2.imread("Images/apples/apple1.jpeg")
# img5 = cv2.imread("Images/apples/apple2.jpg")
# img6 = cv2.imread("Images/templates/apple.jpg")
# img7 = cv2.imread("Images/apples/apple5.jpeg")
# img8 = cv2.imread("Images/apples/apple6.png")
# img9 = cv2.imread("Images/apples/apple7.jpeg")

# images = [img1, img2, img3, img4, img5, img6, img7, img9]

# for i in range(8):
#     if images[i] is None:
#         print('cannot open the image', i+1)
#         exit()
#     print(i, image_recognition(images[i]))
# print(image_recognition(img8))

# ["apple", (100,200), [8, 9], time.time()]

# input:        img is a colored image in numpy array form
# description:  returnValue is a list with two components, each of which is a dictionary corresponding
#               to the recognition result of two fruits, with parameters
#               <type>, <center coordinates>, <weight sensor IDs> and <time>


def main():
    img = cv2.imread("/../src/capture.jpg")
    recognitionResult, _, _ = image_recognition(img)
    fruitPosition1, fruitPosition2 = fruit_position(img)
    # currentTime = date.today().strftime("%d/%m/%y") + " " + \
    # datetime.now().strftime("%H:%M:%S")
    currentTime = int(time.time())
    weightSensorIDs = [
        weightSensorDetection2(
            fruitPosition1[0], fruitPosition1[1], fruitPosition1[2], recognitionResult[0]),
        weightSensorDetection2(
            fruitPosition2[0], fruitPosition2[1], fruitPosition2[2], recognitionResult[1])
    ]
    returnValue = []
    if recognitionResult[0] != "not a fruit":
        returnValue.append(
            {
                "type": recognitionResult[0],
                "center coordinates": (
                    fruitPosition1[0][0] + fruitPosition1[1]/2,
                    fruitPosition1[0][1] + fruitPosition1[2]/2
                ),
                "weight sensor IDs": weightSensorIDs[0],
                "time": currentTime
            }
        )
    if recognitionResult[1] != "not a fruit":
        returnValue.append(
            {
                "type": recognitionResult[1],
                "center coordinates": (
                    fruitPosition2[0][0] + fruitPosition2[1]/2,
                    fruitPosition2[0][1] + fruitPosition2[2]/2
                ),
                "weight sensor IDs": weightSensorIDs[1],
                "time": currentTime
            }
        )
    return returnValue


# input:        center coordinates and height & width of the fruit: (x, y), w, h
# description:  return the ID of the weight sensors that is pressed by the fruit
# the recognition conditions:
#       first row:    height  [770, 1200]
#           (1, 1): width [0, 1000];    (1, 2): width [1000, 1700];     (1, 3): width [1700, 2592]
#       second row:   height  [1200, 1770]
#           (2, 1): width [0, 900];     (2, 2): width [900, 1700];      (2, 3): width [1700, 2592]
#       third row:    height  [1770, 1944]
#           (3, 1): width [0, 850];     (3, 2): width [850, 1740];      (3, 3): width [1740, 2592]


def weightSensorDetection2(coordinates, width, height, type):
    weightSensorCoordinates = parameters.weightSensorCoordinates
    x = coordinates[0] + width / 2
    y = coordinates[1] + height / 2
    leftEnd = 0
    rightEnd = 0
    if type == "apple":
        leftEnd = x - width / 2
        rightEnd = x + width / 2
    else:
        leftEnd = x - width / 2
        rightEnd = x + width / 2
    altitudeUp = y + height / 4
    altitudeBottom = y + height / 2

    IDList = []
    columnBoundaryList = []
    rowNumList = []
    leftColumnNum = 0
    rightColumnNum = 0
    UpRowNum = 0
    DownRowNum = 0

    if altitudeUp < weightSensorCoordinates[0][0][1] and weightSensorCoordinates[0][0][1] - altitudeUp > parameters.weightSensorRange[(1, 1)][1]/4:
        UpRowNum = 1
    elif altitudeUp < weightSensorCoordinates[1][0][1] and weightSensorCoordinates[1][0][1] - altitudeUp > parameters.weightSensorRange[(2, 1)][1]/4:
        UpRowNum = 2
    else:
        UpRowNum = 3

    if altitudeBottom > weightSensorCoordinates[1][0][1] and altitudeBottom - weightSensorCoordinates[1][0][1] > parameters.weightSensorRange[(3, 1)][1]/4:
        DownRowNum = 3
    elif altitudeBottom > weightSensorCoordinates[0][0][1] and altitudeBottom - weightSensorCoordinates[0][0][1] > parameters.weightSensorRange[(2, 1)][1]/4:
        DownRowNum = 2
    else:
        DownRowNum = 1

    rowNum = UpRowNum
    while rowNum <= DownRowNum:
        columnBoundaryList.append(weightSensorCoordinates[rowNum - 1][1])
        rowNumList.append(rowNum)
        rowNum = rowNum + 1

    for row, columnBoundary in zip(rowNumList, columnBoundaryList):
        if leftEnd < columnBoundary[0][1] and columnBoundary[0][1] - leftEnd > parameters.weightSensorRange[(row, 1)][0]/8:
            leftColumnNum = 1
        elif leftEnd < columnBoundary[1][1] and columnBoundary[1][1] - leftEnd > parameters.weightSensorRange[(row, 2)][0]/8:
            leftColumnNum = 2
        else:
            leftColumnNum = 3

        if rightEnd > columnBoundary[2][0] and rightEnd - columnBoundary[2][0] > parameters.weightSensorRange[(row, 3)][0]/8:
            rightColumnNum = 3
        elif rightEnd > columnBoundary[1][0] and rightEnd - columnBoundary[1][0] > parameters.weightSensorRange[(row, 2)][0]/8:
            rightColumnNum = 2
        else:
            rightColumnNum = 1

        if rightColumnNum < leftColumnNum:
            print("error!")
            exit()

        column = leftColumnNum
        while column <= rightColumnNum:
            IDList.append(parameters.weightSensorID[(row, column)])
            column = column + 1

    return IDList
