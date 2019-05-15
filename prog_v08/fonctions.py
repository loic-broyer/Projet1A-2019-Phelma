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

def blur(img):
    #blur the source img and return the result
    return(cv2.GaussianBlur(img,(7,7), 0))

def convertToHSV(img):
    return(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))

def opening(img,iterations=1):
    temp = cv2.erode(img, None, iterations)
    return(cv2.dilate(temp, None, iterations))

def findContours(img):
    return(cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE))


def ptInZone(pttest,Lpt = [[0, 120], [180, 120], [180, 480], [0, 480]]):
    if(pttest[0]<=Lpt[1][0]):
       return(0)##indique que pas dans le rectangle
    if (pttest[0]<=Lpt[0][0]):
       return(0)
    if (pttest[1]<=Lpt[2][1]):
       return(0)
    if (pttest[1]>=Lpt[1][1]):
        return(0)
    return(1)

## used for trackbars opencv
def nothing(x):
    pass

#routine on one core for the multiprocessing function
# arguments is a tuple arguments[0] = capture 
# arguments[1] = display (boolean to turn on or off monitoring)
def acqCoordinates(return_dict,i,arguments):
    capture = arguments[0]
    display = arguments[1]
    ratio = arguments[2]
    transformMat = arguments[3]
    lTrackbar = arguments[4]


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
    #cv2.imshow("correted",correctedFrame)
    centerBackground = np.copy(correctedFrame)

    cv2.imshow("frame",correctedFrame)

    blurred = blur(correctedFrame)
    HSV = convertToHSV(blurred)

    thresholdedRed = threshold(HSV,HminR,HmaxR,SminR,SmaxR,VminR,VmaxR)
    thresholdedGreen = threshold(HSV,HminG,HmaxG,SminG,SmaxG,VminG,VmaxR)
    thresholdedBlue = threshold(HSV,HminB,HmaxB,SminB,SmaxB,VminB,VmaxB)

#determiner et ajuster les seuils
    cv2.imshow("thresholdedRed",thresholdedRed)
    opening(thresholdedRed)
    opening(thresholdedGreen)
    opening(thresholdedBlue)


    lContourRed,_ = cv2.findContours(thresholdedRed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lContourGreen,_ = cv2.findContours(thresholdedGreen, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lContourBlue,_ = cv2.findContours(thresholdedBlue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lContour = [lContourRed, lContourGreen, lContourBlue]
    lCenterRed = []
    lCenterGreen = []
    lCenterBlue = []
    lCenter = [lCenterRed,lCenterGreen,lCenterBlue]
    for i in range (len(lContour)):
       for contour in lContour[i]:
            #print(contour)
            #print("\n")
            #print(type(contour))
            #print("\n")
            center = centroid(contour)
            lCenter[i].append(center)

            if display:
                cv2.circle(centerBackground,center,5,COLOR[i])
    print("lenght of l center red")
    print(len(lCenterRed))
    print("lenght of l center green")
    print(len(lCenterGreen))
    print("length of l center blue")
    print(len(lCenterBlue))

    if display:
        cv2.imshow('window',centerBackground)

    lCentersSorted = []
    # for i in range (len(lCenter)):
    #     for center in lCenter[i]:
    #         if not ptInZone(center) : #verifier ce truc
    #             lCentersSorted.append(center)

    return_dict[0] = lCenter


