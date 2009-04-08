'''
Transform that uses the OpenCV cvCvtColor function to convert between different color spaces.

read() result: New image converted using the conversion constant specified with the convert_method setting value.

:Author: Alan LaMielle
'''

from opencv import cv
from aether.core import AetherTransform

class CVTColor(AetherTransform):

	input_names=('input',)
	defaults={'convert_method':cv.CV_BGR2RGB,'num_channels':3,'enabled':True}

	def read(self):
		frame=self.input.read()
		if self.enabled:
			if self.num_channels==frame.nChannels:
				new_frame=frame
			else:
				new_frame=cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,self.num_channels)
			cv.cvCvtColor(frame,new_frame,self.convert_method)
			if self.num_channels == 1:
				cv.cvMerge(new_frame,new_frame,new_frame,None,frame)
			else :
				frame=new_frame

		return frame
