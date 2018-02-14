from keras.models import Sequential
from keras.utils import np_utils
from keras.layers.core import Dense, Activation, Dropout
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

#Inp
n_classes = 15
df = pd.read_csv('{}_labels.csv'.format(n_classes),sep=',')

print(df.shape)

X = df[['protein','calories','fat','sodium']]
y = df['TYPE']
(N,M) = X.shape
X = X.as_matrix()
y = y.as_matrix()

y = np.eye(n_classes)[y]

X_train , X_test , y_train , y_test = train_test_split(X , y , test_size=0.33, random_state = 42)
                                                       
print(X_train , X_test , y_train , y_test )                                   

# =============================================================================
# # Read data
# train = pd.read_csv('1.csv')
# labels = train.ix[:,0].values.astype('int32')
# X_train = (train.ix[:,1:].values).astype('float32')
# X_test = (pd.read_csv('../input/test.csv').values).astype('float32')
# 
# # convert list of labels to binary class matrix
# y_train = np_utils.to_categorical(labels) 
# 
# =============================================================================
# =============================================================================
# 
# # pre-processing: divide by max and substract mean
# scale = np.max(X_train)
# X_train /= scale
# X_test /= scale
# 
# mean = np.std(X_train)
# X_train -= mean
# X_test -= mean
# =============================================================================

input_dim = X_train.shape[1]
nb_classes = y_train.shape[1]

# Here's a Deep Dumb MLP (DDMLP)
model = Sequential()
model.add(Dense(128, input_dim=input_dim))
model.add(Activation('relu'))
model.add(Dropout(0.15))
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.15))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

# we'll use categorical xent for the loss, and RMSprop as the optimizer
model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

print("Training...")
model.fit(X_train, y_train, nb_epoch=10, batch_size=16, validation_split=0.1, verbose=2)

print("Generating test predictions...")
preds = model.predict_classes(X_test, verbose=0)

# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
# =============================================================================
def write_preds(preds, fname):
    pd.DataFrame({"ImageId": list(range(1,len(preds)+1)), "Label": preds}).to_csv(fname, index=False, header=True)
# 
write_preds(preds, "keras-mlp.csv")
# =============================================================================
