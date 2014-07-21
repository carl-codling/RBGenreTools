# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from gi.repository import GObject,Gtk, Peas
from gi.repository import RB
from gi.repository import Gio

import rb
import json

from RBGenreToolsQueueToolsMenu import RBGenreToolsQueueToolsMenu
from RBGenreToolsQLToolsMenu import RBGenreToolsQLToolsMenu
from RBGenreToolsTree import RBGenreToolsTree
from RBGenreToolsQuicklinks import RBGenreToolsQuicklinks
from ConfigDialog import ConfigDialog
#from RBGenreToolsFilter import RBGenreToolsFilter

class RBGenreTools (GObject.Object, Peas.Activatable):	    
	__gtype_name = 'RBGenreToolsPlugin'
	object = GObject.property(type=GObject.GObject)

	def __init__(self):
		GObject.Object.__init__(self)
		
		self.settings = Gio.Settings("org.gnome.rhythmbox.plugins.RBGenreTools")
		
		shell = self.object
		self.filter = None
		self.genres = []
		self.set_widget_positions()
		self.tree_win = RBGenreToolsTree(self)
		self.store = self.tree_win.store
		self.tree = self.tree_win.tree
		
		self.ql_win = RBGenreToolsQuicklinks(self)
		self.qlstore = self.ql_win.store
		self.qltree = self.ql_win.tree

	def do_activate(self):
		self.init_queuetools()
		self.init_tree_win()
		self.ql_win.set_quicklinks_from_json()
		self.init_quicklinks()
		self.init_ql_menubar()
		#self.init_filter()
		self.set_property_actions()
				
	def do_deactivate(self):
		shell = self.object
		shell.remove_widget (self.tree_win, self.treepos)
		shell.remove_widget (self.tools_menu, self.treepos)
		#shell.remove_widget (self.filter, self.treepos)
		shell.remove_widget (self.ql_win, self.qlpos)
		shell.remove_widget (self.ql_tools_menu, self.qlpos)
	
	# set vars for the position of the genre tree and quicklinks according to user pref
	def set_widget_positions(self):
		self.treepos = RB.ShellUILocation.RIGHT_SIDEBAR
		if self.settings['tree-position-left']:
			self.treepos = RB.ShellUILocation.SIDEBAR
		self.qlpos = RB.ShellUILocation.SIDEBAR
		if self.settings['ql-right']:
			self.qlpos = RB.ShellUILocation.RIGHT_SIDEBAR
			
	# create the queue tools combobox etc. and add to shell		
	def init_queuetools(self):
		shell = self.object
		self.tools_menu = RBGenreToolsQueueToolsMenu(self)
		shell.add_widget (self.tools_menu, self.treepos , expand=False, fill=False)
	
	# create the quick links menu and add to shell
	def init_ql_menubar(self):
		shell = self.object
		self.ql_tools_menu = RBGenreToolsQLToolsMenu(self)
		shell.add_widget (self.ql_tools_menu, self.qlpos , expand=False, fill=False)
	
	# (DISABLED) add the tool to filter the genre tree	
	def init_filter(self):
		shell = self.object
		self.filter = RBGenreToolsFilter(self)
		shell.add_widget (self.filter, self.treepos , expand=False, fill=False)
	
	# create the genre tree and add to shell
	def init_tree_win(self):
		shell = self.object
		if not self.tree_win.genres:	
			self.tree_win.set_genre_list()
			self.tree_win.add_genres_to_store(self.tree_win.genres)
		shell.add_widget (self.tree_win, self.treepos , expand=True, fill=True)
	
	# create the quicklink list and add to shell
	def init_quicklinks(self):
		shell = self.object
		shell.add_widget (self.ql_win, self.qlpos , expand=True, fill=True)
		
	# connect actions on the native genre view
	def set_property_actions(self):	
		shell = self.object
		src = shell.props.library_source
		propviews = src.get_property_views()
		propmodel = propviews[0].get_model() # propviews[0] is the genre property view
		propmodel.connect("row-inserted", self.row_inserted)
		propmodel.connect("row-deleted", self.row_removed)
		propviews[0].connect("properties-selected", self.genre_selection_changed)
	
	# runs when item inserted to native genre store / updates SG genre tree
	def row_inserted(self,store,b,treeiter):
		genre = str(store[treeiter][0])
		self.tree_win.add_genres_to_store([genre])
		
	# runs when item removed from native genre store / updates SG genre tree
	def row_removed(self,a,b,treeiter = None):
		g = a[b][0] # genre str of removed row
		store = self.store
		# If we're not searching a child set then start from beggining of top level
		if not treeiter:
			treeiter = store.get_iter_first()
		while treeiter != None:
			# get the genre string of current iter
			current_iter_genre = str(store[treeiter][:][0])
			# compare the string to the removed item
			if current_iter_genre == g:
				# Only remove match if it has no children
				if not store.iter_has_child(treeiter):
					store.remove(treeiter)
				return True
			# iterate over children
			if store.iter_has_child(treeiter):
				childiter = store.iter_children(treeiter)
				child = self.row_removed(a,b,childiter)
				if child:
					return childiter
			treeiter = store.iter_next(treeiter)
		return None
	
	# runs when the selection in the native genre view changes
	def genre_selection_changed(self,a,b):
		store = self.store
		selection = self.tree.get_selection()
		shell = self.object
		src = shell.props.library_source
		pv = src.get_property_views()
		selection = pv[0].get_selection()
		genres = []
		for genre in selection:
			genres.append(genre)
		self.set_selection(genres)		
	
	# updates SG genre tree when native selection changes (initiated by self.genre_selection_changed)		
	def set_selection(self, genres, treeiter=None):
		store = self.store
		# get the selection from the native genre view
		selection = self.tree.get_selection()
		# If we're not searching a child set then start from beggining of top level
		if not treeiter:
			treeiter = store.get_iter_first()
		while treeiter != None:
			# get the genre string of current iter
			current_iter_genre = str(store[treeiter][:][0])
			if current_iter_genre in genres:
				p = self.store.iter_parent(treeiter)
				if p:
					self.tree.expand_row(self.store.get_path(p), True);
				selection.select_iter(treeiter)
			else:
				selection.unselect_iter(treeiter)
			if store.iter_has_child(treeiter):
				childiter = store.iter_children(treeiter)
				self.set_selection(genres,childiter)
			treeiter = store.iter_next(treeiter)
		# update the quicklink window	
		self.ql_win.update_selection()
			
			
		
		
