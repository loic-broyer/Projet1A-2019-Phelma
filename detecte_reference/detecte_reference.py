#Ce programme a pour objectif de détecter deux points caractéristiques du tapis de jeu
#afin dans déduire l'orientation de la caméra.

#pour éxecuter : ce placer dans le dossier du fichier
#et lancer : python3 ./detecte_reference.py

import cv2
import numpy as np
import copy
from math import *
from fonctions_v0_6 import *

nom_fichier="images_et_photos_des_palets/photo_test_1"

#taille en pixels du petit côté des rectangles (une marge de plus ou moins 20% est ensuite appliqué)
Taille_rouge=100
Taille_vert=72
Taille_bleu=62
############################################################
print("opencv version :", cv2.__version__)
if cv2.__version__ != "4.0.0":
    print("Attention, ce programme a été écrit avec opencv4.0.0")

##########################################################
#Lecture d'une image à partir d'un fichier
img = cv2.imread(nom_fichier+".jpg")
assert img is not None # vérifie que l'image a bien été chargée

###################################################
#réduit la dimension des images
img=cv2.resize(img,(640,480))

#################################################
#seuille l'image pour les trois couleurs
img_vert_init = threshold(img,29,74,20)
img_vert = cv2.erode(img_vert_init, None, iterations=1)
img_vert = cv2.dilate(img_vert, None, iterations=1)
img_vert = cv2.Canny(img_vert, 50, 100, 3)
img_vert = cv2.dilate(img_vert, None, iterations=1)
#img_vert = cv2.erode(img_vert, None, iterations=1)
img_bleu_init = threshold(img,81,102,50)
img_bleu = cv2.erode(img_bleu_init, None, iterations=1)
img_bleu = cv2.dilate(img_bleu, None, iterations=1)
img_bleu = cv2.Canny(img_bleu, 50, 100, 3)
img_bleu = cv2.dilate(img_bleu, None, iterations=1)
#img_bleu = cv2.erode(img_bleu, None, iterations=1)
img_rouge_init = threshold(img,177,10,60)
img_rouge = cv2.erode(img_rouge_init, None, iterations=1)
img_rouge = cv2.dilate(img_rouge, None, iterations=1)
img_rouge = cv2.Canny(img_rouge, 50, 100, 3)
img_rouge = cv2.dilate(img_rouge, None, iterations=1)
#img_rouge = cv2.erode(img_rouge, None, iterations=1)

############################################
#affichage
img_etape_1 = np.concatenate((img_vert_init, img_vert), axis=0)
img_temp = np.concatenate((img_bleu_init, img_bleu), axis=0)
img_etape_1 = np.concatenate((img_etape_1, img_temp), axis=1)
img_temp = np.concatenate((img_rouge_init, img_rouge), axis=0)
img_etape_1 = np.concatenate((img_etape_1, img_temp), axis=1)
#affiche de lignes pour séparer les images
img_etape_1 = cv2.line(img_etape_1, (img_vert.shape[1], 0), (img_vert.shape[1], img_vert.shape[0]*2), 255)
img_etape_1 = cv2.line(img_etape_1, (2*img_vert.shape[1], 0), (2*img_vert.shape[1], img_vert.shape[0]*2), 255)
img_etape_1 = cv2.line(img_etape_1, (0, img_vert.shape[0]), (3*img_vert.shape[1], img_vert.shape[0]), 255)
cv2.imshow("etape de seuillage puis de prise des contours", img_etape_1)

#####################################################
#détecte des segments de droite avec la transformée de Hough probabiliste
#Le deuxième argument est la résolution de la distance en pixels
#le troisième est la résolution de l'angle en radians
#le quatrième est le nombre de vote minimum pour qu'une ligne soit prise en compte
#1° = 0.017rad
#La fonction HoughLines renvoie une liste de droites données en coordonnées polaires (rho, theta)
lignes_bleu = cv2.HoughLinesP(img_bleu, 1, 0.04, int(Taille_bleu*0.4), minLineLength=Taille_bleu*0.6, maxLineGap=Taille_bleu/2)
lignes_vert = cv2.HoughLinesP(img_vert, 1, 0.04, int(Taille_vert*0.4), minLineLength=Taille_vert*0.6, maxLineGap=Taille_vert/2)
lignes_rouge = cv2.HoughLinesP(img_rouge, 1, 0.04, int(Taille_rouge*0.4), minLineLength=Taille_rouge*0.6, maxLineGap=Taille_rouge/2)

