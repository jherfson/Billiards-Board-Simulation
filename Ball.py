class Ball(object):


    def __init__(self):
        self.xValues = [0]
        self.yValues = [0]


    def getCurrentX(self):

        return self.xValues[len(self.xValues)-1]

    def getCurrentY(self):
        return self.yValues[len(self.yValues) -1]

    def getPreviousX(self):
        return self.xValues[len(self.xValues) -2]

    def getPreviousY(self):
        return self.yValues[len(self.yValues) -2]

    def addNewX(self, i):
        self.xValues.append(i)
        return

    def addNewY(self,i):
        self.yValues.append(i)

    def printCoordinates(self):
        strValue = ""
        strValue2 = ""
        a = 1
        while a<len(self.xValues) - 1:
            strValue2 = strValue2 + "[" + str(self.xValues[a]) + "," + str(self.yValues[a]) + "]" + " "
            a = a+1
        for x,y in zip(self.xValues, self.yValues):
            strValue = strValue + "[" + str(x) + "," + str(y) + "]" + " "
        return [strValue, strValue2]

    def getCoordiantes(self):
        coordinatesArray = []
        for x, y in zip(self.xValues, self.yValues):
            coordinatesArray.append([x,y])
        return coordinatesArray












