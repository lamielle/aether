'''
Transform that reads cvMat images flips them using cvFlip.
The flipping is done using the flip_mode setting.
See OpenCV docs for what values of this argument mean.

If the enabled setting is False, this transform is equivalent to the identity.

read() result: a flipped cvMat

:Author: Alan LaMielle
'''

from opencv import cv
from aether.core import AetherTransform

class CVFlip(AetherTransform):

	#Default values for settings this transform needs
	defaults={'flip_mode':1,'enabled':True}

	#Names of inputs this transform expects
	input_names=('input',)

	def read(self):
		'''Flip the cvMat obtained from input using the flip_mode setting'''
		flip=self.input.read()
		if self.enabled:
			cv.cvFlip(flip,None,self.flip_mode)
		return flip
