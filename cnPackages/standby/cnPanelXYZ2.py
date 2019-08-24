#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
from threading import Thread
import time
try:
	from cnWinParam import WinParam
	from cnWinParam import EntryRegx
	from cnDataParam import DataParam
except:
	from myPackages.cnWinParam import WinParam
	from myPackages.cnWinParam import EntryRegx
	from myPackages.cnDataParam import DataParam

class PanelXYZ(Frame):
	def __init__(self, boss, data = None, baseFont = "Courier 8 normal", bg = 'ivory', pady = 5, padx = 0,
			RD = 1.0, PM = 200.0, PV = 1.0, RR = 1.0, PPS = 200.0, width = 300, height = 150,
			maxLenX = 300, maxLenY = 300, maxLenZ = 200):
		Frame.__init__(self, boss, bd = 2, relief = SUNKEN, bg = bg)
		self.data = data
		myFontTitre1	= "{courier new} 8"
		myFontTitre2	= "{courier new} 7"
		myFontXYZ		= "{courier new} 14 bold"

		self.frm1 = Frame(self, bg = bg, pady = 5)
		self.frm1.pack()
		Label(self.frm1, text ="Positionnement de la broche", font = myFontTitre1, bg = bg, fg = "blue").grid(row = 1, column = 2, columnspan = 2)
		Label(self.frm1, text ="Machine(mm)", font = myFontTitre2, bg = bg, fg = "grey").grid(row = 2, column = 2)
		Label(self.frm1, text ="Pièce(mm)", font = myFontTitre2, bg = bg, fg = "grey").grid(row = 2, column = 3)

		Label(self.frm1, text ="Vitesse de progression de la broche", font = myFontTitre1, bg = bg, fg = "blue").grid(row = 1, column = 4, columnspan = 3)
		Label(self.frm1, text ="Maximum(m/mn)",  font = myFontTitre2, bg = bg, fg = "grey").grid(row = 2, column = 4)
		Label(self.frm1, text ="Demandée(m/mn)", font = myFontTitre2, bg = bg, fg = "grey").grid(row = 2, column = 5)
		Label(self.frm1, text ="Calculée(m/mn)", font = myFontTitre2, bg = bg, fg = "grey").grid(row = 2, column = 6)

		Label(self.frm1, text ="X", font = myFontXYZ, bg = bg, fg = "blue").grid(row = 3, column = 1)
		Label(self.frm1, text ="Y", font = myFontXYZ, bg = bg, fg = "blue").grid(row = 4, column = 1)
		Label(self.frm1, text ="Z", font = myFontXYZ, bg = bg, fg = "blue").grid(row = 5, column = 1)

# Affichage de la position de la broche par rapport aux butées des axes machine
		self.entryXma = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryXma.grid(row = 3, column = 2)
		self.entryYma = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryYma.grid(row = 4, column = 2)
		self.entryZma = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryZma.grid(row = 5, column = 2)

# Affichage de la position de la broche par rapport à l'origine pièce défini
		self.entryXop = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryXop.grid(row = 3, column = 3)
		self.entryYop = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryYop.grid(row = 4, column = 3)
		self.entryZop = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryZop.grid(row = 5, column = 3)

# Affichage de la vitesse de déplacement maximum possible sur les trois axes
		self.entryXvm = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryXvm.grid(row = 3, column = 4)
		self.entryYvm = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryYvm.grid(row = 4, column = 4)
		self.entryZvm = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryZvm.grid(row = 5, column = 4)

# Affichage de la vitesse de déplacement demandée sur les trois axes
		self.entryXvd = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryXvd.grid(row = 3, column = 5)
		self.entryYvd = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryYvd.grid(row = 4, column = 5)
		self.entryZvd = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryZvd.grid(row = 5, column = 5)

