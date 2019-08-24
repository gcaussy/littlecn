#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
try:
	from cnPackages.PanelButtonsCmd import PanelButtonsCmd
except:
	from PanelButtonsCmd import PanelButtonsCmd

# Automate régissant les différentes phases de l'IHM décrites dans une matrice
# [Phase courrante, Evénement reçu, Code action à exécuter, nouvelle phase si action Ok, nouvelle phase si action Ko]

class Automate(object):							# Gestion des phases de progression dans la préparation de l'usinage
	def __init__(self, ihmBtn, ihmActionList):
		self.ihmBtn = ihmBtn
		self.ihmActionList = ihmActionList
		self.currentPhase = "01"				# Non encore initialisée
		self.matrice = [

# Phase 01 Principal objectif: Saisie des paramètres machine en premier
			['01', "ARU", "AARU", '01', '01'],	# Action: Arrêt Urgence, retour à la Phase 1
			['01', "OFC", "AOFC", '01', '01'],	# Action: Choix fichier Gcode, si valide: retour Phase 1, sinon idem
			['01', "PAR", "APAR", '02', '01'],	# Action: Saisie paramètres machine, si valide: on passe à la Phase 2, sinon retour à la Phase 1

# Phase 02 Principal objectif: Proposer le calage sur les butées X, Y, Z de la broche --> Fonction lente devant recevoir un acquittement d'exécution
			['02', "ARU", "AARU", '01', '01'],	# Action: Arrêt Urgence, retour à la Phase 1
			['02', "PAR", "APAR", '02', '01'],	# Action: Re-saisie paramètres machine, si valide: on reste à la Phase 2, sinon retour à la Phase 1
			['02', "OFC", "AOFC", '02', '02'],	# Action: Nouveau choix fichier Gcode, si valide: on reste à la Phase 2, sinon retour à la Phase 1
			['02', "POM", "APOM", '03', '03'],	# Action: Positionnement origine outil/calage, toujours valide, passage à la Phase 3

# Phase 03 Principal objectif: Attendre l'acquittement d'exécution du matériel, avant de passer à la phase suivante
			['03', "ARU", "AARU", '01', '01'],	# Action: Arrêt Urgence, retour à la Phase 1
			['03', "ANN", "AANN", '04', '02'],	# Action: Traiter l'évenement d'acquittement reçu du matériel

# Phase 04 Principal objectif: Proposer le positionnement manuel de de la broche sur l'axe Z (sur le point le plus haut de la pièce à usiner)
			['04', "ARU", "AARU", '01', '01'],	# Action: Arrêt Urgence, retour à la Phase 1
			['04', "PAR", "APAR", '01', '01'],	# Action: Re-saisie paramètres machine autorisé
			['04', "OFC", "AOFC", '04', '04'],	# Action: Nouveau choix fichier Gcode, si valide: on reste à la Phase 3, sinon retour à la Phase 1
			['04', "POZ", "APOZ", '05', '03'],	# Action: Positionnement manuel de de la broche sur sur le point le plus haut de la pièce à usiner

# Phase 05 Principal objectif: Déplacements de la broche selon les 3 axes et validation que de la position Z
			['05', "ARU", "AARU", '01', '01'],	# Action: Arrêt Urgence, retour à la Phase 1
#			['05', "PAR", "APAR", '02', '01'],	# Action: Re-saisie paramètres machine autorisé
#			['05', "POM", "APOM", '03', '03'],	# Action: Re-positionnement origine outil/calage, toujours valide, retour à la Phase 3
			['05', "POZ", "AVAZ", '07', '07'],	# Action: Validation de la position Z par le même bouton POZ

# Phase 06 Principal objectif: Attendre l'acquittement d'exécution du matériel, avant de passer à la phase suivante
			['06', "ARU", "AARU", '01', '01'],	# Action: Arrêt Urgence, retour à la Phase 1
			['06', "ANN", "AANN", '05', '05'],	# Action: Traiter l'évenement d'acquittement reçu du matériel

# Phase 07 Principal objectif: Proposer le déplacement manuel de la broche selon les 2 axes XY
			['07', "ARU", "AARU", '01', '01'],	# Action: Arrêt Urgence, retour à la Phase 1
			['07', "PAR", "APAR", '02', '01'],	# Action: Re-saisie paramètres machine autorisé
			['07', "POM", "APOM", '03', '03'],	# Action: Re-positionnement origine outil/calage, toujours valide, retour à la Phase 3
			['07', "POZ", "APOZ", '05', '05'],	# Action: Re-positionnement sur origine Z autorisé
			['07', "PXY", "APXY", '08', '08'],	# Action: Re-positionnement sur origine Z autorisé

# Phase 08 Principal objectif: Déplacements de la broche selon les 3 axes et validation que de la position XY
			['08', "ARU", "AARU", '01', '01'],	# Action: Arrêt Urgence, retour à la Phase 1
			['08', "PXY", "AVXY", '10', '10'],	# Action: Validation du positionnement de XY choisi par le même bouton PXY

# Phase 09 Principal objectif: Attendre l'acquittement d'exécution du matériel, avant de passer à la phase suivante
			['09', "ARU", "AARU", '01', '01'],	# Action: Arrêt Urgence, retour à la Phase 1
			['09', "ANN", "AANN", '08', '08'],	# Action: Traiter l'évenement d'acquittement reçu du matériel

# Phase 10 Principal objectif: Tout est prêt, on peut proposer soit des déplacements manuels de la broche soit en automatique via Gcode
			['10', "ARU", "AARU", '01', '01'],	# Action: Arrêt Urgence, retour à la Phase 1
			['10', "PAR", "APAR", '02', '01'],	# Action: Re-saisie paramètres machine autorisé
			['10', "POM", "APOM", '03', '03'],	# Action: Re-positionnement origine outil/calage, toujours valide, retour à la Phase 3
			['10', "POZ", "APOZ", '05', '05'],	# Action: Re-positionnement sur origine Z autorisé
			['10', "PXY", "APXY", '08', '08'],	# Action: Re-positionnement sur origine XY autorisé
			['10', "MAN", "AMAN", '11', '11'],	# Action: Passage en mode manuel autorisé
			['10', "OFC", "AOFC", '10', '10'],	# Action: Ouverture du fichier Gcode
			['10', "DCY", "ADCY", '13', '13'],	# Action: Lancement du cycle à partir du fichier Gcode si OK

# Phase 11 Principal objectif: Gestion du mode manuel, fin du mode manuel attendu

			['11', "MAN", "AMAF", '10', '10'],	# Fin du mode manuel par le même bouton MAN

# Phase 12  Principal objectif: Attendre l'acquittement d'exécution du matériel, avant de passer à la phase suivante
			['12', "ARU", "AARU", '01', '01'],	# Action: Arrêt Urgence, retour à la Phase 1
			['12', "ANN", "AANN", '11', '11'],	# Action: Traiter l'évenement d'acquittement reçu du matériel

# Phase 13 Principal objectif: établir la liste des commandes primaires et envoi pour exécution
			['13', "ARU", "AARU", '01', '00'],	# Action: Arrêt Urgence, retour à la Phase 1
			['13', "ANN", "AANN", '10', '00']	# Action: Evénement de fin de travail
		]

	def getCurrentPhase(self):
		return(self.currentPhase)

	def atmError():
		print("Erreur Automate dans matriceActionCode")
		exit()

	def execActionAndGetNewPhase(self, eventCode):
		for line in self.matrice:
			matriceCurrentPhase		= line[0]
			matriceEventCode		= line[1]
			matriceActionCode		= line[2]
			matriceNewPhaseIfOk		= line[3]
			matriceNewPhaseIfKo		= line[4]

			if(self.currentPhase == matriceCurrentPhase and eventCode == matriceEventCode):
				ret = self.ihmActionList.get(matriceActionCode, self.atmError)()
				if (ret == True):
					newPhase = matriceNewPhaseIfOk
				else:
					newPhase = matriceNewPhaseIfKo
