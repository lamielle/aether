from aether.core import InputProvider
from pygame.mouse import get_pos

class MouseInputProvider(InputProvider):

	def __init__(self,*args) :
		pass

	def get_com(self) :
		return get_pos()	

	def get_verts(self) :
		return [get_pos()]

	def get_polys(self) :
		return [get_pos()]
