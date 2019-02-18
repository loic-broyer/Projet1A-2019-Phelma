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
import seuillagecouleur as sc

delta_x_min = 15#en nombre de pixels
delta_x_max = 40
delta_y_min = delta_x_min
delta_y_max = delta_x_max
perimetre_min = 3*delta_x_min
perimetre_max = 3*delta_x_max
aire_min = delta_x_min**2
taille_noyau_lissage=3#paramètre de la fonction Canny
nom_fichier="photo_test_1"

def tri_contour_taille(liste_contour):
    #Tri des contours suivant leur périmètre et leur taille en x et en y:
    liste_contour_tries=[]
    for i in range(len(liste_contour)):
        if len(liste_contour[i])>=perimetre_min and len(liste_contour[i])<=perimetre_max:
            print("contour n° "+str(i)+" avec ",len(liste_contour[i])," pixels")
            max_x=liste_contour[i][0][0][0]
            max_y=liste_contour[i][0][0][1]
            min_x=liste_contour[i][0][0][0]
            min_y=liste_contour[i][0][0][1]
            for j in range(1,len(liste_contour[i])):
                if liste_contour[i][j][0][0]>max_x:
                    max_x=liste_contour[i][j][0][0]
                elif liste_contour[i][j][0][0]<min_x:
                    min_x=liste_contour[i][j][0][0]
                if liste_contour[i][j][0][1]>max_y:
                    max_y=liste_contour[i][j][0][1]
                elif liste_contour[i][j][0][1]<min_y:
                    min_y=liste_contour[i][j][0][1]
            delta_x = max_x - min_x
            delta_y = max_y - min_y
            if delta_x >= delta_x_min and delta_x <= delta_x_max and delta_y >= delta_y_min and delta_y <= delta_y_max:
                print("contour n° "+str(i)+"x E", min_x, max_x, "y E", min_y, max_y)
                liste_contour_tries.append(liste_contour[i])
    return liste_contour_tries

def tri_contour_aire(liste_contour):
    #Tri des contours
    #supprime les contours qui ont une aire trop petite
    liste_contour_tries=[]
    for i in range(len(liste_contour)):
        if cv2.contourArea(liste_contour[i]) >= aire_min:
            liste_contour_tries.append(liste_contour[i])
    return liste_contour_tries

def affiche_contour_couleurs_differentes(liste_contour, nb_pixel_x, nb_pixel_y):
    #prend en paramètre les dimensions de l'image dont on a pris les contours
    #affiche tous les contours avec une couleur différente par contour
    img_tous_les_contours = np.full((nb_pixel_x, nb_pixel_y, 3), 0, np.uint8)
    for i in range(len(liste_contour)):
        a=(15*i)%256
        b=(22*i)%256
        c=(9*i)%256
        if a+b+c<80:#pour ne pas avoir de contour trop sombre
            a+=30
            b+=30
            c+=30
        couleur=[a,b,c]
        for j in range(len(liste_contour[i])):
            x=liste_contour[i][j][0][1]
            y=liste_contour[i][j][0][0]
            img_tous_les_contours[x][y]=couleur
    cv2.imshow('tous les contours', img_tous_les_contours)
    cv2.imwrite("contours.png", img_tous_les_contours)
    return


def detecte_palets(img, couleur="vert"):
    #retourne une liste contenant les centres de tous les palets de couleur demandé
    assert couleur in ["rouge", "vert", "bleu"]

    ##########################################################
    #Prise des contours de l'image
    if couleur == "vert":
        img = sc.seuillageCouleur(img,29,74,20)
    elif couleur == "bleu":
        img = sc.seuillageCouleur(img,81,102,50)
    else:
        img = sc.seuillageCouleur(img,81,102,50)

    cv2.imshow('image seuillée pour le '+couleur, img)
    img_canny = cv2.Canny(img, 50, 100, taille_noyau_lissage)
    cv2.imshow('image passée au filtre de Canny pour le '+couleur, img_canny)
    cv2.waitKey(0)

    #########################################################
    #Regroupement des pixels détectés par contour
    liste_contour, _ = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    affiche_contour_couleurs_differentes(liste_contour, img.shape[0], img.shape[1])
    cv2.waitKey(0)

    #########################################################
    #Tri des contours
    liste_contour_tries=tri_contour_aire(tri_contour_taille(liste_contour))

    ###########################################################
    #affichage des contours triés
    img_contours = np.full((img.shape[0], img.shape[1]), 0, np.uint8)
    for i in range(len(liste_contour_tries)):
        for j in range(len(liste_contour_tries[i])):
            x=liste_contour_tries[i][j][0][1]
            y=liste_contour_tries[i][j][0][0]
            #img[x][y]=[255,255,255]-img[x][y]
            img_contours[x][y]=255
#    cv2.imshow('image initiale + contours triés', img)
    cv2.imshow('image initiale + contours triés', img_contours)
    cv2.waitKey(0)

    ##########################################################
    #Calcule le centre des contours
    liste_centre_palets=np.full((len(liste_contour_tries), 2), 0, np.uint32)
    for i in range(len(liste_contour_tries)):
        centre_x=0
        centre_y=0
        for j in range(len(liste_contour_tries[i])):
            centre_x += liste_contour_tries[i][j][0][1]
            centre_y += liste_contour_tries[i][j][0][0]
        liste_centre_palets[i][1] = centre_x/len(liste_contour_tries[i])
        liste_centre_palets[i][0] = centre_y/len(liste_contour_tries[i])
        print(centre_x,len(liste_contour_tries[i]),liste_centre_palets[i][1])
        print(centre_y,len(liste_contour_tries[i]),liste_centre_palets[i][0])

    #rajoute le centre sur l'image des contours
    for i in range(len(liste_centre_palets)):
        img_contours[liste_centre_palets[i][1]][liste_centre_palets[i][0]]=255

    cv2.imshow('contour triés', img_contours)
    cv2.waitKey(0)

    ###########################################################
    """
    cv2.imwrite(nom_fichier+"_canny.png", img_canny)
    cv2.imwrite(nom_fichier+"_gris.png", img)
    cv2.imwrite(nom_fichier+"_contours_seuls.png", img_contours)
    #cv2.imwrite(nom_fichier+"_image_et_contours.png", img_couleur)
    """

    print("initialement :",len(liste_contour),"contours")
    print(len(liste_contour_tries),"contours sélectionnés")
    return liste_centre_palets




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
