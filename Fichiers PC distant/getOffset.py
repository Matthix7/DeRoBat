# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 17:17:28 2019

@author: Quentin

Renvoie l'offset du sonar, a mettre dans le programme mappingFile.py à la variable self.offsetSonar
Procedure:
    On lance le programe ./Test_devices sur la rasp
    On Lance le Client.py sur la rasp
    On lance ce programme sur le PC
"""
import math
from threading import Thread

class GetOffset(Thread):
    
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

    def offsetSonar(self):
        """
        Regalge de l'offset du Sonar, 
        à ne faire qu'une fois que nous avons recu les premières valeur du sonar
        """
        print("---------Reglage offset Sonar-----------")
        print("      Laisser le bateau immobile")
        angleNom = 90
        minSonde = float('inf')
        minAngle = -1
        for sonde,angle in zip(self.sonde,self.angle_sonde):
    
            if sonde < minSonde and sonde != -1:
                minSonde = sonde
                minAngle = angle
                
        self.offset_sonar = angleNom - math.degrees(minAngle) 
        print("---------Offset Sonar, Mini Angle et Mini Sonde : ",self.offset_sonar, math.degrees(minAngle), minSonde)
    
if __name__ == "__main__":
                        
    if self.initSonar:
        self.initSonar = False
        self.offsetSonar()
                    
