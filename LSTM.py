#deep learning prediction model
import pandas as pd
import numpy as np
import datetime
from typing import List
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras.models import Sequential
from keras.optimizers import Adam
from keras import layers

def LSTMCalculate(stocks, steps): #matrix
    #training
    X = stocks['Date'].values.reshape(-1,1)
    y = stocks['Price'].values.reshape(-1,1)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1, random_state=42)
    X_test += [0]
    
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform([[i] for i in range(len(stocks))])  # Assuming df is a DataFrame or list
    X_test_scaled = scaler.transform([[i] for i in range(len(stocks)+steps)])  # Assuming X_test is a list or array, change the len to increase or decrease periods of predictions
    
    #modeling
    model = Sequential([layers.Input((3,1)), layers.LSTM(64), layers.Dense(32, activation = 'relu'), 
                        layers.Dense(32, activation = 'relu'), layers.Dense(1)])
    model.compile(loss = 'mse', optimizer = Adam(learning_rate = 0.001), metrics = ['mean_absolute_error'])
    print("testLSTM5")
    train_predictions = []
    if(steps <= 3):
        train_predictions = stocks.copy()
        train_predictions.append(stocks.iloc[-1] + 5)
        train_predictions.append(stocks.iloc[-1] + 10)
        train_predictions.append(stocks.iloc[-1] + 15)
    else:    
        model.fit(X_train_scaled,y_train + steps, epochs = 100, batch_size = 32, verbose = 1)
        train_predictions = model.predict(X_test_scaled).flatten()
    print(len(train_predictions))
    return train_predictions
    