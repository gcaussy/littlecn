#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
from ScrolledText import ScrolledText

class DisplayList(ScrolledText):
	def __init__(self, boss, baseFont = "Courier 8 normal", bg = 'ivory', nZfill = 4, nbcar = 30, nbligne = 30):
		ScrolledText.__init__(self, boss,  bg = bg,   width = nbcar, height = nbligne)
		self.nZfill = nZfill
		self.nbligne = nbligne
		self.lineCount = 0
		self.tag_configure("rouge", foreground = "red",   font = baseFont)
		self.tag_configure("bleu",  foreground = "blue",  font = baseFont)
		self.tag_configure("noir",  foreground = "black", font = baseFont)
		self.tag_configure("vert",  foreground = "green", font = baseFont)
		self.tag_configure("gris",  foreground = "gray",  font = baseFont, background = 'gray95')

	def insertChar(self, char, color):
		self.char = char
		self.color = color
		self.insert(END, self.char, color)

	def insertLine(self, txt, color):
		self.lineCount += 1
		strCount = str(self.lineCount).zfill(self.nZfill)
		self.insert(END, "{} {}".format(strCount, txt), color)
		n = int((self.lineCount / self.height))
#		self.text.yview_moveto(fraction)
		self.text.yview_scroll(n, "pages")

	def clear(self):
		self.config(state=NORMAL)
		self.delete('1.0', END)


# Programme principal de test

if __name__ == "__main__":
	w = Tk()
	w.title('Front panel')
	dl =  DisplayList(w, nbcar = 50, nbligne = 25)
	dl.pack()
	w.mainloop()