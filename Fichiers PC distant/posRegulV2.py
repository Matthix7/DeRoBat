import cv2
import numpy as np
import cv2.aruco as aruco
import cv2.fisheye as fisheye
import math
from threading import Thread
from regulation2 import getCommande
from numpy.linalg import norm

from calibrate_camera import calibration, undistort


bordBassin = dict() #pour la position des aruco sur le bord

distAr0Ar1 = 3.5 #distance entre l'aruco 0 et 1 (axe des X)
distAr0Ar10 = 3 #distance entre l'aruco 0 et 10 (axe des Y)


############# #Check adresse avec IPUtility #################################
#############################################################################
adressCam1 = 'http://root:1234@169.254.236.203/mjpg/video.mjpg'   
adressCam2 = 'http://root:1234@169.254.206.22/mjpg/video.mjpg'   
adressCam3 = 'http://root:1234@169.254.234.41/mjpg/video.mjpg'    

#############################################################################
#############################################################################

oldCap = 1 #Camera d'ou provient la video (pour l'optimisation)

class Cam(Thread):
    """Acquisition d'images et extraction de la pose du bateau."""
    
    def __init__(self):
        Thread.__init__(self)
        self.is_dead = "alive"
                        
        self.message = str((-1,-1,-1,0,0)) 
        self.commande = (1090,2000)
        
        print('Calibration running...')
        self.newcameramtx, self.roi, self.mtx, self.dist =  calibration()
        
        
        

    def getMessage(self):
        return self.message      # (xBoat, yBoat, heading, servoCommand, motorCommand)
    
    
    
    def isDead(self):
        return self.is_dead
    
    
    
    def run(self):
        cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)
        
        
        neutreServo, neutreMoteur = 1090, 2000
        commandes = np.array([[neutreServo], [neutreMoteur]])
        
        Waypoints = [[0,3],# ,3   ,0.5 ,0.5], #X
                     [3,1]]# ,2.5 ,0.5 ,2.5]] #Y
    
        for k in range(len(Waypoints[0])-1):
            a = np.array([[Waypoints[0][k]], [Waypoints[1][k]]])
            b = np.array([[Waypoints[0][k+1]], [Waypoints[1][k+1]]])

        
#        xTarget = 3.5
#        yTarget = 0.5
        vTarget = 0.4
#        
#        a = np.array([[4], [0]])    
#        b = np.array([[xTarget], [yTarget]])
        X = np.array([[0], [0], [0], [0], [0]])
        
        print('Acquisition running...')
        while True or ((b-a).T @ (b-X[:2])) / (norm(b-a)*norm(b-X[:2])) >= 0:
            
            xBoat, yBoat,theta = run_one_step(a,b,self.newcameramtx, self.roi, self.mtx, self.dist)

            
# =============================================================================
#             Bloc régulation
#            array commandes = ([[radians], [m/s]])
#            array self.commande = ([[pwm], [pwm]])
# =============================================================================
            
            posServo = commandes[0,0]
            posMoteur = commandes[1,0]
            
            if not xBoat is None: #si le bateau n'est pas vu sur la camera -> soustraction sur un None = Bug
            
                X = np.array([[xBoat], [yBoat], [theta], [posServo], [posMoteur]])
                commandes = getCommande(X, a, b, vTarget, commandes)  #Appel module regulation
                
                if commandes[1,0] >= 0:
                    self.commande = (175*commandes[0,0]+neutreServo, (238*commandes[1,0]) + 2000)
                if commandes[1,0] < 0:
                    self.commande = (175*commandes[0,0]+neutreServo, (390*abs(commandes[1,0])) + 3000)
            
                self.commande = (neutreServo, neutreMoteur) #on retire la regualtion
            elif xBoat is None:
                self.commande = (neutreServo, neutreMoteur) #on arrete le bateau si on ne le voit pas 

# =============================================================================
#             Expédition des données utiles en aval
# =============================================================================
            if xBoat != None and yBoat != None:
                print("X = ", xBoat, "\nY = ", yBoat, "\ntheta =", math.degrees(theta))       
                self.message = str( (xBoat , yBoat, theta) + self.commande)
            
            if xBoat == None or yBoat == None:
                self.message = str( (-1, -1, -1) + self.commande)
                
            print("Commande = ", self.commande)
            
            
