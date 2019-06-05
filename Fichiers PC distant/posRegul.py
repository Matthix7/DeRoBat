import cv2
import calibrate_fisheye as calibration
import numpy as np
import cv2.aruco as aruco
import cv2.fisheye as fisheye
import math
import time
from threading import Thread
from regulation import getCommande


bordBassin = dict() #pour la position des aruco sur le bord

############# #Check adresse avec IPUtility #################################
#############################################################################
#adressCam = 'http://root:1234@169.254.236.203/mjpg/video.mjpg'   #Pour Quentin
adressCam = 'http://root:1234@169.254.236.203/mjpg/video.mjpg'   #Pour Matthieu
#############################################################################
#############################################################################

class Cam(Thread):
    """Acquisition d'images et extraction de la pose du bateau."""
    
    def __init__(self):
        Thread.__init__(self)
        self.is_dead = "alive"
                
        self.message = str((-1,-1,-1,0,0)) 
        self.commande = (0,0)
        
        

    def getMessage(self):
        return self.message      # (xBoat, yBoat, heading, servoCommand, motorCommand)
    
    
    
    def isDead(self):
        return self.is_dead
    
    
    
    def run(self):
        print('Calibration running...')
        cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)

        cap1 = cv2.VideoCapture()
        cap1.open(adressCam) 
        
        DIM, K, D = calibration.defineCalibrationParameters()
        
        neutreServo, neutreMoteur = 1090, 2000
        commandes = np.array([[neutreServo], [neutreMoteur]])
        
        xTarget = 9
        yTarget = 9
        vTarget = 0.5 
        
        a = np.array([[0], [0]])    
        b = np.array([[xTarget], [yTarget]])
        
        
        print('Acquisition running.')
        while(cap1.isOpened()):
            
            xBoat, yBoat,theta = run_one_step(cap1, DIM, K, D)
            
            
# =============================================================================
#             Bloc régulation
# =============================================================================
            
            posServo = commandes[0,0] - neutreServo  #A changer
            posMoteur = commandes[1,0] - neutreMoteur #A changer
            
            if not xBoat is None: #si les bateau n'est pas vu sur la camera -> soustraction sur un None = Bug
            
                X = np.array([[xBoat], [yBoat], [theta], [posServo], [posMoteur]])
                commandes = getCommande(X, a, b, vTarget, commandes)  #Appel module regulation
                    
                if commandes[1,0] >= 0:
                    self.commande = (175*commandes[0,0]+neutreServo, (238*commandes[1,0]+27) + 2000)
                if commandes[1,0] < 0:
                    self.commande = (175*commandes[0,0]+neutreServo, (390*abs(commandes[1,0])+31) + 3000)
            
            
# =============================================================================
#             Expédition des utiles en aval
# =============================================================================
            
            if xBoat != None and yBoat != None:
                print("X = ", xBoat * 4/2350, "Y = ", yBoat*3/2000, "theta =", theta)                
                self.message = str( (xBoat * 4/2350, yBoat*3/2000, theta) + self.commande)
            
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
        cap1.release()
        cv2.destroyAllWindows()





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







def undistorted(corner,K,D):
    """
    corner : position du code Aruco dans l'image
    
    Return:
        Point central de l'Aruco après calibration
    """
    
    input_points = np.zeros([1,1,2])
            
    x,y = getArucoCenter(corner)
    
    input_points[0,0,0] = x
    input_points[0,0,1] = y
    
    undistorted = fisheye.undistortPoints(input_points,K,D, R=None, P=K)
    
    return undistorted.reshape(1,2)[0,0], undistorted.reshape(1,2)[0,1]
    





