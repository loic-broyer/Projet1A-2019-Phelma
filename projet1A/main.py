# coding: utf-8

import serverT
import perspective

#parametres de la caméra :
hauteur = 0
alpha = 0
omega = 0
beta0 = 0
gamma0 = 0
xShift = 0
yShift = 0
resoX = 0
resoY = 0

#Paramètres du terrain de jeu (en cm) :
hPalet = 2.5
hGrosPalet = 5
hRobot1 = 0
hRobot2 = 0
hRobotAdv1 = 0
hRobotAdv2 = 0
heigthList = [hRobot1, hRobot2, hRobotAdv1, hRobotAdv2, hPalet, hPalet, hPalet, hGrosPalet]

#paramètres du serveur :
port = 1111

#Registres :
xR1 = 0
yR1 = 0
thetaR1 = 0

xR2 = 0
yR2 = 0
thetaR2 = 0

xR2 = 0
yR2 = 0
thetaR2 = 0

xR2 = 0
yR2 = 0
thetaR2 = 0

red = []
green = []
blue  = []
gold = []

#Code de calibration des paramètres de la caméra ?

#Initialisation
camera = perspective.Camera(hauteur, alpha, omega, beta0, gamma0, xShift, yShift, resoX, resoY)
sock = serverT.initServer(port)

while True:
    #Le code d'acquisition et de traitement de l'image
    
    
    
    #La liste des élements trouvés (element[itemID, {u, v}])
    listeElements = []
    
    for element in listeElements:
        #ID pour designer les objets repérables, dans l'ordre de déclaration des variables
        itemSelector = element[0]
        h = heigthList[itemSelector]
        (u,v) = (ele
    
    #Conversion coordonnées images vers les coordonnées du terrain de jeu
    (x,y) = coordImageToCoordReelle(camera, u, v, h)
    
    #update des registres
    
    #routine serveur (à voir si on arrive a etre synchrone, sinon le faire tourner sur un daemon)
    serverT.routineServer(sock)
    

    
