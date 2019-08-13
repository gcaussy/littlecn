#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
from tkinter.filedialog import askopenfilename
#from tkinter.tix import Balloon
from threading import Thread
import time
#from os import getcwd
import sys
import re

from cnPackages.DataParam				import DataParam
from cnPackages.WinParam				import WinParam
from cnPackages.Automate				import Automate
from cnPackages.AnalyseGcode			import AnalSyntaxGcode
from cnPackages.ThreadMoteurs			import *

from cnPackages.PanelButtonsCmd			import PanelButtonsCmd
from cnPackages.PanelDisplayXYZ			import PanelDisplayXYZ
from cnPackages.PanelButtonsXYZ			import PanelButtonsXYZ
from cnPackages.PanelSettingsMan		import PanelSettingsMan
from cnPackages.PanelDisplayGcode		import PanelDisplayGcode
from cnPackages.PanelDisplayCmdsMotors	import PanelDisplayCmdsMotors
from cnPackages.PanelDisplayPiece		import PanelDisplayPiece
from cnPackages.PanelTrace				import PanelTrace
from cnPackages.PanelBroche				import PanelBroche
from cnPackages.PanelMoteurs			import *

from cnPackages.calculCentreArc			import calculCentreArc

# Programme principal
# ===================

if __name__ == "__main__":

	db = True
	def debug(msg):
		if (db is True):
			pnlDTR.debug(msg)

	def btnAction(btnCode):
		debug("Button {}".format(btnCode))
		pnlDTR.getScr().insertLine("Button {}\n".format(btnCode), "bleu")
		atm.execActionAndGetNewPhase(btnCode)

# Actions à réaliser par l'automate d'état
#
	def actionARU():
#		debug("action ARU")
		pnlBC.disabledAll()
		pnlBC.enabledBtn('ARU')
		pblBXYZ.disabledAll()
		pnlSM.disabledAll()
		return(True)

	def actionPAR():
#		debug("action PAR")
		winPar = WinParam(w, dt)
		return(True)

	def actionPOM():
		debug("action POM")
		pnlDTR.getScr().insertLine("Calage Z puis XY vers les butées\n", "rouge")
		pnlMo.stopAll()
		thx = ThreadCalage(axe = 'X', pnlDisMot = pnlMo, atm = atm, pnlDisXYZ = pnlDXYZ, pnlBC = pnlBC, delay = 5)
		thx.start()
		thy = ThreadCalage(axe = 'Y', pnlDisMot = pnlMo, atm = atm, pnlDisXYZ = pnlDXYZ, pnlBC = pnlBC, delay = 8)
		thy.start()
		thz = ThreadCalage(axe = 'Z', pnlDisMot = pnlMo, atm = atm, pnlDisXYZ = pnlDXYZ, pnlBC = pnlBC, delay = 6)
		thz.start()
		return(True)

	def actionPOZ():
#		debug("action POZ")
		pnlDTR.getScr().insertLine("actionPOZ\n", "rouge")
		pblBXYZ.enabledAll()
		pnlSM.enabledAll()
		return(True)

	def actionVAZ():
#		debug("action VAZ")
		pnlDTR.getScr().insertLine("actionVAZ\n", "rouge")
		pblBXYZ.disabledAll()
		pnlSM.disabledAll()
		pnlDXYZ.setOrigPieceZ()
		return(True)

	def actionPXY():
#		debug("action PXY")
		pnlDTR.getScr().insertLine("actionPXY\n", "rouge")
		pblBXYZ.enabledAll()
		pnlSM.enabledAll()
		return(True)

	def actionVXY():
#		debug("action VXY")
		pnlDTR.getScr().insertLine("actionVXY\n", "rouge")
		pblBXYZ.disabledAll()
		pnlSM.disabledAll()
		pnlDXYZ.setOrigPieceXY()
		return(True)

	def actionMAN():
#		debug("action MAN")
		pnlDTR.getScr().insertLine("actionMAN\n", "rouge")
		pblBXYZ.enabledAll()
		pnlSM.enabledAll()
		pnlBRO.enabledAll()
		return(True)

	def actionMAF():
#		debug("action MAF")
		pnlDTR.getScr().insertLine("actionMAF\n", "rouge")
		pblBXYZ.disabledAll()
		pnlSM.disabledAll()
		pnlBRO.stop()
		pnlBRO.disabledAll()
		return(True)

	def actionOFC():
