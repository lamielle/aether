'''
Transform that converts from a cvMat (image) to a PyGame surface.

read() result: a pygame surface of the same size as its input

:Author: Alan LaMielle
'''

import pygame
from aether.core import AetherTransform

class CVMatPyGameSurface(AetherTransform):

	#Names of the inputs to this transform
	input_names=('input',)

	def read(self):
		'''Capture the current frame from the camera and return it as a pyGame surface'''

		#Read the current frame from the flipped camera
		frame=self.input.read()

		# create a pygame surface
		frame_surface=pygame.image.frombuffer(frame.imageData,(frame.width,frame.height),'RGB')

		return frame_surface
