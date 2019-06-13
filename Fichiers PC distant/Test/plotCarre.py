# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 08:53:00 2019

@author: Quentin
"""
from matplotlib import patches
import matplotlib.pyplot as plt

import cv2

def plot():
    fig = plt.figure()
    plt.title("Représentation théorique du bassin")
    ax = fig.add_subplot(111)
    
    plt.xlim(0,3)
    plt.ylim(0,4)
    
    plt.gca().set_aspect('equal', adjustable = 'box')
    plt.gca().invert_xaxis() #on inverse l'axe x (correspond au y de l'image)
    ax.yaxis.tick_right()
    
    ax.add_artist(
            patches.Rectangle((2.9, 0), 0.1, 0.1,
                              edgecolor = [1,0,0], facecolor = [1,0,0],
                              fill = True))
    
    ax.add_artist(
            patches.Rectangle((0, 0), 0.1, 0.1,
                              edgecolor = [0,1,0], facecolor = [0,1,0],
                              fill = True))
    ax.add_artist(
            patches.Rectangle((0, 3.9), 0.1, 0.1,
                              edgecolor = [0,0,1], facecolor = [0,0,1],
                              fill = True))
def openCV():
    x = 0
    y = 500
    cv2.namedWindow('Representation du bassin', cv2.WINDOW_NORMAL)
    frame = cv2.imread("trois_quatre_mil.png")
    frame[:] = [255,0,0]
    
    frame[x:x+500,y:y+500] = [0,0,255]
    
    cv2.imshow('Representation du bassin', frame)
    
    
if __name__ == "__main__":
    plot()
