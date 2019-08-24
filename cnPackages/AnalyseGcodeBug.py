#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
from tkinter.filedialog import askopenfilename
from math import *
import sys
import re

try:
	from cnPackages.calculCentreArc import calculCentreArc
except:
	from calculCentreArc import calculCentreArc

ABS, REL = True, False					# Mode de calcul des positionnements
NO, POS, LINE, ARC = 0, 1, 2, 3			# Type de forme à réaliser POS = déplacement de positionnement seulement
GO, STOP = True, False					# Action de déplacement en XYZ
HORAIRE, TRIGO = True, False			# Sens de rotation de la broche


# Chargement et analyse du fichier G-Code
# ---------------------------------------

class AnalSyntaxGcode(object):
	def __init__(self):
		# Liste réduite des commandes Gcode autorisées
		self.gmList = {}
		self.gmList['G0']	= (self.fctG0,		"Déplacement rapide")
		self.gmList['G00']	= (self.fctG00,		"Déplacement rapide")
		self.gmList['G01']	= (self.fctG01,		"Interpolation linéaire")
		self.gmList['G02']	= (self.fctG02,		"Interpolation circulaire(sens horaire)")
		self.gmList['G03']	= (self.fctG03,		"Interpolation circulaire(sens trigo)")
		self.gmList['G17']	= (self.fctNone,	"Sélection du plan X-Y")
		self.gmList['G20']	= (self.fctNone,	"Programmation en pouces ")
		self.gmList['G21']	= (self.fctNone,	"Programmation en mm")
		self.gmList['G49']	= (self.fctNone,	"?")
		self.gmList['G50']	= (self.fctNone,	"?")
		self.gmList['G53']	= (self.fctG53,		"Déplacements en coordonnées machine")
		self.gmList['G54']	= (self.fctG54,		"Activation du décalage d'origine pièce (Offset)")
		self.gmList['G80']	= (self.fctNone,	"Annulation de cycle fixe")
		self.gmList['G90']	= (self.fctG90,		"Programmation absolue")
		self.gmList['G91']	= (self.fctG91,		"Programmation relative")
		self.gmList['M0']	= (self.fctM0,		"Arrêt programme")
		self.gmList['M2']	= (self.fctNone,	"Fin de programme")
		self.gmList['M3']	= (self.fctM03,		"Broche sens horaire")
		self.gmList['M5']	= (self.fctM05,		"Arrêt de broche")
		self.gmList['M6']	= (self.fctNone,	"Changement outil")
		self.gmList['M9']	= (self.fctNone,	"Arrosage")
		self.gmList['M00']	= (self.fctNone,	"Arrêt programme")
		self.gmList['M01']	= (self.fctNone,	"Arrêt conditionnel")
		self.gmList['M02']	= (self.fctNone,	"Fin de programme")
		self.gmList['M03']	= (self.fctM03,		"Broche sens horaire")
		self.gmList['M04']	= (self.fctM04,		"Sens antihoraire")
		self.gmList['M05']	= (self.fctM05,		"Arrêt de broche")
		self.gmList['M06']	= (self.fctNone,	"Changement outil")
		self.gmList['M30']	= (self.fctNone,	"Fin programme")
		self.gmList['T1']	= (self.fctNone,	"Choix de l'outil")

		# Liste des commandes G-code avec le format exact de la commande complète
		self.cmdList = {}
		self.cmdList['A'] = (self.fctNone,	"([0-9]+)|([+-]?[0-9]+.[0-9]+)", "Axe A rotatif de la machine (4ème axe)")
		self.cmdList['B'] = (self.fctNone,	"([0-9]+)|([+-]?[0-9]+.[0-9]+)", "Axe B de la machine")
		self.cmdList['C'] = (self.fctNone,	"([0-9]+)|([+-]?[0-9]+.[0-9]+)", "Axe C de la machine")
		self.cmdList['D'] = (self.fctNone,	"[0-9]+", "Valeur de la compensation de rayon d’outil")
		self.cmdList['F'] = (self.fctF,		"([0-9]+)|([0-9]+.[0-9]+)", "Vitesse de déplacement de la broche")
		self.cmdList['G'] = (self.fctNone,	"[0-9]+", "Fonction Générale")
		self.cmdList['H'] = (self.fctNone,	"[0-9]+", "Index d’offset de longueur d’outil")
		self.cmdList['I'] = (self.fctI,		"([0-9]+)|([0-9]+.[0-9]+)", "Centre du cercle selon X")
		self.cmdList['J'] = (self.fctJ,		"([0-9]+)|([0-9]+.[0-9]+)", "Centre du cercle selon Y")
		self.cmdList['K'] = (self.fctNone,	"[0-9]+", "Décalage en Z pour les arcs ")
		self.cmdList['L'] = (self.fctNone,	"[[0-9]+", "Longueur de la broche")
		self.cmdList['M'] = (self.fctNone,	"[0-9]+", "Fonction auxiliaire")
		self.cmdList['N'] = (self.fctNone,	"[0-9]+", "Numéro de ligne")
		self.cmdList['O'] = (self.fctNone,	"[0-9]+", "Incrément Delta en Z dans un cycle G73, G83")
		self.cmdList['P'] = (self.fctNone,	"[0-9]+", "Tempo utilisée dans les cycles de perçage et avec G4 / Mot clé utilisé avec G10")
		self.cmdList['Q'] = (self.fctNone,	"[0-9]+", "Incrément Delta en Z dans un cycle G73, G83")
		self.cmdList['R'] = (self.fctR,		"([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)", "Rayon d’arc")
		self.cmdList['S'] = (self.fctS,		"[0-9]+", "Vitesse de rotation de la broche")
		self.cmdList['T'] = (self.fctT,		"[0-9]+", "Choix du Numéro d’outil")
		self.cmdList['U'] = (self.fctNone,	"[0-9]+", "Axe U de la machine")
		self.cmdList['V'] = (self.fctNone,	"[0-9]+", "Axe V de la machine")
		self.cmdList['W'] = (self.fctNone,	"[0-9]+", "Axe W de la machine")
		self.cmdList['X'] = (self.fctX,		"([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)", "Axe X de la machine")
		self.cmdList['Y'] = (self.fctY,		"([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)", "Axe Y de la machine")
		self.cmdList['Z'] = (self.fctZ,		"([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)", "Axe Z de la machine")
		self.cmdList[';'] = (self.fctNone,	"^;.*$", "Commentaire")
		self.cmdList['%'] = (self.fctNone,	"^$", "Début ou Fin de fichier")

		self.fName = ""
		self.nbErr = 0
		self.cmdsPrimList = []

		self.mode 	= ABS
		self.sens	= HORAIRE
		self.action	= NO

		self.Xc = 0.0
		self.Yc = 0.0
		self.Zc = 0.0

		self.Xi = 0.0
		self.Yi = 0.0
		self.Zi = 0.0

		self.Xmax = 0.0
		self.Ymax = 0.0
		self.Zmax = 0.0

		self.Ii = 0.0
		self.Ji = 0.0
		self.Ri = None

		self.F = 5000
		self.S = 0

	def getVal(self, cmd, expr):
		str = cmd[1:]
		ret = re.match(expr, str)
		if ret is not None:
			val = float(str)
			return(val)
		else:
			print("Erreur sur la valeur", cmd)

	def fctNone(self, val = None):
		pass

	def fctG0(self, val = None):
		self.action = POS

	def fctG00(self, val = None):
		self.action = POS

	def fctG01(self, val = None):
		self.action = LINE

	def fctG02(self, val = None):
		self.action = ARC
		self.sens   = HORAIRE
		self.Ri = None

	def fctG03(self, val = None):
		self.action = ARC
		self.sens   = TRIGO
		self.Ri = None

	def fctG53(self, val = None):	# Fixe l’origine des déplacements par rapport à l’origine machine.
		pass

	def fctG54(self, val = None):	# Fixe l’origine des déplacements par rapport à une coordonnée système .
		pass

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

	def fctF(self, val):
		self.F = int(val)
