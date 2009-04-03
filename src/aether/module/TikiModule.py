"""
This example uses the :class:FaceInputProvider class, which does Haar Cascade Face Detection to return the rectangular coordinates of where OpenCV thinks it sees a face.

Updated to use new transforms API

:Version: 1.1 of 4/2/2009
:Author: Adam Labadorf and Alan LaMielle
"""
from aether.core import AetherModule

import pygame.image
from pygame.color import THECOLORS
import pygame.transform

class TikiModule(AetherModule):

	#Chains this module needs
	chains={'camera':'ScaledCameraChain','face':'BiggestFaceChain'}

	def __init__(self):
		# load our image, this will look in the directory where the file is executed
		self.tiki=pygame.image.load(self.file_path('tiki.png'))

		# make any white in the image transparent
		self.tiki.set_colorkey(THECOLORS["white"])

	def draw(self,screen):
		# get the current frame
		capture=self.camera.read()

		# blit it to the screen
		screen.blit(capture,(0,0))

		# get the rectangle of the biggest face the input provider can find
		face=self.face.read()

		# if it found a face, draw the mask
		if face is not None:

			# face.read() returns coordinates normalized to [0,1], scale it to curr dimensions
			face=[(int(x[0]*self.dims[0]),int(x[1]*self.dims[1])) for x in face]

			# figure out the face's dimensions
			width,height=face[1][0]-face[0][0],face[2][1]-face[1][1]

			# scale the original image onto a new surface and draw to the screen
			scaled_tiki=pygame.transform.scale(self.tiki,(width,height))
			screen.blit(scaled_tiki,face[0])
