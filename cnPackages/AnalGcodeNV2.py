#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
from tkinter.filedialog import askopenfilename
from math import *
import sys
import re

ABS, REL = True, False					# Mode de calcul des positionnements
NO, POS, LINE, ARC = 0, 1, 2, 3			# Type de forme à réaliser POS = déplacement de positionnement seulement
GO, STOP = True, False					# Action de déplacement en XYZ
HORAIRE, TRIGO = True, False			# Sens de rotation de la broche

class AnalSyntaxGcode(object):
	def __init__(self):

#	Liste des commandes Gcode "connues" et classées selon leurs utilisations

		self.cmdList = {}

		self.cmdList['N'] = (self.fctNone,	"Numéro de ligne de commandes Gcode")
		self.cmdList['%'] = (self.fctNone,	"Début ou Fin de fichier")

		self.cmdList['G'] = (self.fctNone,	"Fonction Générale de type Gn, Gnn ou Gnn.n")
		self.cmdList['M'] = (self.fctNone,	"Fonction auxiliaire de type Mn, Mnn")

		self.cmdList['A'] = (self.fctNone,	"Axe A rotatif de la machine (4ème axe)")
		self.cmdList['B'] = (self.fctNone,	"Axe B de la machine")
		self.cmdList['C'] = (self.fctNone,	"Axe C de la machine")
		self.cmdList['U'] = (self.fctNone,	"Axe U de la machine")
		self.cmdList['V'] = (self.fctNone,	"Axe V de la machine")
		self.cmdList['W'] = (self.fctNone,	"Axe W de la machine")
		self.cmdList['X'] = (self.fctNone,	"Axe X de la machine")
		self.cmdList['Y'] = (self.fctNone,	"Axe Y de la machine")
		self.cmdList['Z'] = (self.fctNone,	"Axe Z de la machine")
		self.cmdList['I'] = (self.fctNone,	"Centre du cercle selon X")
		self.cmdList['J'] = (self.fctNone,	"Centre du cercle selon Y")
		self.cmdList['R'] = (self.fctNone,	"Rayon d’arc")
		self.cmdList['K'] = (self.fctNone,	"Décalage en Z pour les arcs ")

		self.cmdList['T'] = (self.fctNone,	"Choix du Numéro d’outil")
		self.cmdList['F'] = (self.fctNone,	"Vitesse de déplacement de la broche")
		self.cmdList['H'] = (self.fctNone,	"Index d’offset de longueur d’outil")
		self.cmdList['L'] = (self.fctNone,	"Longueur de la broche")
		self.cmdList['D'] = (self.fctNone,	"Valeur de la compensation de rayon d’outil")
		self.cmdList['S'] = (self.fctNone,	"Vitesse de rotation de la broche")

		self.cmdList['O'] = (self.fctNone,	"Incrément Delta en Z dans un cycle G73, G83")
		self.cmdList['P'] = (self.fctNone,	"Tempo utilisée dans les cycles de perçage et avec G4 / Mot clé utilisé avec G10")
		self.cmdList['Q'] = (self.fctNone,	"Incrément Delta en Z dans un cycle G73, G83")

		# Liste réduite des commandes Gcode G et M implémentées
		self.gmList = {}
		self.gmList['G0']	= (self.fctNone,	"Déplacement rapide en ligne droite")
		self.gmList['G00']	= (self.fctNone,	"Déplacement rapide en ligne droite")
		self.gmList['G01']	= (self.fctG01,		"Déplacement en ligne droite à vitesse programmée")
		self.gmList['G02']	= (self.fctG02,		"Interpolation circulaire(sens horaire)")
		self.gmList['G03']	= (self.fctG03,		"Interpolation circulaire(sens trigo)")
		self.gmList['G17']	= (self.fctNone,	"Sélection du plan X-Y")
		self.gmList['G70']	= (self.fctNone,	"Entrée des données en pouce")
		self.gmList['G71']	= (self.fctNone,	"Entrée des données en métrique")
		self.gmList['G90']	= (self.fctG90,		"Programmation absolue")
		self.gmList['G91']	= (self.fctG91,		"Programmation relative")

		self.gmList['M0']	= (self.fctM0,		"Arrêt programme")
		self.gmList['M2']	= (self.fctNone,	"Fin de programme")
		self.gmList['M3']	= (self.fctM03,		"Rotation broche sens horaire")
		self.gmList['M5']	= (self.fctM05,		"Arrêt de broche")
		self.gmList['M6']	= (self.fctNone,	"Changement outil")
		self.gmList['M9']	= (self.fctNone,	"Arrosage")

		self.gmList['M00']	= (self.fctNone,	"Arrêt programme")
		self.gmList['M01']	= (self.fctNone,	"Arrêt conditionnel")
		self.gmList['M02']	= (self.fctNone,	"Fin de programme")
		self.gmList['M03']	= (self.fctM03,		"Rotation broche sens horaire")
		self.gmList['M04']	= (self.fctM04,		"Rotation broche Sens antihoraire")
		self.gmList['M05']	= (self.fctM05,		"Arrêt rotation broche")
		self.gmList['M06']	= (self.fctNone,	"Changement outil")
		self.gmList['M30']	= (self.fctNone,	"Fin programme")

		self.fName = ""
		self.nbErr = 0
		self.cmdsPrimList = []

		# Automate d'état contrôlant les diverses syntaxes connues et implémentées dans ce logiciel
		self.atm = [

			('_001', '[ \t]',	self.fNop,		'_001'),
			('_001', '[A-Z]',	self.fVarInit,	'_002'),
			('_001', '[(]',		self.fVarInit,	'(001'),
			('_001', '[#;:]',	self.fVarInit,	'#001'),
			('_001', '[%]',		self.fVarInit,	'%001'),

			('_002', '[+-]',	self.fVarStore,	'_006'),
			('_002', '[0-9]',	self.fVarStore,	'_003'),
			('_002', '[.]',		self.fVarStore,	'_004'),
			('_002', '[ \t]',	self.fNop,		'_005'),

			('_003', '[.]',		self.fVarStore,	'_004'),
			('_003', '[0-9]',	self.fVarStore,	'_003'),
			('_003', '[ \t]',	self.fVarEnd1,	'_001'),
			('_003', '[A-Z]',	self.fVarEnd3,	'_002'),
			('_003', '[(]',		self.fVarEnd3,	'(001'),


			('_004', '[0-9]',	self.fVarStore,	'_004'),
			('_004', '[ \t]',	self.fVarEnd1,	'_001'),
			('_004', '[A-Z]',	self.fVarEnd3,	'_002'),
			('_004', '[(]',		self.fVarEnd3,	'(001'),

			('_005', '[+-]',	self.fVarStore,	'_006'),
			('_005', '[0-9]',	self.fVarStore,	'_003'),
			('_005', '[ \t]',	self.fVarStore,	'_005'),

			('_006', '[0-9]',	self.fVarStore,	'_003'),
			('_006', '[.]',		self.fVarStore,	'_004'),

			('(001', '[)]',		self.fNop,		'_001'),
			('(001', '*',		self.fVarStore,	'(001'),

			('#001', '*',		self.fNop,		'#001'),

			('%001', '*',		self.fNop,		'%001'),
		]

		self.listCmd = []									# Liste des commandes complètes contenues dans une ligne Gcode, ex: G01, X452.78
		self.dicVar = {}									# Liste des valeurs numériques associées aux commandes Gcode

		self.etatCourant = '_001'							# Initialisation de l'état de début de l'automate
		self.codeVar = ''


	def fDebug(self, car):
		print('fDebug --> Etat courant= {}, car=[{}]'.format(self.etatCourant, car))
		return(True)

	def fNop(self, car):
		print('fNop [{}]'.format(self.codeVar))
		pass

