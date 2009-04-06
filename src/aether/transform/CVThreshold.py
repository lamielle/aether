'''
Transform that uses the OpenCV cvCvtColor function to convert between different color spaces.

read() result: New image converted using the conversion constant specified with the convert_method setting value.

:Author: Alan LaMielle
'''

from opencv import cv
from aether.core import AetherTransform

class CVThreshold(AetherTransform):

	input_names=('input',)
	defaults={'threshold':0,'max_threshold':255,'type':cv.CV_THRESH_BINARY,'enabled':True}

	def read(self):
		frame=self.input.read()
		if self.enabled:
			cv_thresh = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1)
			cv.cvThreshold(frame,cv_thresh,self.threshold,self.max_threshold,self.type)
			frame = cv_thresh
		return frame
