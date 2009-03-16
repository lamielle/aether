import os
from aether.error import AetherIOError

class AetherObject(object):
	"""Base class for all Aether related classes.

	AetherObject provides some common methods and data to objects in the Aether system."""

	#Global Aether settings
	settings=None

	def __init__(self): pass

	#Helper method for debug printing
	#Will print only if self.settings.aether.debug is True
	def debug_print(self,output):
		if self.settings.aether.debug: print output

	#Helper method for obtaining the full path to a resource
	#This method searches through all known data directory paths for the given file name
	#If the file is found, the string for the full path to that file is returned
	#Otherwise an AetherIOError is raised
	def get_file_path(self,filename):
		self.debug_print("Searching data directories for file '%s'..."%(filename))
		for data_dir in self.settings.aether.data_dirs:
			self.debug_print("Searching data directory '%s' for file '%s'..."%(data_dir,filename))
			full_path=data_dir+os.sep+filename
			if os.path.isfile(full_path):
				self.debug_print("Found path '%s'..."%(full_path))
				return full_path

		raise AetherIOError("Error: The file '%s' was not found in any of the directories specified in settings value aether.data_dirs (%s)"%(filename,self.settings.aether.data_dirs))
