#pour éxecuter : ce placer dans le dossier du fichier
#python3 ./detecte_reference_avec_hough_classique.py

import cv2
import numpy as np
import matplotlib.pyplot as plt
import copy
from math import *
import time
from fonctions_v0_6 import *

nom_fichier = "videos_test/video_5.mp4"

############################################################
print("opencv version :", cv2.__version__)
if cv2.__version__ != "4.0.0":
    print("Attention, ce programme a été écrit avec opencv4.0.0")

"""
##########################################################
#Lecture d'une image à partir d'un fichier
img_init = cv2.imread(nom_fichier+".jpg")
assert img_init is not None # vérifie que l'image a bien été chargée
"""

#########################################################
#Ouverture du fichier vidéo
capture = cv2.VideoCapture(nom_fichier)


cv2.namedWindow("Hough")
cv2.namedWindow("seuillee et droite")
cv2.namedWindow("Hough 2")
nb_vote_min = 300
reso_angle = 2
pause = 900
saturation = 40
luminosite = 40
nb_dilatation = 1
cv2.createTrackbar('nb vote min',"Hough",nb_vote_min,350,lambda x: None)
cv2.createTrackbar('resolution en millieme de radian',"Hough",reso_angle,50,lambda x: None)
cv2.createTrackbar("pause entre chaque image en ms","Hough",pause,1000,lambda x: None)
cv2.createTrackbar("saturation","seuillee et droite",saturation,255,lambda x: None)
cv2.createTrackbar("luminosite","seuillee et droite",luminosite,255,lambda x: None)
cv2.createTrackbar("nb dilatation-erosion","seuillee et droite",nb_dilatation,4,lambda x: None)

nb_vote_min_2 = 90
angle_min = int(pi*1000/2)
angle_max = int(pi*1000)-200
reso_angle_2 = 4
cv2.createTrackbar('nb vote min 2',"Hough 2",nb_vote_min_2,200,lambda x: None)
cv2.createTrackbar('angle min en millieme de radian',"Hough 2",angle_min,int(pi*1000),lambda x: None)
cv2.createTrackbar('angle max en millieme de radian',"Hough 2",angle_max,int(pi*1000),lambda x: None)
cv2.createTrackbar('resolution en millieme de radian 2',"Hough 2",reso_angle_2,50,lambda x: None)
n_image=0

