class AetherCameraError(Exception):
	"""AetherCameraError is an exception that is raised during exceptional cases while working with a camera"""

	def __init__(self,*args,**kwargs):
		Exception.__init__(self,*args,**kwargs)
