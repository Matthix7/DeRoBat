# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 08:48:01 2019

@author: Quentin
"""
import matplotlib.pyplot as plt
import scipy.stats
import numpy as np


x_min = -4
x_max = 1

std = 0.2

x = np.linspace(x_min, x_max, 100)

y = 2.5*std*scipy.stats.norm.pdf(x,-1,std)

plt.plot(x,y, color='red')

y = 2.5*std*scipy.stats.norm.pdf(x,-0.5,std)

plt.plot(x,y, color='blue')


y = 2.5*std*scipy.stats.norm.pdf(x,0,std)

plt.plot(x,y, color='green')


plt.grid()

plt.xlim(x_min,x_max)
plt.ylim(0,1.2)

plt.title('How to plot a normal distribution in python with matplotlib',fontsize=10)

plt.xlabel('x')
plt.ylabel('Normal Distribution')

plt.pause(2)