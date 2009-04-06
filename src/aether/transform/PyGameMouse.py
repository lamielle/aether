'''
Provides a set of points based on the location of the mouse.  The shape of the points returned by read() is a setting, defaults to a square

read() result: list of lists of vertices

:Author: Adam Labadorf
'''

from opencv import cv
from aether.core import AetherTransform
import pygame.mouse

class PyGameMouse(AetherTransform):

	input_names=('input',)
	defaults={'shape':'square','verts':[]}

	def read(self):
		if self.shape == 'custom' :
			shape = self.verts
		else :
			shape = [(-5,-5),(5,-5),(5,5),(-5,5)]

		pos = pygame.mouse.get_pos()

		return [[(x[0]+pos[0],x[1]+pos[1]) for x in shape]]
