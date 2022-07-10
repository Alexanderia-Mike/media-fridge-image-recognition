import cv2
import matplotlib.pyplot as plt
import numpy as np

from .QuickCommands.crop_resize import crop_resize
from .QuickCommands.crop_resize import fruit_position
from .QuickCommands.crop_resize import is_fruit
from .QuickCommands.image_show import image_show
from .parameters import parameters
from .QuickCommands.mostOftenClrPtn import most_often_color_pattern


# EFFECTS:  recognize the fruit in image by comparing it's outlines with the outlines of templates.
# RETURNS:  a dictionary <resultDict> that shows the similarity of colors between the fruit in the
#           image and the fruit templates
def shape_match(img):
    _, croppedBinaryImg = crop_resize(img)
    resultDict1 = {}
    resultDict2 = {}
    for fruit, templateStr in zip(parameters.fruits, parameters.templates):
        # the template to be compared with
        template = cv2.imread(templateStr, cv2.IMREAD_GRAYSCALE)
        resultDict1[fruit] = cv2.matchTemplate(
            croppedBinaryImg[0], template, cv2.TM_SQDIFF_NORMED)[0][0]
        resultDict2[fruit] = cv2.matchTemplate(
            croppedBinaryImg[1], template, cv2.TM_SQDIFF_NORMED)[0][0]  # match the template and store the result
    return [resultDict1, resultDict2]


# EFFECTS:  match the color of an image with the templates in terms of the most often color pattern
#           of RBG.
# RETURNS:  a dictionary <resultDict> that shows the similarity of colors between the fruit in the
#           image and the fruit templates
def color_match_mostOftClr(img):
    # match the color of the image with the color of the fruit templates.
    # the colors are compared through the color pattern that appears the most often among all pixels
    selImg, _ = crop_resize(img)
    mstOftnClrPtn = [most_often_color_pattern(
        selImg[0]), most_often_color_pattern(
        selImg[1])]  # return the most often color pattern
    resultDict1 = {}
    resultDict2 = {}
    for fruit in parameters.fruits:
        stdClrPtn = parameters.standardColorPattern[fruit]
        error1 = error2 = 0
        for i in range(3):
            error1 = error1 + (mstOftnClrPtn[0][i] - stdClrPtn[i]) ** 2
            error2 = error2 + (mstOftnClrPtn[1][i] - stdClrPtn[i]) ** 2
            # calculate the error based on the square of the difference
        resultDict1[fruit] = error1
        resultDict2[fruit] = error2
    return [resultDict1, resultDict2]


# EFFECTS:  return the least two values inside the DICTIONARY result, along with their corresponding indices
def minimums(result):
    index1 = 0  # the index of the least value
    value1 = None  # the least value
    index2 = 0  # the index of the second least value
    value2 = None  # the second least value
    i = 0
    for fruit in parameters.fruits:
        if value1 is None:
            value1 = result[fruit]
        elif result[fruit] < value1:
            value2 = value1
            index2 = index1
            value1 = result[fruit]
            index1 = i
        else:
            if value2 is None:
                value2 = result[fruit]
                index2 = i
            elif result[fruit] < value2:
                value2 = result[fruit]
                index2 = i
        i = i+1
    return (index1, value1, index2, value2)


def recognition_helper(shapeValue1, shapeValue2, colorValue1, colorValue2, shapeIndex1, shapeIndex2, colorIndex1, colorIndex2):
    result = ""
    method = ""
    certainty = 0

    if shapeValue2 / shapeValue1 > colorValue2 / colorValue1:
        if shapeValue1 < 0.5:
            method = "shape"
            if shapeValue2 > 0.8:  # the result is quite clear
                result = parameters.fruits[shapeIndex1]
                certainty = 1
            elif shapeValue2 < 0.6:  # both of two are possible
                result = parameters.fruits[shapeIndex1] if shapeValue1 < shapeValue2 else parameters.fruits[shapeIndex2]
                certainty = 0.3
            else:
                result = parameters.fruits[shapeIndex1]
                certainty = 0.7
        else:  # cannot really tell what the fruit is according to its shape
            method = "color"
            if colorValue1 < 10:
                if colorValue2 - colorValue1 > 6:  # quite sure through the color
                    result = parameters.fruits[colorIndex1]
                    certainty = 1
                elif colorValue2 - colorValue1 < 3:  # both of two are possible
                    result = parameters.fruits[colorIndex1] if colorValue1 < colorValue2 else parameters.fruits[colorIndex2]
                    certainty = 0.3
                else:
                    result = parameters.fruits[colorIndex1]
                    certainty = 0.7
            else:
                result = parameters.fruits[colorIndex1] if colorValue1 < colorValue2 else parameters.fruits[colorIndex2]
                certainty = 0
    else:
        if colorValue1 < 10:
            method = "color"
            if colorValue2 - colorValue1 > 6:  # quite sure through the color
                result = parameters.fruits[colorIndex1]
                certainty = 1
            elif colorValue2 - colorValue1 < 3:  # both of two are possible
                result = parameters.fruits[colorIndex1] if colorValue1 < colorValue2 else parameters.fruits[colorIndex2]
                certainty = 0.3
            else:
                result = parameters.fruits[colorIndex1]
                certainty = 0.7
        else:
            method = "shape"
            if shapeValue1 < 0.5:
                if shapeValue2 > 0.8:  # the result is quite clear
                    result = parameters.fruits[shapeIndex1]
                    certainty = 1
                elif shapeValue2 < 0.6:  # both of two are possible
                    result = parameters.fruits[shapeIndex1] if shapeValue1 < shapeValue2 else parameters.fruits[shapeIndex2]
                    certainty = 0.3
                else:
                    result = parameters.fruits[shapeIndex1]
                    certainty = 0.7
            else:
                result = parameters.fruits[colorIndex1] if colorValue1 < colorValue2 else parameters.fruits[colorIndex2]
                certainty = 0
    return (result, method, certainty)


# EFFECTS:  recognize the image based on the results returned by shape match and
#           color match (most often color pattern methods)
# EXPLANATION:  the second output would be the method upon which the program makes the judgement
#               the third output shows how certain the program is on the result
def image_recognition(img):
    isFruit = is_fruit(img)
    if isFruit[0] == 0:
        return (['not a fruit', 'not a fruit'], ['none', 'none'], [0, 0])
    shapeResult = shape_match(img)
    colorResult = color_match_mostOftClr(img)
    shapeIndex11, shapeValue11, shapeIndex12, shapeValue12 = minimums(
        shapeResult[0])
    colorIndex11, colorValue11, colorIndex12, colorValue12 = minimums(
        colorResult[0])
    shapeIndex21, shapeValue21, shapeIndex22, shapeValue22 = minimums(
        shapeResult[1])
    colorIndex21, colorValue21, colorIndex22, colorValue22 = minimums(
        colorResult[1])
    result1, method1, certainty1 = recognition_helper(
        shapeValue11, shapeValue12, colorValue11, colorValue12, shapeIndex11, shapeIndex12, colorIndex11, colorIndex12)
    if isFruit[1] == 1:
        result2, method2, certainty2 = recognition_helper(
            shapeValue21, shapeValue22, colorValue21, colorValue22, shapeIndex21, shapeIndex22, colorIndex21, colorIndex22)
    else:
        result2 = "not a fruit"
        method2 = "none"
        certainty2 = 0

    result = [result1, result2]
    method = [method1, method2]
    certainty = [certainty1, certainty2]

    return (result, method, certainty)
