#coding: utf-8

def calculOrientationRobot(directeur, pt1, pt2):
    x_moy_pt = (pt1.x + pt2.x) / 2
    y_moy_pt = (pt1.y + pt2.y) / 2
    dir_x = directeur.x - x_moy_pt
    dir_y = directeur.y - y_moy_pt
    return dir_x, dir_y

def calculBarycentreRobot(directeur, pt1, pt2):
    x_moy = (directeur.x + pt1.x + pt2.x) / 3
    y_moy = (directeur.y + pt1.y + pt2.y) / 3
    return x_moy, y_moy
