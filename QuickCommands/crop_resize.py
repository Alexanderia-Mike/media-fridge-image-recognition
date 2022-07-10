import cv2
import numpy as np

from .image_show import image_show
# crop a image according to the largest contour detected and then resize the image to a specific size


def cnt_area(cnt):
    return cv2.contourArea(cnt, True)


# EFFECTS:  first crop and mask the img so that only fruit is centered and background turns black
#           second resize the img to 200*200
# RETURNS:  resizedFrutiOnly: the fruit image resized so that the fruit is centered
#           resizedCroppedMask: binary image, representing the fruit mask
def crop_resize(img):
    # convert to binary to detect contours
    binaryImg = blue_crop_resize(img)
    _, contours, _ = cv2.findContours(
        binaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # select the fruit contour by selecting the contour with the greatest enclosed area
    sortedCnts = sorted(contours, key=cnt_area, reverse=True)

    # making a mask according to the detected contour
    blackMask = np.zeros(img.shape, dtype=np.uint8)  # a black rectangle
    mask1 = cv2.drawContours(
        blackMask.copy(), [sortedCnts[0]], -1, (255, 255, 255), -1)  # with fruit area being white
    mask2 = cv2.drawContours(
        blackMask.copy(), [sortedCnts[1]], -1, (255, 255, 255), -1)  # with fruit area being white
    mask1 = cv2.cvtColor(mask1, cv2.COLOR_BGR2GRAY)  # convert it to gray
    mask2 = cv2.cvtColor(mask2, cv2.COLOR_BGR2GRAY)  # convert it to gray

    # crop the image and the mask so that the fruit are zoomed in and centered
    x1, y1, w1, h1 = cv2.boundingRect(sortedCnts[0])
    x2, y2, w2, h2 = cv2.boundingRect(sortedCnts[1])  # second largest
    croppedImg1 = img[y1:y1+h1, x1:x1+w1]
    croppedMask1 = mask1[y1:y1+h1, x1:x1+w1]
    croppedImg2 = img[y2:y2+h2, x2:x2+w2]
    croppedMask2 = mask2[y2:y2+h2, x2:x2+w2]

    # set the background of the fruit image to white
    fruitOnly1 = cv2.bitwise_and(croppedImg1, croppedImg1, mask=croppedMask1)
    fruitOnly2 = cv2.bitwise_and(croppedImg2, croppedImg2, mask=croppedMask2)

    # resize to 200*200
    resizedFruitOnly = [cv2.resize(
        fruitOnly1, (200, 200)), cv2.resize(fruitOnly2, (200, 200))]
    resizedCroppedMask = [cv2.resize(
        croppedMask1, (200, 200)), cv2.resize(croppedMask2, (200, 200))]

    return (resizedFruitOnly, resizedCroppedMask)


# EFFECTS:  scan an image and find the position of the fruit.
# RETURNS:  returns the coordinates of the upper corner and the width & length of the fruit, <x,y>, w, h
def fruit_position(img):
    binaryImg = blue_crop_resize(img)
    _, contours, _ = cv2.findContours(
        binaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # select the fruit contour by selecting the contour with the greatest enclosed area
    sortedCnts = sorted(contours, key=cnt_area, reverse=True)

    x1, y1, w1, h1 = cv2.boundingRect(sortedCnts[0])
    x2, y2, w2, h2 = cv2.boundingRect(sortedCnts[1])  # second largest
    return [((x1, y1), w1, h1), ((x2, y2), w2, h2)]

# EFFECTS:  calculate the average RGB of the fruit and then detect the contours based on
#           the calculated threshold


def color_pattern_crop_resize(img, color_pattern):
    blackMask = np.zeros(img.shape[:2], dtype=np.uint8)
    width, height, _ = img.shape
    for w in range(width):
        for h in range(height):
            if img[w, h, 0] > color_pattern[0] or img[w, h, 1] > color_pattern[1] or img[w, h, 2] > color_pattern[2]:
                blackMask[w, h] = 2
    retval, binaryImg = cv2.threshold(blackMask, 1, 255, cv2.THRESH_BINARY)
    return binaryImg


def avrBlueBrightness(img):
    sum = cv2.sumElems(img)
    blueSum = sum[0]
    avr_blue = blueSum / img.size
    return avr_blue


def blue_crop_resize(img):
    blueImg, _, _ = cv2.split(img)
    avr_blue_threshold = avrBlueBrightness(img) * 1.8
    _, binaryImg = cv2.threshold(
        blueImg, avr_blue_threshold, 255, cv2.THRESH_BINARY)
    return binaryImg


def is_fruit(img):
    result = [0, 0]
    binaryImg = blue_crop_resize(img)
    _, contours, _ = cv2.findContours(
        binaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # select the fruit contour by selecting the contour with the greatest enclosed area
    sortedCnts = sorted(contours, key=cnt_area, reverse=True)

    width, height = img.shape[:2]
    total_area = width * height
    if cnt_area(sortedCnts[0]) / total_area > 1/50:
        result[0] = 1
    if cnt_area(sortedCnts[1]) / total_area > 1/50:
        result[1] = 1
    return result
