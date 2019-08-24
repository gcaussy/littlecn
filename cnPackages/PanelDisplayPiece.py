#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
import tkinter.font as tkFont
import re
from math import *

try:
	from cnPackages.AnalCmd import AnalCmd
except:
	from AnalCmd import AnalCmd

class PanelDisplayPiece(Frame):
	def __init__(self, boss, bg = 'ivory', dimH = 1300, dimV = 600, param = None, **Arguments):
		Frame.__init__(self, boss, bg = bg)
		self.refIconZPL = PhotoImage(file = './images/btnZPL.gif')
		self.refIconZMO = PhotoImage(file = './images/btnZMO.gif')

		Label(self, text ="Affichage de la pièce à usiner", font = "{courier new} 12 bold", bg = bg, pady = 3, fg = "blue").pack()

		frm1 = Frame(self, width = dimH, height = dimV)
		frm1.pack()

		self.dimH = dimH
		self.dimV = dimV
		self.can = Canvas(frm1, width = dimH, height = dimV, scrollregion = (0, 0, dimH, dimV), bd = 2, bg = "grey95")

		hbar = Scrollbar(frm1, orient = HORIZONTAL)
		hbar.pack(side = BOTTOM, fill = X)
		hbar.config(command = self.can.xview)

		vbar = Scrollbar(frm1, orient = VERTICAL)
		vbar.pack(side = RIGHT, fill = Y)
		vbar.config(command = self.can.yview)

		self.can.config(width = dimH, height = dimV)
		self.can.config(xscrollcommand = hbar.set, yscrollcommand = vbar.set)
		self.can.pack(expand = True, fill = BOTH)

		# Principaux axes du canvas
		self.decal = 20							# Décalage de offset de la pièce-Machine
		self.Xaxe = self.decal					# Axe des X compte tenu de l'offset
		self.Yaxe = self.dimV - self.decal		# Axe des Y compte tenu de l'offset et Y bas vers haut
		self.Xref = self.Xaxe					# Nouvelle référence pour les X
		self.Yref = self.Yaxe					# Nouvelle référence pour les Y
		self.XCanMax = 0.0						# Pour une visualisation des limites du champ de travail
		self.YCanMax = 0.0						# Idem

		self.XGcodeMax = 0.0					# Tel que calculé à partir du fichier G-Code
		self.YGcodeMax = 0.0
		self.scale = 1							# Pour le zoom

		frm2 = Frame(self, width = dimH, height = dimV)
		btnCentrage = Button(frm2, text = "Centrage", command = lambda mode = '+': self.centrage(mode))
		btnCentrage.pack(side = LEFT)
		btnZoomM = Button(frm2, image = self.refIconZMO, command = lambda mode = '-': self.zoom(mode))
		btnZoomM.pack(side = LEFT)
		btnZoomP = Button(frm2, image = self.refIconZPL, command = lambda mode = '+': self.zoom(mode))
		btnZoomP.pack(side = LEFT)
