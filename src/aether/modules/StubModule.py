import pygame
from pygame.color import THECOLORS
from aether.core import AetherModule

class StubModule(AetherModule) :
	"""Stub module that simply draws a point for the center of mass and a polygon for vertices
	"""

	def __init__(self, driver, **kwargs) :
		#Initalize parent class
		AetherModule.__init__(self,driver,**kwargs)

	def draw(self,screen) :
		screen.fill(THECOLORS["lightblue"])
		#Draw the center of mass
		com=self.input.get_com()
		if com is not None : pygame.draw.circle(screen,THECOLORS["white"],com,5)

		#Draw a polygon
		points = self.input.get_verts()
		if points is not None : pygame.draw.polygon(screen,THECOLORS["red"],points,2)