#	Traitement des commandes lues caractères par caractères selon le cycle : init, store, store, store, ..., end

	def fVarInit(self, car):										# Initialisation d'une commande rencontrée
		# Vérification de la validité de la commande
		if (car in self.cmdList):
			tup = self.cmdList[car]
			comment = tup[1]
			self.dicVar[car] = ''										# Création de la variable associée
#			print('fVarInit', self.codeVar, comment)
			return(True)
		else:
			return(False)


	def fVarStore(self, car):										# Stockage caractère par caractère de la variable associée à la cmd
		# Vérification de la validité de la variable associée

		self.dicVar[self.codeVar] += car							# Création de la variable de type str
#		print('fVarStore', self.codeVar, "=", self.dicVar[self.codeVar])

#	Trois fins possibles identifiées actuellement pour une commande selon le logiciel générateur du Gcode en cours de traitement

	def fVarEnd1(self, car, comment):										# Rencontre des caractères séparateurs [ \t]
		self.traitComEnd(1, car, comment)

	def fVarEnd2(self, car, comment):										# Détection de fin de ligne sans caractère séparateur préalable
		self.traitComEnd(2, car, comment)

	def fVarEnd3(self, car, comment):										# Rencontre des caractères [A-Z(] (absence de caractère séparateur)
		self.traitComEnd(3, car, comment)
		self.codeVar = car
		self.dicVar[car] = ''