#		btnGrilleON = Button(frm2, text = "Grille ON", command = lambda mode = True: self.grille(mode))
#		btnGrilleON.pack(side = LEFT)
#		btnGrilleOFF = Button(frm2, text = "Grille OFF")
#		btnGrilleOFF.pack(side = LEFT)
		btnXleft = Button(frm2, text = "←",   command = lambda mode = 'L': self.move(mode))
		btnXleft.pack(side = LEFT)
		btnXright = Button(frm2, text = "→",  command = lambda mode = 'R': self.move(mode))
		btnXright.pack(side = LEFT)
		btnXtop = Button(frm2, text = "↑",    command = lambda mode = 'T': self.move(mode))
		btnXtop.pack(side = LEFT)
		btnXbottom = Button(frm2, text = "↓", command = lambda mode = 'B': self.move(mode))
		btnXbottom.pack(side = LEFT)
		frm2.pack()

		# Pour un cadrage central ultérieur
		self.Xmax = 0.0
		self.Ymax = 0.0
		self.Zmax = 0.0

	def getCan(self):
		return (self.can)

	def create_lineCn(self, x0, y0, x1, y1, tag = "CN", color = 'red', Xmax = None, Ymax = None):
		self.XGcodeMax = Xmax
		self.YGcodeMax = Ymax
		self.XCanMax = Xmax + self.Xref
		self.YCanMax = self.Yref - Ymax

		X0 = x0 + self.Xref
		Y0 = self.Yref-y0
		X1 = x1 + self.Xref
		Y1 = self.Yref-y1
		self.can.create_line(X0, Y0, X1, Y1, width = 1, fill = color, tag = tag)

	def create_arcCn(self, x0, y0, x1, y1, start, extent, color, tag = "CN", Xmax = None, Ymax = None):
		self.XGcodeMax = Xmax
		self.YGcodeMax = Ymax
		self.XCanMax = Xmax + self.Xref
		self.YCanMax = self.Yref - Ymax

		X0 = x0 + self.Xref
		Y0 = self.Yref - y0
		X1 = x1 + self.Xref
		Y1 = self.Yref - y1
		self.can.create_arc(X0, Y0, X1, Y1, start = start, extent = extent, style = 'arc', width = 1, outline = color, tag = tag)

	def centrage(self, mode):
		if (self.XGcodeMax > 0 and self.YGcodeMax > 0):
			Xcpg = self.XGcodeMax / 2					# Centre X gcode de la pièce
			Ycpg = self.YGcodeMax / 2					# Centre Y gcode de la pièce
			Xcpc = Xcpg + self.Xref						# Centre X de la pièce dans le Canvas
			Ycpc = self.Yref - Ycpg
			Xcc = self.dimH / 2							# Centre X du canvas
			Ycc = self.dimV / 2							# Centre Y du canvas

			dx = Xcc - Xcpc
			dy = Ycc - Ycpc
			print(Xcc, Ycc, dx, dy)
			self.can.move("all", dx, dy)

	def zoom(self, mode):
		x = self.dimH / 2
		y = self.dimV / 2

		if (mode == "+"):
			sc = 1.2
			self.can.scale("all", x, y, sc, sc)
			self.scale *= sc
		else:
			sc = 0.8333
			self.can.scale("all", x, y, sc, sc)
			self.scale *= sc

	def move(self, mode):

		if (mode == 'R'):
			self.can.move("all", +10, 0)
			return
		if (mode == 'L'):
			self.can.move("all", -10, 0)
			return
		if (mode == 'T'):
			self.can.move("all", 0, -10)
			return
		if (mode == 'B'):
			self.can.move("all", 0, +10)
			return

	def grille(self, mode):
		if (mode == True):
			self.can.create_line(0, self.Yaxe, self.dimH -1, self.Yaxe, width = 1, fill = 'blue', tag = "AXE", arrow='last')	# Axe des X
			self.can.create_line(self.Xref, self.dimV -1, self.Xref, 0, width = 1, fill = 'blue', tag = "AXE", arrow='last')	# Axe des Y
#			if (self.Xmax > 0 and self.Ymax > 0):
#				self.can.create_line(0, self.Ymax, self.dimH -1, self.Ymax, width = 1, fill = 'green', tag = "MAX")			# Axe des Xmax
#				self.can.create_line(self.Xmax, self.dimV -1, self.Xmax, 0, width = 1, fill = 'green', tag = "MAX")			# Axe des Ymax
		else:
			pass

	def draw(self, ac, line):
