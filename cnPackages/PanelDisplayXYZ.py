#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
from threading import Thread
import time
#try:
#	from cnPackages.WinParam  import WinParam
#	from cnPackages.EntryRegx import EntryRegx
#	from cnPackages.DataParam import DataParam
#	from cnPackages.ThreadMoteurs import *
#except:
try:
	from WinParam  import WinParam
	from EntryRegx import EntryRegx
	from DataParam import DataParam
	from ThreadMoteurs import *
except:
	print("PanelDisplayXYZ : Erreur import")



class PanelDisplayXYZ(Frame):
	def __init__(self, boss, data, baseFont = "Courier 8 normal", bg = "ivory"):
		Frame.__init__(self, boss, bg = bg)
		Label(self, text ="Positionnement courant", font = "{courier new} 11 bold", bg = bg, fg = "blue").grid(row = 1, column = 1, columnspan = 3)
		Label(self, text ="Machine (en mm)", font = "{courier new} 8 bold", bg = bg, fg = "grey").grid(row = 2, column = 2)
		Label(self, text ="Pièce (en mm)", font = "{courier new} 8 bold", bg = bg, fg = "grey").grid(row = 2, column = 3)
		myFont2 = "{courier new} 16 bold"
		Label(self, text ="X", font = myFont2, bg = bg, fg = "blue").grid(row = 3, column = 1)
		Label(self, text ="Y", font = myFont2, bg = bg, fg = "blue").grid(row = 4, column = 1)
		Label(self, text ="Z", font = myFont2, bg = bg, fg = "blue").grid(row = 5, column = 1)
		Label(self, text ="F", font = myFont2, bg = bg, fg = "black").grid(row = 6, column = 1)
		Label(self, text ="S", font = myFont2, bg = bg, fg = "black").grid(row = 7, column = 1)
		Label(self, text ="mm/minute", font = "{courier new} 8 bold", bg = bg, fg = "grey").grid(row = 6, column = 3, sticky = 'w')
		Label(self, text ="trs/mn", font = "{courier new} 8 bold", bg = bg, fg = "grey").grid(row = 7, column = 3, sticky = 'w')

		eWidth = 8
		self.entryXm = Entry(self, justify = RIGHT, width = eWidth, state = "readonly")
		self.entryXm.grid(row = 3, column = 2, padx = 5)
		self.entryYm = Entry(self, justify = RIGHT, width = eWidth, state = "readonly")
		self.entryYm.grid(row = 4, column = 2, padx = 5)
		self.entryZm = Entry(self, justify = RIGHT, width = eWidth, state = "readonly")
		self.entryZm.grid(row = 5, column = 2, padx = 5)

		self.entryXp = Entry(self, justify = RIGHT, width = eWidth, state = "readonly")
		self.entryXp.grid(row = 3, column = 3, padx = 5)
		self.entryYp = Entry(self, justify = RIGHT, width = eWidth, state = "readonly")
		self.entryYp.grid(row = 4, column = 3, padx = 5)
		self.entryZp = Entry(self, justify = RIGHT, width = eWidth, state = "readonly")
		self.entryZp.grid(row = 5, column = 3, padx = 5)

		self.entryF = Entry(self, justify = RIGHT, width = eWidth, state = "readonly")
		self.entryF.grid(row = 6, column = 2, padx = 5)
		self.entryS = Entry(self, justify = RIGHT, width = eWidth, state = "readonly")
		self.entryS.grid(row = 7, column = 2, padx = 5)

		self.entListM = [self.entryXm, self.entryYm, self.entryZm]
		self.entListP = [self.entryXp, self.entryYp, self.entryZp]

		self.data = data									# data = objet mémorisant ces valeurs

