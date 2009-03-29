import os,sys
import aether
from aether.error import AetherIOError

class AetherObject(object):
	"""Base class for all Aether related classes.

	AetherObject provides some common methods and data to objects in the Aether system."""

	#Global Aether settings
	settings=None

	def __init__(self): pass

	#Modified getattr:
	#First searches settings.aether for the item
	#then searches settings.(self.name) for the item
	def __getattr__(self,item):
		try:
			res=getattr(getattr(self.settings,'aether'),item)
		except AttributeError,e:
			try:
				res=getattr(getattr(self.settings,self.__dict__['name']),item)
			except AttributeError,e:
				res=object.__getattribute__(self,item)
		return res

	#Helper method for debug printing
	#Will print only if self.settings.aether.debug is True
	def debug_print(self,output):
		if self.settings.aether.debug: print output

	#Helper method for obtaining the full path to a resource
	#This method searches through all known data directory paths for the given file name
	#If the file is found, the string for the full path to that file is returned
	#Otherwise an AetherIOError is raised
	def file_path(self,filename):
		self.debug_print("Searching data directories for file '%s'..."%(filename))

		#Get the full collection of directories to search
		search_dirs=self.settings.aether.dirs+[aether.base_dir+os.sep+'data']

		#Search the directories
		for search_dir in search_dirs:
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
	#Additionally, it adds aether.base_dir/{modules,input} to sys.path
	def update_path(self):
		self.debug_print('Updating sys.path with additional directories...')

		#Get the full list of directories to add to sys.path
		new_dirs=self.settings.aether.dirs+[aether.base_dir+os.sep+'modules',aether.base_dir+os.sep+'input']

		#Append each new_dir to sys.path
		for new_dir in new_dirs:
			self.debug_print("Appending directory '%s' to sys.path..."%(new_dir))
			sys.path.append(new_dir)
