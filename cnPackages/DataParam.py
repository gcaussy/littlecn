#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *

class DataParam(object):
	def __init__(self):
# Stockage des valeurs de paramètrage machine. elles sont stockées sous forme string, comme elles ont été saisies
		self.axesList = 'x', 'y', 'z'
		self.courseMax		= {'x': '300',			'y': '300',			'z': '300'}			# Course maximum selon les 3 axes en mm (Dépend du matériel)
		self.deplParPuls	= {'x':   '0.003125',	'y':   '0.003125',	'z':   '0.003125'}	# Déplacement de l'outil en millimètres effectué à chaque puls sur le moteur
		self.vitesseMaxDepl	= {'x':'1000',			'y':'1000',			'z':'1000'}			# Vitesse de déplacement maximum de l'outil en millimètres par minute
		self.frequencePuls	= {'x':'5333',			'y':'5333',			'z':'5333'}			# Fréquence d'envoi des pulses vers le driver du moteur
		self.accelerMax		= {'x':   '3',			'y':   '3',			'z':   '3'}			# Accélération maximum sur un déplacement d'outil en m/s/s
		self.invSensRot		= {'x': False,			'y': False,			'z':   False}		# Sens de rotation
		self.maxRotBroche	= "2000"														# Vitesse maximum de rotation de la broche

# Récupération des valeurs de paramètrage à des fins d'affichage. Donc sous forme de string, telles qu'elles ont été saisies

	def loadCourseMax(self, axe):
		if (axe in self.axesList):
			return(self.courseMax[axe])

	def loadDeplParPuls(self, axe):
		if (axe in self.axesList):
			return(self.deplParPuls[axe])

	def loadVitesseMaxDepl(self, axe):
		if (axe in self.axesList):
			return(self.vitesseMaxDepl[axe])

	def loadFrequencePuls(self, axe):
		if (axe in self.axesList):
			return(self.frequencePuls[axe])

	def loadAccelerMax(self, axe):
		if (axe in self.axesList):
			return(self.accelerMax[axe])

	def loadInvSensRot(self, axe):
		if (axe in self.axesList):
			return(self.invSensRot[axe])

	def loadMaxRotBroche(self):
		return(self.maxRotBroche)

# Sauvegarde des valeurs de paramètrage machine

	def saveStrCourseMax(self, axe, strVal):
		if (axe in self.axesList):
			self.courseMax[axe] = strVal

	def saveStrDeplParPuls(self, axe, strVal):
		if (axe in self.axesList):
			self.deplParPuls[axe] = strVal

	def saveStrVitesseMaxDepl(self, axe, strVal):
		if (axe in self.axesList):
			self.vitesseMaxDepl[axe] = strVal

	def saveStrFrequencePuls(self, axe, strVal):
		if (axe in self.axesList):
			self.frequencePuls[axe] = strVal

	def saveStrAccelerMax(self, axe, strVal):
		if (axe in self.axesList):
			self.accelerMax[axe] = strVal

	def saveStrInvSensRot(self, axe, strVal):
		if (axe in self.axesList):
			self.invSensRot[axe] = strVal

	def saveStrMaxRotBroche(self, strVal):
		self.maxRotBroche = strVal

# Récupération des valeurs de paramètrage machine à des fins de calcul. Donc sous forme de float

	def getFloatCourseMax(self, axe):
		if (axe in self.axesList):
			return(float(self.courseMax[axe]))

	def getFloatDeplParPuls(self, axe):
		if (axe in self.axesList):
			return(float(self.deplParPuls[axe]))

	def getFloatVitesseMaxDepl(self, axe):
		if (axe in self.axesList):
			return(float(self.vitesseMaxDepl[axe]))

	def getFloatFrequencePuls(self, axe):
		if (axe in self.axesList):
			return(float(self.frequencePuls[axe]))

	def getFloatAccelerMax(self, axe):
		if (axe in self.axesList):
			return(float(self.accelerMax[axe]))

	def getFloatInvSensRot(self, axe):
		if (axe in self.axesList):
			return(float(self.invSensRot[axe]))

	def getFloatMaxRotBroche(self):
		return(float(self.maxRotBroche))



# Méthodes de test et mise au point

	def printParam1(self):														# Méthode utilisée pour les tests
		print("Print des données stockées")
		for axe in self.courseMax.keys():
			print("courseMax {} = {}".format(axe, self.courseMax[axe]))
		for axe in self.deplParPuls.keys():
			print("deplParPuls {} = {}".format(axe, self.deplParPuls[axe]))
		for axe in self.vitesseMaxDepl.keys():
			print("vitesseMaxDepl {} = {}".format(axe, self.vitesseMaxDepl[axe]))
		for axe in self.frequencePuls.keys():
			print("frequencePuls {} = {}".format(axe, self.frequencePuls[axe]))
		for axe in self.accelerMax.keys():
			print("accelerMax {} = {}".format(axe, self.accelerMax[axe]))
		for axe in self.invSensRot.keys():
			print("invSensRot {} = {}".format(axe, self.invSensRot[axe]))
		print("self.maxRotBroche = {}".format(self.maxRotBroche))

# Programme principal de test

if __name__ == "__main__":

	w = Tk()
	w.title('class DataParam')
	w.config(bg = "khaki")
	w.geometry("200x50+50+50")

	data = DataParam()
	print(data.loadCourseMax('x'))
	print(data.loadCourseMax('y'))
	print(data.loadCourseMax('z'))

	print(data.loadDeplParPuls('x'))
	print(data.loadDeplParPuls('y'))
	print(data.loadDeplParPuls('z'))

	print(data.loadVitesseMaxDepl('x'))
	print(data.loadVitesseMaxDepl('y'))
	print(data.loadVitesseMaxDepl('z'))

	print(data.loadFrequencePuls('x'))
	print(data.loadFrequencePuls('y'))
	print(data.loadFrequencePuls('z'))

	print(data.loadAccelerMax('x'))
	print(data.loadAccelerMax('y'))
	print(data.loadAccelerMax('z'))

	print(data.loadInvSensRot('x'))
	print(data.loadInvSensRot('y'))
	print(data.loadInvSensRot('z'))

	print(data.loadMaxRotBroche())

	btnParam = Button(w, text="Print data", command=data.printParam1)
	btnParam.pack(side = LEFT)

	w.mainloop()
