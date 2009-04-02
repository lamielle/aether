'''
Transform that resizes the given OpenCV image (cvMat) using the new_size settings value for the new size of the image and interplation_method as the method for doing the resizing interpolation

read() result: a new OpenCV image (cvMat) resized to the specified dimensions

:Author: Alan LaMielle
'''

from opencv import cv
from aether.core import AetherTransform

class CVResize(AetherTransform):

	input_names=('input',)
	defaults={'new_size':(640,480),'interplation_method':cv.CV_INTER_LINEAR}

	def read(self):
		frame=self.input.read()
		scaled_frame=cv.cvCreateImage(cv.cvSize(self.new_size[0],self.new_size[1]),frame.depth,frame.nChannels)
		cv.cvResize(frame,scaled_frame,self.interplation_method)
		return scaled_frame
