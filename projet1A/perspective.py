#coding: utf-8

import math

#Classe definissant les proprietes principales de la camera et ses getters / setters
class Camera:

    #hauteur la hauteur de la camera, alpha l'angle de la camera par rapport à l'horizontale, omega l'angle de la camera par rapport au terrain de jeu autour de l'axe vertical, beta0 l'angle maximal longitudinal vu par la camera, gamma0 l'angle latitudinal maximal vu par la camera, resoX le nombre de pixels en largeur, resoY le nombre de pixels en hauteur, xShift le decalage en x de la camera par rapport à l'origine, yShift en y
    def __init__(self, hauteur, alpha, omega, beta0, gamma0, xShift, yShift, resoX, resoY):
        self.hauteur = hauteur
        self.alpha = alpha
        self.c_alpha = math.cos(alpha)
        self.s_alpha = math.sin(alpha)
        self.omega = omega
        self.c_omega = math.cos(omega)
        self.s_omega = math.sin(omega)
        self.t_beta0 = math.tan(beta0)
        self.beta0 = beta0
        self.t_gamma0 = math.tan(gamma0)
        self.gamma0 = gamma0
        self.xShift = xShift
        self.yShift = yShift
        self.resoX = resoX
        self.resoY = resoY
        
    #getters
    def getPosition(self):
        return self.xShift, self.yShift, self.hauteur
        
    def getOrientation(self):
        return self.alpha, self.omega
        
    def getFoV(self):
        return self.beta0, self.gamma0
        
    def getResolution(self):
        return self.resoX, self.resoY
        
    #setters
    def setPosition(self, x, y, h):
        self.xShift = x
        self.yShift = y
        self.hauteur = h
        
    def setOrientation(alpha, omega):
        self.alpha = alpha
        self.c_alpha = math.cos(alpha)
        self.s_alpha = math.sin(alpha)
        self.omega = omega
        self.c_omega = math.cos(omega)
        self.s_omega = math.sin(omega)
        

def coordImageToCoordReelle(cam, u, v, h):
    """coordImageToCoordReelle(cam, u, v, h) : Transforme les coordonnees en pixel sur l'image d'un point correspondant à une balise ou un palet en coordonnees reelles dans le plan de jeu.
    u et v les coordonnees du point sur l'image, h la hauteur de la balise recherchee (palet ou robot), camera l'objet caméra"""

    #Conversion des coordonnées image en vecteur direction (attention il faut tenir compte du fait que l'image est retournée ou pas)
    x = (u*(2.0/cam.resoX) - 1) *cam.t_beta0
    y = 1
    z = (v*(2.0/cam.resoY) - 1) *cam.t_gamma0
    #Rotation du vecteur direction de alpha et omega
    a = cam.c_omega*x - cam.s_omega*cam.c_alpha*y + cam.s_omega*cam.s_alpha*z
    b = cam.s_omega*x + cam.c_omega*cam.c_alpha*y - cam.c_omega*cam.s_alpha*z
    c = cam.s_alpha*y + cam.c_alpha*z
    #Calcul du point d'intersection avec le plan z = -deltaH
    deltaH = cam.hauteur - h
    xi = deltaH * a/c
    yi = deltaH * b/c
    #coordonnees translatees vers l'origine
    xTrans = xi + cam.xShift
    yTrans = yi + cam.yShift
    return xTrans, yTrans
    
#programme de test
#cam = Camera(18, 1.016, 0, 0.32, 0.54, 0, -4.25, 1836, 3264)
#(xr, yr1) = coordImageToCoordReelle(cam, 0, 2540, 0)
#print(yr1)
#(xr, yr2) = coordImageToCoordReelle(cam, 0, 42, 2)
#print(yr2)
#print(yr1-yr2)
