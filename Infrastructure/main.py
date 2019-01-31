from Scheduling import predictor
import Scheduling.Data.dataGen as data



def CreatePredictor(path):
    return predictor.Predictor(path)

def CreateRouter(path):
    #TODO: Impelement router algorithm
    pass

if __name__ == '__main__':
    #Create random data
    data.generateRandomData(24,"Scheduling/Data/")
    #Build model and train
    predictor = CreatePredictor('Scheduling/Data/')
    #Test predictor
    print(predictor.predict([240,2700,70,5]))
    #Update predictor
    predictor.updateAndTrain([240,2700,70,5,'f'])
    #Check prediction again
    print(predictor.predict([240, 2700, 70, 5]))