#		Valeurs conservées pour un calcul des déplacements
		self.valP = {}										# Position courante en XYZ
		self.valP['x'] = 0.0
		self.valP['y'] = 0.0
		self.valP['z'] = 0.0

		self.valMax = {}									# Position relative max autorisée (Lg max définie param. machine - Offset)
		self.valMax['x'] = self.data.getFloatCourseMax('x')
		self.valMax['y'] = self.data.getFloatCourseMax('y')
		self.valMax['z'] = self.data.getFloatCourseMax('z')

		self.offset	= {}									# Déclalage suite au positionnement origine pièce par rapport au calage machine
		self.offset['x'] = 0.0
		self.offset['y'] = 0.0
		self.offset['z'] = 0.0

		self.memP = {}
		self.memP['x'] = 0.0
		self.memP['y'] = 0.0
		self.memP['z'] = 0.0

		self.entryP = {}
		self.entryP['x'] = self.entryXp						# Référence à l'affichage de la position courante sur l'axe X
		self.entryP['y'] = self.entryYp
		self.entryP['z'] = self.entryZp

		self.entryM = {}
		self.entryM['x'] = self.entryXm						# Référence à l'affichage de la position machine sur l'axe X
		self.entryM['y'] = self.entryYm
		self.entryM['z'] = self.entryZm

		self.valF = 0.0										# Vitesse calculée entre deux steps
		self.valS = 0.0										# Vitesse de la broche définie dans le gcode

		self.lastTimestamp = 0.0							# Dernier temps mémorisé

		self.ff = "{:0.4f}"									# Format de présentation des "float"


	def clear(self):
		global stopUrgence
		stopUrgence = False
		for ent in self.entListM+self.entListP:
			self._setEntry(ent, "?")						# Pour visualiser le clear (Absence de donnée pour le moment)

	def calage(self):										# Remise à zéro suite à un calage machine sur les butées des 3 axes
		for i in self.valP:
			self.valP[i] = 0.0
		for i in self.offset:
			self.offset[i] = 0.0
		for i in self.memP:
			self.memP[i] = 0.0
		self.valF = 0.0
		self.valS = 0.0

		for ent in self.entListM+self.entListP:				# Boucle de remise à zéro des affichages XYZ machine et courants
			str = self.ff.format(0.0)
			self._setEntry(ent, str)

	def setOrigPieceXY(self):								# Visualisation de l'Offset entre le calage machine et le calage pièce
		self.offset['x'] = self.valP['x']
		str = self.ff.format(self.valP['x'])
		self._setEntry(self.entryXm, str)
		self.valP['x'] = 0.0
		str = self.ff.format(self.valP['x'])
		self._setEntry(self.entryXp, str)

		self.offset['y'] = self.valP['y']
		str = self.ff.format(self.valP['y'])
		self._setEntry(self.entryYm, str)
		self.valP['y'] = 0.0
		str = self.ff.format(self.valP['y'])
		self._setEntry(self.entryYp, str)

		for axe in ['x', 'y']:
			self.valMax[axe] = self.data.getFloatCourseMax(axe) - self.offset[axe] - 1
#			print("PanelDisplayXYZ: axe={}, CourseMax={}, offset={}, valMax ={}".
#				format(axe, self.data.getFloatCourseMax(axe), self.offset[axe], self.valMax[axe]))

	def setOrigPieceZ(self):									# Visualisation de la position courante de Z en tant qu'origine pièce Z
		self.offset['z'] = self.valP['z']
		str = self.ff.format(self.valP['z'])
		self._setEntry(self.entryZm, str)
		self.valP['z'] = 0.0
		str = self.ff.format(self.valP['z'])
		self._setEntry(self.entryZp, str)

		for axe in ['z']:
			self.valMax[axe] = self.data.getFloatCourseMax(axe) - self.offset[axe] - 1
#			print("PanelDisplayXYZ: axe={}, CourseMax={}, offset={}, valMax ={}".
#				format(axe, self.data.getFloatCourseMax(axe), self.offset[axe], self.valMax[axe]))

# ----- Visualisation XYZFS ---------

	def setXp(self, val):									# Visualisation de la position X
		if (isinstance(val, float)):						# val doit être de type float
			self.valP['x'] = val
			str = self.ff.format(val)
			self._setEntry(self.entryXp, str)
		else:
			self._setEntry(self.entryXp, "ERR")

	def setYp(self, val):
		if (isinstance(val, float)):						# Visualisation de la position Y
			self.valP['y'] = val
			str = self.ff.format(val)
			self._setEntry(self.entryYp, str)
		else:
			self._setEntry(self.entryYp, "ERR")

	def setZp(self, val):									# Visualisation de la position Z
		if (isinstance(val, float)):
			self.valP['z'] = val
			str = self.ff.format(val)
			self._setEntry(self.entryZp, str)
		else:
			self._setEntry(self.entryZp, "ERR")

	def setF(self, val):									# Visualisation de la vitesse de déplacement de la broche
		if (isinstance(val, float)):
			self.valF = val
			self._setEntry(self.entryF, str(val))
		else:
			self._setEntry(self.entryF, "ERR")

	def setS(self, val):									# Visualisation de la vitesse de rotation de la broche
		if (isinstance(val, float)):
			self.valS = val
			self._setEntry(self.entryS, str(val))
		else:
			self._setEntry(self.entryS, "ERR")

