import database
import predictor
import router

'''
def createPredictor(dataFrame):
    return predictor.Predictor(dataFrame)


def createRouter(dataFrame):
    return router.Router(dataFrame)
    
'''


def sortPandasToWriteSQL(dataFrame, listToSortWith):
    df = dataFrame
    priority = 1
    for location in list(listToSortWith[0]):
        latlong = location.split(',')
        df.at[
            df.loc[(df['lat'] == float(latlong[0])) & (df['lng'] == float(latlong[1]))].index[0], 'priority'] = priority
        priority += 1
    return df


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

    # Demo 2
    # Make server connection
    sqlServer = database.SQLServer('dumpstersite')
    markers = sqlServer.getPandasTable('markers')
    # rawMarkers = sqlServer.getMarkersFromRaw()
    raw = sqlServer.getPandasTable(table='raw')
    scheduler = {'predictor': predictor.Predictor(raw), 'router': router.Router(markers,file=True)}

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

    final = sortPandasToWriteSQL(markers,markersList)
    final['BestDay'] = sqlServer.getDayToPickup()

    sqlServer.writePandas("markers",final)
    sqlServer.close()
