#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from math import *


def calculCentreArc(xA, yA, xB, yB, S, R):
	if ((xA == xB) and (yA == yB)):					# Passer par une notation de type G02 Xnn Ynn Inn Jnn
		return('ERR', 8)
	if (R == 0):
		return('ERR', 10)
	if (S not in ['H', 'T']):
		return('ERR', 12)

	print("DEBUG --- fct: calculCentreArc 14", xA, xB, S, R)

#	Calcul de l'angle de l'arc définit par le segment AB

	angle = 0.0
	dAB = sqrt((xB - xA)**2 + (yB - yA)**2)			# Calcul de la longueur du segment AB
	xD = xA + ((xB - xA) / 2)
	yD = yB + ((yA - yB) / 2)

	align = False
	if (dAB == (abs(R) * 2)):						# A, C, B sont alignés
		align = True
#		angle = degrees(asin((dAB / 2) / R)) * 2	# Angle
#	print("dAB=", dAB, "Angle=", angle)

	if (align == True):								# Cas où le centre du cercle se trouve au centre du segment AB
													# Ici le signe de R n'est pas pris en compte
		if (xA == xB):								# Axe des centres des cercles est vertical

			if (yB > yA):
				orientation = 'N'
				xC = xA
				yC = yA + abs(R)
				return(orientation, align, xC, yC, R, S, dAB)

			if (yB < yA):
				orientation = 'S'
				xC = xA
				yC = yB + abs(R)
				return(orientation, align, xC, yC, R, S, dAB)

		if (yA == yB):								# Axe des centres des cercles est horizontal

			if (xB > xA):
				orientation = 'E'
				xC = xA + abs(R)
				yC = yA
				return(orientation, align, xC, yC, R, S, dAB)

			if (xB < xA):
				orientation = 'O'
				xC = xB + abs(R)
				yC = yA
				return(orientation, align, xC, yC, R, S, dAB)

	else:										# Cas les points A, C, B ne sont pas alignés
		if (xA == xB):							# AB est vertical, axe des centres des deux cercles est horizontal
			dCD = sqrt(R**2 - (dAB/2)**2)
			xC1 = xA - dCD						# ou xB
			yC1 = yD
			xC2 = xA + dCD
			yC2 = yD
#			print("--------------> {:0.2f}, {:0.2f} --- {:0.2f}, {:0.2f}".format(xC1, yC1, xC2, yC2))
			if (yB > yA):
				orientation = 'N'
				if (R > 0):						# Petit arc
					if (S == 'H'):
						return(orientation, align, xC2, yC2, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC1, yC1, R, S, dAB)
				if (R < 0):						# Grand arc
					if (S == 'H'):
						return(orientation, align, xC1, yC1, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC2, yC2, R, S, dAB)

			if (yB < yA):
				orientation = 'S'
				if (R > 0):						# Petit arc
					if (S == 'H'):
						return(orientation, align, xC1, yC1, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC2, yC2, R, S, dAB)
				if (R < 0):						# Grand arc
					if (S == 'H'):
						return(orientation, align, xC2, yC2, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC1, yC1, R, S, dAB)

		elif (yA == yB):							# AB est horizontal, axe des centres des deux cercles est vertical
			dCD = sqrt(R**2 - (dAB/2)**2)
			xC1 = xA + dAB/2						# ou xB
			yC1 = yA + dCD
			xC2 = xA + dAB/2
			yC2 = yA - dCD

			if (xB > xA):
#				print("--------------> {:0.2f}, {:0.2f} --- {:0.2f}, {:0.2f}".format(xC1, yC1, xC2, yC2))
				orientation = 'E'
				if (R > 0):						# Petit arc
					if (S == 'H'):
						return(orientation, align, xC2, yC2, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC1, yC1, R, S, dAB)
				if (R < 0):						# Grand arc
					if (S == 'H'):
						return(orientation, align, xC1, yC1, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC2, yC2, R, S, dAB)

			if (xB < xA):
				orientation = 'O'
				dCD = sqrt(R**2 - (dAB/2)**2)
				xC1 = xB + dAB/2								# ou xB
				yC1 = yA + dCD
				xC2 = xB + dAB/2
				yC2 = yA - dCD
