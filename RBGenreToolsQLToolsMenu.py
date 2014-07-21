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

import random
import rb

class RBGenreToolsQLToolsMenu(Gtk.HBox):
	def __init__(self,_SG):
		Gtk.HBox.__init__(self)	
		
		self._SG = _SG
		self.settings = _SG.settings
		self.grp_btn = Gtk.Button('+')
		self.grp_btn.set_tooltip_text('Create quicklink genre group')
		self.del_btn = Gtk.Button('Delete')
		self.del_btn.set_tooltip_text('Delete selected quicklink')
		
		self.ql_entry = Gtk.Entry()
		self.ql_entry.set_tooltip_text('Add a name for the new quicklink group')
		
		self.add(self.ql_entry)
		self.add(self.grp_btn)
		self.add(self.del_btn)
		if self.settings['show-quicklinks']:
			self.show_all()
		
		self.set_clicked(self.grp_btn,self.create_group)
		self.set_clicked(self.del_btn,self._SG.ql_win.remove)
	
	def set_clicked(self,btn,cb,img=None):
		btn.set_halign(Gtk.Align.START)
		btn.connect("clicked", cb)
		
	
	def create_group(self,a):
		name = self.ql_entry.get_text()
		if len(name)<1:
			return
		self._SG.ql_win.new(name)
		self.ql_entry.set_text("")
		
		
		
