#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import os.path
import fnmatch
import json
import sys
from MtgConfig import MtgConfig
from MtgCard import MtgCard
from subprocess import call

class MtgCollection:

	def __init__(self, filepath=""):
		self.config = MtgConfig()
		self.directory =  os.path.join(self.config.collection_path, 'ByCollections')
		self.json_file = self.config.collection_json
		self.generic_card = self.config.generic_card
		self.useCache = False

	def load(self):
		loaded = False
		if self.useCache:
			loaded = self.loadFromCache()

		if not loaded:
			self.cards = []
			for root, dirnames, filenames in os.walk(self.directory):
				for filename in fnmatch.filter(filenames, '*.card'):
					filepath = os.path.join(root, filename)
					c = MtgCard(filepath)
					if c.loadFromImage():
						self.cards.append(c)
			if self.useCache:
				self.saveToCache()	

	def loadFromCache(self):
		cache_file = os.path.join(self.directory, 'cache.json')
		if os.path.exists(cache_file):
			f = open(cache_file, 'r')
			js = json.loads(f.read())
			self.cards = []
			for j in js:
				c = MtgCard()
				c.loadFromJson(j)
				self.cards.append(c)

			print 'Successful loaded from cache: '+str(len(self.cards)) +' cartas'
			return True
		return False


	def saveToCache(self):
		cache_file = os.path.join(self.directory, 'cache.json')
		f = open(cache_file, 'w')
		print len(self.cards)
		js = json.dumps([c.__dict__ for c in self.cards])
		f.write(js)
		f.close()
		print 'Arquivo de cache atualizado: '+cache_file


	def getCardById(self, id):
		for c in self.cards:
			if c.multiverse_id == id:
				return c
		return None

	def getCardByName(self, name):
		for c in self.cards:
			if c.compareName(name):
				return c
		return None

	def getCardByNameAndExpansion(self, name, expansion_code = None):
		out = []
		for c in self.cards:
			if c.getName().lower() == name.lower() and (expansion_code == None or c.getExpansionCode().lower() == expansion_code.lower()):
				out.append(c)

		newer = None
		for c in out:
			newer = c if newer == None else newer
			newer = c if c.getExpansionRelease() > newer.getExpansionRelease() else newer		
		return newer

	def getCardByNumberAndExpansion(self, number, expansion_code = None):
		out = []
		for c in self.cards:
			if hasattr(c, 'number') and hasattr(c, 'expansion_code'):
	  			if c.getNumber().lower() == str(number).lower() and (expansion_code == None or c.getExpansionCode().lower() == expansion_code.lower()):
		   			out.append(c)

		newer = None
		for c in out:
			newer = c if newer == None else newer
			newer = c if c.getExpansionRelease() > newer.getExpansionRelease() else newer		
		return newer

	def getCardByFile(self, file):
		for c in self.cards:
			if c.path == file:
				return c


	def remapExpansionCode(self, code_from, code_to):
		for c in self.cards:
			if c.expansion_code.lower() == code_from.lower():
				c.expansion_code = code_to.upper()
				c.saveMetadata()
				print 'Remaped: '+c.path


	def sort(self):
		sorted(self.cards, key=lambda card: card.sortText())


	def verifyIntegrity(self):
		self.sort()
		code = ''
		number = 1
		for c in self.cards:
			if code != self.expansion_code:
				code = self.expansion_code 
				number = 1
			if c.number != n:
				print 'Card not found: ['+code +'] '+ n
			else:
				number += 1
			number += 1
			
	def downloadCardsInfo(self, needsImage, needsPrice, needsOpen, files):	
		if os.path.isfile(files):
			self.downloadSingleCardInfo(needsImage, needsPrice, needsOpen, files)
		else:
			count = 1		
			total = len(files)
			for parent, dirnames, filenames in os.walk(files):
				for fn in filenames:
					sys.stdout.write('['+str(count)+']')
					sys.stdout.flush()
					count+=1
					self.downloadSingleCardInfo(needsImage, needsPrice, needsOpen, os.path.join(parent, fn))


	def downloadSingleCardInfo(self, needsImage, needsPrice, needsOpen, filepath):
		if needsImage:
			card = self.getCardByFile(os.path.abspath(filepath))
			if hasattr(card, 'image_url'):
				print 'Skip: '+card.path
				return

			if card.downloadImage():
				print 'Downloaded: '+card.path
			if needsOpen:
				call(["eog", filepath, '&'])

	def printAllExpansions(self):
		exp = []
		exp_code = []
		for c in self.cards:
			i

		for i in range(0, len(exp)):
			print exp_code[i] +'\t'+exp[i]


	def importFromJson(self):
		if not os.path.exists(self.json_file):
			print('Invalid JSON path: '+self.json_file)
			return;

		file = open(self.json_file, "r")
		body = file.read()
		file.close();	
		self.json_collection = json.loads(body)

		exp_n = []
		exp_c = []

		for expansion in self.json_collection.iteritems():
			exp = expansion[1]
			exp_code = exp["code"]
			exp_name = exp["name"]
			exp_release = exp["releaseDate"]
			exp_cards = exp["cards"]
			print exp_code

			if not exp_code in exp_c:
				exp_c.append(exp_code)
				exp_n.append(exp_name)

			continue

			release_year = exp_release[:exp_release.find('-')]
			directory = os.path.join(self.directory, '['+release_year+'] '+exp_name)
			if not os.path.exists(directory):
				os.makedirs(directory)

			for exp_card in exp_cards:
				card = MtgCard()			
				if card.loadFromJson(exp_card):				
					card.expansion_code = exp_code
					card.expansion_name = exp_name
					card.expansion_release = exp_release

					card.setCardDirectory(directory)
					if self.getCardByFile(card.path) != None:
						print 'Skip: '+card.path
						continue

					card.saveCardFile(self.generic_card)
					card.saveMetadata()
					print 'Imported: '+card.path
				else:
					print 'Failed to load: '+ str(exp_card)
		
		for i in range(0, len(exp_n)):
			print exp_c[i] +'\t'+exp_n[i]