#		print("fctF", self.F)

	def fctI(self, val):
		self.Ii = val
		if (self.mode == REL):
			self.Ii = self.Xc + self.Ii
#		print("fctI", self.Ii)

	def fctJ(self, val):
		self.Ji = val
		if (self.mode == REL):
			self.Ji = self.Yc + self.Ji
#		print("fctJ", self.Ji)

	def fctR(self, val):
		self.Ri = val

	def fctS(self, val):
		self.S = int(val)
#		print("fctS", self.S)

	def fctT(self, val = None):
		pass

	def fctX(self, val):
		self.Xi = val
		if (self.mode == REL):
			self.Xi = self.Xc + self.Xi
#		print("fctX", self.Xi)

	def fctY(self, val):
		self.Yi = val
		if (self.mode == REL):
			self.Yi = self.Yc + self.Yi
#		print("fctY", self.Yi)

	def fctZ(self, val):
		self.Zi = val
		if (self.mode == REL):
			self.Zi = self.Zc + self.Zi
#		print("fctZ", self.Zi)


	def openFile(self, st, tr, cm):
		self.fName = askopenfilename()
		try:
			file = open(self.fName, "r")
		except:
			print("Nom de fichier \"{}\" inconnu".format(self.fName))
			sys.exit(0)

		st.clear()
		cm.clear()
		self.nbErr = 0
		self.cmdsPrimList.clear()

		tr.insertLine("Fichier = {}\n".format(self.fName), "noir")
		cm.insertLine("%\n", "bleu", False)
		msg = "P F={} S={} Xc={:0.2f} Yc={:0.2f}".format(self.F, self.S, self.Xc, self.Yc)
		self.cmdsPrimList.append(msg)
		cm.insertLine(msg+'\n', "bleu", False)


