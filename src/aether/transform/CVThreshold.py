'''
Transform that uses the OpenCV cvCvtColor function to convert between different color spaces.

read() result: New image converted using the conversion constant specified with the convert_method setting value.

:Author: Alan LaMielle
'''

from opencv import cv
from aether.core import AetherTransform

class CVThreshold(AetherTransform):

	input_names=('input',)
	defaults={'channels':range(3),'thresholds':[0]*4,'max_thresholds':[255]*4,'type':cv.CV_THRESH_BINARY,'enabled':True}

	def read(self):
		frame=self.input.read()
		if self.enabled:

			cv_rs = [None]*4
			cv_thresh = [0]*4
			cv_max = [255]*4

			for i in self.channels :
				cv_rs[i] = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1)
				cv_thresh[i] = self.thresholds[i]
				cv_max[i] = self.max_thresholds[i]

			# extract the color channel
			cv.cvSplit(frame,cv_rs[0],cv_rs[1],cv_rs[2],cv_rs[3])

			#self.debug_print(cv_rs)
			for i in self.channels :
				cv.cvThreshold(cv_rs[i],cv_rs[i],cv_thresh[i],cv_max[i],self.type)

			#cv_thresh = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,3)
			cv.cvZero(frame)
			cv.cvMerge(cv_rs[0],cv_rs[1],cv_rs[2],cv_rs[3],frame)

			#frame = cv_thresh
		return frame
