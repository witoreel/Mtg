#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from MtgCard import MtgCard
from MtgGet import MtgGetCard
from MtgGet import MtgGetList
from MtgList import MtgList
import argparse
import os.path

class readable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))

def show(file):
	print 'get into '+str(file)

def msearch():
	parser = argparse.ArgumentParser(description='test group')
	subparsers = parser.add_subparsers(help='List of commands')
	sp = subparsers.add_parser('get', help='Get cards from Internet/Library.')
	sp.set_defaults(cmd = 'get')
	sp.add_argument('-c', action='store_true', help='Search a single Card by Name or Number.')
	sp.add_argument('-l', action='store_true', default=True, help='Search cards from a list in a file.')
	sp.add_argument('source', help='Card name in English, Card Number or File with Card List.')
	sp.add_argument('directory', action=readable_dir, help='Output directory where will be stored the new card.')
		
	sp = subparsers.add_parser('show', help='Show metadata information from a card.')
	sp.set_defaults(cmd = 'show')
	sp.add_argument('file', type=argparse.FileType('r'), help='Card file to be shown.')

	sp = subparsers.add_parser('list', help='List cards.')
	sp.set_defaults(cmd = 'list')
	sp.add_argument('-n', '--name', help='List all filtered by name.')
	sp.add_argument('-m', '--mana', help='List all filtered by mana.')
	sp.add_argument('-t', '--text', help='List all filtered by text.')
	sp.add_argument('directory', action=readable_dir, help='Output directory where will be stored the new card.')

	
	args = parser.parse_args()

	if args.cmd == 'get':
		if args.c:
			MtgGetCard(args.source, args.directory)
		elif args.l:
			MtgGetList(args.source, args.directory)
	elif args.cmd == 'show':
		show(args.file)
	elif args.cmd == 'list':
		MtgList(args.directory, args.name, args.mana, args.text)

	
if __name__ == "__main__":
    msearch()
