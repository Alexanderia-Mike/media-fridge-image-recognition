import cv2

# colorPatterns = []
# for i in range(5):
#     for j in range(5):
#         for k in range(5):
#             colorPatterns.append({'b': i+1, 'g': j+1, 'r': k+1})


def patternClass(colorValue):
    if colorValue < 225:
        return colorValue // 25 + 1
    else:
        return 10

# find the color pattern that appears the most often in img


def most_often_color_pattern(img):
    width, height = img.shape[:2]
    patternDict = {}
    for w in range(width):
        for h in range(height):
            if not (img[w, h][:] == [0, 0, 0]).all():
                pattern = (
                    patternClass(img[w, h, 0]),
                    patternClass(img[w, h, 1]),
                    patternClass(img[w, h, 2])
                )
                patternDict[pattern] = patternDict.get(pattern, 0) + 1

    most_opten_pattern = []
    time = 0
    for pattern in patternDict:
        if patternDict[pattern] > time:
            time = patternDict[pattern]
            most_opten_pattern = pattern

    return most_opten_pattern
