from __future__ import with_statement
import yaml

class Settings(object):
	#Dummy class for storing settings section values
	class values(object): pass

	#Non-settings fields
	_non_settings=('debug','loaded','saved')

	def __init__(self,file_name=None,debug=False):
		self.debug=debug
		self.loaded=False
		self.saved=False

		#Load the given file name if one was given
		if None!=file_name: self.load(file_name)

	def __str__(self):
		return yaml.dump(self._get_settings_dict(),default_flow_style=False)

	def save(self,file_name):
		if self.debug: print "Writing settings to file '%s'...\n"%(file_name)

		try:
			#Get a dictionary containing the current settings
			settings=self._get_settings_dict()

			#Write the given dictionary to the given file in YAML format
			with file(file_name,'w') as f:
				yaml.dump(settings,f,default_flow_style=False)

			if self.debug: print "Wrote settings to file '%s'..."%(file_name)
			if self.debug: print yaml.dump(settings,default_flow_style=False)
		except TypeError,e:
			print "Error: Cannot save to Aether YAML settings file '%s' (Exception: %s)."%(file_name,e)

	def load(self,file_name):
		#Assume success in loading from the start
		self.loaded=True

		if self.debug: print "Loading settings from file '%s'...\n"%(file_name)

		#Attempt to load the given file
		try:
			with file(file_name,'r') as f:
				settings=yaml.load(f)
		except TypeError,e:
			print "Error: Cannot load YAML file '%s', please make sure this is a valid Aether YAML settings file (Exception: %s)."%(file_name,e)
			self.loaded=False
		except yaml.scanner.ScannerError,e:
			print "Error: Invalid YAML syntax in file '%s' (Exception: %s)."%(file_name,e)
			self.loaded=False

		#Only try to load the values from 'settings' if loading was successful
		if self.loaded:
			self._set_settings_from_dict(settings)

	#Create a dictionary from the fields of 'self'
	def _get_settings_dict(self):
		settings={}
		for section,values in self.__dict__.items():
			#Fields named in self._non_settings should not be treated as settings values
			if section not in self._non_settings:
				settings[section]={}
				for name,value in values.__dict__.items():
					settings[section][name]=value
		return settings

	#Populate fields of 'self' using the entries in the given dictionary
	def _set_settings_from_dict(self,settings_dict):
		try:
			for section,values in settings_dict.items():
				if self.debug: print "Found Section '%s':"%(section)
				setattr(self,section,Settings.values())
				try:
					for name,value in values.items():
						setattr(getattr(self,section),name,value)
						if self.debug: print "|-Found value: %s: %s (%s)"%(name,repr(value),type(value))
				except AttributeError,e:
					print "Error: Incorrect settings file format: All YAML name/value pairs must specify a Python dictionary (Exception: %s)."%(e)
					self.loaded=False
		except AttributeError,e:
			print "Error: Incorrect settings file format: All YAML settings sections must specify a Python dictionary (Exception: %s)."%(e)
			self.loaded=False
