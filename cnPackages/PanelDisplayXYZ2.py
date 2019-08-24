#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
from threading import Thread
import time
try:
	from WinParam  import WinParam
	from EntryRegx import EntryRegx
	from DataParam import DataParam
except:
	from cnPackages.WinParam  import WinParam
	from cnPackages.EntryRegx import EntryRegx
	from cnPackages.DataParam import DataParam

class PanelDisplayXYZ(Frame):
#	def __init__(self, boss, data = None, baseFont = "Courier 8 normal", bg = "ivory", width = 50, height = 50,
	def __init__(self, boss, data = None, baseFont = "Courier 8 normal", bg = "ivory",
					RD = 1.0, PM = 200.0, PV = 1.0, RR = 1.0, PPS = 200.0,
					maxLenX = 300, maxLenY = 300, maxLenZ = 200):
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

# Mémorisation des diverses valeurs concernant l'environnement matériel
		self.data = data
		avanceMmParPulseX	= self.data.getFloatDeplParPuls('x')	# ex:    0.003125 millimètres par pulse
		vitesseDeplMnX		= self.data.getFloatVitesseMaxDepl('x')	# ex: 1000 millimètres par minute
		accelerationX		= self.data.getFloatAccelerMax('x')		# ex:    3 mètres par seconde par seconde
		avanceMmParPulseY	= self.data.getFloatDeplParPuls('y')	# ex:    0.003125 millimètres par pulse
		vitesseDeplMnY		= self.data.getFloatVitesseMaxDepl('y')	# ex: 1000 millimètres par minute
		accelerationY		= self.data.getFloatAccelerMax('y')		# ex:    3 mètres par seconde par seconde
		avanceMmParPulseZ	= self.data.getFloatDeplParPuls('z')	# ex:    0.003125 millimètres par pulse
		vitesseDeplMnZ		= self.data.getFloatVitesseMaxDepl('z')	# ex: 1000 millimètres par minute
		accelerationZ		= self.data.getFloatAccelerMax('z')		# ex:    3 mètres par seconde par seconde

		self.PPS		= PPS									# Cadence maximum d'envoi des puls vers le moteur PAP ex:200 hertz
		self.PM			= PM									# Nombre de steps pour un tour ex:200 steps
		self.RD			= RD									# RD - Réglage du driver, il peut être réglé en pas entier, demi pas, quart de pas etc.
		self.RR			= RR									# RR - Rapport de réduction entre le moteur et la vis.
		self.PV			= PV									# Pas des vis sans fin en mm ex: 1mm par tour

		self.maxLenX	= maxLenX								# Course maximum pour l'axe X ex: 300 mm
		self.maxLenY	= maxLenY								# Course maximum pour l'axe Y ex: 300 mm
		self.maxLenZ	= maxLenZ								# Course maximum pour l'axe Z ex: 100 mm

		self.offsetX = 0.0
		self.offsetY = 0.0
		self.offsetZ = 0.0

		self.memXp = 0.0
		self.memYp = 0.0
		self.memZp = 0.0

		self.lastTimestamp = 0.0

		self.ff = "{:0.4f}"									# Format de présentation des "float"

	def clear(self):
		global stopUrgence
		stopUrgence = False
		for ent in self.entListM+self.entListP:
			self._setEntry(ent, "-")

	def calage(self):
		for ent in self.entListM+self.entListP:
			str = self.ff.format(0.0)
			self._setEntry(ent, str)

	def setOrigWorkXY(self):
		valXp = float(self.entryXp.get())
		str = self.ff.format(valXp)
		self._setEntry(self.entryXm, str)
		str = self.ff.format(0.0)
		self._setEntry(self.entryXp, str)
		self.offsetX = valXp

		valYp = float(self.entryYp.get())
		str = self.ff.format(valYp)
		self._setEntry(self.entryYm, str)
		str = self.ff.format(0.0)
		self._setEntry(self.entryYp, str)
		self.offserY = valYp

	def setOrigWorkZ(self):
		valZp = float(self.entryZp.get())
		str = self.ff.format(valZp)
		self._setEntry(self.entryZm, str)
		str = self.ff.format(0.0)
		self._setEntry(self.entryZp, str)
		self.offsetZ = valZp

	def setXp(self, val):									# val doit être de type float
		if (isinstance(val, float)):
			str = self.ff.format(val)
			self._setEntry(self.entryXp, str)
		else:
			self._setEntry(self.entryXp, "ERR")

	def setYp(self, val):
		if (isinstance(val, float)):
			str = self.ff.format(val)
			self._setEntry(self.entryYp, str)
		else:
			self._setEntry(self.entryYp, "ERR")

	def setZp(self, val):
		if (isinstance(val, float)):
			str = self.ff.format(val)
			self._setEntry(self.entryZp, str)
		else:
			self._setEntry(self.entryZp, "ERR")

	def setF(self, val):
		if (isinstance(val, float)):
			self._setEntry(self.entryF, str(val))
		else:
			self._setEntry(self.entryF, "ERR")

	def setS(self, val):
		if (isinstance(val, float)):
			self._setEntry(self.entryS, str(val))
		else:
			self._setEntry(self.entryS, "ERR")

	def saveXYp(self):
		strX = self.entryXp.get()
		self.memXp = float(strX)
		strY = self.entryYp.get()
		self.memYp = float(strY)

	def saveZp(self):
		strZ = self.entryZp.get()
		self.memZp = float(strZ)

	def restoreXYp(self):
		str = self.ff.format(self.memXp)
		self._setEntry(self.entryXp, str)
		str = self.ff.format(self.memYp)
		self._setEntry(self.entryYp, str)

	def restoreZp(self):
		str = self.ff.format(self.memZp)
		self._setEntry(self.entryZp, str)

	def addOneStepXp(self):
		self._addOneStepXYZ(self.entryXp, self.entryXm)

	def addOneStepYp(self):
		self._addOneStepXYZ(self.entryYp, self.entryYm)

	def addOneStepZp(self):
		self._addOneStepXYZ(self.entryZp, self.entryZm)

	def _addOneStepXYZ(self, entP, entM):
		currentTs = 0.0
		lgMil = 0.0													# lmm : sera la longueur effectuée en millimètres
		vitesse = 0.0
		try:
			lgMil = self.PV / self.PM								# lmm = longueur effectueé lors d'un pas moteur
		except:
			print("Erreur division")
		currentTs = time.time()										# Timestamp actuel en secondes
		deltaTimeMin = (currentTs - self.lastTimestamp) / 60		# Temps en minutes écoulé entre deux pas moteur
		self.lastTimestamp = currentTs								# Mise à jour du dernier temps pour le prochain calcul

		vitesse = lgMil / deltaTimeMin								# Vitesse en millimètres par minute entre deux pas
		str = "{:0.4f}".format(vitesse)								# Formattage de présentation de la vitesse calculée
		self._setEntry(self.entryF, str)							# Affichage de la vitesse calculée

		valP = float(entP.get())
		valP += lgMil
		str = self.ff.format(valP)
		self._setEntry(entP, str)

		valM = float(entM.get())
		valM += lgMil
		str = self.ff.format(valM)
		self._setEntry(entM, str)

	def getValXp(self):
		str = self.entryXp.get()
		val = float(str)
		return(val)

	def getValYp(self):
		str = self.entryYp.get()
		val = float(str)
		return(val)

	def getValZp(self):
		str = self.entryZp.get()
		val = float(str)
		return(val)

	def _setEntry(self, objEntry, txt):
		objEntry.config(state = NORMAL)
		objEntry.delete(0, END)
		objEntry.insert(0, txt)
		objEntry.config(state = "readonly")

