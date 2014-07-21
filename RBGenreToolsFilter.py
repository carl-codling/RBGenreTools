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



from gi.repository import GObject,Gtk
from gi.repository import RB

import rb
import json

class RBGenreToolsFilter(Gtk.HBox):
	def __init__(self,_SG):
		Gtk.HBox.__init__(self)	
		
		self._SG = _SG
		
		self.settings = _SG.settings
		
		self.list = self.get_list_from_json();
		print(self.list)
		self.combobox = Gtk.ComboBoxText.new()
		self.combobox.set_tooltip_text("Add genres to filter list by right clicking on them in the genre tree")
		self.combobox.append(None,'Show all:')
		self.combobox.append(None,'Show filtered')
		self.combobox.append(None,'Show unfiltered')
		self.combobox.set_active(self.settings['filter'])
		self.combobox.connect("changed", self.toggle_filter)
		self.add(self.combobox)
		
		
		self.combobox.show()
		if self.settings['show-filter']:
			self.show()
		
	def toggle_filter(self,a):
		self.settings['filter'] = self.combobox.get_active()
	
	def append(self,genre):
		_SG = self._SG
		self.list.append(genre)
		f = rb.find_plugin_file(_SG, "filtered.json")
		fo = open(f, "w")
		fo.write(json.dumps(self.list))
		fo.close()
	
	def get_list_from_json(self):
		_SG = self._SG
		f = rb.find_plugin_file(_SG, "filtered.json")
		json_data=open(f)
		filtered = json.load(json_data)
		json_data.close()
		return filtered
