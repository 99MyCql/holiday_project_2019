# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 11:38:56 2019

@author: Shanks
"""

import tensorflow as tf
     
Vector = [1,1,2,5,3]           #定义一个向量
X = [[1,3,2],[2,5,8],[7,5,9]]  #定义一个矩阵
 
with tf.Session() as sess:
    a = tf.argmax(Vector, 0)
    b = tf.argmax(X, 0)
    c = tf.argmax(X, 1)
    
    print(sess.run(a))
    print(sess.run(b))
    print(sess.run(c))