class ThreadPulseX(Thread):
	def __init__(self, win, panelXYZ, dataParam, lgMil, PPS = 200.0):
		Thread.__init__(self)
		self.w      = win				# Fenêtre principale
		self.panel  = panelXYZ			# Référence au paneau d'affichage
		self.data   = dataParam			# Référence aux paramètres machine
		self.delay  = 1 / PPS			# Delai minimum entre deux pulses ex: pps = 200 hertz, soit 1/200 = 5.000 millisecondes
		self.lgMil = lgMil

	def run(self):
		global stopUrgence
		lgMax				= self.data.getFloatCourseMax('x')			# ex:  300 millimètres
		avanceMmParPulse	= self.data.getFloatDeplParPuls('x')		# ex:    0.003125 millimètres par pulse
		vitesseDeplMn		= self.data.getFloatVitesseMaxDepl('x')		# ex: 1000 millimètres par minute
		acceleration		= self.data.getFloatAccelerMax('x')			# ex:    3 mètres par seconde par seconde

		nbPulses 			= int(self.lgMil / avanceMmParPulse)		# ex: lgMil = 0.1 mm / 0.003125 = 32 pulses
		freqMaxPulseHz		= 1/ ((vitesseDeplMn / 60) / self.lgMil)	# ex: 1000 millimètres en 60 secondes = 16,6666666667 mm/s
																		# 0.1 / 16.66666 = 0.0060000 => 1/0.006 = 166 hertz