#				fp.setCurrentPhase(newPhase)
				self.currentPhase = newPhase
#				actionINF("Nouvelle phase={}".format(newPhase))

				self.ihmBtn.disabledAll()
				for line in self.matrice:
					matriceCurrentPhase	= line[0]
					matriceEventCode	= line[1]
					if (newPhase == matriceCurrentPhase):
						self.ihmBtn.enabledBtn(matriceEventCode)
						if (matriceEventCode == "VAL"):
							self.ihmBtn.enabledBtnXYZ()
				break
		else:
			msg = "Situation non prévue dans l'automate: {} inconnu en phase {}".format(eventCode, self.currentPhase)
			print(msg)
			return(False)


# Programme principal de test

if __name__ == "__main__":

	def btnAction(btnCode):
		print("Button {}".format(btnCode))
		atm.execActionAndGetNewPhase(btnCode)

	def ihmActionExt(currentEtat, btnCode, actionCode):
		print("ihmAction: {}-{}".format(currentEtat, btnCode, actionCode))

# Bouton de test des méthodes de IhmButton
	def disable():
		pbc.disabledBtn("ARU")

	def enable():
		pbc.enabledBtn("ARU")

# Actions à réaliser par l'automate d'état
#
	def actionARU():
		print("action ARU")
		return(True)

	def actionPAR():
		print("action PAR")
		return(True)

	def actionPOM():
		print("action POM")
		return(True)

	def actionPOZ():
		print("action POZ")
		return(True)

	def actionVAZ():
		print("action VAZ")
		return(True)

	def actionPXY():
		print("action PXY")
		return(True)

	def actionVXY():
		print("action VXY")
		return(True)

	def actionMAN():
		print("action MAN")
		return(True)

	def actionMAF():
		print("action MAF")
		return(True)

	def actionOFC():
		print("action OFC")
		return(True)

	def actionDCY():
		print("action DCY")
		return(True)

	def actionANN():
		print("action ANN")
		return(True)
		
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
	
	w = Tk()
	w.title('class Automate')
	w.config(bg = "khaki")
	w.geometry("+50+50")

	pbc = PanelButtonsCmd(w, btnAction)
	pbc.pack()
	atm = Automate(pbc, ihmActionList)

	Button(w, text = "ARU Disabled", command = disable).pack(side = LEFT)
	Button(w, text = "ARU Enabled", command = enable).pack(side = LEFT)

	w.mainloop()
