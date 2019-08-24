#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *

class ScrolledText(Frame):
	def __init__(self, boss, baseFont = "Courier 8 normal", bg = 'ivory', nZfill = 4, width = 30, height = 30, **Arguments):
		Frame.__init__(self, boss, bd = 1, relief = GROOVE)
		self.boss = boss
		self.frm1 = Frame(self, bg = bg)
		self.frm1.pack()
		self.nZfill = nZfill
		self.height = height
		self.text = Text(self.frm1, font = baseFont, bg = bg, bd = 1, width = width, height = height)
		scroll = Scrollbar(self.frm1, bd = 1, command = self.text.yview)
		self.text.configure(yscrollcommand = scroll.set)
		self.text.pack(side = LEFT, expand = YES, fill = BOTH, padx = 2, pady = 2)
		scroll.pack(side = RIGHT, expand = NO, fill = Y, padx = 2, pady = 2)
		self.lineCount = 0
		self.text.tag_configure("rouge", foreground = "red",   font = baseFont)
		self.text.tag_configure("bleu",  foreground = "blue",  font = baseFont)
		self.text.tag_configure("noir",  foreground = "black", font = baseFont)
		self.text.tag_configure("vert",  foreground = "green", font = baseFont)
		self.text.tag_configure("gris",  foreground = "gray",  font = baseFont, background = 'gray95')

		self.refresh = 'Y'

	def setRefresh(self, mode):
		self.refresh = mode
		print("ScrolledText=", mode)

	def insertLine(self, txt, color, num = True):
		self.lineCount += 1
		strCount = str(self.lineCount).zfill(self.nZfill)
		if (num == True):
			self.text.insert(END, "{} {}".format(strCount, txt), color)
		else:
			self.text.insert(END, "{}".format(txt), color)
			
		n = int((self.lineCount / self.height))
		self.text.yview_scroll(n, "pages")
		
		if (self.refresh in ['Y', 'N']):
			if (self.refresh == 'Y'):			
				if (self.lineCount % 50 == 0):				# provoquer le refresh de l'écran tous les x insertions
					self.update()

	def clear(self):
		self.text.config(state=NORMAL)
		self.text.delete('1.0', END)
		self.lineCount = 0
		self.update()

# Programme principal de test

if __name__ == "__main__":
	w = Tk()
	w.title('Front panel')
	scr = ScrolledText(w, width = 50, height = 10)
	scr.pack()
	for i in range(40):
		scr.insertLine("012345678901234567890123456789012345678901234\n", "bleu", False)
	w.mainloop()
