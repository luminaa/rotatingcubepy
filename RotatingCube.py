import math
import time
import os
import sys

timeperframe = 1
width, height = 120, 36        # size of the cube
scalex = (width - 4) // 8
scaley = (height - 4) // 8
scaley *= 2
translateX = (width - 4) // 2
translateY = (height - 4) // 2

LINE_CHAR = "+"                 # this will create the lines of the cube

xRotationSpeed = 0.03
yRotationspeed = 0.06
zRotationSpeed = 0.09

X = 0
Y = 1
Z = 2


def line(x1, y1, x2, y2):
    points = [] 

    if (x1 == x2 and y1 == y2 + 1) or (y1 == y2 and x1 == x2 + 1):
        return [(x1, y1), (x2, y2)]

    is_steep = abs(y2 - y1) > abs(x2 - x1)  # line is steep if the basic angle of the line is more than 45° 
    if is_steep:    # change from steep to non-steep so that the algorithm can handle it
        x1, y1 = y1, x1  
        x2, y2 = y2, x2

    is_reversed = x1 > x2 

    if is_reversed:     # if points is going from rigth to left, it swaps it to go from left to right
        x1, x2 = x2, x1 
        y1, y2 = y2, y1  

        dx = x2 - x1
        dy = abs(y2 - y1)
        ey = int(dx / 2)
        cy = y2

        if y1 < y2: 
            ydirection = 1
        else:
            ydirection = -1

        for cx in range(x2, x1 - 1, -1):
            if is_steep:
                points.append((cy, cx))
            else:
                points.append((cx, cy))
            ey -= dy
            if ey <= 0:  
                cy -= ydirection
                ey += dx
    else:  # Get the points on the line going left to right.
        dx = x2 - x1
        dy = abs(y2 - y1)
        ey = int(dx / 2)
        cy = y1
        if y1 < y2:
            ydirection = 1
        else:
            ydirection = -1
        # Calculate the y for every x in this line:
        for cx in range(x1, x2 + 1):
            if is_steep:
                points.append((cy, cx))
            else:
                points.append((cx, cy))
            ey -= dy
            if ey < 0:  # Only change y once extray < 0.
                cy += ydirection
                ey += dx
    return points


def rotate_point(x, y, z, ax, ay, az):

    # x axis:
    rotated_x = x
    rotated_y = (y * math.cos(ax)) - (z * math.sin(ax))
    rotated_z = (y * math.sin(ax)) + (z * math.cos(ax))
    x, y, z = rotated_x, rotated_y, rotated_z

    # y axis:
    rotated_x = (z * math.sin(ay)) + (x * math.cos(ay))
    rotated_y = y
    rotated_z = (z * math.cos(ay)) - (x * math.sin(ay))
    x, y, z = rotated_x, rotated_y, rotated_z

    # z axis:
    rotated_x = (x * math.cos(az)) - (y * math.sin(az))
    rotated_y = (x * math.sin(az)) + (y * math.cos(az))
    rotated_z = z

    return (rotated_x, rotated_y, rotated_z)


def adjustPoint(point):
    return (int(point[X] * scalex + translateX),
            int(point[Y] * scaley + translateY))

cubecorners = [[-1, -1, -1], [ 1, -1, -1], [-1, -1,  1], [ 1, -1,  1], [-1,  1, -1], [ 1,  1, -1], [-1,  1,  1], [ 1,  1,  1]]

rotatedCorners = [None, None, None, None, None, None, None, None]

xRotation = 0.0
yRotation = 0.0
zRotation = 0.0

try:
    while True:
        xRotation += xRotationSpeed
        yRotation += yRotationspeed
        zRotation += zRotationSpeed
        for i in range(len(cubecorners)):
            x = cubecorners[i][X]
            y = cubecorners[i][Y]
            z = cubecorners[i][Z]
            rotatedCorners[i] = rotate_point(x, y, z, xRotation,
                yRotation, zRotation)

        cubePoints = []
        for fromCornerIndex, toCornerIndex in ((0, 1), (1, 3), (3, 2), (2, 0), (0, 4), (1, 5), (2, 6), (3, 7), (4, 5), (5, 7), (7, 6), (6, 4)):
            fromX, fromY = adjustPoint(rotatedCorners[fromCornerIndex])
            toX, toY = adjustPoint(rotatedCorners[toCornerIndex])
            pointsOnLine = line(fromX, fromY, toX, toY)
            cubePoints.extend(pointsOnLine)

        cubePoints = tuple(frozenset(cubePoints))

        for y in range(height):
            for x in range(width):
                if (x, y) in cubePoints:
                    print(LINE_CHAR, end='', flush=False)
                else:
                    print(' ', end='', flush=False)
            print(flush=False)
        print('Press Ctrl-C to quit.', end='', flush=True)

        time.sleep(timeperframe)

        os.system('cls')

except KeyboardInterrupt:
    os.system('cls')
    print('STOPPED')
    sys.exit()
