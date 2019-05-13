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

import socket
import sys
from threading import Thread, RLock, Event
from Thread_Server_Listening import *
from Thread_Server_Writing import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time


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
ax = plt.axes(projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

while alive.is_set():
    X, Y, Z = thread_listening.toMap()
    
    if X != []:
        #Représentation 3D en 2D
#        plt.scatter(X, Y, c = Z, cmap='viridis')
        ax.scatter(X, Y, Z, cmap='viridis')
        plt.pause(2)



# Attend que les threads se terminent
thread_listening.join()