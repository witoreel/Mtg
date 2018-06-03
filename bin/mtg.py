#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from MtgCard import MtgCard
from MtgGet import MtgGetCard
from MtgGet import MtgGetList
from MtgTools import listCards
from MtgConfig import MtgConfig
from MtgCollection import MtgCollection
from MtgTools import downloadCardsInfo
from MtgTools import setIgnoreImage
from MtgTools import importList
from MtgTools import exportToPuca
from MtgTools import exportToDeckbox
from MtgAlias import aliasByNames
from MtgAlias import aliasByColors
from MtgAlias import aliasByCollections
from MtgAlias import aliasByTypes
import argparse
import os.path
from subprocess import call
import time

class readable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))

def mtg():
	#try:
	parser = argparse.ArgumentParser(description='test group')
	subparsers = parser.add_subparsers(help='List of commands')
	sp = subparsers.add_parser('get', help='Get cards from Internet/Library.')
	sp.set_defaults(cmd = 'get')
	sp.add_argument('-c', action='store_true', help='Search a single Card by Name or Number.')
	sp.add_argument('-l', action='store_true', default=True, help='Search cards from a list in a file.')
	sp.add_argument('source', help='Card name in English, Card Number or File with Card List.')
	sp.add_argument('out_directory', action=readable_dir, help='Output directory where will be stored the new card.')
	
	sp = subparsers.add_parser('show', help='Show metadata information from a card.')
	sp.set_defaults(cmd = 'show')
	sp.add_argument('cards_path', help='Path to the cards.')

	#-- Adiciona opções para listagens
	sp = subparsers.add_parser('list', help='List cards.')
	sp.set_defaults(cmd = 'list')
	sp.add_argument('-n', action='store_true', help='List name info.')
	sp.add_argument('-M', action='store_true', help='List convereted mana info.')
	sp.add_argument('-m', action='store_true', help='List mana info.')
	sp.add_argument('-t', action='store_true', help='List type info.')
	sp.add_argument('-s', action='store_true', help='List subtype info.')
	sp.add_argument('-T', action='store_true', help='List text.')
	sp.add_argument('-a', action='store_true', help='List power/toughness info.')
	sp.add_argument('-p', action='store_true', help='List price info.')
	sp.add_argument('-P', action='store_true', help='List total price info.')
	sp.add_argument('-q', action='store_true', help='List quantity info.')
	sp.add_argument('--sort', help='Sort. [P = Price, N = Name, T = Type]')
	sp.add_argument('--all', action='store_true', help='List all info.')
	sp.add_argument('--open', action='store_true', help='List power/toughness info.')
	sp.add_argument('--copy', action='store_true', help='Copy instead symbolic link.')

	sp.add_argument('--name', help='Filter by name.')
	sp.add_argument('--cmc', help='Filter by converted mana cost.')
	sp.add_argument('--mana', help='Filter by mana.')
	sp.add_argument('--type', help='Filter by type.')
	sp.add_argument('--subtype', help='Filter by subtype.')
	sp.add_argument('--text', help='Filter by text.')
	sp.add_argument('--power', help='Filter by power/toughness.')
	sp.add_argument('--price', help='Filter by price (\'<2\', \'>2\', \'2..10\'.')
	sp.add_argument('cards_path', help='Path to the cards.')

	#-- Adiciona opções para configuração
	sp = subparsers.add_parser('cfg', help='Configurations.')
	sp.set_defaults(cmd = 'cfg')
	sp.add_argument('-l', '--library', help='Set library path.')
	sp.add_argument('-d', '--decks', help='Set decks path.')
	sp.add_argument('-s', '--lists', help='Set lists path.')

	#-- Adiciona opções para download
	sp = subparsers.add_parser('download', help='Download data about a card.')
	sp.set_defaults(cmd = 'download')
	sp.add_argument('-i', action='store_true', help='Download the image of a card.')
	sp.add_argument('-p', action='store_true', help='Download the price of a card.')
	sp.add_argument('-f', action='store_true', help='Force download of new image.')
	sp.add_argument('-o', action='store_true', help='Open Card file after download.')
	sp.add_argument('-ig', '--ignore', action='store_true', help='Ignore image download.')
	sp.add_argument('cards_path', help='Path to the cards.')

	#-- Adiciona opções para library	
	sp = subparsers.add_parser('library', help='Options about library.')
	sp.set_defaults(cmd = 'library')
	sp.add_argument('-r', action='store_true', help='Recarrega database from json.')
	sp.add_argument('-v', action='store_true', help='Verify integrity.')
	sp.add_argument('-ef', '--exp_code_from',help='Remap expansion from.')
	sp.add_argument('-et', '--exp_code_to', help='Remap expansion to.')
	sp.add_argument('-an', '--alias_names', action='store_true', help='Create Name Alias Structure.')
	sp.add_argument('-ac', '--alias_colors', action='store_true', help='Create Color Alias Structure.')
	sp.add_argument('-acl', '--alias_collections', action='store_true', help='Create Collection Alias Structure.')

	#-- Adiciona opções para library	
	sp = subparsers.add_parser('alias', help='Options about Alias.')
	sp.set_defaults(cmd = 'alias')
	sp.add_argument('--name', action='store_true', help='Create alias files by name.')
	sp.add_argument('--color', action='store_true', help='Create alias files by color.')
	sp.add_argument('--type', action='store_true', help='Create alias files by type.')
	sp.add_argument('--collection', action='store_true', help='Create alias files by collection.')
	sp.add_argument('cards_path', help='Path to the cards.')
	sp.add_argument('alias_directory', help='Base directory to put the alias.')


	#-- Adiciona opções para load	
	sp = subparsers.add_parser('import', help='Options about Import.')
	sp.set_defaults(cmd = 'import')
	sp.add_argument('--sum', action='store_true', help='Sum cards with same Name/Exp.')
	sp.add_argument('cards_path', help='Path to the cards.')
	sp.add_argument('out_directory', help='DBase directory to put the imported cards.')

	sp = subparsers.add_parser('export', help='Options about Export.')
	sp.set_defaults(cmd = 'export')
	sp.add_argument('-o', action='store_true', help='Open file on finish.')
	sp.add_argument('--puca', action='store_true', help='PucaTrade format.')
	sp.add_argument('--dbox', action='store_true', help='DeckBox format.')
	sp.add_argument('cards_path', help='Path to the cards.')
	sp.add_argument('out_file', help='File of the list.')


	sp = subparsers.add_parser('test', help='Options about Export.')
	sp.set_defaults(cmd = 'test')

	args = parser.parse_args()

	if args.cmd == 'get':
		if args.c:
			MtgGetCard(args.source, args.out_directory)
		elif args.l:
			MtgGetList(args.source, args.out_directory)
	elif args.cmd == 'list':		
		if args.all:
			listCards(args.cards_path, True, True, True, True, True, True, True, args.name, args.cmc, args.mana, args.type, args.subtype, args.text, args.power, args.price, args.open, args.copy, True, True, True, args.sort)
		else:
			listCards(args.cards_path, args.n, args.T, args.m, args.M, args.t, args.s, args.a, args.name, args.cmc, args.mana, args.type, args.subtype, args.text, args.power, args.price, args.open, args.copy, args.p, args.P, args.q, args.sort)
	elif args.cmd == 'download':
		if args.ignore:
			setIgnoreImage(args.cards_path)
		else:
			downloadCardsInfo(args.i, args.p, args.o, args.f, args.cards_path)
	elif args.cmd == 'library':
		collection = MtgCollection()
		collection.load()
		if args.r:
			collection.importFromJson()
		elif args.v:
			collection.verifyIntegrity()
		elif args.exp_code_from and args.exp_code_to:
			collection.remapExpansionCode(args.exp_code_from, args.exp_code_to)
		elif args.alias_names:
			collection.aliasByNames()
		elif args.alias_colors:
			collection.aliasByColors()
		elif args.alias_collections:
			collection.aliasByCollections()
	elif args.cmd == 'import':
		importList(args.cards_path, args.out_directory, args.sum)
	elif args.cmd == 'export':
		if args.puca:
			exportToPuca(args.o, args.cards_path, args.out_file)
		if args.dbox:
			exportToDeckbox(args.o, args.cards_path, args.out_file)
	elif args.cmd == 'alias':
		if args.name:
			aliasByNames(args.cards_path, args.alias_directory)
		if args.color:
			aliasByColors(args.cards_path, args.alias_directory)
		if args.type:
			aliasByTypes(args.cards_path, args.alias_directory)
		if args.collection:
			aliasByCollections(args.cards_path, args.alias_directory)
	elif args.cmd == 'test':
		collection = MtgCollection()
		collection.load()
		collection.printAllExpansions()
		
	#except:
	#	print 'Saindo...'
	
if __name__ == "__main__":
    mtg()
