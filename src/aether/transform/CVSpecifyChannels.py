'''
Transform that extracts the desired channels out of a CV image

read() result: New 3 channel image containing only the channel(s) from the read image specified
in the settings.channels list

:Author: Adam Labadorf
'''

from opencv import cv
from aether.core import AetherTransform

class CVSpecifyChannels(AetherTransform):

	input_names=('input',)
	defaults={'channels':[0]}

	def read(self):
		frame = self.input.read()

		# image we'll eventually return

		# which channels to combine
		cv_rs = [None]*4

		# if frame only has one channel, just return it
		if frame.nChannels == 1 :
			for i in self.channels :
				cv_rs[i] = frame
		else :
			for i in self.channels :
				cv_rs[i] = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1)

			# extract the color channel
			cv.cvSplit(cv_rs[0],cv_rs[1],cv_rs[2],cv_rs[3],cvt_im)

		cvt_im = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,3)
		cv.cvMerge(cv_rs[0],cv_rs[1],cv_rs[2],cv_rs[3],cvt_im)

		return cvt_im
