import predictor
import router
import dataGen as data
import pandas as pd

def CreatePredictor(dataFrame):
    return predictor.Predictor(dataFrame)


def CreateRouter(dataFrame):
    return router.Router(dataFrame)


if __name__ == '__main__':
    # Create random data
    data.generateRandomTrainingData(48, "Data/")
    # Build model and train
    predictor = CreatePredictor(pd.read_csv("Data/training.csv", na_values=['NA', '?']))
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
