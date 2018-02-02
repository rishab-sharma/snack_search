#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 22:29:33 2018

@author: rishab
"""

from sklearn.ensemble import RandomForestClassifier
import pandas as pd

df = pd.read_csv('40_labels.csv', sep=',')

X = df.as_matrix(columns=['calories', 'protein', 'fat', 'sodium'])
y = df.as_matrix(columns=['TYPE'])
print(X,y)

clf = RandomForestClassifier(max_depth=None, random_state=0)
clf.fit(X, y)

from sklearn.externals import joblib
joblib.dump(clf, 'rf_40.pkl') 

clf = joblib.load('rf_40.pkl') 

print(clf.predict([[426, 30,7, 559]]))