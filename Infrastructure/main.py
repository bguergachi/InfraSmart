from Scheduling import predictor
from Data import dataGen as data

def CreatePredictor(path):
    return predictor.Predictor(path)


def CreateRouter(path):
    # TODO: Impelement router algorithm
    pass


if __name__ == '__main__':
    # Create random data
    data.generateRandomTrainingData(48, "Scheduling/Data/")
    # Build model and train
    predictor = CreatePredictor('Scheduling/Data/')
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
