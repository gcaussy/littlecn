#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
try:
	from cnPackages.PanelButtonsCmd			import PanelButtonsCmd
	from cnPackages.DataParam				import DataParam
	from cnPackages.PanelDisplayXYZ			import PanelDisplayXYZ
	from cnPackages.PanelButtonsXYZ			import PanelButtonsXYZ
	from cnPackages.PanelSettingsMan		import PanelSettingsMan
	from cnPackages.PanelDisplayGcode		import PanelDisplayGcode
	from cnPackages.PanelDisplayCmdsMotors	import PanelDisplayCmdsMotors
	from cnPackages.PanelDisplayPiece		import PanelDisplayPiece
	from cnPackages.PanelTrace				import PanelTrace
except:
	from PanelButtonsCmd		import PanelButtonsCmd
	from DataParam				import DataParam
	from PanelDisplayXYZ		import PanelDisplayXYZ
	from PanelButtonsXYZ		import PanelButtonsXYZ
	from PanelSettingsMan		import PanelSettingsMan
	from PanelDisplayGcode		import PanelDisplayGcode
	from PanelDisplayCmdsMotors	import PanelDisplayCmdsMotors
	from PanelDisplayPiece		import PanelDisplayPiece
	from PanelTrace				import PanelTrace

def createFrontPanel(win, bg):
	panelList = []
	# Colonne 1
	frm1 = Frame(win, bg = bg, bd = 2)
	frm1.grid(row = 1, column = 1, sticky = 'n')
	pn1 = PanelButtonsCmd(frm1, fctExt = btnAction)
	pn1.pack()
	panelList.append(pn1)

	# Colonne 2
	frm2 = Frame(win, bg = bg, bd = 2)
	frm2.grid(row = 1, column = 2, sticky = 'n')
	dt = DataParam()
	pn21 = PanelDisplayXYZ(frm2, data = dt)
	pn21.pack()
	panelList.append(pn21)
	pn22 = PanelButtonsXYZ(frm2, cmd = btnActionExt)
	pn22.pack()
	panelList.append(pn22)
	pn23 = PanelSettingsMan(frm2)
	pn23.pack()
	panelList.append(pn23)

	# Colonne 3
	frm3 = Frame(win, bg = bg, bd = 2)
	frm3.grid(row = 1, column = 3, sticky = 'n')
	pn31 = PanelDisplayGcode(frm3, nbChar = 30, nbLine = 10, font = "Helvetica 8 normal")
	pn31.pack()
	panelList.append(pn31)
	pn32 = PanelDisplayCmdsMotors(frm3, nbChar = 30, nbLine = 10, font = "Helvetica 8 normal")
	pn32.pack()
	panelList.append(pn32)

	# Colonne 4
	frm4 = Frame(win, bg = bg, bd = 2)
	frm4.grid(row = 1, column = 4, sticky = 'n')
	pn4 = PanelDisplayPiece(frm4)
	pn4.pack()
	panelList.append(pn4)

	# Colonne 2
	frm5 = Frame(win, bg = bg, bd = 2)
	frm5.grid(row = 1, column = 2, columnspan = 2, sticky = 's')
	pn5 = PanelTrace(frm5, nbChar = 50, nbLine = 6, font = "Helvetica 8 normal")
	pn5.pack()
	panelList.append(pn5)

	return (panelList)




# Programme principal de test
# ---------------------------

if __name__ == "__main__":

	def btnAction(btnCode):
		pass

	def btnActionExt(btnCode):
		pass

	w = Tk()
	w.title('def createFrontPanel')
	bg = 'ivory'
	w.config(bg = bg, bd = 10)
	w.geometry("+50+50")

	panelList = createFrontPanel(w, bg)
	for idx in [4, 5, 7]:
		pn = panelList[idx].getScr()
		for i in range(40):
			pn.insertLine("0123456789012345\n", "bleu")

	w.mainloop()