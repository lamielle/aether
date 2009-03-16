from __future__ import with_statement
import os,yaml

class Settings(object):
	#Dummy class for storing settings section values
	class values(object): pass

	#Default settings file
	settings_file_default='.aether_settings'
	debug_default=False

	#Non-settings fields
	_non_settings_fields=('loaded','saved')

	def __init__(self,settings_dict):
		#Initially we set loaded/saved to successful
		self.loaded=True
		self.saved=True

		#Set some default settings values
		self.load_defaults()

		#Load the debug value, if present
		self.load_debug(settings_dict)

		#Load the settings in the given dictionary
		self.load_from_dict(settings_dict)

		#Load from a settings file
		self.load()

	def __getattr__(self,item):
		#Check if this item already exists
		if item not in Settings._non_settings_fields and not self.__dict__.has_key(item):
			#Create an empty values object if it is not in the Settings._non_settings_fields collection if it does not exist
			self.__dict__[item]=Settings.values()

		#Now do the default operation
		return object.__getattribute__(self,item)

	#String representation from a YAML dump
	def __str__(self):
		return yaml.dump(self.get_settings_dict(),default_flow_style=False).strip()

	#Attempts to load from the setting aether.settings_file if this file exists
	#If this file does not exist, this method does nothing
	#If this file does exist, it attempts to load the file as a YAML Aether settings file
	#self.load is set to True if loading was successful and False otherwise
	#Success is defined as the file not existing or loading the file successfully
	def load(self):
		#Assume success in loading from the start
		self.loaded=True

		#Load the settings file if one is specified and and if it exists
		#Relys on short-circuited 'and' operator as isfile dies if None is passed as its argument
		if None!=self.aether.settings_file and os.path.isfile(self.aether.settings_file):
			if self.aether.debug: print "Loading settings from file '%s'..."%(self.aether.settings_file)

			#Attempt to load the Aether YAML settings file aether.settings_file
			try:
				with file(self.aether.settings_file,'r') as f:
					settings=yaml.load(f)
			except TypeError,e:
				print "Error: Cannot load Aether YAML settings file '%s', please make sure this is a valid Aether YAML settings file (Exception: %s)."%(self.aether.settings_file,e)
				self.loaded=False
			except yaml.scanner.ScannerError,e:
				print "Error: Invalid Aether YAML settings file syntax in file '%s' (Exception: %s)."%(self.aether.settings_file,e)
				self.loaded=False

			#Only try to load the values from 'settings' if loading was successful
			if self.loaded:
				self.load_from_dict(settings)

	#Set aether.{settings_file,debug} to default values
	def load_defaults(self):
		self.aether.settings_file=Settings.settings_file_default
		self.aether.debug=Settings.debug_default

	#Attempts to load the aether.debug setting value
	#This was added to make sure debugging is setup before any other code that may need it is run
	def load_debug(self,settings_dict):
		if settings_dict.has_key('aether'):
			if settings_dict['aether'].has_key('debug'):
				self.aether.debug=settings_dict['aether']['debug']

	#Populate fields of 'self' using the entries in the given dictionary
	#This dictionary should be a 'dictionary of dictionaries', where the keys
	#are strings that represent the section and setting name.
	def load_from_dict(self,settings_dict):
		try:
			for section,values in settings_dict.items():
				if self.aether.debug: print "Found Section '%s':"%(section)
				try:
					for name,value in values.items():
						setattr(getattr(self,section),name,value)
						if self.aether.debug: print "|-Found value: %s: %s (%s)"%(name,repr(value),type(value))
				except AttributeError,e:
					print "Error: Incorrect settings dictionary format: All sections must map to a Python dictionary (Exception: %s)."%(e)
					self.loaded=False
		except AttributeError,e:
			print "Error: The given settings_dict object is not a dictionary (Exception: %s)."%(e)
			self.loaded=False

	#Save the current settings in this Settings object to the file specified in aether.settings_file
	def save(self):
		#Assume success in saving from the start
		self.saved=True

		if self.aether.debug: print "Writing settings to file '%s'..."%(self.aether.settings_file)

		try:
			#Get a dictionary containing the current settings
			settings=self.get_settings_dict()

			#Write the dictionary to the file aether.settings_file in YAML format
			with file(self.aether.settings_file,'w') as f:
				yaml.dump(settings,f,default_flow_style=False)

			if self.aether.debug: print "Wrote settings to file '%s'..."%(self.aether.settings_file)
			if self.aether.debug: print yaml.dump(settings,default_flow_style=False)
		except IOError,e:
			print "Error: Unable to open Aether YAML settings file '%s' for writing (Exception: %s)"%(self.aether.settings_file,e)
			self.saved=False
		except TypeError,e:
			print "Error: Cannot save to Aether YAML settings file '%s' (Exception: %s)."%(self.aether.settings_file,e)
			self.saved=False

	#Create a settings dictionary from the fields of this Settings object
	def get_settings_dict(self):
		settings={}
		for section,values in self.__dict__.items():
			#Fields named in Settings._non_settings_fields should not be treated as settings values
			if section not in Settings._non_settings_fields:
				settings[section]={}
				for name,value in values.__dict__.items():
					settings[section][name]=value
		return settings
