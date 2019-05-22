# coding: utf-8

import socket
import sys

ipAdress = "192.168.4.1"
port = 1111
requestSize = 10000	#Taille de l'objet requete

#Classe d'objet requete
class requestObject():

	def __init__(self, robot, reqType):
		self.reqType = reqType
		self.robot = robot

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

def requeteClient(ip, usedPort, reqObj):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip, usedPort))
	sock.send(wifiFormatInt(reqObj.reqType, 5).encode())
	sock.send(wifiFormatInt(reqObj.robot, 5).encode())
	if(reqObj.reqType == 2):	#Demarrage
		reponse = int(clientsocket.recv(requestSize).decode())
		if(reponse == 1):
			print("OK")
		else:
			print("Pas OK")
	elif(reqObj.reqType == 1):	#Reception des coordonnees
		len1 = int(clientsocket.recv(requestSize).decode())
		for i in range(0, len1):
			print("Liste couleur " + i)
			len2 = int(clientsocket.recv(requestSize).decode())
			for j in range(0, len2):
				print("x" + j + " " + int(clientsocket.recv(requestSize).decode()))
				print("y" + j + " " + int(clientsocket.recv(requestSize).decode()))
	#reponse = sock.recv(requestSize)
	#while(not sys.getsizeof(reponse) == requestSize):
	#	reponse+=sock.recv(requestSize)
	#repObj = pickle.loads(reponse)
	#return repObj

reqObj = requestObject(1, 2)
requeteClient(ipAdress, port, reqObj)
