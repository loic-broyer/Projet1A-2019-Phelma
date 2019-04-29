import cv2
import numpy as np

def centroid(contour):
    """Returns the coordinate X and Y of the centroid of the input contour in the form of a tuple"""
    M = cv2.moments(contour)
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
        img_1 = cv2.inRange(HSVImg, np.array([0,Smin,Vmin]), np.array([Hmax,Smax,Vmax]))
        #seuillage de Hmin à 179
        img_2 = cv2.inRange(HSVImg, np.array([Hmin,Smin,Vmin]), np.array([179,Smax,Vmax]))
        #ou logique entre les deux
        return np.bitwise_or(img_1, img_2)


def sortContourPerimeter(liste_contour,perimetre_min,perimetre_max):
    #Tri des contours suivant leur périmètre et leur taille en x et en y:
    liste_contour_tries=[]
    for i in range(len(liste_contour)):
        if len(liste_contour[i])>=perimetre_min and len(liste_contour[i])<=perimetre_max:
            #print("contour n° "+str(i))
            liste_contour_tries.append(liste_contour[i])
    return liste_contour_tries

def sortContourSurface(liste_contour,aire_min,aire_max):
    #Tri des contours
    #supprime les contours qui ont une aire trop petite
    liste_contour_tries=[]
    for i in range(len(liste_contour)):
        aire = cv2.contourArea(liste_contour[i])
        if aire >= aire_min and aire <= aire_max :
            liste_contour_tries.append(liste_contour[i])
    return liste_contour_tries


    






    