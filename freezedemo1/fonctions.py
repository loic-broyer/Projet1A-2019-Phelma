import cv2
import numpy as np

##init

RED = [0,0,255]
GREEN = [0,255,0]
BLUE = [255,0,0]
COLOR = (RED,GREEN,BLUE)


def centroid(contour):
    """Returns the coordinate X and Y of the centroid of the input contour in the form of a tuple"""
    M = cv2.moments(contour)
    if (M['m00'] !=0 ):
        Cx = int(M['m10']/M['m00'])
        Cy = int(M['m01']/M['m00'])
        return(Cx,Cy)


def threshold(img,Hmin=0,Hmax=179,Smin=0,Smax=255,Vmin=0,Vmax=255):
    """convert the img to hsv and apply the desired threshold and returns the thresholded image"""
    HSVImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if Hmin<=Hmax:
        return cv2.inRange(HSVImg, (Hmin,Smin,Vmin), (Hmax,Smax,Vmax))
    else:
        #seuillage de 0 à Hmax
        img_1 = cv2.inRange(HSVImg, (0,Smin,Vmin), (Hmax,Smax,Vmax))
        #seuillage de Hmin à 179
        img_2 = cv2.inRange(HSVImg, (Hmin,Smin,Vmin), (179,Smax,Vmax))
        #ou logique entre les deux
        return np.bitwise_or(img_1, img_2)


def sortContourPerimeter(liste_contour,perimetre_min,perimetre_max):
    """sort the contours and keeps the ones between permitre_min and permitre_max"""
    liste_contour_tries=[]
    for i in range(len(liste_contour)):
        if len(liste_contour[i])>=perimetre_min and len(liste_contour[i])<=perimetre_max:
            #print("contour n° "+str(i))
            liste_contour_tries.append(liste_contour[i])
    return liste_contour_tries

def sortContourSurface(liste_contour,aire_min,aire_max):
    """sort the contours and keeps the ones between permitre_min and permitre_max"""
    liste_contour_tries=[]
    for i in range(len(liste_contour)):
        aire = cv2.contourArea(liste_contour[i])
        if aire >= aire_min and aire <= aire_max :
            liste_contour_tries.append(liste_contour[i])
    return liste_contour_tries

def blur(img):
    """blur the source img and return the result"""
    return(cv2.GaussianBlur(img,(3,3), 0))

def convertToHSV(img):
    """convert the BGR opencv image to HSV colorspace"""
    return(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))

def opening(img,iterations=1):
    """does an opening(erode then dilate, clear little objects) on img with 1 iteration by default""" 
    temp = cv2.erode(img, None, iterations)
    return(cv2.dilate(temp, None, iterations))

def findContours(img):
    """find the contours in the img"""
    return(cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0])


def ptInZone(pttest,Lzone = (180,120,480)):
    """returns a boolean that tells if the point pttest is in the zone"""
    Xmax = Lzone[0]
    Ymin = Lzone[1]
    Ymax = Lzone[2]
    #print("le point testé")
    #print(pttest)
    if pttest == None:
        return 1
    elif pttest[0] < Xmax and pttest[1]< Ymax and pttest[1] > Ymin:
        return 1
    else:
        return 0


## used for trackbars opencv
def nothing(x):
    pass

