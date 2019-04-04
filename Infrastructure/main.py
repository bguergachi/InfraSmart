import database
import dataGen
import predictor
import router
import pandas as pd
import numpy as np
import datetime

'''
def createPredictor(dataFrame):
    return predictor.Predictor(dataFrame)


def createRouter(dataFrame):
    return router.Router(dataFrame)
    
'''





if __name__ == '__main__':
    '''
    # Demo 1
    # Create random data
    data.generateRandomTrainingData(48, "Data/")
    # Build model and train
    predictor = createPredictor(pd.read_csv("Data/training.csv", na_values=['NA', '?']))
    # Test predictor
    a = predictor.predict([1234, 34523.56, 64.23, 2])
    # Update predictor
    predictor.updateAndTrain([1234, 34523.56, 64.23, 2, 'f'])
    # Check prediction again
    b = predictor.predict([1234, 34523.56, 64.23, 2])

    print("Test:")
    print(a)
    print("After update:")
    print(b)
    '''
    '''
    # Demo 2
    # Make server connection
    sqlServer = database.SQLServer('dumpstersite')
    dataGen.calcData('sensordata',sqlServer)


    sensordata = sqlServer.getPandasTable(table='sensordata')
    markers = sqlServer.getMarkersFromRaw('sensordata')

    # rawMarkers = sqlServer.getMarkersFromRaw()

    scheduler = {'predictor': predictor.Predictor(sensordata), 'router': router.Router(markers,file=True)}

    # Build prediction matrix
    scheduler['predictor'].predict([3245, 19402.08, 100, 2])
    scheduler['predictor'].predict([12, 70651.76, 89.72, 3])
    scheduler['predictor'].predict([312, 36983.10, 46.81, 0])
    scheduler['predictor'].predict([1234, 44078.21, 42.90, 0])
    scheduler['predictor'].predict([7564, 43575.08, 100, 3])
    scheduler['predictor'].predict([3245, 66944.55, 50.95, 1])
    scheduler['predictor'].predict([312, 1854.36, 94.18, 1])
    scheduler['predictor'].predict([312, 992.10, 62.78, 1])

    # Set best day to schedule
    sqlServer.setDayToPickup(scheduler['predictor'].scheduleDay())

    markersList = scheduler['router'].run_genetic_algorithm()

    final = dataGen.sortPandasToWriteSQL(markers,markersList)
    final['DayOfTheWeek'] = sqlServer.getDayToPickup()

    sqlServer.writePandasMarkers("markers",final)
    sqlServer.close()
    '''

    #Demo 3
    #Set database
    sql = database.SQLServer('dumpstersite')
    #Generate training data
    dataGen.generateRandomTrainingData(52,sql,coordinate=sql.customQueryToSQL("SELECT DISTINCT Lat,Lng FROM sensordata"))

    sql.createMetaTable()
    meta = sql.getPandasTable('meta')
    initialCoordinates = tuple(sql.getIntialLocation())
    toPredict = dataGen.calcData(sql, startcoordinate=initialCoordinates)

    training = sql.getPandasTable('trainingData')
    trainingData = training.drop(['lat','lng','date'], axis=1)
    trainingData = trainingData.dropna(axis='rows')

    markers = sql.getMarkersFromTraining()
    markerData = markers.reset_index(drop=True)
    markerData.index.name = 'id'

    scheduler = {'predictor': predictor.Predictor(trainingData), 'router': router.Router(markerData,file=True)}

    for row in toPredict.iterrows():
        index, data = row
        scheduler['predictor'].predict([data['distance'], data['time'], data['availability'], data['day'], data['month']])

    bestDay = scheduler['predictor'].scheduleDay()
    sql.setDayToPickup(bestDay)

    markerData['DayOfTheWeek'] = sql.getDayToPickup()
    markerData['priority'] = 1
    markerData['address'] = 'L'
    sql.insertPandas('markers',markerData)
    sql.close()

    markersList = scheduler['router'].run_genetic_algorithm()
    finalMarkers = dataGen.sortPandasToWriteSQL(markers, markersList)
    finalMarkers = finalMarkers.append(pd.DataFrame([{'lat':initialCoordinates[0],'lng':initialCoordinates[1],'date':datetime.date.today(),'availability':0,'priority':1}]), ignore_index=True)