# =============================================================================
#             Fin du programme
# =============================================================================
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27: #  echap to quit
                self.message = str((999,999,999,0,0))
                self.is_dead = "dead"
                break
            
        print('Acquisition ended.')
        cv2.destroyAllWindows()
        self.message = str((999,999,999,0,0))
        self.is_dead = "dead"




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






#
#def undistorted(corner,K,D):
#    """
#    corner : position du code Aruco dans l'image
#    
#    Return:
#        Point central de l'Aruco après calibration
#    """
#    
#    input_points = np.zeros([1,1,2])
#            
#    x,y = getArucoCenter(corner)
#    
#    input_points[0,0,0] = x
#    input_points[0,0,1] = y
#    
#    undistorted = fisheye.undistortPoints(input_points,K,D, R=None, P=K)
#    
#    return undistorted.reshape(1,2)[0,0], undistorted.reshape(1,2)[0,1]
    

def getThetaCam1():
    """
    Return:
        angle de rotation entre bordBassin et camera axis
    """
    if 10 in bordBassin and 0 in bordBassin:
        return math.pi/2 - math.atan2(bordBassin[10][1] - bordBassin[0][1], bordBassin[10][0] - bordBassin[0][0])
    return math.nan

def getThetaCam2():
    """
    Return:
        angle de rotation entre bordBassin et camera axis
    """
    if 11 in bordBassin and 1 in bordBassin:
        return math.pi/2 - math.atan2(bordBassin[11][1] - bordBassin[1][1], bordBassin[11][0] - bordBassin[1][0])
    return math.nan
def getThetaCam3():
    """
    Return:
        angle de rotation entre bordBassin et camera axis
    """
    if 12 in bordBassin and 2 in bordBassin:
        return math.pi/2 - math.atan2(bordBassin[12][1] - bordBassin[2][1], bordBassin[12][0] - bordBassin[2][0])
    return math.nan
    
def getRotationMatrix(theta):
    """
    theta : angle de rotation entre plan 1 et plan 2
    Return:
        matrice de rotation entre plan 1 et plan 2
    """
    return np.array([[math.cos(theta), -math.sin(theta)],
                     [math.sin(theta), math.cos(theta)]])



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


def getDistCam2():
    """
    Renvoie la distance (en pixel) à ajouter pour avoir la position du bateau dans la camera 2
    dist entre 0 et 1
    """
    
    return abs(bordBassin[0][0] - bordBassin[str(1)][0])

def getDistCam3():
    """
    Renvoie la distance (en pixel) à ajouter pour avoir la position du bateau dans la camera 3
    dist entre 0 et 2
    """
    
    return getDistCam2() + abs(bordBassin[1][0] - bordBassin[str(2)][0])


def getPositionCam1(corners1, ids1, frame1):
    
    """
    corners1 : Corners frame Cam 1
    ids1 : Ids Frame Cam 1
    frame1 : Frame Cam 1
    
    Return:
        xBoat: position en X du bateau
        yBoat: position en Y du bateau
    """
    
    getBordBassin(corners1, ids1)    
    #------ On recupère la position du bateau -------
    
    i,j = np.where(ids1 == 4)
    k,l = np.where(ids1 == 5)
    
    cornerBoat4 = corners1[i[0]][j[0]]
    cornerBoat5 = corners1[k[0]][l[0]]
    
    x4,y4 = getArucoCenter(cornerBoat4)
    x5,y5 = getArucoCenter(cornerBoat5)
    
    x = (x4 + x5)/2
    y = (y4 + y5)/2
    
    drawBoat(frame1, x, y)

    
#--- On ajuste la position du bateau au bassin ---
    if 0 in bordBassin and 10 in bordBassin and str(1) in bordBassin:        
        pos = np.array([[abs(x - bordBassin[0][0])],
                        [abs(y - bordBassin[0][1])]])
    
        pos = getRotationMatrix(getThetaCam1()) @ pos
        
        xBoat = pos[0][0] * distAr0Ar1/(bordBassin[str(1)][0] - bordBassin[0][0])
        yBoat = pos[1][0] * distAr0Ar10/(bordBassin[10][1] - bordBassin[0][1])
        


    else:
        xBoat,yBoat = None,None

#-------------------------------------------------

    return xBoat, yBoat

