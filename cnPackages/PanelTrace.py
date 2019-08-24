#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
try:
	from cnPackages.ScrolledText import ScrolledText
except:
	from ScrolledText import ScrolledText

class PanelTrace(Frame):
	def __init__(self, boss, bg = 'ivory', font = "Helvetica 8 normal", nbChar = 10, nbLine = 30, **Arguments):
		Frame.__init__(self, boss, bg = bg)
		Label(self, text ="Trace", font = "{courier new} 12 bold", bg = bg, fg = "blue").pack()
		self.scr = ScrolledText(self, baseFont = font, width = nbChar, height = nbLine)
		self.scr.pack(expand = YES, fill = BOTH, padx = 8, pady = 8)

	def getScr(self):
		return(self.scr)

	def debug(self, msg):
		self.scr.insertLine("DEBUG: {}\n".format(msg), "rouge", True)

# Programme principal de test
# ---------------------------

if __name__ == "__main__":

	w = Tk()
	w.title('class PanelTrace')
	pdc = PanelTrace(w, nbChar = 50, nbLine = 5, font = "Helvetica 8 normal")
	pdc.pack()
	scr = pdc.getScr()
	for i in range(10):
		scr.insertLine("0123456789012345\n", "bleu", True)
	pdc.debug("Test debug")

	w.mainloop()
