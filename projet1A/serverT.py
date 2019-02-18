# coding: utf-8 

import socket
import threading
import cv2 as cv
import numpy as np
import pickle
import sys


usedPort = 1111

def sendInfo(num, thread):
    thread.clientsocket.send("wesh".encode())


class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket

    def run(self): 
   
        print("Connexion from %s %s" % (self.ip, self.port))
        num = self.clientsocket.recv(4).decode()
        if num == "1" or num == "2":
            sendInfo(int(num), self)
        else:
            print("Erreur : Numéro de robot inconnu")
            self.clientsocket.send("error".encode())


class StreamThread(threading.Thread):

    def __init__(self, ip, port, clientsocket, stream):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        self.stream = stream

    def run(self): 
        data_str = pickle.dumps(self.stream)
        self.clientsocket.send(data_str)
        

#Initialisation
def initServer(port):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", port))
    print("Server is ready")
    return sock
    
#Routine
def routineServer(sock):
    
    sock.listen(10)
    (clientsocket, (ip, port)) = sock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()

#Redirection de stream (stream un objet quelconque) : a vocation de remplacer routineServer pour la generaliser
def stream(sock, stream):
    sock.listen(10)
    (clientsocket, (ip, port)) = sock.accept()
    newthread = StreamThread(ip, port, clientsocket, stream)
    newthread.start()

    
#Programme de test
#sock = initServer(usedPort)
#while True:
#    routineServer(sock)

#Programme de test du stream
cap = cv.VideoCapture(0)
sock = initServer(usedPort)

while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    stream(sock, gray)
cap.release()
cv.destroyAllWindows()




