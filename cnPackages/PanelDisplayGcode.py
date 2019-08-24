#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
try:
	from cnPackages.ScrolledText import ScrolledText
except:
	from ScrolledText import ScrolledText

class PanelDisplayGcode(Frame):
	def __init__(self, boss, bg = 'ivory', font = "Helvetica 8 normal", nbChar = 10, nbLine = 30, **Arguments):
		Frame.__init__(self, boss, bg = bg)
		Label(self, text ="G-Code", font = "{courier new} 12 bold", bg = bg, fg = "blue").pack()
		self.scr = ScrolledText(self, baseFont = font, width = nbChar, height = nbLine)
		self.scr.pack(expand = YES, fill = BOTH, padx = 4, pady = 4)

	def getScr(self):
		return(self.scr)
		
	def setRefresh(self, mode):
		self.scr.setRefresh(mode)

# Programme principal de test
# ---------------------------

if __name__ == "__main__":

	w = Tk()
	w.title('class PanelDisplayGcode')
	pdc = PanelDisplayGcode(w, nbChar = 20, nbLine = 10, font = "Helvetica 8 normal")
	pdc.pack()
	scr = pdc.getScr()
	for i in range(40):
		scr.insertLine("0123456789012345\n", "bleu")

	w.mainloop()