#		print("Ligne en cours: {}".format(line))
		color = 'red'
		tag = 'CN'
		width = 1
		r = ac.loadLine(line)
		status = r[0]
		cause  = r[1]
		if (r[0] is False):
			print("loadLine: {}".format(cause))
			return()
		varA = ac.getVar('A')
		if (varA == 'P'):
			x0 = float(ac.getVar('X1'))
			y0 = float(ac.getVar('Y1'))
			x0 = self.Xref + x0
			y0 = self.Yref - y0

			if (x0 > self.Xmax):
				self.Xmax = x0
			if (y0 > self.Ymax):
				self.Ymax = y0

		elif(varA == 'L'):
			x0 = float(ac.getVar('X1'))
			y0 = float(ac.getVar('Y1'))
			x1 = float(ac.getVar('X2'))
			y1 = float(ac.getVar('Y2'))

			x0 = self.Xref + x0
			y0 = self.Yref - y0
			x1 = self.Xref + x1
			y1 = self.Yref - y1

			if (x0 > self.Xmax):
				self.Xmax = x0
			if (y0 > self.Ymax):
				self.Ymax = y0
			if (x1 > self.Xmax):
				self.Xmax = x1
			if (y1 > self.Ymax):
				self.Ymax = y1

			self.can.create_line(x0, y0, x1, y1, width = width, fill = color, tag = tag)

		elif (varA in ['H', 'T', 'C']):
			X1 = float(ac.getVar('X1'))
			Y1 = float(ac.getVar('Y1'))
			X2 = float(ac.getVar('X2'))
			Y2 = float(ac.getVar('Y2'))
			I = float(ac.getVar('I'))
			J = float(ac.getVar('J'))
			R = float(ac.getVar('R'))

#			print("X1={} Y1={} X2={} Y2={} I={} J={} R={}".format(X1, Y1, X2, Y2, I, J, R))

			if (varA == 'H'):
				Xi = X1
				Yi = Y1
				X1 = X2
				Y1 = Y2
				X2 = Xi
				Y2 = Yi

			# Pour le cadrage eventuel
			if (X1 > self.Xmax):
				self.Xmax = x0
			if (Y1 > self.Ymax):
				self.Ymax = y0
			if (X2 > self.Xmax):
				self.Xmax = x1
			if (Y2 > self.Ymax):
				self.Ymax = y1

			# Calcul de l'angle "Extent"
			a = Y2 - Y1
			b = X2 - X1
			ap2 = a ** 2
			bp2 = b ** 2
			d01 = sqrt(ap2 + bp2)
			d01d2 = d01 / 2
			sin = d01d2 / R
			angle = degrees(asin(sin))
			extent = angle * 2
#			print("A={} X1={} Y1={} X2={} Y2={} R={} a={} b={} extent={}".format(varA, X1, Y1, X2, Y2, R, a, b, extent))

			# Calcul des coordonnées x0, y0, x1, y1 du carré du canvas entourant le cercle
			x0 = I - R
			y0 = J + R
			x1 = I + R
			y1 = J - R

			# Calcul de l'angle "Start"
			Xd = X1 - I
			Yd = Y1 - J
			if   (Yd == 0 and Xd > 0):
				cas = 0
				ajout = 0
			elif (Yd > 0 and Xd > 0):
				cas = 1
				ajout = 0
			elif (Yd > 0 and Xd == 0):
				cas = 2
				ajout = 0
			elif (Yd > 0 and Xd < 0):
				cas = 3
				ajout = 90
			elif (Yd == 0 and Xd < 0):
				cas = 4
				ajout = 180
			elif (Yd < 0 and Xd < 0):
				cas = 5
				ajout = 180
			elif (Yd < 0 and Xd == 0):
				cas = 6
				ajout = 180
			elif (Yd < 0 and Xd > 0):
				cas = 7
				ajout = 270
			else:
				pass
			sin2 = Yd / R
			start = abs(degrees(asin(sin2))) + ajout

			print("Yd={} Xd={} cas={} ajout={} start={} extent={}".format(Yd, Xd, cas, ajout, start, extent))

			x0 = self.Xref + x0
			y0 = self.Yref - y0
			x1 = self.Xref + x1
			y1 = self.Yref - y1
			self.can.create_arc(x0, y0, x1, y1, start = start, extent = extent, style = 'arc', width = width, outline = color, tag = tag)
		else:
			return

	def displayErr(self, numLine, cmd):
		print("ERR - PanelDisplayPiece.py - {} : {}".format(nunLine, cmd))




