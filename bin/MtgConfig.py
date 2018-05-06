#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os.path
from os.path import expanduser
import ConfigParser

class MtgConfig:

	# Construtor
	def __init__(self):
		self.home_dir = expanduser("~")
		self._CONFIG_FILE = os.path.join(self.home_dir,'.mtg/mtg.cfg')
		if not os.path.exists(self._CONFIG_FILE):
			print 'Inicializando arquivo de configuração...'
			self.init()
		else:
			self.load()



	#Inicializa o arquivo com configurações iniciais
	def init(self):
		config = ConfigParser.ConfigParser()

		config.add_section('COLLECTION')
		config.set('COLLECTION', 'path', '~/.mtg/library') 
		config.set('COLLECTION', 'json', '~/.mtg/AllSets.json') 
		config.set('COLLECTION', 'generic', '~/.mtg/generic.jpg') 

		config.add_section('LIBRARY')
		config.set('LIBRARY', 'path', '~/.mtg/library') 

		config.add_section('DECKS')
		config.set('DECKS', 'path', '~/.mtg/decks') 

		config.add_section('LISTS')
		config.set('LISTS', 'path', '~/.mtg/lists') 

		if not os.path.exists('~/.mtg/collection'.replace('~',self.home_dir)):
			os.makedirs('~/.mtg/collection'.replace('~',self.home_dir))
		if not os.path.exists('~/.mtg/library'.replace('~',self.home_dir)):
			os.makedirs('~/.mtg/library'.replace('~',self.home_dir))
		if not os.path.exists('~/.mtg/lists'.replace('~',self.home_dir)):
			os.makedirs('~/.mtg/lists'.replace('~',self.home_dir))
		if not os.path.exists('~/.mtg/decks'.replace('~',self.home_dir)):	
			os.makedirs('~/.mtg/decks'.replace('~',self.home_dir))

		with open(self._CONFIG_FILE, 'w') as configfile:
			config.write(configfile)

		self.load()


	#Carrega as configurações
	def load(self):
		config = ConfigParser.ConfigParser()
		config.read(self._CONFIG_FILE)

		self.collection_path = config.get('COLLECTION','path').replace('~', self.home_dir)
		self.collection_json = config.get('COLLECTION','json').replace('~', self.home_dir)
		self.generic_card = config.get('COLLECTION','generic').replace('~', self.home_dir)

		self.library_path = config.get('LIBRARY', 'path').replace('~', self.home_dir)

		self.decks_path = config.get('DECKS', 'path').replace('~', self.home_dir)

		self.lists_path = config.get('LISTS', 'path').replace('~', self.home_dir)
		

	#ToString
	def __str__(self):
		s = "library.path = "+self.library_path
		s += "\ndecks.path = "+self.decks_path
		s += "\nlists.path = "+self.lists_path
		return s
