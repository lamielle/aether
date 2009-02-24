"""
This example uses the :class:FaceInputProvider class, which does Haar Cascade Face Detection to return the rectangular coordinates of where OpenCV thinks it sees a face.

:Version: 1.0 of 2/24/2009 00:33 in the AM
:Author: Adam Labadorf
"""
from aether.core import AetherDriver, FaceInputProvider, AetherModule

import pygame.image
from pygame.color import THECOLORS
import pygame.transform

class TikiModule(AetherModule) :

	def __init__(self,*args) :
		# need to call parent class' init method explicitly in python
		AetherModule.__init__(self,*args)

		# load our image, this will look in the directory where the file is executed
		self.tiki = pygame.image.load("tiki.png")

		# make any white in the image transparent
		self.tiki.set_colorkey(THECOLORS["white"])


	def draw(self,screen) :
		# get the current frame
		raw_image = self.input.get_curr_frame()

		# scale incoming image to the driver screen size and blit it to the screen
		scaled_raw_image = pygame.transform.scale(raw_image,self.dims)
		screen.blit(scaled_raw_image,(0,0))

		# get the rectangle of the biggest face the input provider can find
		face = self.input.get_verts()

		# if it found a face, draw the mask
		if face is not None :
			# figure out the face's dimensions
			width, height = face[1][0]-face[0][0], face[2][1]-face[1][1]

			# scale the original image onto a new surface and draw to the screen
			scaled_tiki = pygame.transform.scale(self.tiki,(width,height))
			screen.blit(scaled_tiki,face[0])

if __name__ == "__main__" :

	# initialize a FaceInputProvider that looks for faces from the camera image
	face_input = FaceInputProvider("/home/labadorf/development/facedetect/haarcascade_frontalface_alt.xml",flip=True)

	# create the driver
	driver = AetherDriver(640,input=face_input)

	# register the module we just wrote
	driver.register_module(TikiModule(driver))

	# go be a tiki god
	driver.run()
