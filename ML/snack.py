#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 23:59:07 2018

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

X = pd.read_csv('epi_r.csv',sep=',')



print(__doc__)

range_n_clusters = [2, 3, 4, 5, 6 , 7 , 8 , 9 ,10 ,11 , 12 , 13 , 14 , 15 , 16]
n = 30
X = X.dropna(axis = 0).reset_index()
y = X['title']
X = X.drop(['title','rating'],axis = 1)
X = X[['calories','protein','fat','sodium']]
pca = PCA(n_components = 2)
pca.fit(X)
PCA(copy=True, iterated_power='auto', n_components=2, random_state=None,
  svd_solver='auto', whiten=False)
T = pca.transform(X)
print(X.shape)
print(y)
print(T.shape)

X.plot()
plt.show()

X = T
for n_clusters in [5]:
     
     clusterer = KMeans(n_clusters=n_clusters, random_state=1 , max_iter = 10000)
     cluster_labels = clusterer.fit_predict(X)
     fig, (ax2) = plt.subplots(1)
     fig.set_size_inches(18, 7)
     
    # Labeling the clusters
     centers = clusterer.cluster_centers_
     print(centers)

     for i, c in enumerate(centers):
         ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1, s=50, edgecolor='k')
     for i in range(len(T[:,0])):
         ax2.scatter(T[:,0][i],T[:,1][i] , marker = '.')

     ax2.set_title("The visualization of the clustered data.")
     ax2.set_xlabel("Feature space for the 1st feature")
     ax2.set_ylabel("Feature space for the 2nd feature")

     plt.suptitle(("Clustering "
                  "with n_clusters = %d" % n_clusters),
                 fontsize=14, fontweight='bold')

     plt.show()
   
         