#				print("--------------> {:0.2f}, {:0.2f} --- {:0.2f}, {:0.2f}".format(xC1, yC1, xC2, yC2))
				if (R > 0):						# Petit arc
					if (S == 'H'):
						return(orientation, align, xC1, yC1, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC2, yC2, R, S, dAB)
				if (R < 0):						# Grand arc
					if (S == 'H'):
						return(orientation, align, xC2, yC2, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC1, yC1, R, S, dAB)

		else:										#
			if (xB < xA and yB > yA):
				orientation = 'NO'
				tup = calulC1C2(xA, yA, xB, yB, R)
				xC1 = tup[0]
				yC1 = tup[1]
				xC2 = tup[2]
				yC2 = tup[3]
#				print("--------------> {:0.2f}, {:0.2f} --- {:0.2f}, {:0.2f}".format(xC1, yC1, xC2, yC2))
				if (R > 0):						# Petit arc
					if (S == 'H'):
						return(orientation, align, xC2, yC2, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC1, yC1, R, S, dAB)
				if (R < 0):						# Grand arc
					if (S == 'H'):
						return(orientation, align, xC1, yC1, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC2, yC2, R, S, dAB)

			if (xB > xA and yB > yA):
				orientation = 'NE'
				tup = calulC1C2(xA, yA, xB, yB, R)
				xC1 = tup[0]
				yC1 = tup[1]
				xC2 = tup[2]
				yC2 = tup[3]
#				print("--------------> {:0.2f}, {:0.2f} --- {:0.2f}, {:0.2f}".format(xC1, yC1, xC2, yC2))
				if (R > 0):						# Petit arc
					if (S == 'H'):
						return(orientation, align, xC2, yC2, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC1, yC1, R, S, dAB)
				if (R < 0):						# Grand arc
					if (S == 'H'):
						return(orientation, align, xC1, yC1, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC2, yC2, R, S, dAB)

			if (xB > xA and yB < yA):
				orientation = 'SE'
				tup = calulC1C2(xA, yA, xB, yB, R)
				xC1 = tup[0]
				yC1 = tup[1]
				xC2 = tup[2]
				yC2 = tup[3]
#				print("--------------> {:0.2f}, {:0.2f} --- {:0.2f}, {:0.2f}".format(xC1, yC1, xC2, yC2))
				if (R > 0):						# Petit arc
					if (S == 'H'):
						return(orientation, align, xC1, yC1, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC2, yC2, R, S, dAB)
				if (R < 0):						# Grand arc
					if (S == 'H'):
						return(orientation, align, xC2, yC2, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC1, yC1, R, S, dAB)

			if (xB < xA and yB < yA):
				orientation = 'SO'
				tup = calulC1C2(xA, yA, xB, yB, R)
				xC1 = tup[0]
				yC1 = tup[1]
				xC2 = tup[2]
				yC2 = tup[3]
#				print("--------------> {:0.2f}, {:0.2f} --- {:0.2f}, {:0.2f}".format(xC1, yC1, xC2, yC2))
				if (R > 0):						# Petit arc
					if (S == 'H'):
						return(orientation, align, xC2, yC2, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC1, yC1, R, S, dAB)
				if (R < 0):						# Grand arc
					if (S == 'H'):
						return(orientation, align, xC1, yC1, R, S, dAB)
					if (S == 'T'):
						return(orientation, align, xC2, yC2, R, S, dAB)

			return('ERR', 128)


def calulC1C2(xA, yA, xB, yB, R):

	k1 = 2*(xB - xA)
	k2 = 2*(yB - yA)
	k3 =  xA**2 - xB**2 + yA**2 - yB**2

	m = - (k1/k2)
	h = - (k3/k2)
#	print("m={:0.6f}, h={:0.6f}".format(m, h))
#
	a = 1 + m**2
	b = 2*m*h -2*xA - 2*yA*m
	c = yA**2 - 2*yA*h + xA**2 + h**2 - R**2
