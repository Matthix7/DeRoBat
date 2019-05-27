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

reduc=10
X_tab = np.arange(0, 3*reduc, 1) #discrétisation à effectuer
Y_tab = np.arange(0,4*reduc, 1)
Z_tab = np.ones((4*reduc,3*reduc)) * -3
#
#surf  = plt.contourf(X_tab, Y_tab, Z_tab)


fig = plt.figure()
plt.title("Représentation théorique du bassin")
ax = fig.add_subplot(111)

#plt.colorbar(surf)

plt.xlim(0,3)
plt.ylim(0,4)

plt.gca().set_aspect('equal', adjustable = 'box')
plt.gca().invert_xaxis() #on inverse l'axe x (correspond au y de l'image)
ax.yaxis.tick_right()


while alive.is_set():
    X, Y, Z, xBoat, yBoat = thread_listening.toMap()
    
    
    if X != []:
        #Représentation 3D en 2D
#        plt.scatter(X, Y, c = Z, cmap='viridis')
    
#        ax.scatter3D(X, Y, Z, c=Z, cmap='viridis')
        
        #bathy 3d avec scatter couleur entre -3 et -2 m
        for x,y,z in zip(X,Y,Z):
            std = 0.2
            r = 2.5*std*scipy.stats.norm.pdf(z,-2,std)
            g = 2.5*std*scipy.stats.norm.pdf(z,-2.5,std)
            b = 2.5*std*scipy.stats.norm.pdf(z,-3,std)
        
            col = np.array([r,g,b]) #blue if z = -3, green if z = -1.5, red if z = 0
    
            scat = plt.scatter(y, x, marker = 'o', c=col)
            #fig.colorbar(scat, label="Z")

        
        plt.pause(2)
                 
    



# Attend que les threads se terminent
thread_listening.join()