#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from gi.repository import Nemo, GObject, Gtk, GdkPixbuf
import urllib, os, subprocess, re
import locale, gettext
from subprocess import call

APP_NAME = "nemo-pyextensions"
LOCALE_PATH = "/usr/share/locale/"
NAUPYEXT_MTG = 'NAUPYEXT_MTG'
ICONPATH = "~/.mtg/bin/icons/mtg.png"

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP_NAME, LOCALE_PATH)
gettext.textdomain(APP_NAME)
_ = gettext.gettext

class MtgActions(GObject.GObject, Nemo.MenuProvider):

    def __init__(self):
        try:
            factory = Gtk.IconFactory()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(ICONPATH)
            iconset = Gtk.IconSet.new_from_pixbuf(pixbuf)
            factory.add("mtg", iconset)
            factory.add_default()
        except: pass

    #def run(self, menu, element_1, element_2):
    #    """Runs the Meld Comparison of selected files/folders"""
    #    subprocess.call("meld %s %s &" % (element_1, element_2), shell=True)

    def meld_save(self, menu, element):
		call(['gedit', ' ', '&'])

    def get_file_items(self, window, sel_items):
        """Adds the 'Add To Audacious Playlist' menu item to the Nemo right-click menu,
           connects its 'activate' signal to the 'run' method passing the list of selected Audio items"""
		call(['gedit', ' ', '&'])
        num_paths = len(sel_items)
        if num_paths == 0: return
        uri_raw = sel_items[0].get_uri()
        if len(uri_raw) < 7: return
        element_1 = urllib.unquote(uri_raw[7:])
         
        top_menuitem = Nemo.MenuItem(name='Mtg::actions',
                                         label=_('MTG Manage'),
                                         tip=_('Tools for managing your MTG Collection'),
                                         icon='mtg')
        submenu = Nemo.Menu()
        top_menuitem.set_submenu(submenu)
        sub_menuitem_save = Nemo.MenuItem(name='Mtg::download_price',
                                              label=_('Reload prices'),
                                              tip=_('Download and show selected cards prices.'),
                                              icon='prices')
        sub_menuitem_save.connect('activate', self.meld_save, element_1)
        submenu.append_item(sub_menuitem_save)
        return top_menuitem
