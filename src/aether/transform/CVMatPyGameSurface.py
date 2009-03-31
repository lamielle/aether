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

		#This is assuming an OpenCV camera backend
		#In the future, it would be nice to be able to change out the camera backend

		# scale the image to size of the window
#		cvt_scale = cv.cvCreateImage(cv.cvSize(self.capture_dims[0],self.capture_dims[1]),frame.depth,frame.nChannels)
#		cv.cvResize(frame,cvt_scale,cv.CV_INTER_LINEAR)

		# need to convert the colorspace differently depending on where the image came from
#		cvt_color = cv.cvCreateImage(cv.cvSize(cvt_scale.width,cvt_scale.height),cvt_scale.depth,3)
#		if frame.nChannels == 3 : # image is BGR
			# frame is in BGR format, convert it to RGB so the sky isn't orange
#			cv.cvCvtColor(cvt_scale,cvt_color,cv.CV_BGR2RGB)
#		elif frame.nChannels == 1 : # image is grayscale
			# frame is grayscale
#			cv.cvCvtColor(cvt_scale,cvt_color,cv.CV_GRAY2RGB)

		# create a pygame surface
		frame_surface=pygame.image.frombuffer(frame.imageData,(frame.width,frame.height),'RGB')

		return frame_surface