def getPositionCam2(corners2, ids2, frame2):
    """
    corners2 : Corners frame Cam 2
    ids2 : Ids Frame Cam 2
    frame2 : Frame Cam 2
    
    Return:
        xBoat: position en X du bateau
        yBoat: position en Y du bateau
    """
    
    getBordBassin(corners2, ids2,cam2 = True)    
    #------ On recupère la position du bateau -------
    
    i,j = np.where(ids2 == 4)
    k,l = np.where(ids2 == 5)
    
    cornerBoat4 = corners2[i[0]][j[0]]
    cornerBoat5 = corners2[k[0]][l[0]]
    
    x4,y4 = getArucoCenter(cornerBoat4)
    x5,y5 = getArucoCenter(cornerBoat5)
    
    x = (x4 + x5)/2
    y = (y4 + y5)/2
    
    drawBoat(frame2, x, y)
        
#--- On ajuste la position du bateau au bassin ---
    if 1 in bordBassin and 10 in bordBassin and 0 in bordBassin:

    #--- position dans le bassin cam 2 ---
        pos = np.array([[abs(x - bordBassin[1][0])],
                        [abs(y - bordBassin[1][1])]])
    
        pos = getRotationMatrix(getThetaCam2()) @ pos
        
    #--- On ajuste la position du bateau dans le bassin de la camera au bassin en général ---
        pos[0][0] = pos[0][0] + getDistCam2()
        xBoat = pos[0][0] * distAr0Ar1/(bordBassin[str(1)][0] - bordBassin[0][0])
        yBoat = pos[1][0] * distAr0Ar10/(bordBassin[10][1] - bordBassin[0][1])

    else:
        xBoat,yBoat = None,None

#-------------------------------------------------

    return xBoat, yBoat

def getPositionCam3(corners3, ids3, frame3):
    """
    corners3 : Corners frame Cam 3
    ids3 : Ids Frame Cam 3
    frame3 : Frame Cam 3
    
    Return:
        xBoat: position en X du bateau
        yBoat: position en Y du bateau
    """
    
    getBordBassin(corners3, ids3, cam3 = True)    
    #------ On recupère la position du bateau -------
    
    i,j = np.where(ids3 == 4)
    k,l = np.where(ids3 == 5)
    
    cornerBoat4 = corners3[i[0]][j[0]]
    cornerBoat5 = corners3[k[0]][l[0]]
    
    x4,y4 = getArucoCenter(cornerBoat4)
    x5,y5 = getArucoCenter(cornerBoat5)
    
    x = (x4 + x5)/2
    y = (y4 + y5)/2
    
    drawBoat(frame3, x, y)

    
#--- On ajuste la position du bateau au bassin ---
    if 1 in bordBassin and 10 in bordBassin and 0 in bordBassin and 2 in bordBassin:
    #--- in ajuste pour cam3 ---
        pos = np.array([[abs(x - bordBassin[2][0])],
                        [abs(y - bordBassin[2][1])]])
    
    
        pos = getRotationMatrix(getThetaCam3()) @ pos
                
    #--- On ajuste la position du bateau dans le bassin de la camera au bassin en général ---

        pos[0][0] = pos[0][0] + getDistCam3()
        print("-----DIST-----",getDistCam2(), getDistCam3())
        
        xBoat = pos[0][0] * distAr0Ar1/(bordBassin[str(1)][0] - bordBassin[0][0])
        yBoat = pos[1][0] * distAr0Ar10/(bordBassin[10][1] - bordBassin[0][1])

    else:
        xBoat,yBoat = None,None

#-------------------------------------------------

    return xBoat, yBoat






def getCap(corners1, ids1, theta):
    """
    corners1 : Corners Arucos du bateau
    ids1 : Ids Arucos du Bateau
    
    Return:
        angle : cap en radians 
    """
    angle = math.nan

    i1,j1 = np.where(ids1 == 4)
    i2,j2 = np.where(ids1 == 5)

    arucoBoat1 = corners1[i1[0]][j1[0]]
    xAr4, yAr4 = getArucoCenter(arucoBoat1)
    
    arucoBoat2 = corners1[i2[0]][j2[0]]
    xAr5, yAr5 = getArucoCenter(arucoBoat2)
        
    angle = math.atan2( yAr5-yAr4, xAr5-xAr4 ) - theta
    
    return (angle)


def drawPoint(frame,pts):
    """
    pts : point à dessiner (coordonées en M)
    frame : frame sur laquelle il faut dessiner le point
    """
    
