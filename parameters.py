path = 'Images/templates/'
fruits = ['apple', 'banana']
templates = []
for fruit in fruits:
    templates.append(path + fruit + 'Template.jpg')

colorThreshold = {
    "apple": {"blue": [0.1, 0.3], "green": [0.2, 0.4], "red": [0.3, 0.7]},
    "banana": {"blue": [0, 0.15], "green": [0.35, 0.45], "red": [0.43, 0.55]}
}

standardColorPattern = {
    'apple': (4, 5, 9),
    'banana': (2, 7, 9)
}

weightSensorCoordinates = [
    (  # first row
        [670, 1100],  # height
        (  # widths
            [0, 1100],
            [1000, 1750],
            [1750, 2592]
        )
    ),
    (  # second row
        [1050, 1650],  # height
        (  # widths
            [0, 1000],
            [900, 1770],
            [1770, 2592]
        )
    ),
    (  # third row
        [1650, 1944],  # height
        (  # widths
            [0, 950],
            [850, 1850],
            [1850, 2592]
        )
    )
]

weightSensorID = {
    (1, 1): 1,
    (1, 2): 4,
    (1, 3): 7,
    (2, 1): 2,
    (2, 2): 5,
    (2, 3): 8,
    (3, 1): 3,
    (3, 2): 6,
    (3, 3): 9
}

weightSensorRange = {
    (1, 1): (
        weightSensorCoordinates[0][1][0][1] -
        weightSensorCoordinates[0][1][0][0],
        weightSensorCoordinates[0][0][1] - weightSensorCoordinates[0][0][0]
    ),  # (horizontal range, vertical range)
    (1, 2): (
        weightSensorCoordinates[0][1][1][1] -
        weightSensorCoordinates[0][1][1][0],
        weightSensorCoordinates[0][0][1] - weightSensorCoordinates[0][0][0]
    ),
    (1, 3): (
        weightSensorCoordinates[0][1][2][1] -
        weightSensorCoordinates[0][1][2][0],
        weightSensorCoordinates[0][0][1] - weightSensorCoordinates[0][0][0]
    ),
    (2, 1): (
        weightSensorCoordinates[1][1][0][1] -
        weightSensorCoordinates[1][1][0][0],
        weightSensorCoordinates[1][0][1] - weightSensorCoordinates[1][0][0]
    ),
    (2, 2): (
        weightSensorCoordinates[1][1][1][1] -
        weightSensorCoordinates[1][1][1][0],
        weightSensorCoordinates[1][0][1] - weightSensorCoordinates[1][0][0]
    ),
    (2, 3): (
        weightSensorCoordinates[1][1][2][1] -
        weightSensorCoordinates[1][1][2][0],
        weightSensorCoordinates[1][0][1] - weightSensorCoordinates[1][0][0]
    ),
    (3, 1): (
        weightSensorCoordinates[2][1][0][1] -
        weightSensorCoordinates[2][1][0][0],
        weightSensorCoordinates[2][0][1] - weightSensorCoordinates[2][0][0]
    ),
    (3, 2): (
        weightSensorCoordinates[2][1][1][1] -
        weightSensorCoordinates[2][1][1][0],
        weightSensorCoordinates[2][0][1] - weightSensorCoordinates[2][0][0]
    ),
    (3, 3): (
        weightSensorCoordinates[2][1][2][1] -
        weightSensorCoordinates[2][1][2][0],
        weightSensorCoordinates[2][0][1] - weightSensorCoordinates[2][0][0]
    )
}
