# -*- coding: utf-8 -*-

# =============================================================================
# REGULATION SUIVI DE LIGNE
# =============================================================================

"""
Created on Fri May 31 18:20:05 2019

@author: catam
"""

from numpy import array, cos, sin, pi, ones, hstack, vstack, linspace, arange, arctan
from math import atan2
import matplotlib.pyplot as plt
from numpy.linalg import norm, det

# =============================================================================
#              Vecteur d'état                    
#  X = (x, y, cap, angle_safran, vitesse) 
# =============================================================================

# =============================================================================
# Pas temporel 
dt = 0.5
# =============================================================================


# =============================================================================
# Consignes
vTarget = 0.5

# =============================================================================

# =============================================================================
# Contraintes
angle_max = pi/12
vmax = 1
# =============================================================================

# =============================================================================
# Fonction d'évolution
# On considère que les actions sur le moteur et le safran sont immédiates.
# =============================================================================

def newX(X, u):
    X = X.flatten()
    u = u.flatten()
    x, y, cap, servo, v = X[0], X[1], X[2], X[3], X[4]
    
    newX = array([[   x + dt * v * cos(cap)   ],
                  [   y + dt * v * sin(cap)   ],
                  [ cap - dt * v * sin(servo) ],
                  [           u[0]            ],
                  [           u[1]            ]])
    
    return newX



# =============================================================================
# Obtention des dérivées des commandes pour suivi de cap et vitesse.
# =============================================================================

def dCommande(X, w):
    X = X.flatten()
    w = w.flatten()
    cap, servo, v = X[2], X[3], X[4]
    capTarget, vTarget = w[0], w[1]
    
    erreurCap = -sawtooth(capTarget - cap)
    derreur = -v*sin(servo) 
    
    rudderCommand = erreurCap + 2*derreur
    
    motorCommand = vTarget - v
    
    return array([[rudderCommand], [motorCommand]])
    


# =============================================================================
# Elaboration de la consigne
# =============================================================================

def getConsignes(X, a, b, vTarget):
    
    d = b-a
    e = det( hstack(( X[:2]-a, d/norm(d) )) )
    capTarget = atan2(d[1], d[0]) + 0.5*arctan(e)
    
    
    return array([[capTarget], [vTarget]])
    
    
    
# =============================================================================
# Fonction à appeler depuis le module PosRegul
# =============================================================================

def getCommande(X, a, b, vTarget, commande_precedente):
    
    consigne = getConsignes(X, a, b, vTarget)
    dU = dCommande(X, consigne)
    commande = commande_precedente + dt*dU
    commande[0, 0] = max(-angle_max, min(commande[0,0] , angle_max))
    commande[1, 0] = max(-vmax, min(commande[1,0] , vmax))
    
    return commande


# =============================================================================
# Fonctions utiles    
# =============================================================================

def sawtooth(x):
    return (x+pi)%(2*pi)-pi


# =============================================================================
# Fonctions d'affichage. 
# =============================================================================
def plot2D(M,col='black',w=1):
    plt.plot(M[0, :], M[1, :], col, linewidth = w)

def move_motif(M,x,y,θ):
    M1=ones((1,len(M[1,:])))
    M2=vstack((M, M1))
    R = array([[cos(θ),-sin(θ),x], [sin(θ),cos(θ),y]])
    return(R @ M2)
    
def draw_boat(x, size = 0.1):
    x=x.flatten()
    θ=x[2]
    δr = x[3]
    hull=array([[size,0,0], [0,size,0], [0,0,1]])@array([[-1,5,7,7,5,-1,-1,-1],[-2,-2,-1,1,2,2,-2,-2],[1,1,1,1,1,1,1,1]])
    rudder=array([[size,0,0], [0,size,0], [0,0,1]])@array([[-1,1],[0,0],[1,1]])
    R=array([[cos(θ),-sin(θ),x[0]],[sin(θ),cos(θ),x[1]],[0,0,1]])
    Rr=array([[cos(δr),-sin(δr),-1*size],[sin(δr),cos(δr),0],[0,0,1]])
    plot2D(R@hull,'black');
    plot2D(R@Rr@rudder,'red',2);






plt.figure()

# =============================================================================
# Configuration initiale
# =============================================================================
X = array([[0.5], [5], [0], [0.5], [0]])
commandes = array([[0.], [0.]])


Waypoints = [[10, 5, -5, -10],
             [-10, 10, -10, 10]]

for k in range(len(Waypoints[0])-1):
    a = array([[Waypoints[0][k]], [Waypoints[1][k]]])
    b = array([[Waypoints[0][k+1]], [Waypoints[1][k+1]]])
    
    while ((b-a).T @ (b-X[:2])) / (norm(b-a)*norm(b-X[:2])) >= 0:
            
           
        plt.cla()
        plt.xlim((-15, 15))
        plt.ylim((-15, 15))
        plt.gca().set_aspect('equal', adjustable='box')
        
        commandes = getCommande(X, a, b, vTarget, commandes)
        
        X = newX(X, commandes)
         
        
        plt.plot([a[0], b[0]], [a[1], b[1]])
        
        draw_boat(X)
         
        plt.pause(dt)
    







