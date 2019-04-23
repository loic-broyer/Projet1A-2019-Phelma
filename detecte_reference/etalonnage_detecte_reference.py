#pour éxecuter : ce placer dans le dossier du fichier
#python3 ./etalonnage_detecte_reference.py
#résolution de la video en entrée : 640 * 480

import cv2
import numpy as np
import matplotlib.pyplot as plt
import copy
from math import *
import time
from fonctions_v0_6 import *
import matplotlib.pyplot as plt

nom_fichier = "videos_test/video_rasp_1.avi"

############################################################
print("opencv version :", cv2.__version__)
if cv2.__version__ != "4.0.0":
    print("Attention, ce programme a été écrit avec opencv4.0.0")

#########################################################
#Ouverture du fichier vidéo
capture = cv2.VideoCapture(nom_fichier)

#########
#paramètres à donner
L_rouge = 106
L_bleu = 98

cv2.namedWindow("Hough")
cv2.namedWindow("seuillee et droite")
cv2.namedWindow("Hough 2")
plt.figure(1)
nb_vote_min = 180
reso_angle = 2
pause = 900
luminosite = 10
nb_dilatation = 4
seuil_canny=50
cv2.createTrackbar('nb vote min',"Hough",nb_vote_min,350,lambda x: None)
cv2.createTrackbar('seuil canny',"Hough",seuil_canny,100,lambda x: None)
cv2.createTrackbar('resolution en millieme de radian',"Hough",reso_angle,50,lambda x: None)
cv2.createTrackbar("pause entre chaque image en ms","Hough",pause,1000,lambda x: None)
cv2.createTrackbar("decalage luminosite","seuillee et droite",luminosite,255,lambda x: None)
cv2.createTrackbar("nb dilatation","seuillee et droite",nb_dilatation,4,lambda x: None)

nb_vote_min_2 = 90
angle_min = int(pi*1000/2)
angle_max = int(pi*1000)-200
reso_angle_2 = 2
cv2.createTrackbar('nb vote min 2',"Hough 2",nb_vote_min_2,200,lambda x: None)
cv2.createTrackbar('resolution en millieme de radian 2',"Hough 2",reso_angle_2,50,lambda x: None)

n_image=0
L_delta_theta1=[]
L_delta_theta2=[]
L_rho=[]
L_theta=[]

def affiche_ligne(img, liste_lignes, couleur=128, epaisseur=1):
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
        img = cv2.line(img, (int(a*rho - 1000*b), int(b*rho + 1000*a)), (int(a*rho+1000*b), int(b*rho-1000*a)), couleur, epaisseur)
    return img

