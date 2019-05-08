import random, sys, os
from decimal import Decimal
import numpy as np
import pandas as pd
import database
from math import sin, cos, sqrt, atan2, radians, pi
import datetime, calendar
import matplotlib.pyplot as plt
from collections import Counter

# Day array
days = ['m', 'tu', 'w', 'th', 'f']
# Possible location distances
locations = [3245, 1234, 7564, 1233, 312, 534, 12, 24524, 453]


def generateRandomTrainingData(amountOfData, sql, plot=False, mean=1.4, standardDeviation=0.27,
                               coordinate=[(-79.3652141, 43.64631791), (-79.38645152, 43.65184241),
                                           (-79.3708487, 43.66110569), (-79.38603076, 43.67209961),
                                           (-79.36808013, 43.67084828), (-79.39342123, 43.65591903),
                                           (-79.38909398, 43.67188004), (-79.46744499, 42.64582615),
                                           (-79.40361049, 43.65204426)],inital = (43.652042, -79.403610)):
    '''
    This function is a way to generate random data based on a realistic manner. The Accessibility factor is based on
    a randomized cumulative weekly model. This function attempts to simulate real world data using log-normal distribution.
    The parameters for the distribution can be altered by setting the parameters :param mean and :param standardDeviation
    :param amountOfData: Amount of weeks to cycle through for random data
    :param mean: The expected day of highest increase in accessibility.
    :param standardDeviation: The error/spread in the normal distribution for the percent increase distribution
    :return: none
    '''
    # Df data for graphing distribution
    dfp = pd.DataFrame()
    # Set percent values for each location
    percentArray = [0] * len(locations)
    # Set data point
    stringToPrint = ["", "", "", "", "", "", "", ""]
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
            for y in range(len(locations)):
                # Cumulative percent with added randomness
                p = np.random.lognormal(mean, standardDeviation)
                if p < 0:
                    p = 0
                percentArray[y] += round(Decimal((1 / (p + 1))), 4)
                # make random data
                a = random.randint(0, 8)
                stringToPrint[0] = getDistance(coordinate[a],inital)
                stringToPrint[1] = round(Decimal(random.uniform(0, 86400)), 2)
                if percentArray[y] > 1:
                    stringToPrint[2] = 1
                    if plot:
                        # Add data for plotting distribution
                        dfp = dfp.append(pd.DataFrame([{'p': p, 'c': 1}]))
                else:
                    stringToPrint[2] = percentArray[y]
                    if plot:
                        # Add data for plotting distribution
                        dfp = dfp.append(pd.DataFrame([{'p': p, 'c': percentArray[y]}]))
                stringToPrint[3] = random.randint(0, 12)
                stringToPrint[4] = x
                stringToPrint[5] = coordinate[a][0]
                stringToPrint[6] = coordinate[a][1]
                stringToPrint[7] = datetime.datetime.now()
                print(str(stringToPrint[2])+"\t"+str(p))
                # Create present data matrix
                try:
                    currentMatrix = np.vstack((currentMatrix, stringToPrint))
                except:
                    currentMatrix = np.array(stringToPrint)
                # check if threshold is met to label past week
                if percentArray[y] >= 0.7 and pickup == -1:
                    # Reset precentArray
                    percentArray = [0] * len(locations)
                    pickup = x

        # Setup past matrix based on present matrix and last week label
        try:
            pastMatrix = np.hstack((pastMatrix, np.repeat(days[pickup], 5 * len(locations)).reshape((5*len(locations), 1))))
        except NameError as namerr:
            print(namerr)
            pastMatrix = currentMatrix
        # Setup total matrix to print to csv
        try:
            totalMatrix = np.vstack((totalMatrix, pastMatrix))
        except NameError as namerr:
            print(namerr)
            totalMatrix = np.empty((1, 9))
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
    df.columns = ["distance", "time", "availability", "day", "month", "lat", "lng", "date", "schedule"]
    print(df)
    sql.customQueryToSQL("""CREATE TABLE IF NOT EXISTS trainingData (
      `id` int(255) NOT NULL AUTO_INCREMENT,
      `lat` double NOT NULL,
      `lng` double NOT NULL,
      `availability` float NOT NULL,
      `distance` float NOT NULL ,
      `schedule` varchar(5) ,
      `day` int(7) NOT NULL ,
      `time` float NOT NULL ,
      `month` int(12) NOT NULL,
      `date` timestamp NOT NULL,
      PRIMARY KEY (`id`)
    )""")
    sql.insertPandas('trainingData', df, withSchedule=True)

    if plot:
        incremental = dfp['p']
        bins = np.arange(0,6)
        plt.hist(incremental,bins)
        plt.xlabel("Availability Increment")
        plt.ylabel("Frequency")
        plt.title('Distribution of Availability increment')
        plt.show(align="edge", ec="k")

        cumulative = dfp['c']
        bins = np.linspace(0, 1, 40)
        frq, edges = np.histogram(cumulative, bins)
        fig, ax = plt.subplots()
        ax.bar(edges[:-1], frq, width=np.diff(edges), ec="k", align="edge")
        plt.xlabel("Availability Cumulative")
        plt.ylabel("Frequency")
        plt.title('Distribution of Availability cumulated')
        plt.show()

        temp = np.delete(totalMatrix, (0), axis=0)
        labels = [row[8] for row in temp]
        letter_counts = Counter(labels)
        dfA = pd.DataFrame.from_dict(letter_counts, orient='index')
        dfA.plot(kind='bar')
        plt.show()





