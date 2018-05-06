#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import os.path
import fnmatch
import json
import sys
from MtgConfig import MtgConfig
from MtgCollection import MtgCollection
from MtgCard import MtgCard
from subprocess import call
from os.path import expanduser
import shutil


def getCardFilesList(files):
	cards = []	
	if os.path.isfile(files):
		if files.find('.card') > -1:
			cards.append(MtgCard(files))
	else:
		for parent, dirnames, filenames in os.walk(files):
			for fn in filenames:
				if fn.find('.card') > -1:
					 cards.append(MtgCard(os.path.join(parent, fn)))
	return cards

#==========================================================================================================================
def filterCards(cards, name, cmc, mana, type, subtype, text, power, price):
	out = []	
	for card in cards:
		card.loadFromImage()
		match = True
		match = match and card.compareName(name) if name != None else match
		match = match and card.compareMana(mana) if mana != None else match 
		match = match and card.compareCMC(cmc) if cmc != None else match
		match = match and card.compareType(type) if type != None else match
		match = match and card.compareSubType(subtype) if subtype != None else match
		match = match and card.compareText(text) if text != None else match
		match = match and card.comparePower(power) if power != None else match
		match = match and card.comparePrice(price) if price != None else match
		
		out.append(card) if match else None	
	
	return out	


#==========================================================================================================================
def sortAndDistinctCards(cards, sort):
	if sort == None:
		cards = sorted(cards, key=lambda card: card.getName())  
	if sort == 'P':
		cards = sorted(cards, key=lambda card: card.getPrice()*card.getQuantity()) 
	elif sort == 'N':
		cards = sorted(cards, key=lambda card: card.getName()) 
	elif sort == 'T':
		cards = sorted(cards, key=lambda card: card.getType()+card.getSubtype())
	else:
		cards = sorted(cards, key=lambda card: card.getName())  

	out = []
	for card in cards:
		found = False
		for o in out:
			if card.getName().lower() == o.getName().lower():
				found = True
				break
		if not found:
			out.append(card)
	
	return out
	
#==========================================================================================================================
def downloadCardsInfo(needsImage, needsPrice, needsOpen,force, files):	

	cards = getCardFilesList(files)
	for card in cards:
		card.loadFromImage()			
		if needsImage:
			if card != None and hasattr(card, 'image_url') and len(card.image_url) > 0 and not force:
				#print 'Skip: '+card.path
				continue
			if card.downloadImage():
				print 'Downloaded: '+card.path
			if needsOpen:
				call(["eog", filepath, '&'])
		if needsPrice:
			if card != None and card.getPrice() > 0 and not force:
				#print 'Skip: '+card.path + ' at ' +card.price
				continue
			if card.downloadPrice():
				print 'Priced: ['+card.price+'] '+card.path


#==========================================================================================================================

def setIgnoreImage(files):	
	cards = getCardFilesList(files)
	for card in cards:
		card.loadFromImage()
		if hasattr(card, 'image_url') and len(card.image_url) > 0:
			return
		card.image_url = 'ignore'
		card.saveMetadata()

#==========================================================================================================================

def createTempView(cards, copy):	
	home_dir = expanduser("~")
	temp_directory = os.path.join(home_dir,'.mtg/.lsresult/')
	shutil.rmtree(temp_directory)
	os.makedirs(temp_directory)
	for card in cards:
		if hasattr(card, 'expansion_code'):
			filename = card.name + ' ('+card.expansion_code +').card'
		elif hasattr(card, 'expansion_name'):
			filename = card.name + ' ('+card.expansion_name+').card'
		else:
			filename = card.name + '.card'
		filepath = os.path.join(temp_directory, filename)
		if not os.path.exists(filepath):
			if copy:
				call(["cp", card.path, filepath])
			else:
				call(["ln", '-s','-r', card.path, filepath])
	call(["nemo", temp_directory])

#==========================================================================================================================
		
def listCards(files, n, t, m, cm, ty, sty, pt, name, cmc, mana, type, subtype, text, power, sprice, op, copy, quantity,price, total, sort):	
	cards = getCardFilesList(files)
	cards = filterCards(cards, name, cmc, mana, type, subtype, text, power, sprice)
	cards = sortAndDistinctCards(cards, sort)
	if op:
		createTempView(cards, copy)
	else:	
		print parseLsLine('#', 'Nome', 'CMC', 'Mana', 'Type', 'SubType', 'P/T', 'Text', 'Qty.', 'Price', 'Total')
		count = 1
		total_cards = 0
		total_price = 0
		for card in cards:
			ls = card.getLsLine(n, t, m, cm, ty, sty, pt, price, quantity, total)
			print parseLsLine(str(count),ls[0], ls[1], ls[2], ls[3], ls[4], ls[5], ls[6], ls[7], ls[8], ls[9])
			total_cards += int(ls[7]) if ls[7] != None else 0
			total_price += ls[9] if ls[9] != None else 0
			count += 1		
		print parseLsLine('', 'TOTAL', '', '', '', '', '', '', str(total_cards), '', ('R$ '+str(total_price)).replace('.',','))


