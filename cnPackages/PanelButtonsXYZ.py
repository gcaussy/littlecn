#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *

class PanelButtonsXYZ(Frame):
	def __init__(self, boss, cmd, bg = 'ivory', **Arguments):
		Frame.__init__(self, boss, bg = bg, pady = 2)
		Label(self, text ="Déplacements manuels", font = "{courier new} 12 bold", bg = bg, fg = "blue").grid(row = 1, column = 1, columnspan = 4)

		self.btnYPL = Button(self, text = 'Y+')
		self.btnYPL.config(command = lambda arg = "YPL" : cmd(arg))
		self.btnYPL.grid(row = 2, column = 2)

		self.btnZPL = Button(self, text = 'Z+')
		self.btnZPL.config(command = lambda arg = "ZPL" : cmd(arg))
		self.btnZPL.grid(row = 2, column = 4)

		self.btnXMO = Button(self, text = 'X-')
		self.btnXMO.config(command = lambda arg = "XMO" : cmd(arg))
		self.btnXMO.grid(row = 3, column = 1)

		self.btnXPL = Button(self, text = 'X+')
		self.btnXPL.config(command = lambda arg = "XPL" : cmd(arg))
		self.btnXPL.grid(row = 3, column = 3)

		self.btnYMO = Button(self, text = 'Y-')
		self.btnYMO.config(command = lambda arg = "YMO" : cmd(arg))
		self.btnYMO.grid(row = 4, column = 2)

		self.btnZMO = Button(self, text = 'Z-')
		self.btnZMO.config(command = lambda arg = "ZMO" : cmd(arg))
		self.btnZMO.grid(row = 4, column = 4)

		self.btnList = [self.btnYPL, self.btnZPL, self.btnXMO, self.btnXPL, self.btnYMO, self.btnZMO]

#	def btnAction(self, btnCode):
#		print("Action :", btnCode)

	def disabledAll(self):
		for refBtn in self.btnList:
			refBtn.config(state = DISABLED)

	def enabledAll(self):
		for refBtn in self.btnList:
			refBtn.config(state = NORMAL)

	def enabledZBtn(self):
		for refBtn in [self.btnZPL, self.btnZMO]:
			refBtn.config(state = NORMAL)

	def enabledXYBtn(self):
		for refBtn in [ self.btnXPL,  self.btnXMO, self.btnYPL, self.btnYMO]:
			refBtn.config(state = NORMAL)

#	Enabled/Disabled: X- X+, Y- Y+, Z- Z+

	def disabledXBtn(self):
		for refBtn in [ self.btnXPL,  self.btnXMO]:
			refBtn.config(state = DISABLED)

	def enabledXBtn(self):
		for refBtn in [ self.btnXPL,  self.btnXMO]:
			refBtn.config(state = NORMAL)

	def disabledYBtn(self):
		for refBtn in [ self.btnYPL,  self.btnYMO]:
			refBtn.config(state = DISABLED)

	def enabledYBtn(self):
		for refBtn in [ self.btnYPL,  self.btnYMO]:
			refBtn.config(state = NORMAL)

	def disabledZBtn(self):
		for refBtn in [ self.btnZPL,  self.btnZMO]:
			refBtn.config(state = DISABLED)

	def enabledZBtn(self):
		for refBtn in [ self.btnZPL,  self.btnZMO]:
			refBtn.config(state = NORMAL)

# Programme principal de test
# ---------------------------

if __name__ == "__main__":

	def btnActionExt(btnCode):
		print("Action externe:", btnCode)

	w = Tk()
	w.title('classe PanelButtonsXYZ')
	frm1 = Frame(w)
	pm = PanelButtonsXYZ(frm1, cmd = btnActionExt)
	pm.pack()
	frm1.pack()
	btnDisableAll = Button(w, text = 'DisAll', command = pm.disabledAll).pack(side = LEFT)
	btnEnabledAll = Button(w, text = 'EnaAll', command = pm.enabledAll).pack(side = LEFT)
	btnEnableZ    = Button(w, text = 'EnaZ',   command = pm.enabledZBtn).pack(side = LEFT)
	btnEnableXY   = Button(w, text = 'EnaXY',  command = pm.enabledXYBtn).pack(side = LEFT)
	w.mainloop()
