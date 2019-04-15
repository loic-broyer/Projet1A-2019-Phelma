import cv2
import numpy as np

image = cv2.imread('nom_du_fichier'.png)

## pour sauver au format PNG

cv2.imwrite('nom_du_fichier.png', image, [cv2.IMWRITE_PNG_COMPRESSION, 0])
saved_img = cv2.imread(params.out_png)
assert saved_img.all() == img.all()
