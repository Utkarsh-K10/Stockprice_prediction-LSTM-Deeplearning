# -*- coding: utf-8 -*-
"""stockpriceprediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13urQURlzLWHHwgcq-xTW25kwkL4fi9kZ

#Recurrent Neural Network (RNN)
for Google Stock price 2012-2016
"""

import pandas as pd
import numpy as np

"""LOADING Data From 2012-2016"""

train_df = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Google_Stock_Price_Train.csv')

train_df.head()
len(train_df['Open'])

train_set = train_df.iloc[:,1:2].values

"""Feature Scaling"""

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range=(0,1))
scaled_train_df = sc.fit_transform(train_set)
scaled_train_df

"""Creating DataStructre for 60 days timesteps"""

X_train = []
y_train = []

for i in range(60,1258):
  X_train.append(scaled_train_df[i-60:i,0])
  y_train.append(scaled_train_df[i,0])

X_train, y_train = np.array(X_train), np.array(y_train)

print(X_train.shape[1])
print(X_train.shape)

#Reshaping
X_train = np.reshape(X_train, (X_train.shape[0],X_train.shape[1],1))
print(X_train.shape)

#Building RNN
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

regressor = Sequential()

regressor.add(LSTM(units =50, activation = 'relu',return_sequences=True,input_shape = (X_train.shape[1],1)))

regressor.add(LSTM(units=50, activation = 'relu', return_sequences=True))

regressor.add(LSTM(units=50))

regressor.add(Dense(units = 1))

regressor.compile(optimizer='adam',loss='mean_squared_error')

regressor.summary()

regressor.fit(X_train, y_train, batch_size=84, epochs=158, verbose=1)
#Epoch 158/158
#1198/1198 [==============================] - 4s 3ms/step - loss: 3.0414e-04

"""Now Predicting with real google stock with 2017 year"""

dataset_test = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Google_Stock_Price_Test.csv')

dataset_test.head()

real_stock_price = dataset_test.iloc[:,1:2].values

dataset_total = pd.concat((train_df['Open'], dataset_test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)

X_test = []
for i in range(60, 80):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

import matplotlib.pyplot as plt

plt.plot(real_stock_price, color='red', label='Real Google Stock Price 2017')
plt.plot(predicted_stock_price, color = 'blue', label='Predicted price (20-days) 2017')
plt.xlabel('Time in days')
plt.ylabel('Google Stock')
plt.legend()
plt.show()

plt.bar(predicted_stock_price,height=0.8,width=0.25,color='g')