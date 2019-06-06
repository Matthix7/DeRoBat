# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 11:43:10 2019

@author: Quentin
"""
from matplotlib import patches
import matplotlib.pyplot as plt


fig0 = plt.figure(0)
plt.title("Représentation théorique du bassin")
ax = fig0.add_subplot(111)

plt.xlim(0,3)
plt.ylim(0,4)

plt.gca().set_aspect('equal', adjustable = 'box')
plt.gca().invert_xaxis() #on inverse l'axe x (correspond au y de l'image)
ax.yaxis.tick_right()


fig1 = plt.figure(1)
plt.title("Représentation théorique du bassin")
ax = fig1.add_subplot(111)

plt.xlim(0,3)
plt.ylim(0,4)

plt.gca().set_aspect('equal', adjustable = 'box')
plt.gca().invert_xaxis() #on inverse l'axe x (correspond au y de l'image)
ax.yaxis.tick_right()

plt.figure(0)
plt.scatter(1, 2, marker = 'o', c="red")