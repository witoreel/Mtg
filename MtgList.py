#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from MtgCard import MtgCard
import re
import os.path
from os import listdir
from os.path import isfile, join

def MtgList(directory, name, mana, text):

	mana = mana.lower() if mana != None else ""
	name = name.lower() if name != None else ""
	text = text.lower() if text != None else ""

	cards = []
	files = [f for f in listdir(directory) if isfile(join(directory, f))]
	for f in files:
		if f.find('.jpg') > -1:
			card = MtgCard(os.path.join(directory, f))
			
			#Aplica os filtros
			match = True
			if not card.name.lower().find(name) >= 0:
				match = False
			if not card.text.lower().find(text) >= 0:
				match = False
			if not card.mana.lower().find(mana) >= 0:
				match = False

			if match:	
				cards.append(card)

	#Imprime o resultado
	for c in cards:
		print c.name[:30].ljust(30) + c.mana[:10].ljust(10) + c.text[:30].ljust(20)

