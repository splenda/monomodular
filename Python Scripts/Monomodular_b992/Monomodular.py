# http://aumhaa.blogspot.com

import Live
import time
import math

""" All of the Framework files are listed below, but we are only using using some of them in this script (the rest are commented out) """
from _Framework.ButtonElement import ButtonElement # Class representing a button a the controller
from _Framework.ButtonMatrixElement import ButtonMatrixElement # Class representing a 2-dimensional set of buttons
#from _Framework.ButtonSliderElement import ButtonSliderElement # Class representing a set of buttons used as a slider
from _Framework.ChannelStripComponent import ChannelStripComponent # Class attaching to the mixer of a given track
#from _Framework.ChannelTranslationSelector import ChannelTranslationSelector # Class switches modes by translating the given controls' message channel
#from _Framework.ClipSlotComponent import ClipSlotComponent # Class representing a ClipSlot within Live
from _Framework.CompoundComponent import CompoundComponent # Base class for classes encompasing other components to form complex components
from _Framework.ControlElement import ControlElement # Base class for all classes representing control elements on a controller 
from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent # Base class for all classes encapsulating functions in Live
from _Framework.DeviceComponent import DeviceComponent # Class representing a device in Live
#from _Framework.DisplayDataSource import DisplayDataSource # Data object that is fed with a specific string and notifies its observers
from _Framework.EncoderElement import EncoderElement # Class representing a continuous control on the controller
from _Framework.InputControlElement import * # Base class for all classes representing control elements on a controller
#from _Framework.LogicalDisplaySegment import LogicalDisplaySegment # Class representing a specific segment of a display on the controller
#from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
from _Framework.ModeSelectorComponent import ModeSelectorComponent # Class for switching between modes, handle several functions with few controls
from _Framework.NotifyingControlElement import NotifyingControlElement # Class representing control elements that can send values
#from _Framework.PhysicalDisplayElement import PhysicalDisplayElement # Class representing a display on the controller
#from _Framework.SceneComponent import SceneComponent # Class representing a scene in Live
#from _Framework.SessionComponent import SessionComponent # Class encompassing several scene to cover a defined section of Live's session
#from _Framework.SessionZoomingComponent import SessionZoomingComponent # Class using a matrix of buttons to choose blocks of clips in the session
#from _Framework.SliderElement import SliderElement # Class representing a slider on the controller
#from _Framework.TrackEQComponent import TrackEQComponent # Class representing a track's EQ, it attaches to the last EQ device in the track
#from _Framework.TrackFilterComponent import TrackFilterComponent # Class representing a track's filter, attaches to the last filter in the track
from _Framework.TransportComponent import TransportComponent # Class encapsulating all functions in Live's transport section

"""Custom files, overrides, and files from other scripts"""
from SwitchboardElement import SwitchboardElement
from MonoClient import MonoClient


from _Generic.Devices import *

""" Here we define some global variables """
class Monomodular(ControlSurface):
	__module__ = __name__
	__doc__ = " MonoCode controller script "


	def __init__(self, c_instance):
		"""everything except the '_on_selected_track_changed' override and 'disconnect' runs from here"""
		ControlSurface.__init__(self, c_instance)
		self.set_suppress_rebuild_requests(True) # Turn off rebuild MIDI map until after we're done setting up
		self._version_check = 'b992'
		self.log_message("--------------= Monomodular " + str(self._version_check) + " log opened =--------------") 
		self.show_message('Monomodular Loaded')
		self._hosts = []
		self._client = [None for index in range(16)]
		self._setup_monomod()
		self._setup_switchboard()
		self.set_suppress_rebuild_requests(False) #Turn rebuild back on, now that we're done setting up

	

	"""script initialization methods"""
	def _setup_monomod(self):
		for index in range(16):
			self._client[index] = MonoClient(self, index)
			self._client[index].name = 'Client_' + str(index)
		self._active_client = self._client[0]
		self._active_client._is_active = True
	

	def _setup_switchboard(self):
		self._switchboard = SwitchboardElement(self, self._client)
		self._switchboard.name = 'Switchboard'
	


#	def update_display(self):
#		ControlSurface.update_display(self)
#		self._switchboard._ping()
	

	"""general functionality"""
	def disconnect(self):
		"""clean things up on disconnect"""
		self.log_message("--------------= Monomodular " + str(self._version_check) + " log closed =--------------") #Create entry in log file
		#self._switchboard.disconnect()
		#for client in self._client:
		#	client.disconnect()
		self._hosts = []
		ControlSurface.disconnect(self)
		return None

	def connect_script_instances(self, instanciated_scripts):
		hosts = []
		for s in instanciated_scripts:
			#if (s is self):
			#	found_self = True
			if '_monomod_version' in dir(s):
				if s._monomod_version == self._version_check:
					self.log_message('found monomod version ' + str(s._monomod_version) + ' in script ' + str(s._host_name))
					for host in s.hosts:
						hosts.append(host)
						host.connect_to_clients(self)
				else:
					self.log_message('version mismatch: Monomod version ' + str(self._version_check) + ' vs. Host version ' + str(s._monomod_version))
		self._hosts = hosts
		#self.log_message('hosts: ' + str(self._hosts))
				
		


#