#routine on one core for the multiprocessing function
def acqCoordinates(return_dict,i,arguments):
    #unpack arguments
    capture = arguments[0]
    display = arguments[1]
    ratio = arguments[2]
    transformMat = arguments[3]
    lTrackbar = arguments[4]
    colorMat = arguments[5]
    auto = arguments[6]
    tolH = arguments[7][0]
    tolS = arguments[7][1]
    tolV = arguments[7][2]
    distPx = 20

    if auto :
        HminR=(colorMat[0, 0]-tolH)%180
        HmaxR=(colorMat[0, 0]+tolH)%180
        VminR=colorMat[0, 2]-tolV
        VmaxR = 255
        SminR = tolS
        SmaxR = 255

        HminG=(colorMat[1, 0]-tolH)%180
        HmaxG=(colorMat[1, 0]+tolH)%180
        VminG=colorMat[1, 2]-tolV
        VmaxG = 255
        SminG = tolS
        SmaxG = 255

        HminB=(colorMat[2, 0]-tolH)%180
        HmaxB=(colorMat[2, 0]+tolH)%180
        VminB=colorMat[2, 2]-tolV
        VmaxB = 255
        SminB = tolS
        SmaxB = 255
    else:
        HminR = lTrackbar[0][0]
        HmaxR = lTrackbar[0][1]
        SminR = lTrackbar[0][2]
        SmaxR = lTrackbar[0][3]
        VminR = lTrackbar[0][4]
        VmaxR = lTrackbar[0][5]

        HminG = lTrackbar[1][0]
        HmaxG = lTrackbar[1][1]
        SminG = lTrackbar[1][2]
        SmaxG = lTrackbar[1][3]
        VminG = lTrackbar[1][4]
        VmaxG = lTrackbar[1][5]

        HminB = lTrackbar[2][0]
        HmaxB = lTrackbar[2][1]
        SminB = lTrackbar[2][2]
        SmaxB = lTrackbar[2][3]
        VminB = lTrackbar[2][4]
        VmaxB = lTrackbar[2][5]




    has_frame, frame = capture.read()
    if not has_frame:
        print("error reading frame on step i"+ str(i))

    #frame = cv2.resize(frame,(int(500*ratio),500))
    frame = cv2.flip(frame, -1)
    correctedFrame = cv2.warpPerspective(frame,transformMat,(600,600))
    centerBackground = np.copy(correctedFrame)


    blurred = blur(correctedFrame)
    thresholdedRed = threshold(blurred,HminR,HmaxR,SminR,SmaxR,VminR,VmaxR)
    thresholdedGreen = threshold(blurred,HminG,HmaxG,SminG,SmaxG,VminG,VmaxR)
    thresholdedBlue = threshold(blurred,HminB,HmaxB,SminB,SmaxB,VminB,VmaxB)
    # thresholdedBlue = opening(thresholdedRed)
    # thresholdedGreen = opening(thresholdedGreen)
    # thresholdedBlue = opening(thresholdedBlue)


    lContourRed = findContours(thresholdedRed)
    lContourGreen = findContours(thresholdedGreen)
    lContourBlue = findContours(thresholdedBlue)
    lContour = [lContourRed, lContourGreen, lContourBlue]
    lCenterRed = []
    lCenterGreen = []
    lCenterBlue = []
    lCenter = [lCenterRed,lCenterGreen,lCenterBlue]
    #print(lContour)
    for i in range (len(lContour)):
       for contour in lContour[i]:
            center = centroid(contour)
            if(not center == None):
                lCenter[i].append(center)
                if display:
                    cv2.circle(centerBackground,center,5,COLOR[i])



    lCenterSortedR = []
    lCenterSortedG = []
    lCenterSortedB = []
    lCenterSorted = [lCenterSortedR,lCenterSortedG,lCenterSortedB]
    for i in range (len(lCenter)):
        for center in lCenter[i]:
            #print(center)
            if not ptInZone(center) : #verifier ce truc
                lCenterSorted[i].append(center)
                if display:
                    cv2.circle(centerBackground,center,10,COLOR[i])




    lCenterSortedZone = [[],[],[]]
    max = 600 -distPx
    min = distPx
    for i in range (len(lCenterSorted)):
        for center in lCenterSorted[i]:
            if center[1]<max:
                lCenterSortedZone[i].append(center)
                if display:
                    cv2.circle(centerBackground,center,15,COLOR[i])

    if display:
        cv2.imshow("thresholdedRed",thresholdedRed)
        cv2.imshow("thresholdedGreen",thresholdedGreen)
        cv2.imshow("thresholdedBlue",thresholdedBlue)
        cv2.imshow("frame",correctedFrame)
        #cv2.imshow("correted",correctedFrame)
        cv2.imshow('window',centerBackground)
    return(lCenter)

