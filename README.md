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

