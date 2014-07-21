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

from gi.repository import Gtk,Gdk
from gi.repository import RB

UI_INFO = """
<ui>
  <popup name='PopupMenu'>
    <menuitem action='add-to-filter' />
  </popup>
</ui>
"""

class RBGenreToolsTree(Gtk.ScrolledWindow):
	def __init__(self, _SG):
		Gtk.ScrolledWindow.__init__(self)
		
		
		self._SG = _SG	
		self.settings = _SG.settings
		self.uimanager = self.create_ui_manager()
		action_group = Gtk.ActionGroup("my_actions")
		self.add_actions(action_group)
		self.uimanager.insert_action_group(action_group)
		self.popup = self.uimanager.get_widget("/PopupMenu")
		
		self.current_editable = None
		
		self.genres = []
		self.store = Gtk.TreeStore(str, int, str)
		self.tree = Gtk.TreeView(self.store)
		self.tree.enable_model_drag_dest([('text/uri-list',0,0)],Gdk.DragAction.LINK)        
		self.tree.drag_dest_add_text_targets()
		self.tree.drag_dest_add_image_targets()
		self.tree.connect('drag-drop', self.on_drag_drop)
		self.tree.connect('drag-data-received', self.on_drag_data_received)
		self.column = Gtk.TreeViewColumn("Genre")
		title = Gtk.CellRendererText()
		self.column.pack_start(title, True)
		self.column.add_attribute(title, "text", 2)
		self.column.set_sort_column_id(0)
		self.treeselection = self.tree.get_selection()
		Gtk.TreeSelection.set_mode(self.treeselection,Gtk.SelectionMode.MULTIPLE)
		self.tree.append_column(self.column)
		self.tree.connect('button-press-event' , self.button_press_event)
		self.treeselection.connect("changed", self.selection_changed)
		self.add(self.tree)
		if self.settings['show-tree']:
			self.show_all()
		
	
	def button_press_event(self, treeview, event):
		if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3: # right click
			path = self.tree.get_path_at_pos(event.x, event.y)
			treeiter = self.store.get_iter(path[0])
			self.current_editable = self.store[treeiter][0]
			self.popup.popup(None, None, None, None, event.button, event.time)
			return True
	
	def create_ui_manager(self):
		uimanager = Gtk.UIManager()

		uimanager.add_ui_from_string(UI_INFO)

		return uimanager		
	
	def add_actions(self, action_group):
		
		action_group.add_actions([
			("add-to-filter", None, "Add to filter",None,None,self.add_to_filter)
		])
		
	def add_to_filter(self,a):
		if self._SG.filter and self.current_editable:
			self._SG.filter.append(self.current_editable)
	
	# runs when the selected genres in the tree change
	def selection_changed(self,selection):
		shell = self._SG.object
		store=self.store
		model, selected_rows = selection.get_selected_rows()
		# create list to store the genres in the selection
		self.filter = []
		for treepath in selected_rows:
			if treepath != None:
				self.tree.expand_row(treepath, True);
				self.filter.append(model[treepath][0])
		self.set_selection()
		self.close_inactive_parents()
	
	# collapse any parent rows in the tree that don't have selected children	
	def close_inactive_parents(self, treeiter=None):
		store = self.store
		if not treeiter:
			treeiter = store.get_iter_first()
		while treeiter != None:
			
			if store.iter_has_child(treeiter):
				childiter = store.iter_children(treeiter)
				if not self.has_selected_children(childiter):
					self.tree.collapse_row(store.get_path(treeiter))
			treeiter = store.iter_next(treeiter)
	
	# returns true if treeiter has selected children
	def has_selected_children(self,treeiter):
		model, selection = self.treeselection.get_selected_rows()
		
		while treeiter != None:
			if self.store.get_path(treeiter) in selection:
				return True
			if self.store.iter_has_child(treeiter):
				childiter = self.store.iter_children(treeiter)
				if self.has_selected_children(childiter):
					return True
			treeiter = self.store.iter_next(treeiter)
		return False	
		
	def set_selection(self):
		shell = self._SG.object
		src = shell.props.library_source
		gholder = []
		pv = src.get_property_views()
		pm = pv[0].get_model()
		
		for f in self.filter:
			for m in pm:
				if m[0] == f:
					gholder.append(m[0])
		pv[0].set_selection(gholder)
		
		
		
	def set_genre_list(self):
		shell = self._SG.object
		src = shell.props.library_source
		pv = src.get_property_views()
		pm = pv[0].get_model()
		for m in pm:
			self.genres.append(m[0])
			
			
	def process_subgenres(self, genre_list):
		gparent = None
		gstring = genre_list[0]
		first_loop = True
		for t in genre_list:
			if not first_loop:
				gstring = gstring+self.settings['delimiter']+t
			existing_genre = self.genre_exists(gstring, gparent)
			if existing_genre:
				gparent = existing_genre
			else:
				gparent = self.add_genre_to_store(gparent,gstring)
			first_loop = None
			
				
	def genre_exists(self, genre, treeiter):
		store = self.store
		if not treeiter:
			treeiter = store.get_iter_first()
		while treeiter != None:
			current_iter_genre = str(store[treeiter][:][0])
			if current_iter_genre == genre:
				return treeiter
			if store.iter_has_child(treeiter):
				childiter = store.iter_children(treeiter)
				childgenre = self.genre_exists(genre,childiter)
				if childgenre:
					return childgenre
			treeiter = store.iter_next(treeiter)
		return None
					
		
	def add_genres_to_store(self,genres):
		store = self.store
		for genre in genres:
			split_gstring = genre.split(self.settings['delimiter'])
			if len(split_gstring)>1:
				self.process_subgenres(split_gstring)
			elif not self.genre_exists(genre,None):
				self.add_genre_to_store(None,genre)
		
	def add_genre_to_store(self, treeiter, genre):
		store = self.store
		gtree = genre.split(self.settings['delimiter'])
		
		if not treeiter:
			parent = None
			treeiter = store.get_iter_first()
		else:
			parent = treeiter
			treeiter = store.iter_children(treeiter)
		while treeiter != None:
			current_iter_genre = str(store[treeiter][:][0])
			if min(current_iter_genre, genre) == genre:
				return store.insert_before(parent,treeiter,[genre, 0, gtree[len(gtree)-1]])
			treeiter = store.iter_next(treeiter)	
		return store.append(parent,[genre, 0, gtree[len(gtree)-1]])
		
	
        	
	def on_drag_drop(self, widget, context, x, y, time):
		path, pos = self.tree.get_dest_row_at_pos(x,y)
		treeiter = self.store.get_iter(path)
		genre = str(self.store[treeiter][0])
		
		
		
	def on_drag_data_received(self, widget, drag_context, x, y, data, info,time):
		
		
		shell = self._SG.object
		db=shell.props.db
		widget.stop_emission_by_name('drag-data-received')

		path, pos = widget.get_dest_row_at_pos(x,y)
		treeiter = self.store.get_iter(path)
		genre = str(self.store[treeiter][0])
		uris = data.get_uris()
		for uri in uris:
			e = shell.props.db.entry_lookup_by_location(uri)
			db.entry_set(e,3,genre)
		db.commit ()
		
		
		drag_context.finish(True, False, time)
