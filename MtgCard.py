#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pyexiv2
import json
import os.path
from BeautifulSoup import BeautifulSoup as BSHTML
import urllib2
import urllib
import re

class MtgCard:
	def __init__(self, filepath=""):
		self.path = filepath
		self.name = "No name"
		self.mana = "0"
		self.converted_mana = "0"
		self.main_type = "No type"
		self.sub_type = "No type"
		self.text = "No text."
		self.flavor = "No flavor."
		self.p_t = "0/0"
		self.expansion = "No expansion"
		self.rariry = "Common"
		self.number = '0'
		if len(self.path) > 0:
			self.parse()
	
	def parse(self):
		if not os.path.isfile(self.path):
			print('Invalid card path: '+self.path)
			return;
		metadata = pyexiv2.ImageMetadata(self.path)
		metadata.read()
		try:
			data=json.loads(metadata['Exif.Photo.UserComment'].value)
			self.name = data["name"]
			self.converted_mana = data["converted_mana"]
			self.mana = data["mana"]
			self.main_type = data["main_type"]
			self.sub_type = data["sub_type"]
			self.text = data["text"]
			self.flavor = data["flavor"]
			self.p_t = data["p_t"]
			self.expansion = data["expansion"]
			self.rarity = data["rarity"]
			self.number = data["number"]
		except KeyError:
			return

	def save(self):		
		data = {
			"name" : self.name,
			"mana" : self.mana,
			"converted_mana" : self.converted_mana,
			"main_type" : self.main_type,
			"sub_type" : self.sub_type,
			"text" : self.text,
			"flavor" : self.flavor,
			"p_t" : self.p_t,
			"expansion" : self.expansion,
			"rarity" : self.rarity,
			"number" : self.number
		}
		metadata = pyexiv2.ImageMetadata(self.path)
		metadata.read()
		metadata['Exif.Photo.UserComment']=json.dumps(data)
		metadata.write()
		return True


	def searchById(self, number, directory):
		self.search( '', number, directory)

	def searchByName(self, name, directory):
		self.search( name, 0, directory)

	def search(self, card_name, muid, directory):
		#Carregando a pagina para os metadados
		if muid > 0:
			page = urllib2.urlopen('http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid='+str(muid))
			soup = BSHTML(page)
		elif len(card_name) > 0:
			page = urllib2.urlopen('http://gatherer.wizards.com/Pages/Search/Default.aspx?action=advanced&name=+["'+card_name.replace(' ','%20')+'"]')
			soup = BSHTML(page)

		#Carregando metadados
		try:
			div = soup.find("div", {"id": "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow"})
			self.name = div.findAll('div', attrs={'class':'value'})[0].text.encode('utf-8')
		except AttributeError:
			self.name = card_name

		try:
			div = soup.find("div", {"id": "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow"})
			div = div.findAll('div', attrs={'class':'value'})[0]
			self.mana = ''
			for img in div.findAll('img'):
				self.mana += 'B' if img['alt'] == 'Black' else ''
				self.mana += 'R' if img['alt'] == 'Red' else ''
				self.mana += 'U' if img['alt'] == 'Blue' else ''
				self.mana += 'G' if img['alt'] == 'Green' else ''
				self.mana += 'W' if img['alt'] == 'White' else ''
				self.mana += img['alt'] if img['alt'] != 'Black' and img['alt'] != 'Red' and img['alt'] != 'Blue' and img['alt'] != 'Green' and img['alt'] != 'White' else ''
		except AttributeError:
			self.mana = ""
	
		try:
			div = soup.find("div", {"id": "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow"})
			self.converted_mana = div.findAll('div', attrs={'class':'value'})[0].text.encode('utf-8')
		except AttributeError:
			self.converted_mana = ""

		try:
			div = soup.find("div", {"id": "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow"})
			types = div.findAll('div', attrs={'class':'value'})[0].text.encode('utf-8')
			self.main_type = types[:types.find('—')].strip()
			self.sub_type = types[types.find('—')+3:].strip()
		except AttributeError:
			self.main_type = ""
			self.sub_type = ""

		try:
			div = soup.find("div", {"id": "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow"})
			self.text= div.findAll('div', attrs={'class':'value'})[0].text.encode('utf-8')
		except AttributeError:
			self.text = ""

		try:
			div = soup.find("div", {"id": "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_flavorRow"})
			self.flavor = div.findAll('div', attrs={'class':'value'})[0].text.encode('utf-8')
		except AttributeError:
			self.flavor = ""

		try:
			div = soup.find("div", {"id": "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow"})
			self.p_t = div.findAll('div', attrs={'class':'value'})[0].text.encode('utf-8')
		except AttributeError:
			self.p_t = ""

		try:
			div = soup.find("div", {"id": "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_setRow"})
			self.expansion = div.findAll('div', attrs={'class':'value'})[0].text.encode('utf-8')
		except AttributeError:
			self.expansion = ""

		try:
			div = soup.find("div", {"id": "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow"})
			self.rarity = div.findAll('div', attrs={'class':'value'})[0].text.encode('utf-8')
		except AttributeError:
			self.rarity = ""

		try:
			div = soup.find("div", {"id": "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberRow"})
			self.number = div.findAll('div', attrs={'class':'value'})[0].text.encode('utf-8')
		except AttributeError:
			self.number = ""

		self.name = re.sub(r'[^\x00-\x7f]',r'', self.name) 
		self.mana = re.sub(r'[^\x00-\x7f]',r'', self.mana) 
		self.converted_mana = re.sub(r'[^\x00-\x7f]',r'', self.converted_mana) 
		self.main_type = re.sub(r'[^\x00-\x7f]',r'', self.main_type) 
		self.sub_type = re.sub(r'[^\x00-\x7f]',r'', self.sub_type) 
		self.text = re.sub(r'[^\x00-\x7f]',r'', self.text) 
		self.flavor = re.sub(r'[^\x00-\x7f]',r'', self.flavor) 
		self.p_t = re.sub(r'[^\x00-\x7f]',r'', self.p_t) 
		self.expansion = re.sub(r'[^\x00-\x7f]',r'', self.expansion) 
		self.rariry = re.sub(r'[^\x00-\x7f]',r'', self.rariry) 
		self.number = re.sub(r'[^\x00-\x7f]',r'', self.number) 

		#Carregando a pagina para a imagem
		page = urllib2.urlopen('https://magiccards.info/query?q='+self.name.replace(' ','+')+'&v=card&s=cname')
		soup = BSHTML(page)

		# Coleta o endereco da imagem
		img_url = ''
		for img in soup.findAll("img"):
			if img['src'].find('scans') > -1:
				img_url = 'https://magiccards.info/'+img['src']
		

		image_name = re.sub(r'\W+', '', self.name.replace(' ', '_')).lower() + ".jpg"
		if not os.path.exists(directory):
			os.makedirs(directory)
		self.path = os.path.join(directory, image_name)

		#Define o nome da Imagem a ser salva
		image = urllib.URLopener()
		image.retrieve(img_url,self.path)

		self.save()


	def __str__(self):
		s = "-----------------------------------------------------"
		s +="\nCard name: "+self.name
		s +="\nMana: "+self.mana
		s +="\nConverted mana: "+self.converted_mana
		s +="\nMain type: "+self.main_type
		s +="\nSub type: "+self.sub_type
		s +="\nText: "+self.text
		s +="\nFlavor: "+self.flavor
		s +="\nP/T: "+self.p_t
		s +="\nExpansion: "+self.expansion
		s +="\nRarity: "+self.rarity
		s +="\nNumber: "+self.number
		s +="\n-----------------------------------------------------"
		return s
