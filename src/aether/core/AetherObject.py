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
	#Item search order:
	#1) The object's fields
	#2) The settings.(self.name) category
	#3) The settings.aether category
	#
	#The idea here is to search fields in order from 'most local' to 'most global'
	def __getattr__(self,item):
		try:
			res=object.__getattribute__(self,item)
		except AttributeError as e:
			try:
				res=getattr(getattr(self.settings,self.__dict__['name']),item)
			except (KeyError,AttributeError) as e:
				res=getattr(getattr(self.settings,'aether'),item)
		return res

	#Helper method for setting settings values
	#section: Name of the settings section
	#name: Name of the value to set
	#value: Value to set
	#test_exist: If True, the value will only be set if the settings value does not already exist
	def settings_set(self,section_name,value_name,value,test_exist=False):
		#Get the specified settings section
		settings_section=getattr(self.settings,section_name)

		#Determine if the settings value exists
		exists=hasattr(settings_section,value_name)

		#Set the value if we are not testing for existence or if the value does not exist
		if not test_exist or not exists:
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