def parseLsLine(order = None, name = None, cmana = None, mana = None, type = None, subtype = None, power = None, text = None, quant = None, price = None, total = None):
	sizes = []
	sizes.append(3) if order != None else None
	sizes.append(21) if name != None else None
	sizes.append(3) if cmana != None else None
	sizes.append(10) if mana != None else None
	sizes.append(15) if type != None else None
	sizes.append(15) if subtype != None else None
	sizes.append(5) if power != None else None
	sizes.append(100) if text != None else None
	sizes.append(3) if quant != None else None
	sizes.append(8) if price != None else None
	sizes.append(10) if total != None else None
	
	its = []
	its.append(order) if order != None else None
	its.append(name) if name != None else None
	its.append(cmana) if cmana != None else None
	its.append(mana) if mana != None else None
	its.append(type) if type != None else None
	its.append(subtype) if subtype != None else None
	its.append(power) if power != None else None
	its.append(text) if text != None else None
	its.append(str(quant)) if quant != None else None
	its.append(str(price)) if price != None else None
	its.append(str(total)) if total != None else None

	max_lines = 1
	for i in range(0, len(its)):
		q = len(its[i]) // sizes[i]
		max_lines = q if q > max_lines else max_lines
	
	ans = '|'
	repeat = True
	line_witdh = 0
	while repeat:
		repeat = False
		for i in range(0, len(its)):
			t = its[i]
			s = sizes[i]
			if len(t) > s:
				ans += t[:s]
				its[i] = t[s:]
			elif len(t) >= 0:
				ans += t.ljust(s)
				its[i] = ''
			if len(its[i]) > 0:
				repeat = True
			ans += '|'		
		line_witdh = len(ans) if line_witdh == 0 else line_witdh
		ans += '\n|' if repeat else ''
	return getSeparatorLine(sizes)+ '\n'+ ans

def getSeparatorLine(sizes):
	ans = ''
	for s in sizes:
		ans += '+'+''.ljust(s, '-')
	return ans

#==========================================================================================================================

def importList(listfile, directory, sum):

	if not os.path.exists(listfile):
		print 'List file not found: '+listfile

	if not os.path.isfile(listfile):
		print 'List isn\'t a file: '+listfile

	if not os.path.exists(directory):
		print 'Directory not found: '+listfile

	f = open(listfile, 'r')
	lines = f.readlines()
	f.close()

	collection = MtgCollection()
	collection.load()

	sub_directory = directory

	total = len(lines)
	row = 0
	missing = ''
	for line in lines:
		row += 1
		l = line.strip()
		if l == '':
			continue 

		if l[0] == '[' and l.find(']') > 0:
			subdir = l[1:l.find(']')].strip()
			if len(subdir) > 0:
				sub_directory = os.path.join(directory, subdir)
				if not os.path.exists(sub_directory):
					os.makedirs(sub_directory)
			continue
	
		if l.lower().find('x') > 0 and l[:l.lower().find('x')].strip().isdigit():
			quantity = int(l[:l.lower().find('x')])
			l = l[l.lower().find('x')+1:].strip()
		elif l.lower().find(' ') > 0 and l[:l.lower().find(' ')].strip().isdigit():
			quantity = int(l[:l.lower().find(' ')])
			l = l[l.lower().find(' ')+1:].strip()


		expansion_code = None
		if l.find('(') > 0 and l.find(')') > 0:
			expansion_code = l[l.find('(')+1:l.find(')')].strip()
			l = l[:l.find('(')].strip()

		isNumber = (l.find(' ') > -1 and l[:l.find(' ')].isdigit()) or l.isdigit()
		name = l

		if isNumber and expansion_code != None:
			card = collection.getCardByNumberAndExpansion(name.replace(' ',''), expansion_code)
		else:
			card = collection.getCardByNameAndExpansion(name, expansion_code)

		if card == None:
			m = '['+str(row)+'/'+str(total)+'] Card Not Found: '+line.strip()
			missing += m+'\n'
			print m
			continue

		if hasattr(card, 'expansion_code') and hasattr(card, 'number') and card.getType().lower().find('land') > -1:
			filename = card.name + ' ('+card.expansion_code+') ['+card.number+'].card'
		elif hasattr(card, 'expansion_code'):
			filename = card.name + ' ('+card.expansion_code +').card'
		elif hasattr(card, 'expansion_name'):
			filename = card.name + ' ('+card.expansion_name+').card'
		else:
			filename = card.name + '.card'
		filepath = os.path.join(sub_directory, filename)
		if not os.path.exists(filepath):
			call(["cp", card.path, filepath])
			
			c = MtgCard(filepath)
			c.loadFromImage()
			c.quantity = quantity
			c.saveMetadata()
			c.updateQuantityEmblem()
			print '['+str(row)+'/'+str(total)+'] Imported: '+name
		else:
			c = MtgCard(filepath)
			c.loadFromImage()
			c.quantity = c.quantity + quantity
			c.saveMetadata()
			c.updateQuantityEmblem()
			print '['+str(row)+'/'+str(total)+'] Skiped: '+name
	
	if len(missing.strip()) > 0:
		f = open(os.path.join(sub_directory, 'missing.txt'),'w')
		f.write(missing)
		f.close()

	call(["nemo", sub_directory])	


def exportToPuca(needsOpen, files, out_file):	
	exportList(needsOpen, files, out_file, True)

def exportToDeckbox(needsOpen, files, out_file):	
	exportList(needsOpen, files, out_file, False)

#==========================================================================================================================
def exportList(needsOpen, files, out_file, hasExpansion):	

	body = ''
	cards = getCardFilesList(files)
	for card in cards:
		card.loadFromImage()			

	cards = sorted(cards, key=lambda card: card.getName()) 
	for card in cards:
		body += str(card.getQuantity())+' '+card.getName()
		if hasExpansion:
			body += ' ('+card.getExpansionCode()+')' if (card.getExpansionCode() != '') else ''
		body += '\n'
	
	f = open(out_file, 'w')
	f.write(body)
	f.close()

	if needsOpen:
		call(['gedit', out_file])









