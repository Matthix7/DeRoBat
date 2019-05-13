# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 13:44:02 2019

@author: catam
"""

import time
from threading import Thread
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import pi, cos, sin


class Map(Thread):
    """Utilisation du fichier mesures.txt pour générer l'affichage 3D du fond.
    On récupère environ 10 valeurs du sonar par seconde dans mesures.txt,
    et on les copie dans testFile.txt pour utilisation ultérieure.
    L'ensemble de la chaîne (mutex ci-dessous inclus) fait perdre environ 3% 
    des acquisitions du sonar."""
    
    def __init__(self, verrou, filename, inter_thread):
        Thread.__init__(self)
        self.alive = inter_thread
        self.filename = filename
        
        self.verrou = verrou
        self.memoire = 0
        self.input_lines = 0
        
        self.test = open("testFile.txt", 'w')
        self.test.write("(x, y, cap, sonde, angle_sonde)\n")
        self.test.close()
        
#        self.fig=plt.figure()
#        plt.title("Représentation bathymétrique du bassin") 
        
        self.X, self.Y, self.Z = [], [], []
        self.Xcopy, self.Ycopy, self.Zcopy = [], [], []
        self.mapLock = False
    
    def toMap(self):
        return self.mapLock, self.Xcopy, self.Ycopy, self.Zcopy
    
    def run(self):
        
        # On se synchronise avec listening
        while self.alive.isSet():
            measures = []
            self.X, self.Y, self.Z = [], [], []
            
            # On peut lire si listening n'est pas en train d'écrire
            #On commence par compter le nombre de lignes du fichier de mesures
            if self.verrou.acquire(blocking = False):
                print("entree map1")
                measureFile = open(self.filename, 'r')
                
                for i, ligne in enumerate(measureFile):
                    pass
                self.input_lines = i+1
                
                measureFile.close()
                self.verrou.release()
                print("sortie map1")
                time.sleep(1)
                
                
            #Si l'on a un bon nombre de nouvelles mesures disponibles, on les copie.
            if self.input_lines-self.memoire > 50:
                
                if self.verrou.acquire(blocking = True):
                
                    print("entree map2")
                    measureFile = open(self.filename, 'r')
                   
                    for i, ligne in enumerate(measureFile):
                        if i > 2 and i > self.memoire:
                            measures.append(ligne)
                    
                    measureFile.close()
                    self.verrou.release()
                    print("sortie map2")
                
                #Copie dans un autre fichier, exploitable sans risque de pertes.
#                self.test = open("testFile.txt", 'a')
                self.mapLock = True
                for line in measures:
#                    self.test.write(line)
                    
                    #On récupère les valeurs pour plot
                    mes = eval(line)
                    x, y, cap, sonde, angle_sonde = mes[0], mes[1], mes[2], mes[3], 2*pi*mes[4]/360
                    
                    if sonde != -1.0:
                        self.X.append(x+sin(cap)*sonde*sin(angle_sonde))
                        self.Y.append(y-cos(cap)*sonde*sin(angle_sonde))
                        self.Z.append(-sonde*cos(angle_sonde)) #cos(pi ± angle_sonde) plus vraisemblablement
                    
                self.Xcopy, self.Ycopy, self.Zcopy = self.X, self.Y, self.Z
#                self.test.close()
                self.memoire = self.input_lines
                self.mapLock = False
                
                
                
                
                
#                # Représentation 3D
#                plt.scatter(self.X, self.Y, c = self.Z)
#                plt.pause(0.05)
                
                
                
            
            
            
            
            
            