#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 20:55:52 2018

@author: rishab
"""
import pandas as pd

df = pd.read_csv('40_labels.csv', sep=',')

X = df.as_matrix(columns=['calories', 'protein', 'fat', 'sodium'])
y = df.as_matrix(columns=['TYPE'])
print(X,y)

from sklearn.svm import SVC
clf = SVC()
clf.fit(X, y)

# =============================================================================
# import pickle
# s = pickle.dumps(clf)
# 
# clf2 = pickle.loads(s)
# 
# print(clf2.predict([[426, 30,7, 559]]))
# =============================================================================

from sklearn.externals import joblib
joblib.dump(clf, 'svc_40.pkl') 

clf = joblib.load('svc_40.pkl') 

print(clf.predict([[426, 30,7, 559]]))