import cv2
import numpy as np
import time
from math import *
from fonctions import threshold
import server
import socket
import sys

def fonctions4pointsref(capture,socket): #attend une pression sur echap ou un signal réseau
    etalonnage = np.full((10,4,2), -1)#tableau pour stocker les dix dernières positions détectées
    etal_couleur = np.full((10,3,3), -1)#tableau pour stocker les dix dernier triplets de couleurs mesurées
    i=-1#indice pour écrire dans les deux tableaux
    gameStart = False
    while cv2.waitKey(20)!=27 and not gameStart:
        gameStart = server.netWaitForStart(socket, 1, 1)
        debut = time.clock()
        has_frame, img_init = capture.read()
        if not has_frame:
            print("error reading the frame")
            break

        #remet dans le bon sens l'image issue de la caméra du Raspberry pi
        img_init = cv2.flip(img_init, -1)

        ok, points, couleurs = reference(img_init)

        if ok == 0:
            #il y a eu une erreur
            img_init = cv2.putText(img_init, "ERREUR", (img_init.shape[1]//10,img_init.shape[0]//3), cv2.FONT_HERSHEY_PLAIN, 4, 255, thickness=4)
        else:
            img_init = cv2.circle(img_init, tuple(points[0]), 10, [255,0,255], 3)
            img_init = cv2.circle(img_init, tuple(points[1]), 10, [0,0,255], 3)
            img_init = cv2.circle(img_init, tuple(points[2]), 10, [255,0,0], 3)
            img_init = cv2.circle(img_init, tuple(points[3]), 10, [0,255,0], 3)
            img_init = cv2.putText(img_init, "temps total d'execution : "+str(time.clock()-debut)+" s", (8,30), cv2.FONT_HERSHEY_PLAIN, 2, 255, thickness=2)
            img_init = cv2.putText(img_init, "points[0]", (8,60), cv2.FONT_HERSHEY_PLAIN, 2, [255,0,255], thickness=2)
            img_init = cv2.putText(img_init, "points[1]", (8,90), cv2.FONT_HERSHEY_PLAIN, 2, [0,0,255], thickness=2)
            img_init = cv2.putText(img_init, "points[2]", (8,120), cv2.FONT_HERSHEY_PLAIN, 2, [255,0,0], thickness=2)
            img_init = cv2.putText(img_init, "points[3]", (8,150), cv2.FONT_HERSHEY_PLAIN, 2, [0,255,0], thickness=2)

            if i==-1:
                for i in range(10):
                    etalonnage[i] = points
                    etal_couleur[i] = couleurs
                i=0
            else:
                etalonnage[i] = points
                etal_couleur[i] = couleurs
                i = (i+1)%10

        cv2.imshow("initiale", img_init)

    src_pts = np.mean(etalonnage, axis=0, dtype=np.float32)
    dst_pts = np.array([[0, 120], [180, 120], [180, 480], [0, 480]],dtype=np.float32)
    couleurs = np.mean(etal_couleur, axis=0, dtype=np.float32)
    return (cv2.getPerspectiveTransform(src_pts, dst_pts), couleurs, gameStart)



def reference(img_init):
    "retourne les coordonnées des quatre points sur l'image passée en argument, retourne un entier indiquant si la détection a fonctionnée et retourne les valeurs en HSV des trois couleurs mesurées [rouge, vert, bleu]"

    print("appel à la fonction reference")
    #paramètres à donner
    L_rouge = 106
    L_bleu = 98

    nb_vote_min = 180
    reso_angle = 2
    luminosite = 10
    saturation = 20
    nb_dilatation = 4
    seuil_canny=50

    nb_vote_min_2 = 75
    angle_min = int(pi*1000/2)
    angle_max = int(pi*1000)-200
    reso_angle_2 = 2


    img = img_init[0:350,0:500]
    img_canny = cv2.Canny(img, 2*seuil_canny, seuil_canny)

    #création d'un masque pour ignorer une partie de l'image
    masque = np.zeros((img.shape[0], img.shape[1]), np.uint8)
    masque = cv2.fillConvexPoly(masque, np.array([[[100,350],[0,200],[0,100],[300,0],[400,0],[500,100],[500,200],[200,350]]], dtype=np.int32), color=255)
    img_canny = np.bitwise_and(masque, img_canny)#supprime de la détection le coin en haut à gauche

    #détecte des droites avec la transformée de Hough
    #Le deuxième argument est la résolution de la distance en pixels
    #le troisième est la résolution de l'angle en radians
    #le quatrième est le nombre de vote minimum pour qu'une ligne soit prise en compte
    #1° = 0.017rad
    #La fonction HoughLines renvoie une liste de droites données en coordonnées polaires (rho, theta)

    lignes = cv2.HoughLines(img_canny, 1, reso_angle/1000, nb_vote_min, min_theta=0.9, max_theta=1.2)
    if type(lignes)==type(None):
        print("\tERREUR Hough 1 pas de droites detectées")
        return 0, [], []#ERREUR

    #Recherche la ligne à garder
    lignes_top=[]
    rho_max = lignes[:,0,0].max()
    for i in range(len(lignes)):
        if lignes[i][0][0]==rho_max:
            lignes_top.append(lignes[i])
            rho_top = lignes_top[0][0][0]
            theta_top = lignes_top[0][0][1]

    #seuillage pour ne garder que les couleurs claires (enleve le fond noir)

    img_quart = img_init[img_init.shape[0]//2:img_init.shape[0],img_init.shape[1]//2:img_init.shape[1]]
    img_debruite = cv2.GaussianBlur(img, (3, 3), 0)#un  petit débruitage avant le seuillage
    luminosite_moy = np.mean(img_quart[:,:,2])#on définit le seuil à partir de la luminosité moyenne d'un morceau de l'image où il n'y a que le fond du tapis de jeu
    img_seuillee = threshold(img_debruite, Vmin=int(luminosite_moy+luminosite), Smin=saturation)

    img_seuillee = cv2.erode(img_seuillee, None, iterations=1)
    img_seuillee = cv2.dilate(img_seuillee, None, iterations=nb_dilatation+1)

    img_droite = np.zeros((img_canny.shape[0], img_canny.shape[1]), np.uint8)
    img_droite = cv2.line(img_droite, (int(round(lignes_top[0][0][0]/cos(lignes_top[0][0][1]))), 0), (0, int(round(lignes_top[0][0][0]/cos(pi/2 - lignes_top[0][0][1])))), 255)
    img_droite = np.bitwise_and(img_droite, img_seuillee)

    #on récupère enfin la ligne qui nous interesse
    l_contour, _ = cv2.findContours(img_droite, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(l_contour)==0:
        print("\tERREUR Hough 1 pas de droites sur une surface de couleur claire")
        return 0, [], []#ERREUR

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
    #On détecte maintenant les deux lignes horizontales
    lignes = cv2.HoughLines(img_canny, 1, reso_angle_2/1000, nb_vote_min_2, min_theta=theta_top+1, max_theta=theta_top+1.43)
    if type(lignes)==type(None):
        print("\tERREUR Hough 2 pas de droites detectées")
        return 0, [], []#ERREUR

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
        print("\tERREUR pas de doites passant proche des points 1 ou 2")
        return 0, [], []#ERREUR

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
        print("\tERREUR pas de point d'intersection")
        return 0, [], []#ERREUR

    point1 = ( int(round((1/det)*(rho1*sin(theta_top)-rho_top*sin(theta1)))) , int(round((1/det)*(-rho1*cos(theta_top)+rho_top*cos(theta1)))) )
    det = cos(theta2)*sin(theta_top)-sin(theta2)*cos(theta_top)
    if det==0:
        print("\tERREUR pas de point d'intersection")
        return 0, [], []#ERREUR
    point2 = ( int(round((1/det)*(rho2*sin(theta_top)-rho_top*sin(theta2)))) , int(round((1/det)*(-rho2*cos(theta_top)+rho_top*cos(theta2)))) )

    if point1[0]<50 or point1[1]<50 or point2[0]<50 or point2[1]<50:
        print("\tERREUR les points 3 et 4 ont été détectés trop près du bord de l'image")
        return 0, [], []#ERREUR

    #Calcule la position des points 3 et 4
    point3 = (point1[0]-int(round(L_rouge*cos(pi/2 - theta1))), point1[1]+int(round(L_rouge*sin(pi/2 - theta1))))
    point4 = (point2[0]-int(round(L_bleu*cos(pi/2 - theta2))), point2[1]+int(round(L_bleu*sin(pi/2 - theta2))))

    print("\tPoints détectés",point1, point2, point3, point4)


    ###############################################
    #-----Détermine la couleur vue par la caméra des trois zones du tableau périodique
    #on extraie une petite image au voisinage des points 1 et 2
    img_point1 = img_init[point1[1]-50:point1[1], point1[0]-50:point1[0]]
    #un  petit débruitage avant le seuillage
    img_point1s = cv2.GaussianBlur(img_point1, (3, 3), 0)
    #les pixels qui ont une luminosité supérieur au seuil sont remplacés par un pixel blanc et les autre par un noir
    img_point1s = threshold(img_point1s, Vmin=int(luminosite_moy+2*luminosite))
    #ont compte combien de pixel sont blanc
    nb_pixel1 = np.sum(img_point1s)/255
    #les pixels ayant une luminosité importante sont gardés et les autres sont remplacés par un pixel noir
    img_point1s = cv2.cvtColor(img_point1s, cv2.COLOR_GRAY2BGR)
    img_point1a = np.bitwise_and(img_point1s, cv2.cvtColor(img_point1, cv2.COLOR_BGR2HSV))
    #la couleur rouge est obtenue en faisant la moyenne de la valeur des pixels qui ont une luminosité suffisante
    couleur_rouge = [((np.sum((img_point1a[:,:,0]+40)%180)-40*img_point1a.shape[0]*img_point1a.shape[1])/nb_pixel1)%180, np.sum(img_point1a[:,:,1])/nb_pixel1, np.sum(img_point1a[:,:,2])/nb_pixel1]

    #pareil pour le bleu
    img_point2 = img_init[point2[1]-50:point2[1], point2[0]-50:point2[0]]
    img_point2s = cv2.GaussianBlur(img_point2, (3, 3), 0)
    img_point2s = threshold(img_point2s, Vmin=int(luminosite_moy+2*luminosite))
    nb_pixel2 = np.sum(img_point2s)/255
    img_point2s = cv2.cvtColor(img_point2s, cv2.COLOR_GRAY2BGR)
    img_point2a = np.bitwise_and(img_point2s, cv2.cvtColor(img_point2, cv2.COLOR_BGR2HSV))
    couleur_bleue = [np.sum(img_point2a[:,:,0])/nb_pixel2, np.sum(img_point2a[:,:,1])/nb_pixel2, np.sum(img_point2a[:,:,2])/nb_pixel2]

    #Pour obtenir la couleur verte, on calcule la moyenne des points 1 et 2 avec des coeff qui vont bien
    point_v = [int(point1[0]*0.4+point2[0]*0.6), int(point1[1]*0.4+point2[1]*0.6)]
    img_point_v = img_init[point_v[1]-30:point_v[1], point_v[0]-50:point_v[0]]
    img_pointvs = cv2.GaussianBlur(img_point_v, (3, 3), 0)#un  petit débruitage avant le seuillage
    img_pointvs = threshold(img_pointvs, Vmin=int(luminosite_moy+4*luminosite))
    nb_pixelv = np.sum(img_pointvs)/255
    img_pointvs = cv2.cvtColor(img_pointvs, cv2.COLOR_GRAY2BGR)
    img_pointva = np.bitwise_and(img_pointvs, cv2.cvtColor(img_point_v, cv2.COLOR_BGR2HSV))
    couleur_verte = [np.sum(img_pointva[:,:,0])/nb_pixelv, np.sum(img_pointva[:,:,1])/nb_pixelv, np.sum(img_pointva[:,:,2])/nb_pixelv]

    return 1, [np.array(point4), np.array(point2), np.array(point1), np.array(point3)], np.array([couleur_rouge, couleur_verte, couleur_bleue])

def image_couleur(shape, couleur):
    "retourne une image de dimension 'shape' d'une seule couleur, celle passée en argument (en hsv)"
    img = np.full([shape[0], shape[1], 3], couleur, np.uint8)
    return cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

def affiche_3_couleurs(couleurs):
    "affiche dans une fenêtre les trois couleurs détectées"
    img_r = image_couleur([100,100], couleurs[0])
    img_v = image_couleur([100,100], couleurs[1])
    img_b = image_couleur([100,100], couleurs[2])
    cv2.imshow("couleurs", np.concatenate((img_r, img_v, img_b), 1))
    return
