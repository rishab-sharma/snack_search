#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 20:12:23 2018

@author: rishab
"""

from __future__ import print_function
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from tqdm import tqdm

RANDOM_SEED = 42

n_classes = 15

# =============================================================================
# 
# df = pd.read_csv('{}_labels.csv'.format(n_classes),sep=',')
# 
# print(df.shape)
# 
# X = df[['protein','calories','fat','sodium']]
# y = df['TYPE']
# (N,M) = X.shape
# X = X.as_matrix()
# y = y.as_matrix()
# x = np.ones((N,M+1))
# x[:,1:] = X
# X = x
# y = np.eye(n_classes)[y]
# 
# 
# X_train , X_test , y_train , y_test = train_test_split(X , y , test_size=0.33, random_state=RANDOM_SEED)
# 
# =============================================================================
habit = [1,426.0,30.0,7.0,559.0]
recepie_type = 0

n_classes = 15
arr = [habit]
X_ = np.array(arr)
y = [recepie_type]
y_ = np.eye(n_classes)[y]

print(X,y)

# Neural Network Parameters

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

saver = tf.train.Saver()
sess = tf.Session()

init = tf.global_variables_initializer()

# sess.run(init)

saver.restore(sess, "../models/mlp.ckpt")
prediction_run = sess.run(predict , feed_dict={X: X_.reshape(1,5), y: y_.reshape(1,15)})
cost_run = sess.run(cost , feed_dict = {X: X.reshape(1,5), y: y.reshape(1,15)})

print("Predicted Class is {} and Cost is {}".format(prediction_run , cost_run))
# Training
prediction_run = sess.run(predict , feed_dict={X: X_.reshape(1,5), y: y_.reshape(1,15)})
print("Predicted Class is {} ".format(prediction_run ))



sess.close()