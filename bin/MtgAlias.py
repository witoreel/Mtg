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
from MtgTools import getCardFilesList 


def aliasByNames(cards_directory, out_directory):
	alias_directory = os.path.join(out_directory, 'ByNames')
	cards = getCardFilesList(cards_directory)

	total = len(cards)
	count = 1
	for card in cards:
		card.loadFromImage()

		directory = card.name
		if hasattr(card, 'expansion_code'):
			filename = card.name + ' ('+card.expansion_code +').card'
		elif hasattr(card, 'expansion_name'):
			filename = card.name + ' ('+card.expansion_name+').card'
		else:
			filename = card.name + '.card'
		card_path = card.path
		filepath = os.path.join(alias_directory, directory)
		if not os.path.exists(filepath):
			os.makedirs(filepath)
		filepath = os.path.join(filepath, filename)
		if not os.path.exists(filepath):
			print '['+str(count)+'/'+str(total)+'] '+filename
			call(["ln", '-s','-r', card_path, filepath])
		count = count + 1


def aliasByTypes(cards_directory, out_directory):
	alias_directory = os.path.join(out_directory, 'ByTypes')
	cards = getCardFilesList(cards_directory)

	total = len(cards)
	types = []
	subtypes = []
	for card in cards:
		card.loadFromImage()
		for t in card.types:
			if not t in types:
				types.append(t)
		if hasattr(card, 'subtypes'):
			for t in card.subtypes:
				if not t in subtypes:
					subtypes.append(t)
		else:
			subtypes.append('')

	all_dirs = []
	for t in types:
		for st in subtypes:
			all_dirs.append([t, st, []])

	total = len(cards)
	count = 1
	for card in cards:
		for d in all_dirs:
			if d[0] in card.types and ((hasattr(card, 'subtypes') and d[1] in card.subtypes) or (not hasattr(card, 'subtypes') and d[1] == '')):
				d[2].append(card)

	for d in all_dirs:
		for card in d[2]:		
			directory = os.path.join(alias_directory, d[0], d[1])
			if not os.path.exists(directory):
				os.makedirs(directory)

			if hasattr(card, 'expansion_code'):
				filename = card.name + ' ('+card.expansion_code +').card'
			elif hasattr(card, 'expansion_name'):
				filename = card.name + ' ('+card.expansion_name+').card'
			else:
				filename = card.name + '.card'

			card_path = card.path
			filepath = os.path.join(directory, filename)
			if not os.path.exists(filepath):
				print '['+str(count)+'/'+str(total)+'] '+filepath
				call(["ln", '-s','-r', card_path, filepath])
			count = count + 1


