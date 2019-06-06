# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:58:00 2019

@author: Quentin
"""

import numpy as np 
import matplotlib.pyplot as plt

X = np.array([[1,1], [2,2.5], [3, 1], [8, 7.5], [7, 9], [9, 9]])
Y = ['red', 'red', 'red', 'blue', 'blue', 'blue']

plt.figure()
plt.scatter(X[:, 0], X[:, 1], s = 0, color = Y[:])

t1 = plt.Polygon(X[:3,:], color="red")
plt.gca().add_patch(t1)

t2 = plt.Polygon(X[3:6,:], color=Y[3])
plt.gca().add_patch(t2)

t2.remove()

plt.show()

