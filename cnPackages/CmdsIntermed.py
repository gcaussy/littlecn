#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *

ABS, REL = True, False					# Mode de calcul des positionnements
NO, POS, LINE, CIRCLE = 0, 1, 2, 3				# Type de forme à réaliser POS = déplacement de positionnement seulement
GO, STOP = True, False					# Action de déplacement en XYZ
HORAIRE, TRIGO = True, False			# Sens de rotation de la broche

class CmdsIntermed(object):
	def __init__(self, tab):
		self.tab = tab

	def start(self):
		mode 	= ABS
		shape	= LINE
		sens	= HORAIRE
		action	 = STOP

		expr = "([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)"

		print("%")
		Xc = 0.0
		Yc = 0.0
		F = 5000
		S = 0
		print("D\tF={}\tS={}\tXc={:0.4f}\tYc={:0.4f}".format(F, S, Xc, Yc, ))


		for groupe in self.tab:
			cmdsInLine = groupe.split()					# Décomposition du groupe de commandes en une liste de commandes
			for cmd in cmdsInLine:
				firstChar = cmd[0]

				if (firstChar == 'G'):
					if (cmd == "G0"):					# Positionnement de l'outil
						action = POS
						continue
					if (cmd == "G01"):					# Tracé d'une ligne
						action = LINE
						continue
					if (cmd == "G02"):					# Tracé d'un cercle sens Horaire
						action = CIRCLE
						sens   = HORAIRE
						continue
					if (cmd == "G03"):					# Tracé d'un cercle sens Trigo
						action = CIRCLE
						sens   = TRIGO
						continue
					if (cmd == "G90"):					# Mode Absolu
						mode = ABS
						continue
					if (cmd == "G91"):					# Mode Relatif
						mode = REL
						continue
					print("Erreur code inconnu", cmd)

				if (firstChar == 'T'):					# Choix du Numéro d’outil
					continue
				if (firstChar == 'M'):					# Fonction auxiliaire
					continue
				if (firstChar == 'S'):					# Vitesse de rotation de la broche
					S = int(self._getVal(cmd, "[0-9]+"))
					continue
				if (firstChar == 'F'):					# Vitesse d’avance travail
					F = int(self._getVal(cmd, "[0-9]+"))
					continue

				if (firstChar == 'X'):					# Déplacement vers la nouvelle valeur de X
					Xi = self._getVal(cmd, expr)
					if (mode == REL):
						Xi = Xc + Xi
					continue
				if (firstChar == 'Y'):					# Déplacement vers la nouvelle valeur de Y
					Yi = self._getVal(cmd, expr)
					if (mode == REL):
						Yi = Yc + Yi
					continue
				if (firstChar == 'I'):					# Centre du cercle selon X
					Ii = self._getVal(cmd, expr)
					if (mode == REL):
						Ii = Xc + Ii
					continue
				if (firstChar == 'J'):					# Centre du cercle selon Y
					Ji = self._getVal(cmd, expr)
					if (mode == REL):
						Ji = Yc + Ji
					continue
				print("Erreur code inconnu", cmd)

			# ICI fin d'un groupe de commandes
#			print("----> ", groupe)

			if (action == POS):
				S = 0
				Xc = Xi
				Yc = Yi
				print("D\tF={}\tS={}\tXc={:0.4f}\tYc={:0.4f}".format(int(F), int(S), Xi, Yi, ))
				action = NO
				continue

			if (action == LINE):
				print("L\tF={}\tS={}\tX1={:0.4f}\tY1={:0.4f}\tX2={:0.4f}\tY2={:0.4f}".format(F, S, Xc, Yc, Xi, Yi))
				Xc = Xi
				Yc = Yi
				action = NO
				continue

			if (action == CIRCLE):
				print("C\tF={}\tS={}\tX1={:0.4f}\tY1={:0.4f}\tX2={:0.4f}\tY2={:0.4f}\tI={:0.4f}\tJ={:0.4f}".format(F, S, Xc, Yc, Xi, Yi, Ii, Ji))
				Xc = Xi
				Yc = Yi
				action = NO
				continue
		print("%")

	def _getVal(self, cmd, expr):
		str = cmd[1:]
		ret = re.match(expr, str)
		if ret is not None:
			val = float(str)
			return(val)
		else:
			print("Erreur sur la valeur", cmd)


# ([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)"   ret = re.match(expr, att)

# Programme principal
# ===================

if __name__ == "__main__":

	cmdsTab = []									# Mode	cX		cY		tX		tY		Type		Depl
	cmdsTab.append("G90")							# Abs	?		?		?		?		none			?
	cmdsTab.append("G0 X50 Y40")					# Abs	0		0		50		40		position	GO
	cmdsTab.append("T1 M6")							# Abs	50		40		none	none	none		OFF
	cmdsTab.append("M3 S2500")						# Abs	50		50		none	none	none		OFF
	cmdsTab.append("G91")							# Rel	50		50		none	none	none		OFF
	cmdsTab.append("G01 X40 F200")					# Rel	0+50	40		50+40	40		none		ON
	cmdsTab.append("G90")							# Abs	50		40		none	none	none		OFF
	cmdsTab.append("G01 X110 Y20")					# Abs	90		40		110		20		line		ON
	cmdsTab.append("G91")							# Rel
	cmdsTab.append("G03 X30 Y30 I0 J30 F250")		# Rel	110		20		110+30	20+30	Cercle		ON
	cmdsTab.append("G01 Y10 F500")					# Rel	0		50		140		10		Line		ON
	cmdsTab.append("X-90")							# Rel	0		10		-90							# Rel
	cmdsTab.append("G01 F250")
	cmdsTab.append("Y-20")
	cmdsTab.append("G01")
	cmdsTab.append("M5")							# Rel
	cmdsTab.append("M2")							# Rel


#	w = Tk()
#	w.title('AnalSyntaxGcode')
	ci = CmdsIntermed(tab = cmdsTab)
	ci.start()

#	w.mainloop()