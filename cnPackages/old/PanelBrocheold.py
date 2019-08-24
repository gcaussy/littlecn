#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *

class PanelBroche(Frame):
	ON = True
	OFF = False


	def __init__(self, boss, bg = 'ivory', relief = GROOVE, **Arguments):
		Frame.__init__(self, boss, bd = 2, bg = bg, relief = relief, padx = 5, pady = 2)
		self.refIconM0 = PhotoImage(file = './images/mot0.gif')
		self.refIconM1 = PhotoImage(file = './images/mot1.gif')
		self.refIconM2 = PhotoImage(file = './images/mot2.gif')
		self.refIconM3 = PhotoImage(file = './images/mot3.gif')
		self.refIconM4 = PhotoImage(file = './images/mot4.gif')
		self.refIconM5 = PhotoImage(file = './images/mot5.gif')
		self.refIconM6 = PhotoImage(file = './images/mot6.gif')
		self.refIconM7 = PhotoImage(file = './images/mot7.gif')
		self.refIconM8 = PhotoImage(file = './images/mot8.gif')

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

		frm1= Frame(self)
		frm1.pack()
		Label(frm1, text = "Broche", bg = bg, fg = 'blue').pack()
		frm2 = Frame(self, bg = bg)
		frm2.pack()
		self.lbl = Label(frm2, bg = bg, image = self.imgs[1])
		self.lbl.grid(row = 1, column = 1)
		self.ent = Entry(frm2, width = 6, state = 'readonly', justify = RIGHT)
		self.ent.grid(row = 1, column = 2, padx = 10)
		Label(frm2, text = "t/mn", bg = bg).grid(row = 1, column = 3)

		self.status = OFF
		self.i = 1
		self.sens = True
		self.anim()

	def start(self):
		if (self.status == ON):
			return()
		self.status = ON
#		self.i = 1
		self.anim()

	def stop(self):
		self.status = OFF
#		self.lbl.config(image = self.imgs[1])

	def sensH(self):
		self.sens =True

	def sensT(self):
		self.sens =False

	def anim(self):
		if (self.status == ON):
#			self.lbl.config(image = self.imgs[self.i])
			if (self.sens == True):
				self.i += 1
				if (self.i >= 8):
					self.i = 1
			else:
				self.i -= 1
				if (self.i <= 1):
					self.i = 8
			self.lbl.config(image = self.imgs[self.i])
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
	frm = Frame(w, bd = 2, bg = 'ivory', relief = GROOVE, padx = 5, pady = 5)
	frm.pack()
	btstart = Button(frm, text="Start", command = im.start)
	btstart.pack(side=LEFT)
	btstop = Button(frm, text="Stop",   command = im.stop)
	btstop.pack(side=LEFT)
	bth = Button(frm, text="Horaire",   command = im.sensH)
	bth.pack(side=LEFT)
	btt = Button(frm, text="Trigo",     command = im.sensT)
	btt.pack(side=LEFT)

	w.mainloop()