def getPosition(corners1, ids1, frame1, K, D):
    
    """
    corners1 : Corners frame Cam 1
    ids1 : Ids Frame Cam 1
    frame1 : Frame Cam 1
    
    Return:
        xBoat: position en X du bateau
        yBoat: position en Y du bateau (il est inversé ?)
    """
    
    #------ On recupère le bords du bassin ---------
        
    if len(ids1) > 0:
        for id in ids1:
            if id != 4 and id != 5:
                
                i,j = np.where(ids1 == id)
                
                cornerBassin = corners1[i[0]][j[0]]
                
                xBassin, yBassin = undistorted(cornerBassin, K,D)
                
                #xBassin, yBassin = getArucoCenter(cornerBassin)
                            
                bordBassin[id[0]] = xBassin,yBassin
       
    #------------------------------------------------
    
    #------ On recupère la position du bateau -------
    
    i,j = np.where(ids1 == 4)
    k,l = np.where(ids1 == 5)
    
    cornerBoat4 = corners1[i[0]][j[0]]
    cornerBoat5 = corners1[k[0]][l[0]]
    
    #x4,y4 = getArucoCenter(cornerBoat4)

    x4, y4 = undistorted(cornerBoat4,K,D)
    x5, y5 = undistorted(cornerBoat5,K,D)

    #x5,y5 = getArucoCenter(cornerBoat5)
    
    x = (x4 + x5)/2
    y = (y4 + y5)/2
    
#--- On ajuste la position du bateau au bassin ---
    if len(bordBassin) > 0:
        
        xBoat = abs(x - bordBassin[0][0])
        yBoat = abs(y - bordBassin[0][1])
        """
        x4,y4 = getArucoCenter(cornerBoat4)
        x5,y5 = getArucoCenter(cornerBoat5)
        xBoat = (x4 + x5)/2
        yBoat = (y4 + y5)/2
        """

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
    i1,j1 = np.where(ids1 == 4)
    i2,j2 = np.where(ids1 == 5)

    arucoBoat1 = corners1[i1[0]][j1[0]]
    xAr4, yAr4 = getArucoCenter(arucoBoat1)
    
    arucoBoat2 = corners1[i2[0]][j2[0]]  
    xAr5, yAr5 = getArucoCenter(arucoBoat2)
    
    angle = math.atan2( yAr5-yAr4, xAr5-xAr4 )
    return (angle)


    


def run_one_step(cap1, DIM, K, D):
    
    ret1, frame1 = cap1.read()
    if ret1:
        cv2.imshow("Webcam", frame1)
        
        corners1, ids1 = detectAruco(frame1)
        
        if not(ids1 is None) and len(ids1)> 0 and (4 in ids1 and 5 in ids1): #le bateau est sur la cam1 ou la cam2 (ou les deux en meme temps)
            
            theta = getCap(corners1, ids1)
                        
            xBoat, yBoat = getPosition(corners1, ids1, frame1, K, D)
            
            
            
        else: #le bateau n'est sur aucune camera
            print("ERROR : No boat detected")
            xBoat, yBoat, theta = None, None, None
        
    else: #le bateau n'est sur aucune camera
            print("ERROR : No image")
            xBoat, yBoat, theta = None, None, None
    
#    aruco.drawDetectedMarkers(frame1, corners1, ids1)
    
    return xBoat, yBoat,theta






def runTXT(cap1, DIM, K, D, file):

    #------------------- Main ------------------------
    t0 = time.time()
    t = 0
    while t < 2:
        
        ret1, frame1 = cap1.read()
        
        corners1, ids1 = detectAruco(frame1)
        
        if not(ids1 is None) and len(ids1)> 0 and (4 in ids1 and 5 in ids1): #le bateau est sur la cam1 ou la cam2 (ou les deux en meme temps)
            
            theta = getCap(corners1, ids1)
                        
            xBoat, yBoat = getPosition(corners1, ids1, frame1, K, D)
            
            print(xBoat, yBoat,math.degrees(theta))
            print()
            
            if xBoat != None :
                file.write(str(float(xBoat))+"\t"+str(float(yBoat))+"\t"+str(float(theta))+"\n")

            
        else: #le bateau n'est sur aucune camera
            print("ERROR : No boat detected")
            xBoat, yBoat, theta = None, None, None
        
        """
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        """
        
        t = time.time() - t0

    
    return xBoat, yBoat,theta
    


    
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

    