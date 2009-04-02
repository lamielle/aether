'''
Transform that uses the OpenCV cvCvtColor function to convert between different color spaces.

read() result: New image converted using the conversion constant specified with the convert_method setting value.

:Author: Alan LaMielle
'''

from opencv import cv
from aether.core import AetherTransform

class CVTColor(AetherTransform):

	input_names=('input',)
	defaults={'convert_method':cv.CV_BGR2RGB,'enabled':True}

	def read(self):
		frame=self.input.read()
		if self.enabled:
			cv.cvCvtColor(frame,frame,self.convert_method)
		return frame