#		while (True):
		for i in range (10):
			lineFile = file.readline()													# Lecture d'une ligne du fichier G-code en cours
			line = lineFile.strip()														# Suppression du saut de ligne en fin de ligne
			line = line.strip(';')														# Suppression des point-virgule en fin de ligne
			if (line == ''):
				break
			st.insertLine(lineFile, "gris")												# Visualisation de la ligne à traiter

			# Elimination de la ligne de commentaires commençant par ; ou #
			if (line[0] in [';', '#']):
				st.insertLine("ligne éliminée : [{}]\n\n".format(line), "bleu")
				continue

			idx = 0
			tmp = ""
			while idx < len(line):										# Balayage de la ligne en recherche de commentaires de fin de ligne
				c = line[idx]
				if (c in [';', '#']):
					line = line[0:idx-1]								# Ne conserver que le début de ligne
					break												# Arréter le balayage
				idx = idx + 1

			m = re.sub("(\([a-zA-Z0-9 ]*\))", "", line)					# Suppression des commentaires de type (xxxxxx)
			if (m is not None):
				line = m
			line = line.strip()
			st.insertLine("[{}]\n".format(line), "bleu")
			if (line == ""):
				continue

			frm = "{}\t\t\t{}\n"
			cmdsInLine = line.split()											# Création de la liste des commandes contenues dans la ligne
			for cmd in cmdsInLine:												# Récupération d'une commande à traiter
				firstChar = cmd[0]												# Récupération du 1er caractère de la commande
				if (firstChar in [';', '#']):
					break														# Abandonner la ligne en cours

				if (firstChar in self.cmdList):									# Vérification que ce 1er caractère existe dans les commandes G-code
					print("DEBUG AnalyseGcode.py 272 {}".format(cmd))

					tup = self.cmdList[firstChar]
					expr = tup[1]												# Récup expression régulière précisant le format autorisé associé à cette commande
					attrib = cmd[1:]											# Sélection des caractères faisant suite au 1er caractère
					ret = re.match(expr, attrib)								# Vérification de la syntaxe
					if ret is not None:											# None signifie : Erreur de format
						if (firstChar in ['G', 'M']):							# Cas des commandes sans valeur associée
							if (cmd in self.gmList):							# Vérification de l'existence dans la liste des commandes GM
								tup = self.gmList[cmd]							# Récupération du commentaire précisant l'action à réaliser
								print("DEBUG AnalyseGcode.py 280 {}".format(type(tup[0])))
								st.insertLine(frm.format(cmd, tup[1]), "vert")	# Visualisation de la commande dans une nouvelle ligne
								tup[0]()										# Lancement de la fonction correspondante à l'action
								continue										# Passage à la commande suivante

						val = self.getVal(cmd, expr)
						st.insertLine(frm.format(cmd, tup[2]), "vert")			# Visualisation de la commande dans une nouvelle ligne
						tup[0](val)												# Lancement de l'action correspondante
						continue												# Passage à la commande suivante

					else:
						self.nbErr += 1
						st.insertLine(frm.format(cmd, "cmdList : No match"), "rouge")	# Visualisation de l'erreur
				else:
					self.nbErr += 1
					st.insertLine(frm.format(cmd, "cmdList: Code inconnu"), "rouge")	# Visualisation de l'erreur
			st.insertLine("\n", "noir")													# Saut d'une ligne

			print("DEBUG AnalyseGcode.py 296")
			if (self.action == POS):
				print("DEBUG AnalyseGcode.py 298 POS")
				S = 0
				self.Xc = self.Xi
				self.Yc = self.Yi
				msg = "P F={} S={} Xc={:0.2f} Yc={:0.2f}".format(int(self.F), int(self.S), self.Xi, self.Yi)
				self.cmdsPrimList.append(msg)
				cm.insertLine(msg+"\n", "bleu", False)
				self.action = NO
				continue

			print("DEBUG AnalyseGcode.py 308")
			if (self.action == LINE):
				print("DEBUG AnalyseGcode.py 309 LINE")
				msg = "L F={} S={} X1={:0.2f} Y1={:0.2f} X2={:0.2f} Y2={:0.2f}".format(self.F, self.S, self.Xc, self.Yc, self.Xi, self.Yi)
				self.cmdsPrimList.append(msg)
				cm.insertLine(msg+"\n", "bleu", False)
				self.Xc = self.Xi
				self.Yc = self.Yi
				self.action = NO
				continue

			print("DEBUG AnalyseGcode.py 318")
			if (self.action == ARC):
				print("DEBUG AnalyseGcode.py 320 ARC")
				codeArc = ''
				if (self.Xc == self.Xi and self.Yc == self.Yi):			# Test si il s'agit d'un cercle
					codeArc = 'C'
					msg = "{} F={} S={} I={:0.2f} J={:0.2f} R={:0.2f}".format(codeArc, self.F, self.S, self.Ii, self.Ji, self.Ri)
					self.cmdsPrimList.append(msg)
					cm.insertLine(msg+"\n", "rouge", False)
					continue

				if (self.sens == TRIGO):
					codeArc = 'T'
					self.Ri = 10
				elif (self.sens == HORAIRE):
					codeArc  = 'H'
