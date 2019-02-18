import cv2
import numpy as np
#CODAGE BGR PLUTOT QUE RGB



# img = cv2.imread("test1.jpg")
#
# assert img is not None #check if image was loaded

# print('original shape:', img.shape)
# print('dtype:', img.dtype)
#
# width , height = 500, 500
# WMult,HMult = 0.5, 0.5
# resizedImg = cv2.resize(img, (width, height))


# print("resized shape : ", resizedImg.shape)
#
# img_flip_along_x = cv2.flip(resizedImg, 0)
#
# cv2.imwrite("testsave1.jpeg",resizedImg,[cv2.IMWRITE_JPEG_QUALITY,80])
#
#
# size = (img.shape[0:2])
#
#
# cv2.imshow('original image',img)
# cv2.waitKey(2000)


sourceImg = cv2.imread("photo_test_1.jpg")
sourceImg = cv2.resize(sourceImg,(500,500))
assert sourceImg is not None

HSVImg = cv2.cvtColor(sourceImg, cv2.COLOR_BGR2HSV)

def nothing(x):
    pass

cv2.namedWindow('window')
cv2.createTrackbar('Hmin','window',0,179,nothing)
cv2.createTrackbar('Hmax','window',0,179,nothing)
cv2.createTrackbar('Smin','window',0,255,nothing)
cv2.createTrackbar('Smax','window',0,255,nothing)
cv2.createTrackbar('Vmin','window',0,255,nothing)
cv2.createTrackbar('Vmax','window',0,255,nothing)


cv2.imshow("originale",HSVImg)



while True:
    Hmin = cv2.getTrackbarPos('Hmin','window')
    Hmax = cv2.getTrackbarPos('Hmax','window')
    Smin = cv2.getTrackbarPos('Smin','window')
    Smax = cv2.getTrackbarPos('Smax','window')
    Vmin = cv2.getTrackbarPos('Vmin','window')
    Vmax = cv2.getTrackbarPos('Vmax','window')
    Filtered = cv2.inRange(HSVImg, np.array([Hmin,Smin,Vmin]), np.array([Hmax,Smax,Vmax]))
    cv2.imshow('window', Filtered)


    key = cv2.waitKey(3)
    if key == 27:
        break

cv2.destroyAllWindows()