# ----- Sauvegarde et restauration des valeurs XYZ ---------

	def saveXYp(self):										# Sauvegarde de la position des axes XY
		for axe in ['x', 'y']:
			self.memP[axe] = self.valP[axe]

	def saveZp(self):										# Sauvegarde de la position de l'axe Z
		self.memP['z'] = self.valP['z']

	def restoreXYp(self):									# Restauration de position mémorisée des axes XY
		self.valP['x'] = self.memP['x']
		str = self.ff.format(self.valP['x'])
		self._setEntry(self.entryXp, str)
		self.valP['y'] = self.memP['y']
		str = self.ff.format(self.valP['y'])
		self._setEntry(self.entryYp, str)

	def restoreZp(self):									# Restauration de position mémorisée de l'axe Z
		self.valP['z'] = self.memP['z']
		str = self.ff.format(self.valP['z'])
		self._setEntry(self.entryZp, str)

# ----- Calcul des positions et vitesse de déplacement suite à l'envoi d'un seul step vers les axes XYZ ---------

#	Tronc commun de calcul et l'affichage pour les 3 axes XYZ

	def addOneStepXYZ(self, axe, sens):
		currentTs = 0.0
		vitesse = 0.0

		if (sens == '+'):
			if (self.valP[axe] >= self.valMax[axe]):
				print("PanelDisplayXYZ:", sens, self.valP[axe], self.valMax[axe])
				return(False)
		if (sens == '-'):
			if (self.valP[axe] <= 0):
				print("PanelDisplayXYZ:", sens, self.valP[axe], self.valMax[axe])
				return(False)
		print("PanelDisplayXYZ:", sens, self.valP[axe], self.valMax[axe])

		# Calculs du temps écoulé entre deux steps
		currentTs = time.time()										# Timestamp actuel en secondes
		deltaTimeMin = (currentTs - self.lastTimestamp) / 60		# Temps en minutes écoulé entre deux steps vers le moteur
		self.lastTimestamp = currentTs								# Mise à jour du dernier temps pour le prochain calcul

		# Calcul de la vitesse de déplacement entre deux pulses
		F = self.data.getFloatDeplParPuls(axe) / deltaTimeMin		# Vitesse en millimètres par minute entre deux pas
		str = "{:0.4f}".format(F)									# Formattage de présentation de la vitesse calculée
		self._setEntry(self.entryF, str)							# Affichage de la vitesse calculée

		if (sens == '+'):
			self.valP[axe] += self.data.getFloatDeplParPuls(axe)			# Ajout du déplacement origine Pièce
		else:
			self.valP[axe] -= self.data.getFloatDeplParPuls(axe)
		str = self.ff.format(self.valP[axe])
		self._setEntry(self.entryP[axe], str)						# Affichage

		str = self.ff.format(self.offset[axe]+ self.valP[axe])		# Calcul du déplacement à l'offset Machine/Pièce
		self._setEntry(self.entryM[axe], str)						# Affichage
		return(True)

	def getValXYZ(self, axe):
		return(self.valP[axe])

	def _setEntry(self, objEntry, txt):
		objEntry.config(state = NORMAL)
		objEntry.delete(0, END)
		objEntry.insert(0, txt)
		objEntry.config(state = "readonly")

	def changeColor(self, axe, color):
		self.entryP[axe].config(bg = color)


# Programme principal de test
# ---------------------------

