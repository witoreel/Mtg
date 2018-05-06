#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pyexiv2
import json
import os.path
from BeautifulSoup import BeautifulSoup as BSHTML
import urllib2
import urllib
import re
from subprocess import call
from shutil import copyfile
from subprocess import call
import inflect


class MtgCard:

	#Construtores
	def __init__(self, filepath=""):
		if len(filepath) > 0:
			if not os.path.exists(filepath):
				print('Invalid card file: '+filepath)
				return;
		self.path = filepath


	#Carrega o objeto a partir de um Json bruto
	def loadFromJson(self, data):
		self.__dict__ = json.loads(json.dumps(data))
		if hasattr(self, 'name'):
			if len(self.name) > 0:
				return True
		return False


	#Deserializa o objeto json
	def loadFromImage(self):		
		try:
			old_path = self.path
			metadata = pyexiv2.ImageMetadata(self.path)
			metadata.read()
			self.__dict__ = json.loads(metadata['Exif.Photo.UserComment'].value)
			self.path = old_path
			return True
		except:
			os.remove(self.path)
			return False


	#Define o endereço da carta com base no diretorio passado
	def setCardDirectory(self, directory):
		if not os.path.exists(directory):
			print('Invalid directory: '+directory)
			return;
		filename = self.getCardFileName()
		self.path = os.path.join(directory,filename)

	#Define o endereço da carta
	def setCardPath(self, path):
		if not os.path.exists(path):
			print('Invalid card file: '+path)
			return;
		self.path = path


	#Serializa o objeto para json
	def saveMetadata(self):		
		metadata = pyexiv2.ImageMetadata(self.path)
		metadata.read()
		metadata['Exif.Photo.UserComment']=self.toJson()
		metadata.write()
		return True

	def toJson(self):
		return json.dumps(self.__dict__)

	#Cria o arquivo de carta
	def saveCardFile(self, tmp_image):
		copyfile(tmp_image, self.path)


	#Carrega imagem da internet
	def downloadImage(self):
		
		img_url = ''
		try:
			if len(img_url) == 0 and hasattr(self, 'number') and hasattr(self, 'expansion_code'):
				page = urllib2.urlopen('https://magiccards.info/'+self.expansion_code.lower()+'/en/'+str(self.number)+'.html')
				soup = BSHTML(page)
				img_url = ''
				for img in soup.findAll("img"):
					if img['src'].find('scans') > -1:
						img_url = 'https://magiccards.info/'+img['src']
		except urllib2.HTTPError:
			print '[404] https://magiccards.info/'+self.expansion_code.lower()+'/en/'+str(self.number)+'.html'
		except UnicodeDecodeError:
			print '[Unicode] https://magiccards.info/query?q='+self.name.replace(' ', '%20').replace('\'', '%27').replace('û', '%FB')+'+e%3A'+self.expansion_code+'%2Fen&v=card&s=cname'
				
		if len(img_url) == 0 and hasattr(self, 'multiverseid'):
			if hasattr(self, 'multiverseid'):
				img_url = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='+str(self.multiverseid)+'&type=card'
			else:
				if hasattr(self, 'number'):
					print 'No MultiverseId: '+self.expansion_code.lower()+"/"+self.number+" ("+self.path+")"
				else:
					print 'No Metadata: '+self.path
				return False

		try:
			if len(img_url) == 0 and hasattr(self, 'name') and hasattr(self, 'expansion_code'):
				page = urllib2.urlopen('https://magiccards.info/query?q='+self.name.replace(' ', '%20').replace('\'', '%27').replace('û', '%FB')+'+e%3A'+self.expansion_code+'%2Fen&v=card&s=cname')
				soup = BSHTML(page)
				img_url = ''
				for img in soup.findAll("img"):
					if img['src'].find('scans') > -1:
						img_url = 'https://magiccards.info/'+img['src']
		except urllib2.HTTPError:
			print '[404] https://magiccards.info/query?q='+self.name.replace(' ', '%20').replace('\'', '%27').replace('û', '%FB')+'+e%3A'+self.expansion_code+'%2Fen&v=card&s=cname'
		except UnicodeDecodeError:
			print '[Unicode] https://magiccards.info/query?q='+self.name.replace(' ', '%20').replace('\'', '%27')+'+e%3A'+self.expansion_code+'%2Fen&v=card&s=cname'

		try:
			self.loadFromImage()
			image = urllib.URLopener()
			image.retrieve(img_url,self.path)

			self.image_url = img_url
			self.saveMetadata()
		except:
			if hasattr(self, 'expansion_code'):
				print '404 Page not found: ['+self.expansion_code+'] '+self.path
			else:
				print '404 Page not found: '+self.path
			return False
		return True


	#Carrega imagem da internet
	def downloadPrice(self):
		
		price = 'R$ 0,00'
		try:
			page = urllib2.urlopen('https://www.ligamagic.com.br/?view=cards%2Fsearch&card='+self.name.replace(' ','+'))
			soup = BSHTML(page)
			for div in soup.findAll("div", {'id' : 'precos-medio'}):
				price = div.text			
		except urllib2.HTTPError:
			print '[404] https://www.ligamagic.com.br/?view=cards%2Fsearch&card='+self.name.replace(' ','+')
				
		self.loadFromImage()
		self.price = price
		self.saveMetadata()
		return True


	#Verifica se a carta corresponde ao nome
	def compareName(self, key):
		return self.getName().lower().find(key.lower()) > -1

	#Verifica se a carta corresponde a mana
	def compareMana(self, key):
		m = self.getManaCost().lower()
		ans = True
		for c in key:
			ans = ans and m.find(c) > -1
			m = m.replace(c, '')
		ans = ans and len(m) == len(re.sub('[burgw]', '', m))
		return ans

	#Verifica se a carta corresponde a cmc
	def compareCMC(self, key):
		return hasattr(self, 'cmc') and self.cmc == key

	#Verifica se a carta corresponde a type
	def compareType(self, key):
		return self.getType().lower().find(key.lower()) > -1

	#Verifica se a carta corresponde a subtype
	def compareSubType(self, key):
		return self.getSubType().lower().find(key.lower()) > -1

	#Verifica se a carta corresponde a text
	def compareText(self, key):
		return self.getText().lower().find(key.lower()) > -1

	#Verifica se a carta corresponde a power
	def comparePower(self, key):
		return self.getPowerToughness().lower() == key.lower()

	#Verifica se a carta corresponde a preço
	def comparePrice(self, key):
		if len(key) > 0 and key[0] == '>':
			return self.getPrice() >= float(key[1:]) 
		if len(key) > 0 and key[0] == '<':
			return self.getPrice() <= float(key[1:])
		if len(key) > 0 and key.find('..') > -1:
			a = float(key[:key.find('..')])
			b = float(key[key.find('..')+2:])
			return self.getPrice() <= b and self.getPrice() >= a


	def compareId(self, id):
		if hasattr(self, 'multiverseid'):
			return self.multiverseid == id
		return False


	#Sobreescreve o metodo toString
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
		s += " ("+self.month+"/"+self.year+")" if self.month != None and self.year != None else ""
		s +="\nRarity: "+self.rarity
		s +="\nNumber: "+self.number
		s +="\n-----------------------------------------------------"
		return s


	def updateQuantityEmblem(self):
		p = inflect.engine()
		emblem = 'emblem-'+p.number_to_words(self.quantity)
		call(['gvfs-set-attribute','-t','stringv',self.path,'metadata::emblems', emblem])

	#Converte pra unicode e remove espaços duplicados
	#def toUnicode(self, s):
	#	s = s.encode('utf-8');
	#	for i in range(1,10):
	#		s = s.replace('  ', ' ')	
	#	return re.sub(r'[^\x00-\x7f]',r'', str(s)) 


	#Formata o nome da carta
	def getCardFileName(self):
		mask = '%n - %s.card'
		s = mask
		if hasattr(self, 'number'):
			#s = s.replace('%n', self.toUnicode(self.number))
			s = s.replace('%n', str(self.number))
		else:
			s = s.replace('%n - ', '')		
		#s = s.replace('%s', self.toUnicode(self.name))
		s = s.replace('%s', self.name)
		return s


	#Lista as cartas conforme os parametros passados
	def getLsLine(self, n, t, m, cm, ty, sty, pt, pr, tot, q):
		its = []
		its.append(self.getName() if n else None) 
		its.append(self.getConvertedMana() if cm else None)
		its.append(self.getManaCost() if m else None) 
		its.append(self.getType() if ty else None) 
		its.append(self.getSubType() if sty else None) 
		its.append(self.getPowerToughness() if pt else None) 
		its.append(self.getText() if t else None) 	
		its.append(self.getQuantity() if q else None) 	
		its.append(self.getPrice() if pr else None) 
		its.append(self.getTotal() if tot else None) 


		return its

	#Get the object used to Sort
	def sortText(self):
		if hasattr(self, 'number') and hasattr(self, 'expansion_code'):
			return [self.expansion_code, self.number]
		elif hasattr(self, 'expansion_code') and hasattr(self, 'name'):
			return [self.expansion_code, self.name]
		else:
			return [self.name]

	# Get Types
	def getType(self):
		ans = ''
		if hasattr(self, 'types'):
			for t in self.types:
				ans += ' '+t if (len(ans) > 0) else t
		return ans

	# Get Subtaypes
	def getSubType(self):
		ans = ''
		if hasattr(self, 'subtypes'):
			for t in self.subtypes:
				ans += ' '+t if (len(ans) > 0) else t
		return ans

	# Get Power/Toughness
	def getPowerToughness(self):
		return self.power+'/'+self.toughness if hasattr(self, 'power') and hasattr(self, 'toughness') else ''

	# Get ManaCost
	def getManaCost(self):
		return (self.manaCost.replace('{',' ').replace('}','').replace('/','|') if hasattr(self, 'manaCost') else '').strip()

	# Get ConvertedManaCost
	def getConvertedMana(self):
		return str(self.cmc) if hasattr(self, 'cmc') else ''

	# Get ConvertedManaCost
	def getExpansionCode(self):
		return str(self.expansion_code) if hasattr(self, 'expansion_code') else ''

	# Get Text
	def getText(self):
		return self.text.replace('\n', ' ') if hasattr(self, 'text') else ''

	def getNumber(self):
		return self.number.encode('ascii',errors='ignore') if hasattr(self, 'number') else ''


	def getName(self):
		return self.name if hasattr(self, 'name') else ''

	def getExpansionRelease(self):
		return self.expansion_release if hasattr(self, 'expansion_release') else ''

	def getQuantity(self):
		return int(self.quantity) if hasattr(self, 'quantity') else 1

	def getPrice(self):
		return float(self.price.replace('R', '').replace('$', '').replace(' ', '').replace(',', '.')) if hasattr(self, 'price') else 0

	def getTotal(self):
		if hasattr(self, 'price') and hasattr(self, 'quantity'):
			p = self.price.replace('R', '').replace('$', '').replace(' ', '').replace(',', '.')
			p = float(p)
			return p * int(self.quantity)
		return 0


