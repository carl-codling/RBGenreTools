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

from gi.repository import Gtk
import rb
import json

class RBGenreToolsQuicklinks(Gtk.ScrolledWindow):
	def __init__(self, _SG):
		Gtk.ScrolledWindow.__init__(self)
		self.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC);
		self._SG = _SG	
		self.settings = _SG.settings
		
		self.current_quicklink = None
		self.current_quicklink_iter = None
		
		self.store = Gtk.TreeStore(str,bool)
		self.tree = Gtk.TreeView(self.store)
		self.column = Gtk.TreeViewColumn("Quick Links")
		
		title = Gtk.CellRendererText()
		
		self.column.pack_start(title, True)
		self.column.add_attribute(title, "text", 0)
		self.column.set_sort_column_id(0)
		
		self.tree.append_column(self.column)
		self.treeselection = self.tree.get_selection()
		self.treeselection.connect("changed", self.selection_changed)
		self.add(self.tree)
		if self.settings['show-quicklinks']:
			self.show_all()
		
	def selection_changed(self,selection):
		model, treeiter = selection.get_selected()
		self._SG.tree_win.filter = []
		if treeiter != None:
			string = model[treeiter][0]
			self.current_quicklink = string
			self.current_quicklink_iter = treeiter
			for genre in self.quicklinks['groups'][string]:
				self._SG.tree_win.filter.append(genre)
			#self.update_selection()
			self._SG.tree_win.set_selection()
	
	def new(self,title):
		_SG = self._SG
		f = rb.find_plugin_file(_SG, "quicklinks.json")
		fo = open(f, "w")
		ql = self.quicklinks['groups']
		selection = self._SG.tree.get_selection()
		genres = []
		model, rows = selection.get_selected_rows()
		
		for g in rows:
			#print(model,g)
			genres.append(model[g][:][0])
		
		
		ql[title]=genres
		fo.write(json.dumps(self.quicklinks))
		fo.close()
		self.store.append(None,[title,True])
		
	def set_quicklinks_from_json(self):
		_SG = self._SG
		f = rb.find_plugin_file(_SG, "quicklinks.json")
		json_data=open(f)
		self.quicklinks = json.load(json_data)
		for t in self.quicklinks['groups']:
			self.store.append(None,[t,True])
		json_data.close()
		
	def remove(self,a):
		selection = self.tree.get_selection()
		model, row = selection.get_selected()
		
		del self.quicklinks['groups'][model[row][0]]
		model.remove(row)
		_SG = self._SG
		f = rb.find_plugin_file(_SG, "quicklinks.json")
		fo = open(f, "w")
		fo.write(json.dumps(self.quicklinks))
		fo.close()
		
	
	def update_selection(self):
		if self.is_quicklink_selection():
			self.set_selection()
		else:
			self.clear_selection()
		
	def is_quicklink_selection(self):
		_SG = self._SG
		if not self.current_quicklink:
			return False
		selection = self._SG.tree.get_selection()
		genres = []
		model, rows = selection.get_selected_rows()
		for g in rows:
			genres.append(model[g][:][0])
		
		if genres == self.quicklinks['groups'][self.current_quicklink]:
			return True
		return False
		
	def clear_selection(self):
		self.treeselection.unselect_all()
	
	def set_selection(self):
		if not self.treeselection.iter_is_selected(self.current_quicklink_iter):
			self.treeselection.select_iter(self.current_quicklink_iter)	