#    if 0 in bordBassin and 10 in bordBassin and 1 in bordBassin:
#        xPts = pts[0]*(bordBassin[1][0] - bordBassin[0][0])/distAr0Ar1
#        yPts = pts[1]*(bordBassin[10][1] - bordBassin[0][1])/distAr0Ar10
#
#        pos = np.array([[abs(xPts[0] + bordBassin[0][0])],
#                        [abs(yPts[0] + bordBassin[0][1])]])
#    
#        pos =  np.linalg.inv(getRotationMatrix(getTheta())) @ pos 
# 
#        x = int(pos[0][0])
#        y = int(pos[1][0])
#
#        frame[x-10:x+10,y-10:y+10] = [117,222,255]

def drawLine(frame,a,b):
    """
    a : point a (coordonées en M)
    b : point b (coordonées en M)
    frame : frame sur laquelle il faut dessiner la ligne
    """
    
    
    
    
    
def drawBoat(frame, x,y):
    
    if not x is None and not y is None:
        frame[int(x-10):int(x+10),int(y-10):int(y+10)] = [0,0,255]

def chooseCap(newcameramtx, roi, mtx, dist, oldCap, x):
    """
    mise en place d'un oldCap pour optimiser le temps de compilation
    /!\ Ouvrir et fermer des cap prends bcp de temps /!\
    Ne va laguer que lors du changment de caméra
    renvoie le cap qui a le bateau sur son image
    """

    if oldCap == 1:
        cap1 = cv2.VideoCapture()
        cap1.open(adressCam1)
        
        ret1, frame1 = cap1.read()
        frame1 = undistort(frame1, newcameramtx, roi, mtx, dist)
        corners1, ids1 = detectAruco(frame1)
        cap1.release()
        if 4 in ids1 and 5 in ids1:
            return frame1, corners1, ids1, 1
        
        cap2 = cv2.VideoCapture()
        cap2.open(adressCam2)
        
        ret2, frame2 = cap2.read()
        frame2 = undistort(frame2, newcameramtx, roi, mtx, dist)
        corners2, ids2 = detectAruco(frame2)
        cap2.release()
        if 4 in ids2 and 5 in ids2:
            return frame2, corners2, ids2, 2
        
        cap3 = cv2.VideoCapture()
        cap3.open(adressCam3) 
        
        ret3, frame3 = cap3.read()
        frame3 = undistort(frame3, newcameramtx, roi, mtx, dist)
        corners3, ids3 = detectAruco(frame3)
        cap3.release()
        if 4 in ids3 and 5 in ids3:
            return frame3, corners3, ids3, 3


                
    elif oldCap == 2:

        if x <= bordBassin[str(1)][0] :
            cap1 = cv2.VideoCapture()
            cap1.open(adressCam1)
            
            ret1, frame1 = cap1.read()
            frame1 = undistort(frame1, newcameramtx, roi, mtx, dist)
            corners1, ids1 = detectAruco(frame1)
            cap1.release()
            if 4 in ids1 and 5 in ids1:
                return frame1, corners1, ids1, 1

            
        cap2 = cv2.VideoCapture()
        cap2.open(adressCam2) 
        
        ret2, frame2 = cap2.read()
        frame2 = undistort(frame2, newcameramtx, roi, mtx, dist)
        corners2, ids2 = detectAruco(frame2)
        cap2.release()
        if 4 in ids2 and 5 in ids2:
            return frame2, corners2, ids2, 2
        
        cap3 = cv2.VideoCapture()
        cap3.open(adressCam3) 
        
        ret3, frame3 = cap3.read()
        frame3 = undistort(frame3, newcameramtx, roi, mtx, dist)
        corners3, ids3 = detectAruco(frame3)
        cap3.release()
        if 4 in ids3 and 5 in ids3:
            return frame3, corners3, ids3, 3
        
        #on ne l'atteint jamais ???
        cap1 = cv2.VideoCapture()
        cap1.open(adressCam1)
        
        ret1, frame1 = cap1.read()
        frame1 = undistort(frame1, newcameramtx, roi, mtx, dist)
        corners1, ids1 = detectAruco(frame1)
        cap1.release()
        if 4 in ids1 and 5 in ids1:
            return frame1, corners1, ids1, 1


        

    elif oldCap == 3:
        

        if x <= bordBassin[str(2)][0] :
            cap2 = cv2.VideoCapture()
            cap2.open(adressCam2) 
            
            ret2, frame2 = cap2.read()
            frame2 = undistort(frame2, newcameramtx, roi, mtx, dist)
            corners2, ids2 = detectAruco(frame2)
            cap2.release()
            if 4 in ids2 and 5 in ids2:
                return frame2, corners2, ids2, 2

        cap3 = cv2.VideoCapture()
        cap3.open(adressCam3) 
        
        ret3, frame3 = cap3.read()
        frame3 = undistort(frame3, newcameramtx, roi, mtx, dist)
        corners3, ids3 = detectAruco(frame3)
        cap3.release()
        if 4 in ids3 and 5 in ids3:
            return frame3, corners3, ids3, 3
        
        cap2 = cv2.VideoCapture()
        cap2.open(adressCam2) 
        
        ret2, frame2 = cap2.read()
        frame2 = undistort(frame2, newcameramtx, roi, mtx, dist)
        corners2, ids2 = detectAruco(frame2)
        cap2.release()
        if 4 in ids2 and 5 in ids2:
            return frame2, corners2, ids2, 2
        
        cap1 = cv2.VideoCapture()
        cap1.open(adressCam1)
        
        ret1, frame1 = cap1.read()
        frame1 = undistort(frame1, newcameramtx, roi, mtx, dist)
        corners1, ids1 = detectAruco(frame1)
        cap1.release()
        if 4 in ids1 and 5 in ids1:
            return frame1, corners1, ids1, 1



    
   

    return None,None,None,None

