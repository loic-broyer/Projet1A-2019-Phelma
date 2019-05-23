#coding utf-8

import socket
import pickle
import sys

usedPort = 1111
requestSize = 4	#Taille de l'objet requete

#Classe d'objet requete
class requestObject():

	def __init__(self, robot, reqType):
		self.reqType = reqType
		self.robot = robot

#Initialisation (ouverture de la socket)
def initServer(port):
    
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(("", port))
	print("Server is ready")
	return sock

#i le nombre à envoyer et size la taille du buffer (1 = 0001 pour size = 4)
def wifiFormatInt(i, size):
	string = str(i)
	if(len(string) > size):
		print("Erreur : int trop grand")
	elif(len(string) < size):
		diff = size - len(string)
		for k in range(0, diff):
			string = "0" + string
	return string

#[[[x,y],[x,y]], [liste bleue], [liste verte]]
def envoiDesCoordonnees(sock, cList):
	len1 = len(cList)
	sock.send(wifiFormatInt(len1, 5).encode())
	for i in range(0,len1):	#Les listes de couleur
		len2 = len(cList[i])
		sock.send(wifiFormatInt(len2, 5).encode())
		for j in range(0,len2):
			sock.send(wifiFormatInt(cList[i][j][0], 5).encode())
			sock.send(wifiFormatInt(cList[i][j][1], 5).encode())

#Routine (écoute des requetes reseau), cList la liste des coordonnées
def routineServer(sock, cList):
    
	#Ecoute reseau
	sock.listen(10)
	(clientsocket, (ip, port)) = sock.accept()
	print("Connexion from %s %s" % (ip, port))
	#Reception de l'objet requete
	reqObj = requestObject(0,0)
	data = clientsocket.recv(requestSize)
	reqObj.reqType = int(data.decode())
	data = clientsocket.recv(requestSize)
	reqObj.robot = int(data.decode())
	#Reponse à la requete
	if(reqObj.reqType == 0):	#Pull score
		print("Fonction pas encore faite ou ne sera jamais faite mdr")
	elif(reqObj.reqType == 1):	#Pull coords
		envoiDesCoordonnees(sock, cList)
	else:
		print("Erreur : Code requete inconnu.")

#Routine d'attente (requiert un spam constant du robot pour marcher)
def netWaitForStart(sock, ipExperience, port):
	sock.listen(10)
	(clientsocket, (ip, port)) = sock.accept()
	print("Connexion from %s %s" % (ip, port))
	#Reception de l'objet requete
	reqObj = requestObject(0,0)
	data = clientsocket.recv(requestSize)
	reqObj.reqType = int(data.decode())
	data = clientsocket.recv(requestSize)
	reqObj.robot = int(data.decode())
	if(reqObj.reqType == 2):	#Declenchement du protocole de demarrage
		sock.send(wifiFormatInt(1, 5).encode())
		sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ipExperience, port))
		sock.send("START".encode())
		return 1
	else:
		sock.send(wifiFormatInt(0, 5).encode())
		return 0

#main 
#sock = initServer(usedPort)
#while True:
#	routineServer(sock)

