
import cv2
import numpy as np
import matplotlib.pyplot as plt
import copy
import random
from fonctions_v0_6 import *

nom_fichier="photo_test_1"

############################################################
print("opencv version :", cv2.__version__)
if cv2.__version__ != "4.0.0":
    print("Attention, ce programme a été écrit avec opencv4.0.0")

##########################################################
#Lecture d'une image à partir d'un fichier
img_source = cv2.imread(nom_fichier+".jpg")
assert img_source is not None # vérifie que l'image a bien été chargée

###################################################
#réduit la dimension de l'image
print('dimensions :', img_source.shape)
print('dtype:', img_source.dtype)
#img.shape[0] nb de ligne
#img.shape[1] nb de colonne
#cv.imwrite('sortie.png', img_renverse,[cv.IMWRITE_PNG_COMPRESSION, 0])

ratio = img_source.shape[1]/img_source.shape[0]
img_resized = cv2.resize(img_source,(int(900*ratio),900))

rect = np.array([[1148,580],[1760,708],[560,1800],[0,1476]],dtype = "float32")

for e in rect:
    e[0] = e[0]
    e[1] = e[1]

print("ceci est le rect")
print (rect)


(tl,tr,br,bl) = rect

widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
maxWidth = max(int(widthA), int(widthB))
print(maxWidth)

heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
maxHeight = max(int(heightA), int(heightB))
print(maxHeight)


dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")


# compute the perspective transform matrix and then apply it
M = cv2.getPerspectiveTransform(rect, dst)



cadre = np.zeros((10000,10000,3))

cadre[3000:6120,3000:7160] = img_source


warped = cv2.warpPerspective(cadre, M, (3000,3000))





while True:
    cv2.imshow('window',cadre)
    key = cv2.waitKey(3)
    if key == 27:
        break

cv2.destroyAllWindows()
