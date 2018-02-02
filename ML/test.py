#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 22:22:07 2018

@author: rishab
"""

from sklearn.externals import joblib

clf = joblib.load('svc_40.pkl') 
clf2 = joblib.load('rf_40.pkl') 
clf3 = joblib.load('dt_40.pkl') 

print(clf.predict([[426, 30,7, 559]]))
print(clf2.predict([[426, 30,7, 559]]))
print(clf3.predict([[426, 30,7, 559]]))