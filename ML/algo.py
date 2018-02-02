#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 18:47:58 2018

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
for n_clusters in [40]:
     
     clusterer = KMeans(n_clusters=n_clusters, random_state = 1)
     cluster_labels = clusterer.fit_predict(X)
     
#     print(np.unique(cluster_labels , return_counts = True))
     fig, (ax1, ax2) = plt.subplots(1, 2)
     fig.set_size_inches(18, 7)
     ax1.set_xlim([-0.1, 1])
     ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])
     silhouette_avg = silhouette_score(X, cluster_labels)
     print("For n_clusters =", n_clusters,"The average silhouette_score is :", silhouette_avg)
     sample_silhouette_values = silhouette_samples(X, cluster_labels)
     y_lower = 10
     for i in range(n_clusters):
         ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
         ith_cluster_silhouette_values.sort()
         size_cluster_i = ith_cluster_silhouette_values.shape[0]
         y_upper = y_lower + size_cluster_i
         color = cm.spectral(float(i) / n_clusters)
         ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)
         ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
         y_lower = y_upper + 10
     ax1.set_title("The silhouette plot for the various clusters.")
     ax1.set_xlabel("The silhouette coefficient values")
     ax1.set_ylabel("Cluster label")
    
     ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

     ax1.set_yticks([])  # Clear the yaxis labels / ticks
     ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    # 2nd Plot showing the actual clusters formed
     colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
     ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                c=colors, edgecolor='k')

    # Labeling the clusters
     centers = clusterer.cluster_centers_
    # Draw white circles at cluster centers
     ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
                c="white", alpha=1, s=200, edgecolor='k')

     for i, c in enumerate(centers):
         ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
                    s=50, edgecolor='k')

     ax2.set_title("The visualization of the clustered data.")
     ax2.set_xlabel("Feature space for the 1st feature")
     ax2.set_ylabel("Feature space for the 2nd feature")

     plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                  "with n_clusters = %d" % n_clusters),
                 fontsize=14, fontweight='bold')

     plt.show()