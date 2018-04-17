#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sys
from MtgCard import MtgCard
import os.path
from gi.repository import Nautilus, GObject

class OnituIconOverlayExtension(GObject.GObject, Nautilus.InfoProvider):
		def __init__(self):
		    pass

		def update_file_info(self, file):
		    if os.path.splitext(file.get_name())[1] == "fileWithEmblem":
		        file.add_emblem("multimedia")


file.add_emblem("my_super_icon.ico")
	

