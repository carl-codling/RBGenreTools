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

from gi.repository import Gio
from gi.repository import GObject
from gi.repository import PeasGtk
from gi.repository import Gtk
from gi.repository import RB

import gettext
gettext.install('rhythmbox', RB.locale_dir())

class ConfigDialog(GObject.Object, PeasGtk.Configurable):
	__gtype_name__ = 'RBGenreToolsPluginConfigDialog'
	object = GObject.property(type=GObject.Object)

	def __init__(self):
		GObject.Object.__init__(self)
		self.settings = Gio.Settings("org.gnome.rhythmbox.plugins.RBGenreTools")


	def do_create_configure_widget(self):
		
		####### Display tab
		
		page1 = Gtk.VBox()
		
		descr = Gtk.Label("<i>" + _("You have to disable and re-enable this plugin or restart Rhythmbox "
                                    "to apply changes here") + "</i>")
		descr.set_alignment(0, 0)
		descr.set_margin_left(15)
		descr.set_line_wrap(True)
		descr.set_use_markup(True)
		notice = Gtk.HBox()
		notice.pack_start(descr, False, False, 10)
		page1.pack_start(notice, False, False, 10)
		
		# - Show genre tree toggle
		hbox = Gtk.HBox()
		switch = Gtk.Switch()
		switch.set_active(self.settings["show-tree"])
		switch.connect("notify::active", self.switch_toggled, "show-tree")
		label = Gtk.Label("<b>" + _("Show genre tree window") + "</b>")
		label.set_use_markup(True)
		hbox.pack_start(switch, False, False, 5)
		hbox.pack_start(label, False, False, 5)
		page1.pack_start(hbox, False, False, 10)
		
		
		
		# - Show tools toggle
		hbox = Gtk.HBox()
		switch = Gtk.Switch()
		switch.set_active(self.settings["show-tools"])
		switch.connect("notify::active", self.switch_toggled, "show-tools")
		label = Gtk.Label("<b>" + _("Show queue adder") + "</b>")
		label.set_use_markup(True)
		hbox.pack_start(switch, False, False, 5)
		hbox.pack_start(label, False, False, 5)
		page1.pack_start(hbox, False, False, 10)
		
		# Show quick links toggle
		
		self.ql_switch = Gtk.Switch()
		hbox = Gtk.HBox()
		switch = Gtk.Switch()
		switch.set_active(self.settings["show-quicklinks"])
		switch.connect("notify::active", self.switch_toggled, "show-quicklinks")

		label = Gtk.Label("<b>" + _("Show quick link window") + "</b>")
		label.set_use_markup(True)
		hbox.pack_start(switch, False, False, 5)
		hbox.pack_start(label, False, False, 5)
		vbox = Gtk.VBox()
		vbox.pack_start(hbox, False, False, 0)
		page1.pack_start(vbox, False, False, 10)
		
		# Show filter toggle
		
		self.ql_switch = Gtk.Switch()
		hbox = Gtk.HBox()
		switch = Gtk.Switch()
		switch.set_active(self.settings["show-filter"])
		switch.connect("notify::active", self.switch_toggled, "show-filter")

		label = Gtk.Label("<b>" + _("Show filter select") + "</b>")
		label.set_use_markup(True)
		hbox.pack_start(switch, False, False, 5)
		hbox.pack_start(label, False, False, 5)
		vbox = Gtk.VBox()
		vbox.pack_start(hbox, False, False, 0)
		page1.pack_start(vbox, False, False, 10)
		
		
		
		##### Positions tab
		
		page2 = Gtk.VBox()
		descr = Gtk.Label("<i>" + _("You have to disable and re-enable this plugin or restart Rhythmbox "
                                    "to apply changes here") + "</i>")
		descr.set_alignment(0, 0)
		descr.set_margin_left(15)
		descr.set_line_wrap(True)
		descr.set_use_markup(True)
		notice = Gtk.HBox()
		notice.pack_start(descr, False, False, 10)
		page2.pack_start(notice, False, False, 10)
		
		# - Genre tree position
		hbox = Gtk.HBox()
		switch = Gtk.Switch()
		switch.set_active(self.settings["tree-position-left"])
		switch.connect("notify::active", self.switch_toggled, "tree-position-left")
		
		label = Gtk.Label("<b>" + _("Display genre tree on the left") + "</b>")
		label.set_use_markup(True)
		hbox.pack_start(switch, False, False, 5)
		hbox.pack_start(label, False, False, 5)
		hbox.pack_start(descr, False, False, 0)
		page2.pack_start(hbox, False, False, 10)
		
		# - Quick links position
		hbox = Gtk.HBox()
		switch = Gtk.Switch()
		switch.set_active(self.settings["ql-right"])
		switch.connect("notify::active", self.switch_toggled, "ql-right")
		label = Gtk.Label("<b>" + _("Display quick links on the right") + "</b>")
		label.set_use_markup(True)
		hbox.pack_start(switch, False, False, 5)
		hbox.pack_start(label, False, False, 5)
		page2.pack_start(hbox, False, False, 10)
		
		
		##### Filters tab
		
		page3 = Gtk.VBox()
		descr = Gtk.Label("<i>" + _("You have to disable and re-enable this plugin or restart Rhythmbox "
                                    "to apply changes here") + "</i>")
		descr.set_alignment(0, 0)
		descr.set_margin_left(15)
		descr.set_line_wrap(True)
		descr.set_use_markup(True)
		notice = Gtk.HBox()
		notice.pack_start(descr, False, False, 10)
		page3.pack_start(notice, False, False, 10)
		
		# - Enable/disable genre parsing
		hbox = Gtk.HBox()
		switch = Gtk.Switch()
		switch.set_active(self.settings["parse-genres"])
		switch.connect("notify::active", self.switch_toggled, "parse-genres")
		label = Gtk.Label("<b>" + _("Filter genres according to the delimiter set below") + "</b>")
		label.set_use_markup(True)
		hbox.pack_start(switch, False, False, 5)
		hbox.pack_start(label, False, False, 5)
		page3.pack_start(hbox, False, False, 10)
		
		# - Delimiter entry
		hbox = Gtk.HBox()
		
		self.delim_select = Gtk.Entry()
		self.delim_select.set_text(self.settings["delimiter"])
		self.delim_select.connect("activate", self.delimiter_changed)
		label = Gtk.Label("<b>" + _("Genre delimiter") + "</b>")
		label.set_use_markup(True)
		
		self.delim_edit = Gtk.Button()
		self.delim_edit.set_label("Change")
		self.delim_edit.connect("clicked", self.delimiter_changed)
		hbox.pack_start(label, False, False, 5)
		hbox.pack_start(self.delim_select, False, False, 5)
		hbox.pack_start(self.delim_edit, False, False, 5)
		page3.pack_start(hbox, False, False, 10)
		
		nb = Gtk.Notebook()
		nb.append_page(page1, Gtk.Label(_("What to show")))
		nb.append_page(page2, Gtk.Label(_("Where to show it")))
		nb.append_page(page3, Gtk.Label(_("Filtering")))
		
		nb.show_all()
		nb.set_size_request(300, -1)
		
		
		return nb
	
	
	def switch_toggled(self, switch, active, key):
		self.settings[key] = switch.get_active()
        
	def delimiter_changed(self,a):
		if self.delim_select.is_visible():
			self.settings["delimiter"] = self.delim_select.get_text()
			self.delim_select.hide()
			
		else:
			self.delim_select.show()

