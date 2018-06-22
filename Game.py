import matplotlib.pyplot as plt
import sympy
import numpy
import math
import Ball

widthM = 0
lengthN = 0
wallCoordinates = None
bounces = 0
myBall = Ball.Ball()
direction = None

def game():
    global bounces
    global widthM
    global lengthN
    global wallCoordinates
    global direction
    a = 0
    b = 0
    intersectionCounter = 0
    intersectionArray = []
    intersectionArrayValueStore = ""
    inputValue = input("Please enter the values of <Width> <Length> <Px> <Py> <Qx> <Qy>. Please seperate values by one space").split(" ")
    if int(inputValue[0]) < 0:
        print("Width of a Rectangle cannot be negative. The value you have entered has been converted to a positive number.")
        newInput1 = int(inputValue[0])*-1
    elif int(inputValue[0]) == 0:
        print("Width of a rectangle cannot be zero. Unable to Predict a Fix. Please re-enter your values again")
        game()
        return
    elif int(inputValue[0]) > 0:
        newInput1 = int(inputValue[0])
    if int(inputValue[1]) < 0:
        print("Length of a Rectangle cannot be negative. The value you have entered has been converted to a positive number.")
        newInput2 = int(inputValue[1]) * -1
    elif int(inputValue[1]) == 0:
        print("Length of a rectangle cannot be zero. Unable to Predict a Fix. Please re-enter your values again")
        game()
        return
    elif int(inputValue[1]) > 0:
        newInput2 = int(inputValue[1])

    widthM = min(newInput1,newInput2)  # Throw an exception if the value is negative
    lengthN = max(newInput1, newInput2)
    pX = float(inputValue[2])
    pY = float(inputValue[3])
    qX = float(inputValue[4])
    qY = float(inputValue[5])
    wallCoordinates = [[0, 0], [widthM, 0], [widthM, lengthN], [0, lengthN]]
    direction = "Anti Clock"
    start(widthM, widthM)
    while(inHole() == False):
        nextLocation = getNextLocation(int(myBall.getCurrentX()), int(myBall.getCurrentY()), int(myBall.getPreviousX()), int(myBall.getPreviousY()))
        myBall.addNewX(nextLocation[0])
        myBall.addNewY(nextLocation[1])
        if(inHole() == False):
            bounces = bounces + 1
    coordinates = myBall.getCoordiantes()
    printCoordiantes = myBall.printCoordinates()
    while a < len(coordinates) -1:
        intersectionArray.append(wallIntersection(pX, pY, qX, qY, coordinates[a][0], coordinates[a][1], coordinates[a+1][0], coordinates[a+1][1]))
        a = a + 1
    while b < len(intersectionArray):
        if intersectionArray[b] != []:
            intersectionCounter = intersectionCounter + 1
            intersectionArrayValueStore = intersectionArrayValueStore + "[" + str(intersectionArray[b][0]) + "," + str(intersectionArray[b][1]) + "]" + " "
        b = b + 1
    print("Total Path:" + printCoordiantes[0])
    print("Collision Points" + printCoordiantes[1])
    print("bounces:" + " " + str(bounces))
    print("Intersection Points:" + intersectionArrayValueStore)
    print("Total Number of Intersection Points:" + str(intersectionCounter))
    plotPath()
    return

def plotPath():
    print("HERE")
    global widthM
    global lengthN
    a = 0
    xs = [0, widthM, widthM, 0, 0]
    ys = [0,0, lengthN, lengthN, 0]
    plt.axis('equal')
    coordinates = myBall.getCoordiantes()
    for i in range(4):
        plt.xlim(-1, widthM + 1)
        plt.ylim(-1, lengthN + 1)
        x0, x1 = xs[i], xs[i+1]
        y0, y1 = ys[i], ys[i+1]
        plt.plot([x0,x1], [y0,y1])
        plt.draw()
    while a < len(coordinates) - 1:
        plt.ylim(0, lengthN)
        plt.plot([coordinates[a][0], coordinates[a+1][0]], [coordinates[a][1], coordinates[a+1][1]])
        plt.pause(1)
        plt.draw()
        a = a + 1
    plt.show()
    return