#	Traitement commun aux trois fins

	def traitComEnd(self, cas, car, comment):								# Traitement commun aux 3 "fin"
		if (self.codeVar in ['G', 'M']):							# Cas des commandes G et M du gcode
#			print(    'EndCommand ', cas, self.codeVar, "=", self.dicVar[self.codeVar])
			self.execGM(self.codeVar, self.dicVar[self.codeVar], comment)
			return

		elif (self.codeVar in ['N']):								# Cas de la numérotation de ligne
			try:
				str = self.dicVar[self.codeVar]
				val = int(str)
#				print(    'EndInt     ', cas, self.codeVar, "=", val, comment)
				self.execN(self.codeVar, val)
			except:
				print('EndExcept1 ', cas, str, self.codeVar, "=", self.dicVar[self.codeVar])
			return

		else:														# Autres cas qui sont des variables de type X, Y, Z, etc ...
			try:
				str = self.dicVar[self.codeVar]
				val = float(str)
				print('EndVariable', cas, str, self.codeVar, "=", val, self.comment)
				self.execV(self.codeVar, val)
				return
			except:
				print('EndExcept2 ', cas, str, self.codeVar, "=", self.dicVar[self.codeVar])
		return


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
			lineFile = lineFile.strip()									# Supprimer le caractère \n de fin de ligne

			st.insertLine(lineFile, "gris")								# Visualisation de la ligne à traiter

			lg = len(lineFile)											# lg = nombre de caractères dans la ligne en cours
			if (lg == 0):
				continue												# Eliminer la ligne vide et passer à la ligne suivante
			if (lineFile[0] in [';','#']):
				continue												# Eliminer la ligne de commentaires et passer à la ligne suivante
			lineFile = lineFile.strip(';')								# Supprimer le caractère de fin ';' si il existe

			lg = len(lineFile)											# lg = nombre de caractères dans la ligne en cours après purge
			i = 0														# Index pour parcourir la ligne
			self.etatCourant = '_001'									# Réinitialisation de l'état courant de l'automate
			self.listCmd = ''

			while (i < lg):												# Balayage de la ligne Gcode en cours
				car = lineFile[i]										# Lire caractère par caractère
				if (self.etatCourant == '_001'):
					self.codeVar = car
				r = self.searchAtm(car)									# Rechercher ds l'automate la correspondance Etat/car
				if (r[0] == 'ok'):										# Si retour = trouvé
					codeRet = r[1](car)									# Lancer la fonction à exécuter
					if (codeRet == False):
						print("Erreur 244: car=[{}] in {}".format(car, lineFile))
					else:
						self.etatCourant = r[2]								# Enregistrer le nouvel état
				else:
					print("Erreur 248: car=[{}] in {}".format(car, lineFile))
				i += 1															# Passer au caractère suivant
			if (self.etatCourant != '_001'):
				self.fVarEnd2(car)
			print("Fin de traitement d'une ligne ----------------------------------------")

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

	def execGM(self, cmd, val, comment):
		print("--------------------------- GM : {}{}".format(cmd, val, comment))
		tup = self.gmList[cmd+val]
		print(tup[1])
		tup[0](val)											# Lancement de la fonction correspondante

	def execN(self, codeVar, val):
		print("---------------------------  N : {}{}".format(codeVar, val, comment))

	def execV(self, codeVar, val):
		print("---------------------------  V : {}{}".format(codeVar, val, comment))

#	Cas des commandes ou variables non prises en compte

	def fctNone(self, val = None):
		pass

#	Cas des commandes de type G ou M

	def fctG0(self, val = None):
		self.action = POS

	def fctG00(self, val = None):
		self.action = POS

	def fctG01(self, val = None):
		self.action = LINE

	def fctG02(self, val = None):
		self.action = ARC
		self.sens   = HORAIRE
		self.Ri = None				# Ri est aussi utilisé pour faire la distinction entre les deux formats de G02/G03

	def fctG03(self, val = None):
		self.action = ARC
		self.sens   = TRIGO
		self.Ri = None

	def fctG90(self, val = None):	# Mode absolu
		self.mode = ABS

	def fctG91(self, val = None):	# Mode relatif
		self.mode = REL

	def fctM0(self, val = None):	# Faire une pause, le programme repart après une action de l’opérateur.
		pass

	def fctM03(self, val = None):	#
		self.S = 0

	def fctM04(self, val = None):
		self.sens   = TRIGO

	def fctM05(self, val = None):
		self.sens   = HORAIRE





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
