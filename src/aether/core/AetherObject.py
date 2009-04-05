import os,sys
import aether
from aether.error import AetherIOError

class AetherObject(object):
	"""Base class for all Aether related classes.

	AetherObject provides some common methods and data to objects in the Aether system."""

	#Global Aether settings
	settings=None

	#Additional default system directories to search
	system_dirs=['data','module','chain','transform']

	def __init__(self): pass

	#Modified getattr:
	#This is the counterpart to the modified setattr method.
	#This method reads items from certain settings sections in addition to object attributes.
	#Item search order:
	#1) The object's attributes
	#2) The settings.(self.name) section
	#3) The settings.aether section
	#
	#The idea here is to search attributes in order from 'most local' to 'most global'
	def __getattr__(self,item):
		#Search the objects attributes
		try:
			res=object.__getattribute__(self,item)
		except AttributeError as e:
			try:
				#Search the settings section self.name
				res=self.settings_get(self.__dict__['name'],item)
			except (KeyError,AttributeError) as e:
				res=self.settings_get('aether',item)
		return res

	#Modified setattr:
	#This is the counterpart to the modified getattr method.
	#This method sets items in certain settings sections in addition to object attributes.
	#Items in settings sections can only be set if they already exist, no new settings names can be created.
	#Item setting order:
	#1) The settings.(self.name) section (if value already exists)
	#2) The settings.aether section (if value already exists)
	#3) The object's attributes
	def __setattr__(self,item,value):
		#Search for the self.name section
		try:
			self.settings_set(self.__dict__['name'],item,value,raise_not_exists=True)
		except (KeyError,AttributeError) as e:
			try:
				self.settings_set('aether',item,value,raise_not_exists=True)
			except AttributeError as e:
				object.__setattr__(self,item,value)

	#Helper method for reading a settings value
	#section_name: The name of the section to read from
	#value_name: The name of the settings value to read
	#
	#This method raises an AttributeError if the given value_name does not exist in the given section
	def settings_get(self,section_name,value_name):
		return getattr(getattr(self.settings,section_name),value_name)

	#Helper method for setting a dictionary of settings name/value pairs
	#section_name: Name of the settings section
	#settings_dict: Dictionary of settings name/value pairs
	#test_exists: If True, the value will only be set if the settings value does not already exist
	#raise_not_exists: If True and the settings value already exists, an AttributeError will be raised
	def settings_load(self,section_name,settings_dict,test_exists=False,raise_not_exists=False):
		for value_name,value in settings_dict.items():
			#Set the settings value in the given settings section
			self.settings_set(section_name,value_name,value,test_exists,raise_not_exists)

	#Helper method for setting settings values
	#section_name: Name of the settings section
	#value_name: Name of the value to set
	#value: Value to set
	#test_exists: If True, the value will only be set if the settings value does not already exist
	#raise_not_exists: If True and the settings value does not exist, an AttributeError will be raised
	def settings_set(self,section_name,value_name,value,test_exists=False,raise_not_exists=False):
		#Get the specified settings section
		settings_section=getattr(self.settings,section_name)

		#Determine if the settings value exists
		exists=hasattr(settings_section,value_name)

		#Raise an AttributeError if the settings value exists and we are supposed to raise exceptions
		if not exists and raise_not_exists:
			raise AttributeError('Attempted to set a settings value that already exists: %s.%s'%(section_name,value))

		#Set the value if we are not testing for existence or if the value does not exist
		if not test_exists or not exists:
			setattr(settings_section,value_name,value)

	#Helper method for debug printing
	#Will print only if self.settings.aether.debug is True
	def debug_print(self,output):
		if self.settings.aether.debug: print output

	#Helper method for obtaining the full list of search directories
	def search_dirs(self):
		#Start with the directories specified in settings
		search_dirs=self.settings.aether.dirs

		#Append system directories
		search_dirs.extend([aether.base_dir+os.sep+name for name in self.system_dirs])

		return search_dirs

	#Helper method for obtaining the full path to a resource
	#This method searches through all known data directory paths for the given file name
	#If the file is found, the string for the full path to that file is returned
	#Otherwise an AetherIOError is raised
	def file_path(self,filename):
		self.debug_print("Searching data directories for file '%s'..."%(filename))

		#Search the directories
		for search_dir in self.search_dirs():
			file_path=self._search_for_file(filename,search_dir)
			if file_path is not None: break

		#Raise an AetherIOError if the file was not found
		if file_path is None:
			raise AetherIOError("Error: The file '%s' was not found in any of the known directories (%s)"%(filename,search_dirs))

		#Return the path to the file
		return file_path

	#Searches the given directory for the given file name
	def _search_for_file(self,filename,search_dir):
		self.debug_print("Searching data directory '%s' for file '%s'..."%(search_dir,filename))
		full_path=search_dir+os.sep+filename
		if os.path.isfile(full_path):
			self.debug_print("Found path '%s'..."%(full_path))
			return full_path
		else:
			return None

	#Helper method for updating the module path (sys.path)
	#This method appends each directory in aether.dirs to sys.path
	#Additionally, it adds dirs named in AetherObject.system_dirs to sys.path
	def update_path(self):
		self.debug_print('Updating sys.path with additional directories...')

		#Append each new_dir to sys.path
		for new_dir in self.search_dirs():
			self.debug_print("Appending directory '%s' to sys.path..."%(new_dir))
			sys.path.append(new_dir)
