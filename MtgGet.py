#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from MtgCard import MtgCard
import re
import os.path

def MtgGetCard(card_name, directory):

	card_name = card_name if len(card_name) > 0 else imput('Card to search: ')
	card = MtgCard()

	#Verifica se o nome da carta é o numero do multiverId
	if (card_name.isdigit()):
		card.searchById(card_name, directory)
	else:
		card.searchByName(card_name, directory)


def MtgGetList(list_file, directory):

	file = open(list_file, "r") 
	for l in file: 
		if len(l.strip()) > 0:
			card_name = l.replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').strip()	
			image_name = re.sub(r'\W+', '', card_name.replace(' ', '_')).lower() + ".jpg"
			image_name = os.path.join(directory, image_name)
			if not os.path.isfile(image_name):
				try:
					sys.stdout.write((card_name+'... ').ljust(30))
					sys.stdout.flush()		
					card = MtgCard()
					card.searchByName(card_name, directory)
					sys.stdout.write('OK\n')
				except Exception as e:
					sys.stdout.write('[ERRO]\n')
					image_name = re.sub(r'\W+', '', card_name.replace(' ', '_')).lower() + ".txt"
					file = open(os.path.join(directory, image_name), "w")
					file.write('[ERRO]')
					file.close();	
				sys.stdout.flush()		
