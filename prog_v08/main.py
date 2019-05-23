## imports from other files ##
from fonctions import *
from fonctions4pointsref import *
from multiprocessor import *
from server import *
## settings ##

auto = 0
display = 1


## init ##

#init réseau
ipExperience = 8
port = 1111 
socket = initServer(port)

# specify what you want to capture: 0 is the default webcam or "path to file"
capture = cv2.VideoCapture(0)
_,frame = capture.read()
# compute the aspect ratio of a frame in order to resize later if needed
ratio = frame.shape[1]/frame.shape[0]
# variable that keeps track of wether the game has started or not
gameStart = 0
#not used in the final version dictionnary that will keep the results (list of centers or pads)
dictRes = dict()





#trackbars and display
cv2.namedWindow('trackbar')
cv2.namedWindow('autoColor')
cv2.createTrackbar('aireMin','trackbar',0,10000,nothing)
cv2.createTrackbar('aireMax','trackbar',0,10000,nothing)
cv2.createTrackbar('periMin','trackbar',0,10000,nothing)
cv2.createTrackbar('periMax','trackbar',0,10000,nothing)
#Red
cv2.createTrackbar('HminR','trackbar',0,179,nothing)
cv2.createTrackbar('HmaxR','trackbar',0,179,nothing)
cv2.createTrackbar('SminR','trackbar',0,255,nothing)
cv2.createTrackbar('SmaxR','trackbar',0,255,nothing)
cv2.createTrackbar('VminR','trackbar',0,255,nothing)
cv2.createTrackbar('VmaxR','trackbar',0,255,nothing)
#Green
cv2.createTrackbar('HminG','trackbar',0,179,nothing)
cv2.createTrackbar('HmaxG','trackbar',0,179,nothing)
cv2.createTrackbar('SminG','trackbar',0,255,nothing)
cv2.createTrackbar('SmaxG','trackbar',0,255,nothing)
cv2.createTrackbar('VminG','trackbar',0,255,nothing)
cv2.createTrackbar('VmaxG','trackbar',0,255,nothing)
#Blue
cv2.createTrackbar('HminB','trackbar',0,179,nothing)
cv2.createTrackbar('HmaxB','trackbar',0,179,nothing)
cv2.createTrackbar('SminB','trackbar',0,255,nothing)
cv2.createTrackbar('SmaxB','trackbar',0,255,nothing)
cv2.createTrackbar('VminB','trackbar',0,255,nothing)
cv2.createTrackbar('VmaxB','trackbar',0,255,nothing)

#auto threshold adjust margins
cv2.createTrackbar("tolH","autoColor",20,40,lambda x: None)
cv2.createTrackbar("tolS","autoColor",40,80,lambda x: None)
cv2.createTrackbar("tolV","autoColor",40,80,lambda x: None)



## loop before the game starts ##
while not gameStart:
    (transformMat, colorMat) = fonctions4pointsref(capture,socket,ipExperience,port)
    



## main loop ##

while 1:
    #trackbars
    #Red
    HminR = cv2.getTrackbarPos('HminR','trackbar')
    HmaxR = cv2.getTrackbarPos('HmaxR','trackbar')
    SminR = cv2.getTrackbarPos('SminR','trackbar')
    SmaxR = cv2.getTrackbarPos('SmaxR','trackbar')
    VminR = cv2.getTrackbarPos('VminR','trackbar')
    VmaxR = cv2.getTrackbarPos('VmaxR','trackbar')
    #Green
    HminG = cv2.getTrackbarPos('HminG','trackbar')
    HmaxG = cv2.getTrackbarPos('HmaxG','trackbar')
    SminG = cv2.getTrackbarPos('SminG','trackbar')
    SmaxG = cv2.getTrackbarPos('SmaxG','trackbar')
    VminG = cv2.getTrackbarPos('VminG','trackbar')
    VmaxG = cv2.getTrackbarPos('VmaxG','trackbar')
    #Blue
    HminB = cv2.getTrackbarPos('HminB','trackbar')
    HmaxB = cv2.getTrackbarPos('HmaxB','trackbar')
    SminB = cv2.getTrackbarPos('SminB','trackbar')
    SmaxB = cv2.getTrackbarPos('SmaxB','trackbar')
    VminB = cv2.getTrackbarPos('VminB','trackbar')
    VmaxB = cv2.getTrackbarPos('VmaxB','trackbar')

    tolH = cv2.getTrackbarPos("tolH","autoColor")
    tolS = cv2.getTrackbarPos("tolS","autoColor")
    tolV = cv2.getTrackbarPos("tolV","autoColor")

    lAuto = (tolH,tolS,tolV)
    lTrackbar = [[HminR,HmaxR,SminR,SmaxR,VminR,VmaxR],[HminG,HmaxG,SminG,SmaxG,VminG,VmaxG],[HminB,HmaxB,SminB,SmaxB,VminB,VmaxB]]

    ## press p to play the video and process, doesnt work on raspi ##
    key = cv2.waitKey(1)
    lCenter = acqCoordinates(dictRes,0,(capture,display,ratio,transformMat,lTrackbar, colorMat, auto,lAuto))
    
    #envoi de la liste des centres sur le réseau
    envoiDesCoordonnees(sock,cList)




    # routineServer(sock)
    if key == 27:
        break


cv2.destroyAllWindows()
capture.release()
