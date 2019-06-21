# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 09:56:08 2019

@author: Quentin
"""
import cv2
import cv2.aruco as aruco
import numpy as np

from calibrate_camera import calibration, undistort

bordBassin = dict()
adressCam1 = 'http://root:1234@169.254.236.203/mjpg/video.mjpg'   
adressCam2 = 'http://root:1234@169.254.206.22/mjpg/video.mjpg'   
adressCam3 = 'http://root:1234@169.254.234.41/mjpg/video.mjpg'   

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

def getBordBassin(corners1, ids1, cam2=False, cam3=False):
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
                
                if (id[0] == 1 or id[0] == 11) and not(cam2): #on est sur la cam1 et on voit 1 et 11 (sert pour getDist)
                    cornerBassin = corners1[i[0]][j[0]]
                                    
                    xBassin, yBassin = getArucoCenter(cornerBassin)
                                
                    bordBassin[str(id[0])] = xBassin,yBassin #on enregistre getDist sur un str pour pas confondre avec le 0 de cam2

                    
                    
                elif (id[0] == 2 or id[0] == 12) and not(cam3):
                
                    cornerBassin = corners1[i[0]][j[0]]
                                    
                    xBassin, yBassin = getArucoCenter(cornerBassin)
                                
                    bordBassin[str(id[0])] = xBassin,yBassin
                    
                else:
                    cornerBassin = corners1[i[0]][j[0]]
                                    
                    xBassin, yBassin = getArucoCenter(cornerBassin)
                                
                    bordBassin[id[0]] = xBassin,yBassin

def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    w_min = im_list[0].shape[1]
    for im in im_list:
        if w_min > im.shape[1]:
            w_min = im.shape[1]
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)


def cutImage(frame, corners, ids, number):
    
    if number == 1 :
        while not(10 in bordBassin and 0 in bordBassin and str(1) in bordBassin):
            getBordBassin(corners, ids)
            print(bordBassin)
        x = bordBassin[0][0] -10
        y = bordBassin[0][1] -10
        h = abs(bordBassin[10][1] - bordBassin[0][1]) +10
        w = abs(bordBassin[0][0] - bordBassin[str(1)][0]) +10
        crop_img = frame[x:x+w,y:y+h]
        return crop_img
    
    if number == 2:
        while(11 in bordBassin and str(2) in bordBassin and 1 in bordBassin):
            getBordBassin(corners, ids, cam2 = True)
        x = bordBassin[1][0] -10
        y = bordBassin[1][1] -10
        h = abs(bordBassin[11][1] - bordBassin[1][1]) +10
        w = abs(bordBassin[1][0] - bordBassin[str(2)][0]) +10
        crop_img = frame[x:x+w,y:y+h]
        return crop_img

    if number == 3:
        while(2 in bordBassin and 12 in bordBassin and 3 in bordBassin):
            getBordBassin(corners, ids , cam3 = True)
        x = bordBassin[2][0] -10
        y = bordBassin[2][1] -10
        h = abs(bordBassin[12][1] - bordBassin[2][1]) +10
        w = abs(bordBassin[2][0] - bordBassin[3][0]) +10
        crop_img = frame[x:x+w,y:y+h]
        return crop_img


if __name__ == "__main__":

    newcameramtx, roi, mtx, dist =  calibration()
    
    cap1 = cv2.VideoCapture()
    cap1.open(adressCam1)
    ret, frame1 = cap1.read()
    if ret:
        frame1 = undistort(frame1, newcameramtx, roi, mtx, dist)
        corner, ids = detectAruco(frame1)
        cap1.release()
        crop1 = cutImage(frame1, corner, ids, 1)
    #    cv2.imshow("Frame 1", resizeFrame(crop1))
    else:
        crop1 = np.ones((2000,2000))
        
    cap2 = cv2.VideoCapture()
    cap2.open(adressCam2)
    ret, frame2 = cap2.read()
    if ret:
        frame2 = undistort(frame2, newcameramtx, roi, mtx, dist)
        corner, ids = detectAruco(frame2)
        cap2.release()
        crop2 = cutImage(frame2, corner, ids, 2)
    #    cv2.imshow("Frame 2", resizeFrame(crop2))
        
    else:
        crop2 = crop1 * 0
    
    cap3 = cv2.VideoCapture()
    cap3.open(adressCam3) 
    ret, frame3 = cap3.read()
    if ret:
        frame3 = undistort(frame3, newcameramtx, roi, mtx, dist)
        corner, ids = detectAruco(frame3)
        cap3.release()
        crop3 = cutImage(frame3, corner, ids, 3)
    #    cv2.imshow("Frame 3", resizeFrame(crop3))
    else:
        crop2 = crop1 * 0
    
    
    
    im_v_resize = vconcat_resize_min([crop1, crop2,crop3])
    cv2.imwrite('backgroundPlot.png', im_v_resize)