# Programme principal de test
# ---------------------------

if __name__ == "__main__":

	primaryCmds=[
		("A=P X1=0.00 Y1=0.00"),
		("A=P X1=30.00 Y1=80.00"),
		("A=L X1=30.00 Y1=80.00 X2=70.00 Y2=80.00"),
		("A=H X1=70.00 Y1=80.00 X2=90.00 Y2=60.00 I=70.00 J=60.00 R=20.00"),			# Arc 1
		("A=L X1=90.00 Y1=60.00 X2=90.00 Y2=40.00"),
		("A=T X1=90.00 Y1=40.00 X2=110.00 Y2=20.00 I=110.00 J=40.00 R=20.00"),			# Arc 2
		("A=L X1=110.00 Y1=20.00 X2=150.00 Y2=20.00"),
		("A=T X1=150.00 Y1=20.00 X2=170.00 Y2=40.00 I=150.00 J=40.00 R=20.00"),			# Arc 3
		("A=L X1=170.00 Y1=40.00 X2=230.00 Y2=40.00"),
		("A=T X1=230.00 Y1=40.00 X2=230.00 Y2=80.00 I=230.00 J=60.00 R=20.00"),			# Arc 4
		("A=L X1=230.00 Y1=80.00 X2=200.00 Y2=80.00"),
		("A=L X1=200.00 Y1=80.00 X2=200.00 Y2=100.00"),
		("A=T X1=200.00 Y1=100.00 X2=180.00 Y2=120.00 I=180.00 J=100.00 R=20.00"),		# Arc 5
		("A=L X1=180.00 Y1=120.00 X2=160.00 Y2=120.00"),
		("A=H X1=160.00 Y1=120.00 X2=120.00 Y2=120.00 I=140.00 J=120.00 R=20.00"),		# Arc 6
		("A=L X1=120.00 Y1=120.00 X2=100.00 Y2=120.00"),
		("A=T X1=100.00 Y1=120.00 X2=80.00 Y2=100.00 I=100.00 J=100.00 R=20.00"),		# Arc 7
		("A=L X1=80.00 Y1=100.00 X2=60.00 Y2=100.00"),
		("A=L X1=60.00 Y1=100.00 X2=60.00 Y2=120.00"),
		("A=L X1=60.00 Y1=120.00 X2=30.00 Y2=120.00"),
		("A=T X1=30.00 Y1=120.00 X2=30.00 Y2=80.00 I=30.00 J=100.00 R=20.00")			# Arc 8
		]



	def fNone(cmd = None):
		print("fNone", cmd)
	def fLine(cmd = None):
		pass
	def fArc(cmd = None):
		pass
	def fX1(cmd):
		pass
	def fY1(cmd):
		pass
	def fX2(cmd):
		pass
	def fY2(cmd):
		pass
	def fI(cmd):
		pass
	def fJ(cmd):
		pass

	cmdList = {}
	cmdList['D']	= fNone
	cmdList['L']	= fLine
	cmdList['C']	= fArc
	cmdList['F']	= fNone
	cmdList['S']	= fNone
	cmdList['X1']	= fX1
	cmdList['Y1']	= fY1
	cmdList['X2']	= fX2
	cmdList['Y2']	= fY2
	cmdList['I']	= fI
	cmdList['J']	= fJ

	w = Tk()
	w.title('class PanelDisplayPiece')
	w.geometry("+30+30")
	pdp = PanelDisplayPiece(w)
	pdp.pack()
	can = pdp.getCan()
	ac = AnalCmd()
	for line in primaryCmds:
#		print(line)
		pdp.draw(ac, line)

	w.mainloop()
