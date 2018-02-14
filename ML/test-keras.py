#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 14:59:42 2018

@author: rishab
"""
from keras.models import Sequential
from keras.utils import np_utils
from keras.layers.core import Dense, Activation, Dropout
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from keras.models import model_from_json

 
df = pd.read_csv('{}_labels.csv'.format(n_classes),sep=',')

print(df.shape)

X = df[['protein','calories','fat','sodium']]
y = df['TYPE']
Y = df['TYPE']
(N,M) = X.shape
X = X.as_matrix()
y = y.as_matrix()

y = np.eye(n_classes)[y]
 
# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")
 
# evaluate loaded model on test data
loaded_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(X, y, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))

preds = loaded_model.predict_classes(X[2].reshape(1,4), verbose=0)
print(preds)