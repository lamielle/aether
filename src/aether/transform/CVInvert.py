'''
Inverts the read image using cvSubRS, only works on 1 channel images

read() result: inverted 1 channel image

:Author: Adam Labadorf
'''

from opencv import cv
from aether.core import AetherTransform

class CVInvert(AetherTransform):

	input_names=('input',)
	defaults={'enabled':True}

	def read(self):
		frame=self.input.read()
		if self.enabled:
			cv.cvSubRS(frame, cv.cvRealScalar(255), frame)
		return frame
