import numpy as np

def distance(long1,larg1,long2,larg2):
    return(np.sqrt((larg1-larg2)**2+(long1-long2)**2))

def init_correction_robot(longueur,largeur):
    abaque=[] ## il s'agit d'une liste dans laquelle on répertorie des points
    ## de mesure sous la forme: [abscisse,ordonnée,décalage en abscisse,décalage en ordonnée]
    ##l'algorithme doit chercher lui-même le point de mesure le plus proche pour savoir quelle correction appliquer

    correction=np.zeros((longueur,largeur,2),[])
    ## cette matrice aux dimension des images traitées va être complétée avec les coordonnées des points de mesure les plus proches:
    ##Ainsi, on aura plus qu'à consulter le point de même coordonnées dans cette matrice pour savoir la correction à apporter à la position du robot sur l'imageacquise

    for long in range(longueur):
        for larg in range (largeur):
            
            mindistance=distance(long,larg,abaque[0][0],abaque[0][1])
            ireference=0
            for i in range (len(abaque)):
                if (distance(long,larg,abaque[0][0],abaque[0][1])<mindistance):
                    ireference=i
                    mindistance=distance(long,larg,abaque[0][0],abaque[0][1])

            correction[long][larg][0]=abaque[ireference][2]
            correction[long][larg][1]=abaque[ireference][3]
    ## nous n'avons complété que les points pour lesquels nous avons des mesures, il faut maintenant attribuer une valeur aux autres points
    ## idée: on va compléter avec des moyennes pondérées par la distance

    for long in range(longueur):
        for larg in range (largeur):
            abscissenegmin=0
            abscisseposmin=0
            ordonnéenegmin=0
            ordonnéeposmin=0
            
            while(contour[longueur-abscissenegmin][largeur][0]==0):
                abscissenegmin+=1
            while(contour[longueur+abscisseposmin][largeur][0]==0):
                abscisseposmin+=1            
            while(contour[longueur][largeur-ordonnéenegmin][0]==0):
                ordonnéenegmin+=1
            while(contour[longueur][largeur+ordonnéeposmin][0]==0):
                ordonnéenegmin+=1

            correction[long][larg][0]=(correction[long-abscissenegmin][larg][0]+correction[long+abscisseposmin][larg][0])/(abscisseposmin-abscissenegmin)
            correction[long][larg][1]=(correction[long][larg-ordonnéenegmin][1]+correction[long][larg+ordonnéeposmin][1])/(ordonnéeposmin-ordonnéenegmin)
            
    return(correction)
