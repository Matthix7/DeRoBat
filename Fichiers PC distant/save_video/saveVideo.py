# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 10:57:33 2019

@author: Quentin
"""

import cv2
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


adressCam2 = 'http://root:1234@192.168.1.100/mjpg/video.mjpg'   
adressCam3 = 'http://root:1234@192.168.1.103/mjpg/video.mjpg'   
adressCam1 = 'http://root:1234@192.168.1.101/mjpg/video.mjpg'
  
newcameramtx, roi, mtx, dist =  calibration()

cap1 = cv2.VideoCapture()
cap1.open(adressCam1)

cap2 = cv2.VideoCapture()
cap2.open(adressCam2)

cap3 = cv2.VideoCapture()
cap3.open(adressCam3) 


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
outCam1 = cv2.VideoWriter('outputCam1.avi',fourcc, 20.0, (640,480))
outCam2 = cv2.VideoWriter('outputCam2.avi',fourcc, 20.0, (640,480))
outCam3 = cv2.VideoWriter('outputCam3.avi',fourcc, 20.0, (640,480))


while(True):
    key = cv2.waitKey(1) & 0xFF
    ret, frame1 = cap1.read()

    if ret==True:
        frame1 = cv2.flip(frame1,0)

        # write the flipped frame
        frame1 =undistort(frame1, newcameramtx, roi, mtx, dist)
        outCam1.write(frame1)

        cv2.imshow('CAM1',resizeFrame(frame1))
        
    else:
        print("No Cam 1")

        
    ret, frame2 = cap2.read()
    if ret==True:
        frame2 = cv2.flip(frame2,0)

        # write the flipped frame
        frame2 = undistort(frame2, newcameramtx, roi, mtx, dist)
        outCam2.write(frame2)

        cv2.imshow('CAM2',resizeFrame(frame2))
        
    else:
        print("No Cam 2")


    ret, frame3 = cap3.read()
    if ret==True:
        frame3 = cv2.flip(frame3,0)

        # write the flipped frame
        frame3 = undistort(frame3, newcameramtx, roi, mtx, dist)
        outCam3.write(frame3)

        cv2.imshow('CAM3',resizeFrame(frame3))
    else:
        print("No Cam 3")


        
        
    if key == ord('q'):
        break

# Release everything if job is finished
cap1.release()
cap2.release()
cap3.release()
outCam1.release()
outCam2.release()
outCam3.release()

cv2.destroyAllWindows()
