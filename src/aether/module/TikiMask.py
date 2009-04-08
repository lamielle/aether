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

class TikiMask(AetherModule):

	#Chains this module needs
	chains={'camera':'ScaledCameraChain','faces':'FacesChain'}

	def init(self):
		# load our image, this will look in the directory where the file is executed
		self.tiki=pygame.image.load(self.file_path('tiki.png'))

		# make any white in the image transparent
		self.tiki.set_colorkey(THECOLORS["white"])

	def draw(self,screen):
		#Get the current frame
		capture=self.camera.read()

		#Blit it to the screen
		screen.blit(capture,(0,0))

		#For each detected face:
		for face in self.faces.read():
			#Calculate the face's dimensions
			width=face[1][0]-face[0][0]
			height=face[2][1]-face[1][1]

			#Scale the original image onto a new surface
			scaled_tiki=pygame.transform.scale(self.tiki,(width,height))

			#Blit the surface to the screen
			screen.blit(scaled_tiki,face[0])
