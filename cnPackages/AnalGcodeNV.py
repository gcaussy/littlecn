#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
from tkinter.filedialog import askopenfilename
from math import *
import sys
import re

class AnalSyntaxGcode(object):
	def __init__(self):
		self.fName = ""
		self.nbErr = 0
		self.cmdsPrimList = []
		self.atm = [
# A Axe A rotatif de la machine (4ème axe)
# B Axe B de la machine
# C Axe C de la machine
# D Valeur de la compensation de rayon d’outil"
			('_001', '[D]',		self.fVarInit, 'i001'),
# E ?
			('_001', '[E]',		self.fVarInit, 'v001'),
# F Vitesse de déplacement de la broche
			('_001', '[F]',		self.fVarInit, 'F001'),
			('F001', '[0-9]',	self.fVarStore, 'F001'),
			('F001', '[.]',		self.fVarStore, 'F002'),
			('F001', '[ \t;]',	self.fVarEnd1, '_001'),
			('F002', '[0-9]',	self.fVarStore, 'F002'),
			('F002', '[ \t;]',	self.fVarEnd1, '_001'),
# G Fonction Générale
			('_001', '[G]',		self.fVarInit, 'G001'),
			('G001', '[0-9]',	self.fVarStore, 'G001'),
			('G001', '[ \t;]',	self.fVarEnd1, '_001'),
			('G001', '[.]',		self.fVarStore, 'G002'),
			('G002', '[0-9]',	self.fVarStore, 'G002'),
			('G002', '[ \t;]',	self.fVarEnd1, '_001'),
# H Index d’offset de longueur d’outil
			('_001', '[H]',		self.fVarInit, 'i001'),
# I Centre du cercle selon X
			('_001', '[I]',		self.fVarInit, 'v001'),
# J Centre du cercle selon Y
			('_001', '[J]',		self.fVarInit, 'v001'),
# K Décalage en Z pour les arcs
			('_001', '[K]',		self.fVarInit, 'v001'),
# L Longueur de la broche
			('_001', '[L]',		self.fVarInit, 'i001'),
# M Fonction auxiliaire
			('_001', '[M]',		self.fVarInit, 'i001'),
# N Numéro de ligne
			('_001', '[N]',		self.fVarInit, 'i001'),
# O Incrément Delta en Z dans un cycle G73, G83
			('_001', '[O]',		self.fVarInit, 'i001'),
# P Tempo utilisée dans les cycles de perçage et avec G4 / Mot clé utilisé avec G10
			('_001', '[P]',		self.fVarInit, 'P001'),
			('P001', '[0-9]',	self.fVarStore, 'P001'),
			('P001', '[.]',		self.fVarStore, 'P002'),
			('P001', '[ \t;]',	self.fVarEnd1, '_001'),
			('P002', '[0-9]',	self.fVarStore, 'P002'),
			('P002', '[ \t;]',	self.fVarEnd1, '_001'),
# Q Incrément Delta en Z dans un cycle G73, G83
			('_001', '[Q]',		self.fVarInit, 'v001'),
# R Rayon d’arc
			('_001', '[R]',		self.fVarInit, 'v001'),
# S Vitesse de rotation de la broche
			('_001', '[S]',		self.fVarInit, 'i001'),
# T Choix du Numéro d’outil
			('_001', '[T]',		self.fVarInit, 'i001'),
# U Axe U de la machine
# V Axe V de la machine
# W Axe W de la machine
# X Axe X
			('_001', '[X]',		self.fVarInit, 'v001'),
# Y Axe Y
			('_001', '[Y]',		self.fVarInit, 'v001'),
# Z Axe Z
			('_001', '[Z]',		self.fVarInit, 'v001'),
# Espace multiple
			('_001', '[ \t;]',	self.fDebug, '_001'),
# ( Début de commentaire selon certains interpréteurs
			('_001', '[(]',		self.fVarInit, '(001'),
			('(001', '[)]',		self.fVarEnd1, '_001'),
			('(001', '*',		self.fVarStore, '(001'),
# # Début de commentaire jusqu'en fin de ligne selon certains interpréteurs
			('_001', '[#]',		self.fDebug, '#001'),
			('#001', '*',		self.fDebug, '#001'),
# ; Début de commentaire jusqu'en fin de ligne selon certains interpréteurs
			('_001', '[;]',		self.fNop, ';001'),
			(';001', '*',		self.fNop, ';001'),
# % Début ou Fin de fichier
			('_001', '[%]',		self.fVarInit, '%001'),
			('%001', '*',		self.fNop, '%001'),
# Tronc commun aux variables X, Y, Z, I, J
			('v001', '[-+]',	self.fVarStore, 'v002'),
			('v001', '[0-9]',	self.fVarStore, 'v003'),
			('v001', '[ \t]',	self.fNop, 'v005'),
			('v002', '[0-9]',	self.fVarStore, 'v003'),
			('v003', '[0-9]',	self.fVarStore, 'v003'),
			('v003', '[.]',		self.fVarStore, 'v004'),
			('v003', '[ \t;]',	self.fVarEnd1, '_001'),
			('v003', '@',		self.fVarEnd2, '_001'),
			('v004', '[0-9]',	self.fVarStore, 'v004'),
			('v004', '[ \t;]',	self.fVarEnd1, '_001'),
			('v005', '[ \t]',	self.fNop, 'v005'),
			('v005', '[0-9]',	self.fVarStore, 'v003'),
			('v005', '[-+]',	self.fVarStore, 'v002'),
# Tronc commun aux entiers toujours positifs
			('i001', '[0-9]',	self.fVarStore, 'i001'),
			('i001', '[ \t;]',	self.fVarEnd1, '_001'),
		]

		self.var = {}

		self.etatCourant = '_001'
		self.codeVar = ''


	def fDebug(self, car):
		print('fDebug --> Etat courant= {}, car=[{}]'.format(self.etatCourant, car))
		return(True)

	def fNop(self, car):
		print('fNop', self.codeVar, "=", self.var[self.codeVar])

	def fVarInit(self, car):
		self.var[car] = ''										# Création de la variable
