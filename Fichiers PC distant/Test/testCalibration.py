# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:26:18 2019

@author: Quentin
"""
import cv2
import cv2.aruco as aruco
from calibrate_camera import calibration, undistort
import numpy as np
import math
import matplotlib.pyplot as plt


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



def getBordBassin(corners1, ids1):
    """
    corners1 : Corner de la frame
    ids1 : id de la frame
    
    -> Met bordBassin à jour avec les arucos (sauf 4 et 5)
    """
    #------ On recupère le bords du bassin ---------
        
    if not(ids1 is None) and len(ids1) > 0: 
        for id in ids1:
            if id != 4 and id != 5:
                
                i,j = np.where(ids1 == id)
                
                cornerBassin = corners1[i[0]][j[0]]
                
#                xBassin, yBassin = undistorted(cornerBassin, K,D)
                
                xBassin, yBassin = getArucoCenter(cornerBassin)
                            
                bordBassin[id[0]] = xBassin,yBassin




def getPosition(corners1, ids1, frame1):
    
    """
    corners1 : Corners frame Cam 1
    ids1 : Ids Frame Cam 1
    frame1 : Frame Cam 1
    
    Return:
        xBoat: position en X du bateau
        yBoat: position en Y du bateau
    """
    
    getBordBassin(corners1, ids1)  
    x, y = None, None
    i,j = [],[]
    #------ On recupère la position du bateau -------
    if not ids1 is None and 4 in ids1:
    
        i,j = np.where(ids1 == 4)
    
    if len(i) > 0:
        
        cornerBoat4 = corners1[i[0]][j[0]]
        
        x4,y4 = getArucoCenter(cornerBoat4)
        
        x = x4 
        y = y4
    
#--- On ajuste la position du bateau au bassin ---
    if 0 in bordBassin and 10 in bordBassin and 12 in bordBassin and not x is None:
        
        pos = np.array([[abs(x - bordBassin[0][0])],
                        [abs(y - bordBassin[0][1])]])
    
    
        pos = getRotationMatrix(getTheta()) @ pos
        
        
        xBoat = pos[0][0] * 3.5/(bordBassin[12][0] - bordBassin[0][0])
        yBoat = pos[1][0] * 3/(bordBassin[10][1] - bordBassin[0][1])

    else:
        xBoat,yBoat = None,None

#-------------------------------------------------

    return xBoat, yBoat





def getCap(corners1, ids1):
    """
    corners1 : Corners Arucos du bateau
    ids1 : Ids Arucos du Bateau
    
    Return:
        angle : cap en radians 
    """
    angle = math.nan
    if 0 in bordBassin and 10 in bordBassin:
    
        i1,j1 = np.where(ids1 == 4)
        i2,j2 = np.where(ids1 == 5)
    
        arucoBoat1 = corners1[i1[0]][j1[0]]
        xAr4, yAr4 = getArucoCenter(arucoBoat1)
        
        arucoBoat2 = corners1[i2[0]][j2[0]]  
        xAr5, yAr5 = getArucoCenter(arucoBoat2)
            
        angle = math.atan2( yAr5-yAr4, xAr5-xAr4 ) - getTheta()
    
    return (angle)
    

newcameramtx, roi, mtx, dist =  calibration()
cap = cv2.VideoCapture()
cap.open('http://root:1234@169.254.236.203/mjpg/video.mjpg')
print("Acquisition running...")

fig = plt.figure()
plt.title("Test Calibration")

ax = fig.add_subplot(111)

plt.xlim(-1,5)
plt.ylim(-1,4)
plt.xlabel('Red = No Calib, Green = Calib')

plt.grid()

plt.gca().set_aspect('equal', adjustable = 'box')
plt.gca().invert_xaxis() #on inverse l'axe x (correspond au y de l'image)
ax.yaxis.tick_right()


while(True):
    
    key = cv2.waitKey(1) & 0xFF
    
    ret, frameNC = cap.read()
    frameC = undistort(frameNC, newcameramtx, roi, mtx, dist)
    
    cornerNC, idsNC = detectAruco(frameNC)
    aruco.drawDetectedMarkers(frameNC, cornerNC, idsNC)
    cornerC, idsC = detectAruco(frameC)
    aruco.drawDetectedMarkers(frameC, cornerC, idsC)
    
    cv2.imshow('Frame No Calib', resizeFrame(frameNC))
    
    cv2.imshow('Frame Calib', resizeFrame(frameC))
    
    xnc, ync = getPosition(cornerNC,idsNC,frameNC)
    xc, yc = getPosition(cornerC,idsC,frameC)

    if xc is None or xnc is None:
        print("xc or xnc is None")
        print("xc : ", xc)
        print("xnc : ", xnc)
    else:

        if key == ord('s'):
            print("acquis")
            plt.scatter(ync,xnc, marker = 'o', c="red")
            plt.scatter(yc,xc, marker = 'o', c="green")
            plt.pause(2)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
