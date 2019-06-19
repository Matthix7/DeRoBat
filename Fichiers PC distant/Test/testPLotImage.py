# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 09:43:32 2019

@author: Quentin
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg

figScat = plt.figure(0)
plt.title("Représentation locale du bassin")
figScat.patch.set_visible(False)


min, max = (-3, 0) #max and min for the colorbar (in meters)
step = 0.01

# Setting up a colormap that's a simple transtion
mymap = mpl.colors.LinearSegmentedColormap.from_list('mycolors',['blue','green','red'])

# Using contourf to provide my colorbar info, then clearing the figure
Z = [[0,0],[0,0]]
levels = np.arange(min,max+step,step)
CS3 = plt.contourf(Z, levels, cmap=mymap)
plt.clf()

figScat.subplots_adjust(left=0,right=1,bottom=0,top=1)
ax = figScat.add_subplot(111)

cb = plt.colorbar(CS3, orientation= "horizontal") # using the colorbar info I got from contourf
plt.gca().set_aspect('equal', adjustable = 'box')

plt.axis('off')
cb.remove()

img=mpimg.imread('backgroungPlot.png')
imgplot = plt.imshow(img)

plt.scatter(10, 10, marker = 'o', c = 'red')
extent = ax.get_window_extent().transformed(figScat.dpi_scale_trans.inverted())
plt.savefig("foo.png", bbox_inches=extent)


