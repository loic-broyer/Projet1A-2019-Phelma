#coding utf-8

import socket
import pickle
import sys

usedPort = 1111
requestSize = 10000 #Taille de l'objet requete

#Classe d'objet requete
class requestObject():

    def __init__(self, robot, reqType, argument):
        self.reqType = reqType
        self.robot = robot
        self.argument = argument

#Initialisation (ouverture de la socket)
def initServer(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", port))
    print("Server is ready")
    return sock

#Routine (écoute des requetes reseau)
def routineServer(sock):
    #Ecoute reseau
    sock.listen(10)
    (clientsocket, (ip, port)) = sock.accept()
    print("Connexion from %s %s" % (ip, port))
    #Reception de l'objet requete
    data = sock.recv(requestSize)
    while(not sys.getsizeof(data) == requestSize):
        data+=sock.recv(requestSize)
    reqObj = pickle.loads(data)
    #Reponse à la requete
    if(reqObj.reqType == 0):    #Pull setup status
        data_str = pickle.dumps(gameVariables[0])
        clientsocket.send(data_str)
    elif(reqObj.reqType == 1):  #Push setup status
        gameVariables[0][reqObj.robot] = 1
    elif(reqObj.reqType == 2):  #Pull score
        data_str = pickle.dumps(gameVariables[1])
        clientsocket.send(data_str)
    elif(reqObj.reqType == 3):  #Push score (TODO : voir si on a besoin de controle)
        gameVariables[1] += reqObj.argument
    elif(reqObj.reqType == 4):  #Pull coords
        data_str = pickle.dumps(gameVariables[2])
        clientsocket.send(data_str)
    elif(reqObj.reqType == 5):  #Push coords (TODO : voir si on a besoin de controle)
        gameVariables[2][reqObj.robot] = reqObj.argument
    else:
        print("Erreur : Code requete inconnu.")

#Routine d'attente (requiert un spam constant du robot pour marcher)
def netWaitForStart(sock):
    sock.listen(10)
    (clientsocket, (ip, port)) = sock.accept()
    print("Connexion from %s %s" % (ip, port))
    #Reception de l'objet requete
    data = sock.recv(requestSize)
    while(not sys.getsizeof(data) == requestSize):
        data+=sock.recv(requestSize)
        reqObj = pickle.loads(data)
    if(reqObj.reqType == 6):
        return 1
    else:
        return 0

#main
#sock = initServer(usedPort)
#while True:
#   routineServer(sock)

