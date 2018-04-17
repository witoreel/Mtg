#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from MtgCard import MtgCard
import os.path

def mcat():
	filepath = os.path.join(os.getcwd(),sys.argv[1])
	if not os.path.isfile(filepath):
			print('Invalid card path: '+filepath)
			return;

	card = MtgCard(filepath)
	print card
	
if __name__ == "__main__":
    mcat()
