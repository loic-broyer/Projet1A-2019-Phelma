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
ratio = img_source.shape[1]/img_source.shape[0]
img_resized = cv2.resize(img_source,(int(600*ratio),600))
print(img_resized.shape)
#blur =

print('dimensions :', img_source.shape)
print('dtype:', img_source.dtype)
#img.shape[0] nb de ligne
#img.shape[1] nb de colonne
#cv.imwrite('sortie.png', img_renverse,[cv.IMWRITE_PNG_COMPRESSION, 0])
#cv2.imshow('image resized', img_resized)
#key = cv2.waitKey(2000)
blurred = cv2.GaussianBlur(img_resized,(7,7), 0)
#cv2.imshow('img',blurred)
thresholded = threshold(blurred,32,41,41,255)
#cv2.imshow('img',thresholded)


def nothing(x):
    pass
cv2.namedWindow('window')
cv2.createTrackbar('iteration','window',1,8,nothing)



while True:
    nbIteration = cv2.getTrackbarPos('iteration','window')
    #ouverture
    filtered = cv2.erode(thresholded, None, iterations=nbIteration)
    filtered = cv2.dilate(filtered, None, iterations=nbIteration)
    cv2.imshow('window',filtered)
    key = cv2.waitKey(3)
    if key == 27:
        break

cv2.destroyAllWindows()
