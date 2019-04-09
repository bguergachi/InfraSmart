# Tensorflow and Keras
import tensorflow as tf
from tensorflow import keras
#from ann_visualizer.visualize import ann_viz
from sklearn import preprocessing

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os, sys, math

# Set verbosity of tensorflow


inputNodes = 4


class Predictor:
    def __init__(self, dataFrame,dataFolderPath=None):
        '''
        Create a neural network predictor to schedule day of the week
        :param dataFolderPath: path to data folder with .csv file, .db file and .hdf5 file
        '''
        self._dataFolderPath = dataFolderPath
        print(tf.__version__)
        sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
        tf.logging.set_verbosity(tf.logging.ERROR)

        try:
            df = pd.read_csv(dataFolderPath, na_values=['NA', '?'])
        except:
            df = dataFrame

        print("DataFrame:\n\n")
        print(df)
        print("\n\n")

        #Convert index to day string
        self._days = ['m', 'tu', 'w', 'th', 'f']

        self._encode_text_index(df, "schedule")
        self._x, self._y = df.as_matrix(["distance", "time", "availability", "day", "month"]), np.stack(
            df["schedule"].values, axis=0)

        print(self._x)
        print(self._y)

        self._buildModel()
        self.train()

    def _buildModel(self):
        '''
        Build neural network Model
        :return: null
        '''

        self._model = keras.Sequential()

        self._model.add(keras.layers.Dense(inputNodes, input_dim=self._x.shape[1], activation=tf.nn.sigmoid))
        self._model.add(keras.layers.Dense(math.ceil(inputNodes*2/3), kernel_initializer='normal'))
        self._model.add(keras.layers.Activation(tf.nn.sigmoid))
        self._model.add(keras.layers.Dense(self._y.shape[1], activation=tf.nn.softmax))

        self._model.summary()

    def train(self):
        '''
        Train model created by object
        :return: null
        '''
        print("Training model...")
        self._model.compile(optimizer=tf.train.AdamOptimizer(), loss='categorical_crossentropy', metrics=['accuracy'])
        #monitor = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=1e-3, patience=5, verbose=0, mode='auto')
        #checkpointer = keras.callbacks.ModelCheckpoint(filepath=self._dataFolderPath + "optimized_weights.hdf5",
        #                                               verbose=0, save_best_only=True)  # save best model
        self._history = self._model.fit(self._x, self._y, verbose=2, epochs=100)
        # Use when data is large enough
        # self._model.load_weights(self._dataFolderPath+"optimized_weights.hdf5") # load weights from best model

    def predict(self, input):
        '''
        Predict data point for what day to schedule. This must be later averaged to determine the true day to schedule.
        The predicted data point will be added to a matrix to be later averaged. The matrix can be retrieved using
        :param input: input data to check predictions
        :return: predicted value
        '''
        x_in = np.array([input, ])
        print("Predicting for input:")
        print(x_in)
        print("\nPredictor matrix")
        predict = self._model.predict(x_in)

        # Set variable if not yet set
        try:
            self._weeklyMatrix = np.vstack((self._weeklyMatrix, predict))
        except:
            self._weeklyMatrix = predict

        print(self._weeklyMatrix, "\n")

        return predict

    def scheduleDayVector(self):
        '''
        Get probabilities of what day will be best to pick up on
        :return: vector with column averages of weekly matrix
        '''
        self._weeklyProbability = np.mean(self._weeklyMatrix, axis=0)
        return self._weeklyProbability

    def scheduleDay(self,threshold=None,reset=True):
        '''
        Get day to schedule based on highest probability or probability threshold user passes
        :return: string of day to schedule
        '''
        if threshold == None:
            list = np.argmax(self.scheduleDayVector()).tolist()
            if reset:
                self._weeklyMatrix = None
            try:
                return self._days[list[0]]
            except:
                return self._days[list]
        if reset:
            self._weeklyMatrix = None
        return self.scheduleDayVector()[np.where(self.scheduleDayVector() > threshold)]

    def getAccuracy(self):
        return self._history.history()

    # Update data and train model again
    def updateAndTrain(self, data):
        '''
        Update data and train the model
        :param data: data point to append to csv file, should be an array of length inputNodes
        :return:
        '''
        file = open(self._dataFolderPath + 'training.csv', 'a')
        stringToAppend = ""
        for i in range(len(data) - 1):
            stringToAppend += str(data[i]) + ","
        stringToAppend += str(data[i + 1]) + "\n"
        print("Updating .csv file with new data point\n")
        file.write(stringToAppend)
        file.close()
        self.train()

    #
    def _to_xy(self, df, target):
        '''
        Convert a Pandas dataframe to the x,y inputs that TensorFlow needs
        :param df: dataframe
        :param target: what column to target for output
        :return: x values matrix, y values column vector
        '''

        result = []
        for x in df.columns:
            if x != target:
                result.append(x)

        # find out the type of the target column.  Is it really this hard? :(
        target_type = df[target].dtypes
        target_type = target_type[0] if hasattr(target_type, '__iter__') else target_type

        # Encode to int for classification, float otherwise. TensorFlow likes 32 bits.
        if target_type in (np.int64, np.int32):
            # Classification
            dummies = pd.get_dummies(df[target])
            return df.as_matrix(result).astype(np.float32), dummies.as_matrix().astype(np.float32)
        else:
            # Regression
            return df.as_matrix(result).astype(np.float32), df.as_matrix([target]).astype(np.float32)

    def _encode_text_index(self, df, name):
        '''
        Encode text to one-hot encoding vectors
        :param df: dataframe to alter
        :param name: column to encode
        :return:
        '''
        conversionDic = {'m': np.asarray([1, 0, 0, 0, 0]), 'tu': np.asarray([0, 1, 0, 0, 0]),
                         'w': np.asarray([0, 0, 1, 0, 0]), 'th': np.asarray([0, 0, 0, 1, 0]),
                         'f': np.asarray([0, 0, 0, 0, 1])}
        df[name] = df[name].map(conversionDic)
        print(df)

    def getWeeklyMatrix(self):
        '''
        Get the weekly matrix data. This data can be used to determine the right day to schedule
        :return: weekly matrix data
        '''
        return self._weeklyMatrix


if __name__ == "__main__":
    # Testing if working
    main = Predictor("Data/")
    print(main.predict([234, 2345, 347, 45, 2]))
    print(main.predict([230, 2300, 300, 40, 2]))