#		print("nbPulses = {}".format(self.nbPulses))
		n = 0
		while (n < nbPulses):
			if (stopUrgence == False):
				self.panel.addOneStepXp()
				time.sleep(self.delay)
				n += 1
				self.w.update()
#				print("Pulse sur X : {}".format(n))
			else:
#				print("Arrêt d'urgence demandé")
				break


# Programme principal de test
# ---------------------------

if __name__ == "__main__":

	def runMoteurX(lgMil):
		th = ThreadPulseX(w, p, dt, lgMil)
		th.start()

	def runMoteurY():
#		th = ThreadPulseY(w, p, dt, lgMil)
#		th.start()
		pass

	def runMoteurZ():
#		th = ThreadPulseZ(w, p, dt, lgMil)
#		th.start()
		pass

	def runMoteurXYZ():
#		thx = ThreadPulseX(w, panel, lgMil)
#		thy = ThreadPulseY(w, lgMil, panel)
#		thz = ThreadPulseZ(w, lgMil, panel)
#		thx.start()
#		thy.start()
#		thz.start()
		pass

	def stop():
		global stopUrgence
		stopUrgence = True

	def param():
		winPar = WinParam(w, dt)


	stopUrgence = False

	w = Tk()
	w.title('classe PanelXYZ et des Thread moteur')
	dt = DataParam()													# Installation des données de paramètrage du matériel
	p = PanelDisplayXYZ(w, data = dt)
	p.pack()

	frm = Frame(w)
	dim = 10
	btnClear = Button(frm, width = dim, text="Clear All", command=p.clear)
	btnClear.grid(row = 1, column = 1)

	btnCalage = Button(frm, width = dim, text="Calage M", command=p.calage)
	btnCalage.grid(row = 1, column = 2)

	btnOrigWork = Button(frm, width = dim, text="Set origine XY", command = p.setOrigWorkXY)
	btnOrigWork.grid(row = 1, column = 3)

	btnOrigWork = Button(frm, width = dim, text="Set origine Z", command = p.setOrigWorkZ)
	btnOrigWork.grid(row = 1, column = 4)

	BtnSetXp = Button(frm, width = dim, text="Set Xp", command = lambda val = 100.0: p.setXp(val))
	BtnSetXp.grid(row = 2, column = 1)

	BtnSetYp = Button(frm, width = dim, text="Set Yp", command = lambda val = 200.0: p.setYp(val))
	BtnSetYp.grid(row = 2, column = 2)

	BtnSetZp = Button(frm, width = dim, text="Set Zp", command = lambda val = 10.0: p.setZp(val))
	BtnSetZp.grid(row = 2, column = 3)

	BtnSavXp = Button(frm, width = dim, text="Save XY", command = p.saveXYp)
	BtnSavXp.grid(row = 3, column = 1)

	BtnSavZp = Button(frm, width = dim, text="Save Z", command = p.saveZp)
	BtnSavZp.grid(row = 3, column = 2)

	BtnRstXp = Button(frm, width = dim, text="Restore XY", command = p.restoreXYp)
	BtnRstXp.grid(row = 3, column = 3)

	BtnRstZp = Button(frm, width = dim, text="Restore Z", command = p.restoreZp)
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
