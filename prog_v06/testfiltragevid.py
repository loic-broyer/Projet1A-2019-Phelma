# -*- coding: utf-8 -*-
#pour éxecuter : ce placer dans le dossier du fichier
#cd ~/Bureau/projet_1A_phelma_2018-2019/
#python3 ./prog_python_v0.1.py
#utilise opencv4.0.0

import cv2
import numpy as np
import matplotlib.pyplot as plt
import copy
import random
from fonctions_v0_6 import *

nom_fichier="photo_test_1"





############################################################
print("opencv version :", cv2.__version__)
if cv2.__version__ != "4.0.0":
    print("Attention, ce programme a été écrit avec opencv4.0.0")

##########################################################
#Lecture d'une image à partir d'un fichier
img_source = cv2.imread(nom_fichier+".jpg")
assert img_source is not None # vérifie que l'image a bien été chargée

###################################################
#réduit la dimension de l'image



print('dimensions :', img_source.shape)
print('dtype:', img_source.dtype)
#img.shape[0] nb de ligne
#img.shape[1] nb de colonne
#cv.imwrite('sortie.png', img_renverse,[cv.IMWRITE_PNG_COMPRESSION, 0])


def nothing(x):
    pass
cv2.namedWindow('window')
cv2.createTrackbar('iterationDilatation','window',0,8,nothing)
cv2.createTrackbar('iterationOuverture','window',0,8,nothing)
cv2.createTrackbar('aireMin','window',0,10000,nothing)
cv2.createTrackbar('aireMax','window',0,10000,nothing)
cv2.createTrackbar('periMin','window',0,10000,nothing)
cv2.createTrackbar('periMax','window',0,10000,nothing)
cv2.createTrackbar('Hmin','window',0,179,nothing)
cv2.createTrackbar('Hmax','window',0,179,nothing)
cv2.createTrackbar('Smin','window',0,255,nothing)
cv2.createTrackbar('Smax','window',0,255,nothing)
cv2.createTrackbar('Vmin','window',0,255,nothing)
cv2.createTrackbar('Vmax','window',0,255,nothing)


capture = cv2.VideoCapture("vidtest.mp4")
_,frame = capture.read()
ratio = frame.shape[1]/frame.shape[0]

while True:
    nbIterationOuverture = cv2.getTrackbarPos('iterationOuverture','window')
    nbIterationDilatation = cv2.getTrackbarPos('iterationDilatation','window')
    aireMin = cv2.getTrackbarPos('aireMin','window')
    aireMax = cv2.getTrackbarPos('aireMax','window')
    periMin = cv2.getTrackbarPos('periMin','window')
    periMax = cv2.getTrackbarPos('periMax','window')
    Hmin = cv2.getTrackbarPos('Hmin','window')
    Hmax = cv2.getTrackbarPos('Hmax','window')
    Smin = cv2.getTrackbarPos('Smin','window')
    Smax = cv2.getTrackbarPos('Smax','window')
    Vmin = cv2.getTrackbarPos('Vmin','window')
    Vmax = cv2.getTrackbarPos('Vmax','window')
    key = cv2.waitKey(1)

    if key == ord('p'):
        has_frame, frame = capture.read()
        if not has_frame:
            capture = cv2.VideoCapture("vidtest.mp4")
            print("error reading the frame")
            #break
            has_frame, frame = capture.read()

    
    frame = cv2.resize(frame,(int(600*ratio),600))

    blurred = cv2.GaussianBlur(frame,(7,7), 0)
    blurred = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    filtered = threshold(blurred,Hmin,Hmax,Smin,Smax,Vmin,Vmax)
    filtered = cv2.dilate(filtered, None, iterations=nbIterationDilatation)


    #ouverture
    filtered = cv2.erode(filtered, None, iterations=nbIterationOuverture)
    filtered = cv2.dilate(filtered, None, iterations=nbIterationOuverture)

    liste_contour, _ = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    liste_contour = triContourPerimetre(liste_contour,periMin,periMax)
    liste_contour = triContourAire(liste_contour,aireMin,aireMax)
    contourBackground = np.copy(frame)
    DrawContoursDifferentColors(liste_contour,contourBackground)

    cv2.imshow('window',filtered)
    cv2.imshow('contours',contourBackground)
    
    if key == 27:
        break

cv2.destroyAllWindows()
