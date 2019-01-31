import random,sys,os
from decimal import Decimal
import numpy as np

days = ['m','tu','w','th','f']
locations = [3245,1234,7564,1233,312,534,12]


def generateRandomData(amountOfData,dataPath):
    stringToPrint = ["","","",""]
    pickup = -1
    file = open(dataPath+"training.csv", "w")
    file.write("Location,Time,Accessibility,Day,Priority\n")
    for i in range(amountOfData):
        for x in range(5):
            for y in range(6):
                percent = round(Decimal(random.random() * 100), 0)
                stringToPrint[0] = locations[random.randint(0,6)]
                stringToPrint[1] = round(Decimal(random.uniform(0,86400)),0)
                stringToPrint[2] = percent
                stringToPrint[3] = x
                try:
                    global currentMatrix
                    currentMatrix = np.array(stringToPrint)
                except:
                    currentMatrix = np.vstack((currentMatrix,stringToPrint))
                if percent >= 70 and pickup == -1:
                    pickup = x
        try:
            global pastMatrix
            pastMatrix = currentMatrix
        except:
            pastMatrix = np.concatenate((pastMatrix, np.repeat(days[x], 5 * 6)), axis=1)

        try:
            global totalMatrix
            totalMatrix = np.empty((1,5))
        except:
            totalMatrix = np.vstack((totalMatrix,pastMatrix))
        pastMatrix = currentMatrix
        pickup = -1

    file.write(np.array2string(totalMatrix, precision=2, separator=',',suppress_small=True))
    file.close()