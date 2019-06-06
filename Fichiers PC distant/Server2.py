# -*- coding: utf-8 -*-
"""
Created on Thu May 23 15:43:31 2019

@author: Quentin
"""

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



plt.figure()
plt.title("Représentation théorique du bassin")

pas = 1/20
Z_tab = -3*np.ones((int(4/pas), int(3/pas)))
X_tab = np.linspace(0,3,np.shape(Z_tab)[1])
Y_tab = np.linspace(0,4,np.shape(Z_tab)[0])

while alive.is_set():
    X, Y, Z,x,y = thread_listening.toMap()
    
    if X != []:
        #Représentation 3D en 2D
#        plt.scatter(X, Y, c = Z, cmap='viridis')
    
#        ax.scatter3D(X, Y, Z, c=Z, cmap='viridis')
        
         
         for ind in range(len(X)): 
             Z_tab[int(Y[ind]/pas)][int(X[ind]/pas)] = np.mean([Z_tab[int(Y[ind]/pas)][int(X[ind]/pas)], Z[ind]])
         
         plt.contourf(X_tab, Y_tab, Z_tab)
            
         plt.draw()
        
         plt.pause(0.5)
    



# Attend que les threads se terminent
thread_listening.join()