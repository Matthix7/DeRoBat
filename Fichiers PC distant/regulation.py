# -*- coding: utf-8 -*-
"""
Created on Fri May 31 18:20:05 2019

@author: catam
"""

from numpy import array, cos, sin, pi, ones, vstack
from math import atan2
import matplotlib.pyplot as plt
from numpy.linalg import norm

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
xTarget = 3
yTarget = 3
vTarget = 0.5

w = array([[xTarget], [yTarget], [vTarget]])
# =============================================================================

# =============================================================================
# Contraintes
angle_max = pi/6
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
    x, y, cap, servo, v = X[0], X[1], X[2], X[3], X[4]
    xTarget, yTarget, vTarget = w[0], w[1], w[2]
    
    capTarget = atan2(yTarget - y, xTarget - x)
    erreurCap = -sawtooth(capTarget - cap)
    derreur = -v*sin(servo) 
    
    rudderCommand = erreurCap + 2*derreur
    
    motorCommand = vTarget - v
    
    return array([[rudderCommand], [motorCommand]])
    
  
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

a = array([[-1], [-1]])
b = array([[9], [4]])
w = array([[b[0]], [b[1]], [vTarget]])

X = array([[a[0,0]], [a[0,0]], [0], [0.5], [0]])
consignes = array([[0.], [0.]])


while ((b-a).T @ (b-X[:2])) / (norm(b-a)*norm(b-X[:2])) >= 0:

    plt.cla()
    plt.xlim((-3, 10))
    plt.ylim((-3, 10))
    plt.gca().set_aspect('equal', adjustable='box')
    
    plt.plot([a[0], b[0]], [a[1], b[1]])
    
    dU = dCommande(X, w)
    consignes += dt*dU
    consignes[0, 0] = max(-angle_max, min(consignes[0] , angle_max))
    
    X = newX(X, consignes)
     
    
    
    draw_boat(X)
     
    plt.pause(dt)
    
    
a = b
b = array([[-1], [9]])
w = array([[b[0]], [b[1]], [vTarget]])



while ((b-a).T @ (b-X[:2])) / (norm(b-a)*norm(b-X[:2])) >= 0:

    plt.cla()
    plt.xlim((-3, 10))
    plt.ylim((-3, 10))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.plot([a[0], b[0]], [a[1], b[1]])
    
    
    dU = dCommande(X, w)
    consignes += dt*dU
    consignes[0, 0] = max(-angle_max, min(consignes[0] , angle_max))
    
    X = newX(X, consignes)
     
    
    
    draw_boat(X)
     
    plt.pause(dt)








