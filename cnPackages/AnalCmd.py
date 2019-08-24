#!/usr/bin/python3
# -*- coding:Utf-8 -*-
import re


class AnalCmd():
	def __init__(self):
		self.cmdList = {}
		self.cmdList['A']	= "[PLCTH]"											# Action à réaliser
		self.cmdList['F']	= "[0-9]{1,4}"										# Vitesse d'avance outil
		self.cmdList['S']	= "[0-9]{1,4}"										# Vitesse de la broche
		self.cmdList['X1']	= "([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)"				# Coordonnée X du point de départ de l'usinage
		self.cmdList['Y1']	= "([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)"				# Coordonnée Y du point de départ de l'usinage
		self.cmdList['X2']	= "([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)"				# Coordonnée X du point d'arrivée de l'usinage
		self.cmdList['Y2']	= "([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)"				# Coordonnée Y du point d'arrivée de l'usinage
		self.cmdList['I']	= "([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)"				# Coordonnée X du centre d'un cercle ou arc
		self.cmdList['J']	= "([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)"				# Coordonnée X du centre d'un cercle ou arc
		self.cmdList['R']	= "([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)"				# Valeur de rayon du cercle ou de l'arc de cercle

		self.varList = {}

	def loadLine(self, line):
		status = False
		self.varList.clear()
		cmdTup = line.split()
		for cmd in cmdTup:
			ret = re.findall("(\w+)=([0-9A-Za-z.]+)", cmd)	# Contrôle du format de la commande
			if (ret is None):
				cause = "Format invalide: {}:".format(cmd)
				return(status, cause)						# Erreur de format général de la variable
			nomVar = ret[0][0]								# Extraction du nom de la variable
			valVar = ret[0][1]								# Extraction de la valeur de la variable
			try:
				regx = self.cmdList[nomVar]					# Récupération de l'expression régulière correspondant à la nature de la variable
			except:
				cause = "Nom de variable invalide: {}".format(cmd)
				return(status, cause)	# Erreur sur le nom de la variable
			ret = re.match(regx, valVar)					# Contrôle de validité de la valeur
			if (ret is None):
				cause = "Valeur variable invalide: {}".format(cmd)
				return(status, cause)						# Erreur de format de la variable
			try:
				v = self.varList[nomVar]					# Vérification que la variable n'existe pas déjà initialisée
				cause = "Variable déjà initialisée {}".format(cmd)
				return(status, cause)
			except:
				self.varList[nomVar] = valVar				# Enregistrement de la variable avec sa valeur dans le dico varList
		status = True
		return(status, '')

	def getVar(self, key):
		try:
			v = self.varList[key]
		except:
			status = False
			cause  = "Nom de variable non définie: {}".format(key)
			return(status, cause)
		return(v)

	def dumpVar(self):										# Lister toutes les variables extraites de la ligne de commande
		for key in self.varList:
			print(key, self.varList[key])

if __name__ == "__main__":


	msgList = [
		("A=P X1=0.00 Y1=0.00"),
		("A=P X1=30.00 Y1=80.00"),
		("A=L X1=30.00 Y1=80.00 X2=70.00 Y2=80.00"),
		("A=H X1=70.00 Y1=80.00 X2=90.00 Y2=60.00 I=70.00 J=60.00 R=20.00"),
		("A=L X1=90.00 Y1=60.00 X2=90.00 Y2=40.00"),
		("A=T X1=90.00 Y1=40.00 X2=110.00 Y2=20.00 I=110.00 J=20.00 R=20.00"),
		("A=L X1=110.00 Y1=20.00 X2=150.00 Y2=20.00"),
		("A=T X1=150.00 Y1=20.00 X2=170.00 Y2=40.00 I=150.00 J=40.00 R=20.00"),
		("A=L X1=170.00 Y1=40.00 X2=230.00 Y2=40.00"),
		("A=T X1=230.00 Y1=40.00 X2=230.00 Y2=80.00 I=230.00 J=60.00 R=20.00"),
		("A=L X1=230.00 Y1=80.00 X2=200.00 Y2=80.00"),
		("A=L X1=200.00 Y1=80.00 X2=200.00 Y2=100.00"),
		("A=T X1=200.00 Y1=100.00 X2=110.00 Y2=180.00 I=180.00 J=100.00 R=20.00"),
		("A=L X1=180.00 Y1=120.00 X2=160.00 Y2=120.00"),
		("A=H X1=160.00 Y1=120.00 X2=120.00 Y2=120.00 I=140.00 J=120.00 R=20.00"),
		("A=L X1=120.00 Y1=120.00 X2=100.00 Y2=120.00"),
		("A=T X1=100.00 Y1=120.00 X2=80.00 Y2=100.00 I=100.00 J=100.00 R=20.00"),
		("A=L X1=80.00 Y1=100.00 X2=60.00 Y2=100.00"),
		("A=L X1=60.00 Y1=100.00 X2=60.00 Y2=120.00"),
		("A=L X1=60.00 Y1=120.00 X2=30.00 Y2=120.00"),
		("A=T X1=30.00 Y1=120.00 X2=30.00 Y2=80.00 I=30.00 J=100.00 R=20.00")
	]

	ac = AnalCmd()
	for line in msgList:
		print(line)
		r = ac.loadLine(line)
		status = r[0]
		cause  = r[1]
		if (r[0] is False):
			print("loadLine: {}".format(cause))
			continue

#		ac.dumpVar()

		print('getvar[A]:', ac.getVar('A'))




