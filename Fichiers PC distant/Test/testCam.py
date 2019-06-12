# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 17:05:33 2019

@author: Quentin
"""
import cv2
import cv2.aruco as aruco
from calibrate_camera import calibration, undistort

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

newcameramtx, roi, mtx, dist =  calibration()
cap = cv2.VideoCapture()
cap.open('http://root:1234@169.254.236.203/mjpg/video.mjpg')

while(True):
    
    key = cv2.waitKey(1) & 0xFF
    
    ret, frame = cap.read()
    corner, ids = detectAruco(frame)
    aruco.drawDetectedMarkers(frame, corner, ids)
    frame = undistort(frame, newcameramtx, roi, mtx, dist)

    
    cv2.imshow("Webcam", resizeFrame(frame))
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
