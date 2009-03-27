class AetherModuleLoadError(Exception):
	"""AetherModuleLoaderror is an exception that is raised during exceptional cases while loading modules"""

	def __init__(self,*args,**kwargs):
		Exception.__init__(self,*args,**kwargs)
