# Liste réduite des commandes G-code avec le format exact de la commande complète
#
cmdList = {}
cmdList['A'] = "([0-9]+)|([+-]?[0-9]+.[0-9]+)"			# Axe A rotatif de la machine (4ème axe)
cmdList['B'] = "([0-9]+)|([+-]?[0-9]+.[0-9]+)"			# Axe B de la machine
cmdList['C'] = "([0-9]+)|([+-]?[0-9]+.[0-9]+)"			# Axe C de la machine
cmdList['D'] = "[0-9]+"									# Valeur de la compensation de rayon d’outil
cmdList['F'] = "([0-9]+)|([0-9]+.[0-9]+)"				# Vitesse d’avance travail
cmdList['G'] = "[0-9]+"									# Fonction Générale
cmdList['H'] = ""										# Index d’offset de longueur d’outil
cmdList['I'] = "([0-9]+)|([0-9]+.[0-9]+)"				# Centre du cercle selon X
cmdList['J'] = "([0-9]+)|([0-9]+.[0-9]+)"				# Centre du cercle selon Y
cmdList['K'] = "[0-9]+"									#.Décalage en Z pour les arcs et dans les cycles préprogrammés G87 / Distance de déplacement par tour de broche avec G33
cmdList['L'] = "[[0-9]+"								# Longueur de l'outil
cmdList['M'] = "[0-9]+"									# Fonction auxiliaire
cmdList['N'] = "[0-9]+"									# Numéro de ligne
cmdList['O'] = "[0-9]+"									# Incrément Delta en Z dans un cycle G73, G83
cmdList['P'] = "[]"										# Temporisation utilisée dans les cycles de perçage et avec G4 / Mot clé utilisé avec G10
cmdList['Q'] = ""										# Incrément Delta en Z dans un cycle G73, G83
cmdList['R'] = "([0-9]+)|([0-9]+.[0-9]+)"				# Rayon d’arc ou plan de retrait dans un cycle préprogrammé
cmdList['S'] = "[0-9]+"									# Vitesse de rotation de la broche
cmdList['T'] = "[0-9]+"									# Choix du Numéro d’outil
cmdList['U'] = "[0-9]+"									# Axe U de la machine
cmdList['V'] = "[0-9]+"									# Axe V de la machine
cmdList['W'] = "[0-9]+"									# Axe W de la machine
cmdList['X'] = "([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)"		# Axe X de la machine
cmdList['Y'] = "([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)"		# Axe Y de la machine
cmdList['Z'] = "([+-]?[0-9]+)|([+-]?[0-9]+.[0-9]+)"		# Axe Z de la machine
cmdList[';'] = "^;.*$"									# Commentaire
cmdList['%'] = "^$"										# Début ou Fin de fichier

# Liste des commandes préparatoires de type G
#
gmList = {}
gmList['G0']	= "Déplacement rapide"
gmList['G01']	= "Interpolation linéaire"
gmList['G02']	= "Interpolation circulaire (sens horaire, anti-trigo)"
gmList['G03']	= "Interpolation circulaire (sens anti-horaire, trigo)"
gmList['G17']	= "Sélection du plan X-Y"
gmList['G20']	= "Programmation en pouces "
gmList['G21']	= "Programmation en mm"
gmList['G53']	= "?"
gmList['G54']	= "Activation du décalage d'origine pièce (Offset)"
gmList['G90']	= "Programmation absolue"
gmList['G91']	= "Programmation en coordonnées relative"

gmList['M0']	= "Arrêt de programme"
gmList['M2']	= "Fin de programme"
gmList['M3']	= "Broche sens horaire"
gmList['M5']	= "Arrêt de broche"
gmList['M6']	= "Changement d'outil"
gmList['M9']	= "Arrosage ??"
gmList['M00']	= "Arrêt de programme"
gmList['M01']	= "Arrêt conditionnel du programme"
gmList['M02']	= "Fin de programme"
gmList['M03']	= "Broche sens horaire"
gmList['M04']	= "Sens antihoraire"
gmList['M05']	= "Arrêt de broche"
gmList['M06']	= "Changement d'outil"

#
# Liste des commandes associées avec une valeur
#
xList = {}
xList['F']	= "Vitesse de déplacement"
xList['L']	= "Longueur de l'outil"
xList['R']	= "Rayon"
xList['S']	= "Vitesse de broche"
xList['T']	= "Sélection ou changement d'outil"
xList['X']	= "Coordonnée de l'axe X"
xList['Y']	= "Coordonnée de l'axe Y"
xList['Z']	= "Coordonnée de l'axe Z"
xList['A']	= "Coordonnée d'axes"
xList['B']	= "Coordonnée d'axes"
xList['C']	= "Coordonnée d'axes"
xList['%']	= "Fin de fichier"

