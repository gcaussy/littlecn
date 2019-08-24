#!/usr/bin/python3
# -*- coding:Utf-8 -*-
from tkinter import *
from threading import Thread
import time
from AnalyseGcode import *
from Automate import *
from ButtonFlipFlop import *
from CmdsIntermed import *
from DataParam import *
from DisplayList import *
from EntryRegx import *
from PanelBroche import *
from PanelButtonsCmd import *
from PanelButtonsXYZ import *
from PanelDisplayCmdsMotors import *
from PanelDisplayGcode import *
from PanelDisplayPiece import *
from PanelDisplayXYZ import *
from PanelMoteurs import *
from PanelSettingsMan import *
from PanelTrace import *
from ScrolledText import *
from ThreadMoteurs import *
from WinParam import *
print("Fin des imports")
ag = AnalSyntaxGcode()
am = Automate(None, None)
bff = ButtonFlipFlop()
