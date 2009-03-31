'''
Transform that reads cvMat images flips them.

read() result: a flipped cvMat

:Author: Alan LaMielle
'''

from opencv import cv
from aether.core import AetherTransform

class CVFlip(AetherTransform):

	#Names of inputs this transform expects
	input_names=('input',)

	def read(self):
		'''Capture the current frame from the camera and flip it'''

		#Read the current frame from the camera wrapper
		frame=self.input.read()
		cv.cvFlip(frame,None,1)
		return frame
