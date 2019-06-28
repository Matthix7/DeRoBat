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
from threading import Thread
import time
from posRegulV2 import Cam

class Writing_Server(Thread):
    """Prise en charge des fonctionnalités d'écriture du serveur"""
    
    def __init__(self, PORT_ALLER):
        Thread.__init__(self)
        self.PORT_ALLER = PORT_ALLER
        
    
    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        hote = ''
        port = self.PORT_ALLER   
        
        serveur_lance = True
                      
        
        connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_principale.bind((hote, port))        
        connexion_principale.listen(5)
        print("Le serveur est prêt à écrire sur le port {}".format(port))
        
        sock_client, infos_connexion = connexion_principale.accept()
        
        # Création des threads
        thread_cam = Cam()
        
        # Lancement des threads
        thread_cam.start()
        
        while serveur_lance :
            time.sleep(0.5)
            
            #On récupère le message venant de la caméra
            msg_a_envoyer = thread_cam.getMessage()
            
            #On l'encode pour envoi par socket
            msg_a_envoyer = (str(msg_a_envoyer)+'_').encode()
            
            # On envoie le message
            sock_client.send(msg_a_envoyer)
            
            #L'appui sur echap dans la fenêtre Webcam déclenche la condition
            if thread_cam.isDead() == "dead":
                break
            
        # Signal d'extinction
        sock_client.send((str((999,999,999))+'_').encode())
        time.sleep(1)
        sock_client.send((str((999,999,999))+'_').encode())
        time.sleep(1)
        
        print("Ending write")
        thread_cam.join()
        sock_client.close()
        connexion_principale.close()
        print("Fermeture connexion écriture serveur")