def calcData(sql, startcoordinate=(43.652042, -79.403610), sqlTable='sensordata'):
    try:
        df = sql.getPandasTable(sqlTable, "SELECT * FROM " + sqlTable + " WHERE Processed <> 1")
    except:
        return pd.DataFrame()

    idToWrite = []


    dfW = pd.DataFrame(columns=['distance', 'time', 'day', 'month', 'availability', 'lat', 'lng', 'date'])

    sql.customQueryToSQL("""CREATE TABLE IF NOT EXISTS trainingData (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `lat` double NOT NULL,
  `lng` double NOT NULL,
  `availability` float NOT NULL,
  `distance` float NOT NULL ,
  `schedule` varchar(5) ,
  `day` int(7) NOT NULL ,
  `time` float NOT NULL ,
  `month` int(12) NOT NULL,
  `date` timestamp NOT NULL,
  PRIMARY KEY (`id`)
)""")

    for index, row in df.iterrows():
        idToWrite.append(index)

        distance = getDistance(startcoordinate,(row['Lat'],row['Lng']))

        dt = (df.at[index, 'CollectTime'].strftime('%Y-%m-%d %H:%M:%S')).split(' ')
        year, month, day = (int(x) for x in dt[0].split('-'))

        h, m, s = dt[1].split(':')
        time = int(h) * 3600 + int(m) * 60 + int(s)

        availability = row['Data']

        dfW = dfW.append(pd.DataFrame([{'distance': distance, 'time': time, 'day': day, 'month': month,
                                        'availability': availability, 'lat': row['Lat'], 'lng': row['Lng'],
                                        'date': row['CollectTime']}]), ignore_index=True)

    sql.insertPandas('trainingData', dfW)

    for id in idToWrite:
        sql.customQueryToSQL("UPDATE " + sqlTable + " SET Processed = '1' WHERE id=" + str(id))

    return dfW


def sortPandasToWriteSQL(dataFrame, listToSortWith):
    df = dataFrame
    priority = 2
    for location in list(listToSortWith[0]):
        latlong = location.split(',')
        df.at[
            df.loc[(df['lat'] == float(latlong[0])) & (df['lng'] == float(latlong[1]))].index[0], 'priority'] = priority
        priority += 1
    return df

def getDistance(startcoordinate,coordinate):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(startcoordinate[0])
    lon1 = radians(startcoordinate[1])
    lat2 = radians(coordinate[0])
    lon2 = radians(coordinate[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


if __name__ == '__main__':
    generateRandomTrainingData(24, database.SQLServer('zone_1'), plot=True)