###########################################################
#affichage des lignes détectées
def affiche_ligne(img, liste_lignes, couleur):
    for i in range(len(liste_lignes)):
        if liste_lignes[i][0][1]==liste_lignes[i][0][3] or liste_lignes[i][0][0]==liste_lignes[i][0][2]:
            cv2.line(img, (liste_lignes[i][0][0], liste_lignes[i][0][1]), (liste_lignes[i][0][2], liste_lignes[i][0][3]), (0,0,0))
        else:
            cv2.line(img, (liste_lignes[i][0][0], liste_lignes[i][0][1]), (liste_lignes[i][0][2], liste_lignes[i][0][3]), couleur)
    return img

def affiche_ligne_2(img, liste_lignes_vert, liste_lignes_bleu, liste_lignes_rouge):
    img = cv2.putText(img, str(len(liste_lignes_vert))+" lignes vertes detectees", (8,20), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0))
    img = cv2.putText(img, str(len(liste_lignes_bleu))+" lignes bleu detectees", (8,40), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0))
    img = cv2.putText(img, str(len(liste_lignes_rouge))+" lignes rouges detectees", (8,60), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0))
    img=affiche_ligne(img, liste_lignes_vert, (0,255,0))
    img=affiche_ligne(img, liste_lignes_bleu, (255,0,0))
    img=affiche_ligne(img, liste_lignes_rouge, (0,0,255))
    return img

def verifie_occurence_ligne(liste_1, liste_2, tol_p=10):
    """Cette fonction prend en paramètre deux listes de segments"""
    liste_sortie=[]
    for i in range(len(liste_1)):
        for k in range(len(liste_2)):
            if liste_1[i][0][1]==liste_1[i][0][3] or liste_1[i][0][0]==liste_1[i][0][2]:
                continue
            if liste_2[k][0][1]==liste_2[k][0][3] or liste_2[k][0][0]==liste_2[k][0][2]:
                continue#on enleve tout de suite les segments verticaux ou horizontaux
            teta1=atan((liste_1[i][0][0]-liste_1[i][0][2])/(liste_1[i][0][1]-liste_1[i][0][3]))
            teta2=atan((liste_2[k][0][0]-liste_2[k][0][2])/(liste_2[k][0][1]-liste_2[k][0][3]))
            if abs(teta1-teta2)>0.1:
                continue
            if (abs(liste_1[i][0][0]-liste_2[k][0][0])<=tol_p and abs(liste_1[i][0][1]-liste_2[k][0][1])<=tol_p):
                liste_sortie.append([[liste_1[i][0][2], liste_1[i][0][3], liste_2[k][0][2], liste_2[k][0][3]]])
            elif abs(liste_1[i][0][2]-liste_2[k][0][2])<=tol_p and abs(liste_1[i][0][3]-liste_2[k][0][3])<=tol_p:
                liste_sortie.append([[liste_1[i][0][0], liste_1[i][0][1], liste_2[k][0][0], liste_2[k][0][1]]])
            elif abs(liste_1[i][0][0]-liste_2[k][0][2])<=tol_p and abs(liste_1[i][0][1]-liste_2[k][0][3])<=tol_p:
                liste_sortie.append([[liste_1[i][0][2], liste_1[i][0][3], liste_2[k][0][0], liste_2[k][0][1]]])
            elif abs(liste_1[i][0][2]-liste_2[k][0][0])<=tol_p and abs(liste_1[i][0][3]-liste_2[k][0][1])<=tol_p:
                liste_sortie.append([[liste_1[i][0][0], liste_1[i][0][1], liste_2[k][0][2], liste_2[k][0][3]]])
    return liste_sortie
img2=copy.deepcopy(img)
img3=np.full((img.shape[0], img.shape[1], 3), 250, np.uint8)
cv2.imshow("Lignes de chaque couleur detectees", affiche_ligne_2(img, lignes_vert, lignes_bleu, lignes_rouge))

lignes_sortie1=verifie_occurence_ligne(lignes_vert, lignes_bleu)
lignes_sortie=verifie_occurence_ligne(lignes_sortie1, lignes_rouge)

img2 = cv2.putText(img2, str(len(lignes_sortie))+" lignes detectees", (8,20), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0))
img3 = cv2.putText(img3, str(len(lignes_sortie))+" lignes detectees", (8,20), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0))
cv2.imshow("Lignes finalement detectees", affiche_ligne(img2, lignes_sortie, (0,0,0)))
cv2.imshow("Lignes finalement detectees2", affiche_ligne(img3, lignes_sortie, (0,0,0)))
cv2.waitKey(0)
#print(lignes_sortie)
#lignes=verifie_occurence_ligne(lignes_rouge, verifie_occurence_ligne(lignes_vert, lignes_bleu))
#cv2.imshow("Lignes detectees", affiche_ligne(img, lignes))