#		print('fVarInit', self.codeVar)

	def fVarStore(self, car):
		self.var[self.codeVar] += car							# Création de la variable de type str
#		print('fVarStore', self.codeVar, "=", self.var[self.codeVar])

	def fVarEnd1(self, car):
		print('fVarEnd1', self.codeVar, "=", self.var[self.codeVar])

	def fVarEnd2(self, car):
		print('fVarEnd2', self.codeVar, "=", self.var[self.codeVar])


	def openFile(self, st, tr, cm):
		self.fName = askopenfilename()
		try:
			file = open(self.fName, "r")
		except:
			print("Nom de fichier \"{}\" inconnu".format(self.fName))
			return

		st.clear()
		cm.clear()
		self.nbErr = 0
		self.cmdsPrimList.clear()
		tr.insertLine("Fichier = {}\n".format(self.fName), "noir")

		while (True):
			lineFile = file.readline()									# Lecture d'une ligne du fichier G-code en cours
			lineFile = lineFile.strip()									# Supprimer le caractère de fin
			st.insertLine(lineFile, "gris")								# Visualisation de la ligne à traiter

			lg = len(lineFile)											# lg = nombre caractères dans la ligne en cours
			if (lg == 0):
				continue												# Eliminer la ligne
			i = 0														# Index pour parcourir la ligne
			self.etatCourant = '_001'									# Réinitialisation de l'état courant
			while (i < lg):												# Balayage de la ligne Gcode en cours
				car = lineFile[i]										# Lire caractère par caractère
				if (self.etatCourant == '_001'):
					self.codeVar = car
				r = self.searchAtm(car)									# Rechercher ds l'automate la correspondance Etat/car
				if (r[0] == 'ok'):										# Si retour = trouvé
					r[1](car)											# Lancer la fonction à exécuter
					self.etatCourant = r[2]								# Enregistrer le nouvel état
				else:
					print("Erreur 255: car=[{}] in {}".format(car, lineFile))
				i += 1															# Passer au caractère suivant
			if (self.etatCourant != '_001'):
				self.fVarEnd1(car)

		return

	def searchAtm(self, char):
		for line in self.atm:
			etat1 = line[0]
			regx  = line[1]
			fct   = line[2]
			etat2 = line[3]
			if (self.etatCourant != etat1):
				continue									# Continuer à balayer la table
			if (regx == '*'):								# Dans ce cas on accepte tous les caractères
				return('ok', fct, etat2)
			ret = re.match(regx, char)						# Controler le caractère avec la description de l'expression régulière
			if (ret is not None):							# Si trouvé :
				return('ok', fct, etat2)					# 	retour avec la fonction à exécuter et le nouvel état dans l'automate

		return('ko')										# Si non trouvé, il y a une erreur de description dans l'automate

# Programme principal
# ===================

if __name__ == "__main__":

	class PrintGcode(object):
		def __init__(self):
			pass

		def insertLine(self, text, color, flag = None):
			msg = text.strip()
			if (msg != ""):
				print(msg)

		def clear(self):
			print("------------------- DEBUT -----------------------")

	w = Tk()
	w.title('AnalSyntaxGcode')
	print('TEST ANALYSE GCODE NEW VERSION')

	st = PrintGcode()
	asg = AnalSyntaxGcode()
	btn1 = Button(w, text = "Test", command = lambda arg1 = st, arg2 = st, arg3 = st: asg.openFile(arg1, arg2, arg3))
	btn1.pack()
#	btn2 = Button(w, text = "Get", command = getResult)
#	btn2.pack()

	w.mainloop()
	print("END")
