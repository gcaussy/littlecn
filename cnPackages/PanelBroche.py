#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *

class PanelBroche(Frame):
	ON = True
	OFF = False

	def __init__(self, boss, bg = 'ivory', **Arguments):
		Frame.__init__(self, boss, bd = 2, bg = bg, padx = 5, pady = 2)
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

		Label(self, text ="Broche (Mode manuel)", font = "{courier new} 11 bold", bg = bg, fg = "blue").pack()
		frm2 = Frame(self, bg = bg)
		frm2.pack(side = LEFT)
		self.btnMOT = Button(frm2, text = "MOT", image = self.imgs[0], relief = GROOVE, command = self.flipflopMA)						# Moteur: Marche/Arrêt
		self.btnMOT.pack(side = LEFT)
		self.btnMHT = Button(frm2, text = "MOT", image = self.refIconMH, relief = GROOVE, command = self.flipflopHT)						# Moteur: Marche/Arrêt
		self.btnMHT.pack(side = LEFT)

		frm3 = Frame(self, bg = bg)
		frm3.pack(side = LEFT)		
		self.ent = Entry(frm3, width = 6, state = 'readonly', justify = RIGHT)
		self.ent.pack()
		Label(frm3, text = "trs/minute", font = "{courier new} 8 bold", fg = "grey", bg = bg).pack()
	
		self.status = OFF
		self.i = 1
		self.sens = True
		self.anim()

	def enabledAll(self):
		self.btnMOT.config(state = NORMAL)
		self.btnMHT.config(state = NORMAL)
		self.ent.config(state = NORMAL)

	def disabledAll(self):
		self.btnMOT.config(state = DISABLED)
		self.btnMHT.config(state = DISABLED)
		self.ent.config(state = DISABLED)

	def flipflopMA(self):
		if (self.status == OFF):
			self.start()
		else:
			self.stop()

	def flipflopHT(self):
		if (self.sens == True):
			self.sensT()
		else:
			self.sensH()

	def start(self):
		if (self.status == OFF):
			self.status = ON
#			self.i = 1
			self.anim()

	def stop(self):
		if (self.status == ON):
			self.status = OFF
			self.btnMOT.config(image = self.imgs[0])

	def sensH(self):
		if (self.sens == False):
			self.sens =True
			self.btnMOT.config(image = self.imgs[0])
			self.btnMHT.config(image = self.refIconMH)

	def sensT(self):
		if (self.sens == True):
			self.sens =False
			self.btnMOT.config(image = self.imgs[0])
			self.btnMHT.config(image = self.refIconMT)

	def anim(self):
		if (self.status == ON):
#			self.lbl.config(image = self.btnMOT[self.i])
			if (self.sens == True):
				self.i += 1
				if (self.i >= 8):
					self.i = 1
			else:
				self.i -= 1
				if (self.i <= 1):
					self.i = 8
			self.btnMOT.config(image = self.imgs[self.i])
			self.after(300, self.anim)

	def setSpeed(self, tpm):
		self.ent.config(state = NORMAL)
		self.ent.delete(0, END)
		self.ent.insert(0, str(tpm))
		self.ent.config(state = "readonly")


# Programme principal de test


if __name__ == "__main__":

	w = Tk()
	w.title('class ImgAnim')
	w.geometry("+50+50")

	im = PanelBroche(w, bg = 'ivory', relief = GROOVE)
	im.pack()
	im.setSpeed(2500)
	frm = Frame(w, bd = 2, bg = 'ivory', padx = 5, pady = 5)
	frm.pack()
	btstart = Button(frm, text="Start M1", command = im.start)
	btstart.pack(side=LEFT)
	btstop = Button(frm, text="Stop M1",   command = im.stop)
	btstop.pack(side=LEFT)
	bth = Button(frm, text="Horaire",   command = im.sensH)
	bth.pack(side=LEFT)
	btt = Button(frm, text="Trigo",     command = im.sensT)
	btt.pack(side=LEFT)

	w.mainloop()