while(cv2.waitKey(pause)!=27):
    n_image+=1
    has_frame, img_init = capture.read()
    #capture.release()
    if not has_frame:
        capture.release()
        capture = cv2.VideoCapture(nom_fichier)
        has_frame, img_init = capture.read()
        n_image=1
        if not has_frame:
            print("error reading the frame")
            break

    nb_vote_min = cv2.getTrackbarPos('nb vote min',"Hough")
    reso_angle = cv2.getTrackbarPos('resolution en millieme de radian',"Hough")
    pause = cv2.getTrackbarPos("pause entre chaque image en ms","Hough")
    saturation = cv2.getTrackbarPos("saturation","seuillee et droite")
    luminosite = cv2.getTrackbarPos("luminosite","seuillee et droite")
    nb_dilatation = cv2.getTrackbarPos("nb dilatation-erosion","seuillee et droite")

    nb_vote_min_2 = cv2.getTrackbarPos('nb vote min 2',"Hough 2")
    angle_min = cv2.getTrackbarPos('angle min en millieme de radian',"Hough 2")
    angle_max = cv2.getTrackbarPos('angle max en millieme de radian',"Hough 2")
    reso_angle_2 = cv2.getTrackbarPos('resolution en millieme de radian 2',"Hough 2")
    ###################################################
    #réduction de la dimension de l'image
    img_init=cv2.resize(img_init,(1280, 720))

    #img_init = cv2.flip(img_init, 1)
    #cv2.imshow("e", img_init)
    #cv2.waitKey(0)

    #debruitage
    #img_debruite = cv2.GaussianBlur(img_init, (3, 3), 0)
    #cv2.imshow("debruite", img_debruite)
    #img_init = img_debruite

    img = img_init[:,0:img_init.shape[1]//2]#on ne traite que la partie gauche de l'image
    img_canny = cv2.Canny(img, 100, 50, 3)
    #cv2.imshow("Canny", img_canny)

    #####################################################
    #détecte des droites avec la transformée de Hough
    #Le deuxième argument est la résolution de la distance en pixels
    #le troisième est la résolution de l'angle en radians
    #le quatrième est le nombre de vote minimum pour qu'une ligne soit prise en compte
    #1° = 0.017rad
    #La fonction HoughLines renvoie une liste de droites données en coordonnées polaires (rho, theta)
    debut=time.clock()
    lignes = cv2.HoughLines(img_canny, 1, reso_angle/1000, nb_vote_min, min_theta=0.2, max_theta=pi/2-0.2)
    fin=time.clock()
    if type(lignes)==type(None):
        lignes=[]

    ###########################################################
    #affichage des lignes détectées
    def affiche_ligne(img, liste_lignes, couleur=128):
        """affiche des lignes passées en coordonnées polaires"""
        img = cv2.putText(img, str(len(liste_lignes))+" lignes detectees", (8,20), cv2.FONT_HERSHEY_PLAIN, 1, 255)
        for i in range(len(liste_lignes)):
            rho = liste_lignes[i][0][0]
            theta = liste_lignes[i][0][1]
            a = cos(theta)
            b = sin(theta)
            #print("rho : ", liste_lignes[i][0][0],"theta : ", liste_lignes[i][0][1],(int(liste_lignes[i][0][0]/cos(liste_lignes[i][0][1])), 0), (0, int(liste_lignes[i][0][0]/cos(pi/2 - liste_lignes[i][0][1]))))
            #prog perso : img = cv2.line(img, (int(rho/a), 0), (0, int(rho/b)), couleur)
            #source de la ligne suivante : https://docs.opencv.org/3.4.0/d9/db0/tutorial_hough_lines.html
            img = cv2.line(img, (int(a*rho - 1000*b), int(b*rho + 1000*a)), (int(a*rho+1000*b), int(b*rho-1000*a)), couleur)
        return img

    ####################################################
    #Recherche la ligne à garder
    lignes_top=[]
    rho_max = lignes[:,0,0].max()
    for i in range(len(lignes)):
        if lignes[i][0][0]==rho_max:
            lignes_top.append(lignes[i])


    #img_canny = cv2.putText(img_canny, "execute en "+str(fin-debut)+" s", (8,40), cv2.FONT_HERSHEY_PLAIN, 1, 255)
    #img_canny = cv2.putText(img_canny, "image numero "+str(n_image), (8,60), cv2.FONT_HERSHEY_PLAIN, 1, 255)
    img_hough = cv2.cvtColor(img_canny, cv2.COLOR_GRAY2BGR)
    if lignes_top!=[]:
        img_hough = cv2.putText(img_hough, "rho "+str(lignes_top[0][0][0])+" theta "+str(lignes_top[0][0][1]), (8,80), cv2.FONT_HERSHEY_PLAIN, 1, 255)
    img_hough = affiche_ligne(img_hough, lignes, [0,0,255])
    img_hough = affiche_ligne(img_hough, lignes_top, [255,0,255])
    cv2.imshow("Hough", img_hough)

    ##################################################
    #seuillage pour ne garder que les couleurs claires (enleve le fond noir)
    img_seuillee = threshold(img, Smin=saturation, Vmin=luminosite)
    img_seuillee = cv2.dilate(img_seuillee, None, iterations=nb_dilatation+1)
    img_seuillee = cv2.erode(img_seuillee, None, iterations=nb_dilatation)

    img_droite = np.zeros((img_canny.shape[0], img_canny.shape[1]), np.uint8)
    debut=time.clock()
    img_droite = cv2.line(img_droite, (int(lignes_top[0][0][0]/cos(lignes_top[0][0][1])), 0), (0, int(lignes_top[0][0][0]/cos(pi/2 - lignes_top[0][0][1]))), 255)
    cv2.imshow("seuillee et droite", np.bitwise_or(img_droite, img_seuillee))
    img_droite = np.bitwise_and(img_droite, img_seuillee)
    img_droite_2 = copy.deepcopy(img_droite)
    fin=time.clock()
    img_droite_2 = cv2.putText(img_droite_2, "execute en "+str(fin-debut)+" s", (8,20), cv2.FONT_HERSHEY_PLAIN, 1, 255)
    #cv2.imshow("droite && seuillee", img_droite_2)

    ################################################
    #on récupère enfin la ligne qui nous interesse
    l_contour, _ = cv2.findContours(img_droite, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    affiche_contour_couleurs_differentes(l_contour, img_droite.shape[0], img_droite.shape[1])

    #on cherche la plus grande ligne
    len_max=0
    for i in range(len(l_contour)):
        if len(l_contour[i])>len_max:
            ligne=l_contour[i]
            len_max=len(l_contour[i])

    #on prend les deux extremités du segment
    point1 = (ligne[:,0,0].min(), ligne[:,0,1].max())
    point2 = (ligne[:,0,0].max(), ligne[:,0,1].min())

    #on affiche ces deux points
    img_finale = cv2.circle(img_init, point1, 10, [0,0,255], 3)
    img_finale = cv2.circle(img_finale, point2, 10, [0,0,255], 3)
    cv2.imshow("resultat", img_finale)



    #############################################
    #############################################
    #On détecte maintenant les deux lignes horizontales
    debut=time.clock()
    lignes = cv2.HoughLines(img_canny, 1, reso_angle_2/1000, nb_vote_min_2, min_theta=angle_min/1000, max_theta=angle_max/1000)
    fin=time.clock()
    if type(lignes)==type(None):
        lignes=[]
    img_hough_2 = affiche_ligne(img_canny, lignes, 255)

    #On cherche les droites passant par les deux points détectés précedement
    droite1=[]#droite passant par le point 1
    droite2=[]#droite passant par le point 2
    for i in range(len(lignes)):
        rho = lignes[i][0][0]
        theta = lignes[i][0][1]
        if abs(point1[0]*cos(theta)+point1[1]*sin(theta) - rho)<=5:
            droite1 = [lignes[i]]
        if abs(point2[0]*cos(theta)+point2[1]*sin(theta) - rho)<=5:
            droite2 = [lignes[i]]

    img_hough_2 = cv2.cvtColor(img_hough_2, cv2.COLOR_GRAY2BGR)
    img_hough_2 = affiche_ligne(img_hough_2, droite1, [255,0,255])
    img_hough_2 = affiche_ligne(img_hough_2, droite2, [255,0,255])

    img_hough_2 = cv2.putText(img_hough_2, "execute en "+str(fin-debut)+" s", (8,40), cv2.FONT_HERSHEY_PLAIN, 1, 255)

    img_hough_2 = cv2.circle(img_hough_2, point1, 5, [0,0,255], 1)
    img_hough_2 = cv2.circle(img_hough_2, point2, 5, [0,0,255], 1)
    cv2.imshow("Hough 2", img_hough_2)
