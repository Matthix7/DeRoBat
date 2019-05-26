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
import time
from threading import Thread, RLock
import select
from Thread_Client_Writing import *
#from Thread_Server_Listening import *
from Thread_Client_Listening import *
#from Thread_Server_Writing import *


class Writing_Client(Thread):
    """Prise en charge des fonctionnalités d'écriture du client"""
    
    def __init__(self, thread_listening, PORT_RETOUR, hote, inter_thread, PORT_SONAR):
        Thread.__init__(self)
        self.listening_client = thread_listening
        self.PORT_RETOUR = PORT_RETOUR
        self.PORT_SONAR = PORT_SONAR
        self.hote = hote
        self.alive = inter_thread
        
    
    def run(self):
        """Code à exécuter pendant l'exécution du thread."""   
        
        hote = self.hote
        port = self.PORT_RETOUR
        sonar = self.PORT_SONAR
        
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        sock_server.connect((hote, port))
        print("Connexion d\'écriture établie avec le serveur sur le port {}".format(port))
        
        sock_sonar= socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        sock_sonar.connect(("127.0.0.1", sonar))
        print("Connexion d'écoute établie avec le sonar sur le port {}".format(sonar))
        
        
        while self.alive.isSet():
            
            pos = self.listening_client.getPos()
            
            ############################################################
            ################      Ecoute sonar       ###################            
            ############################################################
            
            try:
                serveur_a_lire, wlist, xlist = select.select([sock_sonar],[], [])
        
            except select.error:
                pass
        
            else:
                
                # Client est de type socket
                msg_recu = sock_sonar.recv(1024)
                
                # Peut planter si le message contient des caractères spéciaux
                msg_recu = msg_recu.decode()
                try:
                    msg_recu = msg_recu.split()[-2]
                except:
                    msg_recu = msg_recu.split()[0]
    
                #~ print("Reçu Sonar {}".format(msg_recu))
                data_sonar = eval(msg_recu)
    
                
                
            
            ############################################################
            ################    Ecriture serveur   #####################            
            ############################################################
                        
            msg_a_envoyer = str(pos+data_sonar)            
                            
            msg_a_envoyer = msg_a_envoyer.encode()
                
            # On envoie le message
            sock_server.send(msg_a_envoyer)
            msg_recu = sock_server.recv(1024)
            print("Envoi Serveur{}".format(msg_a_envoyer.decode()))# Là encore, peut planter s'il y a des accents
            time.sleep(0.0075) # Ajusté pour essayer d'exploiter toutes les acquisitions
        
        
        msg_a_envoyer = "(999,999,999,999,999)"            
                            
        msg_a_envoyer = msg_a_envoyer.encode()
            
        # On envoie le message
        sock_server.send(msg_a_envoyer)
        msg_recu = sock_server.recv(1024)
        print("Envoi Serveur{}".format(msg_a_envoyer.decode()))# Là encore, peut planter s'il y a des accents
        
        sock_sonar.close()
        sock_server.close()
        print("Fermeture de la connexion écriture client")
        
        
