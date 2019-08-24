#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *

class PanelDisplayOneMoteur(Frame):
	ON = True
	OFF = False

	def __init__(self, boss, axe = 'X', bg = 'red', **Arguments):
		Frame.__init__(self, boss, bd = 0, bg = bg, padx = 5, pady = 0)
		self.refIconM0 = PhotoImage(file = './images/mot0.gif')
		self.refIconM1 = PhotoImage(file = './images/mot1.gif')
		self.refIconM2 = PhotoImage(file = './images/mot2.gif')
		self.refIconM3 = PhotoImage(file = './images/mot3.gif')
		self.refIconM4 = PhotoImage(file = './images/mot4.gif')
		self.refIconM5 = PhotoImage(file = './images/mot5.gif')
		self.refIconM6 = PhotoImage(file = './images/mot6.gif')
		self.refIconM7 = PhotoImage(file = './images/mot7.gif')
		self.refIconM8 = PhotoImage(file = './images/mot8.gif')
		self.refIconMH = PhotoImage(file = './images/motH.gif')
		self.refIconMT = PhotoImage(file = './images/motT.gif')

		self.imgs = []
		self.imgs.append(self.refIconM0)
		self.imgs.append(self.refIconM1)
		self.imgs.append(self.refIconM2)
		self.imgs.append(self.refIconM3)
		self.imgs.append(self.refIconM4)
		self.imgs.append(self.refIconM5)
		self.imgs.append(self.refIconM6)
		self.imgs.append(self.refIconM7)
		self.imgs.append(self.refIconM8)

		self.axe = axe

		Label(self, text = axe, bg = bg, bd = 0, font = "{courier new} 11 bold", fg = "blue").pack()
		frm2 = Frame(self, bg = bg)
		frm2.pack()
		self.lblMOT = Label(frm2, bg = bg, bd = 0, text = axe, image = self.imgs[0])	# Moteur: Marche/Arrêt
		self.lblMOT.pack()

		self.status = OFF
		self.i = 1
		self.sens = True
		self.anim()

	def enabled(self):
		self.lblMOT.config(state = NORMAL)

	def disabled(self):
		self.lblMOT.config(state = DISABLED)

	def start(self):
		self.status = ON
#		self.i = 1
		self.anim()

	def stop(self):
		self.status = OFF
		self.lblMOT.config(image = self.imgs[0])

	def sensH(self):
		self.sens = True
		self.lblMOT.config(image = self.imgs[0])

	def sensT(self):
		self.sens = False
		self.lblMOT.config(image = self.imgs[0])

	def anim(self):
		if (self.status == ON):
#			self.lbl.config(image = self.lblMOT[self.i])
			if (self.sens == True):
				self.i += 1
				if (self.i >= 8):
					self.i = 1
			else:
				self.i -= 1
				if (self.i <= 1):
					self.i = 8
			self.lblMOT.config(image = self.imgs[self.i])
			self.after(300, self.anim)

class PanelDisplayAllMotors(Frame):
	def __init__(self, boss, bg = 'black', **Arguments):
		Frame.__init__(self, boss, bd = 2, bg = bg, padx = 5)

		self.pMx = PanelDisplayOneMoteur(self, axe = 'X', bg = bg)
		self.pMx.pack(side = LEFT)
		self.pMx.stop()
		self.pMy = PanelDisplayOneMoteur(self, axe = 'Y', bg = bg)
		self.pMy.pack(side = LEFT)
		self.pMy.stop()
		self.pMz = PanelDisplayOneMoteur(self, axe = 'Z', bg = bg)
		self.pMz.pack(side = LEFT)
		self.pMz.stop()

	def start(self, axe):
		if (axe == 'X'):
#			self.pMx.sensH()
			self.pMx.start()
			return()
		if (axe == 'Y'):
#			self.pMy.sensH()
			self.pMy.start()
			return()
		if (axe == 'Z'):
#			self.pMz.sensH()
			self.pMz.start()
			return()

	def stop(self, axe):
		if (axe == 'X'):
			self.pMx.sensH()
			self.pMx.stop()
			return()
		if (axe == 'Y'):
			self.pMy.sensH()
			self.pMy.stop()
			return()
		if (axe == 'Z'):
			self.pMz.sensH()
			self.pMz.stop()
			return()

	def stopAll(self):
		self.pMx.stop()
		self.pMy.stop()
		self.pMz.stop()

	def sensH(self, axe):
		if (axe == 'X'):
			self.pMx.sensH()
			return()
		if (axe == 'Y'):
			self.pMy.sensH()
			return()
		if (axe == 'Z'):
			self.pMz.sensH()
			return()
		print("ERR=", axe)

	def sensT(self, axe):
		if (axe == 'X'):
			self.pMx.sensT()
			return()
		if (axe == 'Y'):
			self.pMy.sensT()
			return()
		if (axe == 'Z'):
			self.pMz.sensT()
			return()
		print("ERR=", axe)

# Programme principal de test

if __name__ == "__main__":

	w = Tk()
	w.title('class ImgAnim')
	w.geometry("+50+50")
	bg = 'ivory'

	im = PanelDisplayAllMotors(w, bg = bg)
	im.pack()

	frm = Frame(w, bd = 2, padx = 5, pady = 5)
	frm.pack()

	btstart = Button(frm, text="Start X",	command = lambda arg = 'X': im.start(arg))
	btstart.pack(side=LEFT)
	btstop = Button(frm, text="Stop",		command = im.stopAll)
	btstop.pack(side=LEFT)
	bth = Button(frm, text="Horaire",		command = lambda arg = 'X': im.sensH(arg))
	bth.pack(side=LEFT)
	btt = Button(frm, text="Trigo",			command = lambda arg = 'X': im.sensT(arg))
	btt.pack(side=LEFT)

	w.mainloop()
