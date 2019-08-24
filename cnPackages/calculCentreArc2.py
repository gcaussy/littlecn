#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from math import *


def calculCentreArc(xA, yA, xB, yB, sens, rayon):

# Calcul des coefficients m1 et h1 de la droite passant par les deux centres


	k1 = 2*(xB - xA)
	k2 = 2*(yB - yA)
	k3 =  xA**2 - xB**2 + yA**2 - yB**2
#	print("k1={:0.6f}, k2={:0.6f}, k3c={:06f}".format(k1, k2, k3))

	if (k1 == 0):			# Cas d'un axe de centres des cercles vertical
		pente = 'v'
	elif (k2 == 0):			# Cas d'un axe de centres des cercles Horizontal
		pente = 'h'
		m1 = 1
	else:
		m1 = - (k1/k2)
		h1 = - (k3/k2)
#	print("m1={:0.6f}, h1={:0.6f}".format(m1, h1))

# Calcul des coordonnées xC1,yC1 et xC2,yC2 des deux cercles passant par les points A et B
	a = 1 + m1**2
	b = 2*m1*h1 -2*xA - 2*yA*m1
	c = yA**2 - 2*yA*h1 + xA**2 + h1**2 - rayon**2
#	print("a={:0.6f}, b={:0.6f}, c={:0.6f}".format(a, b, c))

	delta = sqrt(b**2 - 4*a*c)
	xC1 = (-b - delta) / (2*a)
	xC2 = (-b + delta) / (2*a)

	yC1 = m1*xC1 + h1
	yC2 = m1*xC2 + h1

	try:
		P = (yB - yA) / (xB - xA)
	except:
		P = 0
		print("Pente: Verticale")

	print("xC1={:0.6f}, yC1={:0.6f}  ---  xC2={:0.6f}, yC2={:0.6f} --- Pente={:0.6f}".format(xC1, yC1, xC2, yC2, P))

# Vérification du cas ou l'arc de cercle fait 180 degrès (Cas où ACB sont alignés)
	xCAB = (xB - xA) / 2
	yCAB = (yB - yA) / 2




if __name__ == "__main__":

	tab1 = [
		(110, 20 , 140, 50, 'H', +30),		# Sens Horaire, R > 0 = Chemin le plus cours
		(110, 20 , 140, 50, 'T', +30),		# Sens Trigo  , R > 0 = Chemin le plus cours
		(110, 20 , 140, 50, 'H', -30),		# Sens Horaire, R < 0 = Chemin le plus long
		(110, 20 , 140, 50, 'T', -30),		# Sens Trigo  , R < 0 = Chemin le plus long

		(230, 60, 260, 30, 'H', +30),
		(230, 60, 260, 30, 'T', +30),
		(230, 60, 260, 30, 'H', -30),
		(230, 60, 260, 30, 'T', -30),

		(260, 130, 240, 110, 'H', +20),
		(260, 130, 240, 110, 'T', +20),
		(260, 130, 240, 110, 'H', -20),
		(260, 130, 240, 110, 'T', -20),

		(93.431, 110, 90, 90, 'H', +60),
		(93.431, 110, 90, 90, 'T', +60),
		(93.431, 110, 90, 90, 'H', -60),
		(93.431, 110, 90, 90, 'T', -60)
		]

	tab2 = [
		( 1, 10,  5, 10, 'H', +2),		# 1
		( 9,  9,  9,  7, 'H', +2),		# 2
		(18,  7, 20,  5, 'H', +2),		# 3
		(20, 12, 22, 12, 'H', +2),		# 4
		(13, 13, 15, 15, 'H', +2),		# 5
		( 7, 16,  7, 12, 'H', +2),		# 6
		( 6,  3,  4,  5, 'H', +2),		# 7
		(20,  5, 18,  7, 'H', +2),		# 8
		(12,  4, 14,  4, 'H', +2),		# 9
		( 3, 17,  3, 15, 'H', +2),		# 10
		( 3, 15,  3, 17, 'H', +2),		# 11
		]

	cas = 1
	for tup in tab2:
		print(cas)
		tupC = calculCentreArc(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
#		print("xC={:0.6f}, yC={:0.6f}, R={:0.6f}, S={}".format(tupC[0], tupC[1], tupC[2], tupC[3]))
		cas += 1

"""
	for tup in tab1:
		tupC = calculCentreArc(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
		print("xC={:0.6f}, yC={:0.6f}, R={:0.6f}, S={}".format(tupC[0], tupC[1], tupC[2], tupC[3]))
"""
