import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib

df = pd.read_csv('epi_r.csv',sep=",")
df = df.dropna(axis=0).reset_index()
df = df.drop(labels=['index','title'],axis=1)

matplotlib.style.use('ggplot') # Look Pretty
c = ['red', 'green', 'blue', 'orange', 'yellow', 'brown']

def doPCA(data, dimensions = 2):
  from sklearn.decomposition import RandomizedPCA
  model = RandomizedPCA(n_components = dimensions)
  model.fit(data)
  return model
  
T = preprocessing.StandardScaler().fit_transform(df)

def doKMeans(data, clusters = 0):
  model = KMeans(n_clusters = clusters)
  labels = model.fit_predict(data)
  return model.cluster_centers_, model.labels_
  
n_clusters = 5
centroids, labels = doKMeans(T, n_clusters)

print centroids

display_pca = doPCA(T)
T = display_pca.transform(T)
CC = display_pca.transform(centroids)

# Visualize all the samples. Give them the color of their cluster label
fig = plt.figure()
ax = fig.add_subplot(111)
sample_colors = [ c[labels[i]] for i in range(len(T)) ]
ax.scatter(T[:, 0], T[:, 1], c=sample_colors, marker='.', alpha=0.2)


# Plot the Centroids as X's, and label them
ax.scatter(CC[:, 0], CC[:, 1], marker='x', s=169, linewidths=3, zorder=1000, c=c)
for i in range(len(centroids)): ax.text(CC[i, 0], CC[i, 1], str(i), zorder=500010, fontsize=18, color=c[i])



# Add the cluster label back into the dataframe and display it:
df['label'] = pd.Series(labels, index=df.index)
print df

plt.show()  


#####################################################################

C = 1
kernel = 'linear'

X = df
print X.head()
print "<\\\\\\\\\\\\\\\\\\\\\>"


print "<\\\\\\\\\\\\\\\\\\\\\>"
X.dropna(axis = 0, how = 'any', inplace = True)
y = X.label
X.drop('label', axis = 1, inplace = True)
td = X.head()
print "+++"
print td
print "+++"

y = y.map({'type 1': 0, 'type 2': 1, 'type 3': 2, 'type 4': 3 , 'type 5': 4})

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.6, random_state = 7)


from sklearn.svm import SVC
svc = SVC(C = C, kernel = kernel)

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 5)

print X_train


print y_train

print "TRAINING MODEL"
svc.fit(X_train,y_train)
print "TRAINIG COMPLETED"

print svc.predict(td)

plt.show()
