#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
from tkinter.filedialog import askopenfilename
from math import *
import sys
import re

try:
	from cnPackages.calculCentreArc import calculCentreArc
	from cnPackages.AnalCmd import AnalCmd
except:
	from calculCentreArc import calculCentreArc
	from AnalCmd import AnalCmd

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
		self.Ri = None				# Ri est aussi utilisé pour faire la distinction entre les deux formats de G02/G03

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

		while (True):
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
					tup = self.cmdList[firstChar]
					expr = tup[1]												# Récup expression régulière précisant le format autorisé associé à cette commande
					attrib = cmd[1:]											# Sélection des caractères faisant suite au 1er caractère
					ret = re.match(expr, attrib)								# Vérification de la syntaxe
					if ret is not None:											# None signifie : Erreur de format
						if (firstChar in ['G', 'M']):							# Cas des commandes sans valeur associée
							if (cmd in self.gmList):							# Vérification de l'existence dans la liste des commandes GM
								tup = self.gmList[cmd]							# Récupération du commentaire précisant l'action à réaliser
								st.insertLine(frm.format(cmd, tup[1]), "vert")	# Visualisation de la commande dans une nouvelle ligne
								if (type(tup[0]).__name__ == 'method'):
									tup[0]()									# Lancement de la fonction correspondante à l'action
									continue									# Passage à la commande suivante
								else:
									break										# Abandonner la ligne en cours

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

#			print("----> DEBUG 300  AVANT Xc={}, Yc={}\n".format(self.Xc, self.Yc))

			if (self.action == POS):
				S = 0
				self.Xc = self.Xi
				self.Yc = self.Yi
				msg = "A=P F={} S={} X1={:0.2f} Y1={:0.2f}".format(int(self.F), int(self.S), self.Xi, self.Yi)
				self.cmdsPrimList.append(msg)
				cm.insertLine(msg+"\n", "bleu", False)
				self.action = NO
				print("----> DEBUG 300  APRES POS:  Xc={}, Yc={}\n".format(self.Xc, self.Yc))
				continue

			if (self.action == LINE):
				msg = "A=L F={} S={} X1={:0.2f} Y1={:0.2f} X2={:0.2f} Y2={:0.2f}".format(self.F, self.S, self.Xc, self.Yc, self.Xi, self.Yi)
				self.cmdsPrimList.append(msg)
				cm.insertLine(msg+"\n", "bleu", False)
				self.Xc = self.Xi
				self.Yc = self.Yi
				self.action = NO
				print("----> DEBUG 300  APRES LINE: Xc={}, Yc={}\n".format(self.Xc, self.Yc))
				continue

			if (self.action == ARC):
				codeArc = ''

				if (self.Xc == self.Xi and self.Yc == self.Yi):			# Test si il s'agit d'un cercle
					codeArc = 'C'
					msg = "A={} F={} S={} I={:0.2f} J={:0.2f} R={:0.2f}".format(codeArc, self.F, self.S, self.Ii, self.Ji, self.Ri)
					self.cmdsPrimList.append(msg)
					cm.insertLine(msg+"\n", "rouge", False)
					continue

				if (self.sens == TRIGO):
					codeArc = 'T'
					self.Ri = None
				elif (self.sens == HORAIRE):
					codeArc  = 'H'
					self.Ri = None
				else:
					print("ERR 335")

				if (self.Ri is not None):			# cas: G02 Xnnn Ynnn Rnnn (Le centre du cercle est à calculer)
					#     calculCentreArc(     xA,      yA,      xB,      yB,         S,      R)
					tup = calculCentreArc(self.Xc, self.Yc, self.Xi, self.Yi, self.sens, self.Ri)
					#     return(tag, align, xC2, yC2, R, S, dAB)
					#     return('ERR',     , code

					if (tup[0] is not None and tup[0] == 'ERR'):			# code de debbugage
						print("ERR 345")
						continue
					align		= tup[1]			# align False ou True
					self.Ii		= tup[2]			# centre du cercle en x
					self.Ji		= tup[3]			# centre du cercle en y
					self.Ri		= tup[4]			# rayon du cercle

				# Tronc commun aux deux formes de description d'un arc de cercle
				print("----> DEBUG 357  Tronc commun:  Xi={}, Yi={}\n".format(self.Xi, self.Yi))
				if (self.Xc == self.Ii and self.Xc == self.Xi):			# Demi lune verticale
					dci = abs(self.Yc - self.Yi)
					self.Ri = dci / 2
					angle = 180

				elif (self.Yc == self.Ji and self.Yc == self.Yi):		# Demi lune horizontale
					dci = abs(self.Xc - self.Xi)
					self.Ri = dci / 2
					angle = 180

				else:
					self.Ri = sqrt(((self.Xc - self.Ii) ** 2) + ((self.Yc - self.Ji) ** 2))
					dci = sqrt((self.Xi - self.Xc) ** 2 + (self.Yi - self.Yc) ** 2)
					angle = degrees(asin((dci/2)/self.Ri))

				print("----> DEBUG 370  Ri={}, dci={}\n".format(self.Ri, dci))

				msg = "A={} F={} S={} X1={:0.2f} Y1={:0.2f} X2={:0.2f} Y2={:0.2f} I={:0.2f} J={:0.2f} R={:0.2f} A={:0.2f}".format(
								codeArc, self.F, self.S, self.Xc, self.Yc, self.Xi, self.Yi, self.Ii, self.Ji, self.Ri, angle)
				self.cmdsPrimList.append(msg)
				cm.insertLine(msg+"\n", "rouge", False)

				self.Xc = self.Xi					# Mise à jour des valeurs courantes
				self.Yc = self.Yi
				self.action = NO
				print("----> DEBUG 300  APRES ARC:  Xc={}, Yc={}\n".format(self.Xc, self.Yc))
				continue

