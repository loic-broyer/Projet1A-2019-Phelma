import cv2
import numpy as np

def seuillageCouleur(img,Hmin=0,Hmax=179,Smin=0,Smax=255,Vmin=0,Vmax=255):
    HSVImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return cv2.inRange(HSVImg, np.array([Hmin,Smin,Vmin]), np.array([Hmax,Smax,Vmax]))
