# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 17:05:33 2019

@author: Quentin
"""
import cv2
import cv2.aruco as aruco

from calibrate_camera import calibration, undistort

adressCam2 = 'http://root:1234@169.254.236.203/mjpg/video.mjpg'   
adressCam3 = 'http://root:1234@169.254.206.22/mjpg/video.mjpg'   
adressCam1 = 'http://root:1234@169.254.15.151/mjpg/video.mjpg'    

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

cap1 = cv2.VideoCapture()
cap1.open(adressCam1)

cap2 = cv2.VideoCapture()
cap2.open(adressCam2)

cap3 = cv2.VideoCapture()
cap3.open(adressCam3) 
    


while(True):
    
    key = cv2.waitKey(1) & 0xFF
    
    ret, frame1 = cap1.read()
    if ret:
        frame1 = undistort(frame1, newcameramtx, roi, mtx, dist)
        corner, ids = detectAruco(frame1)
        aruco.drawDetectedMarkers(frame1, corner, ids)
        cv2.imshow("Webcam 1", resizeFrame(frame1))
    else:
        print("No Cam 1")


    ret, frame2 = cap2.read()
    if ret:
        frame2 = undistort(frame2, newcameramtx, roi, mtx, dist)
        corner, ids = detectAruco(frame2)
        aruco.drawDetectedMarkers(frame2, corner, ids)
        cv2.imshow("Webcam 2", resizeFrame(frame2))
    else:
        print("No Cam 2")

        
    ret, frame3 = cap3.read()
    if ret:
        frame3 = undistort(frame3, newcameramtx, roi, mtx, dist)
        corner, ids = detectAruco(frame3)
        aruco.drawDetectedMarkers(frame3, corner, ids)
        cv2.imshow("Webcam 3", resizeFrame(frame3))
    else:
        print("No Cam 3")

#    frame1 = undistort(frame1, newcameramtx, roi, mtx, dist)    

    if key == 27:
        break

cap1.release()
cap2.release()
cap3.release()
cv2.destroyAllWindows()
