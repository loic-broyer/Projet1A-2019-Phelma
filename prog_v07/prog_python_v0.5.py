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
from fonctions_v0_5 import *

nom_fichier="photo_test_1"





############################################################
print("opencv version :", cv2.__version__)
if cv2.__version__ != "4.0.0":
    print("Attention, ce programme a été écrit avec opencv4.0.0")

##########################################################
#Lecture d'une image à partir d'un fichier
img_couleur_grande = cv2.imread(nom_fichier+".jpg")
assert img_couleur_grande is not None # vérifie que l'image a bien été chargée

###################################################
#réduit la dimension de l'image
img_couleur = cv2.resize(img_couleur_grande,(img_couleur_grande.shape[1]//6,img_couleur_grande.shape[0]//6))

print('dimensions :', img_couleur.shape)
print('dtype:', img_couleur.dtype)
#img.shape[0] nb de ligne
#img.shape[1] nb de colonne
#cv.imwrite('sortie.png', img_renverse,[cv.IMWRITE_PNG_COMPRESSION, 0])
cv2.imshow('image initiale', img_couleur)

liste_centre_palets_vert=detecte_palets(img_couleur, "vert")
print(liste_centre_palets_vert)