# Affichage de la vitesse de déplacement calculée sur les trois axes
		self.entryXvc = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryXvc.grid(row = 3, column = 6)
		self.entryYvc = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryYvc.grid(row = 4, column = 6)
		self.entryZvc = Entry(self.frm1, justify = RIGHT, state = "readonly")
		self.entryZvc.grid(row = 5, column = 6)

		self.frm2 = Frame(self, bg = bg, pady = 5)
		self.frm2.pack()
		Label(self.frm2, text ="Vitesse de déplacement résultante(m/mn)", font = myFontTitre2, bg = bg, fg = "grey").grid(row = 1, column = 1, sticky = "w")
		Label(self.frm2, text ="Accélération maximum", font = myFontTitre2, bg = bg, fg = "grey").grid(row = 2, column = 1, sticky = "w")
		Label(self.frm2, text ="Vitesse de rotation demandée de broche(t/mn)", font = myFontTitre2, bg = bg, fg = "grey").grid(row = 3, column = 1, sticky = "w")

		self.entryVre = Entry(self.frm2, justify = RIGHT, state = "readonly")
		self.entryVre.grid(row = 1, column = 2)
		self.entryAde = Entry(self.frm2, justify = RIGHT, state = "readonly")
		self.entryAde.grid(row = 2, column = 2)
		self.entryVbr = Entry(self.frm2, justify = RIGHT, state = "readonly")
		self.entryVbr.grid(row = 3, column = 2)


		self.entryList = [self.entryXma, self.entryYma, self.entryZma, self.entryXop, self.entryYop, self.entryZop,
						  self.entryXvm, self.entryYvm, self.entryZvm, self.entryXvd, self.entryYvd, self.entryZvd, self.entryXvc, self.entryYvc, self.entryZvc,
						  self.entryVre, self.entryAde, self.entryVbr]

		self.entListM = [self.entryXma, self.entryYma, self.entryZma]
		self.entListP = [self.entryXop, self.entryYop, self.entryZop]

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

		self.memXop = 0.0
		self.memYop = 0.0
		self.memZop = 0.0

		self.lastTimestamp = 0.0

		self.ff = "{:0.4f}"									# Format de présentation des "float"

		self._insertAllEntry()



#		self.entryF = Entry(self, justify = RIGHT, width = eWidth, state = "readonly")
#		self.entryF.grid(row = 6, column = 2, padx = 5)
#		self.entryS = Entry(self, justify = RIGHT, width = eWidth, state = "readonly")
#		self.entryS.grid(row = 7, column = 2, padx = 5)

	def _insertAllEntry(self):
		for entry in self.entryList:
			entry.config(state = 'normal', width = 10, font = "{courier new} 11")
			entry.delete(0, END)
#			entry.insert(0, str)
			entry.config(state = 'readonly')

	def clear(self):
		global stopUrgence
		stopUrgence = False
		for ent in self.entryList:
			self._setEntry(ent, "-")

	def calage(self):
		for ent in self.entryList:
			str = self.ff.format(0.0)
			self._setEntry(ent, str)

	def setOrigWorkXY(self):
		valXop = float(self.entryXop.get())
		str = self.ff.format(valXop)
		self._setEntry(self.entryXma, str)
		str = self.ff.format(0.0)
		self._setEntry(self.entryXop, str)
		self.offsetX = valXop

		valYop = float(self.entryYop.get())
		str = self.ff.format(valYop)
		self._setEntry(self.entryYma, str)
		str = self.ff.format(0.0)
		self._setEntry(self.entryYop, str)
		self.offsetY = valYop

	def setOrigWorkZ(self):
		valZop = float(self.entryZop.get())
		str = self.ff.format(valZop)
		self._setEntry(self.entryZma, str)
		str = self.ff.format(0.0)
		self._setEntry(self.entryZop, str)
		self.offsetZ = valZop

	def setXop(self, val):									# val doit être de type float
		if (isinstance(val, float)):
			str = self.ff.format(val)
			self._setEntry(self.entryXop, str)
		else:
			self._setEntry(self.entryXop, "ERR")

	def setYop(self, val):
		if (isinstance(val, float)):
			str = self.ff.format(val)
			self._setEntry(self.entryYop, str)
		else:
			self._setEntry(self.entryYop, "ERR")

	def setZop(self, val):
		if (isinstance(val, float)):
			str = self.ff.format(val)
			self._setEntry(self.entryZop, str)
		else:
			self._setEntry(self.entryZop, "ERR")

	def setF(self, val):
		if (isinstance(val, float)):
			self._setEntry(self.entryXvc, str(val))
		else:
			self._setEntry(self.entryXvc, "ERR")

	def setS(self, val):
		if (isinstance(val, float)):
			self._setEntry(self.entryS, str(val))
		else:
			self._setEntry(self.entryS, "ERR")

	def saveXYop(self):
		strX = self.entryXop.get()
		self.memXop = float(strX)
		strY = self.entryYop.get()
		self.memYop = float(strY)

	def saveZop(self):
		strZ = self.entryZop.get()
		self.memZop = float(strZ)

	def restoreXYop(self):
		str = self.ff.format(self.memXop)
		self._setEntry(self.entryXop, str)
		str = self.ff.format(self.memYop)
		self._setEntry(self.entryYop, str)

	def restoreZop(self):
		str = self.ff.format(self.memZop)
		self._setEntry(self.entryZop, str)

	def addOneStepXop(self):
		self._addOneStepXYZ(self.entryXop, self.entryXma, self.entryXvd)

	def addOneStepYop(self):
		self._addOneStepXYZ(self.entryYop, self.entryYma)

	def addOneStepZp(self):
		self._addOneStepXYZ(self.entryZop, self.entryZma)

	def _addOneStepXYZ(self, entP, entM, entVd):

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
		self._setEntry(self.entryXvc, str)							# Affichage de la vitesse calculée

		valP = float(entP.get())
		valP += lgMil
		str = self.ff.format(valP)
		self._setEntry(entP, str)

		valM = float(entM.get())
		valM += lgMil
		str = self.ff.format(valM)
		self._setEntry(entM, str)

	def getValXop(self):
		str = self.entryXop.get()
		val = float(str)
		return(val)

	def getValYop(self):
		str = self.entryYop.get()
		val = float(str)
		return(val)

	def getValZop(self):
		str = self.entryZop.get()
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
		lgMax				= self.data.getFloatCourseMax('x')		# ex:  300 millimètres
		avanceMmParPulse	= self.data.getFloatDeplParPuls('x')	# ex:    0.003125 millimètres par pulse
		vitesseDeplMn		= self.data.getFloatVitesseMaxDepl('x')	# ex: 1000 millimètres par minute
		acceleration		= self.data.getFloatAccelerMax('x')		# ex:    3 mètres par seconde par seconde

		nbPulses 			= int(self.lgMil / avanceMmParPulse)	# ex: lgMil = 0.1 mm / 0.003125 = 32 pulses
		freqMaxPulseHz		= 1/ ((vitesseDeplMn / 60) / self.lgMil)		# ex: 1000 millimètres en 60 secondes = 16,6666666667 mm/s
																	# 0.1 / 16.66666 = 0.0060000 => 1/0.006 = 166 hertz

