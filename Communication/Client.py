# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 22:46:28 2019

@author: Matthieu
SOCKETS : 
https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/234698-le-reseau
THREADS:
https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/2235545-la-programmation-parallele-avec-threading
"""

import socket
import sys
from threading import Thread, RLock
from Thread_Client_Writing import *
#from Thread_Server_Writing import *
#from Thread_Server_Listening import *
from Thread_Client_Listening import *


##### Mettre ici l'adresse IP du PC bord du bassin ######
#####----------------------------------------------######
#hote = "192.168.43.30" #sur InternetByMatth
#hote = "10.3.141.203" #sur raspi-DeRoBat pour Matthieu
hote = "10.3.141.243" #sur raspi-DeRoBat pour Quentin
#########################################################


PORT_ALLER = 12800
PORT_RETOUR = 12801
PORT_SONAR = 12802



# Création des threads
thread_listening = Listening_Client(PORT_ALLER, PORT_RETOUR, hote, PORT_SONAR)

# Lancement des threads
thread_listening.start()

# Attend que les threads se terminent
thread_listening.join()
