#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from MtgCard import MtgCard
import re
import os.path
import urllib2
import urllib
from bs4 import BeautifulSoup  as BSHTML

def MtgGetCard(key, directory):
	key = key if len(key) > 0 else imput('Card to search: ')

	#Carregando a pagina para os metadados
	if key.isdigit():
		page = urllib2.urlopen('http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid='+str(key))
		soup = BSHTML(page)
	else:
		page = urllib2.urlopen('http://gatherer.wizards.com/Pages/Search/Default.aspx?action=advanced&name=+["'+key.replace(' ','%20')+'"]')
		soup = BSHTML(page)

	multiverse_id = 0
	try:
		multiverse_id = int(page.url[page.url.rfind('=')+1:])
	except AttributeError:
		return False

	if multiverse_id == 0:
		return False

	#Carregando pagina para pegar legalidade e coleções
	ids_list = []
	page = urllib2.urlopen('http://gatherer.wizards.com/Pages/Card/Printings.aspx?multiverseid='+str(multiverse_id))
	soup = BSHTML(page)
	try:
		for i in range(0,100):
			a = soup.find("a", {"id": "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_PrintingsList_listRepeater_ctl0"+str(i)+"_cardTitle"})
			if a == None:
				break
			href = a["href"]
			try:
				muid = href[href.rfind("=")+1:]
			except AttributeError:
				muid = 0

			if muid > 0:			
				ids_list.append(muid)
	except AttributeError:
		self.text = ""

	for muid in ids_list:
		card = MtgCard()
		card.search(muid, directory)
		print card



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
