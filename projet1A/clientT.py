# coding: utf-8

import socket
import sys
import cv2 as cv
import numpy as np
import pickle

#Pour le reseau local, il semblerait que l'ip par defaut du routeur (serveur heberge dessus) soit 10.42.0.1
ipAdress = "10.42.0.66"
port = 1111
robot = 1
imgSize = 307395

#Requete
def requeteClient(ip, usedPort, rob):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, usedPort))
    sock.send(str(rob).encode())
    reponse = sock.recv(100).decode()
    if(reponse == "error"):
        print("Error from server")
    else:
        print(reponse)
    sock.close()
    
def requeteStream(ip, usedPort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, usedPort))
    data = sock.recv(imgSize)
    while(not sys.getsizeof(data) == imgSize):
        data+=sock.recv(imgSize)
    var = pickle.loads(data)
    return var
    
#while True:
 #   requeteClient(ipAdress, port, robot)

#Programme de test du stream
while(True):
    var = requeteStream(ipAdress, port)
    cv.imshow('frame', var)
    if cv.waitKey(100) & 0xFF == ord('q'):
        break
  