def aliasByColors(cards_directory, out_directory):
	alias_directory = os.path.join(out_directory, 'ByColors')
	cards = getCardFilesList(cards_directory)
	
	total = len(cards)
	count = 1
	colors = ['I', 'L','B', 'G', 'U', 'R', 'W', 'BG', 'BGR', 'BGRU', 'BGRW', 'BGU', 'BGUR', 'BGUW', 'BGW', 'BGWR', 'BGWU', 'BR', 'BRG', 'BRGU', 'BRGW', 'BRU', 'BRUG', 'BRUW', 'BRW', 'BRWG', 'BRWU', 'BU', 'BUG', 'BUGR', 'BUGW', 'BUR', 'BURG', 'BURW', 'BUW', 'BUWG', 'BUWR', 'BW', 'BWG', 'BWGR', 'BWGU', 'BWR', 'BWRG', 'BWRU', 'BWU', 'BWUG', 'BWUR', 'GB', 'GBR', 'GBRU', 'GBRW', 'GBU', 'GBUR', 'GBUW', 'GBW', 'GBWR', 'GBWU', 'GR', 'GRB', 'GRBU', 'GRBW', 'GRU', 'GRUB', 'GRUW', 'GRW', 'GRWB', 'GRWU', 'GU', 'GUB', 'GUBR', 'GUBW', 'GUR', 'GURB', 'GURW', 'GUW', 'GUWB', 'GUWR', 'GW', 'GWB', 'GWBR', 'GWBU', 'GWR', 'GWRB', 'GWRU', 'GWU', 'GWUB', 'GWUR', 'RB', 'RBG', 'RBGU', 'RBGW', 'RBU', 'RBUG', 'RBUW', 'RBW', 'RBWG', 'RBWU', 'RG', 'RGB', 'RGBU', 'RGBW', 'RGU', 'RGUB', 'RGUW', 'RGW', 'RGWB', 'RGWU', 'RU', 'RUB', 'RUBG', 'RUBW', 'RUG', 'RUGB', 'RUGW', 'RUW', 'RUWB', 'RUWG', 'RW', 'RWB', 'RWBG', 'RWBU', 'RWG', 'RWGB', 'RWGU', 'RWU', 'RWUB', 'RWUG', 'UB', 'UBG', 'UBGR', 'UBGW', 'UBR', 'UBRG', 'UBRW', 'UBW', 'UBWG', 'UBWR', 'UG', 'UGB', 'UGBR', 'UGBW', 'UGR', 'UGRB', 'UGRW', 'UGW', 'UGWB', 'UGWR', 'UR', 'URB', 'URBG', 'URBW', 'URG', 'URGB', 'URGW', 'URW', 'URWB', 'URWG', 'UW', 'UWB', 'UWBG', 'UWBR', 'UWG', 'UWGB', 'UWGR', 'UWR', 'UWRB', 'UWRG', 'WB', 'WBG', 'WBGR', 'WBGU', 'WBR', 'WBRG', 'WBRU', 'WBU', 'WBUG', 'WBUR', 'WG', 'WGB', 'WGBR', 'WGBU', 'WGR', 'WGRB', 'WGRU', 'WGU', 'WGUB', 'WGUR', 'WR', 'WRB', 'WRBG', 'WRBU', 'WRG', 'WRGB', 'WRGU', 'WRU', 'WRUB', 'WRUG', 'WU', 'WUB', 'WUBG', 'WUBR', 'WUG', 'WUGB', 'WUGR', 'WUR', 'WURB', 'WURG', 'BWURG']
	for card in cards:
		card.loadFromImage()
		hasColor = False
		for color in colors:
			color = toColorArray(color)
			found = not hasattr(card, 'colors') and (color[0] == 'Land' and card.getType().lower().find('land') > -1)
			found = found or not hasattr(card, 'colors') and (color[0] == 'Incolor' and card.getType().lower().find('land') == -1)
			found = found or hasattr(card, 'colors') and len(card.colors) == 0 and (color[0] == 'Land' and card.getType().lower().find('land') > -1)
			found = found or hasattr(card, 'colors') and len(card.colors) == 0 and (color[0] == 'Incolor' and card.getType().lower().find('land') == -1)
			found = found or hasattr(card, 'colors') and isArrayEqual(color, card.colors)
			if found:
				hasColor = True
				directory = getArrayDirectory(color)
				if hasattr(card, 'expansion_code'):
					filename = card.name + ' ('+card.expansion_code +').card'
				elif hasattr(card, 'expansion_name'):
					filename = card.name + ' ('+card.expansion_name+').card'
				else:
					filename = card.name + '.card'
				card_path = card.path
				filepath = os.path.join(alias_directory, directory)
				if not os.path.exists(filepath):
					os.makedirs(filepath)
				filepath = os.path.join(filepath, filename)
				if not os.path.exists(filepath):
					print '['+str(count)+'/'+str(total)+'] '+filename
					call(["ln", '-s','-r', card_path, filepath])
		
		if not hasColor:
			if hasattr(card, 'colors'):
				print '[ERROR] ' +card.colors
			else:
				print '[ERROR] ' +card.name
		count = count + 1
				

def isArrayEqual(array_a, array_b):
	for a in array_a:
		if not a in array_b:
			return False
	for b in array_b:
		if not b in array_a:
			return False
	return True

def toColorArray(color):
	array = []
	array.append('Blue') if 'U' in color else None
	array.append('Black') if 'B' in color else None
	array.append('Red') if 'R' in color else None
	array.append('White') if 'W' in color else None
	array.append('Green') if 'G' in color else None
	array.append('Incolor') if 'I' in color else None
	array.append('Land') if 'L' in color else None
	return array

def getArrayDirectory(array):
	directory = ''
	for a in array:
		if len(directory) > 0:
			directory += '-'
		directory += a
	return directory


