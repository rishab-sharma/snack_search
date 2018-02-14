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


#Neural Network Parameters
input_size = 5 # 4 Features and 1 bias
h_1 = 20
h_2 = 60
output = n_classes

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

habit = [1,426.0,30.0,7.0,559.0]
recepie_type = 0
# 
n_classes = 15
arr = habit
X1 = np.array(arr).reshape(1,5)
y1 = [recepie_type]
y1 = np.eye(n_classes)[y1]
y1 = y1[0].reshape(1,15)
y1=y1[0]
X1=X1[0]
print(X1)
print(y1)
# 
saver = tf.train.Saver()
sess2 = tf.Session()
# 
init = tf.global_variables_initializer()

sess2.run(init)
saver.restore(sess2, "../models/mlp.ckpt")

prediction_run = sess2.run(predict , feed_dict={X: X1.reshape(1,5), y: y1.reshape(1,15)})

print("Predicted Class is {}".format(prediction_run))

sess2.close()