#			n += 1
		file.close()
		st.insertLine("nbErr={}\n".format(self.nbErr), "rouge")
		tr.insertLine("nbErr={}\n".format(self.nbErr), "rouge")
		return (self.nbErr)

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

			if (firstChar in ['T', 'H']):
				# ARC sens Trigo ou Horaire : tronc commun
				# Récupération des valeurs de la ligne de codes intermédiaires
				# Ex: H F=200 S=2500 X1=30.00 Y1=120.00 X2=30.00 Y2=80.00 I=30.00 J=100.00 R=20.00 A=180.00
				#     0 1     2      3        4         5        6        7       8        9       10
				X1_CodeInt = float(cmdTab[3][3:])
				Y1_CodeInt = float(cmdTab[4][3:])
				X2_CodeInt = float(cmdTab[5][3:])
				Y2_CodeInt = float(cmdTab[6][3:])
				I_CodeInt = float(cmdTab[7][2:])
				Y_CodeInt = float(cmdTab[8][2:])
				R_CodeInt = float(cmdTab[9][2:])
				A_CodeInt = float(cmdTab[10][2:])

				# Enregistrement des valeurs max pour le Cadrage ultérieur au centre du Canvas
				if (X1_CodeInt > self.Xmax):
					self.Xmax = X1_CodeInt
				if (X2_CodeInt > self.Xmax):
					self.Xmax = X2_CodeInt
				if (Y_CodeInt > self.Ymax):
					self.Ymax = Y1_CodeInt
				if (Y2_CodeInt > self.Ymax):
					self.Ymax = Y2_CodeInt

				#
#				Xd = x1Gcode - x0Gcode
#				Yd = y1Gcode - y0Gcode
#				Hd = sqrt(Xd**2 + Yd**2)
#				Rd = sqrt((ycGcode - y1Gcode)**2 + (x1Gcode - xcGcode)**2)

				# Calcul des coordonnées x0, y0, x1, y1 du carré du canvas entourant le cercle
				x0_Can = I_CodeInt - R_CodeInt
				y0_Can = J_CodeInt + R_CodeInt
				x1_Can = I_CodeInt + R_CodeInt
				y1_Can = J_CodeInt - R_CodeInt

				# Calcul de l'angle "Start" à partir de l'horizontale passant par le centre du cercle
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
	print('TEST ANALYSE GCODE')

	st = PrintGcode()
	asg = AnalSyntaxGcode()

	btn1 = Button(w, text = "Test", command = lambda arg1 = st, arg2 = st, arg3 = st: asg.openFile(arg1, arg2, arg3))
	btn1.pack()
	btn2 = Button(w, text = "Get", command = getResult)
	btn2.pack()

	w.mainloop()
	print("END")