while cv2.waitKey(pause)!=27:
    n_image+=1
    has_frame, img_init = capture.read()
    if not has_frame:
        capture.release()#Si on est arrivé à la fin de la vidéo, on la ferme puis la relance
        capture = cv2.VideoCapture(nom_fichier)
        has_frame, img_init = capture.read()
        n_image=1
        if not has_frame:
            print("error reading the frame")
            break

    nb_vote_min = cv2.getTrackbarPos('nb vote min',"Hough")
    seuil_canny = cv2.getTrackbarPos('seuil canny',"Hough")
    reso_angle = cv2.getTrackbarPos('resolution en millieme de radian',"Hough")
    pause = cv2.getTrackbarPos("pause entre chaque image en ms","Hough")
    luminosite = cv2.getTrackbarPos("decalage luminosite","seuillee et droite")
    nb_dilatation = cv2.getTrackbarPos("nb dilatation","seuillee et droite")

    nb_vote_min_2 = cv2.getTrackbarPos('nb vote min 2',"Hough 2")
    reso_angle_2 = cv2.getTrackbarPos('resolution en millieme de radian 2',"Hough 2")

    debut_tot=time.clock()

    ###################################################
    img_init = cv2.flip(img_init, -1)#remet dans le bon sens l'image issue de la caméra du Raspberry pi


    img_resultat = copy.deepcopy(img_init)

    img = img_init[0:350,0:500]#on ne traite que la partie gauche de l'image
    img_canny = cv2.Canny(img, 2*seuil_canny, seuil_canny)

    #création d'un masque pour ignorer une partie de l'image
    masque = np.zeros((img.shape[0], img.shape[1]), np.uint8)
    masque = cv2.fillConvexPoly(masque, np.array([[[100,350],[0,200],[0,100],[300,0],[400,0],[500,100],[500,200],[200,350]]], dtype=np.int32), color=255)
    img_canny = np.bitwise_and(masque, img_canny)#supprime le coin à gauche de la détection
    #cv2.imshow("Canny", img_canny)

    img_resultat = cv2.putText(img_resultat, "pretraitement "+str(int((time.clock()-debut_tot)*1000))+" ms", (8,img_resultat.shape[0]-20), cv2.FONT_HERSHEY_PLAIN, 2, 255, thickness=2)
    #####################################################
    #détecte des droites avec la transformée de Hough
    #Le deuxième argument est la résolution de la distance en pixels
    #le troisième est la résolution de l'angle en radians
    #le quatrième est le nombre de vote minimum pour qu'une ligne soit prise en compte
    #1° = 0.017rad
    #La fonction HoughLines renvoie une liste de droites données en coordonnées polaires (rho, theta)
    debut=time.clock()
    lignes = cv2.HoughLines(img_canny, 1, reso_angle/1000, nb_vote_min, min_theta=1, max_theta=1.2)
    if type(lignes)==type(None):
        img_resultat = cv2.putText(img_resultat, "ERREUR : hough 1", (img_resultat.shape[1]//3,img_resultat.shape[0]//3), cv2.FONT_HERSHEY_PLAIN, 3, 255, thickness=3)
        cv2.imshow("resultat", img_resultat)
        cv2.waitKey(100)
        continue


    ####################################################
    #Recherche la ligne à garder
    lignes_top=[]
    rho_max = lignes[:,0,0].max()
    for i in range(len(lignes)):
        if lignes[i][0][0]==rho_max:
            lignes_top.append(lignes[i])
            rho_top = lignes_top[0][0][0]
            theta_top = lignes_top[0][0][1]

    L_rho.append(rho_top)
    L_theta.append(theta_top)


    #img_canny = cv2.putText(img_canny, "execute en "+str(fin-debut)+" s", (8,40), cv2.FONT_HERSHEY_PLAIN, 1, 255)
    #img_canny = cv2.putText(img_canny, "image numero "+str(n_image), (8,60), cv2.FONT_HERSHEY_PLAIN, 1, 255)
    img_hough = cv2.cvtColor(img_canny, cv2.COLOR_GRAY2BGR)
    img_hough = cv2.putText(img_hough, "execute en : "+str(time.clock()-debut)+" s", (8,40), cv2.FONT_HERSHEY_PLAIN, 1, 255)
    img_resultat = cv2.putText(img_resultat, "Hough1 "+str(int((time.clock()-debut)*1000))+" ms", (8,img_resultat.shape[0]-60), cv2.FONT_HERSHEY_PLAIN, 2, 255, thickness=2)
    img_hough = cv2.putText(img_hough, "rho "+str(rho_top)+" theta "+str(theta_top), (8,60), cv2.FONT_HERSHEY_PLAIN, 1, 255)
    img_hough = affiche_ligne(img_hough, lignes, [0,0,255])
    img_hough = affiche_ligne(img_hough, lignes_top, [255,0,255])
    cv2.imshow("Hough", img_hough)

    ##################################################
    #seuillage pour ne garder que les couleurs claires (enleve le fond noir)
    debut=time.clock()
    img_quart = img_init[img_init.shape[0]//2:img_init.shape[0],img_init.shape[1]//2:img_init.shape[1]]
    img_debruite = cv2.GaussianBlur(img, (3, 3), 0)#un  petit débruitage avant le seuillage
    luminosite_moy = np.mean(img_quart[:,:,2])#on définit le seuil à partir de la saturation de la luminosité moyenne d'un morceau de l'image où il n'y a que le fond du tapis de jeu
    img_seuillee = threshold(img_debruite, Vmin=int(luminosite_moy+luminosite))

    img_seuillee = cv2.erode(img_seuillee, None, iterations=1)
    img_seuillee = cv2.dilate(img_seuillee, None, iterations=nb_dilatation+1)

    img_droite = np.zeros((img_canny.shape[0], img_canny.shape[1]), np.uint8)
    img_droite = cv2.line(img_droite, (int(lignes_top[0][0][0]/cos(lignes_top[0][0][1])), 0), (0, int(lignes_top[0][0][0]/cos(pi/2 - lignes_top[0][0][1]))), 255)
    img_droite2 = np.bitwise_or(img_droite, img_seuillee)
    img_droite2 = cv2.putText(img_droite2, "luminosite moyenne : "+str(luminosite_moy), (8,40), cv2.FONT_HERSHEY_PLAIN, 1, 128)
    img_droite2 = cv2.putText(img_droite2, "execute en : "+str(time.clock()-debut)+" s", (8,60), cv2.FONT_HERSHEY_PLAIN, 1, 128)
    cv2.imshow("seuillee et droite", img_droite2)
    img_droite = np.bitwise_and(img_droite, img_seuillee)

    ################################################
    #on récupère enfin la ligne qui nous interesse
    debut=time.clock()
    l_contour, _ = cv2.findContours(img_droite, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#CHAIN_APPROX_NONE
    affiche_contour_couleurs_differentes(l_contour, img_droite.shape[0], img_droite.shape[1])

    if len(l_contour)==0:
        img_resultat = cv2.putText(img_resultat, "ERREUR : pas de ligne en intersection avec l'image seuillee", (img_resultat.shape[1]//10,img_resultat.shape[0]//3), cv2.FONT_HERSHEY_PLAIN, 2, 255, thickness=2)
        cv2.imshow("resultat", img_resultat)
        cv2.waitKey(100)
        continue

    #on cherche la plus grande ligne
    len_max=0
    for i in range(len(l_contour)):
        if len(l_contour[i])>len_max:
            ligne=l_contour[i]
            len_max=len(l_contour[i])

    #on prend les deux extremités du segment et on apporte une petite correction
    point1 = (ligne[:,0,0].min() + int(cos(pi/2-theta_top)*3), ligne[:,0,1].max() - int(sin(pi/2-theta_top)*3))
    point2 = (ligne[:,0,0].max() - int(cos(pi/2-theta_top)*4), ligne[:,0,1].min() + int(sin(pi/2-theta_top)*4))

    img_hough_2 = cv2.cvtColor(img_canny, cv2.COLOR_GRAY2BGR)
    #on affiche ces deux points
    img_hough_2 = cv2.circle(img_hough_2, point1, 10, [0,255,0], 2)
    img_hough_2 = cv2.circle(img_hough_2, point2, 10, [0,255,0], 2)
    img_hough_2 = cv2.putText(img_hough_2, "prise des points 1 et 2 executee en : "+str(time.clock()-debut)+" s", (8,80), cv2.FONT_HERSHEY_PLAIN, 1, 128)
    cv2.imshow("resultat", img_hough_2)



    #############################################
    #############################################
    #On détecte maintenant les deux lignes horizontales
    debut=time.clock()
    lignes = cv2.HoughLines(img_canny, 1, reso_angle_2/1000, nb_vote_min_2, min_theta=theta_top+1, max_theta=theta_top+1.43)
    if type(lignes)==type(None):
        img_resultat = cv2.putText(img_resultat, "ERREUR : hough 2", (img_resultat.shape[1]//3,img_resultat.shape[0]//3), cv2.FONT_HERSHEY_PLAIN, 3, 255, thickness=3)
        cv2.imshow("resultat", img_resultat)
        cv2.waitKey(100)
        continue
    img_hough_2 = affiche_ligne(img_hough_2, lignes, 255)
    img_hough_2 = cv2.putText(img_hough_2, "execute en "+str(time.clock()-debut)+" s", (8,40), cv2.FONT_HERSHEY_PLAIN, 1, 255)
    cv2.imshow("Hough 2", img_hough_2)

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
        img_resultat = cv2.putText(img_resultat, "ERREUR : pas de ligne passant proche du point 1 ou 2", (img_resultat.shape[1]//10,img_resultat.shape[0]//3), cv2.FONT_HERSHEY_PLAIN, 2, 255, thickness=2)
        cv2.imshow("resultat", img_resultat)
        cv2.waitKey(100)
        continue

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
        img_resultat = cv2.putText(img_resultat, "ERREUR : calcul du point d'intersection", (img_resultat.shape[1]//10,img_resultat.shape[0]//3), cv2.FONT_HERSHEY_PLAIN, 2, 255, thickness=2)
        cv2.imshow("resultat", img_resultat)
        cv2.waitKey(100)
        continue
    point1 = ( int((1/det)*(rho1*sin(theta_top)-rho_top*sin(theta1))) , int((1/det)*(-rho1*cos(theta_top)+rho_top*cos(theta1))) )
    det = cos(theta2)*sin(theta_top)-sin(theta2)*cos(theta_top)
    if det==0:
        img_resultat = cv2.putText(img_resultat, "ERREUR : calcul du point d'intersection", (img_resultat.shape[1]//10,img_resultat.shape[0]//3), cv2.FONT_HERSHEY_PLAIN, 2, 255, thickness=2)
        cv2.imshow("resultat", img_resultat)
        cv2.waitKey(100)
        continue
    point2 = ( int((1/det)*(rho2*sin(theta_top)-rho_top*sin(theta2))) , int((1/det)*(-rho2*cos(theta_top)+rho_top*cos(theta2))) )

    point3 = (point1[0]-int(L_rouge*cos(pi/2 - theta1)), point1[1]+int(L_rouge*sin(pi/2 - theta1)))
    point4 = (point2[0]-int(L_bleu*cos(pi/2 - theta2)), point2[1]+int(L_bleu*sin(pi/2 - theta2)))


    img_hough_2 = affiche_ligne(img_hough_2, droite1, [0,128,255], 2)
    img_hough_2 = affiche_ligne(img_hough_2, droite2, [255,0,255], 2)

    img_hough_2 = cv2.putText(img_hough_2, "rho "+str(rho1)+" theta "+str(theta1)+" delta theta 1 "+str(theta_top-theta1), (8,60), cv2.FONT_HERSHEY_PLAIN, 1, [0,128,255])
    img_hough_2 = cv2.putText(img_hough_2, "rho "+str(rho2)+" theta "+str(theta2)+" delta theta 2 "+str(theta_top-theta2), (8,80), cv2.FONT_HERSHEY_PLAIN, 1, [255,0,255])

    L_delta_theta1.append(theta_top-theta1)
    L_delta_theta2.append(theta_top-theta2)
    if n_image !=0 and n_image%100==0:
        plt.subplot(122)
        plt.plot(L_delta_theta1, L_delta_theta2, marker='+', linestyle=' ')
        plt.xlabel("delta theta 1")
        plt.ylabel("delta theta 2")
        plt.subplot(121)
        plt.plot(L_theta, L_rho, marker='+', linestyle=' ')
        plt.xlabel("theta hough 1")
        plt.ylabel("rho hough 1")
        plt.show()

    img_hough_2 = cv2.circle(img_hough_2, point1, 10, [255,0,255], 2)
    img_hough_2 = cv2.circle(img_hough_2, point2, 10, [0,0,255], 2)
    img_hough_2 = cv2.circle(img_hough_2, point3, 10, [255,0,255], 2)
    img_hough_2 = cv2.circle(img_hough_2, point4, 10, [0,0,255], 2)
    cv2.imshow("Hough 2", img_hough_2)

    img_resultat = cv2.circle(img_resultat, point1, 10, [255,0,255], 2)
    img_resultat = cv2.circle(img_resultat, point2, 10, [0,0,255], 2)
    img_resultat = cv2.circle(img_resultat, point3, 10, [255,0,255], 2)
    img_resultat = cv2.circle(img_resultat, point4, 10, [0,0,255], 2)
    img_resultat = cv2.putText(img_resultat, "temps total d'execution : "+str(time.clock()-debut_tot)+" s", (8,30), cv2.FONT_HERSHEY_PLAIN, 2, 255, thickness=2)
    cv2.imshow("resultat", img_resultat)

    cv2.imshow("masque pour ne traiter qu'une partie de l'image", masque)
