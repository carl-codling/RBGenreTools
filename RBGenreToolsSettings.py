from os import system, path

import rb
from gi.repository import RB, Gtk, Gio, GObject, PeasGtk

import gettext
gettext.install('rhythmbox', RB.locale_dir())

class RBGenreToolsSettings (GObject.Object, PeasGtk.Configurable):	    
	__gtype_name = 'RBGenreToolsSettings'
	object = GObject.property(type=GObject.GObject)

	def __init__(self):
		GObject.Object.__init__(self)
		self.settings = Gio.Settings("org.gnome.rhythmbox.plugins.RBGenreTools")
		
	def set_quicklink(self,genre_str):
		print(genre_str)
		
