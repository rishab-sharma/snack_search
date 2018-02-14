from __future__ import print_function
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from tqdm import tqdm

RANDOM_SEED = 42

n_classes = 15


df = pd.read_csv('{}_labels.csv'.format(n_classes),sep=',')

print(df.shape)

X = df[['protein','calories','fat','sodium']]
y = df['TYPE']
(N,M) = X.shape
X = X.as_matrix()
y = y.as_matrix()
x = np.ones((N,M+1))
x[:,1:] = X
X = x
y = np.eye(n_classes)[y]


X_train , X_test , y_train , y_test = train_test_split(X , y , test_size=0.33, random_state=RANDOM_SEED)

#Neural Network Parameters
input_size = 5 # 4 Features and 1 bias
h_1 = 20
h_2 = 60
output = n_classes
learning_rate = 0.01

# Neural Network
w_1 = tf.Variable(tf.random_normal([input_size , h_1],stddev = 0.1))

w_2 = tf.Variable(tf.random_normal([h_1 , h_2] , stddev = 0.1))

w_3 = tf.Variable(tf.random_normal([h_2 , output] , stddev = 0.1))

X = tf.placeholder("float" , shape=[None , input_size])

y = tf.placeholder("float" , shape=[None , output])

c1 = tf.nn.leaky_relu((tf.matmul(X , w_1)))

c2 = tf.nn.leaky_relu((tf.matmul(c1 , w_2)))

c3 = tf.matmul(c2 , w_3)

predict = tf.argmax(c3 , axis = 1)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels = y, logits = c3))

updates = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Tensorflow Session
saver = tf.train.Saver(sharded=True)
sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)

# Training
for epoch in range(1):
    for i in tqdm(range(len(X_train))):
		sess.run(updates , feed_dict = {X: X_train[i:i+1] , y: y_train[i:i+1]})
    train_accuracy = np.mean(np.argmax(y_train, axis=1) == sess.run(predict, feed_dict={X: X_train, y: y_train}))
    test_accuracy  = np.mean(np.argmax(y_test , axis=1) == sess.run(predict, feed_dict={X: X_test, y: y_test}))
    print()
    print("Epoch = %d, train accuracy = %.2f%%, test accuracy = %.2f%%" % (epoch + 1, 100. * train_accuracy, 100. * test_accuracy))
save_path = saver.save(sess, "../models/mlp.ckpt")
print("Model Saved at {} with name MLP.ckpt".format(save_path))
sess.close()