#		print("nbPulses = {}".format(self.nbPulses))
		n = 0
		while (n < nbPulses):
			if (stopUrgence == False):
				self.panel.addOneStepXop()
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
	w.title('Test de la classe PanelXYZ et des Thread moteur')
	dt = DataParam()													# Installation des données de paramètrage du matériel
	p = PanelXYZ(w, data = dt)
	p.pack()
	w.config(bg = 'ivory', padx = 0)

	frm = Frame(w, relief = GROOVE, bg = 'ivory', pady = 15)
	dim = 10
	btnClear = Button(frm, width = dim, text="Clear All", command=p.clear)
	btnClear.grid(row = 1, column = 1)

	btnCalage = Button(frm, width = dim, text="Calage M", command=p.calage)
	btnCalage.grid(row = 1, column = 2)

	btnOrigWork = Button(frm, width = dim, text="Set origine XY", command = p.setOrigWorkXY)
	btnOrigWork.grid(row = 1, column = 3)

	btnOrigWork = Button(frm, width = dim, text="Set origine Z", command = p.setOrigWorkZ)
	btnOrigWork.grid(row = 1, column = 4)

	BtnSetXp = Button(frm, width = dim, text="Set Xp", command = lambda val = 100.0: p.setXop(val))
	BtnSetXp.grid(row = 2, column = 1)

	BtnSetYp = Button(frm, width = dim, text="Set Yp", command = lambda val = 200.0: p.setYop(val))
	BtnSetYp.grid(row = 2, column = 2)

	BtnSetZp = Button(frm, width = dim, text="Set Zp", command = lambda val = 10.0: p.setZop(val))
	BtnSetZp.grid(row = 2, column = 3)

	BtnSavXp = Button(frm, width = dim, text="Save XY", command = p.saveXYop)
	BtnSavXp.grid(row = 3, column = 1)

	BtnSavZp = Button(frm, width = dim, text="Save Z", command = p.saveZop)
	BtnSavZp.grid(row = 3, column = 2)

	BtnRstXp = Button(frm, width = dim, text="Restore XY", command = p.restoreXYop)
	BtnRstXp.grid(row = 3, column = 3)

	BtnRstZp = Button(frm, width = dim, text="Restore Z", command = p.restoreZop)
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