def collinear(aX,aY,bX, bY, cX, cY):
    if math.isclose(aX * (bY - cY) + bX * (cY - aY) + cX * (aY - bY), 0, rel_tol = 1e-8, abs_tol = 0):
        return True
    else:
        return False


# aX and aY is the current location of the ball
def getWall(aX, aY):
    global wallCoordinates
    if collinear(aX, aY, wallCoordinates[0][0], wallCoordinates[0][1], wallCoordinates[1][0], wallCoordinates[1][1]):
        return "Bottom Wall"
    elif collinear(aX, aY, wallCoordinates[1][0], wallCoordinates[1][1], wallCoordinates[2][0],wallCoordinates[2][1]):
        return "Right Wall"
    elif collinear(aX, aY, wallCoordinates[2][0], wallCoordinates[2][1], wallCoordinates[3][0], wallCoordinates[3][1]):
        return "Top Wall"
    elif collinear(aX, aY, wallCoordinates[3][0], wallCoordinates[3][1], wallCoordinates[0][0],wallCoordinates[0][1]):
        return "Left Wall"


# aX, aY is the current location and bX, bY is the previous location
def getBaseVector(currentX,currentY,previousX,previousY):
    global widthM
    global lengthN
    if getWall(currentX, currentY) == "Right Wall":
        if direction == "Anti Clock":
            return [(widthM - currentX), (lengthN - currentY)]
        elif direction == "Clock":
            return [(currentX - widthM), (0 - currentY)]
    elif getWall(currentX, currentY) == "Top Wall":
        if direction == "Clock":
            return [(widthM - currentX), (lengthN - currentY)]
        if direction == "Anti Clock":
            return [(0 - currentX), (lengthN - currentY)]
    elif getWall(currentX, currentY) == "Left Wall":
        if direction == "Anti Clock":
            return [(0 - currentX), (0 - currentY)]
        elif direction == "Clock":
            return [(0 - currentX), (lengthN - currentY)]
    elif getWall(currentX, currentY) == "Bottom Wall":
        if direction == "Clock":
            return [(0 - currentX), (0 - currentY)]
        if direction == "Anti Clock":
            return [(widthM - currentX), (currentY - 0)]

def wallIntersection(aX, aY, bX, bY, w1X, w1Y, w2X, w2Y):
    intersectionPoint = []
    if numpy.cross([bX-aX, bY-aY], [w2X - w1X, w2Y - w1Y]) != 0:
        s, t = sympy.symbols('s t')
        solve = sympy.solve([s*(w2X - w1X) - t*(bX - aX) - aX + w1X, s*(w2Y - w1Y) - t*(bY - aY) - aY + w1Y], dict = True)
        #print(float(solve[0][t]))
        #print(float(solve[0][s]))
        parameters = [float(solve[0][s]), float(solve[0][t])]

        if parameters[0] <=1 and parameters[1] <=1:
            intersectionPoint = [aX + parameters[1]*(bX - aX), aY + parameters[1]*(bY - aY)]
            return intersectionPoint
        else:
            return []
    else:
        return []



