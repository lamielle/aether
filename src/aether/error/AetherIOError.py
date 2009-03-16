class AetherIOError(Exception):
	"""AetherIOError is an exception that is raised during exceptional cases while doing IO operations"""

	def __init__(self,*args,**kwargs):
		Exception.__init__(self,*args,**kwargs)
