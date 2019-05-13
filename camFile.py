# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 15:26:25 2019

@author: Matthieu
"""

import cv2
import numpy as np
from threading import Thread


class Cam(Thread):
    """Prise en charge des fonctionnalités d'écriture du serveur"""
    
    def __init__(self):
        Thread.__init__(self)
        self.center1 = (0,0) 
        self.is_dead = "alive"
        self.compteur = 0
    
    
    def getMessage(self):
        message = str((self.center1[0], self.center1[1], 0))
        self.compteur += 1
        
        return message
    
    def isDead(self):
        return self.is_dead
    
    def run(self):

        cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)
        
        
        cap = cv2.VideoCapture(0)
        c = 0
        self.center1 = (0,0)
        
        # define range of blue color in HSV
        # voir https://www.google.com/search?client=firefox-b&q=%23D9E80F
        # convertir valeur dans [0,179], [0,255], [0,255]
        
        teinte_min = 160
        teinte_max = 207
        sat_min = 50
        sat_max = 100
        val_min = 51
        val_max = 100
        
        
        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, img = cap.read()
            
            if ret == True:
                
                # Take each frame
                frame = img
                
                # Convert BGR to HSV
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
                
                lower_yellow = np.array([int(teinte_min/2),int(sat_min*255/100),int(val_min*255/100)])
                upper_yellow = np.array([int(teinte_max/2),int(sat_max*255/100),int(val_max*255/100)])
                
                # Threshold the HSV image to get only yellow/green colors
                mask1 = cv2.inRange(hsv, lower_yellow, upper_yellow)
                mask1 = cv2.medianBlur(mask1, 5)
                        
                
                # Bitwise-AND mask and original image
                res = cv2.bitwise_and(frame,frame, mask= mask1)
        #        cv2.imshow('frame',frame)
        #        cv2.imshow('mask',mask1)
        #        cv2.imshow('res',res)
                
                
                
                ret1,thresh1 = cv2.threshold(mask1,127,255,0)
                im2,contours1,hierarchy1 = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, 2)
                
                if len(contours1) > 0:
                    cnt1 = max(contours1, key = cv2.contourArea)            
                    
                    (x1,y1),radius1 = cv2.minEnclosingCircle(cnt1)
                    self.center1 = (int(x1),int(y1))
                    radius1 = int(radius1)        
                    
                    cv2.circle(frame,self.center1,radius1,(255,0,0),2)
                    cv2.circle(frame,self.center1,5,(255,0,0),2)
                    
#                    print("Centre bleu :", self.center1)
                    
                cv2.imshow('Webcam',frame)
                
                
                
                key = cv2.waitKey(1) & 0xFF
                if key == 27:
                    self.center1 = (999,999)
                    self.is_dead = "dead"
                    break
                elif key == 32:
                    c += 1
                    cv2.imwrite('fra%i.png'%c,frame)
                    print("Picture saved")
                
        
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()