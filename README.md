### Introduction

This project is able to detect the categories and the locations of fruits based on a provided image. The image processing is implemented through the tool package OpenCV2.


### Usage

name the image to be detected as "capture.jpg", and put the image into the file "./src/". Then run the function `main()` and a dictionary in the format of 

```
{
    "type": TYPE,
    "center coordinates": (X, Y),
    "weight sensor IDs": WEIGHT_ID,
    "time": CURRENT_TIME
}
```
which tells the category of the fruit `TYPE` (apple, banana, etc.), the location of the fruit `(X, Y)`, and the current time `TIME`. The third argument `WEIGHT_ID` is used to pinpoint the weight sensors that is beneath that fruit, and later another program that has access to all weight sensor data will use this parameter to identify the weight of this fruit.


### Files

- "image_recognition.py": some helper functions, including the functions to do the shape matching, color matching, and some intermediate calculation helpers.
- "parameters.py": some constant parameters, such as the threshold to do binarization, weight sensor locations and so on.
- "recognition.py": the main function and some helper functions
- "QuickCommands/": some frequently used tools such as image cropping and resizing and so on.