#	print("a={:0.6f}, b={:0.6f}, c={:0.6f}".format(a, b, c))

	delta = sqrt(b**2 - 4*a*c)
	xC1 = (-b - delta) / (2*a)
	xC2 = (-b + delta) / (2*a)

	yC1 = m*xC1 + h
	yC2 = m*xC2 + h

#	print("\n\nxC1={:0.6f}, yC1={:0.6f}  ---  xC2={:0.6f}, yC2={:0.6f}".format(xC1, yC1, xC2, yC2))
	return(xC1, yC1, xC2, yC2)


if __name__ == "__main__":

	tab0 = [
# Alignement ACB
#	Un seul cercle
#	départs possibles selon les sens Horaire et Trigo, mais un seul arc de 180°
#	Donc R positif ou négatif ne déterminent pas de petits ou grands arcs de cercle
#	4 cas uniquement pour tester que le code réagit correctement même si R négatif n'a pas de raison d'être

# Orientation Nord
		( '#', 'Orient. Nord, 2 demi-cercles, 2 départs H/T possibles, R- non significatif'),
		( 11, 3, 13,  3, 17, 'H', +2),				#  1	1	# Petit arc, sens Horaire
		( 12, 3, 13,  3, 17, 'T', +2),				#  2	1	# Petit arc, sens Trigo
		( 13, 3, 13,  3, 17, 'H', -2),				#  3	1	# Grand arc, sens Horaire		(Sans signification)
		( 14, 3, 13,  3, 17, 'T', -2),				#  4	1	# Grand arc, sens Trigo			(Sans signification)
# Orientation Sud
		( '#', 'Orient. Sud,  2 demi-cercles, 2 départs H/T possibles, R- non significatif'),
		( 21, 3, 12,  3,  8, 'H', +2),				#  5	2
		( 22, 3, 12,  3,  8, 'T', +2),				#  6	2
		( 23, 3, 12,  3,  8, 'H', -2),				#  7	2
		( 24, 3, 12,  3,  8, 'T', -2),				#  8	2
# Orientation Est
		( '#', 'Orient. Est, 2 demi-cercles, 2 départs H/T possibles, R- non significatif'),
		( 31, 1,  5,  5,  5, 'H', +2),				#  9	3
		( 32, 1,  5,  5,  5, 'T', +2),				# 10	3
		( 33, 1,  5,  5,  5, 'H', -2),				# 11	3
		( 34, 1,  5,  5,  5, 'T', -2),				# 12	3
# Orientation Ouest
		( '#', 'Orient. Ouest, 2 demi-cercles, 2 départs H/T possibles, R- non significatif'),
		( 41, 10,  3,  6,  3, 'H', +2),				# 13	4
		( 42, 10,  3,  6,  3, 'T', +2),				# 14	4
		( 43, 10,  3,  6,  3, 'H', -2),				# 15	4
		( 44, 10,  3,  6,  3, 'T', -2),				# 16	4

# Non alignement ACB
#	4 directions possibles NO, NE, SE, SO,
#	2 cercles possibles,
#	4 départs possibles selon les sens Horaire et Trigo, selon le signe de R : 2 petits arcs, 2 grands arcs

# Orientation Nord et Sud
		( '#', 'Orient. verticale Nord, Non alignement ACB, 2 cercles, 4 départs H/T et signe de R'),
		( 51, 11, 13,   11, 16,   'H', +2.9),		# 17	5
		( 52, 11, 13,   11, 16,   'T', +2.9),		# 18	5
		( 53, 11, 13,   11, 16,   'H', -2.9),		# 19	5
		( 54, 11, 13,   11, 16,   'T', -2.9),		# 20	5
		( '#', 'Orient. verticale Sud, Non alignement ACB, 2 cercles, 4 départs H/T et signe de R'),
		( 55, 11,  8.5,   11,  5.5, 'H', +2.9),		# 21	5
		( 56, 11,  8.5,   11,  5.5, 'T', +2.9),		# 22	5nnnnnnnnnnnnn, b:         !v w  jhjh
		( 57, 11,  8.5,   11,  5.5, 'H', -2.9),		# 23	5
		( 58, 11,  8.5,   11,  5.5, 'T', -2.9),		# 24	5
# Orientation Est et Ouest
		( '#', 'Orient. horizontale Est, Non alignement ACB, 2 cercles, 4 départs H/T et signe de R'),
		( 61, 18,  9, 22,  9, 'H', +2.9),			# 25	6
		( 62, 18,  9, 22,  9, 'T', +2.9),			# 26	6
		( 63, 18,  9, 22,  9, 'H', -2.9),			# 27	6
		( 64, 18,  9, 22,  9, 'T', -2.9),			# 28	6
		( '#', 'Orient. Horizontale Ouest, Non alignement ACB, 2 cercles, 4 départs H/T et signe de R'),
		( 65,  6,  11.75,  2,  11.75, 'H', +3),		# 29	6
		( 66,  6,  11.75,  2,  11.75, 'T', +3),		# 30	6
		( 67,  6,  11.75,  2,  11.75, 'H', -3),		# 31	6
		( 68,  6,  11.75,  2,  11.75, 'T', -3),		# 32	6
# Orientation Nord-Ouest et Sud-Est
		( '#', 'Orient. NO, Non alignement ACB, 2 cercles, 4 départs H/T et signe de R'),
		( 71, 15, 11, 12, 13, 'H', +3),				# 33	7
		( 72, 15, 11, 12, 13, 'T', +3),				# 34	7
		( 73, 15, 11, 12, 13, 'H', -3),				# 37	7
		( 74, 15, 11, 12, 13, 'T', -3),				# 38	7
		( '#', 'Orient. SE, Non alignement ACB, 2 cercles, 4 départs H/T et signe de R'),
		( 75, 19, 10, 21,  7, 'H', +5.15),			# 35	7
		( 76, 19, 10, 21,  7, 'T', +5.15),			# 36	7
		( 77, 19, 10, 21,  7, 'H', -5.15),			# 39	7
		( 78, 19, 10, 21,  7, 'T', -5.15),			# 40	7
# Orientation Nord-Est et Sud-Ouest
		( '#', 'Orient. NE, Non alignement ACB, 2 cercles, 4 départs H/T et signe de R'),
		( 81, 5,  2, 6.5, 3.5, 'H', +3),			# 41	8
		( 82, 5,  2, 6.5, 3.5, 'T', +3),			# 42	8
		( 83, 5,  2, 6.5, 3.5, 'H', -3),			# 43	8
		( 84, 5,  2, 6.5, 3.5, 'T', -3),			# 44	8
		( '#', 'Orient. SO, Non alignement ACB, 2 cercles, 4 départs H/T et signe de R'),
		( 85, 6.5, 3.5, 5,  2, 'H', +3),			# 45	8
		( 86, 6.5, 3.5, 5,  2, 'T', +3),			# 46	8
		( 87, 6.5, 3.5, 5,  2, 'H', -3),			# 47	8
		( 88, 6.5, 3.5, 5,  2, 'T', -3),			# 48	8
		]

	numLine = 1
	for line in tab0:
		if (line[0] == '#'):
			print('\n', numLine, line[1])
		else:
			#      calculCentreArc(xA, yA, xB, yB, S, R)
			tupC = calculCentreArc(line[1], line[2], line[3], line[4], line[5], line[6])
			if (tupC[0] == 'ERR'):
				print(cas, "Erreur", tupC[1])
			else:
			#                    (orientation, align,    xC,     yC,      R,        S,     dAB)
				print("{:2d}, cas={} - orient={}, align={},\txC={:^6.2f}, yC={:^6.2f}, R={:^6.2f}, S={}, dAB={:0.2f}".format(
				   numLine, line[0], tupC[0], tupC[1], tupC[2], tupC[3], tupC[4], tupC[5], tupC[6]))
		numLine += 1

