from fonction_reference import reference
import cv2
import time
import numpy as np

nom_fichier = "videos_test/video_rasp_1.avi"
capture = cv2.VideoCapture(nom_fichier)#Ouverture du fichier vidéo

while cv2.waitKey(15)!=27:
    debut = time.clock()
    has_frame, img_init = capture.read()
    if not has_frame:
        capture.release()#Si on est arrivé à la fin de la vidéo, on la ferme puis la relance
        capture = cv2.VideoCapture(nom_fichier)
        has_frame, img_init = capture.read()
        n_image=1
        if not has_frame:
            print("error reading the frame")
            break

    img_init = cv2.flip(img_init, -1)#remet dans le bon sens l'image issue de la caméra du Raspberry pi
    ok, point1, point2, point3, point4 = reference(img_init)

    if ok == 0:
        #il y a eu une erreur
        img_init = cv2.putText(img_init, "ERREUR", (img_init.shape[1]//10,img_init.shape[0]//3), cv2.FONT_HERSHEY_PLAIN, 4, 255, thickness=4)
    else:
        img_init = cv2.circle(img_init, point1, 10, [255,0,255], 3)
        img_init = cv2.circle(img_init, point2, 10, [0,0,255], 3)
        img_init = cv2.circle(img_init, point3, 10, [255,0,0], 3)
        img_init = cv2.circle(img_init, point4, 10, [0,255,0], 3)
        img_init = cv2.putText(img_init, "temps total d'execution : "+str(int((time.clock()-debut)*1000))+" ms", (8,30), cv2.FONT_HERSHEY_PLAIN, 2, 255, thickness=2)
        img_init = cv2.putText(img_init, "point1", (8,60), cv2.FONT_HERSHEY_PLAIN, 2, [255,0,255], thickness=2)
        img_init = cv2.putText(img_init, "point2", (8,90), cv2.FONT_HERSHEY_PLAIN, 2, [0,0,255], thickness=2)
        img_init = cv2.putText(img_init, "point3", (8,120), cv2.FONT_HERSHEY_PLAIN, 2, [255,0,0], thickness=2)
        img_init = cv2.putText(img_init, "point4", (8,150), cv2.FONT_HERSHEY_PLAIN, 2, [0,255,0], thickness=2)

    cv2.imshow("resultat", img_init)
