#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
import os
try:
	from cnPackages.ButtonFlipFlop import ButtonFlipFlop
except:
	from ButtonFlipFlop import ButtonFlipFlop

class PanelButtonsCmd(Frame):
	def __init__(self, boss, fctExt, bg = 'ivory', **Arguments):
		Frame.__init__(self, boss, bg = bg, bd = 1, **Arguments)
		bg = bg

		self.fctExt = fctExt
		Label(self, text ="Cmds", font = "{courier new} 12 bold", bg = bg, fg = "blue").grid(row = 1, column = 1, columnspan = 2)
		# Références aux images utilisées pour les boutons
		self.refIconARU = PhotoImage(file = './images/btnARU.gif')
		self.refIconPAR = PhotoImage(file = './images/btnPAR.gif')
		self.refIconPOM = PhotoImage(file = './images/btnPOM.gif')
		self.refIconPOZ = PhotoImage(file = './images/btnPOZ.gif')
		self.refIconVOZ = PhotoImage(file = './images/btnVOZ.gif')
		self.refIconPXY = PhotoImage(file = './images/btnPXY.gif')
		self.refIconVXY = PhotoImage(file = './images/btnVXY.gif')
		self.refIconMAN = PhotoImage(file = './images/btnMAN.gif')
		self.refIconMAR = PhotoImage(file = './images/btnMAR.gif')
		self.refIconMAB = PhotoImage(file = './images/btnMAB.gif')
		self.refIconOFC = PhotoImage(file = './images/btnOFC.gif')
		self.refIconDCY = PhotoImage(file = './images/btnDCY.gif')
		self.refIconVAL = PhotoImage(file = './images/btnVAL.gif')
		self.refIconANN = PhotoImage(file = './images/btnANN.gif')

		self.lblList = []
		self.btnList = []

		self.lblARU = Label(self, text = "Arrêt urgence")
		self.lblList.append(self.lblARU)
		self.btnARU = Button(self, text = "ARU", image = self.refIconARU, relief = GROOVE)						# Arrêt d'urgence
		self.btnList.append(self.btnARU)

		self.lblPAR = Label(self, text = "Paramètres machine")
		self.lblList.append(self.lblPAR)
		self.btnPAR = Button(self, text = "PAR", image = self.refIconPAR, relief = GROOVE)						# Paramétrage machine
		self.btnList.append(self.btnPAR)

		self.lblPOM = Label(self, text = "Origine machine")
		self.lblList.append(self.lblPOM)
		self.btnPOM = Button(self, text = "POM", image = self.refIconPOM, relief = GROOVE)						# Origine machine
		self.btnList.append(self.btnPOM)

		self.lblPOZ = Label(self, text = "Origine pièce Z")
		self.lblList.append(self.lblPOZ)
		self.btnPOZ = ButtonFlipFlop(self, text = "POZ", imgon = self.refIconPOZ, imgoff = self.refIconVOZ, relief = GROOVE,
									 action = lambda arg = "POZ": self.fctExt(arg))												# Origine Z
		self.btnList.append(self.btnPOZ)

		self.lblPXY = Label(self, text = "Origine pièce XY")
		self.lblList.append(self.lblPXY)
		self.btnPXY = ButtonFlipFlop(self, text = "PXY", imgon = self.refIconPXY, imgoff = self.refIconVXY, relief = GROOVE,
									 action = lambda arg = "PXY": self.fctExt(arg))												# Origine Z
		self.btnList.append(self.btnPXY)

		self.lblMAN = Label(self, text = "Mode manuel")
		self.lblList.append(self.lblMAN)
		self.btnMAN = ButtonFlipFlop(self, text = "MAN", imgon = self.refIconMAN, imgoff = self.refIconMAR, relief = GROOVE,
									 action = lambda arg = "MAN": self.fctExt(arg))												# Passage mode manuel
		self.btnList.append(self.btnMAN)

		self.lblOFC = Label(self, text = "Lire G-Code")
		self.lblList.append(self.lblOFC)
		self.btnOFC = Button(self, text = "OFC", image = self.refIconOFC, relief = GROOVE)										# Choisir fichier GCode
		self.btnList.append(self.btnOFC)

		self.lblDCY = Label(self, text = "Départ cycle")
		self.lblList.append(self.lblDCY)
		self.btnDCY = Button(self, text = "DCY", image = self.refIconDCY, relief = GROOVE)										# Départ cycle
		self.btnList.append(self.btnDCY)

		self.lblANN = Label(self, text = "Annulation")
		self.lblList.append(self.lblANN)
		self.btnANN = Button(self, text = "ANN", image = self.refIconANN, relief = GROOVE)									# Fin d'action lente  ... provisoire
		self.btnList.append(self.btnANN)

#		r = 2
#		c = 1
#		for lblRef in self.lblList:
#			lblRef.config(font = "{Courier new} 7", fg = "grey", bg = bg)
#			lblRef.grid(row = r, column = c, sticky = 'e')
#			r += 1
		r = 2
		c = 2
		self.btnCodeToRef = {}
		for btnRef in self.btnList:												# Cas des boutons de la class Button
			btnCode = btnRef.cget("text")										# Récupération du code du bouton : ARU, PAR, POM, etc.
			self.btnCodeToRef[btnCode] = btnRef									# Association du code du bouton avec son instance
			if (btnCode not in ['MAN', 'POZ', 'PXY']):							# Cas particulier des boutons de la class ButtonFlipFlop()
#				btnRef.config(action = self.xx)
#			else:
				btnRef.config(command = lambda arg = btnCode: self.fctExt(arg))
			btnRef.grid(row = r, column = c)
			r += 1

# Gestion de l'affichage des boutons de commande IHM
#
	def disabledBtn(self, btnCode):
		refBtn = self.btnCodeToRef[btnCode]
		refBtn.config(state=DISABLED)

	def enabledBtn(self, btnCode):
		refBtn = self.btnCodeToRef[btnCode]
		refBtn.config(state=NORMAL)

	def disabledAll(self):
		for refBtn in self.btnList:
			refBtn.config(state=DISABLED)

# Programme principal de test

if __name__ == "__main__":

	def btnAction(btnCode):
		print("Button {}".format(btnCode))

	w = Tk()
	w.title('class PanelButtonsCmd')
	w.config(bg = "khaki")
	w.geometry("+50+50")
	pbc = PanelButtonsCmd(w, btnAction)
	pbc.pack()
	w.mainloop()
