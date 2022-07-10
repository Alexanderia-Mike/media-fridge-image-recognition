import cv2
import matplotlib.pyplot as plt
import numpy as np


def color_weight(img):
    bImg, gImg, rImg = cv2.split(img)
    sum = np.zeros(bImg.shape, dtype=np.uint16)
    sum = sum + bImg + rImg + gImg + np.uint16(1)

    bWeight = bImg / sum
    gWeight = gImg / sum
    rWeight = rImg / sum

    return (bWeight, gWeight, rWeight)
