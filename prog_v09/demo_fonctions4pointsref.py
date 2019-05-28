from fonctions4pointsref import fonctions4pointsref, affiche_3_couleurs
from fonctions import threshold
import cv2
import time
import numpy as np

nom_fichier = "../videos_test/video_rasp_1.avi"
capture = cv2.VideoCapture(nom_fichier)#Ouverture du fichier vidéo

#Phase d'étalonnage
perspective_m, couleurs = fonctions4pointsref(capture)#appel à la fonction qui retourne les valeurs d'étalonnage
#affiche dans une fenêtre les trois couleurs détectées
cv2.namedWindow("couleurs")
affiche_3_couleurs(couleurs)

print("couleurs :", couleurs)
print("Fin de l'étalonnage")
#Commence la détection des palets et des robots
tol_teinte=20
seuil_sat=40
tol_lumin=40
cv2.createTrackbar("tolerance teinte","couleurs",tol_teinte,40,lambda x: None)
cv2.createTrackbar("seuil saturation","couleurs",seuil_sat,80,lambda x: None)
cv2.createTrackbar("tolerance luminosite","couleurs",tol_lumin,80,lambda x: None)


while cv2.waitKey(20)!=27:
    tol_teinte = cv2.getTrackbarPos("tolerance teinte","couleurs")
    seuil_sat = cv2.getTrackbarPos("seuil saturation","couleurs")
    tol_lumin = cv2.getTrackbarPos("tolerance luminosite","couleurs")

    debut = time.clock()
    has_frame, img_init = capture.read()
    if not has_frame:
        capture.release()#Si on est arrivé à la fin de la vidéo, on la ferme puis la relance
        capture = cv2.VideoCapture(nom_fichier)
        has_frame, img_init = capture.read()
        if not has_frame:
            print("error reading the frame")
            break


    #remet dans le bon sens l'image issue de la caméra du Raspberry pi
    img_init = cv2.flip(img_init, -1)

    cv2.imshow('initiale', img_init)
    img = cv2.warpPerspective(img_init, perspective_m, (600, 600))
    cv2.imshow('corrige', img)
    #un  petit débruitage avant le seuillage
    img = cv2.GaussianBlur(img, (3, 3), 0)
    #seuillage suivant les couleurs détectées pendant l'étalonnage
    img_seuillee_r = threshold(img, Hmin=(couleurs[0, 0]-tol_teinte)%180, Hmax=(couleurs[0, 0]+tol_teinte)%180, Vmin=couleurs[0, 2]-tol_lumin, Smin=seuil_sat)
    cv2.imshow("seuillee rouge", img_seuillee_r)
    img_seuillee_v = threshold(img, Hmin=couleurs[1, 0]-tol_teinte, Hmax=couleurs[1, 0]+tol_teinte, Vmin=couleurs[1, 2]-tol_lumin, Smin=seuil_sat)
    cv2.imshow("seuillee verte", img_seuillee_v)
    img_seuillee_b = threshold(img, Hmin=couleurs[2, 0]-tol_teinte, Hmax=couleurs[2, 0]+tol_teinte, Vmin=couleurs[2, 2]-tol_lumin, Smin=seuil_sat)
    cv2.imshow("seuillee bleue", img_seuillee_b)

cv2.destroyAllWindows()
capture.release()