if __name__ == "__main__":

	def runMoteurX(lgEnMil):
		th = ThreadPulse(w, 'x', '+', pdis, dt, lgEnMil, retThread )
		th.start()

	def runMoteurY(lgEnMil):
		th = ThreadPulse(w, 'y', '+', pdis, dt, lgEnMil, retThread )
		th.start()
		pass

	def runMoteurZ(lgEnMil):
		th = ThreadPulse(w, 'z', '+', pdis, dt, lgEnMil, retThread )
		th.start()
		pass

	def runMoteurXYZ():
#		thx = ThreadPulseX(w, panel, lgEnMil)
#		thy = ThreadPulseY(w, lgEnMil, panel)
#		thz = ThreadPulseZ(w, lgEnMil, panel)
#		thx.start()
#		thy.start()
#		thz.start()
		pass

	def stop():
		global stopUrgence
		stopUrgence = True

	def param():
		winPar = WinParam(w, dt)

	def retThread(axe, stopAxe):
		print("PanelDisplayXYZ: retThread: axe={}, stopAxe={}".format(axe, stopAxe))

	stopUrgence = False

	w = Tk()
	w.title('classe PanelXYZ et des Thread moteur')
	dt = DataParam()													# Installation des données de paramètrage du matériel
	pdis = PanelDisplayXYZ(w, data = dt)
	pdis.pack()

	frm = Frame(w)
	dim = 10
	btnClear = Button(frm, width = dim, text="Clear All", command=pdis.clear)
	btnClear.grid(row = 1, column = 1)

	btnCalage = Button(frm, width = dim, text="Calage M", command=pdis.calage)
	btnCalage.grid(row = 1, column = 2)

	btnOrigPiece = Button(frm, width = dim, text="Set origine XY", command = pdis.setOrigPieceXY)
	btnOrigPiece.grid(row = 1, column = 3)

	btnOrigPiece = Button(frm, width = dim, text="Set origine Z", command = pdis.setOrigPieceZ)
	btnOrigPiece.grid(row = 1, column = 4)

	BtnSetXp = Button(frm, width = dim, text="Set Xp", command = lambda val = 100.0: pdis.setXp(val))
	BtnSetXp.grid(row = 2, column = 1)

	BtnSetYp = Button(frm, width = dim, text="Set Yp", command = lambda val = 200.0: pdis.setYp(val))
	BtnSetYp.grid(row = 2, column = 2)

	BtnSetZp = Button(frm, width = dim, text="Set Zp", command = lambda val = 10.0: pdis.setZp(val))
	BtnSetZp.grid(row = 2, column = 3)

	BtnSavXp = Button(frm, width = dim, text="Save XY", command = pdis.saveXYp)
	BtnSavXp.grid(row = 3, column = 1)

	BtnSavZp = Button(frm, width = dim, text="Save Z", command = pdis.saveZp)
	BtnSavZp.grid(row = 3, column = 2)

	BtnRstXp = Button(frm, width = dim, text="Restore XY", command = pdis.restoreXYp)
	BtnRstXp.grid(row = 3, column = 3)

	BtnRstZp = Button(frm, width = dim, text="Restore Z", command = pdis.restoreZp)
	BtnRstZp.grid(row = 3, column = 4)

	BtnPitchXp = Button(frm, width = dim, text="0.1 mm sur X", command = lambda lg = 0.1: runMoteurX(lg))
	BtnPitchXp.grid(row = 4, column = 1)

	BtnPitchYp = Button(frm, width = dim, text="1.0 mm sur Y", command = lambda lg = 1: runMoteurY(lg))
	BtnPitchYp.grid(row = 4, column = 2)
	frm.pack()

	BtnPitchZp = Button(frm, width = dim, text="10.0 mm sur Z", command = lambda lg = 10: runMoteurZ(lg))
	BtnPitchZp.grid(row = 4, column = 3)

	BtnPitchXYZp = Button(frm, width = dim, text="10.0 mm XYZ", command = lambda lg = 10: runMoteurXYZ(lg))
	BtnPitchXYZp.grid(row = 4, column = 4)

	BtnStop = Button(frm, width = dim, text="STOP", command = stop)
	BtnStop.grid(row = 5, column = 1)

	BtnPAR = Button(frm, width = dim, text="Paramètres", command = param)
	BtnPAR.grid(row = 5, column = 2)

	w.mainloop()
