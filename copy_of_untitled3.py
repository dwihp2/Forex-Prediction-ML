# -*- coding: utf-8 -*-
"""Copy of Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16qR6gBzgW-ycfai-gV8Yiib9PyYGjBJG
"""

# Commented out IPython magic to ensure Python compatibility.
#Import libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#This is a magic command. It will display the plotting image directly below the code cell
# %matplotlib inline

dataset_train_path = os.getcwd() + "/day-train.csv"
dataset_train = pd.read_csv(dataset_train_path)
dataset_train.tail()

training_set = dataset_train.iloc[:,5:6].values

print(training_set)
print("********************")
print(training_set.shape)

#----------------------------------------------#
# Additional Information (Things to Remember!) #
#----------------------------------------------#

print(type(dataset_train))
print(type(dataset_train.iloc[:,5:6]))   
print(type(dataset_train.iloc[:,5:6].values))

# iloc[rangeofRows, rangeofColumns]
# Indexing starts from zero.
# ":" indicates entire range.
# "5:6" indicates column one only. Because, the upper bound will be excluded. 
# mathematical operation are performed on the arrays. So, it is crusial to convert the data to arrays.

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range = (0,1)) 
scaled_training_set = scaler.fit_transform(training_set)

# scaled_training_set

X_train = []
y_train = []
for i in range(60,len(training_set)):
    X_train.append(scaled_training_set[i-60:i, 0])
    y_train.append(scaled_training_set[i, 0])
X_train = np.array(X_train)
y_train = np.array(y_train)

print(X_train.shape)
print(y_train.shape)

X_train = np.reshape(X_train,(X_train.shape[0], X_train.shape[1], 1))

X_train.shape

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout

#--------------------------------------------#
#  Initialization and Adding layers to RNN   #
#--------------------------------------------#
regressor = Sequential()

regressor.add(LSTM(units = 100, return_sequences= True, input_shape = (X_train.shape[1], 1)))   # the first LSTM layer
regressor.add(Dropout(0.2))                     

regressor.add(LSTM(units = 100, return_sequences= True))  # the second LSTM layer
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 100, return_sequences= True))  # the third LSTM layer
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 100, return_sequences= True))  # the fourth LSTM layer
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 100))  # the fifth LSTM layer
regressor.add(Dropout(0.2))

regressor.add(Dense(units=1))   # the dense layer

#-----------------------------------------------------#
#  Compiling and Fitting the RNN to the Training set  #
#-----------------------------------------------------#

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error') 
regressor.fit(X_train, y_train, epochs=100, batch_size=32)

# the loss function "mean_squared_error"(MSE) is used because it is a Regression problem.
# epochs = no of iterations. After every 32 (batch_size) datasets, the MSE will be calculated and 
# the tweaks will be Back Propagated i.e., the weights will be tweaked for every 32 training datasets.

#Read Data from CSV file (For Prediction 20 Mei 2020)
predict_next_day = pd.read_csv('02-juli.csv', parse_dates=True, index_col=0)

#create a new dataframe
#iloc[:,4:5] is to select all range in column 4-5 that is close column
new_df = predict_next_day.iloc[:,4:5]
#get the last 60 day closing price values and convert the dataframe to an array
last_60_days = new_df[-60:].values
#scale the data to be values beetween 0 and 1
last_60_days_scaled = scaler.transform(last_60_days)
#create an empty list
Xx_test = []
#append the past 60 days 
Xx_test.append(last_60_days_scaled)
#convert the X_test data set to a numpy array
Xx_test = np.array(Xx_test)
#Reshape the data
Xx_test = np.reshape(Xx_test, (Xx_test.shape[0], Xx_test.shape[1], 1))
#Get the predicted scaled price
pred_price = regressor.predict(Xx_test)
#undo the scaling
pred_price = scaler.inverse_transform(pred_price)

print(pred_price)
# pred_price