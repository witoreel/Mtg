#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from MtgCard import MtgCard
import re
import os.path

def msearch_list():

	if len(sys.argv) < 2:
		print 'Where is the list file?'
		return
	
	if len(sys.argv) < 3:
		print 'Where is the output directory?'
		return
 		
	list_file = sys.argv[1]
	directory = sys.argv[2]

	file = open(list_file, "r") 
	for l in file: 
		if len(l.strip()) > 0:			
			card_name = l.replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').strip()	
			image_name = re.sub(r'\W+', '', card_name.replace(' ', '_')).lower() + ".jpg"
			image_name = os.path.join(directory, image_name)
			if not os.path.isfile(image_name):
				try:
					card = MtgCard()
					card.search(card_name, directory)
				except Exception as e:
					print '[ERROR]: '+card_name
					image_name = re.sub(r'\W+', '', card_name.replace(' ', '_')).lower() + ".txt"
					file = open(os.path.join(directory, image_name), "w")
					file.write('[ERRO]')
					file.close();

				print
				print



	
if __name__ == "__main__":
    msearch_list()
