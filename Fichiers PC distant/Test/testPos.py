# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:14:37 2019

@author: Quentin
"""
import cv2
import cv2.aruco as aruco
import math
import numpy as np
bordBassin = dict() #pour la position des aruco sur le bord

def resizeFrame(frame):
    """
    frame : image a resize (l'image de la camera étant trop grande pour mon ecran)
    Return:
        newFrame: image resize
    """
    
    imgScale = 0.4
    newX,newY = frame.shape[1]*imgScale, frame.shape[0]*imgScale
    newFrame = cv2.resize(frame,(int(newX),int(newY)))
    
    return newFrame


def detectAruco(image):#return aruco's position and id
    """
    image : image ou on doit trouver les Arucos
    Return:
        corners : Position de chaque Aruco dans l'image
        ids : Id de chaque Aruco dans l'image
    """
        
    #image = cv2.imread(image)
    
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)#only for aruco from the database
    parameters = aruco.DetectorParameters_create()
    
    
    corners, ids, rejectedImgPoints = aruco.detectMarkers(image, aruco_dict, parameters=parameters)

    return corners, ids

def getArucoCenter(corner):
    """
    corner : position du code Aruco dans l'image
    Return:
        x : position en x du centre du code Aruco
        y : position en y du centre du code Aruco
    """
        
    y =int((corner[0][0] + corner[1][0] + corner[2][0] + corner[3][0]) /4)#centre du code en Y
    x = int((corner[0][1] + corner[1][1] + corner[2][1] + corner[3][1]) /4)#centre du code en Y
    
    return x,y

def getBordBassinNoCalib(corners1, ids1):
    #------ On recupère le bords du bassin ---------
        
    if not(ids1 is None) and len(ids1) > 0: 
        for id in ids1:
            if id != 4 and id != 5:
                
                i,j = np.where(ids1 == id)
                
                cornerBassin = corners1[i[0]][j[0]]
                
#                xBassin, yBassin = undistorted(cornerBassin, K,D)
                
                xBassin, yBassin = getArucoCenter(cornerBassin)
                            
                bordBassin[id[0]] = xBassin,yBassin
def getTheta():
    """
    Return:
        angle de rotation entre bordBassin et camera axis
    """
    return math.pi/2 - math.atan2(bordBassin[10][1] - bordBassin[0][1], bordBassin[10][0] - bordBassin[0][0])

    
def getRotationMatrix(theta):
    """
    theta : angle de rotation entre plan 1 et plan 2
    Return:
        matrice de rotation entre plan 1 et plan 2
    """
    return np.array([[math.cos(theta), -math.sin(theta)],
                     [math.sin(theta), math.cos(theta)]])




def getPositionNoCalib(corners1, ids1, frame1):
    
    """
    corners1 : Corners frame Cam 1
    ids1 : Ids Frame Cam 1
    frame1 : Frame Cam 1
    
    Return:
        xBoat: position en X du bateau
        yBoat: position en Y du bateau (il est inversé ?)
    """
    
    getBordBassinNoCalib(corners1,ids1)
    
#------ On recupère la position du bateau -------
    
    i,j = np.where(ids1 == 5)
    if len(i) == 0:
        return None,None
    cornerBoat5 = corners1[i[0]][j[0]]
    
    #x4,y4 = getArucoCenter(cornerBoat4)


    x5,y5 = getArucoCenter(cornerBoat5)
        
    x = x5
    y = y5 

    
    if len(bordBassin) > 1:
        
        pos = np.array([[abs(x - bordBassin[0][0])],
                        [abs(y - bordBassin[0][1])]])
    
        if 0 in bordBassin and 10 in bordBassin and 12 in bordBassin:
            pos = getRotationMatrix(getTheta()) @ pos
        else:
            return None, None
        
        xBoat = pos[0][0]
        yBoat = pos[1][0]

    else:
        xBoat,yBoat = None,None

 
    return xBoat,yBoat

    



cap = cv2.VideoCapture()
cap.open('http://root:1234@169.254.236.203/mjpg/video.mjpg')

while(True):
    
    key = cv2.waitKey(1) & 0xFF
    
    ret, frame = cap.read()
    corner, ids = detectAruco(frame)
    aruco.drawDetectedMarkers(frame, corner, ids)
    
    
    x, y = getPositionNoCalib(corner,ids,frame)
    if not x is None:
        print("--------Draw Boat--------")
        print(x,y)
        pos = np.array([[abs(x + bordBassin[0][0])],
                        [abs(y + bordBassin[0][1])]])
    
        pos =  np.linalg.inv(getRotationMatrix(getTheta())) @ pos 
 
        x = pos [0][0]
        y = pos[1][0]
        frame[int(x-10):int(x+10), int(y-10):int(y+10)] = [0,0,255]
    cv2.imshow('Arcuo', resizeFrame(frame))

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
