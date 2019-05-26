# -*- coding: utf-8 -*-
"""
Created on Tue May 21 13:05:35 2019

@author: Quentin
"""
import cv2

def getTouche():
    return cv2.waitKey(1) & 0xFF

def commande(servo, moteur, sensibilite = 1):
    touche = getTouche()
    
    if touche == ord('q'):
        servo = servo - sensibilite
    
    if touche == ord('d'):
        servo = servo + sensibilite
    
    if touche == ord('z'):
        moteur = moteur + sensibilite
    
    if touche == ord('s'):
        moteur = moteur - sensibilite
    
    return servo, moteur
        

if __name__ == "__main__":
    
    cap = cv2.VideoCapture(0)
    
    while(True):
        ret, frame = cap.read()
        cv2.imshow('frame',frame)
        
        if not commande(0,0):
            break

    cap.release()
    cv2.destroyAllWindows()

    