#		debug("action OFC")
		pnlDTR.getScr().insertLine("actionOFC\n", "rouge")
		n = asg.openFile(pnlDGC.getScr(), pnlDTR.getScr(), pnlDCM.getScr())
		if (n == 0):
			asg.createCmdCanvas(pnlDP)
			return(True)
		return(False)

	def actionDCY():
#		debug("action DCY")
		nb = asg.getNbErr()
		if (nb == 0):
			asg.createCmdCanvas(pnlDP)
			return(True)
		return(False)

	def actionANN():
		debug("action ANN")
		return(True)

	def actionACK():
		debug("action ACK")
		pass

	def ihmActionExt(currentEtat, btnCode, actionCode):
#		debug("ihmAction: {}-{}".format(currentEtat, btnCode, actionCode))
		pass

	def btnxyzAction(btnCode):
		lgEnMil = pnlSM.getFloatPas()
		msg = "btnCode={}, lgEnMil={:0.4f}\n".format(btnCode, lgEnMil)
		debug(msg)
		if (btnCode == "XMO"):
			pblBXYZ.disabledXBtn()
			th = ThreadPulse(w, 'x', '-', pnlDXYZ, dt, lgEnMil, retThread)
			th.run()
			return
		if (btnCode == "XPL"):
			pblBXYZ.disabledXBtn()
			th = ThreadPulse(w, 'x', '+', pnlDXYZ, dt, lgEnMil, retThread)
			th.run()
			return
		if (btnCode == "YMO"):
			pblBXYZ.disabledYBtn()
			th = ThreadPulse(w, 'y', '-', pnlDXYZ, dt, lgEnMil, retThread)
			th.run()
			return
		if (btnCode == "YPL"):
			pblBXYZ.disabledYBtn()
			th = ThreadPulse(w, 'y', '+', pnlDXYZ, dt, lgEnMil, retThread)
			th.run()
			return
		if (btnCode == "ZMO"):
			pblBXYZ.disabledZBtn()
			th = ThreadPulse(w, 'z', '-', pnlDXYZ, dt, lgEnMil, retThread)
			th.run()
			return
		if (btnCode == "ZPL"):
			pblBXYZ.disabledZBtn()
			th = ThreadPulse(w, 'z', '+', pnlDXYZ, dt, lgEnMil, retThread)
			th.run()
			return

	def retThread(axe, stopAxe):
		if (stopAxe == True):
			pnlDXYZ.changeColor(axe, 'red')
			time.sleep(1)
			pnlDXYZ.changeColor(axe, 'blue')

		if (axe == 'x'):
			pblBXYZ.enabledXBtn()
			return()
		if (axe == 'y'):
			pblBXYZ.enabledYBtn()
			return()
		if (axe == 'z'):
			pblBXYZ.enabledZBtn()
			return()

	def setRefresh(var):
		mode = var.get()
		pnlDGC.setRefresh(mode)

	ihmActionList = {}
	ihmActionList["AARU"] = actionARU		# Référence de l'action ARU (Arrêt d'urgence)
	ihmActionList["APAR"] = actionPAR		# Référence de l'action PAR (Saisie des paramètres machine)
	ihmActionList["APOM"] = actionPOM		# Référence de l'action POM (Positionnement origine machine : Calage sur les butées)
	ihmActionList["APOZ"] = actionPOZ		# Référence de l'action POZ (Positonnement Origine pièce Z : point le plus haut de la pièce)
	ihmActionList["AVAZ"] = actionVAZ		# Référence de l'action VQY (Validation Origine Z définie au moyen des touches de déplacement XYZ)
	ihmActionList["APXY"] = actionPXY		# Référence de l'action PXY (Positionnement Origine pièce XY)
	ihmActionList["AVXY"] = actionVXY		# Référence de l'action VXY (Validation Origine pièce XY)
	ihmActionList["AMAN"] = actionMAN		# Référence de l'action MAN (Passage en mode manuel)
	ihmActionList["AMAF"] = actionMAF		# Référence de l'action MAF (Fin du mode manuel)
	ihmActionList["AOFC"] = actionOFC		# Référence de l'action OFC (Ouverture du fichier Gcode)
	ihmActionList["ADCY"] = actionDCY		# Référence de l'action DCY (Démarrage cycle d'interprétation du fichier gcode choisi)
	ihmActionList["AANN"] = actionANN		# Référence de l'action ANN (PROVISOIRE pour test des fonctions lentes)

	dbg = False
	stopUrgence = False
	dt = DataParam()
	asg = AnalSyntaxGcode()

	w = Tk()
	w.title('LittelCN')
	w.geometry("+10+10")
	bg = 'ivory'
	w.config(bg = bg, bd = 10)

