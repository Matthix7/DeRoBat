# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 22:46:28 2019

@author: Matthieu
SOCKETS : 
https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/234698-le-reseau
THREADS:
https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/2235545-la-programmation-parallele-avec-threading

/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\
Si mode manuel :
    BIEN ECRIRE 'fin' A LA FIN DE COMMUNICATION POUR FERMER LES SOCKETS (à écrire côté serveur) !!!
Si mode caméra:
    Appuyer sur Echap pour quitter la fenêtre 'Webcam', ce qui entraîne les fermetures de socket.
"""

from threading import Thread, RLock, Event
from Thread_Server_Listening import *
from Thread_Server_Writing import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import scipy.stats
import numpy as np


PORT_ALLER = 12800
PORT_RETOUR = 12801

# Synchronise l'extinction de Server et Listening
alive = Event()
alive.set()

# Création des threads
thread_listening = Listening_Server(PORT_ALLER, PORT_RETOUR, alive)

# Lancement des threads
thread_listening.start()


#------------ Init pour l'affichage de le Scatter-----------
figScat = plt.figure(0)
plt.title("Représentation du bassin Locale")
ax = figScat.add_subplot(111)


plt.xlim(0,3)
plt.ylim(0,4)

plt.gca().set_aspect('equal', adjustable = 'box')
plt.gca().invert_xaxis() #on inverse l'axe x (correspond au y de l'image)
ax.yaxis.tick_right()

nbPlot = 0 #contient le nombre de plot fait sur le scatter

#--------------------------------------------------------
#------------ Init pour l'affichage de le Contourf-----------
figCont = plt.figure(1)
plt.title("Représentation du bassin Globale")
ax = figCont.add_subplot(111)

plt.gca().set_aspect('equal', adjustable = 'box')
plt.gca().invert_xaxis() #on inverse l'axe x (correspond au y de l'image)
ax.yaxis.tick_right()

X_Cont = [] #stockage des valeurs de x,y,z
Y_Cont = []
Z_Cont = []

#--------------------------------------------------------

while alive.is_set():
    X, Y, Z, xBoat, yBoat = thread_listening.toMap()
    
#    if not xBoat is None and xBoat != 0 and yBoat != 0 and xBoat != -1 and yBoat != -1:
#        traceX.append(xBoat)
#        traceY.append(yBoat)
#    
#    X = []
    if X != []:
        #Représentation 3D en 2D
        #bathy 3d avec scatter couleur entre -3 et 0 m
        for x,y,z in zip(X,Y,Z):
            std = 0.4
            r = 2.5*std*scipy.stats.norm.pdf(z,0,std)
            g = 2.5*std*scipy.stats.norm.pdf(z,-1.5,std)
            b = 2.5*std*scipy.stats.norm.pdf(z,-3,std)
        
            col = np.array([[r,g,b]]) #blue if z = -3, green if z = -1.5, red if z = -0
            plt.figure(0)
            plt.scatter(y, x, marker = 'o', c=col)
            
            X_Cont.append(y)
            Y_Cont.append(x)
            Z_Cont.append(z)
            
        
        plt.figure(0)
        plt.plot(yBoat, xBoat, marker = 'x', color = 'red')
        
            
        nbPlot += 1
        if nbPlot >= 10:
            print("-----------------CLEAR AXES----------------")
            plt.figure(0)
            plt.cla()
            plt.title("Représentation du bassin Locale")
            ax = figScat.add_subplot(111)
            plt.xlim(0,3)
            plt.ylim(0,4)
            plt.gca().set_aspect('equal', adjustable = 'box')
            plt.gca().invert_xaxis() #on inverse l'axe x (correspond au y de l'image)
            ax.yaxis.tick_right()

            nbPlot = 0           
            print("-----------------Update Bathymetrie----------------")
            
            pas = 1/10
            ZCont = -3*np.ones((int(4/pas), int(3/pas)))
            XCont = np.linspace(0,3,np.shape(ZCont)[1])
            YCont = np.linspace(0,4,np.shape(ZCont)[0])               
            
            
            for ind in range(len(X_Cont)): 
                ZCont[int(Y_Cont[ind]/pas)][int(X_Cont[ind]/pas)] = np.mean([ZCont[int(Y_Cont[ind]/pas)][int(X_Cont[ind]/pas)], Z_Cont[ind]])
         
            plt.figure(1)
            plt.contourf(XCont, YCont, ZCont)
            plt.draw()
            
        plt.pause(2)

            
            
#    time.sleep(0.1)

                 
#plt.plot(traceY, traceX, marker = 'x', color = 'red')
#print(traceY)


# Attend que les threads se terminent
thread_listening.join()



