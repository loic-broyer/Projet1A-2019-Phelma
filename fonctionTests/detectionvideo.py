#import fonctions as f
import cv2
import numpy
import fonctions_v0_5 as f


capture = cv2.VideoCapture(0)

while True:
    has_frame, frame = capture.read()
    if not has_frame:
        print("error reading the frame")
        break
    liste_centre_palets_vert= f.detecte_palets(frame, "vert",0)
    for point in liste_centre_palets_vert:
        cv2.circle(frame,point,3,(255,0,0),-1)
    cv2.imshow('camera',frame)
    key = cv2.waitKey(3)
    if key == 27:
        break
