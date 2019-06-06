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
from threading import Thread, Lock, Event
import select
from Thread_Server_Writing import Writing_Server
from mappingFile import Map


class Listening_Server(Thread):
    """Prise en charge des fonctionnalités d'écoute du serveur"""
    
    def __init__(self, PORT_ALLER, PORT_RETOUR, inter_thread):
        Thread.__init__(self)
        # Définition des ports utiles
        self.PORT_ALLER = PORT_ALLER
        self.PORT_RETOUR = PORT_RETOUR
        
        self.generalAlive = inter_thread
        
        # Synchronise l'extinction de listening et mapping
        self.alive = Event()
        self.alive.set()
        
        # Synchronise les lectures/écritures dans mesures.txt
        self.verrou = Lock()
        
        #Préparation du fichier de sauvegarde des mesures
        self.filename = 'mesures.txt'
        self.file = open(self.filename, 'w')
        self.file.write("(x, y, cap, sonde, angle_sonde)\n")
        self.file.close()
        
        self.X, self.Y, self.Z, self.xBoat, self.yBoat = [], [], [], 0, 0
        
        
        
    def toMap(self):
        return self.X, self.Y, self.Z, self.xBoat, self.yBoat
    
    
    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        hote = ''
        port = self.PORT_RETOUR        
        
        connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_principale.bind((hote, port))
        connexion_principale.listen(5)
        print("Le serveur écoute à présent sur le port {}".format(port))
        
        
        # Création des threads
        thread_map = Map(self.verrou, self.filename, self.alive)
        thread_writing = Writing_Server(self.PORT_ALLER)
        
        
        # Lancement du tread d'écriture
        thread_writing.start()
        
        # Attente de connexion        
        sock_client, infos_connexion = connexion_principale.accept()
        
        # Lancement du thread de traitement
        thread_map.start()
        
        while self.alive.isSet():
                                       
            try:
                clients_a_lire, wlist, xlist = select.select([sock_client],[], [])
        
            except select.error:
                pass
        
            else:
                       
                # Client est de type socket
                msg_recu = sock_client.recv(1024)
                # Peut planter si le message contient des caractères spéciaux
                msg_recu = msg_recu.decode()
#                print("Reçu Client {}".format(msg_recu))
                
                if msg_recu != '' and self.verrou.acquire(blocking = False):
#                    print("entree listening")
                    
                    self.file = open(self.filename, 'a')
                    self.file.write(str(msg_recu)+"\n")
                    self.file.close()
                    
                    self.verrou.release()
#                    print("sortie listening")
                
                if eval(msg_recu)[0] == 999:
                    self.alive.clear()
                
                sock_client.send(b"Client 5 / 5")
                
                mapLock, X, Y, Z, xBoat, yBoat = thread_map.toMap()
                if not mapLock:
                    self.X, self.Y, self.Z, self.xBoat, self.yBoat = X, Y, Z, xBoat, yBoat
                                
                    
    
        self.file.close()
        print("Ending listen") 
    
        self.generalAlive.clear()
                  
        thread_writing.join()
        thread_map.join()
        
        sock_client.close()
        connexion_principale.close()
        print("Fermeture connexion écoute serveur")