#					self.Ri = 20
				else:
					print("Erreur 328")

				print("DEBUG -- 334")
				if (self.Ri is not None):
					#     calculCentreArc(     xA,      yA,     xB,      yB,          S,      R)
					tup = calculCentreArc(self.Xc, self.Yc, self.Xi, self.Yi, self.sens, self.Ri)
					#     return(orientation, align, xC2, yC2, R, S, dAB)
					self.Ii = tup[0]
					self.Ji = tup[1]
					print(self.Ri, tup[0], tup[1])






	def	getNbErr(self):
		return(self.nbErr)

	def getPrimList(self):
		return (self.cmdsPrimList)

	def createCmdCanvas(self, panel):
		can = panel.getCan()
		can.delete("all")
		self.Xmax = 0.0
		self.Ymax = 0.0
		self.Zmax = 0.0

		for cmd in self.cmdsPrimList:
			cmdTab = cmd.split()
			firstChar = cmd[0]
			if (firstChar == 'P'):							# POSITION
				x1 = float(cmdTab[3][3:])
				y1 = float(cmdTab[4][3:])

			if (firstChar == 'L'):							# LINE
				str = cmdTab[3]
				x0 = float(cmdTab[3][3:])
				y0 = float(cmdTab[4][3:])
				x1 = float(cmdTab[5][3:])
				y1 = float(cmdTab[6][3:])
				panel.create_lineCn(x0, y0, x1, y1, tag = "CN", Xmax = self.Xmax, Ymax = self.Ymax)
				if (x0 > self.Xmax):
					self.Xmax = x0
				if (x1 > self.Xmax):
					self.Xmax = x1
				if (y0 > self.Ymax):
					self.Ymax = y0
				if (y1 > self.Ymax):
					self.Ymax = y1

			if (firstChar in ['T', 'H']):							# ARC sens Trigo ou Horaire
				x0Gcode = float(cmdTab[3][3:])
				y0Gcode = float(cmdTab[4][3:])
				x1Gcode = float(cmdTab[5][3:])
				y1Gcode = float(cmdTab[6][3:])
				xcGcode = float(cmdTab[7][2:])
				ycGcode = float(cmdTab[8][2:])

				if (x0Gcode > self.Xmax):
					self.Xmax = x0Gcode
				if (x1Gcode > self.Xmax):
					self.Xmax = x1Gcode
				if (y0Gcode > self.Ymax):
					self.Ymax = y0Gcode
				if (y1Gcode > self.Ymax):
					self.Ymax = y1Gcode

				Xd = x1Gcode - x0Gcode
				Yd = y1Gcode - y0Gcode
				Hd = sqrt(Xd**2 + Yd**2)
				Rd = sqrt((ycGcode - y1Gcode)**2 + (x1Gcode - xcGcode)**2)
				x0Can = xcGcode - Rd
				y0Can = ycGcode + Rd
				x1Can = xcGcode + Rd
				y1Can = ycGcode - Rd
				x1Can = xcGcode + Rd
				sinV = (Hd/2) / Rd
				angleRad = asin(sinV)
				angleDeg = degrees(angleRad) * 2
				panel.create_arcCn(x0Can, y0Can, x1Can, y1Can, start=270, extent=angleDeg, color = 'red', tag = "CN", Xmax = self.Xmax, Ymax = self.Ymax)

			if (firstChar == 'C'):
				pass

		return()



# Programme principal
# ===================

class PrintGcode(object):
	def __init__(self):
		pass

	def insertLine(self, text, color, flag = None):
		msg = text.strip()
		if (msg != ""):
			print(msg)

	def clear(self):
		print("------------------- DEBUT -----------------------")

if __name__ == "__main__":

	def getResult():
		print("nbErr=", asg.getNbErr())
		pl = asg.getPrimList()
		print(type(pl))
		for cmd in pl:
			print("-->", cmd)

	w = Tk()
	w.title('AnalSyntaxGcode')
	print("TEST ANALYSE GCODE")

	st = PrintGcode()
	asg = AnalSyntaxGcode()

	btn1 = Button(w, text = "Test", command = lambda arg1 = st, arg2 = st, arg3 = st: asg.openFile(arg1, arg2, arg3))
	btn1.pack()
	btn2 = Button(w, text = "Get", command = getResult)
	btn2.pack()

	w.mainloop()
	print("END")

