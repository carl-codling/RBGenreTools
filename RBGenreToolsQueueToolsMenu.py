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
import math

class RBGenreToolsQueueToolsMenu(Gtk.HBox):
	def __init__(self,_SG):
		Gtk.HBox.__init__(self)	
		
		self._SG = _SG
		
		self.settings = _SG.settings
		self.btn = Gtk.Button()
		self.btn.set_label("<<")
		self.btn.connect("clicked", self.init_queue)
		self.add(self.btn)
		
		self.combobox = Gtk.ComboBoxText.new()
		self.combobox.set_tooltip_text("Add a random selection from the currently selected genres to the queue")
		self.combobox.append(None,'Queue random selection:')
		self.combobox.append(None,'All')
		self.combobox.append(None,'1 song')
		self.combobox.append(None,'5 songs')
		self.combobox.append(None,'10 songs')
		self.combobox.append(None,'25 songs')
		self.combobox.append(None,'50 songs')
		self.combobox.append(None,'15 minutes')
		self.combobox.append(None,'30 minutes')
		self.combobox.append(None,'1 hour')
		self.combobox.append(None,'90 minutes')
		self.combobox.append(None,'2 hours')
		self.combobox.set_active(0)
		self.combobox.connect("changed", self.init_queue)
		self.add(self.combobox)
		
		
		self.combobox.show()
		if self.settings['show-tools']:
			self.show()
		
		
	
	def init_queue(self,a):
		qtype = self.combobox.get_active()
		if qtype == 0:
			self.btn.hide()
			return
		else:
			self.btn.show()
		if qtype == 1:
			self.queue_selected()
		elif qtype == 2:
			self.queue_rand(1)
		elif qtype == 3:
			self.queue_rand(5)
		elif qtype == 4:
			self.queue_rand(10)
		elif qtype == 5:
			self.queue_rand(25)
		elif qtype == 6:
			self.queue_rand(50)
		elif qtype == 7:
			self.queue_by_playtime(0.25)
		elif qtype == 8:
			self.queue_by_playtime(0.5)
		elif qtype == 9:
			self.queue_by_playtime(1)
		elif qtype == 10:
			self.queue_by_playtime(1.5)
		elif qtype == 11:
			self.queue_by_playtime(2)
		#self.combobox.set_active(0)	
	
		
	def queue_selected(self):
		shell = self._SG.object
		src = shell.props.library_source
		qsrc = shell.props.queue_source
		for treerow in src.props.query_model:
			entry, path = list(treerow)
			qsrc.add_entry(entry, -1)
			
	def queue_rand(self,n=10):
		shell = self._SG.object
		src = shell.props.library_source
		qsrc = shell.props.queue_source
		list_holder = {}
		for treerow in src.props.query_model:
			entry, path = list(treerow)
			if qsrc.get_entry_view().get_entry_contained(entry):
				print('already in list')
			else:
				genre = entry.get_string(RB.RhythmDBPropType.GENRE)
				if genre not in list_holder:
					list_holder[genre] = [] 
				list_holder[genre].append(entry)
		outp_list = []
		gcount = len(list_holder)
		for g in list_holder:
			list_holder[g] = random.sample(list_holder[g], len(list_holder[g]))
			ecount = math.ceil(n/gcount)
			for e in list_holder[g]:
				
				outp_list.append(e)
				ecount -= 1
				if ecount == 0:
					break
		outp_list = random.sample(outp_list, len(outp_list))
		
		i = 0
		for e in outp_list:
			qsrc.add_entry(e, -1)
			i+=1
			if i == n:
				break
			
	def queue_by_playtime(self, hours=1):
		shell = self._SG.object
		src = shell.props.library_source
		qsrc = shell.props.queue_source
		seconds = hours*60*60
		list_holder = {}
		for treerow in src.props.query_model:
			entry, path = list(treerow)
			if entry in qsrc:
				break
			duration = entry.get_ulong(RB.RhythmDBPropType.DURATION)
			genre = entry.get_string(RB.RhythmDBPropType.GENRE)
			if genre not in list_holder:
				list_holder[genre] = [] 
			if duration < seconds/2:
				list_holder[genre].append([entry,duration])
		outp_list = []
		
		gcount = len(list_holder)
		for g in list_holder:
			list_holder[g] = random.sample(list_holder[g], len(list_holder[g]))
			ecount = math.ceil(seconds/gcount)
			for e in list_holder[g]:
				
				outp_list.append(e)
				ecount -= e[1]
				if ecount < 1:
					break
		outp_list = random.sample(outp_list, len(outp_list))
		
		i = 0
		for e in outp_list:
			qsrc.add_entry(e[0], -1)
			i+=e[1]
			if i > seconds:
				break
