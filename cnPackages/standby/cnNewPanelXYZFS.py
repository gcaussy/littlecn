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
	def __init__(self, boss, data = None, baseFont = "Courier 8 normal", bg = "ivory", width = 300, height = 150):
		Frame.__init__(self, boss, bd = 2, relief = SUNKEN, bg = bg)
		myFontTitre1	= "{courier new} 8"
		myFontTitre2	= "{courier new} 7"
		myFontXYZ		= "{courier new} 14 bold"

		Label(self, text ="Positionnement de la broche", font = myFontTitre1, bg = bg, fg = "blue").grid(row = 1, column = 2, columnspan = 2)
		Label(self, text ="Machine(mm)", font = myFontTitre2, bg = bg, fg = "grey").grid(row = 2, column = 2)
		Label(self, text ="Pièce(mm)", font = myFontTitre2, bg = bg, fg = "grey").grid(row = 2, column = 3)

		Label(self, text ="Vitesse de progression de la broche", font = myFontTitre1, bg = bg, fg = "blue").grid(row = 1, column = 4, columnspan = 3)
		Label(self, text ="Maximum(m/mn)",  font = myFontTitre2, bg = bg, fg = "grey").grid(row = 2, column = 4)
		Label(self, text ="Demandée(m/mn)", font = myFontTitre2, bg = bg, fg = "grey").grid(row = 2, column = 5)
		Label(self, text ="Calculée(m/mn)", font = myFontTitre2, bg = bg, fg = "grey").grid(row = 2, column = 6)

		Label(self, text ="Accélération", font = myFontTitre1, bg = bg, fg = "blue").grid(row = 1, column = 7)
		Label(self, text ="Demandée(m/s/s)", font = myFontTitre2, bg = bg, fg = "grey").grid(row = 2, column = 7)

		Label(self, text ="X", font = myFontXYZ, bg = bg, fg = "blue").grid(row = 3, column = 1)
		Label(self, text ="Y", font = myFontXYZ, bg = bg, fg = "blue").grid(row = 4, column = 1)
		Label(self, text ="Z", font = myFontXYZ, bg = bg, fg = "blue").grid(row = 5, column = 1)

# Affichage de la position de la broche par rapport aux butées des axes machine
		self.entryXma = Entry(self, justify = RIGHT, state = "readonly")
		self.entryXma.grid(row = 3, column = 2, padx = 5)
		self.entryYma = Entry(self, justify = RIGHT, state = "readonly")
		self.entryYma.grid(row = 4, column = 2, padx = 5)
		self.entryZma = Entry(self, justify = RIGHT, state = "readonly")
		self.entryZma.grid(row = 5, column = 2, padx = 5)

# Affichage de la position de la broche par rapport à l'origine pièce défini
		self.entryXop = Entry(self, justify = RIGHT, state = "readonly")
		self.entryXop.grid(row = 3, column = 3, padx = 5)
		self.entryYop = Entry(self, justify = RIGHT, state = "readonly")
		self.entryYop.grid(row = 4, column = 3, padx = 5)
		self.entryZop = Entry(self, justify = RIGHT, state = "readonly")
		self.entryZop.grid(row = 5, column = 3, padx = 5)

# Affichage de la vitesse de déplacement maximum possible sur les trois axes
		self.entryXvm = Entry(self, justify = RIGHT, state = "readonly")
		self.entryXvm.grid(row = 3, column = 4, padx = 5)
		self.entryYvm = Entry(self, justify = RIGHT, state = "readonly")
		self.entryYvm.grid(row = 4, column = 4, padx = 5)
		self.entryZvm = Entry(self, justify = RIGHT, state = "readonly")
		self.entryZvm.grid(row = 5, column = 4, padx = 5)

# Affichage de la vitesse de déplacement demandée sur les trois axes
		self.entryXvd = Entry(self, justify = RIGHT, state = "readonly")
		self.entryXvd.grid(row = 3, column = 5, padx = 5)
		self.entryYvd = Entry(self, justify = RIGHT, state = "readonly")
		self.entryYvd.grid(row = 4, column = 5, padx = 5)
		self.entryZvd = Entry(self, justify = RIGHT, state = "readonly")
		self.entryZvd.grid(row = 5, column = 5, padx = 5)

# Affichage de la vitesse de déplacement calculée sur les trois axes
		self.entryXvc = Entry(self, justify = RIGHT, state = "readonly")
		self.entryXvc.grid(row = 3, column = 6, padx = 5)
		self.entryYvc = Entry(self, justify = RIGHT, state = "readonly")
		self.entryYvc.grid(row = 4, column = 6, padx = 5)
		self.entryZvc = Entry(self, justify = RIGHT, state = "readonly")
		self.entryZvc.grid(row = 5, column = 6, padx = 5)

# Affichage de l'accélération demandée de la vitesse de déplacement sur les trois axes
		self.entryXac = Entry(self, justify = RIGHT, state = "readonly")
		self.entryXac.grid(row = 3, column = 7, padx = 5)
		self.entryYac = Entry(self, justify = RIGHT, state = "readonly")
		self.entryYac.grid(row = 4, column = 7, padx = 5)
		self.entryZac = Entry(self, justify = RIGHT, state = "readonly")
		self.entryZac.grid(row = 5, column = 7, padx = 5)

		self.entryList = [self.entryXma, self.entryYma, self.entryZma, self.entryXop, self.entryYop, self.entryZop,
						  self.entryXvm, self.entryYvm, self.entryZvm, self.entryXvd, self.entryYvd, self.entryZvd, self.entryXvc, self.entryYvc, self.entryZvc,
						  self.entryXac, self.entryYac, self.entryZac]

		self._insertAllEntry("1000.00000")

	def _insertAllEntry(self, str):
		for entry in self.entryList:
			entry.config(state = 'normal', width = 14, font = "{courier new} 10")
			entry.delete(0, END)
			entry.insert(0, str)
			entry.config(state = 'readonly')


# Programme principal de test
# ---------------------------

if __name__ == "__main__":
	w = Tk()
	w.title('Test de la classe nouveau PanelXYZ')
	dt = DataParam()													# Installation des données de paramètrage du matériel
	p = PanelXYZ(w, data = dt)
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