# Agencement du panneau de commandes
#	w
#		frmA (w)										pack(side=LEFT)
#			pnlBC = PanelButtonsCmd (frmA)					pack()
#			frmAB (frmA)									pack()
#				frmABA (frmAB)									pack(side=LEFT)
#					pnlDXYZ = PanelDisplayXYZ	(frmABA)			pack()
#					pnlBXYZ = PanelButtonsXYZ	(frmABA)			pack()
#					pnlSM	= PanelSettingsMan	(frmABA)			pack()
#					pnlBRO	= PanelBroche		(frmABA)			pack()
#				frmABB (frmAB)									pack(side=LEFT)
#					pnlDGC	= PanelDisplayGcode		(frmABB)		pack()
#					pnlDCM	= PanelDisplayCmdsMotors(frmABB)		pack()
#					Checkbutton-Refresh				(frmABB)		pack()
#			pnlDTR = PanelTrace(frmA)							pack()
#		frmB(w)											pack (side=LEFT)
#			pnlMo = PanelMoteurs (frmB)						pack()
#			pnlDP = PanelDisplayPiece (frmB)				pack()
#
#
	panelList = []
	frmA = Frame(w, bg = bg)
	frmA.pack(side=LEFT)

	pnlBC = PanelButtonsCmd(frmA, fctExt = btnAction)
	pnlBC.pack()
	panelList.append(pnlBC)

	frmAB = Frame(frmA, bg = bg)
	frmAB.pack()

	frmABA = Frame(frmAB, bg = bg)
	frmABA.pack(side=LEFT)

	pnlDXYZ = PanelDisplayXYZ(frmABA, data = dt)
	pnlDXYZ.pack()
	panelList.append(pnlDXYZ)
	pnlDXYZ.clear()

	pblBXYZ = PanelButtonsXYZ(frmABA, cmd = btnxyzAction)
	pblBXYZ.pack()
	panelList.append(pblBXYZ)

	pnlSM = PanelSettingsMan(frmABA)
	pnlSM.pack()
	panelList.append(pnlSM)

	pnlBRO = PanelBroche(frmABA, bg = bg)
	pnlBRO.pack()
	pnlBRO.setSpeed(2500)
	panelList.append(pnlBRO)

	frmABB = Frame(frmAB, bg = bg)
	frmABB.pack(side=LEFT)

	pnlDGC = PanelDisplayGcode(frmABB, nbChar = 65, nbLine = 16, font = "Courrier 8 normal")
	pnlDGC.pack()
	panelList.append(pnlDGC)

	pnlDCM = PanelDisplayCmdsMotors(frmABB, nbChar = 65, nbLine = 16, font = "Courrier 8 normal")
	pnlDCM.pack()
	panelList.append(pnlDCM)

	refresh = StringVar()
	refresh.set('Y')
	chkBtn = Checkbutton(frmABB, text="Refresh",  bg = bg, variable = refresh,
			onvalue='Y', offvalue='N', command = lambda arg = refresh: setRefresh(arg))
	chkBtn.pack()

	pnlDTR = PanelTrace(frmA, nbChar = 110, nbLine = 6, font = "Helvetica 8 normal")
	pnlDTR.pack()

	frmB = Frame(w, bg = bg, bd = 0)
	frmB.pack(side = LEFT)

	pnlMo = PanelDisplayAllMotors(frmB, bg = bg, bd = 0)
	pnlMo.pack(side = TOP)
	panelList.append(pnlMo)

	pnlDP = PanelDisplayPiece(frmB, dimH = 600, dimV = 550)
	pnlDP.pack()
	panelList.append(pnlDP)

	pnlBC.disabledAll()
	pnlBC.enabledBtn('ARU')
	pblBXYZ.disabledAll()
	pnlSM.disabledAll()
	pnlBRO.disabledAll()
	pnlDTR.getScr().insertLine("Start\n", "bleu")

	atm = Automate(pnlBC,ihmActionList)
	w.mainloop()
