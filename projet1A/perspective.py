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


    #Calcule les angles alpha et omega sachant les coordonnées réelles et sur l'image d'un point.
    def computeOrientation(self,deltaH,u,v,xi,yi):
        x = (u*(2.0/self.resoX) - 1) *self.t_beta0
        y = 1
        z = (v*(2.0/self.resoY) - 1) *self.t_gamma0
	alpha = -3.14
	max = 1000
	omega_opt=0
	alpha_opt=0
	while alpha <= 3.14:
	    cos_a = math.cos(alpha)
	    sin_a = math.sin(alpha)
	    a = x + y*cos_a - z*sin_a
	    b = x - y*cos_a + z*sin_a
	    c = (xi+yi)*(y*sin_a + z*cos_a) / deltaH
	    a2 = a**2
	    b2 = b**2
	    c2 = c**2
	    sin_o = (c*b + math.sqrt(c2 * b2 - (b2 + a2)*(c2-a2))) / (a2+b2)
	    if sin_o > 1 or sin_o < -1:
	        sin_o = (c*b - math.sqrt(c2 * b2 - (b2 + a2)*(c2-a2))) / (a2+b2)
	        print("zbu")
	    o = math.arcsin(sin_o)
	    cos_o = math.cos(o)
	    x_calc = deltaH*(cos_o*x - sin_o*cos_a*y + sin_o*sin_a*z) / (sin_a*y+cos_a*z)
	    y_calc = deltaH*(sin_o*x + cos_o*cos_a*y - cos_o*sin_a*z) / (sin_a*y+cos_a*z)
	    dist = math.sqrt((x_calc-xi)**2 + (y_calc-yi)**2)
	    if dist < max:
	        max = dist
		omega_opt = o
		alpha_opt = alpha
	    alpha = alpha+0.1
	alpha=alpha_opt-0.1
	max = 1000
	omega_opt2=0
	alpha_opt2=0
	while alpha < alpha_opt + 0.1:
	    cos_a = math.cos(alpha)
	    sin_a = math.sin(alpha)
	    a = x + y*cos_a - z*sin_a
	    b = x - y*cos_a + z*sin_a
	    c = (xi+yi)*(y*sin_a + z*cos_a) / deltaH
	    a2 = a**2
	    b2 = b**2
	    c2 = c**2
	    sin_o = (c*b + math.sqrt(c2 * b2 - (b2 + a2)*(c2-a2))) / (a2+b2)
	    if sin_o > 1 or sin_o < -1:
	        sin_o = (c*b - math.sqrt(c2 * b2 - (b2 + a2)*(c2-a2))) / (a2+b2)
	        print("zbu")
	    o = math.arcsin(sin_o)
	    cos_o = math.cos(o)
	    x_calc = deltaH*(cos_o*x - sin_o*cos_a*y + sin_o*sin_a*z) / (sin_a*y+cos_a*z)
	    y_calc = deltaH*(sin_o*x + cos_o*cos_a*y - cos_o*sin_a*z) / (sin_a*y+cos_a*z)
	    dist = math.sqrt((x_calc-xi)**2 + (y_calc-yi)**2)
	    if dist < max:
	        max = dist
		omega_opt2 = o
		alpha_opt2 = alpha
	    alpha = alpha+0.1
	return omega_opt2, alpha_opt2
        
<<<<<<< HEAD

def coordImageToCoordReelle(cam, u, v, h):
    """coordImageToCoordReelle(cam, u, v, h) : Transforme les coordonnees en pixel sur l'image d'un point correspondant à une balise ou un palet en coordonnees reelles dans le plan de jeu.
    u et v les coordonnees du point sur l'image, h la hauteur de la balise recherchee (palet ou robot), camera l'objet caméra"""
=======
def coordImageToCoordReelle(cam, u, v, h):
"""coordImageToCoordReelle(cam, u, v, h) : Transforme les coordonnees en pixel sur l'image d'un point correspondant à une balise ou un palet en coordonnees reelles dans le plan de jeu.
u et v les coordonnees du point sur l'image, h la hauteur de la balise recherchee (palet ou robot), camera l'objet caméra"""
>>>>>>> e0ee25ccba27b5591c1c655493f1b3c093e89f48

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
