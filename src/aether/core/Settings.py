from __future__ import with_statement
from ConfigParser import ConfigParser

class Settings(object):
	__slots__=('threshold','transform','min_area')

	#Settings section/value names
	_settings_section='Input Settings'
	_setting_threshold='threshold'
	_setting_transform='transform'
	_setting_min_area='min_area'

	def __init__(self,threshold=0,transform=None,min_area=0):
		self.threshold=threshold
		self.transform=[] if None is transform else transform
		self.min_area = min_area

	def save(self,file_name):
		config=ConfigParser()
		config.add_section(self._settings_section)
		config.set(self._settings_section,self._setting_threshold,self.threshold)
		config.set(self._settings_section,self._setting_transform,self.transform)
		config.set(self._settings_section,self._setting_min_area,self.min_area)
		with file(file_name,'w') as f:
			config.write(f)

	def load(self,file_name):
		config=ConfigParser()
		config.read(file_name)
		self.threshold=int(config.get(self._settings_section,self._setting_threshold))
		self.transform=eval(config.get(self._settings_section,self._setting_transform))
		self.min_area=int(config.get(self._settings_section,self._setting_min_area))
