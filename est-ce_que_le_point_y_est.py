import numpy as np

def distance(pta,ptb):
    return(np.sqrt((pta[0]-ptb[0])**2+(pta[1]-ptb[1])**2))

def moyenne(pta,ptb,ptc):
    pt=[]
    pt.append((pta[0]+ptb[0]+ptc[0])/3)
    pt.append((pta[1]+ptb[1]+ptc[1])/3)
    return pt

def point_commun(liste1,liste2,liste3,tolérance):
    communs=[]
    for L1 in range(len(liste1)):
        for L2 in range(len(liste2)):
            for L3 in range (len(liste3)):
                if (distance(liste1[L1],liste2[L3])<tolerance):
                    if (distance(liste2[L2],liste3[L3])<tolerance):
                        communs.append(moyenne(liste1[L1],liste2[L2],liste3[L3]))
    return(communs)
