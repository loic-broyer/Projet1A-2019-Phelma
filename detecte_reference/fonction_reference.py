import cv2
import numpy as np
from math import *
from fonctions_v0_6 import threshold


#########
#paramètres à donner
L_rouge = 106
L_bleu = 98

nb_vote_min = 180
reso_angle = 2
pause = 900
luminosite = 10
nb_dilatation = 4
seuil_canny=50

nb_vote_min_2 = 90
angle_min = int(pi*1000/2)
angle_max = int(pi*1000)-200
reso_angle_2 = 2


def reference(img_init):
    """retourne les coordonnées des quatre points sur l'image passée en argument, retourne aussi un entier indiquant si la détection a fonctionnée"""

    img = img_init[0:350,0:500]
    img_canny = cv2.Canny(img, 2*seuil_canny, seuil_canny)

    #création d'un masque pour ignorer une partie de l'image
    masque = np.zeros((img.shape[0], img.shape[1]), np.uint8)
    masque = cv2.fillConvexPoly(masque, np.array([[[100,350],[0,200],[0,100],[300,0],[400,0],[500,100],[500,200],[200,350]]], dtype=np.int32), color=255)
    img_canny = np.bitwise_and(masque, img_canny)#supprime de la détection le coin en haut à gauche


    #####################################################
    #détecte des droites avec la transformée de Hough
    #Le deuxième argument est la résolution de la distance en pixels
    #le troisième est la résolution de l'angle en radians
    #le quatrième est le nombre de vote minimum pour qu'une ligne soit prise en compte
    #1° = 0.017rad
    #La fonction HoughLines renvoie une liste de droites données en coordonnées polaires (rho, theta)

    lignes = cv2.HoughLines(img_canny, 1, reso_angle/1000, nb_vote_min, min_theta=1, max_theta=1.2)
    if type(lignes)==type(None):
        return 0, (0,0), (0,0), (0,0), (0,0)#ERREUR


    ####################################################
    #Recherche la ligne à garder
    lignes_top=[]
    rho_max = lignes[:,0,0].max()
    for i in range(len(lignes)):
        if lignes[i][0][0]==rho_max:
            lignes_top.append(lignes[i])
            rho_top = lignes_top[0][0][0]
            theta_top = lignes_top[0][0][1]

    ##################################################
    #seuillage pour ne garder que les couleurs claires (enleve le fond noir)

    img_quart = img_init[img_init.shape[0]//2:img_init.shape[0],img_init.shape[1]//2:img_init.shape[1]]
    img_debruite = cv2.GaussianBlur(img, (3, 3), 0)#un  petit débruitage avant le seuillage
    luminosite_moy = np.mean(img_quart[:,:,2])#on définit le seuil à partir de la luminosité moyenne d'un morceau de l'image où il n'y a que le fond du tapis de jeu
    img_seuillee = threshold(img_debruite, Vmin=int(luminosite_moy+luminosite))

    img_seuillee = cv2.erode(img_seuillee, None, iterations=1)
    img_seuillee = cv2.dilate(img_seuillee, None, iterations=nb_dilatation+1)

    img_droite = np.zeros((img_canny.shape[0], img_canny.shape[1]), np.uint8)
    img_droite = cv2.line(img_droite, (int(lignes_top[0][0][0]/cos(lignes_top[0][0][1])), 0), (0, int(lignes_top[0][0][0]/cos(pi/2 - lignes_top[0][0][1]))), 255)
    img_droite = np.bitwise_and(img_droite, img_seuillee)

    ################################################
    #on récupère enfin la ligne qui nous interesse
    l_contour, _ = cv2.findContours(img_droite, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#CHAIN_APPROX_NONE

    if len(l_contour)==0:
        return 0, (0,0), (0,0), (0,0), (0,0)#ERREUR

    #on cherche la plus grande ligne
    len_max=0
    for i in range(len(l_contour)):
        if len(l_contour[i])>len_max:
            ligne=l_contour[i]
            len_max=len(l_contour[i])

    #on prend les deux extremités du segment et on apporte une petite correction
    point1 = (ligne[:,0,0].min() + int(cos(pi/2-theta_top)*3), ligne[:,0,1].max() - int(sin(pi/2-theta_top)*3))
    point2 = (ligne[:,0,0].max() - int(cos(pi/2-theta_top)*4), ligne[:,0,1].min() + int(sin(pi/2-theta_top)*4))



    #############################################
    #############################################
    #On détecte maintenant les deux lignes horizontales
    lignes = cv2.HoughLines(img_canny, 1, reso_angle_2/1000, nb_vote_min_2, min_theta=theta_top+1, max_theta=theta_top+1.43)
    if type(lignes)==type(None):
        return 0, (0,0), (0,0), (0,0), (0,0)#ERREUR


    #On calcule la distance minimale entre une droite et chacun des deux points
    #(on exclut aussi les droites qui n'ont pas le bon angle par rapport à la grande droite détectée avant)
    min1=100
    min2=100
    for i in range(len(lignes)):
        rho = lignes[i][0][0]
        theta = lignes[i][0][1]
        if abs(point1[0]*cos(theta)+point1[1]*sin(theta) - rho)<min1 and -1.43<theta_top-theta<-1.17:
            min1 = abs(point1[0]*cos(theta)+point1[1]*sin(theta) - rho)
        if abs(point2[0]*cos(theta)+point2[1]*sin(theta) - rho)<min2 and -1.26<theta_top-theta<-1:
            min2 = abs(point2[0]*cos(theta)+point2[1]*sin(theta) - rho)

    #on stocke dans deux listes les droites qui passent proche des points à une distance max de la distance minimale + 5
    l_droite1=[]#droites passant proche du point 1
    l_droite2=[]#droites passant proche du point 2
    for i in range(len(lignes)):
        rho = lignes[i][0][0]
        theta = lignes[i][0][1]
        if abs(point1[0]*cos(theta)+point1[1]*sin(theta) - rho)<=min1+3:
            l_droite1.append(lignes[i])
        if abs(point2[0]*cos(theta)+point2[1]*sin(theta) - rho)<=min2+3:
            l_droite2.append(lignes[i])

    if l_droite1 == [] or l_droite2 == []:
        return 0, (0,0), (0,0), (0,0), (0,0)#ERREUR

    #la droite 1 sélectionnée sera celle parmi la liste qui a l'angle theta le plus petit
    theta_min = l_droite1[0][0][1]
    droite1 = [l_droite1[0]]
    for i in range(len(droite1)):
        if l_droite1[i][0][1]<theta_min:
            theta_min = l_droite1[i][0][1]
            droite1 = [l_droite1[i]]

    #la droite 2 sélectionnée sera celle parmi la liste qui a l'angle theta le plus grand
    theta_max = l_droite2[0][0][1]
    droite2 = [l_droite2[0]]
    for i in range(len(droite2)):
        if droite1[i][0][1]<theta_min:
            theta_min = l_droite2[i][0][1]
            droite2 = [l_droite2[i]]

    rho1 = droite1[0][0][0]
    theta1 = droite1[0][0][1]
    rho2 = droite2[0][0][0]
    theta2 = droite2[0][0][1]

    #on recalcule les points 1 et 2 plus précisemment
    det = cos(theta1)*sin(theta_top)-sin(theta1)*cos(theta_top)
    if det==0:
        return 0, (0,0), (0,0), (0,0), (0,0)#ERREUR
    point1 = ( int((1/det)*(rho1*sin(theta_top)-rho_top*sin(theta1))) , int((1/det)*(-rho1*cos(theta_top)+rho_top*cos(theta1))) )
    det = cos(theta2)*sin(theta_top)-sin(theta2)*cos(theta_top)
    if det==0:
        return 0, (0,0), (0,0), (0,0), (0,0)#ERREUR
    point2 = ( int((1/det)*(rho2*sin(theta_top)-rho_top*sin(theta2))) , int((1/det)*(-rho2*cos(theta_top)+rho_top*cos(theta2))) )

    point3 = (point1[0]-int(L_rouge*cos(pi/2 - theta1)), point1[1]+int(L_rouge*sin(pi/2 - theta1)))
    point4 = (point2[0]-int(L_bleu*cos(pi/2 - theta2)), point2[1]+int(L_bleu*sin(pi/2 - theta2)))

    return 1, point4, point2, point1, point3
