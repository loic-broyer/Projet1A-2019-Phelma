import cv2
import numpy as np


def centroid(contour):
    """Returns the coordinate X and Y of the centroid of the input contour in the form of a tuple"""
    M = cv2.moments(contour)
    #print(contour)
    #print("AAAAAAAAAAAa")
    if (M['m00'] !=0 ):
        Cx = int(M['m10']/M['m00'])
        Cy = int(M['m01']/M['m00'])
        return(Cx,Cy)


def threshold(img,Hmin=0,Hmax=179,Smin=0,Smax=255,Vmin=0,Vmax=255):
    HSVImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if Hmin<=Hmax:
        return cv2.inRange(HSVImg, np.array([Hmin,Smin,Vmin]), np.array([Hmax,Smax,Vmax]))
    else:
        #seuillage de 0 à Hmax
        img_temp_1 = cv2.inRange(HSVImg, np.array([0,Smin,Vmin]), np.array([Hmax,Smax,Vmax]))
        #seuillage de Hmin à 179
        img_temp_2 = cv2.inRange(HSVImg, np.array([Hmin,Smin,Vmin]), np.array([179,Smax,Vmax]))
        #somme des deux
        for i in range(img_temp_1.shape[0]):
            for j in range(img_temp_1.shape[1]):
                if img_temp_2[i][j]==255:
                    img_temp_1[i][j]=255
        return img_temp_1



def triContourPerimetre(liste_contour,perimetre_min,perimetre_max):
    #Tri des contours suivant leur périmètre et leur taille en x et en y:
    liste_contour_tries=[]
    for i in range(len(liste_contour)):
        if len(liste_contour[i])>=perimetre_min and len(liste_contour[i])<=perimetre_max:
            print("contour n° "+str(i))
            liste_contour_tries.append(liste_contour[i])
    return liste_contour_tries

def triContourAire(liste_contour,aire_min,aire_max):
    #Tri des contours
    #supprime les contours qui ont une aire trop petite
    liste_contour_tries=[]
    for i in range(len(liste_contour)):
        aire = cv2.contourArea(liste_contour[i])
        if aire >= aire_min and aire <= aire_max :
            liste_contour_tries.append(liste_contour[i])
    return liste_contour_tries

def DrawContoursDifferentColors(liste_contour, img):
    #prend en paramètre les dimensions de l'image dont on a pris les contours
    #affiche tous les contours avec une couleur différente par contour
    for i in range(len(liste_contour)):
        a=(15*i)%256
        b=(22*i)%256
        c=(9*i)%256
        if a+b+c<80:#pour ne pas avoir de contour trop sombre
            a+=30
            b+=30
            c+=30
        couleur=[a,b,c]
        cv2.drawContours(img,liste_contour[i],-1,couleur,2)



def detecte_palets(img, couleur="vert", affichage=0):
    #retourne une liste contenant les centres de tous les palets de la couleur demandée
    #passer 0 en paramètre d'affichage pour ne pas afficher les images intermédiaires
    assert couleur in ["rouge", "vert", "bleu"]

    ##########################################################
    #Prise des contours de l'image
    if couleur == "vert":
        img = seuillageCouleur(img,29,74,20)
    elif couleur == "bleu":
        img = seuillageCouleur(img,81,102,50)
    else:
        img = seuillageCouleur(img,177,10,60)

    img_canny = cv2.Canny(img, 50, 100, 3)
    if affichage != 0:
        cv2.imshow('image seuillée pour le '+couleur, img)
        cv2.imshow('image passée au filtre de Canny pour le '+couleur, img_canny)
        cv2.waitKey(0)

    #########################################################
    #Regroupement des pixels détectés par contour
    liste_contour, _ = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if affichage != 0:
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
    if affichage != 0:
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
        liste_centre_palets[i][1] = centre_x//len(liste_contour_tries[i])
        liste_centre_palets[i][0] = centre_y//len(liste_contour_tries[i])
        if affichage == 1:
            print(centre_x,len(liste_contour_tries[i]),liste_centre_palets[i][1])
            print(centre_y,len(liste_contour_tries[i]),liste_centre_palets[i][0])

    #rajoute le centre sur l'image des contours
    for i in range(len(liste_centre_palets)):
        img_contours[liste_centre_palets[i][1]][liste_centre_palets[i][0]]=255

    if affichage != 0:
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
