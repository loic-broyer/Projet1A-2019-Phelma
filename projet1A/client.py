# coding: utf-8

import socket
import sys
import pickle

ipAdress = "10.42.0.66"
port = 1111
robot = 1
requestSize = 10000	#Taille de l'objet requete

#Classe d'objet requete
class requestObject():

	def __init__(self, robot, reqType, argument):
		self.reqType = reqType
		self.robot = robot
		self.argument = argument

def requeteClient(ip, usedPort, reqObj):
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip, usedPort))
	data_str = pickle.dumps(reqObj)
	sock.send(data_str)
	reponse = sock.recv(requestSize)
    	while(not sys.getsizeof(reponse) == requestSize):
        	reponse+=sock.recv(requestSize)
    	repObj = pickle.loads(reponse)
	return repObj
