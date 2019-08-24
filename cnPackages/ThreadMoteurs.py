#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
from threading import Thread
import time

#try:
#	from cnPackages.PanelMoteurs import *
#	from cnPackages.DataParam import DataParam
#	from cnPackages.PanelDisplayXYZ	import PanelDisplayXYZ
#except:

try:
	from PanelDisplayXYZ import PanelDisplayXYZ
except:
	print("ThreadMoteurs : Erreur import PanelDisplayXYZ")
try:
	from PanelMoteurs import *
except:
	print("ThreadMoteurs : Erreur import PanelMoteurs")
try:
	from DataParam import DataParam
except:
	print("ThreadMoteurs : Erreur import DataParam")


#------ Thread Moteurs ------
OK = True
KO = False

class ThreadPulse(Thread):
	def __init__(self, win, axe, sens, panelXYZ, dataParam, lgEnMil, retThread):
		Thread.__init__(self)
		self.w = win													# Fenêtre principale
		self.axe = axe
		self.sens = sens
		self.panelXYZ = panelXYZ										# Référence au paneau d'affichage
		self.data = dataParam											# Référence aux paramètres machine
		frequence = self.data.getFloatFrequencePuls(axe)				# ex: 5333 hertz
		self.delay = 1 / frequence										# Delai entre deux pulses soit 1/5333 = 0.1875 millisecondes
		self.lgEnMil = lgEnMil											# Longueur à parcourir en millimètres
		self.retThread = retThread										# Référence à la fonction de fin d'action
#		print("frequence=", frequence, "delay=", self.delay)

	def run(self):
		global stopUrgence
		stopUrgence = False
		lgMax	= self.data.getFloatCourseMax(self.axe)					# ex:  300 millimètres
		app		= self.data.getFloatDeplParPuls(self.axe)				# ex:    0.003125 millimètres par pulse
		vdmn	= self.data.getFloatVitesseMaxDepl(self.axe)			# ex: 1000 millimètres par minute
		acc		= self.data.getFloatAccelerMax(self.axe)				# ex:    3 mètres par seconde par seconde

		nbPulses 			= self.lgEnMil / app 						# ex: lgEnMil = 0.1 mm / 0.003125 = 32 pulses
		print("ThreadMoteurs: lgEnMil={:0.7f}, app={:0.7f}, nbPulses={:0.7f}".format(self.lgEnMil, app, nbPulses))
		nbPulses = int(nbPulses)
		freqMaxPulseHz		= 1 / ((vdmn / 60) / self.lgEnMil)			# ex: 1000 millimètres en 60 secondes = 16,6666666667 mm/s																		# 0.1 mm / 16.66666 = 0.0060000 => 1/0.006 = 166 hertz


		n = 0
		self.stopAxe = False
		while (n < nbPulses):
			if (stopUrgence == False):
				ret = self.panelXYZ.addOneStepXYZ(self.axe, self.sens)	#
				if (ret == True):
					time.sleep(self.delay)
					n += 1
				else:										# Arrêt demandé pour Cause de fin de déplacement possible
					self.retThread(self.axe, True)
					return
				self.w.update()
			else:
				print("Arrêt d'urgence demandé")
				break
		self.retThread(self.axe, False)



class ThreadCalage(Thread):
	rdv = 0													# Variable de Class : comptage des Thread actifs : Point de RDV des Thread
	def __init__(self, axe, pnlDisMot, atm, pnlDisXYZ, pnlBC, delay):
		Thread.__init__(self)
		self.axe = axe										# Axe concerné : 'X', 'Y', 'Z'
		self.pnlDisMot = pnlDisMot							# Référence au Panel visualisant les moteurs en rotation
		self.atm = atm										# Référence à l'automate pour lui envoyer un événement de fin de tâche
		self.pnlDisXYZ = pnlDisXYZ							# Référence au Panel visualisant les positions courantes des axes X Y et Z
		self.pnlBC = pnlBC									# Référence au Panel des boutons de commande généraux
		self.delay = delay									# Provisoire pour la simulation d'une action lente

	def run(self):
#		global stopUrgence									# Pour plustard quand le Hardware sera là
		ThreadCalage.rdv += 1								# Incrémenter le nombre de Thread en cours
		self.pnlDisMot.start(self.axe)						# Visualisation de la rotation du moteur
		self.pnlDisMot.sensT(self.axe)						# Calage en ARRIERE sur les switchs de butée
		time.sleep(self.delay)								# Simulation en attendant le hardware
		self.pnlDisMot.stop(self.axe)						# Visualisation : moteur à l'arrêt
		ThreadCalage.rdv -= 1								# Décrémenter le compteur des instances en cours
#		print(self.axe, ThreadCalage.rdv)
		if (ThreadCalage.rdv == 0):							# Tous les thread ont terminé leur mission
			if (self.pnlDisXYZ is not None):				# En phase de test unitaire pnlDisXYZ n'est pas renseigné
				self.pnlDisXYZ.calage()						# Mettre à zéro le positionnement XYZ
			if (self.pnlBC is not None):					# En phase de test unitaire pnlBC n'est pas renseigné
				self.pnlBC.stop('POM')						# Suppression du clignotement du bouton 'POM' (Calage machine)
			if (self.atm is not None):						# En phase de test unitaire atm n'est pas renseigné
				self.atm.execActionAndGetNewPhase('ANN')	# Informer l'automate de la fin d'exécution de la tache de calage machine
															# Une fois que TOUS les Thread aient terminé leur travail



# Programme principal de test
# ---------------------------

if __name__ == "__main__":

	def avanceX(lg):										# Pour le test unitaire
		tp = ThreadPulse(win = w, axe = 'x', sens = '+', panelXYZ = pxyz, dataParam = dt, lgEnMil = lg, retThread = retThread)
		tp.start()

	def retThread(axe, stopAxe):										# Pour le test unitaire
		print("ThreadMoteurs: retThread: axe={}, stopAxe={}".format(axe, stopAxe))

	stopUrgence = False

	w = Tk()
	w.title('classe Thread moteur')
	dt = DataParam()

	pxyz = PanelDisplayXYZ(w, dt)
	pxyz.pack()
	pxyz.clear()

	pdam = PanelDisplayAllMotors(w)
	pdam.pack()
	pdam.stopAll()

	thx = ThreadCalage(axe = 'X', pnlDisMot = pdam, atm = None, pnlDisXYZ = pxyz, pnlBC = None, delay = 5)
	thx.start()
	thy = ThreadCalage(axe = 'Y', pnlDisMot = pdam, atm = None, pnlDisXYZ = pxyz, pnlBC = None, delay = 8)
	thy.start()
	thz = ThreadCalage(axe = 'Z', pnlDisMot = pdam, atm = None, pnlDisXYZ = pxyz, pnlBC = None, delay = 6)
	thz.start()

	frm =Frame(w)
	frm.pack()
	lg = 10
	btnPulseA = Button(frm, text = "10 mm sur X", command = lambda arg = lg: avanceX(arg))
	btnPulseA.pack(side = LEFT)
	lg = 0.1
	btnPulseB = Button(frm, text = "0.1 mm sur X", command = lambda arg = lg: avanceX(arg))
	btnPulseB.pack(side = LEFT)
	w.mainloop()


