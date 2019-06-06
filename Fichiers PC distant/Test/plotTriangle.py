# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:58:00 2019

@author: Quentin
"""

import numpy as np 
import matplotlib.pyplot as plt
import math
figScat = plt.figure(0)
plt.title("Représentation du bassin Locale")
ax = figScat.add_subplot(111)
plt.xlim(-5,5)
plt.ylim(-5,5)

plt.gca().set_aspect('equal', adjustable = 'box')
plt.gca().invert_xaxis() #on inverse l'axe x (correspond au y de l'image)
ax.yaxis.tick_right()


x,y,t = 0,0,90
t = math.radians(t)
X = np.array([[x-0.02,y+0.02], [x-0.02,y-0.02], [x+0.04*np.sign(t)*t, y+0.04*np.sign(t)*t]])


t1 = plt.Polygon(X[:3,:], color="red")
plt.gca().add_patch(t1)

#t2.remove()

plt.show()

