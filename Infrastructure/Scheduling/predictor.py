#Tensorflow and Keras
import tensorflow as tf
from tensorflow import keras
from sklearn import preprocessing

#Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os, sys


class predictor:
    def __init__(self,dataFolderPath):
        self._dataFolderPath = dataFolderPath
        print(tf.__version__)
        sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

        df = pd.read_csv(self._dataFolderPath,na_values=['NA','?'])

        print("DataFrame:\n\n")
        print(df)



        self._nodes = 4

        self._encode_text_index(df,"priority")
        self._x,self._y = self._to_xy(df,"priority")

        print(self._x)
        print(self._y)

        self._buildModle()


    def _buildModle(self):



        self._model = keras.Sequential()

        self._model.add(keras.layers.Dense(self._nodes, input_dim=self._x.shape[1],activation=tf.nn.relu))
        self._model.add(keras.layers.Dense(7, kernel_initializer='normal'))
        self._model.add(keras.layers.Activation(tf.nn.sigmoid))

        self._model.summary()



    def train(self):

        self._model.compile(optimizer=tf.train.AdamOptimizer(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        monitor = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=1e-3, patience=5, verbose=0, mode='auto')
        checkpointer = keras.callbacks.ModelCheckpoint(filepath=self._dataFolderPath+"optimized_weights.hdf5", verbose=0, save_best_only=True)  # save best model
        self._model.fit(self._x, self._y, callbacks=[monitor, checkpointer], verbose=0, epochs=1000)
        self._model.load_weights(self._dataFolderPath+"optimized_weights.hdf5") # load weights from best model

    # Convert a Pandas dataframe to the x,y inputs that TensorFlow needs
    def _to_xy(self,df, target):
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

    def _encode_text_index(self,df, name):
        le = preprocessing.LabelEncoder()
        df[name] = le.fit_transform(df[name])
        return le.classes_

if __name__ == "__main__":
    main = predictor("Data/training.csv")
    main.train()
