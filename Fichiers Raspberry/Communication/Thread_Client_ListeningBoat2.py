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
from threading import Thread, RLock, Event
import select
import Thread_Client_Writing
from Thread_Client_Listening import *

import serial
import time

#arduino = serial.Serial('/dev/ttyACM0', 115200)


class Listening_Client(Thread):
    """Prise en charge des fonctionnalités d'écoute du serveur"""
    
    def __init__(self, PORT_ALLER, PORT_RETOUR, hote, PORT_SONAR):
        Thread.__init__(self)
        self.PORT_ALLER = PORT_ALLER
        self.PORT_RETOUR = PORT_RETOUR
        self.PORT_SONAR = PORT_SONAR
        self.hote = hote
        self.alive = Event()
        self.alive.set()
        self.pos = (0,0,0)
        
        
    def getPos(self):         
         return self.pos
    
    
    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        
                
        hote = self.hote
        port = self.PORT_ALLER    
        
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        sock_server.connect((hote, port))
        print("Connexion d\'écoute établie avec le serveur sur le port {}".format(port))
        
        
         # Création des threads
        thread_writing = Thread_Client_Writing.Writing_Client(self, self.PORT_RETOUR, self.hote, self.alive, self.PORT_SONAR)
        
        # Lancement des threads
        thread_writing.start()        
        
                
        while self.alive.isSet():
            
            try:
                serveur_a_lire, wlist, xlist = select.select([sock_server],[], [])
        
            except select.error:
                pass
        
            else:
                
                # Client est de type socket
                msg_recu = sock_server.recv(1024)
                
                            
                # Peut planter si le message contient des caractères spéciaux
                msg_recu = msg_recu.decode()
                #~ print("Reçu Serveur{}".format(msg_recu))
                
                
                try:
                    msg_recu = msg_recu.split('_')[-2]
                except:
                    msg_recu = msg_recu.split('_')[0]
                    

                tuple_recu = eval(msg_recu)
                print("Reçu Serveur{}".format(tuple_recu))
                
                
                # On s'arrête en cas de réception du message d'arrêt
                if tuple_recu in [(999, 999, 999), (999,999,0), (999,999,999,0,0)]:
                    self.alive.clear()
                    
                    message1 = str(int(1090+offset))
                    message1 = message1.encode()
                    message2 = str(2000)
                    message2 = message2.encode()
                    
                    #arduino.write(message2)
                    time.sleep(0.5)
                    #arduino.write(message1)
                    
                    time.sleep(0.5)
                    print("End Mission")
                    break
                
                
                else:
                    self.pos = (tuple_recu[0], tuple_recu[1], tuple_recu[2])
                    commande = (tuple_recu[3], tuple_recu[4])
                    
                    
                    msg_arduino1 = commande[0]  #servo
                    msg_arduino2 = commande[1]  #moteur
                    
                    offset = 0 #Correction servo
                    msg_arduino1 = int(max(1040,min(msg_arduino1, 1180-40))+offset)
                    
                    if msg_arduino2 < 3000:
                        msg_arduino2 = int(max(2000,min(msg_arduino2, 2254)))
                    if msg_arduino2 >= 3000:
                        msg_arduino2 = int(max(3000,min(msg_arduino2, 3254)))
                    
                    msg_arduino1 = str(msg_arduino1).encode()  #Commande servo
                    msg_arduino2 = str(msg_arduino2).encode()  #Commande moteur
                    
                    #arduino.write(msg_arduino1)
                    time.sleep(0.25)
                    #arduino.write(msg_arduino2)
                    time.sleep(0.25)    
                
                
        thread_writing.join()
        
        sock_server.close()            
        print("Fermeture de la connexion écoute client")
        
        
    
















