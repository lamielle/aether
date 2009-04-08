'''
Transform that provides methods for getting the coordinates of laser points in an captured image.

read() result: The image it is passed without modification
get_points(): returns coordinates of the laser points

:Author: Adam Labadorf
'''

from opencv import cv
from aether.core import AetherTransform
import pygame

class DebugShadowPolys(AetherTransform):

	input_names=('thresh2pg','camera','shadow',)
	defaults={}

	def read(self):
		src = self.camera.read()
		thresh = self.thresh2pg.read()
		polys = self.shadow.read()

		return src,thresh,polys