def setCap(number=1):
    global oldCap
    oldCap = number
    
def run_one_step(a, b, newcameramtx, roi, mtx, dist):
    
    if not 'xBoat' in locals():
        xBoat = 0
    frame, corners, ids, number = chooseCap(newcameramtx, roi, mtx, dist, oldCap,xBoat)
    
    if frame is None:
        print("ERROR : No Boat detected")
        print("bordBassin = ", bordBassin)
        return None, None, None
        
        
    if number == 1: #le bateau est sur la cam1
        setCap(1)
        aruco.drawDetectedMarkers(frame, corners, ids)

        theta = getCap(corners, ids, getThetaCam1())
                    
        xBoat, yBoat = getPositionCam1(corners, ids, frame)
        print("-----Webcam 1-----")

        
        
    elif number == 2:#le bateau est sur la cam2
        setCap(2)
        aruco.drawDetectedMarkers(frame, corners, ids)

        theta = getCap(corners, ids, getThetaCam2())
                    
        xBoat, yBoat = getPositionCam2(corners, ids, frame)
        print("-----Webcam 2-----")
        
    elif number == 3: #le bateau est sur la cam3
        setCap(3)
        aruco.drawDetectedMarkers(frame, corners, ids)

        theta = getCap(corners, ids, getThetaCam3())
                    
        xBoat, yBoat = getPositionCam3(corners, ids, frame)
        print("-----Webcam 3-----")
            
    if math.isnan(theta):
        print("ERROR: theta is nan")
        return -1,-1,-1
    
    cv2.imshow("Webcam", frame)

    
    return xBoat, yBoat,theta






#def runTXT(cap1, DIM, K, D, file):
#
#    #------------------- Main ------------------------
#    t0 = time.time()
#    t = 0
#    while t < 2:
#        
#        ret1, frame1 = cap1.read()
#        
#        corners1, ids1 = detectAruco(frame1)
#        
#        if not(ids1 is None) and len(ids1)> 0 and (4 in ids1 and 5 in ids1): #le bateau est sur la cam1 ou la cam2 (ou les deux en meme temps)
#            
#            theta = getCap(corners1, ids1)
#                        
#            xBoat, yBoat = getPositionCam1(corners1, ids1, frame1, K, D)
#            
#            print(xBoat, yBoat,math.degrees(theta))
#            print()
#            
#            if xBoat != None :
#                file.write(str(float(xBoat))+"\t"+str(float(yBoat))+"\t"+str(float(theta))+"\n")
#
#            
#        else: #le bateau n'est sur aucune camera
#            print("ERROR : No boat detected")
#            xBoat, yBoat, theta = None, None, None
#        
#        """
#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
#        """
#        
#        t = time.time() - t0
#
#    
#    return xBoat, yBoat,theta
    


    
#if __name__ == "__main__":
#    
#    cap1, DIM, K, D = init() # initialisation à ne lancer que 1 fois
#    file = open('testfile.txt', 'w')
#    while(True):
#        xBoat, yBoat,theta = run_one_step(cap1, DIM, K, D)# à mettre dans une bouvle while(true)
#        
#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
#    
#    file.close()
#    cap1.release()
#    cv2.destroyAllWindows()

    