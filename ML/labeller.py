#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 00:32:33 2018

@author: rishab
"""
from __future__ import print_function
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

n_classes = 15

X = pd.read_csv('epi_r.csv',sep=',')

X = X.dropna(axis = 0).reset_index()
y = X['title']
X = X.drop(['title','rating'],axis = 1)
X = X[['calories','protein','fat','sodium']]
pca = PCA(n_components = 2)
pca.fit(X)
PCA(copy=True, iterated_power='auto', n_components=2, random_state=None,
  svd_solver='auto', whiten=False)
T = pca.transform(X)


clusterer = KMeans(n_clusters= n_classes, random_state=1 , max_iter = 10000)
cluster_labels = clusterer.fit_predict(T)

df = pd.DataFrame(data = X )
df2 = pd.DataFrame(data = cluster_labels , columns = ['TYPE'])
df3 = pd.DataFrame(data = T , columns = ['DR_f1' , 'DR_f2'])
result = pd.concat([df , df2 , y , df3] , axis = 1)

print(result)
result.to_csv('{}_labels.csv'.format(n_classes))