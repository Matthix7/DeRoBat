# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 14:15:55 2019

@author: Quentin
"""

import numpy as np
import cv2
import glob

def calibration():

    print("Define Calibration Parameter...")
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
    
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    
    images = glob.glob('calib_images/*.jpg')
    i = 0
    for fname in images:
        print(len(images)-i, " images remaining")
        i+=1
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
    
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
    
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)
    
            # Draw and display the corners
#            img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
#            cv2.imshow('img',cv2.resize(img,(int(img.shape[1]*0.4),int(img.shape[0]*0.4))))
#            cv2.waitKey(5)
    
#    cv2.destroyAllWindows()
    
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    print("Get Optimal Parameter...")
    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    return newcameramtx, roi, mtx, dist

def undistort(img, newcameramtx, roi, mtx, dist):
    
#    print("Undistort image...")
    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    
#    print("Crop Image according to ROI...")
    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
#    cv2.imshow('calibresult',cv2.resize(dst,(int(dst.shape[1]*0.4),int(dst.shape[0]*0.4))))
    return dst

if __name__ == "__main__":
    img = cv2.imread("left0.jpg")
    newcameramtx, roi, mtx, dist =  calibration()
    new_img = undistort(img, newcameramtx, roi, mtx, dist)
    cv2.imshow('calibresult',cv2.resize(new_img,(int(new_img.shape[1]*0.4),int(new_img.shape[0]*0.4))))