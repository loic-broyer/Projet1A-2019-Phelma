#coding: utf-8

import server.py as server
import perspective.py as persp
import multiprocessor.py as mproc

#Definition Camera (demander à Loïc pour les variables)
cam = persp.Camera(hauteur, 0, 0, beta0, gamma0, xShift, yShift, resoX, resoY)

#Calibration caméra (demander à Loïc pour les variables)
(omega, alpha) = cam.computeOrientation(deltaH, u, v, xi, yi)
cam.setOrientation(alpha, omega)

#Init reseau (port à definir)
sock = server.initServer(port)

#Ecoute réseau pour le départ
server.netWaitForStart()

#Split et join des cores (core le nbr de cores dispo, fonction la fonction à appeler, arguments ses arguments)
mproc.runMultiCore(core, fonction, arguments)

#Conversion des coordonnées des robots
(xr, yr) = persp.coordImageToCoordReelle(cam, u, v, h)

#Routine reseau (sock retourné par l'init)
server.routineServer(sock)
