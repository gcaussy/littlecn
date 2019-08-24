#! /usr/bin/env python
# -*- coding:Utf8 -*-

# Exemple de barre d'outils avec expression lambda :

# Suivant que l'on exécute ce script sous Python 3 ou Python 2,
# on utilisera le module Tkinter correspondant :
try:
    from tkinter import *      # module Tkinter pour Python 3
except:
    from Tkinter import *      # module Tkinter pour Python 2

from random import randrange

class ToolBar(Frame):
    "Barre d'outils (petits boutons avec icônes)"
    def __init__(self, boss, images =[], command =None, **Arguments):
        Frame.__init__(self, boss, bd =1, **Arguments)
        # <images> = liste des noms d'icônes à placer sur les boutons
        self.command =command           # commande à exécuter lors du clic
        nBou =len(images)               # Nombre de boutons à construire
        # Les icônes des boutons doivent être placées dans des variables
        # persistantes. Une liste fera l'affaire :
        self.photoI =[None]*nBou
        for b in range(nBou):
            # Création de l'icône (objet PhotoImage Tkinter) :
            self.photoI[b] =PhotoImage(file = images[b] +'.gif')
            # Création du bouton. On fait appel à une fonction lambda
            # pour pouvoir transmettre un argument à la méthode <action> :
            bou = Button(self, image =self.photoI[b], bd =2, relief =GROOVE,
                         command = lambda arg =b: self.action(arg))
            bou.pack(side =LEFT)

    def action(self, index):
        # Exécuter <command> avec l'indice du bouton comme argument :
        self.command(index)

class Application(Frame):
    def __init__(self):
        Frame.__init__(self)
        # noms des fichiers contenant les icones (format GIF):
        icones =('floppy_2', 'coleo', 'papi2', 'pion_1', 'pion_2', 'pion_3',
                 'pion_4', 'help_4', 'clear')
        # Création de la barre d'outils :
        self.barOut =ToolBar(self, images =icones, command =self.transfert)
        self.barOut.pack(expand =YES, fill =X)
        # Création du canevas destiné à recevoir les images :
        self.ca = Canvas(self, width =400, height =200, bg ='orange')
        self.ca.pack()
        self.pack()

    def transfert(self, b):
        if b ==8:
            self.ca.delete(ALL)       # Effacer tout dans le canevas
        else:
            # Recopier l'icône du bouton b (extraite de la barre) => canevas :
            x, y = randrange(25,375), randrange(25,175)
            self.ca.create_image(x, y, image =self.barOut.photoI[b])

Application().mainloop()

