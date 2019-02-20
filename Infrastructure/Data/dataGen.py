import random, sys, os
from decimal import Decimal
import numpy as np
import pandas as pd

# Day array
days = ['m', 'tu', 'w', 'th', 'f']
# Possible location distances
locations = [3245, 1234, 7564, 1233, 312, 534, 12]


def generateRandomTrainingData(amountOfData, dataPath, mean=2, standardDeviation=1):
    '''
    This function is a way to generate random data based on a realistic manner. The Accessibility factor is based on
    a randomized cumulative weekly model. This function attempts to simulate real world data using log-normal distribution.
    The parameters for the distribution can be altered by setting the parameters :param mean and :param standardDeviation
    :param amountOfData: Amount of weeks to cycle through for random data
    :param dataPath: The location of the csv data file
    :param mean: The expected day of highest increase in accessibility.
    :param standardDeviation: The error/spread in the normal distribution for the percent increase distribution
    :return: none
    '''
    # Set percent values for each location
    percentArray = [0] * len(locations)
    # Set data point
    stringToPrint = ["", "", "", ""]
    # Set pickup day index
    pickup = -1
    # Global variables to keep track of data and correct label
    global currentMatrix
    global pastMatrix
    global totalMatrix
    # loop for number of weeks
    for i in range(amountOfData):
        # loop for all days of the week
        for x in range(5):
            # Loop for all possible sensor locations
            for y in range(6):
                # Cumulative percent with added randomness
                percentArray[y] += round(Decimal((random.normalvariate(mean, standardDeviation) / 5) * 100), 2)
                # make random data
                stringToPrint[0] = locations[random.randint(0, 6)]
                stringToPrint[1] = round(Decimal(random.uniform(0, 86400)), 2)
                stringToPrint[2] = percentArray[y] if percentArray[y] <= 100 else 0 if percentArray[y] < 0 else 100
                stringToPrint[3] = x
                print(stringToPrint[2])
                # Create present data matrix
                try:
                    currentMatrix = np.vstack((currentMatrix, stringToPrint))
                except:
                    currentMatrix = np.array(stringToPrint)
                # check if threshold is met to label past week
                if percentArray[y] >= 70 and pickup == -1:
                    # Reset precentArray
                    percentArray = [0] * len(locations)
                    pickup = x

        # Setup past matrix based on present matrix and last week label
        try:
            pastMatrix = np.hstack((pastMatrix, np.repeat(days[pickup], 5 * 6).reshape((30, 1))))
        except NameError as namerr:
            print(namerr)
            pastMatrix = currentMatrix
        # Setup total matrix to print to csv
        try:
            totalMatrix = np.vstack((totalMatrix, pastMatrix))
        except NameError as namerr:
            print(namerr)
            totalMatrix = np.empty((1, 5))
        # reset past matrix
        pastMatrix = currentMatrix
        # reset current matrix
        currentMatrix = None
        # reset pickup day
        pickup = -1
        # Reset precentArray
        percentArray = [0] * len(locations)
    # Data frame and print to csv file after done generating data
    df = pd.DataFrame(totalMatrix)
    df = df.iloc[1:]
    df.columns = ["Location", "Time", "Accessibility", "Day", "Priority"]
    df.to_csv(dataPath + "training.csv", index=False)


if __name__ == '__main__':
    generateRandomTrainingData(24, "")