def getNextLocation(currentX, currentY, previousX, previousY):
    global wallCoordinates
    global widthM
    global lengthN
    global direction
    baseVector = getBaseVector(currentX, currentY, previousX, previousY)
    x, y = sympy.symbols('x y')
    if direction == "Anti Clock":
        solve = sympy.solve([((x - currentX) * baseVector[0]) + ((y - currentY) * baseVector[1]) -
                         baseVector[0]**2 - baseVector[1]**2,
                         ((x - currentX)*baseVector[1]*(-1)) + ((y-currentY)*baseVector[0]*(1)) - baseVector[0]**2 - baseVector[1]**2], dict = True)
    else:
        solve = sympy.solve([((x - currentX) * baseVector[0]) + ((y - currentY) * baseVector[1]) -
                             baseVector[0] ** 2 - baseVector[1] ** 2,
                             ((x - currentX) * baseVector[1] * 1) - ((y - currentY) * baseVector[0] * 1) - baseVector[
                                 0] ** 2 - baseVector[1] ** 2], dict=True)
    locationArray = [(float(solve[0][x])), (float(solve[0][y]))]
    if locationArray[0] > widthM:
        if locationArray[1] - currentY < 0:
            direction = "Clock"
            return wallIntersection(currentX, currentY, locationArray[0], locationArray[1], wallCoordinates[1][0], wallCoordinates[1][1], wallCoordinates[2][0], wallCoordinates[2][1])
        elif locationArray[1] - currentY > 0:
            direction = "Anti Clock"
            return wallIntersection(currentX, currentY, locationArray[0], locationArray[1], wallCoordinates[1][0], wallCoordinates[1][1], wallCoordinates[2][0], wallCoordinates[2][1])
    elif locationArray[0] < 0:
        if locationArray[1] - currentY <0:
            direction = "Anti Clock"
            return  wallIntersection(currentX, currentY, locationArray[0], locationArray[1], wallCoordinates[3][0], wallCoordinates[3][1], wallCoordinates[0][0], wallCoordinates[0][1])
        elif locationArray[1] - currentY >0:
            direction = "Clock"
            return wallIntersection(currentX, currentY, locationArray[0], locationArray[1], wallCoordinates[3][0],wallCoordinates[3][1], wallCoordinates[0][0], wallCoordinates[0][1])
    elif locationArray[1] > lengthN:
        if locationArray[0] - currentX > 0:
            direction = "Clock"
            return wallIntersection(currentX, currentY, locationArray[0], locationArray[1], wallCoordinates[2][0], wallCoordinates[2][1], wallCoordinates[3][0], wallCoordinates[3][1])
        elif locationArray[0] - currentX < 0:
            direction = "Anti Clock"
            return wallIntersection(currentX, currentY, locationArray[0], locationArray[1], wallCoordinates[2][0], wallCoordinates[2][1], wallCoordinates[3][0], wallCoordinates[3][1])
    elif locationArray[1] < 0:
        if locationArray[0] - currentX < 0:
            direction = "Clock"
            return wallIntersection(currentX, currentY, locationArray[0], locationArray[1], wallCoordinates[0][0], wallCoordinates[0][1], wallCoordinates[1][0], wallCoordinates[1][1])
        elif locationArray[0] - currentX > 0:
            direction = "Anti Clock"
            return wallIntersection(currentX, currentY, locationArray[0], locationArray[1], wallCoordinates[0][0], wallCoordinates[0][1], wallCoordinates[1][0], wallCoordinates[1][1])
    else:
        return locationArray


def inHole():
    global widthM
    global lengthN
    if (math.isclose(int(myBall.getCurrentX()), 0, rel_tol = 1e-8) and math.isclose(int(myBall.getCurrentY()), 0, rel_tol =1e-8) \
            or (math.isclose(int(myBall.getCurrentX()), widthM, rel_tol=1e-8) and math.isclose(int(myBall.getCurrentY()), 0, rel_tol = 1e-8)) \
            or (math.isclose(int(myBall.getCurrentX()), widthM, rel_tol=1e-8) and math.isclose(int(myBall.getCurrentY()), lengthN, rel_tol = 1e-8))  \
            or (math.isclose(int(myBall.getCurrentX()), 0, rel_tol=1e-8) and math.isclose(int(myBall.getCurrentY()), lengthN, rel_tol = 1e-8))):
        return True
    else:
        return False


def start(a, b):
    global bounces
    myBall.addNewX(a)
    myBall.addNewY(b)
    bounces = bounces + 1


if __name__ == '__main__':
    game()




